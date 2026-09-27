# OpenMP Matrix Multiplication

## Objective

Implement the same 4000 × 4000 matrix multiplication using OpenMP shared-memory parallelism.

## Approach

OpenMP divides the matrix multiplication work among multiple CPU threads.

The outer loop is parallelized so that different rows of the result matrix can be processed concurrently.

The implementation uses:

```c
#pragma omp parallel for
```

The number of threads can be controlled using `OMP_NUM_THREADS`.

## Problem

Matrices `A` and `B` are 4000 × 4000 and every element is initialized to `1.0`.

The result is:

`C = A × B`

Expected value of every element:

```text
4000.00
```

## Source Code

`matrix_openmp.c`

## Compilation

```bash
gcc -O2 -fopenmp matrix_openmp.c -o matrix_openmp
```

## Execution

For example, using 8 OpenMP threads:

```bash
export OMP_NUM_THREADS=8
./matrix_openmp
```

## Verification

The computed result should contain:

```text
4000.00
```

## Performance Result


| Metric         |         Result |
| -------------- | -------------: |
| Matrix size    |    4000 × 4000 |
| OpenMP threads | To be recorded |
| Execution time | To be measured |
| Verification   |        4000.00 |

## Screenshot

The execution screenshot will be stored in:

```text
screenshots/openmp/
```
