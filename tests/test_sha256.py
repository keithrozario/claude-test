"""Tests for the sha256_hash function"""

import hashlib
from hello_world_package import sha256_hash


def test_sha256_hash_hello_world():
    """Test that sha256_hash returns the correct hash for 'hello world'."""
    data = b"hello world"

    # Calculate expected hash using Python's hashlib
    expected_hash = hashlib.sha256(data).hexdigest()

    # Test our function
    result = sha256_hash(data)

    assert result == expected_hash
    assert isinstance(result, str)


def test_sha256_hash_empty():
    """Test SHA256 hash of empty string."""
    data = b""
    expected_hash = hashlib.sha256(data).hexdigest()
    result = sha256_hash(data)
    assert result == expected_hash


def test_sha256_hash_abc():
    """Test SHA256 hash of 'abc'."""
    data = b"abc"
    expected_hash = hashlib.sha256(data).hexdigest()
    result = sha256_hash(data)
    assert result == expected_hash


def test_sha256_hash_long():
    """Test SHA256 hash of longer message (multiple blocks)."""
    data = b"The quick brown fox jumps over the lazy dog"
    expected_hash = hashlib.sha256(data).hexdigest()
    result = sha256_hash(data)
    assert result == expected_hash


def test_sha256_hash_exactly_one_block():
    """Test SHA256 hash of message exactly 55 bytes (fits in one block with padding)."""
    data = b"a" * 55
    expected_hash = hashlib.sha256(data).hexdigest()
    result = sha256_hash(data)
    assert result == expected_hash


def test_sha256_hash_two_blocks():
    """Test SHA256 hash of message requiring two blocks."""
    data = b"a" * 100
    expected_hash = hashlib.sha256(data).hexdigest()
    result = sha256_hash(data)
    assert result == expected_hash


def test_sha256_hash_binary():
    """Test SHA256 hash with binary data (not text)."""
    data = bytes(range(256))
    expected_hash = hashlib.sha256(data).hexdigest()
    result = sha256_hash(data)
    assert result == expected_hash
