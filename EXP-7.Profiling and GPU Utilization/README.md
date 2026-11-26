
# Experiment 7: Profiling and GPU Utilization

## 1. Aim

To analyze GPU utilization using profiling tools, identify GPU idle time and memory-transfer overhead, and improve GPU performance using pinned host memory and CUDA streams.

## 2. Objectives

- Understand GPU profiling and utilization.
- Identify GPU kernel execution time and idle periods.
- Analyze host-to-device and device-to-host memory transfers.
- Compare pageable and pinned host memory.
- Implement asynchronous memory transfers using CUDA streams.
- Improve GPU utilization by overlapping data transfers with computation.
- Compare baseline and optimized GPU performance.

## 3. Hardware and Software Requirements

### Hardware

| Component | Specification |
|---|---|
| GPU | NVIDIA GeForce RTX 5060 Ti |
| GPU Memory | 16 GB |
| Operating System | Windows |

### Software

| Software / Tool | Version |
|---|---|
| Python | 3.14.10 |
| PyTorch | 2.15.0+cu132 |
| CUDA Toolkit | 13.4 |
| NVIDIA Driver | 610.88 |
| Profiling Tool | PyTorch Profiler |
| GPU Monitoring Tool | NVIDIA-SMI |
| Timeline Visualization | Perfetto |

## 4. Concepts Used

### GPU Profiling

GPU profiling is the process of measuring and analyzing GPU operations to understand how a workload executes. It helps identify kernel execution time, memory-transfer overhead, idle periods, and performance bottlenecks.

### GPU Utilization

GPU utilization represents the percentage of the measured time during which the GPU was actively executing work. Higher utilization can indicate that the GPU is spending less time waiting for additional work.

### Pageable Host Memory

Pageable memory is normal CPU memory. When transferring data from pageable memory to GPU memory, additional staging operations may be required.

### Pinned Host Memory

Pinned memory is host memory that is page-locked. It supports efficient DMA transfers and asynchronous memory transfers.

### CUDA Streams

CUDA streams are sequences of GPU operations that can execute independently. Multiple streams can allow data transfers and computation to overlap when dependencies and hardware capabilities permit.

### Double Buffering

Double buffering uses two device-side buffers so that one buffer can be processed while data for another buffer is being transferred.

## 5. Experimental Procedure

### Stage 1: Baseline Execution

The baseline workload was executed using:

- Pageable host memory.
- Default CUDA stream.
- Blocking memory transfers.

**Command:**

