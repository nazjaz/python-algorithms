# Number Theoretic Transform (NTT)

A Python implementation of the Number Theoretic Transform (NTT) as an alternative to FFT for exact integer arithmetic using modular arithmetic.

## Project Title and Description

This project implements the Number Theoretic Transform (NTT) algorithm for efficient polynomial multiplication and convolution operations using modular arithmetic instead of complex numbers. NTT provides exact integer results without floating-point errors, making it ideal for problems requiring precise integer arithmetic.

NTT is similar to FFT but operates in modular arithmetic, using a primitive root of unity modulo a prime number. This makes it particularly useful in competitive programming, cryptography, and applications where exact integer results are required.

**Target Audience**: Developers working with polynomial algorithms, competitive programmers, cryptographers, and anyone needing exact integer arithmetic for polynomial operations.

## Features

- Number Theoretic Transform (NTT) implementation using Cooley-Tukey algorithm
- Inverse NTT (INTT) for converting back to coefficient representation
- Polynomial multiplication in O(n log n) time with exact integer results
- Convolution operations (linear and circular)
- Autocorrelation and cross-correlation functions
- Polynomial evaluation using Horner's method
- Polynomial string representation
- Automatic primitive root detection
- Configurable prime modulus
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/ntt-number-theoretic-transform
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Note: This project has no external dependencies for core functionality, but pytest is included for testing.

## Configuration

### Default Modulus

The default modulus is `998244353`, which is a prime of the form `k*2^n + 1` (specifically `119*2^23 + 1`). This allows NTT to work with sizes up to 2^23.

### Custom Modulus

You can specify a custom prime modulus when initializing NTT. The modulus must:
- Be a prime number
- Be of the form `k*2^n + 1` for some k and large n
- Have a primitive root (automatically detected)

Common choices:
- `998244353` (default, supports up to 2^23)
- `7340033` (supports up to 2^20)
- `469762049` (supports up to 2^26)

## Usage

### Command-Line Interface

#### Polynomial Multiplication

Multiply two polynomials:

```bash
python src/main.py --multiply --poly1 "1,2,3" --poly2 "4,5"
```

Output:
```
Modulus: 998244353
Primitive root: 3
Polynomial 1: 1 + 2x + 3x^2
Polynomial 2: 4 + 5x
Product: 4 + 13x + 22x^2 + 15x^3
Coefficients: [4, 13, 22, 15]
```

#### Convolution

Compute convolution of two signals:

```bash
python src/main.py --convolve --poly1 "1,2,3" --poly2 "4,5"
```

#### Circular Convolution

Compute circular (cyclic) convolution:

```bash
python src/main.py --circular --poly1 "1,2,3" --poly2 "4,5,6"
```

#### Autocorrelation

Compute autocorrelation of a signal:

```bash
python src/main.py --autocorr "1,2,3"
```

#### Cross-Correlation

Compute cross-correlation of two signals:

```bash
python src/main.py --crosscorr "1,2,3;4,5"
```

#### Polynomial Evaluation

Evaluate polynomial at a point:

```bash
python src/main.py --evaluate "1,2,3;5"
```

#### Custom Modulus

Use a custom prime modulus:

```bash
python src/main.py --multiply --poly1 "1,2" --poly2 "3,4" --mod 7340033
```

### Programmatic Usage

```python
from src.main import NTT

# Create NTT instance
ntt = NTT()

# Multiply polynomials
poly1 = [1, 2, 3]
poly2 = [4, 5]
product = ntt.multiply_polynomials(poly1, poly2)
print(f"Product: {product}")

# Compute convolution
signal1 = [1, 2, 3]
signal2 = [4, 5]
convolution = ntt.convolve(signal1, signal2)
print(f"Convolution: {convolution}")

# Compute circular convolution
signal1 = [1, 2, 3]
signal2 = [4, 5, 6]
circular = ntt.circular_convolution(signal1, signal2)
print(f"Circular convolution: {circular}")

# Autocorrelation
signal = [1, 2, 3]
autocorr = ntt.autocorrelation(signal)
print(f"Autocorrelation: {autocorr}")

# Cross-correlation
signal1 = [1, 2, 3]
signal2 = [4, 5]
crosscorr = ntt.cross_correlation(signal1, signal2)
print(f"Cross-correlation: {crosscorr}")

# Evaluate polynomial
coefficients = [1, 2, 3]
value = ntt.evaluate_polynomial(coefficients, 5)
print(f"P(5) mod {ntt.mod} = {value}")

# Get polynomial string
poly_str = ntt.polynomial_to_string(coefficients)
print(f"Polynomial: {poly_str}")
```

