# String Reverser Algorithm

A Python implementation of string reversal using multiple methods (slicing, loop, recursion) with comprehensive performance comparison. This tool helps understand different approaches to string reversal and their performance characteristics.

## Project Title and Description

The String Reverser tool implements string reversal using five different methods: Python slicing, basic loop, optimized loop, recursion, and built-in reversed() function. It provides detailed performance comparison, timing analysis, and comprehensive reports to help understand the trade-offs between different implementation strategies.

This tool solves the problem of understanding string reversal implementations by providing side-by-side performance comparison and detailed analysis of different algorithmic approaches.

**Target Audience**: Students learning algorithms, developers studying string manipulation, educators teaching computer science concepts, and anyone interested in understanding string reversal and performance analysis.

## Features

- Five different reversal methods: slicing, loop, optimized loop, recursive, built-in
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Error handling for edge cases
- Recursion depth protection

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/string-reverser
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

Compare all methods:

```bash
python src/main.py "Hello World"
```

### Specific Method

Use a specific reversal method:

```bash
python src/main.py "Hello World" --method slicing
python src/main.py "Hello World" --method loop
python src/main.py "Hello World" --method recursive
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py "Hello World" --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py "Hello World" --report report.txt
```

### Command-Line Arguments

- `text`: (Required) String to reverse
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Reversal method - slicing, loop, loop_optimized, recursive, builtin, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Methods:**
1. Run: `python src/main.py "Hello World"`
2. Review timing for each method
3. Identify fastest method

**Study Algorithms:**
1. Use specific method: `python src/main.py "test" --method recursive`
2. Review logs to see algorithm execution
3. Understand different approaches

**Performance Analysis:**
1. Test with different string lengths
2. Use multiple iterations: `python src/main.py "long string" --iterations 1000`
3. Generate reports for detailed metrics

## Project Structure

```
string-reverser/
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

- `src/main.py`: Contains the `StringReverser` class and main logic
- `config.yaml`: Configuration file with recursion and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Reversal Methods

**Slicing Method:**
- Uses Python's slice notation: `text[::-1]`
- Most Pythonic and concise
- Time Complexity: O(n)
- Space Complexity: O(n)

**Loop Method:**
- Builds reversed string character by character
- Prepends each character to result
- Time Complexity: O(n)
- Space Complexity: O(n)

**Optimized Loop Method:**
- Uses in-place swapping with list
- More memory efficient
- Time Complexity: O(n)
- Space Complexity: O(1) for the algorithm itself

**Recursive Method:**
- Uses function calls to reverse string
- Recursively reverses substring and appends first character
- Time Complexity: O(n)
- Space Complexity: O(n) due to call stack

**Built-in reversed() Method:**
- Uses Python's built-in reversed() function
- Joins reversed iterator
- Time Complexity: O(n)
- Space Complexity: O(n)

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
- All reversal methods with various inputs
- Edge cases (empty string, single character, special characters)
- Performance comparison functionality
- Error handling
- Report generation

## Troubleshooting

### Common Issues

**RecursionError:**
- String is too long for recursive approach
- Increase max_depth in config.yaml (not recommended for very long strings)
- Use iterative methods for long strings

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Ensure config.yaml exists and is valid YAML
- Check file permissions
- Verify configuration structure matches expected format

### Error Messages

**"Maximum recursion depth exceeded"**: String is too long for recursive approach. Use iterative method or increase max_depth.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use slicing method** for production code (most Pythonic and efficient)
2. **Use recursive method** for learning and small strings
3. **Compare performance** to understand trade-offs
4. **Use multiple iterations** for accurate timing measurements
5. **Review logs** to see algorithm execution details

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
