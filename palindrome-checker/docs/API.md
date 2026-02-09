# API Documentation

## PalindromeChecker Class

The main class for checking if strings are palindromes using multiple algorithms.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the PalindromeChecker with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.
- `ValueError`: If configuration file is empty.

**Side Effects:**
- Loads configuration
- Sets up logging
- Initializes string normalization options

#### `is_palindrome_two_pointer(text: str) -> bool`

Check if string is palindrome using two-pointer approach.

**Parameters:**
- `text` (str): String to check.

**Returns:**
- `bool`: True if palindrome, False otherwise.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

**Algorithm:**
- Uses two pointers starting from both ends
- Moves pointers towards center comparing characters
- Stops when pointers meet or mismatch found

**Example:**
```python
checker = PalindromeChecker()
result = checker.is_palindrome_two_pointer("racecar")
print(result)  # True
```

#### `is_palindrome_reverse(text: str) -> bool`

Check if string is palindrome using reverse comparison.

**Parameters:**
- `text` (str): String to check.

**Returns:**
- `bool`: True if palindrome, False otherwise.

**Time Complexity:** O(n)
**Space Complexity:** O(n) for reversed string

**Algorithm:**
- Reverses the string
- Compares original with reversed string
- Returns True if they match

**Example:**
```python
checker = PalindromeChecker()
result = checker.is_palindrome_reverse("racecar")
print(result)  # True
```

#### `is_palindrome_stack(text: str) -> bool`

Check if string is palindrome using stack-based approach.

**Parameters:**
- `text` (str): String to check.

**Returns:**
- `bool`: True if palindrome, False otherwise.

**Time Complexity:** O(n)
**Space Complexity:** O(n) for stack

**Algorithm:**
- Pushes first half of string onto stack
- Compares second half with stack contents
- Pops from stack and compares with second half characters

**Example:**
```python
checker = PalindromeChecker()
result = checker.is_palindrome_stack("racecar")
print(result)  # True
```

#### `compare_algorithms(text: str, iterations: int = 1) -> Dict[str, any]`

Compare performance of different palindrome checking algorithms.

**Parameters:**
- `text` (str): String to check.
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `text`: Original input text
  - `text_length`: Length of input text
  - `normalized_length`: Length after normalization
  - `iterations`: Number of iterations performed
  - `two_pointer`: Dictionary with result, time, and success status
  - `reverse`: Dictionary with result, time, and success status
  - `stack`: Dictionary with result, time, and success status
  - `fastest`: Name of fastest method (if all succeeded)
  - `fastest_time`: Time of fastest method

**Example:**
```python
checker = PalindromeChecker()
comparison = checker.compare_algorithms("racecar", iterations=100)
print(f"Fastest: {comparison['fastest']}")
print(f"Time: {comparison['fastest_time']*1000:.4f} ms")
```

#### `generate_report(comparison_data: Dict[str, any], output_path: Optional[str] = None) -> str`

Generate performance comparison report.

**Parameters:**
- `comparison_data` (Dict[str, any]): Performance comparison data from compare_algorithms().
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Results from all three approaches
- Timing information for each approach
- Performance summary
- Algorithm complexity information

**Example:**
```python
comparison = checker.compare_algorithms("racecar")
report = checker.generate_report(comparison, output_path="report.txt")
print(report)
```

### Attributes

#### `case_sensitive: bool`

Whether to consider case when checking palindromes, configured from config.yaml.

#### `ignore_spaces: bool`

Whether to ignore spaces when checking palindromes, configured from config.yaml.

#### `ignore_punctuation: bool`

Whether to ignore punctuation when checking palindromes, configured from config.yaml.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### String Normalization

All methods apply normalization based on configuration:
- Case conversion (if `case_sensitive: false`)
- Space removal (if `ignore_spaces: true`)
- Punctuation removal (if `ignore_punctuation: true`)

### Example Usage

```python
from src.main import PalindromeChecker

# Initialize with default config
checker = PalindromeChecker()

# Or with custom config
checker = PalindromeChecker(config_path="custom_config.yaml")

# Check using specific method
result = checker.is_palindrome_two_pointer("racecar")
print(f"Two-pointer: {result}")

result = checker.is_palindrome_reverse("racecar")
print(f"Reverse: {result}")

result = checker.is_palindrome_stack("racecar")
print(f"Stack: {result}")

# Compare all approaches
comparison = checker.compare_algorithms("racecar")
print(f"Fastest: {comparison['fastest']}")

# Generate report
report = checker.generate_report(comparison, output_path="report.txt")
```

### Algorithm Complexity Comparison

**Two-Pointer Approach:**
- Time: O(n) - single pass through string
- Space: O(1) - constant extra space
- Best for: Large strings, production code, memory efficiency

**Reverse Comparison Approach:**
- Time: O(n) - string reversal and comparison
- Space: O(n) - reversed string storage
- Best for: Simple cases, readability, learning

**Stack-Based Approach:**
- Time: O(n) - single pass with stack operations
- Space: O(n) - stack storage
- Best for: Learning stack data structures, demonstrating stack usage

### Performance Notes

- Two-pointer approach is generally fastest and most memory efficient
- Reverse comparison is simple and intuitive
- Stack-based approach demonstrates stack data structure usage
- All approaches produce identical results
- Performance differences become more noticeable with longer strings and more iterations
- Normalization options (case, spaces, punctuation) affect all methods equally

### Edge Cases

- Empty strings are considered palindromes (by definition)
- Single character strings are palindromes
- All methods handle edge cases consistently
- Normalization is applied before checking in all methods
