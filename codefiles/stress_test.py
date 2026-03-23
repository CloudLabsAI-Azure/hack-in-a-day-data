"""
Infrastructure Stress Test Script
Generates CPU, memory, and disk load on Windows VM for testing Azure Monitor telemetry.
"""

import multiprocessing
import time
import os
import sys
import argparse


def cpu_worker(duration):
    """Single CPU worker that burns CPU for the specified duration."""
    end_time = time.time() + duration
    while time.time() < end_time:
        _ = sum(i * i for i in range(10000))


def cpu_stress(duration=300, workers=None):
    """Run CPU stress test using multiple processes."""
    if workers is None:
        workers = multiprocessing.cpu_count()
    print(f"[CPU] Starting stress test: {workers} workers for {duration} seconds...")
    processes = []
    for _ in range(workers):
        p = multiprocessing.Process(target=cpu_worker, args=(duration,))
        p.start()
        processes.append(p)

    start = time.time()
    while any(p.is_alive() for p in processes):
        elapsed = int(time.time() - start)
        remaining = max(0, duration - elapsed)
        print(f"[CPU] Running... {elapsed}s elapsed, {remaining}s remaining", end="\r")
        time.sleep(5)

    for p in processes:
        p.join()
    print(f"\n[CPU] Stress test complete after {duration} seconds.")


def memory_stress(size_mb=512, duration=300):
    """Allocate memory and hold it for the specified duration."""
    print(f"[Memory] Starting stress test: allocating {size_mb} MB for {duration} seconds...")
    try:
        data = bytearray(size_mb * 1024 * 1024)
        # Touch the memory to ensure it is physically allocated
        for i in range(0, len(data), 4096):
            data[i] = 1
        print(f"[Memory] Allocated {size_mb} MB successfully.")

        start = time.time()
        while time.time() - start < duration:
            elapsed = int(time.time() - start)
            remaining = max(0, duration - elapsed)
            print(f"[Memory] Holding... {elapsed}s elapsed, {remaining}s remaining", end="\r")
            time.sleep(5)

        del data
        print(f"\n[Memory] Stress test complete. Memory released.")
    except MemoryError:
        print(f"[Memory] ERROR: Could not allocate {size_mb} MB. Try a smaller value.")


def disk_stress(size_mb=1024, hold_seconds=120):
    """Write data to disk to consume disk space temporarily."""
    path = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "infraops_stress_test")
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, "stress_data.bin")
    print(f"[Disk] Starting stress test: writing {size_mb} MB to {filepath}...")

    chunk = b"X" * (1024 * 1024)  # 1 MB chunk
    try:
        with open(filepath, "wb") as f:
            for i in range(size_mb):
                f.write(chunk)
                if (i + 1) % 100 == 0:
                    print(f"[Disk] Written {i + 1}/{size_mb} MB...")

        print(f"[Disk] Write complete. {size_mb} MB written to disk.")
        print(f"[Disk] Holding for {hold_seconds} seconds before cleanup...")

        start = time.time()
        while time.time() - start < hold_seconds:
            elapsed = int(time.time() - start)
            remaining = max(0, hold_seconds - elapsed)
            print(f"[Disk] Holding... {elapsed}s elapsed, {remaining}s remaining", end="\r")
            time.sleep(5)

        print()
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print("[Disk] Cleanup complete. Temporary file removed.")
        try:
            os.rmdir(path)
        except OSError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infrastructure Stress Test for Azure Monitor")
    parser.add_argument(
        "--type",
        choices=["cpu", "memory", "disk", "all"],
        default="all",
        help="Type of stress test to run (default: all)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=300,
        help="Duration in seconds for CPU and memory tests (default: 300)",
    )
    parser.add_argument(
        "--cpu-workers",
        type=int,
        default=None,
        help="Number of CPU workers (default: all cores)",
    )
    parser.add_argument(
        "--memory-mb",
        type=int,
        default=512,
        help="Memory to allocate in MB (default: 512)",
    )
    parser.add_argument(
        "--disk-mb",
        type=int,
        default=1024,
        help="Disk space to use in MB (default: 1024)",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("  Infrastructure Stress Test")
    print("=" * 60)
    print(f"  Type: {args.type}")
    if args.type in ("cpu", "all"):
        print(f"  CPU Duration: {args.duration}s, Workers: {args.cpu_workers or 'all cores'}")
    if args.type in ("memory", "all"):
        print(f"  Memory: {args.memory_mb} MB for {args.duration}s")
    if args.type in ("disk", "all"):
        print(f"  Disk: {args.disk_mb} MB")
    print("=" * 60)
    print()

    if args.type in ("cpu", "all"):
        cpu_stress(duration=args.duration, workers=args.cpu_workers)
        print()

    if args.type in ("memory", "all"):
        memory_stress(size_mb=args.memory_mb, duration=args.duration)
        print()

    if args.type in ("disk", "all"):
        disk_stress(size_mb=args.disk_mb)
        print()

    print("All stress tests complete.")
