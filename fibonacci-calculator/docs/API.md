# API Documentation

## FibonacciCalculator Class

The main class for calculating Fibonacci numbers using multiple approaches.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the FibonacciCalculator with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.
- `ValueError`: If configuration file is empty.

**Side Effects:**
- Loads configuration
- Sets up logging
- Initializes recursion depth limit and memoization cache

#### `fibonacci_naive(n: int, depth: int = 0) -> int`

Calculate nth Fibonacci number using naive recursion.

**Parameters:**
- `n` (int): Position in Fibonacci sequence (0-indexed).
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `int`: nth Fibonacci number.

**Raises:**
- `ValueError`: If n is negative.
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(2^n) - exponential
**Space Complexity:** O(n) - call stack

**Example:**
```python
calculator = FibonacciCalculator()
result = calculator.fibonacci_naive(10)
print(result)  # 55
print(f"Recursive calls: {calculator.recursive_calls}")
```

#### `fibonacci_memoized(n: int, depth: int = 0) -> int`

Calculate nth Fibonacci number using memoization (dynamic programming).

**Parameters:**
- `n` (int): Position in Fibonacci sequence (0-indexed).
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `int`: nth Fibonacci number.

**Raises:**
- `ValueError`: If n is negative.
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(n) - linear
**Space Complexity:** O(n) - memoization cache + call stack

**Example:**
```python
calculator = FibonacciCalculator()
calculator.memo = {}  # Clear cache
result = calculator.fibonacci_memoized(10)
print(result)  # 55
print(f"Recursive calls: {calculator.recursive_calls}")
print(f"Memo entries: {len(calculator.memo)}")
```

#### `fibonacci_iterative(n: int) -> int`

Calculate nth Fibonacci number using iterative approach.

**Parameters:**
- `n` (int): Position in Fibonacci sequence (0-indexed).

**Returns:**
- `int`: nth Fibonacci number.

**Raises:**
- `ValueError`: If n is negative.

**Time Complexity:** O(n) - linear
**Space Complexity:** O(1) - constant

**Example:**
```python
calculator = FibonacciCalculator()
result = calculator.fibonacci_iterative(10)
print(result)  # 55
```

#### `compare_approaches(n: int, iterations: int = 1) -> Dict[str, any]`

Compare performance of different Fibonacci calculation approaches.

**Parameters:**
- `n` (int): Position in Fibonacci sequence.
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `n`: Input value
  - `iterations`: Number of iterations performed
  - `naive_recursion`: Dictionary with result, time, recursive_calls, and success status
  - `memoized`: Dictionary with result, time, recursive_calls, memo_size, and success status
  - `iterative`: Dictionary with result, time, and success status
  - `fastest`: Name of fastest method (if all succeeded)
  - `fastest_time`: Time of fastest method

**Example:**
```python
calculator = FibonacciCalculator()
comparison = calculator.compare_approaches(20, iterations=100)
print(f"Fastest: {comparison['fastest']}")
print(f"Time: {comparison['fastest_time']*1000:.4f} ms")
```

#### `generate_report(comparison_data: Dict[str, any], output_path: Optional[str] = None) -> str`

Generate performance comparison report.

**Parameters:**
- `comparison_data` (Dict[str, any]): Performance comparison data from compare_approaches().
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Results from all three approaches
- Timing information for each approach
- Recursive call counts
- Memoization statistics
- Performance summary
- Speedup analysis
- Algorithm complexity information

**Example:**
```python
comparison = calculator.compare_approaches(20)
report = calculator.generate_report(comparison, output_path="report.txt")
print(report)
```

### Attributes

#### `max_recursive_depth: int`

Maximum recursion depth allowed, configured from config.yaml.

#### `memo: Dict[int, int]`

Memoization cache storing previously calculated Fibonacci values.

#### `recursive_calls: int`

Total number of recursive calls made during last calculation.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import FibonacciCalculator

# Initialize with default config
calculator = FibonacciCalculator()

# Or with custom config
calculator = FibonacciCalculator(config_path="custom_config.yaml")

# Calculate using specific method
result = calculator.fibonacci_naive(10)
print(f"Naive: {result}")

calculator.memo = {}
calculator.recursive_calls = 0
result = calculator.fibonacci_memoized(10)
print(f"Memoized: {result}")

result = calculator.fibonacci_iterative(10)
print(f"Iterative: {result}")

# Compare all approaches
comparison = calculator.compare_approaches(20)
print(f"Fastest: {comparison['fastest']}")

# Generate report
report = calculator.generate_report(comparison, output_path="report.txt")
```

### Algorithm Complexity Comparison

**Naive Recursion:**
- Time: O(2^n) - exponential, recalculates same values
- Space: O(n) - call stack depth
- Best for: Educational purposes, very small n (n < 20)

**Memoized (Dynamic Programming):**
- Time: O(n) - linear, avoids redundant calculations
- Space: O(n) - memoization cache + call stack
- Best for: Learning dynamic programming, medium n

**Iterative:**
- Time: O(n) - linear
- Space: O(1) - constant extra space
- Best for: Large n, production code

### Performance Notes

- Memoization provides dramatic speedup (1000x+) compared to naive recursion
- For n=30, naive recursion makes millions of recursive calls
- Memoized approach makes only n recursive calls
- Iterative approach is most space-efficient
- All approaches produce identical results
- Performance differences become dramatic for larger values of n

### Memoization Benefits

- **Eliminates redundant calculations**: Each Fibonacci value is calculated only once
- **Dramatic speedup**: Reduces time complexity from O(2^n) to O(n)
- **Cache reuse**: Subsequent calls with same n are instant
- **Trade-off**: Uses O(n) extra space for cache

### Edge Cases

- n=0: Returns 0 (base case)
- n=1: Returns 1 (base case)
- Negative n: Raises ValueError
- Large n: Naive recursion may be very slow or hit recursion limits
- Memoization cache persists between calls (clear with `calculator.memo = {}`)

### Important Notes

- **Clear memoization cache**: Set `calculator.memo = {}` before each calculation if you want fresh cache
- **Recursive call counting**: Reset `calculator.recursive_calls = 0` before each calculation
- **Large values**: Use iterative approach for very large n (n > 1000)
- **Performance**: Memoization provides exponential speedup over naive recursion
- **Space trade-off**: Memoization uses O(n) space but provides O(n) time vs O(2^n) time
