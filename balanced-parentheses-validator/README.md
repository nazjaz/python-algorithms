# Balanced Parentheses Validator

A Python implementation of a balanced parentheses validator using a stack data structure. This tool validates if parentheses, brackets, and braces are properly balanced in a given string, supporting multiple bracket types: `()`, `[]`, `{}`, `<>`.

## Project Title and Description

The Balanced Parentheses Validator provides a complete stack-based solution for validating balanced parentheses in strings. It demonstrates the practical application of stack data structures in solving real-world problems like syntax validation, expression parsing, and code analysis.

This tool solves the problem of quickly and efficiently checking if brackets in an expression are properly matched and balanced, which is essential for parsing expressions, validating code syntax, and ensuring proper nesting in various programming contexts.

**Target Audience**: Students learning data structures, developers studying stack implementations, educators teaching computer science concepts, and anyone interested in understanding how stacks are used in practical algorithms.

## Features

- Stack-based balanced parentheses validation
- Support for multiple bracket types: `()`, `[]`, `{}`, `<>`
- Detailed validation results with bracket counts
- Unmatched bracket identification
- Comprehensive logging
- Detailed validation reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/balanced-parentheses-validator
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

### Basic Validation

Validate a simple expression:

```bash
python src/main.py "()[]{}"
```

### Detailed Validation

Show detailed validation results including bracket counts:

```bash
python src/main.py "()[]{}" --details
```

### Generate Report

Generate a detailed validation report:

```bash
python src/main.py "()[]{}" --details --report report.txt
```

### Demonstration Mode

Run demonstration with example expressions:

```bash
python src/main.py --demo
```

### Command-Line Arguments

- `expression`: (Optional) Expression to validate for balanced parentheses
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-d, --details`: Show detailed validation results
- `-r, --report`: Output path for validation report
- `--demo`: Run demonstration with example expressions

### Common Use Cases

**Validate Simple Expression:**
1. Run: `python src/main.py "()[]{}"`
2. Review validation result
3. Understand stack-based validation

**Get Detailed Analysis:**
1. Run: `python src/main.py "()[]{}" --details`
2. Review bracket counts
3. Check for unmatched brackets

**Validate Code-Like Expressions:**
1. Run: `python src/main.py "function() { return [1, 2]; }"`
2. Verify balanced brackets in code snippets
3. Use for syntax validation

**Study Stack Operations:**
1. Run: `python src/main.py --demo`
2. Review different validation scenarios
3. Understand stack behavior

## Project Structure

```
balanced-parentheses-validator/
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

- `src/main.py`: Contains the `BalancedParenthesesValidator` class with stack-based validation logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the validator
- `logs/`: Directory for application log files

## Algorithm Details

### Stack Data Structure

The validator uses a stack (implemented as a Python list) to track opening brackets. The stack follows LIFO (Last In, First Out) principle, which is perfect for matching nested brackets.

**Operations Used:**
- `push()`: Add opening bracket to stack - O(1)
- `pop()`: Remove opening bracket when closing bracket found - O(1)
- `is_empty()`: Check if stack is empty - O(1)

### Validation Algorithm

**Algorithm Steps:**
1. Initialize an empty stack
2. Iterate through each character in the expression
3. If character is an opening bracket: push onto stack
4. If character is a closing bracket:
   - If stack is empty: expression is unbalanced
   - Pop from stack and check if brackets match
   - If brackets don't match: expression is unbalanced
5. After processing all characters:
   - If stack is empty: expression is balanced
   - If stack is not empty: expression is unbalanced

**Time Complexity:** O(n) where n is the length of the expression
**Space Complexity:** O(n) for stack storage in worst case (all opening brackets)

### Supported Bracket Types

- `()`: Parentheses
- `[]`: Square brackets
- `[]`: Curly braces
- `<>`: Angle brackets

### Example Validation Process

**Expression:** `([{}])`

1. `(` - Push onto stack: `[`(`]`
2. `[` - Push onto stack: `[`(`, `[`]`
3. `{` - Push onto stack: `[`(`, `[`, `{`]`
4. `}` - Pop `{`, matches `}`: `[`(`, `[`]`
5. `]` - Pop `[`, matches `]`: `[`(`]`
6. `)` - Pop `(`, matches `)`: `[]`
7. Stack is empty: **BALANCED**

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
- Balanced expressions (simple, nested, mixed types)
- Unbalanced expressions (unmatched, mismatched, wrong order)
- Edge cases (empty string, no brackets, partial matches)
- Stack operations and bracket matching
- Detailed validation and reporting
- Error handling

## Troubleshooting

### Common Issues

**ValueError: Configuration file is empty:**
- Config file exists but is empty or invalid
- Check that config.yaml has proper YAML structure

**FileNotFoundError: Configuration file not found:**
- Config file path is incorrect
- Use `-c` or `--config` to specify correct path

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

**"Invalid YAML in configuration file"**: Config file has syntax errors. Verify YAML format.

**"Failed to save report"**: Cannot write report file. Check file permissions and path.

### Best Practices

1. **Use detailed mode** for comprehensive analysis: `--details`
2. **Generate reports** for documentation: `--report report.txt`
3. **Check logs** to understand validation process
4. **Test with simple expressions** first
5. **Use demonstration mode** to see examples: `--demo`

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
