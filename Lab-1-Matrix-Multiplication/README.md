<<<<<<< HEAD

 Lab 1 — Matrix Multiplication using Sequential, OpenMP, MPI and CUDA

 Objective
=======
Lab 1 — Matrix Multiplication using Sequential, OpenMP, MPI and CUDA Objective
>>>>>>> 01c3c77 (Add complete Lab 1 matrix multiplication setup)

Implement matrix multiplication using different computational approaches and analyze their performance:

1. Sequential CPU
2. OpenMP shared-memory CPU
3. MPI distributed-memory CPU
4. CUDA GPU

The execution times of the different implementations are compared to understand the performance benefits of parallel computation.

---

 Problem Statement

Perform multiplication of two 4000 × 4000 matrices using sequential and parallel computing techniques.

Matrices A and B are initialized with 1.0 values. Therefore, every element of the resulting matrix C is expected to be:

C[i][j] = 4000.00


The same matrix multiplication problem is implemented using four different approaches:

* Sequential CPU
* OpenMP
* MPI
* CUDA

The execution time of each implementation is recorded for performance comparison.

---

## 1. Sequential Matrix Multiplication

The sequential implementation performs matrix multiplication using three nested loops.

* `i` selects the row of matrix A
* `j` selects the column of matrix B
* `k` performs the multiplication and summation

### Source Code

`matrix_sequential.c`

### Compilation

```bash
gcc -O2 matrix_sequential.c -o matrix_sequential
```

### Execution

```bash
./matrix_sequential
```

### Verification

Since all elements of matrices A and B are initialized to 1.0:

```text
C[0][0] = 4000.00
```

The result is verified by checking the computed matrix element.

### Evidence

| Screenshot                  | Description                                     |
| --------------------------- | ----------------------------------------------- |
| `01-gcc-version.jpeg`       | GCC compiler version                            |
| `02-source-code.jpeg`       | Sequential matrix multiplication source code    |
| `03-compilation.jpeg`       | Compilation of the sequential program           |
| `04-sequential-output.jpeg` | Program output, verification and execution time |

---

## 2. OpenMP Matrix Multiplication

The OpenMP implementation uses shared-memory parallelism to divide matrix multiplication work among multiple CPU threads.

The outer loop of matrix multiplication is parallelized using OpenMP.

### Source Code

`matrix_openmp.c`

### Compilation

```bash
gcc -O2 -fopenmp matrix_openmp.c -o matrix_openmp
```

### Execution

```bash
./matrix_openmp
```

### Verification

The result is verified using:

```text
C[0][0] = 4000.00
```

### Performance Measurement

The execution time is recorded and compared with the sequential implementation to observe the effect of CPU thread-level parallelism.

### Evidence

| Screenshot              | Description                                |
| ----------------------- | ------------------------------------------ |
| `06-openmp-output.jpeg` | OpenMP execution output and execution time |

---

## 3. MPI Matrix Multiplication

The MPI implementation uses distributed-memory parallelism.

The rows of matrix A are divided among multiple MPI processes. Each process performs matrix multiplication for its assigned rows and contributes to the final result.

### Source Code

`matrix_mpi.c`

### Compilation

```bash
mpicc -O2 matrix_mpi.c -o matrix_mpi
```

### Execution

The MPI program is executed using multiple processes. For example:

```bash
mpirun -np 4 ./matrix_mpi
```

### Verification

The result is verified using:

```text
C[0][0] = 4000.00
```

### Performance Measurement

The execution time is recorded for the MPI implementation and compared with the sequential and OpenMP implementations.

### Evidence

| Screenshot           | Description                                 |
| -------------------- | ------------------------------------------- |
| `07-mpi-output.jpeg` | MPI output, verification and execution time |

---

## 4. CUDA Matrix Multiplication

The CUDA implementation uses GPU parallelism to perform matrix multiplication.

The computation of individual elements of matrix C is assigned to CUDA threads. Multiple threads execute matrix multiplication operations concurrently on the GPU.

### Source Code

`matrix_cuda.cu`

### Compilation

```bash
nvcc -O2 matrix_cuda.cu -o matrix_cuda
```

### Execution

```bash
./matrix_cuda
```

### Verification

The result is verified using:

```text
C[0][0] = 4000.00
```

### Performance Measurement

The CUDA execution time is recorded and compared with the CPU-based implementations.

The GPU-based implementation demonstrates how massively parallel computation can be used for matrix multiplication.

### Evidence

| Screenshot                 | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| `12-nvidia-version.jpeg`   | NVIDIA/CUDA environment information                    |
| `13-cuda-source.jpeg`      | CUDA matrix multiplication source code                 |
| `14-cuda-compilation.jpeg` | CUDA compilation                                       |
| `15-cuda-output.jpeg`      | CUDA execution output, verification and execution time |

---

## 5. Performance Comparison

The execution times obtained from all four implementations are compared.

| Implementation | Processing Model     | Execution Time (seconds) |
| -------------- | -------------------- | -----------------------: |
| Sequential     | Single CPU thread    |                        — |
| OpenMP         | Multiple CPU threads |                        — |
| MPI            | Multiple processes   |                        — |
| CUDA           | GPU threads          |                        — |

Replace `—` with the actual execution time obtained from your experiments.

---

## Performance Analysis

The four implementations use different parallel computing approaches.

### Sequential

The sequential implementation executes the matrix multiplication using a single CPU execution flow. It provides the baseline execution time.

### OpenMP

OpenMP uses multiple threads on the same shared-memory system. Different threads can process different rows of the output matrix simultaneously.

### MPI

MPI divides the computation among multiple processes. Each process handles a portion of the matrix multiplication and communicates with other processes to produce the final result.

### CUDA

CUDA uses the GPU's large number of parallel threads to perform matrix multiplication. Each CUDA thread can calculate one or more elements of the output matrix.

The measured execution times are used to observe the performance difference between these approaches.

---

## 6. Conclusion

Matrix multiplication was implemented using four different computational approaches:

1. Sequential CPU
2. OpenMP shared-memory parallelism
3. MPI distributed-memory parallelism
4. CUDA GPU parallelism

The sequential implementation provides the baseline for performance comparison. OpenMP and MPI demonstrate CPU-based parallel execution, while CUDA demonstrates GPU-based parallel computation.

The execution times obtained from each implementation are compared to understand the performance characteristics of different parallel computing models.

```
```
