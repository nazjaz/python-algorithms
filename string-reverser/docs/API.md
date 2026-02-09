# API Documentation

## StringReverser Class

The main class for reversing strings using multiple methods and comparing performance.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the StringReverser with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.
- `ValueError`: If configuration file is empty.

**Side Effects:**
- Loads configuration
- Sets up logging
- Initializes recursion depth limit

#### `reverse_slicing(text: str) -> str`

Reverse string using Python slicing.

**Parameters:**
- `text` (str): String to reverse.

**Returns:**
- `str`: Reversed string.

**Time Complexity:** O(n)
**Space Complexity:** O(n)

**Example:**
```python
reverser = StringReverser()
result = reverser.reverse_slicing("hello")
print(result)  # "olleh"
```

#### `reverse_loop(text: str) -> str`

Reverse string using loop method.

**Parameters:**
- `text` (str): String to reverse.

**Returns:**
- `str`: Reversed string.

**Time Complexity:** O(n)
**Space Complexity:** O(n)

**Example:**
```python
reverser = StringReverser()
result = reverser.reverse_loop("hello")
print(result)  # "olleh"
```

#### `reverse_loop_optimized(text: str) -> str`

Reverse string using optimized loop with in-place swapping.

**Parameters:**
- `text` (str): String to reverse.

**Returns:**
- `str`: Reversed string.

**Time Complexity:** O(n)
**Space Complexity:** O(1) for algorithm itself

**Example:**
```python
reverser = StringReverser()
result = reverser.reverse_loop_optimized("hello")
print(result)  # "olleh"
```

#### `reverse_recursive(text: str, depth: int = 0) -> str`

Reverse string using recursive method.

**Parameters:**
- `text` (str): String to reverse.
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `str`: Reversed string.

**Raises:**
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(n)
**Space Complexity:** O(n) due to call stack

**Example:**
```python
reverser = StringReverser()
result = reverser.reverse_recursive("hello")
print(result)  # "olleh"
```

#### `reverse_builtin(text: str) -> str`

Reverse string using built-in reversed() function.

**Parameters:**
- `text` (str): String to reverse.

**Returns:**
- `str`: Reversed string.

**Time Complexity:** O(n)
**Space Complexity:** O(n)

**Example:**
```python
reverser = StringReverser()
result = reverser.reverse_builtin("hello")
print(result)  # "olleh"
```

#### `compare_performance(text: str, iterations: int = 1) -> Dict[str, any]`

Compare performance of different string reversal methods.

**Parameters:**
- `text` (str): String to reverse.
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `input_length`: Length of input string
  - `iterations`: Number of iterations performed
  - `slicing`: Dictionary with result, time, and success status
  - `loop`: Dictionary with result, time, and success status
  - `loop_optimized`: Dictionary with result, time, and success status
  - `recursive`: Dictionary with result, time, and success status
  - `builtin`: Dictionary with result, time, and success status
  - `fastest`: Name of fastest method (if all succeeded)
  - `fastest_time`: Time of fastest method

**Example:**
```python
reverser = StringReverser()
comparison = reverser.compare_performance("hello", iterations=100)
print(f"Fastest: {comparison['fastest']}")
print(f"Time: {comparison['fastest_time']*1000:.4f} ms")
```

#### `generate_report(comparison_data: Dict[str, any], output_path: Optional[str] = None) -> str`

Generate performance comparison report.

**Parameters:**
- `comparison_data` (Dict[str, any]): Performance comparison data from compare_performance().
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Results from all five methods
- Timing information for each method
- Performance summary
- Algorithm complexity information

**Example:**
```python
comparison = reverser.compare_performance("hello")
report = reverser.generate_report(comparison, output_path="report.txt")
print(report)
```

### Attributes

#### `max_recursive_depth: int`

Maximum recursion depth allowed, configured from config.yaml.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import StringReverser

# Initialize with default config
reverser = StringReverser()

# Or with custom config
reverser = StringReverser(config_path="custom_config.yaml")

# Reverse using specific method
result = reverser.reverse_slicing("hello")
print(result)

# Compare all methods
comparison = reverser.compare_performance("hello", iterations=1000)
print(f"Fastest: {comparison['fastest']}")

# Generate report
report = reverser.generate_report(comparison, output_path="report.txt")
```

### Algorithm Complexity Comparison

**Slicing Method:**
- Time: O(n) - single slice operation
- Space: O(n) - creates new string
- Best for: Production code, most Pythonic

**Loop Method:**
- Time: O(n) - single pass through string
- Space: O(n) - builds new string
- Best for: Learning, explicit algorithm

**Optimized Loop Method:**
- Time: O(n) - single pass with swapping
- Space: O(1) - in-place algorithm
- Best for: Memory-constrained environments

**Recursive Method:**
- Time: O(n) - n function calls
- Space: O(n) - call stack depth
- Best for: Learning recursion, small strings

**Built-in reversed() Method:**
- Time: O(n) - iterator creation and join
- Space: O(n) - creates new string
- Best for: Readable code, standard library usage

### Performance Notes

- Slicing method is generally fastest in Python
- Recursive method may hit stack limits for long strings
- Optimized loop provides memory efficiency
- All methods produce identical results
- Performance differences become more noticeable with longer strings and more iterations
