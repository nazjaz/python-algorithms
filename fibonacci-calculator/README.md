# Fibonacci Calculator

A Python implementation of Fibonacci number calculation using naive recursion, dynamic programming with memoization, and iterative approaches. This tool provides comprehensive performance comparison and detailed analysis of different algorithmic strategies.

## Project Title and Description

The Fibonacci Calculator tool implements three different approaches to calculate Fibonacci numbers: naive recursion, dynamic programming with memoization, and iterative method. It provides detailed performance comparison, timing analysis, and comprehensive reports to help understand the trade-offs between different implementation strategies and the power of memoization.

This tool solves the problem of understanding Fibonacci calculation implementations by providing side-by-side performance comparison and detailed analysis of different algorithmic approaches, demonstrating the significant performance improvement achieved through dynamic programming and memoization.

**Target Audience**: Students learning algorithms and dynamic programming, developers studying optimization techniques, educators teaching computer science concepts, and anyone interested in understanding Fibonacci calculation and performance optimization.

## Features

- Naive recursive Fibonacci calculation
- Dynamic programming with memoization
- Iterative Fibonacci calculation
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Recursive call counting
- Memoization cache statistics
- Error handling for edge cases

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/fibonacci-calculator
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

The tool uses a YAML configuration file to define recursion limits and logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Recursion Settings:**
- `recursion.max_depth`: Maximum recursion depth allowed (default: 1000)

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
recursion:
  max_depth: 1000

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Performance Comparison (Default)

Compare all approaches:

```bash
python src/main.py 10
```

### Specific Method

Use a specific calculation method:

```bash
python src/main.py 10 --method naive
python src/main.py 10 --method memoized
python src/main.py 10 --method iterative
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py 10 --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py 10 --report report.txt
```

### Command-Line Arguments

- `n`: (Required) Position in Fibonacci sequence (0-indexed)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Calculation method - naive, memoized, iterative, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Approaches:**
1. Run: `python src/main.py 20`
2. Review timing for each approach
3. Observe dramatic speedup with memoization

**Study Dynamic Programming:**
1. Use memoized method: `python src/main.py 20 --method memoized`
2. Review logs to see cache hits
3. Understand memoization benefits

**Performance Analysis:**
1. Test with different values of n
2. Use multiple iterations: `python src/main.py 20 --iterations 1000`
3. Generate reports for detailed metrics
4. Observe exponential vs linear time complexity

**Understand Recursion:**
1. Use naive method: `python src/main.py 10 --method naive`
2. Review recursive call count
3. Compare with memoized approach

## Project Structure

```
fibonacci-calculator/
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

- `src/main.py`: Contains the `FibonacciCalculator` class and main logic
- `config.yaml`: Configuration file with recursion and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Fibonacci Calculation Methods

**Naive Recursion:**
- Recursively calculates fib(n-1) + fib(n-2)
- Time Complexity: O(2^n) - exponential
- Space Complexity: O(n) - call stack
- Recalculates same values multiple times
- Very slow for large n

**Dynamic Programming with Memoization:**
- Uses cache to store previously calculated values
- Time Complexity: O(n) - linear
- Space Complexity: O(n) - memoization cache + call stack
- Avoids redundant calculations
- Much faster than naive recursion

**Iterative:**
- Uses loop to build Fibonacci sequence
- Time Complexity: O(n) - linear
- Space Complexity: O(1) - constant
- Most efficient in terms of space
- Fast and simple

### Performance Comparison

For n=30:
- Naive recursion: ~1 second (millions of recursive calls)
- Memoized: ~0.001 seconds (n recursive calls)
- Iterative: ~0.0001 seconds (n iterations)

The memoized approach provides dramatic speedup (1000x+) compared to naive recursion for larger values of n.

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
- Calculation with various inputs
- Edge cases (n=0, n=1, negative n)
- Performance comparison functionality
- Error handling (recursion depth, invalid input)
- Report generation
- All three implementation approaches
- Memoization cache behavior

## Troubleshooting

### Common Issues

**RecursionError:**
- n is too large for recursive approaches
- Increase max_depth in config.yaml (not recommended for very large n)
- Use iterative approach for large n

**Very Slow Performance:**
- Naive recursion is exponential - avoid for n > 30
- Use memoized or iterative approach for larger values
- Consider iterative approach for very large n

**ValueError: n must be non-negative:**
- n must be >= 0
- Check input value

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Maximum recursion depth exceeded"**: n is too large for recursive approach. Use iterative method or increase max_depth.

**"n must be non-negative"**: Input value is negative. Fibonacci sequence is only defined for non-negative integers.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use iterative approach** for large n and production code
2. **Use memoized approach** for learning dynamic programming
3. **Use naive recursion** only for small n (n < 20) or educational purposes
4. **Compare performance** to understand trade-offs
5. **Use multiple iterations** for accurate timing measurements
6. **Review logs** to see algorithm execution details
7. **Observe speedup** achieved through memoization

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