```cmd
python gpu_workload.py --mode baseline --profile
````

The program generated the profiling trace:

`trace_baseline.json`

### **Stage 2: Optimized Execution**

The workload was optimized using:

- Pinned host memory.
- Two CUDA streams.
- Asynchronous memory transfers.
- Double buffering.

**Command:**

```
python gpu_workload.py --mode optimized --profile
```

The program generated the profiling trace:

`trace_optimized.json`

### **Stage 3: Trace Analysis**

The profiler traces were analyzed using:

```
python analyze_trace.py trace_baseline.json
python analyze_trace.py trace_optimized.json
```

For comparison:

```
python analyze_trace.py trace_baseline.json trace_optimized.json
```

### **Stage 4: GPU Monitoring**

NVIDIA-SMI was used to monitor GPU utilization and memory usage during execution. The monitoring measurements were saved in CSV files.

### **Stage 5: Timeline Visualization**

The baseline and optimized profiler traces were opened in Perfetto to visualize GPU operations, memory transfers, execution intervals, and idle gaps.

## **6. Experimental Configuration**

| Parameter            | Value                      |
| -------------------- | -------------------------- |
| GPU                  | NVIDIA GeForce RTX 5060 Ti |
| GPU Memory           | 16 GB                      |
| Batch Size           | 67 MB                      |
| Number of Batches    | 200                        |
| Repetitions          | 3                          |
| Framework            | PyTorch                    |
| Programming Language | Python                     |
| CUDA Toolkit         | 13.4                       |

## **7. Execution Performance Comparison**

| Parameter            | Baseline       | Optimized       |
| -------------------- | -------------- | --------------- |
| Total Execution Time | 3.915 s        | 1.928 s         |
| Time Per Batch       | 19.58 ms       | 9.64 ms         |
| Throughput           | 51.1 batches/s | 103.7 batches/s |
| Checksum             | 4.198830e+09   | 4.198830e+09    |
| Speedup              | 1×             | 2.03×           |

The optimized execution achieved approximately **2.03× speedup** compared with the baseline execution.

## **8. GPU Profiling Results**

| Parameter                 | Baseline  | Optimized |
| ------------------------- | --------- | --------- |
| Profiled Window           | 198.57 ms | 108.18 ms |
| Kernel Busy Time          | 92.09 ms  | 93.01 ms  |
| Estimated GPU Utilization | 46.4%     | 86.0%     |
| Idle Gaps (>50 µs)        | 9         | 9         |
| Total Idle Gap Duration   | 93.16 ms  | 1.42 ms   |

The estimated GPU utilization increased from 46.4% to 86.0%. The total duration of idle gaps decreased significantly after optimization.

**Note:** GPU utilization values are estimates calculated from kernel activity within the analyzed profiler trace window. They are not full-run hardware utilization averages.

## **9. Memory Transfer and CUDA Stream Performance**

| Parameter                | Baseline       | Optimized   |
| ------------------------ | -------------- | ----------- |
| Host Memory Type         | Pageable       | Pinned      |
| Host-to-Device Copy Time | 100.10 ms      | 51.55 ms    |
| Device-to-Host Copy Time | 0.07 ms        | 0.08 ms     |
| Total Copy Busy Time     | 100.17 ms      | 51.63 ms    |
| Copy/Compute Overlap     | 0.00 ms        | 40.41 ms    |
| CUDA Streams             | Default Stream | Two Streams |

Pinned host memory reduced the measured host-to-device transfer time. Using separate CUDA streams enabled data transfers and computation to overlap.

## **10. GPU Kernel Execution Breakdown**

| GPU Operation                | Baseline | Optimized |
| ---------------------------- | -------- | --------- |
| Matrix Multiplication (GEMM) | 60.36 ms | 60.91 ms  |
| Element-wise Addition        | 10.36 ms | 10.44 ms  |
| Element-wise Multiplication  | 10.26 ms | 10.40 ms  |
| Other Vectorized Operations  | 9.75 ms  | 9.88 ms   |
| Reduction                    | 1.37 ms  | 1.38 ms   |

The GPU computation times remained approximately similar in both executions. The main improvement came from more efficient memory transfers and reduced idle time.

*Note: Kernel timings are profiler measurements from the respective traces. Minor differences between repeated runs are expected.*

## **11. Performance Graphs**

### **Graph 1: Execution Time Comparison**

### **Graph 2: GPU Utilization Comparison**

### **Graph 3: Memory Transfer Time Comparison**

### **Graph 4: Idle Time and Copy/Compute Overlap**

## **12. GPU Profiling Timeline Screenshots**

### **12.1 Baseline GPU Timeline**

The baseline timeline shows the original execution pattern, including memory transfers, kernel activity, and idle periods.

### **12.2 Optimized GPU Timeline**

The optimized timeline shows the execution pattern after introducing pinned memory, asynchronous transfers, and multiple CUDA streams. It demonstrates the overlap between memory transfers and GPU computation.

## **13. Execution Screenshots**

### **13.1 Baseline Execution Output**

### **13.2 Optimized Execution Output**

## **14. Observations**

1. Baseline execution took 3.915 seconds, whereas optimized execution took 1.928 seconds.
2. The optimized workload achieved approximately 2.03× speedup.
3. Throughput increased from 51.1 to 103.7 batches per second.
4. Estimated GPU utilization increased from 46.4% to 86.0% in the analyzed profiler traces.
5. Host-to-device copy time decreased from approximately 100.10 ms to 51.55 ms.
6. Copy/compute overlap increased from 0.00 ms to 40.41 ms.
7. Total idle gap duration decreased from 93.16 ms to 1.42 ms.
8. Both executions produced the same reported checksum of 4.198830e+09.

## **15. Conclusion**

The experiment demonstrated the importance of efficient memory transfers and GPU workload scheduling in improving GPU performance.

The baseline implementation used pageable host memory, the default CUDA stream, and blocking memory transfers. The optimized implementation introduced pinned host memory, asynchronous transfers, two CUDA streams, and double buffering.

The optimized implementation reduced total execution time from 3.915 seconds to 1.928 seconds, achieving approximately 2.03× speedup. The analyzed profiler trace also showed increased estimated GPU utilization and reduced idle time.

Therefore, the experiment demonstrated that improving data-transfer efficiency and overlapping memory transfers with computation can significantly improve GPU workload performance.

## **16. Files Description**

| File / Folder          | Description                                   |
| ---------------------- | --------------------------------------------- |
| `gpu_workload.py`      | Executes baseline and optimized GPU workloads |
| `analyze_trace.py`     | Analyzes GPU profiler traces                  |
| `trace_baseline.json`  | Baseline profiling trace                      |
| `trace_optimized.json` | Optimized profiling trace                     |
| `smi_baseline.csv`     | Baseline NVIDIA-SMI monitoring data           |
| `smi_optimized.csv`    | Optimized NVIDIA-SMI monitoring data          |
| `graphs/`              | Performance comparison graphs                 |
| `screenshots/`         | Execution and Perfetto timeline screenshots   |
| `README.md`            | Experiment documentation                      |

````
