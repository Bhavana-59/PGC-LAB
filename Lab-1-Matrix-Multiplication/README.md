# Lab 1 — Matrix Multiplication using Sequential, OpenMP, MPI and CUDA

## Objective

Implement the same matrix multiplication problem using four computational approaches:

1. Sequential CPU
2. OpenMP shared-memory CPU
3. MPI distributed-memory CPU
4. CUDA GPU

The execution times of the different implementations will be compared to understand the performance effects of sequential and parallel computation.

## Problem Statement

Multiply two `4000 × 4000` matrices:

```text
C = A × B
```

All elements of matrices `A` and `B` are initialized to `1.0`.

Therefore, every element of the resulting matrix `C` should be:

```text
4000.00
```

This provides a common verification value for all four implementations.

## Experiment Structure

```text
Lab-1-Matrix-Multiplication/
│
├── README.md
│
├── sequential/
│   ├── README.md
│   └── matrix_sequential.c
│
├── openmp/
│   ├── README.md
│   └── matrix_openmp.c
│
├── mpi/
│   ├── README.md
│   └── matrix_mpi.c
│
├── cuda/
│   ├── README.md
│   └── matrix_cuda.cu
│
└── screenshots/
    ├── sequential/
    ├── openmp/
    ├── mpi/
    ├── cuda/
    └── comparison/
```

## 1. Sequential CPU

The sequential implementation performs matrix multiplication using three nested loops on the CPU.

It acts as the **baseline** for calculating speedup for the other implementations.

## 2. OpenMP

OpenMP uses shared-memory parallelism.

The matrix multiplication workload is divided among multiple CPU threads using an OpenMP parallel loop.

## 3. MPI

MPI demonstrates distributed-memory parallelism.

Multiple MPI processes compute different portions of the matrix multiplication and communicate to distribute input data and collect the final result.

The experiment uses four Ubuntu machines/processes for the distributed setup.

## 4. CUDA

CUDA uses GPU parallelism.

A CUDA thread is assigned to each output element of matrix `C`, allowing a large number of matrix elements to be calculated concurrently.

## Verification

All four implementations solve the same mathematical problem and should produce:

```text
4000.00
```

for the verified result value.

## Results

The following table will be completed using the **actual execution times obtained during the experiment**.

| Approach   | Execution Time (s) |          Speedup | Verification |
| ---------- | -----------------: | ---------------: | -----------: |
| Sequential |     To be measured |            1.00× |      4000.00 |
| OpenMP     |     To be measured | To be calculated |      4000.00 |
| MPI        |     To be measured | To be calculated |      4000.00 |
| CUDA       |     To be measured | To be calculated |      4000.00 |

Speedup will be calculated relative to the sequential execution time.

## Performance Comparison

After all four implementations are executed, the following comparisons will be added:

* Execution-time comparison
* Speedup comparison
* Performance observations

The generated comparison graphs will be stored in:

```text
screenshots/comparison/
```

## Observations

The observations will be based on the actual measured results.

The comparison will consider:

* Sequential CPU computation
* Shared-memory CPU parallelism using OpenMP
* Distributed-memory computation using MPI
* GPU parallelism using CUDA
* Communication and data-transfer overheads where applicable

## Conclusion

The conclusion will be written after collecting the actual experimental measurements.

It will summarize what was learned from implementing the same matrix multiplication using sequential CPU, shared-memory CPU, distributed-memory CPU, and GPU approaches.

