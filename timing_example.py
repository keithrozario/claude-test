#!/usr/bin/env python3
"""Examples of using the timing utilities."""

from hello_world_package import sha256_hash, HashTimer, time_hash, benchmark_hash


def example_1_manual_timer():
    """Example 1: Using HashTimer manually."""
    print("Example 1: Manual HashTimer")
    print("-" * 50)

    data = b"hello world"
    timer = HashTimer()

    timer.start()
    result = sha256_hash(data)
    timer.stop()

    print(f"Data: {data}")
    print(f"Hash: {result}")
    print(f"Time: {timer}")
    print(f"Time (ms): {timer.get_elapsed_ms():.3f} ms")
    print(f"Time (µs): {timer.get_elapsed_us():.3f} µs")
    print()


def example_2_context_manager():
    """Example 2: Using time_hash context manager."""
    print("Example 2: Context Manager")
    print("-" * 50)

    data = b"The quick brown fox jumps over the lazy dog"

    with time_hash() as timer:
        result = sha256_hash(data)

    print(f"Data: {data}")
    print(f"Hash: {result}")
    print(f"Time: {timer}")
    print()


def example_3_benchmark_function():
    """Example 3: Using benchmark_hash for multiple iterations."""
    print("Example 3: Benchmark Function")
    print("-" * 50)

    data = b"a" * 1024  # 1 KB
    iterations = 100

    avg_time, result = benchmark_hash(sha256_hash, data, iterations)

    print(f"Data size: {len(data)} bytes")
    print(f"Iterations: {iterations}")
    print(f"Average time: {avg_time * 1000:.3f} ms")
    print(f"Throughput: {len(data) / avg_time / 1024:.1f} KB/s")
    print(f"Hash: {result}")
    print()


def example_4_compare_sizes():
    """Example 4: Compare timing for different data sizes."""
    print("Example 4: Compare Different Data Sizes")
    print("-" * 50)

    sizes = [10, 100, 1000, 10000]

    print(f"{'Size (bytes)':<15} {'Time':<15} {'Throughput':<15}")
    print("-" * 45)

    for size in sizes:
        data = b"x" * size

        with time_hash() as timer:
            result = sha256_hash(data)

        throughput = size / timer.get_elapsed() / 1024  # KB/s

        print(f"{size:<15} {str(timer):<15} {throughput:.1f} KB/s")

    print()


if __name__ == "__main__":
    print("SHA256 Timing Examples")
    print("=" * 50)
    print()

    example_1_manual_timer()
    example_2_context_manager()
    example_3_benchmark_function()
    example_4_compare_sizes()
