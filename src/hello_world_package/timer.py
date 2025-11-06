"""Simple timing utilities for measuring hash performance."""

import time
from typing import Optional
from contextlib import contextmanager


class HashTimer:
    """Timer for measuring hash calculation duration."""

    def __init__(self):
        """Initialize timer."""
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.elapsed: Optional[float] = None

    def start(self):
        """Start the timer."""
        self.start_time = time.perf_counter()
        self.end_time = None
        self.elapsed = None

    def stop(self):
        """Stop the timer and calculate elapsed time."""
        if self.start_time is None:
            raise RuntimeError("Timer not started")
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.end_time = None
        self.elapsed = None

    def get_elapsed(self) -> float:
        """Get elapsed time in seconds.

        Returns:
            Elapsed time in seconds

        Raises:
            RuntimeError: If timer hasn't been stopped
        """
        if self.elapsed is None:
            raise RuntimeError("Timer not stopped")
        return self.elapsed

    def get_elapsed_ms(self) -> float:
        """Get elapsed time in milliseconds."""
        return self.get_elapsed() * 1000

    def get_elapsed_us(self) -> float:
        """Get elapsed time in microseconds."""
        return self.get_elapsed() * 1_000_000

    def __str__(self) -> str:
        """Get formatted elapsed time."""
        if self.elapsed is None:
            return "Timer not stopped"

        if self.elapsed < 1e-6:
            return f"{self.elapsed * 1e9:.2f} ns"
        elif self.elapsed < 1e-3:
            return f"{self.elapsed * 1e6:.2f} µs"
        elif self.elapsed < 1:
            return f"{self.elapsed * 1e3:.2f} ms"
        else:
            return f"{self.elapsed:.2f} s"


@contextmanager
def time_hash():
    """Context manager for timing hash operations.

    Usage:
        with time_hash() as timer:
            result = sha256_hash(data)
        print(f"Hash took: {timer}")

    Yields:
        HashTimer instance
    """
    timer = HashTimer()
    timer.start()
    try:
        yield timer
    finally:
        timer.stop()


def benchmark_hash(hash_func, data: bytes, iterations: int = 1) -> tuple[float, str]:
    """Benchmark a hash function.

    Args:
        hash_func: Hash function to benchmark
        data: Data to hash
        iterations: Number of iterations to run

    Returns:
        Tuple of (average_time_seconds, hash_result)
    """
    start = time.perf_counter()

    for _ in range(iterations):
        result = hash_func(data)

    end = time.perf_counter()
    avg_time = (end - start) / iterations

    return avg_time, result
