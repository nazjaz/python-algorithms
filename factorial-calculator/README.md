# Factorial Calculator

A Python implementation of factorial calculation using both iterative and recursive approaches with comprehensive performance comparison. This tool helps understand the differences between iterative and recursive implementations and their performance characteristics.

## Project Title and Description

The Factorial Calculator tool implements factorial calculation using three different approaches: iterative, recursive, and memoized recursive. It provides detailed performance comparison, timing analysis, and comprehensive reports to help understand the trade-offs between different implementation strategies.

This tool solves the problem of understanding factorial calculation implementations by providing side-by-side performance comparison and detailed analysis of different algorithmic approaches.

**Target Audience**: Students learning algorithms, developers studying recursion vs iteration, educators teaching computer science concepts, and anyone interested in understanding factorial calculation and performance analysis.

## Features

- Iterative factorial calculation
- Recursive factorial calculation
- Memoized recursive factorial calculation
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Error handling for edge cases
- Recursion depth protection

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/factorial-calculator
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

### Iterative Approach Only

```bash
python src/main.py 10 --method iterative
```

### Recursive Approach Only

```bash
python src/main.py 10 --method recursive
```

### Memoized Approach Only

```bash
python src/main.py 10 --method memoized
```

### Generate Report

```bash
python src/main.py 10 --report report.txt
```

### Command-Line Arguments

- `number`: (Required) Non-negative integer to calculate factorial for
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Calculation method - iterative, recursive, memoized, or compare (default: compare)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Approaches:**
1. Run: `python src/main.py 10`
2. Review timing for each approach
3. Identify fastest method for given input

**Study Recursion:**
1. Use recursive method: `python src/main.py 5 --method recursive`
2. Review logs to see call stack
3. Understand recursion depth

**Performance Analysis:**
1. Test with different numbers
2. Generate reports: `python src/main.py 20 --report analysis.txt`
3. Compare performance trends

## Project Structure

```
factorial-calculator/
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

- `src/main.py`: Contains the `FactorialCalculator` class and main logic
- `config.yaml`: Configuration file with recursion and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Factorial Definition

Factorial of a non-negative integer n (denoted as n!) is the product of all positive integers less than or equal to n.

- 0! = 1
- 1! = 1
- n! = n × (n-1) × (n-2) × ... × 2 × 1

### Implementation Approaches

**Iterative Approach:**
- Uses a loop to multiply numbers from 1 to n
- Time Complexity: O(n)
- Space Complexity: O(1)
- No recursion overhead
- Generally faster for large numbers

**Recursive Approach:**
- Uses function calls to break problem into smaller subproblems
- Time Complexity: O(n)
- Space Complexity: O(n) due to call stack
- More intuitive for some problems
- May hit recursion limits for large numbers

**Memoized Recursive Approach:**
- Recursive with caching of computed results
- Time Complexity: O(n)
- Space Complexity: O(n) for memoization table
- Combines recursion benefits with performance optimization
- Useful when same values are computed multiple times

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
- Factorial calculation with various inputs
- Edge cases (0, 1, negative numbers)
- Performance comparison functionality
- Error handling
- Report generation
- All three implementation approaches

## Troubleshooting

### Common Issues

**RecursionError:**
- Input number is too large for recursive approach
- Increase max_depth in config.yaml (not recommended for very large numbers)
- Use iterative approach for large numbers

**ValueError for Negative Numbers:**
- Factorial is not defined for negative numbers
- Ensure input is non-negative

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Factorial is not defined for negative numbers"**: Input must be non-negative integer.

**"Maximum recursion depth exceeded"**: Number is too large for recursive approach. Use iterative method or increase max_depth.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use iterative approach** for large numbers (typically > 1000)
2. **Use recursive approach** for learning and small numbers
3. **Compare performance** to understand trade-offs
4. **Review logs** to see algorithm execution details
5. **Generate reports** for performance analysis

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
