# Miller-Rabin API Documentation

## Classes

### MillerRabin

Main class for Miller-Rabin primality test implementation.

#### Constants

- `DETERMINISTIC_BASES`: Dictionary mapping thresholds to lists of bases for deterministic testing

#### Methods

##### `__init__(self) -> None`

Initialize Miller-Rabin tester.

**Returns**: None

**Example**:
```python
mr = MillerRabin()
```

---

##### `is_prime_probabilistic(self, n: int, k: int = 10) -> bool`

Test if n is prime using probabilistic Miller-Rabin test.

**Parameters**:
- `n` (int): Number to test.
- `k` (int): Number of random bases to test. Default: 10.

**Returns**:
- `bool`: True if n is probably prime, False if n is definitely composite.

**Raises**:
- `ValueError`: If n < 2 or k < 1.

**Example**:
```python
mr = MillerRabin()
is_prime = mr.is_prime_probabilistic(97, k=10)
```

**Error Probability**: 4^(-k). For k=10, error probability is approximately 1 in 1,000,000.

---

##### `is_prime_deterministic(self, n: int) -> bool`

Test if n is prime using deterministic Miller-Rabin test.

Uses known sets of bases for different ranges to provide deterministic results up to 341,550,071,728,321.

**Parameters**:
- `n` (int): Number to test.

**Returns**:
- `bool`: True if n is prime, False if n is composite.

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
mr = MillerRabin()
is_prime = mr.is_prime_deterministic(97)
```

**Note**: For numbers larger than 341,550,071,728,321, falls back to probabilistic test with k=20.

---

##### `find_next_prime(self, n: int, deterministic: bool = False) -> int`

Find the next prime number after n.

**Parameters**:
- `n` (int): Starting number.
- `deterministic` (bool): Use deterministic test if True. Default: False.

**Returns**:
- `int`: Next prime number after n.

**Raises**:
- `ValueError`: If n < 1.

**Example**:
```python
mr = MillerRabin()
next_p = mr.find_next_prime(100)
# Returns: 101
```

---

##### `find_previous_prime(self, n: int, deterministic: bool = False) -> int`

Find the previous prime number before n.

**Parameters**:
- `n` (int): Starting number.
- `deterministic` (bool): Use deterministic test if True. Default: False.

**Returns**:
- `int`: Previous prime number before n, or 2 if no prime exists.

**Raises**:
- `ValueError`: If n < 3.

**Example**:
```python
mr = MillerRabin()
prev_p = mr.find_previous_prime(100)
# Returns: 97
```

---

##### `generate_prime(self, bits: int, deterministic: bool = False) -> int`

Generate a random prime number with specified number of bits.

**Parameters**:
- `bits` (int): Number of bits for the prime.
- `deterministic` (bool): Use deterministic test if True. Default: False.

**Returns**:
- `int`: Random prime number with approximately 'bits' bits.

**Raises**:
- `ValueError`: If bits < 2.
- `RuntimeError`: If prime generation fails after maximum attempts.

**Example**:
```python
mr = MillerRabin()
prime = mr.generate_prime(32)
# Returns a random 32-bit prime
```

---

##### `count_primes_in_range(self, start: int, end: int, deterministic: bool = False) -> int`

Count prime numbers in a range.

**Parameters**:
- `start` (int): Start of range (inclusive).
- `end` (int): End of range (inclusive).
- `deterministic` (bool): Use deterministic test if True. Default: False.

**Returns**:
- `int`: Number of primes in the range.

**Raises**:
- `ValueError`: If start > end or start < 2.

**Example**:
```python
mr = MillerRabin()
count = mr.count_primes_in_range(2, 100)
# Returns: 25
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_mod_power(self, base: int, exp: int, mod: int) -> int`

Compute base^exp mod mod efficiently using binary exponentiation.

##### `_decompose(self, n: int) -> tuple[int, int]`

Decompose n-1 as d * 2^r where d is odd.

##### `_witness(self, a: int, d: int, r: int, n: int) -> bool`

Check if a is a witness for compositeness of n.

##### `_get_deterministic_bases(self, n: int) -> Optional[List[int]]`

Get deterministic bases for given n.

---

## Usage Examples

### Basic Primality Testing

```python
from src.main import MillerRabin

mr = MillerRabin()

# Probabilistic test
is_prime = mr.is_prime_probabilistic(97, k=10)
print(f"97 is prime: {is_prime}")

# Deterministic test
is_prime = mr.is_prime_deterministic(97)
print(f"97 is prime: {is_prime}")
```

### Finding Primes

```python
mr = MillerRabin()

# Find next prime
next_p = mr.find_next_prime(100)
print(f"Next prime after 100: {next_p}")

# Find previous prime
prev_p = mr.find_previous_prime(100)
print(f"Previous prime before 100: {prev_p}")
```

### Prime Generation

```python
mr = MillerRabin()

# Generate random prime
prime = mr.generate_prime(32)
print(f"Generated 32-bit prime: {prime}")

# Generate with deterministic test
prime = mr.generate_prime(32, deterministic=True)
print(f"Generated 32-bit prime (deterministic): {prime}")
```

### Counting Primes

```python
mr = MillerRabin()

# Count primes in range
count = mr.count_primes_in_range(2, 100)
print(f"Number of primes in [2, 100]: {count}")

# Count with deterministic test
count = mr.count_primes_in_range(2, 100, deterministic=True)
print(f"Number of primes in [2, 100] (deterministic): {count}")
```

---

## Performance Characteristics

- **Single test**: O(k * log³ n) where k is number of rounds, n is the number
- **Modular exponentiation**: O(log n) using binary exponentiation
- **Prime generation**: O(k * log³ n) per attempt, typically succeeds quickly
- **Space complexity**: O(1) for all operations

---

## Notes

- Probabilistic test error probability is 4^(-k) where k is the number of rounds
- Deterministic test is guaranteed correct for numbers up to 341,550,071,728,321
- For cryptographic applications, use deterministic variant when possible
- For very large numbers, use probabilistic variant with k ≥ 20
- The test correctly identifies Carmichael numbers as composite
- All operations use efficient modular arithmetic

---

## Deterministic Test Ranges

The deterministic test uses specific bases for different ranges:

- Up to 2,047: base [2]
- Up to 1,373,653: bases [2, 3]
- Up to 9,080,191: bases [31, 73]
- Up to 25,326,001: bases [2, 3, 5]
- Up to 3,215,031,751: bases [2, 3, 5, 7]
- Up to 4,759,123,141: bases [2, 7, 61]
- Up to 1,122,004,669,633: bases [2, 13, 23, 1662803]
- Up to 2,152,302,898,747: bases [2, 3, 5, 7, 11]
- Up to 3,474,749,660,383: bases [2, 3, 5, 7, 11, 13]
- Up to 341,550,071,728,321: bases [2, 3, 5, 7, 11, 13, 17]
