Lab 1 — Matrix Multiplication using Sequential, OpenMP, MPI and CUDA  Objective

Implement matrix multiplication using different computational approaches and analyze their performance:

1.Sequential CPU
2.OpenMP shared-memory CPU
3.MPI distributed-memory CPU
4.CUDA GPU
The execution times of the different implementations are compared to understand the performance benefits of parallel computation.


Problem Statement

Perform multiplication of two 4000 × 4000 matrices using sequential and parallel computing techniques.

Matrices A and B are initialized with 1.0 values. Therefore, every element of the resulting matrix C is expected to be:

C[i][j] = 4000.00
1. Sequential Matrix Multiplication

The sequential implementation performs matrix multiplication using three nested loops.

i selects the row of matrix A
j selects the column of matrix B
k performs the multiplication and summation
Compilation
gcc -O2 matrix_sequential.c -o matrix_sequential
Execution
./matrix_sequential
Verification

The result is verified using:

C[0][0] = 4000.00

The sequential implementation provides the baseline execution time for comparison with the parallel implementations.

Evidence
Screenshot	Description
01-gcc-version.jpeg	Compiler version
02-source-code.jpeg	Sequential matrix multiplication source code
03-compilation.jpeg	Compilation of the program
04-sequential-output.jpeg	Execution output and verification
