#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define SIZE (256L * 1024 * 1024)

int main()
{
    char *buffer = malloc(SIZE);

    if (buffer == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    double start, end;
    double sum = 0.0;

    // First-touch initialization
    #pragma omp parallel for
    for (long i = 0; i < SIZE; i += 64) {
        buffer[i] = 1;
    }

    start = omp_get_wtime();

    // Read one byte from every cache line
    #pragma omp parallel for reduction(+:sum)
    for (long i = 0; i < SIZE; i += 64) {
        sum += buffer[i];
    }

    end = omp_get_wtime();

    printf("Memory size: %ld MB\n", SIZE / (1024 * 1024));
    printf("Threads: %d\n", omp_get_max_threads());
    printf("Sum: %.0f\n", sum);
    printf("Access time: %.6f seconds\n", end - start);

    free(buffer);
    return 0;
}
