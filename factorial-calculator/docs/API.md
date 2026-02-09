# API Documentation

## FactorialCalculator Class

The main class for calculating factorials using iterative and recursive approaches.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the FactorialCalculator with configuration.

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

#### `factorial_iterative(n: int) -> int`

Calculate factorial using iterative approach.

**Parameters:**
- `n` (int): Non-negative integer to calculate factorial for.

**Returns:**
- `int`: Factorial of n.

**Raises:**
- `ValueError`: If n is negative.

**Time Complexity:** O(n)
**Space Complexity:** O(1)

**Example:**
```python
calculator = FactorialCalculator()
result = calculator.factorial_iterative(5)
print(result)  # 120
```

#### `factorial_recursive(n: int, depth: int = 0) -> int`

Calculate factorial using recursive approach.

**Parameters:**
- `n` (int): Non-negative integer to calculate factorial for.
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `int`: Factorial of n.

**Raises:**
- `ValueError`: If n is negative.
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(n)
**Space Complexity:** O(n) due to call stack

**Example:**
```python
calculator = FactorialCalculator()
result = calculator.factorial_recursive(5)
print(result)  # 120
```

#### `factorial_memoized(n: int, memo: Optional[Dict[int, int]] = None) -> int`

Calculate factorial using memoized recursive approach.

**Parameters:**
- `n` (int): Non-negative integer to calculate factorial for.
- `memo` (Optional[Dict[int, int]]): Dictionary for memoization. Default: None.

**Returns:**
- `int`: Factorial of n.

**Raises:**
- `ValueError`: If n is negative.

**Time Complexity:** O(n)
**Space Complexity:** O(n) for memoization table

**Example:**
```python
calculator = FactorialCalculator()
result = calculator.factorial_memoized(5)
print(result)  # 120
```

#### `compare_performance(n: int) -> Dict[str, any]`

Compare performance of different factorial approaches.

**Parameters:**
- `n` (int): Non-negative integer to calculate factorial for.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `input`: Input value n
  - `iterative`: Dictionary with result, time, and success status
  - `recursive`: Dictionary with result, time, and success status
  - `memoized`: Dictionary with result, time, and success status
  - `fastest`: Name of fastest approach (if all succeeded)
  - `fastest_time`: Time of fastest approach

**Example:**
```python
calculator = FactorialCalculator()
comparison = calculator.compare_performance(10)
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
comparison = calculator.compare_performance(10)
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
from src.main import FactorialCalculator

# Initialize with default config
calculator = FactorialCalculator()

# Or with custom config
calculator = FactorialCalculator(config_path="custom_config.yaml")

# Calculate using specific method
result = calculator.factorial_iterative(10)
print(f"Iterative: {result}")

result = calculator.factorial_recursive(10)
print(f"Recursive: {result}")

result = calculator.factorial_memoized(10)
print(f"Memoized: {result}")

# Compare all approaches
comparison = calculator.compare_performance(10)
print(f"Fastest: {comparison['fastest']}")

# Generate report
report = calculator.generate_report(comparison, output_path="report.txt")
```

### Algorithm Complexity Comparison

**Iterative Approach:**
- Time: O(n) - single loop
- Space: O(1) - constant extra space
- Best for: Large numbers, production code

**Recursive Approach:**
- Time: O(n) - n function calls
- Space: O(n) - call stack depth
- Best for: Learning, small numbers, elegant code

**Memoized Recursive Approach:**
- Time: O(n) - n function calls with caching
- Space: O(n) - memoization table
- Best for: Repeated calculations, medium numbers

### Performance Notes

- Iterative approach is generally fastest for large numbers
- Recursive approach may hit stack limits for large numbers
- Memoized approach provides benefits when same values computed multiple times
- All approaches produce identical results
- Performance differences become more noticeable with larger inputs
