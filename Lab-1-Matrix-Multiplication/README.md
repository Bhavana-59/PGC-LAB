# Lab 1 — Matrix Multiplication using Sequential, OpenMP, MPI and CUDA

## Objective

Implement matrix multiplication using different computational approaches and analyze their performance:

1. Sequential CPU
2. OpenMP shared-memory CPU
3. MPI distributed-memory CPU
4. CUDA GPU

The execution times of the different implementations are compared to understand the performance benefits of parallel computation.

---

## Problem Statement

Perform multiplication of two `4000 × 4000` matrices using sequential and parallel computing techniques.

Matrices `A` and `B` are initialized with `1.0` values. Therefore, every element of the resulting matrix `C` is expected to be:

```text
C[i][j] = 4000.00
