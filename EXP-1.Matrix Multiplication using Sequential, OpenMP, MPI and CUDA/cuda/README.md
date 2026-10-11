# CUDA Matrix Multiplication

## Objective

Implement 4000 × 4000 matrix multiplication using CUDA GPU parallelism.

## Approach

The CUDA implementation assigns one CUDA thread to each output element of matrix `C`.

For a 4000 × 4000 result matrix:

* Output elements = 16,000,000
* Block size = 16 × 16
* Threads per block = 256
* Grid size = 250 × 250 blocks

Each CUDA thread calculates one element of the result matrix using the corresponding row of `A` and column of `B`.

## Problem

Matrices `A` and `B` are both 4000 × 4000 and contain `1.0` in every element.

The result is:

`C = A × B`

Expected value:

```text
4000.00
```

## Source Code

`matrix_cuda.cu`

## Compilation

```bash
nvcc -O2 matrix_cuda.cu -o matrix_cuda
```

## Execution

```bash
./matrix_cuda
```

The program measures CUDA execution using CUDA events.

## Verification

The computed result should contain:

```text
4000.00
```

## Performance Result

The actual GPU information, kernel time, and total execution time will be recorded after running the experiment.

| Metric               |         Result |
| -------------------- | -------------: |
| Matrix size          |    4000 × 4000 |
| GPU                  | To be recorded |
| Kernel time          | To be measured |
| Total execution time | To be measured |
| Verification         |        4000.00 |

## Screenshot

The execution screenshot will be stored in:

```text
screenshots/cuda/
```
