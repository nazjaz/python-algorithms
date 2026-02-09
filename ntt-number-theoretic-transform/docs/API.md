# NTT API Documentation

## Classes

### NTT

Main class for Number Theoretic Transform implementation.

#### Constants

- `DEFAULT_MOD`: `998244353` - Default prime modulus
- `DEFAULT_ROOT`: `3` - Default primitive root

#### Methods

##### `__init__(self, mod: int = DEFAULT_MOD, root: Optional[int] = None) -> None`

Initialize NTT with modulus and primitive root.

**Parameters**:
- `mod` (int): Prime modulus. Should be of form k*2^n + 1 for large n. Default: 998244353.
- `root` (Optional[int]): Primitive root modulo mod. If None, will be computed automatically.

**Raises**:
- `ValueError`: If mod is not prime or root is invalid.

**Example**:
```python
ntt = NTT()
ntt = NTT(mod=7340033)
ntt = NTT(mod=998244353, root=3)
```

---

##### `ntt(self, coefficients: List[int]) -> List[int]`

Compute Number Theoretic Transform.

Converts polynomial from coefficient representation to point-value representation using modular arithmetic.

**Parameters**:
- `coefficients` (List[int]): List of polynomial coefficients (integers).

**Returns**:
- `List[int]`: List of NTT values (point-value representation modulo mod).

**Raises**:
- `ValueError`: If coefficients list is empty.

**Example**:
```python
ntt = NTT()
coeffs = [1, 2, 3, 4]
result = ntt.ntt(coeffs)
```

---

##### `intt(self, values: List[int]) -> List[int]`

Compute Inverse Number Theoretic Transform.

Converts polynomial from point-value representation back to coefficient representation.

**Parameters**:
- `values` (List[int]): List of NTT values (point-value representation).

**Returns**:
- `List[int]`: List of polynomial coefficients modulo mod.

**Raises**:
- `ValueError`: If values list is empty.

**Example**:
```python
ntt = NTT()
values = ntt.ntt([1, 2, 3, 4])
result = ntt.intt(values)
# Returns: [1, 2, 3, 4]
```

---

##### `multiply_polynomials(self, poly1: List[int], poly2: List[int]) -> List[int]`

Multiply two polynomials using NTT.

**Parameters**:
- `poly1` (List[int]): Coefficients of first polynomial.
- `poly2` (List[int]): Coefficients of second polynomial.

**Returns**:
- `List[int]`: Coefficients of product polynomial modulo mod.

**Raises**:
- `ValueError`: If either polynomial is empty.

**Example**:
```python
ntt = NTT()
poly1 = [1, 2, 3]
poly2 = [4, 5]
result = ntt.multiply_polynomials(poly1, poly2)
# Returns: [4, 13, 22, 15]
```

---

##### `convolve(self, signal1: List[int], signal2: List[int]) -> List[int]`

Compute convolution of two signals using NTT.

**Parameters**:
- `signal1` (List[int]): First signal.
- `signal2` (List[int]): Second signal.

**Returns**:
- `List[int]`: Convolution result modulo mod.

**Raises**:
- `ValueError`: If either signal is empty.

**Example**:
```python
ntt = NTT()
signal1 = [1, 2, 3]
signal2 = [4, 5]
result = ntt.convolve(signal1, signal2)
```

---

##### `circular_convolution(self, signal1: List[int], signal2: List[int]) -> List[int]`

Compute circular (cyclic) convolution of two signals.

**Parameters**:
- `signal1` (List[int]): First signal.
- `signal2` (List[int]): Second signal.

**Returns**:
- `List[int]`: Circular convolution result modulo mod.

**Raises**:
- `ValueError`: If signals have different lengths or are empty.

**Example**:
```python
ntt = NTT()
signal1 = [1, 2, 3]
signal2 = [4, 5, 6]
result = ntt.circular_convolution(signal1, signal2)
```

---

##### `autocorrelation(self, signal: List[int]) -> List[int]`

Compute autocorrelation of a signal.

**Parameters**:
- `signal` (List[int]): Input signal.

**Returns**:
- `List[int]`: Autocorrelation result modulo mod.

**Raises**:
- `ValueError`: If signal is empty.

**Example**:
```python
ntt = NTT()
signal = [1, 2, 3]
result = ntt.autocorrelation(signal)
```

