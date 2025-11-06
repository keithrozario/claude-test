"""SHA256 hashing functionality"""


# SHA256 Constants
# Initial hash values (H): first 32 bits of fractional parts of square roots of first 8 primes
_H_INIT = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19,
]

# Round constants (K): first 32 bits of fractional parts of cube roots of first 64 primes
_K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]


def _rotr(n: int, b: int) -> int:
    """Rotate right (circular right shift) by b bits.

    Args:
        n: 32-bit integer to rotate
        b: Number of bits to rotate

    Returns:
        Rotated 32-bit integer
    """
    return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF


def _shr(n: int, b: int) -> int:
    """Shift right by b bits (fills with zeros).

    Args:
        n: 32-bit integer to shift
        b: Number of bits to shift

    Returns:
        Shifted 32-bit integer
    """
    return (n >> b) & 0xFFFFFFFF


def _ch(x: int, y: int, z: int) -> int:
    """SHA256 Ch (Choose) function: (x AND y) XOR (NOT x AND z).

    Args:
        x, y, z: 32-bit integers

    Returns:
        32-bit result
    """
    return ((x & y) ^ (~x & z)) & 0xFFFFFFFF


def _maj(x: int, y: int, z: int) -> int:
    """SHA256 Maj (Majority) function: (x AND y) XOR (x AND z) XOR (y AND z).

    Args:
        x, y, z: 32-bit integers

    Returns:
        32-bit result
    """
    return ((x & y) ^ (x & z) ^ (y & z)) & 0xFFFFFFFF


def _sigma0(x: int) -> int:
    """SHA256 Σ₀ function: ROTR²(x) XOR ROTR¹³(x) XOR ROTR²²(x).

    Args:
        x: 32-bit integer

    Returns:
        32-bit result
    """
    return _rotr(x, 2) ^ _rotr(x, 13) ^ _rotr(x, 22)


def _sigma1(x: int) -> int:
    """SHA256 Σ₁ function: ROTR⁶(x) XOR ROTR¹¹(x) XOR ROTR²⁵(x).

    Args:
        x: 32-bit integer

    Returns:
        32-bit result
    """
    return _rotr(x, 6) ^ _rotr(x, 11) ^ _rotr(x, 25)


def _sigma_lower0(x: int) -> int:
    """SHA256 σ₀ function: ROTR⁷(x) XOR ROTR¹⁸(x) XOR SHR³(x).

    Args:
        x: 32-bit integer

    Returns:
        32-bit result
    """
    return _rotr(x, 7) ^ _rotr(x, 18) ^ _shr(x, 3)


def _sigma_lower1(x: int) -> int:
    """SHA256 σ₁ function: ROTR¹⁷(x) XOR ROTR¹⁹(x) XOR SHR¹⁰(x).

    Args:
        x: 32-bit integer

    Returns:
        32-bit result
    """
    return _rotr(x, 17) ^ _rotr(x, 19) ^ _shr(x, 10)


def _pad_message(message: bytes) -> bytes:
    """Pad message to be a multiple of 512 bits (64 bytes).

    Steps:
    1. Append a single '1' bit (0x80 byte)
    2. Append '0' bits until length ≡ 448 (mod 512) bits
    3. Append original message length as 64-bit big-endian integer

    Args:
        message: Original message bytes

    Returns:
        Padded message as bytes
    """
    msg_len = len(message)
    msg_bit_len = msg_len * 8

    # Append the '1' bit (0x80 = 10000000 in binary)
    message += b'\x80'

    # Calculate how many zero bytes we need
    # We need to reach (448 bits = 56 bytes) mod 64
    # Currently we have: msg_len + 1 bytes
    # We need: ((msg_len + 1) + zero_bytes) % 64 == 56
    current_len = msg_len + 1
    zero_bytes = (56 - current_len % 64) % 64

    # Append zero bytes
    message += b'\x00' * zero_bytes

    # Append original length as 64-bit big-endian integer
    message += msg_bit_len.to_bytes(8, 'big')

    return message


def _process_block(block: bytes, hash_values: list[int]) -> list[int]:
    """Process a single 512-bit (64-byte) block.

    Args:
        block: 64-byte block to process
        hash_values: Current hash values (8 integers)

    Returns:
        Updated hash values (8 integers)
    """
    # Step 5.1: Prepare message schedule (W)
    w = [0] * 64

    # First 16 words: split block into 32-bit big-endian words
    for t in range(16):
        w[t] = int.from_bytes(block[t*4:(t+1)*4], 'big')

    # Remaining 48 words: computed using formula
    for t in range(16, 64):
        w[t] = (_sigma_lower1(w[t-2]) + w[t-7] + _sigma_lower0(w[t-15]) + w[t-16]) & 0xFFFFFFFF

    # Step 5.2: Initialize working variables
    a, b, c, d, e, f, g, h = hash_values

    # Step 5.3: Main compression loop (64 rounds)
    for t in range(64):
        t1 = (h + _sigma1(e) + _ch(e, f, g) + _K[t] + w[t]) & 0xFFFFFFFF
        t2 = (_sigma0(a) + _maj(a, b, c)) & 0xFFFFFFFF

        h = g
        g = f
        f = e
        e = (d + t1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (t1 + t2) & 0xFFFFFFFF

    # Step 5.4: Update hash values
    new_hash = [
        (hash_values[0] + a) & 0xFFFFFFFF,
        (hash_values[1] + b) & 0xFFFFFFFF,
        (hash_values[2] + c) & 0xFFFFFFFF,
        (hash_values[3] + d) & 0xFFFFFFFF,
        (hash_values[4] + e) & 0xFFFFFFFF,
        (hash_values[5] + f) & 0xFFFFFFFF,
        (hash_values[6] + g) & 0xFFFFFFFF,
        (hash_values[7] + h) & 0xFFFFFFFF,
    ]

    return new_hash


def sha256_hash(data: bytes) -> str:
    """Compute SHA256 hash of arbitrary binary data.

    Args:
        data: Binary data of any size to hash

    Returns:
        str: Hexadecimal string representation of the SHA256 hash
    """
    # Step 1: Pad the message
    padded = _pad_message(data)

    # Step 2: Initialize hash values
    hash_values = _H_INIT.copy()

    # Step 4 & 5: Process each 512-bit (64-byte) block
    num_blocks = len(padded) // 64
    for i in range(num_blocks):
        block = padded[i*64:(i+1)*64]
        hash_values = _process_block(block, hash_values)

    # Step 6: Produce final hash (concatenate all hash values)
    hash_hex = ''.join(f'{h:08x}' for h in hash_values)

    return hash_hex
