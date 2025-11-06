# SHA256 Implementation Plan

## How SHA256 Works

SHA256 (Secure Hash Algorithm 256-bit) is a cryptographic hash function that takes an input of arbitrary length and produces a fixed 256-bit (32-byte) output. The algorithm processes the input in 512-bit blocks through a series of logical operations.

## Algorithm Steps

### 1. Message Preprocessing (Padding)

The input message must be padded to ensure its length is a multiple of 512 bits.

**Steps:**
1. Append a single '1' bit to the end of the message
2. Append '0' bits until the message length ≡ 448 (mod 512)
   - This leaves exactly 64 bits of space at the end
3. Append the original message length as a 64-bit big-endian integer
   - This represents the length in bits before padding

**Example:**
- Original message: `b"hello world"` = 88 bits
- After step 1: 88 + 1 = 89 bits
- After step 2: pad with zeros to 448 bits
- After step 3: append 64-bit length (88) → total = 512 bits (one block)

### 2. Initialize Hash Values (H)

SHA256 uses eight 32-bit hash values, initialized to specific constants:
- These are the first 32 bits of the fractional parts of the square roots of the first 8 primes (2, 3, 5, 7, 11, 13, 17, 19)

```
H[0] = 0x6a09e667
H[1] = 0xbb67ae85
H[2] = 0x3c6ef372
H[3] = 0xa54ff53a
H[4] = 0x510e527f
H[5] = 0x9b05688c
H[6] = 0x1f83d9ab
H[7] = 0x5be0cd19
```

### 3. Initialize Round Constants (K)

SHA256 uses 64 constant 32-bit words:
- These are the first 32 bits of the fractional parts of the cube roots of the first 64 primes (2, 3, 5, ..., 311)

```
K[0..63] = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    ... (total 64 values)
]
```

### 4. Parse Message into 512-bit Blocks

Divide the padded message into N blocks of 512 bits each:
- Block[0], Block[1], ..., Block[N-1]

### 5. Process Each Block

For each 512-bit block, perform the following:

#### 5.1 Prepare Message Schedule (W)

Create a 64-entry message schedule array W[0..63]:

1. **First 16 words:** Split the 512-bit block into sixteen 32-bit big-endian words
   - W[0] through W[15] = first 16 words from the block

2. **Remaining 48 words:** Compute using the following formula for t = 16 to 63:
   ```
   W[t] = σ₁(W[t-2]) + W[t-7] + σ₀(W[t-15]) + W[t-16]
   ```

   Where:
   - σ₀(x) = ROTR⁷(x) ⊕ ROTR¹⁸(x) ⊕ SHR³(x)
   - σ₁(x) = ROTR¹⁷(x) ⊕ ROTR¹⁹(x) ⊕ SHR¹⁰(x)
   - ROTR^n(x) = circular right shift by n bits
   - SHR^n(x) = right shift by n bits (fill with zeros)
   - ⊕ = XOR operation

#### 5.2 Initialize Working Variables

Set eight working variables to the current hash values:
```
a = H[0]
b = H[1]
c = H[2]
d = H[3]
e = H[4]
f = H[5]
g = H[6]
h = H[7]
```

#### 5.3 Main Compression Loop

For t = 0 to 63, perform the following operations:

1. Calculate T₁:
   ```
   T₁ = h + Σ₁(e) + Ch(e, f, g) + K[t] + W[t]
   ```

2. Calculate T₂:
   ```
   T₂ = Σ₀(a) + Maj(a, b, c)
   ```

3. Update working variables:
   ```
   h = g
   g = f
   f = e
   e = d + T₁
   d = c
   c = b
   b = a
   a = T₁ + T₂
   ```

**Where the functions are:**

- **Ch(x, y, z)** = (x ∧ y) ⊕ (¬x ∧ z)
  - "Choose": if x then y else z

- **Maj(x, y, z)** = (x ∧ y) ⊕ (x ∧ z) ⊕ (y ∧ z)
  - "Majority": result is the majority bit from x, y, z

- **Σ₀(x)** = ROTR²(x) ⊕ ROTR¹³(x) ⊕ ROTR²²(x)

- **Σ₁(x)** = ROTR⁶(x) ⊕ ROTR¹¹(x) ⊕ ROTR²⁵(x)

All operations use modulo 2³² arithmetic (32-bit words).

#### 5.4 Update Hash Values

After processing all 64 rounds, add the working variables to the hash values:
```
H[0] = H[0] + a
H[1] = H[1] + b
H[2] = H[2] + c
H[3] = H[3] + d
H[4] = H[4] + e
H[5] = H[5] + f
H[6] = H[6] + g
H[7] = H[7] + h
```

All additions are performed modulo 2³².

### 6. Produce Final Hash

After processing all blocks, concatenate the eight hash values H[0] through H[7] to produce the final 256-bit hash:

```
Hash = H[0] || H[1] || H[2] || H[3] || H[4] || H[5] || H[6] || H[7]
```

Convert to hexadecimal string for standard representation (64 hex characters).

## Summary of Operations Required

1. **Bitwise operations:**
   - AND (∧)
   - OR (∨)
   - XOR (⊕)
   - NOT (¬)
   - Right shift (SHR)
   - Circular right rotation (ROTR)

2. **Arithmetic operations:**
   - Addition modulo 2³² (32-bit unsigned)

3. **Data handling:**
   - Big-endian byte ordering
   - Bit manipulation
   - Block processing (512-bit chunks)

## Notes

- All operations work on 32-bit words
- All addition is modulo 2³² (overflow wraps around)
- All multi-byte values are big-endian
- The algorithm is deterministic: same input always produces same output
