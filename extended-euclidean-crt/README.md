# Extended Euclidean Algorithm and Chinese Remainder Theorem

A Python implementation of the extended Euclidean algorithm for computing modular inverses and the Chinese Remainder Theorem for solving systems of congruences.

## Project Title and Description

This project implements the extended Euclidean algorithm for computing greatest common divisors (GCD) and Bézout coefficients, enabling efficient computation of modular inverses. It also implements the Chinese Remainder Theorem (CRT) for solving systems of simultaneous congruences, both in the standard case (coprime moduli) and the general case (non-coprime moduli).

These algorithms are fundamental in number theory, cryptography, and computational mathematics, with applications in RSA encryption, modular arithmetic, and solving systems of linear congruences.

**Target Audience**: Developers working with number theory, cryptography, competitive programming, and anyone needing efficient modular arithmetic operations.

## Features

- Extended Euclidean algorithm for computing GCD and Bézout coefficients
- Modular inverse computation
- Linear congruence solving
- Chinese Remainder Theorem (standard case with coprime moduli)
- Chinese Remainder Theorem (general case with non-coprime moduli)
- Least Common Multiple (LCM) computation
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/extended-euclidean-crt
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

#### Compute GCD

```bash
python src/main.py --gcd 48,18
```

Output:
```
GCD(48, 18) = 6
```

#### Extended GCD

```bash
python src/main.py --extended-gcd 48,18
```

Output:
```
Extended GCD(48, 18):
  GCD = 6
  Coefficients: x = -1, y = 3
  Verification: 48*-1 + 18*3 = 6
```

#### Modular Inverse

```bash
python src/main.py --modular-inverse 3,7
```

Output:
```
Modular inverse of 3 modulo 7: 5
Verification: (3 * 5) mod 7 = 1
```

#### Solve Linear Congruence

```bash
python src/main.py --solve-congruence 3,1,7
```

Output:
```
Solutions to 3x ≡ 1 (mod 7): [5]
  Verification: 3*5 mod 7 = 1
```

#### Chinese Remainder Theorem

```bash
python src/main.py --crt "2,3,2;3,5,7"
```

Output:
```
Chinese Remainder Theorem solution:
  Remainders: [2, 3, 2]
  Moduli: [3, 5, 7]
  Solution: x ≡ 23 (mod 105)
  Verification 1: 23 mod 3 = 2 (expected 2)
  Verification 2: 23 mod 5 = 3 (expected 3)
  Verification 3: 23 mod 7 = 2 (expected 2)
```

#### General CRT (Non-Coprime Moduli)

```bash
python src/main.py --crt-general "1,2,3;2,3,4"
```

#### Compute LCM

```bash
python src/main.py --lcm 4,6
```

Output:
```
LCM(4, 6) = 12
```

### Programmatic Usage

```python
from src.main import ExtendedEuclidean

# Create ExtendedEuclidean instance
ee = ExtendedEuclidean()

# Extended GCD
gcd, x, y = ee.extended_gcd(48, 18)
print(f"GCD: {gcd}, Coefficients: x={x}, y={y}")

# Modular inverse
inv = ee.modular_inverse(3, 7)
print(f"Modular inverse: {inv}")

# Solve congruence
solutions = ee.solve_congruence(3, 1, 7)
print(f"Solutions: {solutions}")

# Chinese Remainder Theorem
result = ee.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
if result:
    x, M = result
    print(f"Solution: x ≡ {x} (mod {M})")

# LCM
lcm = ee.lcm(4, 6)
print(f"LCM: {lcm}")
```

### Common Use Cases

1. **Compute modular inverse for cryptography**
   ```bash
   python src/main.py --modular-inverse 65537,1000000007
   ```

2. **Solve system of congruences**
   ```bash
   python src/main.py --crt "2,3,2;3,5,7"
   ```

3. **Compute GCD**
   ```bash
   python src/main.py --gcd 48,18
   ```

## Project Structure

