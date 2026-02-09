# Pollard's Rho API Documentation

## Classes

### PollardRho

Main class for Pollard's rho factorization algorithm.

#### Methods

##### `__init__(self) -> None`

Initialize Pollard's rho factorizer.

**Returns**: None

**Example**:
```python
pr = PollardRho()
```

---

##### `find_factor(self, n: int, max_attempts: int = 10, max_iterations: int = 10000) -> Optional[int]`

Find a non-trivial factor of n.

Tries multiple values of c if the first attempt fails.

**Parameters**:
- `n` (int): Number to factor.
- `max_attempts` (int): Maximum number of attempts with different c values. Default: 10.
- `max_iterations` (int): Maximum iterations per attempt. Default: 10000.

**Returns**:
- `Optional[int]`: A non-trivial factor of n, or None if not found.

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
pr = PollardRho()
factor = pr.find_factor(100)
# Returns: 2 (or another factor)
```

---

##### `factorize(self, n: int, max_attempts: int = 10) -> Dict[int, int]`

Factorize n completely into prime factors with multiplicities.

**Parameters**:
- `n` (int): Number to factorize.
- `max_attempts` (int): Maximum attempts per factor search. Default: 10.

**Returns**:
- `Dict[int, int]`: Dictionary mapping prime factors to their multiplicities.

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
pr = PollardRho()
factors = pr.factorize(100)
# Returns: {2: 2, 5: 2}
```

---

##### `factorize_list(self, n: int, max_attempts: int = 10) -> List[int]`

Factorize n into a list of prime factors (with multiplicities).

**Parameters**:
- `n` (int): Number to factorize.
- `max_attempts` (int): Maximum attempts per factor search. Default: 10.

**Returns**:
- `List[int]`: List of prime factors (may contain duplicates), sorted.

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
pr = PollardRho()
factors = pr.factorize_list(100)
# Returns: [2, 2, 5, 5]
```

---

##### `get_all_factors(self, n: int, max_attempts: int = 10) -> List[int]`

Get all divisors of n.

**Parameters**:
- `n` (int): Number to get divisors for.
- `max_attempts` (int): Maximum attempts per factor search. Default: 10.

**Returns**:
- `List[int]`: List of all divisors of n (sorted).

**Raises**:
- `ValueError`: If n < 1.

**Example**:
```python
pr = PollardRho()
divisors = pr.get_all_factors(100)
# Returns: [1, 2, 4, 5, 10, 20, 25, 50, 100]
```

---

##### `is_prime(self, n: int, max_attempts: int = 10) -> bool`

Check if n is prime using factorization.

**Parameters**:
- `n` (int): Number to test.
- `max_attempts` (int): Maximum attempts per factor search. Default: 10.

**Returns**:
- `bool`: True if n is prime, False otherwise.

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
pr = PollardRho()
is_prime = pr.is_prime(97)
# Returns: True
```

---

##### `prime_factors(self, n: int, max_attempts: int = 10) -> List[int]`

Get distinct prime factors of n.

**Parameters**:
- `n` (int): Number to factorize.
- `max_attempts` (int): Maximum attempts per factor search. Default: 10.

**Returns**:
- `List[int]`: List of distinct prime factors (sorted).

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
pr = PollardRho()
prime_factors = pr.prime_factors(100)
# Returns: [2, 5]
```

---

##### `factorization_string(self, n: int, max_attempts: int = 10) -> str`

Get string representation of factorization.

**Parameters**:
- `n` (int): Number to factorize.
- `max_attempts` (int): Maximum attempts per factor search. Default: 10.

**Returns**:
- `str`: String representation like "2^2 * 5^2".

**Raises**:
- `ValueError`: If n < 2.

**Example**:
```python
pr = PollardRho()
fact_str = pr.factorization_string(100)
# Returns: "2^2 * 5^2"
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_gcd(self, a: int, b: int) -> int`

Compute greatest common divisor using Euclidean algorithm.

##### `_polynomial(self, x: int, c: int, n: int) -> int`

Polynomial function f(x) = (x² + c) mod n.

##### `_pollard_rho_single(self, n: int, c: int = 1, max_iterations: int = 10000) -> Optional[int]`

Find a single factor of n using Pollard's rho algorithm with Floyd's cycle detection.

##### `_is_prime_simple(self, n: int) -> bool`

Simple primality test for small numbers using trial division.

---

## Usage Examples

### Basic Factorization

```python
from src.main import PollardRho

pr = PollardRho()

# Complete factorization
factors = pr.factorize(100)
print(f"Factors: {factors}")  # {2: 2, 5: 2}

# Find a single factor
factor = pr.find_factor(100)
print(f"A factor: {factor}")  # 2
```

### Getting Divisors

```python
pr = PollardRho()

# Get all divisors
divisors = pr.get_all_factors(100)
print(f"Divisors: {divisors}")
# [1, 2, 4, 5, 10, 20, 25, 50, 100]

# Get distinct prime factors
prime_factors = pr.prime_factors(100)
print(f"Prime factors: {prime_factors}")  # [2, 5]
```

### Primality Testing

```python
pr = PollardRho()

# Check if prime
is_prime = pr.is_prime(97)
print(f"Is prime: {is_prime}")  # True

is_prime = pr.is_prime(100)
print(f"Is prime: {is_prime}")  # False
```

### Factorization String

```python
pr = PollardRho()

# Get factorization string
fact_str = pr.factorization_string(100)
print(f"Factorization: {fact_str}")  # "2^2 * 5^2"
```

---

## Performance Characteristics

- **Expected time**: O(√p) where p is the smallest prime factor
- **Worst case**: O(n) if n is prime
- **Space complexity**: O(1) - constant space
- **Success rate**: High for numbers with small factors, lower for primes

---

## Notes

- The algorithm is probabilistic and may require multiple attempts
- Works best when numbers have small prime factors
- May fail for very large primes (returns None)
- Increasing max_attempts improves success rate but increases runtime
- The algorithm uses Floyd's cycle detection (tortoise and hare)
- Polynomial function f(x) = (x² + c) mod n is used to generate sequences
