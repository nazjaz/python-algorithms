# API Documentation

## ArraySumCalculator Class

The main class for calculating sum of array elements using iterative and recursive approaches.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the ArraySumCalculator with configuration.

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

#### `sum_iterative(array: List[float]) -> float`

Calculate sum using iterative approach.

**Parameters:**
- `array` (List[float]): List of numbers to sum.

**Returns:**
- `float`: Sum of all elements in array.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

**Example:**
```python
calculator = ArraySumCalculator()
result = calculator.sum_iterative([1, 2, 3, 4, 5])
print(result)  # 15.0
```

#### `sum_recursive(array: List[float], depth: int = 0) -> float`

Calculate sum using recursive approach.

**Parameters:**
- `array` (List[float]): List of numbers to sum.
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `float`: Sum of all elements in array.

**Raises:**
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(n)
**Space Complexity:** O(n) due to call stack

**Example:**
```python
calculator = ArraySumCalculator()
result = calculator.sum_recursive([1, 2, 3, 4, 5])
print(result)  # 15.0
```

#### `sum_recursive_indexed(array: List[float], index: int = 0, depth: int = 0) -> float`

Calculate sum using recursive approach with index parameter.

**Parameters:**
- `array` (List[float]): List of numbers to sum.
- `index` (int): Current index in array. Default: 0.
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `float`: Sum of all elements from index to end.

**Raises:**
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(n)
**Space Complexity:** O(n) due to call stack

**Example:**
```python
calculator = ArraySumCalculator()
result = calculator.sum_recursive_indexed([1, 2, 3, 4, 5])
print(result)  # 15.0
```

#### `compare_performance(array: List[float], iterations: int = 1) -> Dict[str, any]`

Compare performance of different sum calculation approaches.

**Parameters:**
- `array` (List[float]): List of numbers to sum.
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `array_length`: Length of input array
  - `iterations`: Number of iterations performed
  - `iterative`: Dictionary with result, time, and success status
  - `recursive`: Dictionary with result, time, and success status
  - `recursive_indexed`: Dictionary with result, time, and success status
  - `fastest`: Name of fastest method (if all succeeded)
  - `fastest_time`: Time of fastest method

**Example:**
```python
calculator = ArraySumCalculator()
comparison = calculator.compare_performance([1, 2, 3, 4, 5], iterations=100)
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
- Results from all three approaches
- Timing information for each approach
- Performance summary
- Algorithm complexity information

**Example:**
```python
comparison = calculator.compare_performance([1, 2, 3, 4, 5])
report = calculator.generate_report(comparison, output_path="report.txt")
print(report)
```

### Attributes

#### `max_recursive_depth: int`

Maximum recursion depth allowed, configured from config.yaml.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import ArraySumCalculator

# Initialize with default config
calculator = ArraySumCalculator()

# Or with custom config
calculator = ArraySumCalculator(config_path="custom_config.yaml")

# Calculate using specific method
result = calculator.sum_iterative([1, 2, 3, 4, 5])
print(f"Iterative: {result}")

result = calculator.sum_recursive([1, 2, 3, 4, 5])
print(f"Recursive: {result}")

result = calculator.sum_recursive_indexed([1, 2, 3, 4, 5])
print(f"Recursive Indexed: {result}")

# Compare all approaches
comparison = calculator.compare_performance([1, 2, 3, 4, 5])
print(f"Fastest: {comparison['fastest']}")

# Generate report
report = calculator.generate_report(comparison, output_path="report.txt")
```

### Algorithm Complexity Comparison

**Iterative Approach:**
- Time: O(n) - single loop
- Space: O(1) - constant extra space
- Best for: Large arrays, production code

**Recursive Approach:**
- Time: O(n) - n function calls
- Space: O(n) - call stack depth
- Best for: Learning, small arrays, elegant code

**Recursive Indexed Approach:**
- Time: O(n) - n function calls
- Space: O(n) - call stack depth
- Best for: Learning, more memory efficient than slicing variant

### Performance Notes

- Iterative approach is generally fastest for large arrays
- Recursive approaches may hit stack limits for large arrays
- All approaches produce identical results
- Performance differences become more noticeable with larger arrays and more iterations
- Recursive indexed is more memory efficient than recursive with slicing
