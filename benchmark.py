#!/usr/bin/env python3
"""Benchmark SHA256 implementation performance."""

import time
import hashlib
from hello_world_package import sha256_hash


def time_hash(data: bytes, num_iterations: int = 1) -> tuple[float, str]:
    """Time the SHA256 hash calculation.

    Args:
        data: Binary data to hash
        num_iterations: Number of times to run (for averaging)

    Returns:
        Tuple of (average_time_seconds, hash_result)
    """
    start = time.perf_counter()

    for _ in range(num_iterations):
        result = sha256_hash(data)

    end = time.perf_counter()
    avg_time = (end - start) / num_iterations

    return avg_time, result


def format_size(num_bytes: int) -> str:
    """Format byte size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"


def format_time(seconds: float) -> str:
    """Format time in human-readable format."""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"


def benchmark():
    """Run comprehensive benchmark of SHA256 implementation."""
    print("SHA256 Pure Python Implementation - Performance Benchmark")
    print("=" * 80)
    print()

    # Test different data sizes
    test_sizes = [
        (0, "Empty"),
        (11, "Hello world (11 bytes)"),
        (64, "Exactly 1 block (64 bytes)"),
        (128, "2 blocks (128 bytes)"),
        (1024, "1 KB"),
        (10 * 1024, "10 KB"),
        (100 * 1024, "100 KB"),
        (1024 * 1024, "1 MB"),
    ]

    print(f"{'Data Size':<30} {'Time':<15} {'Throughput':<20} {'Hash (first 16 chars)'}")
    print("-" * 80)

    for size, description in test_sizes:
        # Create test data
        if size == 0:
            data = b""
        elif size == 11:
            data = b"hello world"
        else:
            data = b"a" * size

        # Determine number of iterations based on size
        # Smaller data = more iterations for accurate timing
        if size < 1024:
            iterations = 1000
        elif size < 10 * 1024:
            iterations = 100
        elif size < 100 * 1024:
            iterations = 10
        else:
            iterations = 1

        # Time the hash
        avg_time, hash_result = time_hash(data, iterations)

        # Calculate throughput (bytes per second)
        if avg_time > 0 and size > 0:
            throughput = size / avg_time
            throughput_str = f"{format_size(int(throughput))}/s"
        else:
            throughput_str = "N/A"

        size_str = f"{description} ({format_size(size)})"
        time_str = format_time(avg_time)
        hash_preview = hash_result[:16]

        print(f"{size_str:<30} {time_str:<15} {throughput_str:<20} {hash_preview}")

    print()
    print("=" * 80)

    # Compare with Python's hashlib
    print("\nComparison with hashlib.sha256:")
    print("-" * 80)

    test_data = b"a" * 10240  # 10 KB
    iterations = 100

    # Time our implementation
    our_time, our_hash = time_hash(test_data, iterations)

    # Time hashlib
    start = time.perf_counter()
    for _ in range(iterations):
        lib_hash = hashlib.sha256(test_data).hexdigest()
    end = time.perf_counter()
    lib_time = (end - start) / iterations

    print(f"Our implementation:  {format_time(our_time)}")
    print(f"hashlib.sha256:      {format_time(lib_time)}")
    print(f"Slowdown factor:     {our_time / lib_time:.1f}x")
    print(f"Hashes match:        {'✓' if our_hash == lib_hash else '✗'}")


if __name__ == "__main__":
    benchmark()
