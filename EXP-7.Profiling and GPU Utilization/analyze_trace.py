
"""
Experiment 7: Analyze PyTorch GPU profiler traces.

Usage:
    python analyze_trace.py trace_baseline.json
    python analyze_trace.py trace_baseline.json trace_optimized.json
"""

import collections
import json
import sys

GAP_US = 50

COMPUTE_HINTS = (
    "gemm", "sgemm", "cutlass",
    "cublas", "conv", "wmma"
)


def merge(intervals):
    intervals = sorted(intervals)
    output = []

    for start, end in intervals:
        if output and start <= output[-1][1]:
            output[-1][1] = max(output[-1][1], end)
        else:
            output.append([start, end])

    return output


def total(intervals):
    return sum(end - start for start, end in intervals)


def overlap(a, b):
    i = j = result = 0

    while i < len(a) and j < len(b):
        start = max(a[i][0], b[j][0])
        end = min(a[i][1], b[j][1])

        if end > start:
            result += end - start

        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1

    return result


def label(name):
    low = name.lower()

    if any(hint in low for hint in COMPUTE_HINTS):
        return "compute-bound"

    return "memory-bound"


def analyze(path):

    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    events = data["traceEvents"] if isinstance(data, dict) else data

    kernels = []
    copies = []

    kernel_names = collections.defaultdict(lambda: [0, 0.0])
    copy_names = collections.defaultdict(lambda: [0, 0.0])

    for event in events:

        if event.get("ph") != "X":
            continue

        category = event.get("cat", "")
        start = event["ts"]
        duration = event.get("dur", 0)
        name = event.get("name", "Unknown")

        if category == "kernel":
            kernels.append([start, start + duration])
            kernel_names[name[:60]][0] += 1
            kernel_names[name[:60]][1] += duration

        elif category in ("gpu_memcpy", "gpu_memset"):
            copies.append([start, start + duration])
            copy_names[name[:60]][0] += 1
            copy_names[name[:60]][1] += duration

    if not kernels:
        print(f"{path}: No GPU kernels found in trace.")
        return None

    k = merge(kernels)
    c = merge(copies)

    start = min(k[0][0], c[0][0] if c else k[0][0])
    end = max(k[-1][1], c[-1][1] if c else k[-1][1])

    span = end - start
    busy = total(k)
    copy_busy = total(c)
    copy_overlap = overlap(k, c)

    gaps = [
        k[i + 1][0] - k[i][1]
        for i in range(len(k) - 1)
    ]

    large_gaps = [gap for gap in gaps if gap > GAP_US]

    print("\n" + "=" * 72)
    print(path)
    print("=" * 72)

    print(f"Profiled window            : {span / 1000:9.2f} ms")
    print(f"Kernel busy time           : {busy / 1000:9.2f} ms")
    print(f"GPU utilization            : {100 * busy / span:9.1f} %")
    print(f"Copy busy time             : {copy_busy / 1000:9.2f} ms")
    print(f"Copy overlapped with kernel: {copy_overlap / 1000:9.2f} ms")

    print(
        f"Idle gaps > {GAP_US} us        : "
        f"{len(large_gaps):9d} "
        f"(total {sum(large_gaps) / 1000:.2f} ms)"
    )

    print("\nKERNELS")
    print(f"{'Calls':>6} {'Total ms':>10} {'Label':<15} Name")

    for name, (count, duration) in sorted(
        kernel_names.items(),
        key=lambda item: -item[1][1]
    ):
        print(
            f"{count:6d} "
            f"{duration / 1000:10.2f} "
            f"{label(name):<15} "
            f"{name}"
        )

    print("\nMEMORY COPIES")
    print(f"{'Calls':>6} {'Total ms':>10} Name")

    for name, (count, duration) in sorted(
        copy_names.items(),
        key=lambda item: -item[1][1]
    ):
        print(
            f"{count:6d} "
            f"{duration / 1000:10.2f} "
            f"{name}"
        )

    return span, busy, copy_busy, copy_overlap, len(large_gaps)


def main():

    if len(sys.argv) < 2:
        raise SystemExit(
            "Usage: python analyze_trace.py trace_*.json"
        )

    rows = []

    for path in sys.argv[1:]:
        result = analyze(path)

        if result:
            rows.append((path, result))

    if len(rows) > 1:

        print("\nSUMMARY")
        print(
            f"{'File':<24}"
            f"{'Window ms':>12}"
            f"{'Util %':>10}"
            f"{'Overlap ms':>13}"
            f"{'Gaps':>8}"
        )

        for path, (span, busy, _, overlap_time, gaps) in rows:

            print(
                f"{path:<24}"
                f"{span / 1000:12.1f}"
                f"{100 * busy / span:10.1f}"
                f"{overlap_time / 1000:13.1f}"
                f"{gaps:8d}"
            )


if __name__ == "__main__":
    main()
