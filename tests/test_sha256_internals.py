"""Tests for SHA256 internal functions"""

from hello_world_package.pyhash import (
    _pad_message, _rotr, _shr, _H_INIT, _K,
    _ch, _maj, _sigma0, _sigma1, _sigma_lower0, _sigma_lower1
)


def test_pad_message_hello_world():
    """Test padding for 'hello world' (11 bytes = 88 bits)."""
    message = b"hello world"
    padded = _pad_message(message)

    # Padded message should be a multiple of 64 bytes (512 bits)
    assert len(padded) % 64 == 0

    # For 11 bytes: 11 + 1 (0x80) + 52 zeros + 8 (length) = 72 -> rounds to 128
    # Actually: 11 + 1 = 12, need to reach 56 mod 64 = 44 more zeros, then 8 = 64 total
    assert len(padded) == 64

    # Check first 11 bytes are original message
    assert padded[:11] == b"hello world"

    # Check byte 11 is 0x80 (the '1' bit)
    assert padded[11] == 0x80

    # Check bytes 12-55 are zeros
    assert padded[12:56] == b'\x00' * 44

    # Check last 8 bytes represent length 88 in big-endian
    # 88 = 0x0000000000000058
    assert padded[56:64] == (88).to_bytes(8, 'big')


def test_pad_message_empty():
    """Test padding for empty message."""
    message = b""
    padded = _pad_message(message)

    # Should be exactly 64 bytes (one block)
    assert len(padded) == 64

    # First byte should be 0x80
    assert padded[0] == 0x80

    # Bytes 1-55 should be zeros
    assert padded[1:56] == b'\x00' * 55

    # Last 8 bytes should be 0 (length = 0)
    assert padded[56:64] == (0).to_bytes(8, 'big')


def test_pad_message_exact_block():
    """Test padding for message that's exactly one block (64 bytes)."""
    message = b"a" * 64
    padded = _pad_message(message)

    # Should be 128 bytes (needs new block for padding)
    assert len(padded) == 128

    # First 64 bytes are original
    assert padded[:64] == b"a" * 64

    # Byte 64 is 0x80
    assert padded[64] == 0x80

    # Last 8 bytes are length: 64 * 8 = 512 bits
    assert padded[120:128] == (512).to_bytes(8, 'big')


def test_constants_h_init():
    """Test that H initial values are defined correctly."""
    assert len(_H_INIT) == 8
    assert _H_INIT[0] == 0x6a09e667
    assert _H_INIT[7] == 0x5be0cd19


def test_constants_k():
    """Test that K round constants are defined correctly."""
    assert len(_K) == 64
    assert _K[0] == 0x428a2f98
    assert _K[63] == 0xc67178f2


def test_rotr():
    """Test rotate right operation."""
    # Test ROTR^7(0x12345678)
    # 0x12345678 >> 7 = 0x002468AC (rightmost 25 bits)
    # 0x12345678 << 25 = 0xF0000000 (leftmost 7 bits moved left)
    # Result: 0xF02468AC
    assert _rotr(0x12345678, 7) == 0xF02468AC

    # Test ROTR^1(0x80000000)
    # 10000000000000000000000000000000
    # Rotate right by 1:
    # 01000000000000000000000000000000
    # = 0x40000000
    assert _rotr(0x80000000, 1) == 0x40000000

    # Test ROTR^1(0x00000001)
    # 00000000000000000000000000000001
    # Rotate right by 1:
    # 10000000000000000000000000000000
    # = 0x80000000
    assert _rotr(0x00000001, 1) == 0x80000000


def test_shr():
    """Test shift right operation."""
    # Test SHR^3(0x12345678)
    # 00010010001101000101011001111000
    # Shift right by 3:
    # 00000010010001101000101011001111
    # = 0x02468ACF
    assert _shr(0x12345678, 3) == 0x02468ACF

    # Test SHR^10(0xFFFFFFFF)
    # All 1s shifted right by 10 should have 10 zeros on left
    # = 0x003FFFFF
    assert _shr(0xFFFFFFFF, 10) == 0x003FFFFF

    # Test SHR^1(0x80000000)
    assert _shr(0x80000000, 1) == 0x40000000


def test_ch():
    """Test Ch (Choose) function."""
    # Ch(x, y, z) = (x AND y) XOR (NOT x AND z)
    # If x bit is 1, choose y; if x bit is 0, choose z

    # All zeros
    assert _ch(0x00000000, 0x00000000, 0x00000000) == 0x00000000

    # x=0xFFFFFFFF: choose all from y
    assert _ch(0xFFFFFFFF, 0x12345678, 0xABCDEF00) == 0x12345678

    # x=0x00000000: choose all from z
    assert _ch(0x00000000, 0x12345678, 0xABCDEF00) == 0xABCDEF00

    # Mixed: x=0xF0F0F0F0
    # Where x is 1, take from y (0x12345678)
    # Where x is 0, take from z (0xABCDEF00)
    result = _ch(0xF0F0F0F0, 0x12345678, 0xABCDEF00)
    assert result == 0x1B3D5F70


def test_maj():
    """Test Maj (Majority) function."""
    # Maj(x, y, z) = (x AND y) XOR (x AND z) XOR (y AND z)
    # Result is the majority bit at each position

    # All zeros
    assert _maj(0x00000000, 0x00000000, 0x00000000) == 0x00000000

    # All ones
    assert _maj(0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF) == 0xFFFFFFFF

    # Two agree on 1, one is 0: result is 1
    assert _maj(0xFFFFFFFF, 0xFFFFFFFF, 0x00000000) == 0xFFFFFFFF

    # Two agree on 0, one is 1: result is 0
    assert _maj(0x00000000, 0x00000000, 0xFFFFFFFF) == 0x00000000


def test_sigma0():
    """Test Σ₀ function."""
    # Σ₀(x) = ROTR²(x) XOR ROTR¹³(x) XOR ROTR²²(x)
    x = 0x12345678
    result = _sigma0(x)
    expected = _rotr(x, 2) ^ _rotr(x, 13) ^ _rotr(x, 22)
    assert result == expected

    # Test with known value
    assert _sigma0(0x00000000) == 0x00000000


def test_sigma1():
    """Test Σ₁ function."""
    # Σ₁(x) = ROTR⁶(x) XOR ROTR¹¹(x) XOR ROTR²⁵(x)
    x = 0x12345678
    result = _sigma1(x)
    expected = _rotr(x, 6) ^ _rotr(x, 11) ^ _rotr(x, 25)
    assert result == expected

    # Test with known value
    assert _sigma1(0x00000000) == 0x00000000


def test_sigma_lower0():
    """Test σ₀ function."""
    # σ₀(x) = ROTR⁷(x) XOR ROTR¹⁸(x) XOR SHR³(x)
    x = 0x12345678
    result = _sigma_lower0(x)
    expected = _rotr(x, 7) ^ _rotr(x, 18) ^ _shr(x, 3)
    assert result == expected

    # Test with known value
    assert _sigma_lower0(0x00000000) == 0x00000000


def test_sigma_lower1():
    """Test σ₁ function."""
    # σ₁(x) = ROTR¹⁷(x) XOR ROTR¹⁹(x) XOR SHR¹⁰(x)
    x = 0x12345678
    result = _sigma_lower1(x)
    expected = _rotr(x, 17) ^ _rotr(x, 19) ^ _shr(x, 10)
    assert result == expected

    # Test with known value
    assert _sigma_lower1(0x00000000) == 0x00000000
