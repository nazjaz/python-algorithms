# GCD Calculator

A Python implementation of the Greatest Common Divisor (GCD) calculator using the Euclidean algorithm and Extended Euclidean algorithm. The Extended Euclidean algorithm finds coefficients for linear combinations, enabling solutions to linear Diophantine equations and modular inverse calculations.

## Project Title and Description

The GCD Calculator provides complete implementations of the Euclidean algorithm and Extended Euclidean algorithm for finding the greatest common divisor of integers. The Extended Euclidean algorithm also finds coefficients x and y such that gcd(a, b) = ax + by, which is essential for cryptography, number theory, and solving linear Diophantine equations.

This tool solves the problem of efficiently calculating GCDs and finding linear combinations, which are fundamental operations in number theory, cryptography (especially RSA), and various algorithmic problems.

**Target Audience**: Students learning algorithms and number theory, developers studying cryptography, educators teaching computer science and mathematics, and anyone interested in understanding Euclidean algorithms and their applications.

## Features

- Euclidean algorithm for GCD calculation
- Extended Euclidean algorithm for linear combinations
- GCD calculation for multiple numbers
- Least Common Multiple (LCM) calculation
- Modular inverse calculation
- Linear combination verification
- Comprehensive logging
- Detailed calculation reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/gcd-calculator
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python src/main.py --help
```

## Configuration

### Configuration File (config.yaml)

The tool uses a YAML configuration file to define logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/app.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic GCD Calculation

Calculate GCD of two numbers:

```bash
python src/main.py 48 18
```

### Extended Euclidean Algorithm

Calculate GCD with linear combination coefficients:

```bash
python src/main.py 48 18 --extended
```

### Detailed Results

Show detailed calculation results:

```bash
python src/main.py 48 18 --details
```

### Calculate LCM

Calculate Least Common Multiple:

```bash
python src/main.py 48 18 --lcm
```

### GCD of Multiple Numbers

Calculate GCD of multiple numbers:

```bash
python src/main.py --multiple 48 18 12
```

### Modular Inverse

Find modular inverse:

```bash
python src/main.py 3 --modular-inverse 11
```

### Generate Report

Generate detailed calculation report:

```bash
python src/main.py 48 18 --extended --report report.txt
```

### Demonstration Mode

Run demonstration with example calculations:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `a`: (Optional) First integer
- `b`: (Optional) Second integer
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-e, --extended`: Use Extended Euclidean algorithm
- `-d, --details`: Show detailed calculation results
- `-r, --report`: Output path for calculation report
- `--multiple`: Calculate GCD of multiple numbers
- `--lcm`: Calculate LCM instead of GCD
- `--modular-inverse MODULUS`: Find modular inverse (requires first number)
- `--demo`: Run demonstration with example calculations

### Common Use Cases

**Calculate Basic GCD:**
1. Run: `python src/main.py 48 18`
2. Review GCD result
3. Understand Euclidean algorithm

**Find Linear Combination:**
1. Run: `python src/main.py 48 18 --extended`
2. Review coefficients x and y
3. Verify: 48*x + 18*y = gcd(48, 18)

**Calculate LCM:**
1. Run: `python src/main.py 48 18 --lcm`
2. Review LCM result
3. Verify: gcd * lcm = a * b

**Find Modular Inverse:**
1. Run: `python src/main.py 3 --modular-inverse 11`
2. Review modular inverse
3. Verify: (3 * inverse) mod 11 = 1

**Study Algorithm:**
1. Run: `python src/main.py --demo`
2. Review different calculation scenarios
3. Understand algorithm behavior

## Project Structure

