# Stack Data Structure

A Python implementation of stack data structure with push, pop, peek operations and demonstration of its use in expression evaluation (postfix and infix). This tool provides comprehensive stack operations and expression evaluation capabilities.

## Project Title and Description

The Stack Data Structure tool implements a complete stack data structure with all fundamental operations (push, pop, peek) and demonstrates its practical application in evaluating mathematical expressions. It supports both postfix (Reverse Polish Notation) and infix expression evaluation, showing how stacks are used in real-world algorithms.

This tool solves the problem of understanding stack data structures and their applications by providing a complete implementation with practical examples in expression evaluation, making it ideal for educational purposes.

**Target Audience**: Students learning data structures, developers studying stack implementations, educators teaching computer science concepts, and anyone interested in understanding stacks and expression evaluation.

## Features

- Complete stack data structure implementation
- Push, pop, peek operations
- Expression evaluation (postfix and infix)
- Infix to postfix conversion
- Stack operations demonstration
- Comprehensive logging
- Detailed evaluation reports
- Error handling for edge cases

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/stack-data-structure
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

### Stack Operations Demonstration

Demonstrate basic stack operations:

```bash
python src/main.py "demo" --demo
```

### Evaluate Postfix Expression

Evaluate a postfix (Reverse Polish Notation) expression:

```bash
python src/main.py "3 4 + 2 *" --type postfix
```

### Evaluate Infix Expression

Evaluate an infix expression:

```bash
python src/main.py "(3 + 4) * 2" --type infix
```

### Auto-detect Expression Type

Let the tool detect expression type:

```bash
python src/main.py "3 4 + 2 *" --type auto
python src/main.py "(3 + 4) * 2" --type auto
```

### Generate Report

Generate evaluation report:

```bash
python src/main.py "(3 + 4) * 2" --type infix --report report.txt
```

### Command-Line Arguments

- `expression`: (Required) Expression to evaluate or "demo" for demonstration
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-t, --type`: Expression type - postfix, infix, or auto (default: auto)
- `-r, --report`: Output path for evaluation report
- `--demo`: Run stack operations demonstration

### Common Use Cases

**Learn Stack Operations:**
1. Run: `python src/main.py "demo" --demo`
2. Observe push, pop, peek operations
3. Understand stack behavior

**Evaluate Postfix Expressions:**
1. Run: `python src/main.py "3 4 + 2 *" --type postfix`
2. Review evaluation process
3. Understand stack usage in postfix evaluation

**Evaluate Infix Expressions:**
1. Run: `python src/main.py "(3 + 4) * 2" --type infix`
2. See infix to postfix conversion
3. Review evaluation result

**Study Expression Evaluation:**
1. Test with different expressions
2. Review logs to see stack operations
3. Generate reports for detailed analysis

## Project Structure

```
stack-data-structure/
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

- `src/main.py`: Contains the `Stack` and `ExpressionEvaluator` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Stack Data Structure

**Operations:**
- `push(item)`: Add item to top of stack - O(1)
- `pop()`: Remove and return top item from stack - O(1)
- `peek()`: View top item without removing - O(1)
- `is_empty()`: Check if stack is empty - O(1)
- `size()`: Get number of items - O(1)

**Characteristics:**
- LIFO (Last In, First Out) data structure
- Implemented using Python list
- All operations are O(1) time complexity
- O(n) space complexity for n items

### Expression Evaluation

**Postfix Evaluation:**
1. Read tokens from left to right
2. If operand, push onto stack
3. If operator, pop two operands, apply operator, push result
4. Final result is on stack

**Infix to Postfix Conversion:**
1. Use stack to handle operator precedence
2. Process tokens and operators according to precedence
3. Handle parentheses correctly
4. Output postfix expression

**Infix Evaluation:**
1. Convert infix to postfix
2. Evaluate postfix expression

### Supported Operators

- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `^`: Exponentiation

### Operator Precedence

1. `^` (highest)
2. `*`, `/`
3. `+`, `-` (lowest)

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
- Stack operations (push, pop, peek, is_empty, size)
- Edge cases (empty stack, invalid operations)
- Postfix expression evaluation
- Infix expression evaluation
- Infix to postfix conversion
- Error handling
- Report generation

## Troubleshooting

### Common Issues

**IndexError: Stack is empty:**
- Attempted to pop or peek from empty stack
- Check that stack has items before operations

**ValueError: Invalid expression:**
- Expression has syntax errors
- Check operator and operand placement
- Verify parentheses are balanced

**Division by zero:**
- Expression contains division by zero
- Check expression for `/ 0` or `/0.0`

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Stack is empty"**: Attempted to pop or peek from empty stack. Ensure stack has items.

**"Invalid expression"**: Expression has syntax errors. Check format and operators.

**"Division by zero"**: Expression contains division by zero. Check operands.

**"Mismatched parentheses"**: Parentheses in expression are not balanced.

### Best Practices

1. **Use postfix notation** for simpler evaluation
2. **Check stack size** before operations in custom code
3. **Handle errors** when evaluating expressions
4. **Review logs** to understand stack operations
5. **Test with simple expressions** first
6. **Use parentheses** in infix expressions for clarity

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
