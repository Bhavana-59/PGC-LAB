
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define N 100000000L
#define SIZE (256L * 1024 * 1024)

void false_sharing_test(int threads, int padded)
{
    int stride = padded ? 8 : 1;
    size_t bytes = ((size_t)threads * stride * sizeof(long) + 63) / 64 * 64;

    long *cnt = aligned_alloc(64, bytes);
    if (!cnt) {
        printf("Counter allocation failed\n");
        return;
    }

    for (int i = 0; i < threads * stride; i++)
        cnt[i] = 0;

    omp_set_num_threads(threads);

    double start = omp_get_wtime();

    #pragma omp parallel
    {
        int id = omp_get_thread_num();
        volatile long *p = &cnt[id * stride];

        for (long i = 0; i < N / threads; i++)
            (*p)++;
    }

    double elapsed = omp_get_wtime() - start;

    long total = 0;
    for (int i = 0; i < threads; i++)
        total += cnt[i * stride];

    printf("%-9s | threads=%d | total=%ld | time=%.6f s\n",
           padded ? "padded" : "adjacent",
           threads, total, elapsed);

    free(cnt);
}

void memory_test(int threads)
{
    char *buffer = malloc(SIZE);

    if (!buffer) {
        printf("Memory allocation failed\n");
        return;
    }

    omp_set_num_threads(threads);

    #pragma omp parallel for
    for (long i = 0; i < SIZE; i += 64)
        buffer[i] = 1;

    double start = omp_get_wtime();
    long long sum = 0;

    #pragma omp parallel for reduction(+:sum)
    for (long i = 0; i < SIZE; i += 64)
        sum += buffer[i];

    double elapsed = omp_get_wtime() - start;

    printf("Memory | threads=%d | sum=%lld | time=%.6f s\n",
           threads, sum, elapsed);

    free(buffer);
}

int main(void)
{
    printf("FALSE-SHARING COMPARISON\n");
    printf("------------------------\n");

    int thread_counts[] = {1, 2, 4};

    for (int i = 0; i < 3; i++) {
        int threads = thread_counts[i];

        false_sharing_test(threads, 0);
        false_sharing_test(threads, 1);
        printf("\n");
    }

    printf("NUMA LOCAL MEMORY COMPARISON\n");
    printf("----------------------------\n");

    memory_test(1);
    memory_test(2);

    return 0;
}
