# Sequential Matrix Multiplication

## Objective

Implement 4000 × 4000 matrix multiplication using a sequential CPU approach and use it as the baseline for comparison with OpenMP, MPI, and CUDA.

## Problem

Two matrices `A` and `B`, each of size 4000 × 4000, are initialized with `1.0` in every element.

The result is calculated as:

`C = A × B`

Since every element of `A` and `B` is `1.0`, every element of `C` should be:

```text
4000.00
```

## Implementation

The sequential implementation uses three nested loops:

* `i` selects a row of matrix `A`.
* `j` selects a column of matrix `B`.
* `k` performs the multiplication and accumulation.

The matrices are dynamically allocated using `malloc()`.

## Source Code

`matrix_sequential.c`

## Compilation

```bash
gcc -O2 matrix_sequential.c -o matrix_sequential
```

## Execution

```bash
./matrix_sequential
```

## Verification

The program checks the computed result.

Expected value:

```text
4000.00
```

## Performance Result

The execution time will be filled after the actual experiment is performed.

| Metric         |         Result |
| -------------- | -------------: |
| Matrix size    |    4000 × 4000 |
| Execution time |     549.322 sec|
| Verification   |        4000.00 |

## Screenshot

The execution screenshot will be stored in:

```text
screenshots/sequential/
```