```
gcd-calculator/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── .env.example             # Environment variables template
├── src/
│   └── main.py              # Main application code
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains the `GCDCalculator` class with Euclidean and Extended Euclidean algorithms
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the calculator
- `logs/`: Directory for application log files

## Algorithm Details

### Euclidean Algorithm

The Euclidean algorithm is based on the principle that:
```
gcd(a, b) = gcd(b, a mod b)
```

**Algorithm Steps:**
1. Start with two numbers a and b
2. While b != 0:
   - Set a = b, b = a mod b
3. When b = 0, a is the GCD

**Example:**
```
gcd(48, 18)
= gcd(18, 48 mod 18) = gcd(18, 12)
= gcd(12, 18 mod 12) = gcd(12, 6)
= gcd(6, 12 mod 6) = gcd(6, 0)
= 6
```

**Time Complexity:** O(log min(a, b))
**Space Complexity:** O(1)

### Extended Euclidean Algorithm

The Extended Euclidean algorithm finds coefficients x and y such that:
```
gcd(a, b) = ax + by
```

**Algorithm Steps:**
1. Initialize: r1 = a, r2 = b, x1 = 1, y1 = 0, x2 = 0, y2 = 1
2. While r2 != 0:
   - Calculate quotient q = r1 // r2
   - Update: r1, r2 = r2, r1 mod r2
   - Update coefficients using matrix multiplication
3. When r2 = 0, r1 is the GCD and (x1, y1) are the coefficients

**Example:**
```
gcd(48, 18) = 6
48 * 1 + 18 * (-2) = 6
```

**Time Complexity:** O(log min(a, b))
**Space Complexity:** O(1)

### Relationship with LCM

The GCD and LCM are related by:
```
gcd(a, b) * lcm(a, b) = |a * b|
```

Therefore:
```
lcm(a, b) = |a * b| / gcd(a, b)
```

### Modular Inverse

The modular inverse of a modulo m is a number x such that:
```
(a * x) mod m = 1
```

The modular inverse exists only if gcd(a, m) = 1. It can be found using the Extended Euclidean algorithm.

## Applications

### Cryptography

- **RSA Algorithm**: Uses Extended Euclidean algorithm for key generation
- **Modular Arithmetic**: Finding multiplicative inverses
- **Public Key Cryptography**: GCD calculations for security

### Number Theory

- **Linear Diophantine Equations**: Solving ax + by = c
- **Chinese Remainder Theorem**: Finding solutions to systems of congruences
- **Prime Factorization**: GCD calculations in factorization algorithms

### Practical Applications

- **Simplifying Fractions**: gcd(numerator, denominator)
- **Algorithm Optimization**: GCD in various algorithms
- **Computer Graphics**: GCD for pixel calculations
- **Music Theory**: GCD for rhythm patterns

## Testing

### Run Tests

```bash
python -m pytest tests/
```

### Run Tests with Coverage

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite aims for minimum 80% code coverage, testing:
- Basic GCD calculations
- Extended Euclidean algorithm
- Multiple number GCD
- LCM calculations
- Modular inverses
- Edge cases (zero, negative numbers, coprime numbers)
- Linear combination verification
- Error handling

## Troubleshooting

### Common Issues

**ValueError: GCD of (0, 0) is undefined:**
- Both numbers are zero
- GCD is undefined for (0, 0)
- Use non-zero numbers

**ValueError: Cannot calculate GCD of empty list:**
- Empty list provided for multiple GCD
- Provide at least one number

**Modular inverse doesn't exist:**
- gcd(a, m) != 1
- Modular inverse exists only when a and m are coprime
- Choose coprime numbers

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"GCD of (0, 0) is undefined"**: Both numbers are zero. GCD is undefined in this case.

**"Cannot calculate GCD of empty list"**: No numbers provided. Provide at least one number.

**"Modular inverse doesn't exist"**: gcd(a, m) != 1. Choose coprime numbers.

**"Modulus must be positive"**: Modulus must be greater than zero.

### Best Practices

1. **Use extended mode** for linear combinations: `--extended`
2. **Generate reports** for documentation: `--report report.txt`
3. **Check logs** to understand calculation process
4. **Test with simple numbers** first
5. **Use demonstration mode** to see examples: `--demo`
6. **Verify results** using linear combination verification

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes following PEP 8 style guidelines
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/`
6. Submit a pull request

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Include docstrings for all public functions and classes
- Use meaningful variable names
- Write tests for all new functionality

### Pull Request Process

1. Ensure code follows project standards
2. Update documentation if needed
3. Add/update tests
4. Ensure all tests pass
5. Submit PR with clear description of changes

## License

This project is part of the python-algorithms collection. Please refer to the parent repository for license information.
