import matplotlib.pyplot as plt

# -----------------------------
# Data
# -----------------------------

threads = [1, 2, 3, 4, 6, 8]

pthread_time = [
    1.991827,
    1.010035,
    0.961158,
    0.746451,
    0.786221,
    0.778870
]

openmp_time = [
    1.949716,
    0.985749,
    0.845327,
    0.719812,
    0.696243,
    0.690229
]

# Sequential baseline
sequential_time = 2.568768

# -----------------------------
# Calculate Speedup
# -----------------------------

pthread_speedup = [
    sequential_time / t for t in pthread_time
]

openmp_speedup = [
    sequential_time / t for t in openmp_time
]

# -----------------------------
# Calculate Efficiency
# -----------------------------

pthread_efficiency = [
    (s / p) * 100
    for s, p in zip(pthread_speedup, threads)
]

openmp_efficiency = [
    (s / p) * 100
    for s, p in zip(openmp_speedup, threads)
]

# =====================================================
# GRAPH 1: Threads vs Execution Time
# =====================================================

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    pthread_time,
    marker='o',
    label='Pthreads'
)

plt.plot(
    threads,
    openmp_time,
    marker='o',
    label='OpenMP'
)

plt.xlabel('Number of Threads')
plt.ylabel('Execution Time (seconds)')
plt.title('Number of Threads vs Execution Time')
plt.xticks(threads)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('threads_vs_time.png', dpi=300)
plt.show()


# =====================================================
# GRAPH 2: Threads vs Speedup
# =====================================================

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    pthread_speedup,
    marker='o',
    label='Pthreads'
)

plt.plot(
    threads,
    openmp_speedup,
    marker='o',
    label='OpenMP'
)

plt.xlabel('Number of Threads')
plt.ylabel('Speedup')
plt.title('Number of Threads vs Speedup')
plt.xticks(threads)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('threads_vs_speedup.png', dpi=300)
plt.show()


# =====================================================
# GRAPH 3: Threads vs Efficiency
# =====================================================

plt.figure(figsize=(8, 5))

plt.plot(
    threads,
    pthread_efficiency,
    marker='o',
    label='Pthreads'
)

plt.plot(
    threads,
    openmp_efficiency,
    marker='o',
    label='OpenMP'
)

plt.xlabel('Number of Threads')
plt.ylabel('Efficiency (%)')
plt.title('Number of Threads vs Efficiency')
plt.xticks(threads)
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('threads_vs_efficiency.png', dpi=300)
plt.show()