### Common Use Cases

1. **Polynomial Multiplication**
   ```bash
   python src/main.py --multiply --poly1 "1,2,3" --poly2 "4,5"
   ```

2. **Signal Convolution**
   ```bash
   python src/main.py --convolve --poly1 "1,2,3" --poly2 "4,5"
   ```

3. **Polynomial Evaluation**
   ```bash
   python src/main.py --evaluate "1,2,3;5"
   ```

## Project Structure

```
ntt-number-theoretic-transform/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main NTT implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `NTT` class with all core functionality for NTT, polynomial multiplication, and convolution operations.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various polynomial sizes.
- **docs/API.md**: Detailed API documentation for all classes and methods.
- **logs/**: Directory for log files (if logging to files is enabled).

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestNTT::test_multiply_polynomials_simple
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- NTT and inverse NTT operations
- Polynomial multiplication
- Convolution operations
- Edge cases (empty inputs, single elements)
- Large polynomials
- Round-trip consistency (NTT followed by INTT)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/ntt-number-theoretic-transform"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: `ValueError: Size n does not divide mod-1`

**Solution**: The input size must be a power of 2 that divides (mod-1). Use a larger modulus or reduce the input size. The default modulus 998244353 supports sizes up to 2^23.

**Issue**: Results are incorrect for large coefficients

**Solution**: Ensure all coefficients are within the valid range for the modulus. Results are computed modulo the prime modulus.

### Error Messages

- **"Coefficients list cannot be empty"**: Provide at least one coefficient.
- **"Signals must have the same length for circular convolution"**: Ensure both signals have the same length.
- **"Invalid format"**: Check the format of input arguments (use commas to separate coefficients, semicolons to separate different inputs).

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```
4. Create a feature branch: `git checkout -b feature/your-feature-name`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Run tests before committing

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Write clear commit messages following conventional commit format
4. Submit pull request with description of changes

## Algorithm Details

### Number Theoretic Transform

The NTT uses the Cooley-Tukey divide-and-conquer algorithm similar to FFT, but operates in modular arithmetic:

1. **Divide**: Split polynomial into even and odd indexed coefficients
2. **Conquer**: Recursively compute NTT of both halves
3. **Combine**: Combine results using primitive root of unity

The algorithm requires:
- A prime modulus `p` of the form `k*2^n + 1`
- A primitive root `g` modulo `p`
- The root of unity for size `n` is `g^((p-1)/n) mod p`

### Polynomial Multiplication

Polynomial multiplication using NTT:

1. Convert both polynomials to point-value representation using NTT
2. Multiply corresponding point values modulo the prime
3. Convert result back to coefficient representation using inverse NTT

This achieves O(n log n) time complexity with exact integer results.

### Advantages over FFT

- **Exact arithmetic**: No floating-point errors
- **Integer results**: All operations are exact modulo the prime
- **No precision issues**: Works perfectly for integer coefficients
- **Deterministic**: Same input always produces same output

### Limitations

- **Modulus constraint**: Results are computed modulo a prime
- **Size constraint**: Maximum size is limited by the modulus (must divide p-1)
- **Prime requirement**: Requires a prime modulus of specific form

### Time Complexity

- **NTT/INTT**: O(n log n) where n is the polynomial degree
- **Polynomial multiplication**: O(n log n) where n is the maximum degree
- **Convolution**: O(n log n) where n is the signal length
- **Polynomial evaluation**: O(n) where n is the degree

### Space Complexity

- **NTT/INTT**: O(n) for storing intermediate results
- **Polynomial multiplication**: O(n) for result storage
- **Convolution**: O(n) for result storage

## Mathematical Background

### Primitive Root

A primitive root `g` modulo a prime `p` is a number such that:
- `g^(p-1) ≡ 1 (mod p)`
- `g^k ≢ 1 (mod p)` for any `1 ≤ k < p-1`

### Root of Unity

For size `n` dividing `p-1`, the root of unity is:
```
ω = g^((p-1)/n) mod p
```

This satisfies:
- `ω^n ≡ 1 (mod p)`
- `ω^k ≢ 1 (mod p)` for any `1 ≤ k < n`

### Discrete NTT

The NTT of a sequence `a[0..n-1]` is:
```
A[k] = Σ(j=0 to n-1) a[j] * ω^(jk) mod p
```

### Inverse NTT

The inverse NTT is:
```
a[j] = (1/n) * Σ(k=0 to n-1) A[k] * ω^(-jk) mod p
```

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
