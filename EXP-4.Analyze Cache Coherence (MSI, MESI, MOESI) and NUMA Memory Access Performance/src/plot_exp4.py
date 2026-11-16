
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------
# GRAPH 1: False Sharing Comparison
# Program 2 median measurements
# --------------------------------

threads = [1, 2, 4]
adjacent = [0.0220, 0.0139, 0.0082]
padded = [0.0210, 0.0116, 0.0082]

x = np.arange(len(threads))
width = 0.35

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, adjacent, width, label="Adjacent")
plt.bar(x + width/2, padded, width, label="Padded")

plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.title("False Sharing: Adjacent vs Padded")
plt.xticks(x, threads)
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graph1_false_sharing.png", dpi=300)
plt.close()


# --------------------------------
# GRAPH 2: NUMA Local Memory
# Program 4 measurements
# --------------------------------

numa_threads = [1, 2]
memory_time = [0.016123, 0.013546]

plt.figure(figsize=(8, 5))
plt.bar(numa_threads, memory_time)

plt.xlabel("Number of Threads")
plt.ylabel("Memory Access Time (seconds)")
plt.title("NUMA Local Memory Performance")
plt.xticks(numa_threads)
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graph2_numa_performance.png", dpi=300)
plt.close()


# --------------------------------
# GRAPH 3: Cache Coherence Protocols
# Program 1: 1000 iterations
# --------------------------------

protocols = ["MSI", "MESI", "MOESI"]

adjacent_bus = [4000, 3999, 3999]
padded_bus = [4, 2, 2]

x = np.arange(len(protocols))

plt.figure(figsize=(8, 5))
plt.bar(x - width/2, adjacent_bus, width, label="Adjacent")
plt.bar(x + width/2, padded_bus, width, label="Padded")

plt.xlabel("Cache Coherence Protocol")
plt.ylabel("Number of Bus Transactions")
plt.title("Bus Transactions: MSI, MESI and MOESI")
plt.xticks(x, protocols)
plt.yscale("log")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("graph3_coherence_protocols.png", dpi=300)
plt.close()

print("All 3 graphs generated successfully!")
print("1. graph1_false_sharing.png")
print("2. graph2_numa_performance.png")
print("3. graph3_coherence_protocols.png")
