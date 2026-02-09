# Balanced Parentheses Validator API Documentation

## Overview

The Balanced Parentheses Validator provides a stack-based solution for validating balanced parentheses, brackets, and braces in strings. It supports multiple bracket types: `()`, `[]`, `{}`, `<>`.

## Classes

### BalancedParenthesesValidator

Main class for validating balanced parentheses using stack data structure.

#### Constructor

```python
BalancedParenthesesValidator(config_path: str = "config.yaml") -> None
```

Initialize validator with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### is_balanced

```python
is_balanced(expression: str) -> bool
```

Check if parentheses in expression are balanced using stack.

**Parameters:**
- `expression` (str): String expression to validate

**Returns:**
- `bool`: True if parentheses are balanced, False otherwise

**Example:**
```python
validator = BalancedParenthesesValidator()
result = validator.is_balanced("()[]{}")
# Returns: True
```

##### get_unmatched_brackets

```python
get_unmatched_brackets(expression: str) -> List[str]
```

Get list of unmatched brackets in expression.

**Parameters:**
- `expression` (str): String expression to analyze

**Returns:**
- `List[str]`: List of unmatched bracket characters. Empty list if balanced.

**Example:**
```python
unmatched = validator.get_unmatched_brackets("(((")
# Returns: ['(', '(', '(']
```

##### validate_with_details

```python
validate_with_details(expression: str) -> Dict[str, any]
```

Validate expression and return detailed results.

**Parameters:**
- `expression` (str): String expression to validate

**Returns:**
- `Dict[str, any]`: Dictionary containing:
  - `is_balanced` (bool): Boolean indicating if expression is balanced
  - `unmatched_brackets` (List[str]): List of unmatched brackets
  - `bracket_count` (Dict[str, int]): Dictionary with counts of each bracket type

**Example:**
```python
result = validator.validate_with_details("()[]{}")
# Returns: {
#   'is_balanced': True,
#   'unmatched_brackets': [],
#   'bracket_count': {'(': 1, ')': 1, '[': 1, ']': 1, '{': 1, '}': 1, '<': 0, '>': 0}
# }
```

##### generate_report

```python
generate_report(
    expression: str,
    result: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate validation report.

**Parameters:**
- `expression` (str): Expression that was validated
- `result` (Dict[str, any]): Validation result dictionary from `validate_with_details`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If insufficient permissions to write file

**Example:**
```python
result = validator.validate_with_details("()[]{}")
report = validator.generate_report("()[]{}", result, output_path="report.txt")
```

## Supported Bracket Types

- Parentheses: `()` 
- Square brackets: `[]`
- Curly braces: `{}`
- Angle brackets: `<>`

## Algorithm Complexity

- **Time Complexity**: O(n) where n is the length of the expression
- **Space Complexity**: O(n) for stack storage in worst case

## Stack Operations

The validator uses the following stack operations:
- `push()`: Add opening bracket to stack - O(1)
- `pop()`: Remove opening bracket when closing bracket found - O(1)
- `is_empty()`: Check if stack is empty - O(1)

## Usage Examples

### Basic Validation

```python
from src.main import BalancedParenthesesValidator

validator = BalancedParenthesesValidator()
print(validator.is_balanced("()[]{}"))  # True
print(validator.is_balanced("([)]"))   # False
```

### Detailed Validation

```python
result = validator.validate_with_details("()[]{}")
print(f"Balanced: {result['is_balanced']}")
print(f"Bracket counts: {result['bracket_count']}")
```

### Generate Report

```python
result = validator.validate_with_details("()[]{}")
report = validator.generate_report("()[]{}", result, "report.txt")
```
