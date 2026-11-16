
import matplotlib.pyplot as plt
import numpy as np

# Thread counts
threads = [1, 2, 4, 8]

# Execution times from your experiment
times = {
    "None":     [0.0049, 0.0106, 0.0148, 0.0134],
    "Critical": [0.1224, 0.2213, 0.6869, 0.5517],
    "Atomic":   [0.0696, 0.1720, 0.2180, 0.2098],
    "Lock":     [0.1164, 0.4454, 0.9756, 0.8056]
}

# Final counter values
counts = {
    "None":     [10000000, 8370472, 4106587, 3840331],
    "Critical": [10000000, 10000000, 10000000, 10000000],
    "Atomic":   [10000000, 10000000, 10000000, 10000000],
    "Lock":     [10000000, 10000000, 10000000, 10000000]
}

# ------------------------------------------------
# GRAPH 1: Execution Time Comparison
# ------------------------------------------------

plt.figure(figsize=(10, 6))

for method, values in times.items():
    plt.plot(threads, values, marker='o', linewidth=2, label=method)

plt.title("Execution Time vs Number of Threads")
plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.xticks(threads)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("execution_time.png")
plt.show()


# ------------------------------------------------
# GRAPH 2: Final Counter Value Comparison
# ------------------------------------------------

plt.figure(figsize=(10, 6))

for method, values in counts.items():
    plt.plot(threads, values, marker='o', linewidth=2, label=method)

plt.title("Final Counter Value vs Number of Threads")
plt.xlabel("Number of Threads")
plt.ylabel("Final Counter Value")
plt.xticks(threads)
plt.axhline(y=10000000, linestyle='--', label="Expected Count")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("counter_comparison.png")
plt.show()


# ------------------------------------------------
# GRAPH 3: Execution Time of Protected Methods
# ------------------------------------------------

protected_methods = ["Critical", "Atomic", "Lock"]

x = np.arange(len(threads))
width = 0.25

plt.figure(figsize=(10, 6))

for i, method in enumerate(protected_methods):
    plt.bar(
        x + (i - 1) * width,
        times[method],
        width,
        label=method
    )

plt.title("Execution Time of Synchronization Methods")
plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.xticks(x, threads)
plt.grid(axis='y')
plt.legend()
plt.tight_layout()
plt.savefig("synchronization_comparison.png")
plt.show()

print("All three graphs generated successfully!")
