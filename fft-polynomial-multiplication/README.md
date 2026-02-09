# Fast Fourier Transform (FFT) for Polynomial Multiplication

A Python implementation of the Fast Fourier Transform (FFT) algorithm for efficient polynomial multiplication and convolution operations.

## Project Title and Description

This project implements the Cooley-Tukey FFT algorithm for efficient polynomial multiplication and convolution operations. The FFT enables O(n log n) polynomial multiplication instead of the naive O(n²) approach, making it essential for large polynomial operations, signal processing, and various computational applications.

The implementation includes FFT, inverse FFT, polynomial multiplication, convolution operations, and various signal processing utilities. This is particularly useful in competitive programming, signal processing, and numerical computation applications.

**Target Audience**: Developers working with polynomial algorithms, signal processing, competitive programmers, and anyone needing efficient polynomial operations.

## Features

- Fast Fourier Transform (FFT) implementation using Cooley-Tukey algorithm
- Inverse FFT (IFFT) for converting back to coefficient representation
- Polynomial multiplication in O(n log n) time
- Convolution operations (linear and circular)
- Autocorrelation and cross-correlation functions
- Polynomial evaluation using Horner's method
- Polynomial string representation
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library (cmath for complex numbers).

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/fft-polynomial-multiplication
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

This project does not require configuration files or environment variables. All functionality is available through the command-line interface or by importing the classes directly.

## Usage

### Command-Line Interface

#### Polynomial Multiplication

Multiply two polynomials:

```bash
python src/main.py --multiply --poly1 "1,2,3" --poly2 "4,5"
```

Output:
```
Polynomial 1: 1.00 + 2.00x + 3.00x^2
Polynomial 2: 4.00 + 5.00x
Product: 4.00 + 13.00x + 22.00x^2 + 15.00x^3
Coefficients: [4, 13, 22, 15]
```

#### Convolution

Compute convolution of two signals:

```bash
python src/main.py --convolve --poly1 "1,2,3" --poly2 "4,5"
```

Output:
```
Signal 1: [1, 2, 3]
Signal 2: [4, 5]
Convolution: [4, 13, 22, 15]
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

Output:
```
Polynomial: 1.00 + 2.00x + 3.00x^2
P(5) = 86.0
```

### Programmatic Usage

```python
from src.main import FFT

# Create FFT instance
fft = FFT()

# Multiply polynomials
poly1 = [1, 2, 3]
poly2 = [4, 5]
product = fft.multiply_polynomials(poly1, poly2)
print(f"Product: {product}")

# Compute convolution
signal1 = [1, 2, 3]
signal2 = [4, 5]
convolution = fft.convolve(signal1, signal2)
print(f"Convolution: {convolution}")

# Compute circular convolution
signal1 = [1, 2, 3]
signal2 = [4, 5, 6]
circular = fft.circular_convolution(signal1, signal2)
print(f"Circular convolution: {circular}")

# Autocorrelation
signal = [1, 2, 3]
autocorr = fft.autocorrelation(signal)
print(f"Autocorrelation: {autocorr}")

# Cross-correlation
signal1 = [1, 2, 3]
signal2 = [4, 5]
crosscorr = fft.cross_correlation(signal1, signal2)
print(f"Cross-correlation: {crosscorr}")

# Evaluate polynomial
coefficients = [1, 2, 3]
value = fft.evaluate_polynomial(coefficients, 5)
print(f"P(5) = {value}")

# Get polynomial string
poly_str = fft.polynomial_to_string(coefficients)
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
fft-polynomial-multiplication/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main FFT implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `FFT` class with all core functionality for FFT, polynomial multiplication, and convolution operations.
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
pytest tests/test_main.py::TestFFT::test_multiply_polynomials_simple
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- FFT and inverse FFT operations
- Polynomial multiplication
- Convolution operations
- Edge cases (empty inputs, single elements)
- Large polynomials
- Round-trip consistency (FFT followed by IFFT)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/fft-polynomial-multiplication"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Numerical precision errors

**Solution**: The FFT algorithm uses floating-point arithmetic, so small numerical errors are expected. The implementation uses rounding for final results. For higher precision, consider using decimal arithmetic or specialized libraries.

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

### Fast Fourier Transform

The FFT uses the Cooley-Tukey divide-and-conquer algorithm:

1. **Divide**: Split polynomial into even and odd indexed coefficients
2. **Conquer**: Recursively compute FFT of both halves
3. **Combine**: Combine results using twiddle factors

The algorithm requires the input size to be a power of 2, so the implementation automatically pads to the next power of 2.

### Polynomial Multiplication

Polynomial multiplication using FFT:

1. Convert both polynomials to point-value representation using FFT
2. Multiply corresponding point values
3. Convert result back to coefficient representation using inverse FFT

This achieves O(n log n) time complexity instead of O(n²) for naive multiplication.

### Convolution

Convolution is equivalent to polynomial multiplication:
- Linear convolution: Standard polynomial multiplication
- Circular convolution: Polynomial multiplication with periodic boundary conditions

### Time Complexity

- **FFT/IFFT**: O(n log n) where n is the polynomial degree
- **Polynomial multiplication**: O(n log n) where n is the maximum degree
- **Convolution**: O(n log n) where n is the signal length
- **Polynomial evaluation**: O(n) where n is the degree

### Space Complexity

- **FFT/IFFT**: O(n) for storing intermediate results
- **Polynomial multiplication**: O(n) for result storage
- **Convolution**: O(n) for result storage

## Mathematical Background

### Discrete Fourier Transform

The DFT of a sequence `a[0..n-1]` is:
```
A[k] = Σ(j=0 to n-1) a[j] * ω^(-jk)
```
where `ω = e^(2πi/n)` is the n-th root of unity.

### Inverse DFT

The inverse DFT is:
```
a[j] = (1/n) * Σ(k=0 to n-1) A[k] * ω^(jk)
```

### Polynomial Multiplication

Given polynomials:
- P(x) = a₀ + a₁x + a₂x² + ...
- Q(x) = b₀ + b₁x + b₂x² + ...

Their product R(x) = P(x) * Q(x) has coefficients:
```
r[k] = Σ(i+j=k) a[i] * b[j]
```

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
