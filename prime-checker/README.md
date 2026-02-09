# Prime Checker Algorithm

A Python implementation of prime number checking using trial division method with optimizations for even numbers. This tool efficiently determines if a number is prime and provides detailed analysis of the algorithm's performance.

## Project Title and Description

The Prime Checker tool implements an optimized trial division algorithm to check if numbers are prime. It uses several key optimizations including early even number detection, testing only odd divisors, and limiting checks to the square root of the number. The tool provides comprehensive analysis and reporting capabilities.

This tool solves the problem of efficiently checking primality by demonstrating optimization techniques that significantly reduce the number of divisions needed compared to naive approaches.

**Target Audience**: Students learning algorithms, developers studying number theory, educators teaching computer science concepts, and anyone interested in understanding prime number algorithms and optimization techniques.

## Features

- Optimized trial division algorithm
- Early detection of even numbers (except 2)
- Only tests odd divisors for efficiency
- Limits checks to square root of number
- Detailed division counting and analysis
- Find all primes in a given range
- Comprehensive performance reports
- Step-by-step logging of algorithm execution

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/prime-checker
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

### Check Single Number

Check if a number is prime:

```bash
python src/main.py 17
```

### With Detailed Analysis

Show detailed analysis:

```bash
python src/main.py 17 --analysis
```

### Find Primes in Range

Find all primes in a range:

```bash
python src/main.py --range 1 100
```

### Generate Report

Generate analysis report:

```bash
python src/main.py 17 --report report.txt
```

### Command-Line Arguments

- `number`: (Optional) Number to check for primality
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-r, --range START END`: Find all primes in range [START, END]
- `--report`: Output path for analysis report
- `--analysis`: Show detailed analysis information

### Common Use Cases

**Check Primality:**
1. Run: `python src/main.py 29`
2. Get immediate result
3. Review divisions performed

**Find Primes:**
1. Use range option: `python src/main.py --range 1 50`
2. Get list of all primes in range
3. Study prime distribution

**Performance Analysis:**
1. Test with different numbers
2. Use `--analysis` to see optimization benefits
3. Generate reports for detailed metrics

## Project Structure

```
prime-checker/
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

- `src/main.py`: Contains the `PrimeChecker` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Trial Division Method

Trial division is a simple method to check if a number is prime by testing divisibility by all integers up to the square root of the number.

**Basic Algorithm:**
1. Check if number is less than 2 (not prime)
2. Check if number is 2 (prime)
3. Check if number is even (not prime, except 2)
4. Test divisibility by odd numbers from 3 to √n
5. If no divisor found, number is prime

### Optimizations

**Even Number Optimization:**
- Immediately reject even numbers (except 2)
- Reduces checks by approximately 50% for even numbers
- Only test odd divisors (step by 2)

**Square Root Limit:**
- Only test divisors up to √n
- If n has a factor greater than √n, it must have a corresponding factor less than √n
- Reduces complexity from O(n) to O(√n)

**Time Complexity:** O(√n)
**Space Complexity:** O(1)

**Comparison Count:**
- Naive approach: n-1 divisions
- Optimized approach: ~√n/2 divisions (for odd numbers)
- Improvement: Significant reduction, especially for large numbers

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
- Prime checking for various numbers
- Edge cases (0, 1, 2, small primes, large numbers)
- Even number optimization
- Range finding functionality
- Analysis data correctness
- Report generation
- Error handling

## Troubleshooting

### Common Issues

**Large Number Performance:**
- Trial division becomes slow for very large numbers
- Consider using probabilistic methods for very large inputs
- Current implementation is optimized but still O(√n)

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Ensure config.yaml exists and is valid YAML
- Check file permissions
- Verify configuration structure matches expected format

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

**"Failed to save report"**: Cannot write to output directory. Check permissions and disk space.

### Best Practices

1. **Use for moderate-sized numbers** (up to ~10^12 for reasonable performance)
2. **Review analysis** to understand optimization benefits
3. **Use range finding** to discover primes in intervals
4. **Study division counts** to understand algorithm efficiency
5. **Compare with naive approach** to appreciate optimizations

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
