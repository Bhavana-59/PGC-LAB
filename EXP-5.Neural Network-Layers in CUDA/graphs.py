
import matplotlib.pyplot as plt
import numpy as np
import os

# =========================================
# CUDA EXPERIMENT 5 - PERFORMANCE GRAPHS
# Only Run 1 and Run 2 are included
# =========================================

# Create graph output folder
os.makedirs("results/graphs", exist_ok=True)

runs = ["Run 1", "Run 2"]
x = np.arange(len(runs))
width = 0.25

# Actual experiment measurements
cpu_time = [0.998885, 0.928910]
gpu_kernel = [0.061146, 0.024962]
gpu_end_to_end = [0.287955, 0.118950]

kernel_speedup = [16.336172, 37.213560]
end_to_end_speedup = [3.468893, 7.809248]

# Additional non-kernel time
additional_time = [
    0.287955 - 0.061146,
    0.118950 - 0.024962
]


# =========================================
# GRAPH 1: CPU vs GPU EXECUTION TIME
# =========================================

plt.figure(figsize=(9, 6))

plt.bar(
    x - width, cpu_time, width,
    label="CPU Compute Time"
)

plt.bar(
    x, gpu_kernel, width,
    label="GPU Kernel-Only Time"
)

plt.bar(
    x + width, gpu_end_to_end, width,
    label="GPU End-to-End Time"
)

plt.title("CPU vs GPU Execution Time", fontsize=15)
plt.xlabel("Experiment Runs")
plt.ylabel("Execution Time (ms)")
plt.xticks(x, runs)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(
    "results/graphs/01_cpu_vs_gpu_execution_time.png",
    dpi=300
)
plt.show()


# =========================================
# GRAPH 2: GPU SPEEDUP COMPARISON
# =========================================

plt.figure(figsize=(9, 6))

plt.bar(
    x - width / 2, kernel_speedup, width,
    label="Kernel-Only Speedup"
)

plt.bar(
    x + width / 2, end_to_end_speedup, width,
    label="End-to-End Speedup"
)

plt.title("GPU Speedup Comparison", fontsize=15)
plt.xlabel("Experiment Runs")
plt.ylabel("Speedup (Times)")
plt.xticks(x, runs)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(
    "results/graphs/02_gpu_speedup_comparison.png",
    dpi=300
)
plt.show()


# =========================================
# GRAPH 3: GPU EXECUTION TIME BREAKDOWN
# =========================================

plt.figure(figsize=(9, 6))

plt.bar(
    x, gpu_kernel,
    label="GPU Kernel-Only Time"
)

plt.bar(
    x, additional_time,
    bottom=gpu_kernel,
    label="Additional Non-Kernel Time"
)

plt.title("GPU Execution Time Breakdown", fontsize=15)
plt.xlabel("Experiment Runs")
plt.ylabel("Execution Time (ms)")
plt.xticks(x, runs)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(
    "results/graphs/03_gpu_execution_time_breakdown.png",
    dpi=300
)
plt.show()


# =========================================
# COMPLETION MESSAGE
# =========================================

print("\nAll 3 graphs generated successfully!")
print("Saved inside: results/graphs/")
