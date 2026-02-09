# Palindrome Checker

A Python implementation of palindrome checking using multiple algorithms: two-pointer, reverse comparison, and stack-based approaches. This tool provides comprehensive performance comparison and detailed analysis of different algorithmic strategies.

## Project Title and Description

The Palindrome Checker tool implements three different algorithms to check if a string is a palindrome: two-pointer approach, reverse comparison, and stack-based method. It provides detailed performance comparison, timing analysis, and comprehensive reports to help understand the trade-offs between different implementation strategies.

This tool solves the problem of understanding palindrome checking implementations by providing side-by-side performance comparison and detailed analysis of different algorithmic approaches.

**Target Audience**: Students learning algorithms, developers studying string manipulation, educators teaching computer science concepts, and anyone interested in understanding palindrome checking and performance analysis.

## Features

- Two-pointer palindrome checking algorithm
- Reverse comparison palindrome checking algorithm
- Stack-based palindrome checking algorithm
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Configurable string normalization (case sensitivity, spaces, punctuation)
- Error handling for edge cases

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/palindrome-checker
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

The tool uses a YAML configuration file to define string processing options and logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**String Processing Options:**
- `options.case_sensitive`: Whether to consider case when checking (default: false)
- `options.ignore_spaces`: Whether to ignore spaces (default: false)
- `options.ignore_punctuation`: Whether to ignore punctuation (default: false)

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
options:
  case_sensitive: false
  ignore_spaces: false
  ignore_punctuation: false

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Performance Comparison (Default)

Compare all algorithms:

```bash
python src/main.py "racecar"
```

### Specific Algorithm

Use a specific checking method:

```bash
python src/main.py "racecar" --method two_pointer
python src/main.py "racecar" --method reverse
python src/main.py "racecar" --method stack
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py "racecar" --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py "racecar" --report report.txt
```

### Command-Line Arguments

- `text`: (Required) Text string to check for palindrome
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Checking method - two_pointer, reverse, stack, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Algorithms:**
1. Run: `python src/main.py "racecar"`
2. Review timing for each algorithm
3. Identify fastest algorithm

**Study Algorithms:**
1. Use specific method: `python src/main.py "racecar" --method two_pointer`
2. Review logs to see algorithm execution
3. Understand different approaches

**Performance Analysis:**
1. Test with different string lengths
2. Use multiple iterations: `python src/main.py "racecar" --iterations 1000`
3. Generate reports for detailed metrics

**Case-Insensitive Checking:**
1. Configure `case_sensitive: false` in config.yaml
2. Run: `python src/main.py "RaceCar"`
3. Will check as palindrome

**Ignore Spaces:**
1. Configure `ignore_spaces: true` in config.yaml
2. Run: `python src/main.py "race car"`
3. Will check as palindrome

## Project Structure

```
palindrome-checker/
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

- `src/main.py`: Contains the `PalindromeChecker` class and main logic
- `config.yaml`: Configuration file with string processing and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Palindrome Checking Methods

**Two-Pointer Approach:**
- Uses two pointers starting from both ends
- Moves pointers towards center comparing characters
- Time Complexity: O(n)
- Space Complexity: O(1)
- Most memory efficient
- Generally fastest for large strings

**Reverse Comparison Approach:**
- Reverses the string and compares with original
- Time Complexity: O(n)
- Space Complexity: O(n) for reversed string
- Simple and intuitive
- Easy to understand

**Stack-Based Approach:**
- Uses stack to reverse first half
- Compares second half with stack contents
- Time Complexity: O(n)
- Space Complexity: O(n) for stack
- Demonstrates stack data structure usage
- Good for learning stack operations

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
- Palindrome checking with various inputs
- Edge cases (empty string, single character, special characters)
- Performance comparison functionality
- Error handling
- Report generation
- All three implementation approaches
- String normalization options

## Troubleshooting

### Common Issues

**Empty String:**
- Empty strings are considered palindromes (by definition)
- This is expected behavior

**Special Characters:**
- Configure `ignore_punctuation: true` to ignore punctuation
- Configure `ignore_spaces: true` to ignore spaces
- Configure `case_sensitive: false` for case-insensitive checking

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

**"Invalid YAML"**: The config.yaml file has syntax errors. Check YAML syntax.

### Best Practices

1. **Use two-pointer approach** for large strings and production code
2. **Use reverse comparison** for simple cases and readability
3. **Use stack-based approach** for learning stack data structures
4. **Compare performance** to understand trade-offs
5. **Use multiple iterations** for accurate timing measurements
6. **Review logs** to see algorithm execution details
7. **Configure normalization** based on requirements (case, spaces, punctuation)

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
