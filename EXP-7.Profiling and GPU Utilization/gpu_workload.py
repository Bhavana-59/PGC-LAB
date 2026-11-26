
"""
Experiment 7: Profiling and GPU Utilization

Baseline:
    Pageable host memory, default stream, blocking copies.

Optimized:
    Pinned host memory, two CUDA streams, double buffering,
    asynchronous host-device transfers.
"""

import argparse
import math
import time
import torch


# ------------------------------------------------------------
# 1. CREATE GPU WEIGHTS
# ------------------------------------------------------------

def make_weights(n):
    g = torch.Generator().manual_seed(1)
    return (torch.randn(n, n, generator=g) / math.sqrt(n)).cuda()


# ------------------------------------------------------------
# 2. CREATE HOST BATCHES
# ------------------------------------------------------------

def make_host_batches(rows, cols, pinned, unique=4):
    g = torch.Generator().manual_seed(0)
    batches = []

    for _ in range(unique):
        t = torch.randn(rows, cols, generator=g)
        batches.append(t.pin_memory() if pinned else t)

    return batches


# ------------------------------------------------------------
# 3. GPU COMPUTATION
# ------------------------------------------------------------

def compute(x, w, reps):
    y = x

    for _ in range(reps):
        y = y @ w
        y = torch.relu(y)
        y = y.mul_(0.5).add_(1.0)

    return y.sum(dim=1)


# ------------------------------------------------------------
# 4. BASELINE VERSION
# Pageable memory + blocking transfers
# ------------------------------------------------------------

def run_baseline(host, w, reps, nbatches):
    results = []

    for i in range(nbatches):
        x = host[i % len(host)].cuda()
        r = compute(x, w, reps)
        results.append(r.cpu())

    torch.cuda.synchronize()
    return torch.stack(results)


# ------------------------------------------------------------
# 5. OPTIMIZED VERSION
# Pinned memory + two streams + double buffering
# ------------------------------------------------------------

def run_optimized(host, w, reps, nbatches):
    rows, cols = host[0].shape

    copy_s = torch.cuda.Stream()
    comp_s = torch.cuda.Stream()

    buf = [
        torch.empty(rows, cols, device="cuda")
        for _ in range(2)
    ]

    copied = [torch.cuda.Event() for _ in range(2)]
    freed = [torch.cuda.Event() for _ in range(2)]

    out_host = torch.empty(nbatches, rows).pin_memory()

    torch.cuda.synchronize()

    for e in freed:
        e.record(comp_s)

    def issue_copy(i):
        k = i % 2

        copy_s.wait_event(freed[k])

        with torch.cuda.stream(copy_s):
            buf[k].copy_(
                host[i % len(host)],
                non_blocking=True
            )
            copied[k].record(copy_s)

    issue_copy(0)

    for i in range(nbatches):
        k = i % 2

        if i + 1 < nbatches:
            issue_copy(i + 1)

        comp_s.wait_event(copied[k])

        with torch.cuda.stream(comp_s):
            r = compute(buf[k], w, reps)

            freed[k].record(comp_s)

            out_host[i].copy_(r, non_blocking=True)

    torch.cuda.synchronize()

    return out_host


# ------------------------------------------------------------
# 6. MAIN FUNCTION
# ------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["baseline", "optimized"],
        required=True
    )

    parser.add_argument("--batches", type=int, default=200)
    parser.add_argument("--rows", type=int, default=16384)
    parser.add_argument("--cols", type=int, default=1024)
    parser.add_argument("--reps", type=int, default=3)
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--profile-batches", type=int, default=10)

    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA GPU not available.")

    pinned = args.mode == "optimized"

    fn = run_optimized if pinned else run_baseline

    host = make_host_batches(
        args.rows, args.cols, pinned
    )

    w = make_weights(args.cols)

    print("\n======================================")
    print(" EXPERIMENT 7: GPU PROFILING")
    print("======================================")

    print(f"GPU          : {torch.cuda.get_device_name(0)}")
    print(f"Mode         : {args.mode}")
    print(f"Batch size   : {args.rows * args.cols * 4 / 1e6:.0f} MB")
    print(f"Batches      : {args.batches}")
    print(f"Repetitions  : {args.reps}")

    # Warm-up
    print("\nWarming up GPU...")
    fn(host, w, args.reps, 3)
    torch.cuda.synchronize()

    # Timed execution
    print("Running workload...")

    t0 = time.perf_counter()

    res = fn(host, w, args.reps, args.batches)

    torch.cuda.synchronize()

    dt = time.perf_counter() - t0

    print("\n========== PERFORMANCE RESULTS ==========")

    print(f"Total time : {dt:.3f} s")
    print(f"Per batch  : {dt / args.batches * 1000:.2f} ms")
    print(f"Throughput : {args.batches / dt:.1f} batches/s")

    checksum = res.double().sum().item()

    print(f"Checksum   : {checksum:.6e}")

    # PyTorch profiler
    if args.profile:

        print("\nProfiling GPU workload...")

        from torch.profiler import profile, ProfilerActivity

        with profile(
            activities=[
                ProfilerActivity.CPU,
                ProfilerActivity.CUDA
            ]
        ) as prof:

            fn(
                host,
                w,
                args.reps,
                args.profile_batches
            )

            torch.cuda.synchronize()

        name = f"trace_{args.mode}.json"

        prof.export_chrome_trace(name)

        print(f"\nTrace saved: {name}")

        for key in ("cuda_time_total", "device_time_total"):
            try:
                print(
                    prof.key_averages().table(
                        sort_by=key,
                        row_limit=10
                    )
                )
                break
            except Exception:
                continue

    print("\n======================================")
    print(" EXPERIMENT COMPLETED")
    print("======================================\n")


if __name__ == "__main__":
    main()
