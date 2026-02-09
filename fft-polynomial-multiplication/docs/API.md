# FFT API Documentation

## Classes

### FFT

Main class for Fast Fourier Transform implementation.

#### Methods

##### `__init__(self) -> None`

Initialize FFT instance.

**Returns**: None

**Example**:
```python
fft = FFT()
```

---

##### `fft(self, coefficients: List[complex]) -> List[complex]`

Compute Fast Fourier Transform of polynomial coefficients.

Converts polynomial from coefficient representation to point-value representation using divide-and-conquer approach.

**Parameters**:
- `coefficients` (List[complex]): List of polynomial coefficients (complex numbers).

**Returns**:
- `List[complex]`: List of FFT values (point-value representation).

**Raises**:
- `ValueError`: If coefficients list is empty.

**Example**:
```python
fft = FFT()
coeffs = [complex(1, 0), complex(2, 0), complex(3, 0), complex(4, 0)]
result = fft.fft(coeffs)
```

---

##### `ifft(self, values: List[complex]) -> List[complex]`

Compute Inverse Fast Fourier Transform.

Converts polynomial from point-value representation back to coefficient representation.

**Parameters**:
- `values` (List[complex]): List of FFT values (point-value representation).

**Returns**:
- `List[complex]`: List of polynomial coefficients.

**Raises**:
- `ValueError`: If values list is empty.

**Example**:
```python
fft = FFT()
values = [complex(10, 0), complex(-2, 0), complex(-2, 0), complex(-2, 0)]
result = fft.ifft(values)
```

---

##### `multiply_polynomials(self, poly1: List[float], poly2: List[float]) -> List[float]`

Multiply two polynomials using FFT.

**Parameters**:
- `poly1` (List[float]): Coefficients of first polynomial.
- `poly2` (List[float]): Coefficients of second polynomial.

**Returns**:
- `List[float]`: Coefficients of product polynomial.

**Raises**:
- `ValueError`: If either polynomial is empty.

**Example**:
```python
fft = FFT()
poly1 = [1, 2, 3]
poly2 = [4, 5]
result = fft.multiply_polynomials(poly1, poly2)
# Returns: [4, 13, 22, 15]
```

---

##### `convolve(self, signal1: List[float], signal2: List[float]) -> List[float]`

Compute convolution of two signals using FFT.

Convolution is equivalent to polynomial multiplication.

**Parameters**:
- `signal1` (List[float]): First signal.
- `signal2` (List[float]): Second signal.

**Returns**:
- `List[float]`: Convolution result.

**Raises**:
- `ValueError`: If either signal is empty.

**Example**:
```python
fft = FFT()
signal1 = [1, 2, 3]
signal2 = [4, 5]
result = fft.convolve(signal1, signal2)
# Returns: [4, 13, 22, 15]
```

---

##### `circular_convolution(self, signal1: List[float], signal2: List[float]) -> List[float]`

Compute circular (cyclic) convolution of two signals.

**Parameters**:
- `signal1` (List[float]): First signal.
- `signal2` (List[float]): Second signal.

**Returns**:
- `List[float]`: Circular convolution result.

**Raises**:
- `ValueError`: If signals have different lengths or are empty.

**Example**:
```python
fft = FFT()
signal1 = [1, 2, 3]
signal2 = [4, 5, 6]
result = fft.circular_convolution(signal1, signal2)
```

---

##### `autocorrelation(self, signal: List[float]) -> List[float]`

Compute autocorrelation of a signal.

**Parameters**:
- `signal` (List[float]): Input signal.

**Returns**:
- `List[float]`: Autocorrelation result.

**Raises**:
- `ValueError`: If signal is empty.

**Example**:
```python
fft = FFT()
signal = [1, 2, 3]
result = fft.autocorrelation(signal)
```

---

##### `cross_correlation(self, signal1: List[float], signal2: List[float]) -> List[float]`

Compute cross-correlation of two signals.

**Parameters**:
- `signal1` (List[float]): First signal.
- `signal2` (List[float]): Second signal.

**Returns**:
- `List[float]`: Cross-correlation result.

**Raises**:
- `ValueError`: If either signal is empty.

**Example**:
```python
fft = FFT()
signal1 = [1, 2, 3]
signal2 = [4, 5]
result = fft.cross_correlation(signal1, signal2)
```

---

##### `evaluate_polynomial(self, coefficients: List[float], x: float) -> float`

Evaluate polynomial at a point using Horner's method.

**Parameters**:
- `coefficients` (List[float]): Polynomial coefficients.
- `x` (float): Point to evaluate at.

**Returns**:
- `float`: Polynomial value at x.

**Example**:
```python
fft = FFT()
coefficients = [1, 2, 3]
value = fft.evaluate_polynomial(coefficients, 5)
# Returns: 1*25 + 2*5 + 3 = 38
```

---

##### `polynomial_to_string(self, coefficients: List[float]) -> str`

Convert polynomial coefficients to string representation.

**Parameters**:
- `coefficients` (List[float]): Polynomial coefficients.

**Returns**:
- `str`: String representation of polynomial.

**Example**:
```python
fft = FFT()
coefficients = [1, 2, 3]
result = fft.polynomial_to_string(coefficients)
# Returns: "1.00 + 2.00x + 3.00x^2"
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_next_power_of_two(self, n: int) -> int`

Find the smallest power of two greater than or equal to n.

---

## Usage Examples

### Basic FFT Operations

```python
from src.main import FFT

fft = FFT()

# Compute FFT
coeffs = [complex(1, 0), complex(2, 0), complex(3, 0), complex(4, 0)]
fft_result = fft.fft(coeffs)

# Compute inverse FFT
ifft_result = fft.ifft(fft_result)
```

### Polynomial Multiplication

```python
fft = FFT()
poly1 = [1, 2, 3]
poly2 = [4, 5]
product = fft.multiply_polynomials(poly1, poly2)
print(f"Product: {product}")
```

### Convolution Operations

```python
fft = FFT()
signal1 = [1, 2, 3]
signal2 = [4, 5]

# Linear convolution
convolution = fft.convolve(signal1, signal2)

# Circular convolution (signals must have same length)
signal1 = [1, 2, 3]
signal2 = [4, 5, 6]
circular = fft.circular_convolution(signal1, signal2)
```

### Correlation Operations

```python
fft = FFT()

# Autocorrelation
signal = [1, 2, 3]
autocorr = fft.autocorrelation(signal)

# Cross-correlation
signal1 = [1, 2, 3]
signal2 = [4, 5]
crosscorr = fft.cross_correlation(signal1, signal2)
```

---

## Performance Characteristics

- **FFT/IFFT**: O(n log n) where n is the polynomial degree
- **Polynomial multiplication**: O(n log n) where n is the maximum degree
- **Convolution**: O(n log n) where n is the signal length
- **Polynomial evaluation**: O(n) where n is the degree

---

## Notes

- The FFT algorithm requires input size to be a power of 2. The implementation automatically pads to the next power of 2.
- Results are rounded to integers for polynomial multiplication (assuming integer coefficients).
- The implementation uses Python's `cmath` module for complex number operations.
- Small numerical errors may occur due to floating-point arithmetic, but results are rounded appropriately.