---

##### `cross_correlation(self, signal1: List[int], signal2: List[int]) -> List[int]`

Compute cross-correlation of two signals.

**Parameters**:
- `signal1` (List[int]): First signal.
- `signal2` (List[int]): Second signal.

**Returns**:
- `List[int]`: Cross-correlation result modulo mod.

**Raises**:
- `ValueError`: If either signal is empty.

**Example**:
```python
ntt = NTT()
signal1 = [1, 2, 3]
signal2 = [4, 5]
result = ntt.cross_correlation(signal1, signal2)
```

---

##### `evaluate_polynomial(self, coefficients: List[int], x: int) -> int`

Evaluate polynomial at a point using Horner's method.

**Parameters**:
- `coefficients` (List[int]): Polynomial coefficients.
- `x` (int): Point to evaluate at.

**Returns**:
- `int`: Polynomial value at x modulo mod.

**Example**:
```python
ntt = NTT()
coefficients = [1, 2, 3]
value = ntt.evaluate_polynomial(coefficients, 5)
# Returns: (1*25 + 2*5 + 3) mod mod
```

---

##### `polynomial_to_string(self, coefficients: List[int]) -> str`

Convert polynomial coefficients to string representation.

**Parameters**:
- `coefficients` (List[int]): Polynomial coefficients.

**Returns**:
- `str`: String representation of polynomial.

**Example**:
```python
ntt = NTT()
coefficients = [1, 2, 3]
result = ntt.polynomial_to_string(coefficients)
# Returns: "1 + 2x + 3x^2"
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_is_prime(self, n: int) -> bool`

Check if a number is prime.

##### `_mod_power(self, base: int, exp: int, mod: int) -> int`

Compute base^exp mod mod efficiently.

##### `_mod_inverse(self, a: int, mod: int) -> int`

Compute modular inverse using extended Euclidean algorithm.

##### `_find_primitive_root(self, mod: int) -> int`

Find a primitive root modulo mod.

##### `_prime_factors(self, n: int) -> List[int]`

Find prime factors of a number.

##### `_next_power_of_two(self, n: int) -> int`

Find the smallest power of two greater than or equal to n.

##### `_get_root_of_unity(self, n: int) -> int`

Get primitive root of unity for size n.

##### `_ntt_recursive(self, coefficients: List[int], n: int, root: int) -> List[int]`

Recursive helper for NTT computation.

---

## Usage Examples

### Basic NTT Operations

```python
from src.main import NTT

ntt = NTT()

# Compute NTT
coeffs = [1, 2, 3, 4]
ntt_result = ntt.ntt(coeffs)

# Compute inverse NTT
intt_result = ntt.intt(ntt_result)
# intt_result == coeffs
```

### Polynomial Multiplication

```python
ntt = NTT()
poly1 = [1, 2, 3]
poly2 = [4, 5]
product = ntt.multiply_polynomials(poly1, poly2)
print(f"Product: {product}")
```

### Convolution Operations

```python
ntt = NTT()
signal1 = [1, 2, 3]
signal2 = [4, 5]

# Linear convolution
convolution = ntt.convolve(signal1, signal2)

# Circular convolution (signals must have same length)
signal1 = [1, 2, 3]
signal2 = [4, 5, 6]
circular = ntt.circular_convolution(signal1, signal2)
```

### Correlation Operations

```python
ntt = NTT()

# Autocorrelation
signal = [1, 2, 3]
autocorr = ntt.autocorrelation(signal)

# Cross-correlation
signal1 = [1, 2, 3]
signal2 = [4, 5]
crosscorr = ntt.cross_correlation(signal1, signal2)
```

---

## Performance Characteristics

- **NTT/INTT**: O(n log n) where n is the polynomial degree
- **Polynomial multiplication**: O(n log n) where n is the maximum degree
- **Convolution**: O(n log n) where n is the signal length
- **Polynomial evaluation**: O(n) where n is the degree

---

## Notes

- All operations are performed modulo the prime modulus
- Results are exact integers (no floating-point errors)
- The modulus must be a prime of the form k*2^n + 1
- Maximum size is limited by the modulus (must divide p-1)
- The implementation automatically finds a primitive root if not provided
- All coefficients are reduced modulo the prime before operations
