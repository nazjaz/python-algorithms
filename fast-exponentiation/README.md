# Fast Exponentiation Calculator

A Python implementation of fast exponentiation using the exponentiation by squaring algorithm. This tool calculates a^n in O(log n) time complexity instead of O(n) time, with comprehensive time complexity analysis, method comparison, and support for modular exponentiation.

## Project Title and Description

The Fast Exponentiation Calculator provides efficient power calculation using the exponentiation by squaring algorithm (also known as binary exponentiation). It demonstrates how divide-and-conquer techniques can dramatically improve algorithm efficiency, reducing time complexity from O(n) to O(log n).

This tool solves the problem of efficiently calculating large powers, which is essential in cryptography, number theory, and computational mathematics. It includes time complexity analysis to help understand the performance improvements.

**Target Audience**: Students learning algorithms, developers studying optimization techniques, educators teaching algorithm analysis, cryptography enthusiasts, and anyone interested in understanding fast exponentiation.

## Features

- Fast exponentiation algorithm (exponentiation by squaring)
- Iterative and recursive implementations
- Naive method for comparison
- Modular exponentiation support
- Time complexity analysis
- Method comparison with speedup calculation
- Algorithm step tracking
- Execution time measurement
- Detailed analysis reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/fast-exponentiation
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

### Basic Calculation

Calculate power using fast exponentiation:

```bash
python src/main.py 2 10
```

### With Method Selection

Specify calculation method:

```bash
python src/main.py 2 10 --method fast_iterative
python src/main.py 2 10 --method fast_recursive
python src/main.py 2 10 --method naive
```

### Track Algorithm Steps

Show algorithm steps:

```bash
python src/main.py 2 10 --steps
```

### Compare Methods

Compare naive and fast methods:

```bash
python src/main.py 2 10 --compare
```

### Modular Exponentation

Calculate modular exponentiation:

```bash
python src/main.py 2 10 --modular 7
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py 2 10 --report report.txt
```

### Demonstration Mode

Run demonstration with example calculations:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `base`: (Optional) Base number
- `exponent`: (Optional) Exponent (non-negative integer)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Method to use (naive, fast_recursive, fast_iterative)
- `--modular MODULUS`: Calculate modular exponentiation
- `-s, --steps`: Track and show algorithm steps
- `--compare`: Compare naive and fast methods
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example calculations

### Common Use Cases

**Calculate Power:**
1. Run: `python src/main.py 2 10`
2. Review result and time complexity
3. Understand fast exponentiation

**Compare Methods:**
1. Run: `python src/main.py 2 20 --compare`
2. Review speedup factor
3. Understand performance difference

**Study Algorithm:**
1. Run: `python src/main.py 2 10 --steps`
2. Review algorithm steps
3. Understand exponentiation by squaring

**Modular Arithmetic:**
1. Run: `python src/main.py 3 5 --modular 7`
2. Review modular result
3. Understand modular exponentiation

## Project Structure

```
fast-exponentiation/
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

- `src/main.py`: Contains the `FastExponentiationCalculator` class with all methods
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the calculator
- `logs/`: Directory for application log files

## Algorithm Details

### Fast Exponentiation (Exponentiation by Squaring)

The fast exponentiation algorithm uses divide-and-conquer to reduce time complexity:

**Key Insight:**
- If exponent is even: base^exponent = (base^(exponent/2))^2
- If exponent is odd: base^exponent = base * (base^((exponent-1)/2))^2

**Example: Calculating 2^10**

```
2^10 = (2^5)^2
2^5 = 2 * (2^2)^2
2^2 = (2^1)^2
2^1 = 2

Steps:
1. 2^1 = 2
2. 2^2 = (2^1)^2 = 4
3. 2^5 = 2 * (2^2)^2 = 2 * 16 = 32
4. 2^10 = (2^5)^2 = 32^2 = 1024

Total: 4 operations (vs 10 for naive method)
```

### Time Complexity Analysis

| Method | Time Complexity | Space Complexity | Operations for 2^10 |
|--------|----------------|------------------|---------------------|
| Naive | O(n) | O(1) | 10 |
| Fast (Iterative) | O(log n) | O(1) | ~4 |
| Fast (Recursive) | O(log n) | O(log n) | ~4 |

### Algorithm Steps

**Iterative Method:**
1. Initialize result = 1
2. While exponent > 0:
   - If exponent is odd: multiply result by current base
   - Square the base
   - Divide exponent by 2
3. Return result

**Recursive Method:**
1. Base case: if exponent == 0, return 1
2. Base case: if exponent == 1, return base
3. If exponent is even: return (power(base, exponent/2))^2
4. If exponent is odd: return base * (power(base, (exponent-1)/2))^2

### Modular Exponentation

For large numbers, modular exponentiation calculates (base^exponent) mod modulus efficiently:

**Algorithm:**
- Same as fast exponentiation
- Apply modulus after each multiplication
- Prevents integer overflow
- Essential for cryptography (RSA, etc.)

## Applications

### Cryptography

- **RSA Algorithm**: Modular exponentiation for encryption/decryption
- **Diffie-Hellman**: Key exchange using modular exponentiation
- **Digital Signatures**: Signature generation and verification

### Number Theory

- **Fermat's Little Theorem**: Efficient modular inverse calculation
- **Euler's Theorem**: Modular arithmetic operations
- **Prime Testing**: Miller-Rabin primality test

### Computational Mathematics

- **Large Number Calculations**: Handle very large exponents
- **Matrix Exponentiation**: Fast matrix powers
- **Fibonacci Numbers**: Fast Fibonacci calculation

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
- Naive power calculation
- Fast recursive exponentiation
- Fast iterative exponentiation
- Modular exponentiation
- Time complexity analysis
- Method comparison
- Edge cases (zero exponent, negative base, etc.)
- Error handling

## Troubleshooting

### Common Issues

**ValueError: Exponent must be non-negative:**
- Exponent must be >= 0
- Use positive integers for exponents
- For negative exponents, calculate 1/(base^|exponent|) separately

**ValueError: Modulus must be positive:**
- Modulus must be > 0
- Use positive integers for modular arithmetic

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Exponent must be non-negative"**: Exponent is negative. Use non-negative integers.

**"Modulus must be positive"**: Modulus is zero or negative. Use positive integers.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use fast method** for large exponents: `--method fast_iterative`
2. **Compare methods** to see speedup: `--compare`
3. **Track steps** to understand algorithm: `--steps`
4. **Use modular** for large numbers: `--modular MODULUS`
5. **Generate reports** for documentation: `--report report.txt`
6. **Use demonstration mode** to see examples: `--demo`

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
