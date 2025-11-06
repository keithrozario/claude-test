# SHA256 Timing Guide

This guide shows how to measure the performance of SHA256 hash calculations using the built-in timing utilities.

## Quick Start

### Method 1: Context Manager (Recommended)

```python
from hello_world_package import sha256_hash, time_hash

data = b"hello world"

with time_hash() as timer:
    result = sha256_hash(data)

print(f"Hash: {result}")
print(f"Time: {timer}")  # Auto-formatted (e.g., "123.45 µs")
```

### Method 2: Manual Timer

```python
from hello_world_package import sha256_hash, HashTimer

data = b"hello world"
timer = HashTimer()

timer.start()
result = sha256_hash(data)
timer.stop()

print(f"Time: {timer}")
print(f"Time (ms): {timer.get_elapsed_ms():.3f} ms")
print(f"Time (µs): {timer.get_elapsed_us():.3f} µs")
print(f"Time (s): {timer.get_elapsed():.6f} s")
```

### Method 3: Benchmark Function

```python
from hello_world_package import sha256_hash, benchmark_hash

data = b"a" * 1024  # 1 KB
iterations = 100

avg_time, result = benchmark_hash(sha256_hash, data, iterations)

throughput = len(data) / avg_time / 1024  # KB/s
print(f"Average time: {avg_time * 1000:.3f} ms")
print(f"Throughput: {throughput:.1f} KB/s")
```

## Available Scripts

### Comprehensive Benchmark

Run the full benchmark suite to test various data sizes:

```bash
uv run python benchmark.py
```

Output example:
```
SHA256 Pure Python Implementation - Performance Benchmark
================================================================================

Data Size                      Time            Throughput           Hash (first 16 chars)
--------------------------------------------------------------------------------
Empty (0.0 B)                  105.10 µs       N/A                  e3b0c44298fc1c14
Hello world (11 bytes)         99.77 µs        107.7 KB/s           b94d27b9934d3e08
1 KB (1.0 KB)                  1.73 ms         577.5 KB/s           2edc986847e209b4
1 MB (1.0 MB)                  1.69 s          604.5 KB/s           9bc1b2a288b26af7
```

### Timing Examples

Run example timing code:

```bash
uv run python timing_example.py
```

## API Reference

### HashTimer

A timer class for measuring execution time.

**Methods:**
- `start()` - Start the timer
- `stop()` - Stop the timer and calculate elapsed time
- `reset()` - Reset the timer to initial state
- `get_elapsed()` - Get elapsed time in seconds
- `get_elapsed_ms()` - Get elapsed time in milliseconds
- `get_elapsed_us()` - Get elapsed time in microseconds
- `__str__()` - Get auto-formatted time string

### time_hash()

Context manager for timing hash operations.

**Usage:**
```python
with time_hash() as timer:
    result = sha256_hash(data)
# timer.elapsed is automatically set
```

### benchmark_hash(hash_func, data, iterations)

Benchmark a hash function with multiple iterations.

**Parameters:**
- `hash_func` - Hash function to benchmark
- `data` - Binary data to hash
- `iterations` - Number of times to run (for averaging)

**Returns:**
- Tuple of `(average_time_seconds, hash_result)`

## Performance Tips

1. **Use multiple iterations** for small data to get accurate measurements:
   ```python
   avg_time, _ = benchmark_hash(sha256_hash, b"small", iterations=1000)
   ```

2. **For large data** (>100 KB), single iteration is usually sufficient:
   ```python
   with time_hash() as timer:
       sha256_hash(large_data)
   ```

3. **Calculate throughput** to compare performance across different data sizes:
   ```python
   throughput_mbps = (len(data) / timer.get_elapsed()) / (1024 * 1024)
   print(f"Throughput: {throughput_mbps:.2f} MB/s")
   ```

## Expected Performance

For reference, the pure Python implementation achieves:

- **Throughput**: ~600 KB/s for large data (>1 KB)
- **Small data**: ~100-200 µs per hash
- **Comparison**: ~2900x slower than C-based hashlib.sha256()

This is expected for a pure Python implementation and demonstrates the algorithm correctly!
