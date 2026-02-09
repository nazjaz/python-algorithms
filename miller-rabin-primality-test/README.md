# Miller-Rabin Primality Test

A Python implementation of the Miller-Rabin primality test with both probabilistic and deterministic variants for efficient large number testing.

## Project Title and Description

This project implements the Miller-Rabin primality test, a probabilistic algorithm for determining whether a number is prime. It includes both a probabilistic variant (for general use) and a deterministic variant (for numbers up to 341,550,071,728,321) that provides guaranteed correct results.

The Miller-Rabin test is one of the most practical primality tests and is widely used in cryptography and number theory applications. Unlike simple trial division, it can efficiently test very large numbers.

**Target Audience**: Developers working with cryptography, number theory, competitive programming, and anyone needing efficient primality testing for large numbers.

## Features

- Probabilistic Miller-Rabin test with configurable number of rounds
- Deterministic Miller-Rabin test for numbers up to 341,550,071,728,321
- Find next/previous prime numbers
- Generate random prime numbers with specified bit length
- Count primes in a range
- Efficient modular exponentiation
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/miller-rabin-primality-test
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

### Deterministic Test Limits

The deterministic variant uses known sets of bases for different ranges:
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

For numbers larger than 341,550,071,728,321, the probabilistic variant is used.

## Usage

### Command-Line Interface

#### Test a Number for Primality

Test using probabilistic method (default):

```bash
python src/main.py 97
```

Output:
```
Testing 97 using probabilistic (k=10) Miller-Rabin test
97 is prime
```

Test using deterministic method:

```bash
python src/main.py --test 97 --deterministic
```

Output:
```
Testing 97 using deterministic Miller-Rabin test
97 is prime
```

#### Custom Number of Rounds

```bash
python src/main.py --test 97 --rounds 20
```

#### Find Next Prime

```bash
python src/main.py --next-prime 100
```

Output:
```
Next prime after 100 (using probabilistic test): 101
```

#### Find Previous Prime

```bash
python src/main.py --prev-prime 100
```

Output:
```
Previous prime before 100 (using probabilistic test): 97
```

#### Generate Random Prime

```bash
python src/main.py --generate 32
```

Output:
```
Generated 32-bit prime (using probabilistic test): 2147483647
```

#### Count Primes in Range

```bash
python src/main.py --count "2,100"
```

Output:
```
Number of primes in [2, 100] (using probabilistic test): 25
```

### Programmatic Usage

```python
from src.main import MillerRabin

# Create Miller-Rabin instance
mr = MillerRabin()

# Test primality (probabilistic)
is_prime = mr.is_prime_probabilistic(97, k=10)
print(f"97 is prime: {is_prime}")

# Test primality (deterministic)
is_prime = mr.is_prime_deterministic(97)
print(f"97 is prime: {is_prime}")

# Find next prime
next_p = mr.find_next_prime(100)
print(f"Next prime after 100: {next_p}")

# Find previous prime
prev_p = mr.find_previous_prime(100)
print(f"Previous prime before 100: {prev_p}")

# Generate random prime
prime = mr.generate_prime(32)
print(f"Generated 32-bit prime: {prime}")

# Count primes in range
count = mr.count_primes_in_range(2, 100)
print(f"Number of primes in [2, 100]: {count}")
```

### Common Use Cases

1. **Test if a number is prime**
   ```bash
   python src/main.py --test 97 --deterministic
   ```

2. **Find next prime**
   ```bash
   python src/main.py --next-prime 1000
   ```

3. **Generate cryptographic prime**
   ```bash
   python src/main.py --generate 256 --deterministic
   ```

4. **Count primes in range**
   ```bash
   python src/main.py --count "1000,2000"
   ```

## Project Structure

```
miller-rabin-primality-test/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main Miller-Rabin implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `MillerRabin` class with all core functionality for primality testing, prime generation, and prime counting.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various number sizes.
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
pytest tests/test_main.py::TestMillerRabin::test_is_prime_deterministic_small_primes
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Probabilistic and deterministic primality testing
- Edge cases (small numbers, even numbers, etc.)
- Large prime numbers
- Composite numbers including Carmichael numbers
- Prime generation and finding
- Range counting
- Error handling

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/miller-rabin-primality-test"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Probabilistic test gives incorrect result

**Solution**: Increase the number of rounds (k parameter). The default is 10, but for critical applications, use 20 or more rounds. For guaranteed results, use the deterministic variant when possible.

**Issue**: Deterministic test falls back to probabilistic

**Solution**: The number is too large (> 341,550,071,728,321). Use the probabilistic variant with a higher number of rounds.

### Error Messages

- **"n must be >= 2"**: The number to test must be at least 2.
- **"k must be >= 1"**: The number of rounds must be at least 1.
- **"bits must be >= 2"**: Prime generation requires at least 2 bits.
- **"start must be <= end"**: Range start must be less than or equal to end.

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

### Miller-Rabin Test

The Miller-Rabin test is based on Fermat's little theorem and works as follows:

1. **Decompose n-1**: Write n-1 as d * 2^r where d is odd
2. **Test bases**: For each base a:
   - Compute a^d mod n
   - If a^d ≡ 1 (mod n) or a^(d*2^i) ≡ -1 (mod n) for some i, n passes this test
   - Otherwise, a is a witness that n is composite
3. **Result**: If all bases pass, n is probably prime (probabilistic) or definitely prime (deterministic)

### Probabilistic Variant

- Uses random bases
- Error probability: 4^(-k) where k is the number of rounds
- Suitable for very large numbers
- Fast and practical

### Deterministic Variant

- Uses specific sets of bases for different ranges
- Guaranteed correct for numbers up to 341,550,071,728,321
- Slower but provides certainty
- Based on known research on deterministic bases

### Time Complexity

- **Single test**: O(k * log³ n) where k is number of rounds, n is the number
- **Modular exponentiation**: O(log n) using binary exponentiation
- **Prime generation**: O(k * log³ n) per attempt, typically succeeds quickly

### Space Complexity

- **O(1)**: Constant space for all operations

## Mathematical Background

### Fermat's Little Theorem

If p is prime and gcd(a, p) = 1, then:
```
a^(p-1) ≡ 1 (mod p)
```

### Miller-Rabin Test

For an odd number n > 1, write n-1 = d * 2^r where d is odd.

If n is prime, then for any a with 1 < a < n:
- Either a^d ≡ 1 (mod n)
- Or a^(d*2^i) ≡ -1 (mod n) for some 0 ≤ i < r

If neither condition holds, n is composite and a is a witness.

### Deterministic Bases

Research has shown that for numbers up to certain limits, testing with specific sets of bases provides deterministic results. The implementation uses known sets of bases for different ranges.

## Security Considerations

- For cryptographic applications, use deterministic variant when possible
- For very large numbers, use probabilistic variant with k ≥ 20
- The test correctly identifies Carmichael numbers as composite
- Error probability decreases exponentially with number of rounds

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
