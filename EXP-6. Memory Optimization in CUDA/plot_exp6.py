
import matplotlib.pyplot as plt

# Experiment 6: CUDA Memory Optimization

# Experimental results
methods = ["Uncoalesced", "Coalesced"]

execution_times = [0.7882, 0.4107]
bandwidth = [158.59, 304.37]

# --------------------------------
# Graph 1: Execution Time
# --------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(methods, execution_times)

plt.title("CUDA Matrix Transpose - Execution Time")
plt.xlabel("Transpose Method")
plt.ylabel("Execution Time (ms)")

plt.grid(axis="y", linestyle="--", alpha=0.5)

for bar, value in zip(bars, execution_times):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.4f} ms",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("graph1_transpose_time.png", dpi=300)
plt.show()

# --------------------------------
# Graph 2: Memory Bandwidth
# --------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(methods, bandwidth)

plt.title("CUDA Matrix Transpose - Memory Bandwidth")
plt.xlabel("Transpose Method")
plt.ylabel("Bandwidth (GB/s)")

plt.grid(axis="y", linestyle="--", alpha=0.5)

for bar, value in zip(bars, bandwidth):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.2f} GB/s",
        ha="center",
        va="bottom"
    )

plt.tight_layout()
plt.savefig("graph2_memory_bandwidth.png", dpi=300)
plt.show()

# --------------------------------
# Performance Summary
# --------------------------------

speedup = execution_times[0] / execution_times[1]

print("\n========== EXPERIMENT 6 GRAPH SUMMARY ==========")
print(f"Uncoalesced Time : {execution_times[0]:.4f} ms")
print(f"Coalesced Time   : {execution_times[1]:.4f} ms")
print(f"Uncoalesced BW   : {bandwidth[0]:.2f} GB/s")
print(f"Coalesced BW     : {bandwidth[1]:.2f} GB/s")
print(f"Speedup          : {speedup:.2f}x")
print("Graphs saved successfully!")
