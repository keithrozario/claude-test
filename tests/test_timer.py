"""Tests for timing utilities."""

import time
from hello_world_package import HashTimer, time_hash, benchmark_hash, sha256_hash


def test_hash_timer_basic():
    """Test basic HashTimer functionality."""
    timer = HashTimer()
    timer.start()
    time.sleep(0.01)  # Sleep for 10ms
    timer.stop()

    elapsed = timer.get_elapsed()
    assert elapsed >= 0.01  # Should be at least 10ms
    assert elapsed < 0.02   # Should be less than 20ms


def test_hash_timer_reset():
    """Test HashTimer reset."""
    timer = HashTimer()
    timer.start()
    time.sleep(0.01)
    timer.stop()

    timer.reset()
    assert timer.elapsed is None
    assert timer.start_time is None


def test_hash_timer_format():
    """Test HashTimer string formatting."""
    timer = HashTimer()
    timer.start()
    time.sleep(0.001)  # 1ms
    timer.stop()

    time_str = str(timer)
    # Should format as milliseconds
    assert "ms" in time_str or "µs" in time_str


def test_time_hash_context_manager():
    """Test time_hash context manager."""
    data = b"test data"

    with time_hash() as timer:
        result = sha256_hash(data)

    assert timer.elapsed is not None
    assert timer.elapsed > 0
    assert result is not None


def test_benchmark_hash():
    """Test benchmark_hash function."""
    data = b"hello world"
    iterations = 10

    avg_time, result = benchmark_hash(sha256_hash, data, iterations)

    assert avg_time > 0
    assert result == sha256_hash(data)  # Verify hash is correct


def test_hash_timer_conversions():
    """Test HashTimer time unit conversions."""
    timer = HashTimer()
    timer.start()
    time.sleep(0.001)  # 1ms
    timer.stop()

    ms = timer.get_elapsed_ms()
    us = timer.get_elapsed_us()

    assert ms >= 1.0
    assert us >= 1000.0
    assert abs(ms - us / 1000) < 0.01  # Should be consistent
