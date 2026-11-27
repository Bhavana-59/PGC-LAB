
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cuda_runtime.h>

#define TILE 32
#define BLK 16

// CUDA error checking macro
#define CHECK(call) do { \
    cudaError_t cudaStatus = (call); \
    if (cudaStatus != cudaSuccess) { \
        fprintf(stderr, "CUDA error: %s (%s:%d)\n", \
                cudaGetErrorString(cudaStatus), __FILE__, __LINE__); \
        exit(1); \
    } \
} while (0)

// ------------------------------------------
// 1. Uncoalesced Matrix Transpose
// ------------------------------------------
__global__ void transposeNaive(
    const float *in, float *out, int N)
{
    int x = blockIdx.x * TILE + threadIdx.x;
    int y = blockIdx.y * TILE + threadIdx.y;

    if (x < N && y < N)
        out[x * N + y] = in[y * N + x];
}

// ------------------------------------------
// 2. Coalesced Matrix Transpose
// ------------------------------------------
__global__ void transposeCoalesced(
    const float *in, float *out, int N)
{
    __shared__ float tile[TILE][TILE + 1];

    int x = blockIdx.x * TILE + threadIdx.x;
    int y = blockIdx.y * TILE + threadIdx.y;

    if (x < N && y < N)
        tile[threadIdx.y][threadIdx.x] =
            in[y * N + x];

    __syncthreads();

    x = blockIdx.y * TILE + threadIdx.x;
    y = blockIdx.x * TILE + threadIdx.y;

    if (x < N && y < N)
        out[y * N + x] =
            tile[threadIdx.x][threadIdx.y];
}

// ------------------------------------------
// 3. Naive Matrix Multiplication
// ------------------------------------------
__global__ void matMulNaive(
    const float *A,
    const float *B,
    float *C,
    int N)
{
    int row = blockIdx.y * BLK + threadIdx.y;
    int col = blockIdx.x * BLK + threadIdx.x;

    if (row < N && col < N) {
        float sum = 0.0f;

        for (int k = 0; k < N; k++)
            sum += A[row * N + k] *
                   B[k * N + col];

        C[row * N + col] = sum;
    }
}

// ------------------------------------------
// 4. Kernel Function Pointer
// ------------------------------------------
typedef void (*TKernel)(
    const float *, float *, int);

// ------------------------------------------
// 5. Transpose Timing Function
// ------------------------------------------
float timeTranspose(
    TKernel k,
    dim3 g,
    dim3 b,
    const float *in,
    float *out,
    int N,
    int reps)
{
    cudaEvent_t startEvent, stopEvent;

    CHECK(cudaEventCreate(&startEvent));
    CHECK(cudaEventCreate(&stopEvent));

    CHECK(cudaMemset(
        out, 0,
        (size_t)N * N * sizeof(float)));

    // Warm-up launch
    k<<<g, b>>>(in, out, N);

    CHECK(cudaGetLastError());
    CHECK(cudaDeviceSynchronize());

    CHECK(cudaEventRecord(startEvent));

    // Timed launches
    for (int r = 0; r < reps; r++)
        k<<<g, b>>>(in, out, N);

    CHECK(cudaEventRecord(stopEvent));
    CHECK(cudaEventSynchronize(stopEvent));

    float ms;

    CHECK(cudaEventElapsedTime(
        &ms, startEvent, stopEvent));

    CHECK(cudaEventDestroy(startEvent));
    CHECK(cudaEventDestroy(stopEvent));

    return ms / reps;
}

// ------------------------------------------
// 6. Transpose Correctness Verification
// ------------------------------------------
bool checkTranspose(
    const float *in,
    const float *out,
    int N)
{
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            if (out[j * N + i] !=
                in[i * N + j])
                return false;
        }
    }

    return true;
}

// ------------------------------------------
// 7. Matrix Multiplication Verification
// ------------------------------------------
bool checkMatMul(
    const float *A,
    const float *B,
    const float *C,
    int N)
{
    for (int t = 0; t < 20; t++) {
        int i = rand() % N;
        int j = rand() % N;

        double ref = 0.0;

        for (int k = 0; k < N; k++)
            ref += (double)A[i * N + k] *
                   B[k * N + j];

        if (fabs(ref - C[i * N + j]) >
            1e-3 * fabs(ref) + 1e-3)
            return false;
    }

    return true;
}




