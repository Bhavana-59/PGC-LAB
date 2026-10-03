
```text
~/PGC_LAB/multithread_exp/pthreads/README.md
```

````markdown
# Part A — Pthreads

## Objective

To understand thread creation, management, work distribution, race conditions, synchronization, and performance using POSIX Threads (Pthreads).

---

## Programs

| Program | Concept Demonstrated |
|---|---|
| `thread1.c` | Creating and joining a single thread |
| `thread2.c` | Creating and managing multiple threads |
| `thread_sum.c` | Dividing work among threads |
| `race.c` | Demonstrating a race condition |
| `mutex.c` | Preventing race conditions using a mutex |
| `pthread_perf.c` | Measuring parallel execution performance |

---

## 1. thread1.c — Single Thread Creation

### Purpose

Demonstrates how to create one additional thread using Pthreads.

### Important functions

```c
pthread_create()
pthread_join()
````

### Compile

```bash
gcc thread1.c -o thread1 -pthread
```

### Run

```bash
./thread1
```

### Concept

The main thread creates a new thread using `pthread_create()`.
The main thread waits for the new thread using `pthread_join()`.

---

## 2. thread2.c — Multiple Threads

### Purpose

Demonstrates creation and management of multiple threads.

### Compile

```bash
gcc thread2.c -o thread2 -pthread
```

### Run

```bash
./thread2
```

### Concept

Multiple threads are created using an array of `pthread_t`.

The output order may vary because the operating system schedules the threads independently.

---

## 3. thread_sum.c — Work Distribution

### Purpose

Demonstrates dividing a computational task among multiple threads.

### Compile

```bash
gcc thread_sum.c -o thread_sum -pthread
```

### Run

```bash
./thread_sum
```

### Concept

The array is divided into smaller portions.

Each thread calculates the sum of its assigned portion, and the partial results are combined to obtain the final sum.

This demonstrates basic parallel work distribution.

---

## 4. race.c — Race Condition

### Purpose

To demonstrate a race condition when multiple threads access shared data.

### Compile

```bash
gcc race.c -o race -pthread
```

### Run

```bash
./race
```

### Concept

Multiple threads increment the same shared variable.

Since the increment operation is not protected, threads may interfere with each other.

Therefore, the final result may be different from the expected value.

This demonstrates the need for synchronization when accessing shared data.

---

## 5. mutex.c — Synchronization Using Mutex

### Purpose

To solve the race condition using a mutex.

### Compile

```bash
gcc mutex.c -o mutex -pthread
```

### Run

```bash
./mutex
```

### Concept

A mutex allows only one thread at a time to enter the critical section.

Important functions:

```c
pthread_mutex_lock()
pthread_mutex_unlock()
pthread_mutex_init()
pthread_mutex_destroy()
```

The shared counter is protected so that the expected result is obtained.

---

## 6. pthread_perf.c — Performance Analysis

### Purpose

To measure the execution time of a parallel program using different numbers of threads.

### Compile

```bash
gcc pthread_perf.c -o pthread_perf -pthread
```

### Run

```bash
./pthread_perf
```

### Threads Tested

```text
1, 2, 3, 4, 6, 8
```

### Performance Metrics

#### Speedup

```text
Speedup = Sequential Time / Pthreads Time
```

#### Efficiency

```text
Efficiency = Speedup / Number of Threads × 100
```

### Results

The execution time was measured for different thread counts and used in the Part C performance analysis.

---

## Key Learning

Through these programs, the following Pthreads concepts were understood:

* Thread creation
* Thread joining
* Multiple thread management
* Work distribution
* Shared data
* Race conditions
* Critical sections
* Mutex synchronization
* Parallel performance
* Speedup and efficiency

---

## Screenshots

Execution screenshots for each program are available in:

```text
screenshots/
```

````
