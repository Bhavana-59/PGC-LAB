

````markdown
# Multithreaded Programming using Pthreads and OpenMP

## Experiment

Develop multithreaded programs using parallel programming libraries to understand thread creation, management, coordination, synchronization, and performance improvement.

---

## Aim

To develop multithreaded programs using **Pthreads** and **OpenMP** and understand:

- Thread creation and management
- Work distribution among threads
- Race conditions
- Synchronization
- Thread coordination
- Parallel performance
- Speedup and efficiency

---

## Technologies Used

- C
- GCC
- POSIX Threads (Pthreads)
- OpenMP
- Linux / Ubuntu
- Python
- Matplotlib

---

## Repository Structure

```text
multithread_exp/
│
├── README.md
│
├── pthreads/
│   ├── README.md
│   ├── thread1.c
│   ├── thread2.c
│   ├── thread_sum.c
│   ├── race.c
│   ├── mutex.c
│   ├── pthread_perf.c
│   └── screenshots/
│
├── openmp/
│   ├── README.md
│   ├── omp1.c
│   ├── omp_sum.c
│   ├── omp_race.c
│   ├── omp_critical.c
│   ├── omp_barrier.c
│   ├── omp_perf.c
│   └── screenshots/
│
└── performance/
    ├── README.md
    ├── sequential.c
    ├── plot_graphs.py
    ├── threads_vs_time.png
    ├── threads_vs_speedup.png
    └── threads_vs_efficiency.png
````

---

# Part A — Pthreads

Pthreads provides a low-level interface for creating and managing threads in C.

The programs demonstrate:

1. Creating a single thread
2. Creating multiple threads
3. Dividing work among threads
4. Demonstrating a race condition
5. Solving the race condition using a mutex
6. Measuring multithreaded performance

### Compilation

```bash
gcc thread1.c -o thread1 -pthread
```

For other Pthreads programs:

```bash
gcc filename.c -o filename -pthread
```

### Execution

```bash
./filename
```

---

# Part B — OpenMP

OpenMP provides compiler directives for parallel programming in C.

The programs demonstrate:

1. Parallel region and thread identification
2. Work sharing and reduction
3. Race condition
4. Synchronization using critical section
5. Thread coordination using barrier
6. Performance measurement

### Compilation

```bash
gcc filename.c -o filename -fopenmp
```

### Execution

```bash
./filename
```

---

# Part C — Performance Analysis

The performance analysis compares sequential execution with Pthreads and OpenMP implementations.

### Metrics

**Speedup**

```text
Speedup = Sequential Time / Parallel Time
```

**Efficiency**

```text
Efficiency = Speedup / Number of Threads × 100
```

### Thread Counts Tested

```text
1, 2, 3, 4, 6, 8
```

### Sequential Baseline

The average sequential execution time obtained from 10 runs was:

```text
2.568768 seconds
```

### Performance Graphs

The following graphs were generated:

* Number of Threads vs Execution Time
* Number of Threads vs Speedup
* Number of Threads vs Efficiency

The graphs compare the performance of **Pthreads and OpenMP**.

---

## Observations

* Increasing the number of threads generally reduced execution time.
* Parallel execution provided speedup compared with the sequential baseline.
* Speedup did not increase linearly with the number of threads.
* Thread management, scheduling, synchronization, memory access, and virtualization overhead can affect performance.
* Pthreads provides explicit control over thread creation and synchronization.
* OpenMP provides a simpler higher-level approach to parallel programming.

---

## Learning Outcomes

After completing this experiment, the following concepts were understood:

* Creation and management of threads
* Work distribution
* Shared data and race conditions
* Mutex-based synchronization
* OpenMP parallel regions
* Reduction and work sharing
* Critical sections and barriers
* Performance measurement
* Speedup and efficiency analysis

````

