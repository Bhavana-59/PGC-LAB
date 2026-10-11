# MPI Matrix Multiplication

## Objective

Implement 4000 × 4000 matrix multiplication using MPI distributed-memory parallelism.

## Approach

The MPI implementation distributes portions of matrix `A` among multiple MPI processes.

For the four-process experiment:

* Matrix rows are divided among the processes.
* `MPI_Scatter` distributes portions of matrix `A`.
* `MPI_Bcast` broadcasts matrix `B`.
* Each process computes its local portion of the result.
* `MPI_Gather` collects the partial results at the root process.

## Problem

Matrices `A` and `B` are both 4000 × 4000 and contain `1.0` in every element.

The result is:

`C = A × B`

Expected value:

```text
4000.00
```

## Source Code

`matrix_mpi.c`

## Compilation

```bash
mpicc -O2 matrix_mpi.c -o matrix_mpi
```

## Execution

For four MPI processes using a hostfile:

```bash
mpirun -np 4 --hostfile hosts sh -c '$HOME/matrix_mpi'
```

The `hosts` file contains the participating machines used for the distributed experiment.

## Verification

The computed result should contain:

```text
4000.00
```

## Performance Result

The actual execution time and MPI configuration will be recorded after running the experiment.

| Metric         |         Result |
| -------------- | -------------: |
| Matrix size    |    4000 × 4000 |
| MPI processes  | To be recorded |
| Execution time | To be measured |
| Verification   |        4000.00 |

## Screenshot

The execution screenshot will be stored in:

```text
screenshots/mpi/
```