int main(int argc, char *argv[])
{
    // Default matrix sizes
    int NT = 4096;
    int NM = 1024;

    if (argc >= 2)
        NT = atoi(argv[1]);

    if (argc >= 3)
        NM = atoi(argv[2]);

    if (NT <= 0 || NM <= 0) {
        printf("Matrix sizes must be positive.\n");
        return 1;
    }

    srand(1234);

    printf("\n====================================\n");
    printf(" CUDA EXPERIMENT 6\n");
    printf(" Memory Optimization\n");
    printf("====================================\n");

    // ----------------------------------
    // GPU Information
    // ----------------------------------
    int device = 0;
    cudaDeviceProp prop;

    CHECK(cudaGetDevice(&device));
    CHECK(cudaGetDeviceProperties(&prop, device));

    printf("\nGPU Information\n");
    printf("------------------------------------\n");
    printf("GPU Name          : %s\n", prop.name);
    printf("Compute Capability: %d.%d\n",
           prop.major, prop.minor);
    printf("Global Memory     : %.2f GB\n",
           prop.totalGlobalMem / (1024.0 * 1024.0 * 1024.0));

    // ==================================
    // EXPERIMENT 1: MATRIX TRANSPOSE
    // ==================================

    printf("\n====================================\n");
    printf(" EXPERIMENT 1: MATRIX TRANSPOSE\n");
    printf("====================================\n");

    size_t bytesT =
        (size_t)NT * NT * sizeof(float);

    float *h_in = (float *)malloc(bytesT);
    float *h_naive = (float *)malloc(bytesT);
    float *h_coalesced = (float *)malloc(bytesT);

    float *d_in = nullptr;
    float *d_out = nullptr;

    if (!h_in || !h_naive || !h_coalesced) {
        printf("Host memory allocation failed.\n");
        return 1;
    }

    // Initialize input matrix
    for (size_t i = 0; i < (size_t)NT * NT; i++)
        h_in[i] = (float)(i % 1000);

    CHECK(cudaMalloc((void **)&d_in, bytesT));
    CHECK(cudaMalloc((void **)&d_out, bytesT));

    CHECK(cudaMemcpy(
        d_in, h_in, bytesT,
        cudaMemcpyHostToDevice));

    dim3 blockT(TILE, TILE);
    dim3 gridT(
        (NT + TILE - 1) / TILE,
        (NT + TILE - 1) / TILE);

    int repsT = 20;

    // Uncoalesced transpose
    float naiveTime = timeTranspose(
        transposeNaive,
        gridT, blockT,
        d_in, d_out,
        NT, repsT);

    CHECK(cudaMemcpy(
        h_naive, d_out, bytesT,
        cudaMemcpyDeviceToHost));

    bool naivePass =
        checkTranspose(h_in, h_naive, NT);

    // Coalesced transpose
    float coalescedTime = timeTranspose(
        transposeCoalesced,
        gridT, blockT,
        d_in, d_out,
        NT, repsT);

    CHECK(cudaMemcpy(
        h_coalesced, d_out, bytesT,
        cudaMemcpyDeviceToHost));

    bool coalescedPass =
        checkTranspose(h_in, h_coalesced, NT);

    // Effective bandwidth
    double dataGB =
        (2.0 * bytesT) / (1024.0 * 1024.0 * 1024.0);

    double naiveBW =
        dataGB / (naiveTime / 1000.0);

    double coalescedBW =
        dataGB / (coalescedTime / 1000.0);

    double transposeSpeedup =
        naiveTime / coalescedTime;

    printf("\nTranspose Results (N = %d)\n", NT);
    printf("------------------------------------\n");

    printf("Uncoalesced Time : %.4f ms\n",
           naiveTime);

    printf("Uncoalesced BW   : %.2f GB/s\n",
           naiveBW);

    printf("Uncoalesced Check: %s\n",
           naivePass ? "PASS" : "FAIL");

    printf("\nCoalesced Time   : %.4f ms\n",
           coalescedTime);

    printf("Coalesced BW     : %.2f GB/s\n",
           coalescedBW);

    printf("Coalesced Check  : %s\n",
           coalescedPass ? "PASS" : "FAIL");

    printf("\nTranspose Speedup: %.2fx\n",
           transposeSpeedup);

    // Release transpose memory
    CHECK(cudaFree(d_in));
    CHECK(cudaFree(d_out));

    free(h_in);
    free(h_naive);
    free(h_coalesced);

    // ==================================
    // EXPERIMENT 2: MATRIX MULTIPLICATION
    // ==================================

    printf("\n====================================\n");
    printf(" EXPERIMENT 2: MATRIX MULTIPLICATION\n");
    printf("====================================\n");

    size_t bytesM =
        (size_t)NM * NM * sizeof(float);

    float *h_A = (float *)malloc(bytesM);
    float *h_B = (float *)malloc(bytesM);
    float *h_C = (float *)malloc(bytesM);

    float *d_A = nullptr;
    float *d_B = nullptr;
    float *d_C = nullptr;

    if (!h_A || !h_B || !h_C) {
        printf("Host memory allocation failed.\n");
        return 1;
    }

    // Initialize matrices
    for (size_t i = 0; i < (size_t)NM * NM; i++) {
        h_A[i] = (float)(rand() % 10) / 10.0f;
        h_B[i] = (float)(rand() % 10) / 10.0f;
    }

    CHECK(cudaMalloc((void **)&d_A, bytesM));
    CHECK(cudaMalloc((void **)&d_B, bytesM));
    CHECK(cudaMalloc((void **)&d_C, bytesM));

    CHECK(cudaMemcpy(
        d_A, h_A, bytesM,
        cudaMemcpyHostToDevice));

    CHECK(cudaMemcpy(
        d_B, h_B, bytesM,
        cudaMemcpyHostToDevice));

    dim3 blockM(BLK, BLK);

    dim3 gridM(
        (NM + BLK - 1) / BLK,
        (NM + BLK - 1) / BLK);

    // Warm-up
    matMulNaive<<<gridM, blockM>>>(
        d_A, d_B, d_C, NM);

    CHECK(cudaGetLastError());
    CHECK(cudaDeviceSynchronize());

    // CUDA timing events
    cudaEvent_t startEvent, stopEvent;

    CHECK(cudaEventCreate(&startEvent));
    CHECK(cudaEventCreate(&stopEvent));

    int repsM = 5;

    CHECK(cudaEventRecord(startEvent));

    for (int r = 0; r < repsM; r++) {
        matMulNaive<<<gridM, blockM>>>(
            d_A, d_B, d_C, NM);
    }

    CHECK(cudaEventRecord(stopEvent));
    CHECK(cudaEventSynchronize(stopEvent));

    float matMulTime;

    CHECK(cudaEventElapsedTime(
        &matMulTime,
        startEvent,
        stopEvent));

    matMulTime /= repsM;

    CHECK(cudaEventDestroy(startEvent));
    CHECK(cudaEventDestroy(stopEvent));

    CHECK(cudaMemcpy(
        h_C, d_C, bytesM,
        cudaMemcpyDeviceToHost));

    bool matMulPass =
        checkMatMul(h_A, h_B, h_C, NM);

    double operations =
        2.0 * NM * NM * NM;

    double gflops =
        operations / (matMulTime * 1.0e6);

    printf("\nMatrix Multiplication Results (N = %d)\n",
           NM);

    printf("------------------------------------\n");

    printf("Execution Time : %.4f ms\n",
           matMulTime);

    printf("Performance    : %.2f GFLOPS\n",
           gflops);

    printf("Correctness    : %s\n",
           matMulPass ? "PASS" : "FAIL");

    // ==================================
    // FINAL SUMMARY
    // ==================================

    printf("\n====================================\n");
    printf(" FINAL EXPERIMENT SUMMARY\n");
    printf("====================================\n");

    printf("GPU              : %s\n", prop.name);

    printf("Transpose Naive  : %.4f ms\n",
           naiveTime);

    printf("Transpose Coalesced: %.4f ms\n",
           coalescedTime);

    printf("Transpose Speedup: %.2fx\n",
           transposeSpeedup);

    printf("Naive Matrix Mul : %.4f ms\n",
           matMulTime);

    printf("Matrix GFLOPS    : %.2f\n",
           gflops);

    printf("Naive Transpose  : %s\n",
           naivePass ? "PASS" : "FAIL");

    printf("Coalesced Transpose: %s\n",
           coalescedPass ? "PASS" : "FAIL");

    printf("Matrix Multiply  : %s\n",
           matMulPass ? "PASS" : "FAIL");

    printf("\n====================================\n");
    printf(" EXPERIMENT COMPLETED\n");
    printf("====================================\n");

    // Cleanup
    CHECK(cudaFree(d_A));
    CHECK(cudaFree(d_B));
    CHECK(cudaFree(d_C));

    free(h_A);
    free(h_B);
    free(h_C);

    CHECK(cudaDeviceReset());

    return 0;
}