```
extended-euclidean-crt/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `ExtendedEuclidean` class with all core functionality for GCD, modular inverses, and CRT.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various scenarios.
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
pytest tests/test_main.py::TestExtendedEuclidean::test_modular_inverse_simple
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Extended GCD computation and verification
- Modular inverse computation
- Congruence solving
- Chinese Remainder Theorem (both variants)
- Edge cases (zero, negative numbers, etc.)
- Error handling

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/extended-euclidean-crt"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Modular inverse returns None

**Solution**: The modular inverse exists only when gcd(a, m) = 1. If the numbers are not coprime, no inverse exists.

**Issue**: CRT returns None

**Solution**: Check that:
- All moduli are positive
- For standard CRT, moduli should be pairwise coprime
- For general CRT, the system must be consistent (solutions exist)

### Error Messages

- **"Modulus must be positive"**: All moduli must be positive integers.
- **"Remainders and moduli must have same length"**: The lists must have matching lengths.
- **"List cannot be empty"**: Cannot compute LCM of empty list.

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

### Extended Euclidean Algorithm

The extended Euclidean algorithm computes not only the GCD of two numbers a and b, but also finds integers x and y (Bézout coefficients) such that:

```
ax + by = gcd(a, b)
```

**Algorithm**:
1. If a = 0, return (b, 0, 1)
2. Recursively compute (gcd, x₁, y₁) = extended_gcd(b mod a, a)
3. Compute x = y₁ - (b // a) * x₁
4. Compute y = x₁
5. Return (gcd, x, y)

### Modular Inverse

The modular inverse of a modulo m is a number x such that:

```
ax ≡ 1 (mod m)
```

It exists if and only if gcd(a, m) = 1. The extended Euclidean algorithm is used to find it.

### Chinese Remainder Theorem

Given a system of congruences:
```
x ≡ r₁ (mod m₁)
x ≡ r₂ (mod m₂)
...
x ≡ rₙ (mod mₙ)
```

**Standard Case** (moduli are pairwise coprime):
- Solution is unique modulo M = m₁ × m₂ × ... × mₙ
- Uses formula: x = Σ(rᵢ × Mᵢ × inv(Mᵢ)) mod M
  where Mᵢ = M / mᵢ and inv(Mᵢ) is the modular inverse of Mᵢ modulo mᵢ

**General Case** (moduli need not be coprime):
- Uses iterative method to solve pairs of congruences
- Solution is unique modulo LCM of all moduli
- System must be consistent (solutions exist)

### Time Complexity

- **Extended GCD**: O(log min(a, b))
- **Modular inverse**: O(log min(a, m))
- **CRT (standard)**: O(n × log M) where n is number of equations, M is product of moduli
- **CRT (general)**: O(n² × log M)
- **LCM**: O(log min(a, b))

### Space Complexity

- **All operations**: O(1) - constant space (excluding recursion stack)

## Mathematical Background

### Bézout's Identity

For any integers a and b, there exist integers x and y such that:
```
ax + by = gcd(a, b)
```

The extended Euclidean algorithm finds these coefficients.

### Modular Inverse

If gcd(a, m) = 1, then there exists a unique x (modulo m) such that:
```
ax ≡ 1 (mod m)
```

This x is the modular inverse of a modulo m.

### Chinese Remainder Theorem

**Theorem**: If m₁, m₂, ..., mₙ are pairwise coprime positive integers, then for any integers r₁, r₂, ..., rₙ, the system of congruences:
```
x ≡ r₁ (mod m₁)
x ≡ r₂ (mod m₂)
...
x ≡ rₙ (mod mₙ)
```
has a unique solution modulo M = m₁ × m₂ × ... × mₙ.

## Applications

- **Cryptography**: RSA key generation, modular exponentiation
- **Number Theory**: Solving Diophantine equations
- **Competitive Programming**: Efficient modular arithmetic
- **Error Correction**: Reed-Solomon codes
- **Scheduling**: Finding common periods

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
