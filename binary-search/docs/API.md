# API Documentation

## BinarySearch Class

The main class for searching elements in sorted arrays using binary search algorithm.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the BinarySearch with configuration.

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

#### `search_iterative(array: List[float], target: float) -> Optional[int]`

Search for target in sorted array using iterative binary search.

**Parameters:**
- `array` (List[float]): Sorted array to search.
- `target` (float): Value to search for.

**Returns:**
- `Optional[int]`: Index of target if found, None otherwise.

**Raises:**
- `ValueError`: If array is not sorted.

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

**Example:**
```python
searcher = BinarySearch()
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = searcher.search_iterative(array, 5)
print(result)  # 4
```

#### `search_recursive(array: List[float], target: float, left: int = 0, right: Optional[int] = None, depth: int = 0) -> Optional[int]`

Search for target in sorted array using recursive binary search.

**Parameters:**
- `array` (List[float]): Sorted array to search.
- `target` (float): Value to search for.
- `left` (int): Left boundary of search range. Default: 0.
- `right` (Optional[int]): Right boundary of search range. Default: len(array) - 1.
- `depth` (int): Current recursion depth (for tracking). Default: 0.

**Returns:**
- `Optional[int]`: Index of target if found, None otherwise.

**Raises:**
- `ValueError`: If array is not sorted.
- `RecursionError`: If recursion depth exceeds maximum.

**Time Complexity:** O(log n)
**Space Complexity:** O(log n) due to call stack

**Example:**
```python
searcher = BinarySearch()
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = searcher.search_recursive(array, 5)
print(result)  # 4
```

#### `compare_approaches(array: List[float], target: float, iterations: int = 1) -> Dict[str, any]`

Compare performance of iterative and recursive binary search.

**Parameters:**
- `array` (List[float]): Sorted array to search.
- `target` (float): Value to search for.
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `array_length`: Length of input array
  - `target`: Target value searched
  - `iterations`: Number of iterations performed
  - `iterative`: Dictionary with result, time, comparisons, and success status
  - `recursive`: Dictionary with result, time, comparisons, recursive_calls, and success status
  - `fastest`: Name of fastest method (if both succeeded)
  - `fastest_time`: Time of fastest method

**Example:**
```python
searcher = BinarySearch()
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
comparison = searcher.compare_approaches(array, 5, iterations=100)
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
- Results from both approaches
- Timing information for each approach
- Comparison counts
- Performance summary
- Algorithm complexity information

**Example:**
```python
comparison = searcher.compare_approaches(array, 5)
report = searcher.generate_report(comparison, output_path="report.txt")
print(report)
```

### Internal Methods

#### `_validate_sorted(array: List[float]) -> bool`

Validate that array is sorted in ascending order.

**Parameters:**
- `array` (List[float]): Array to validate.

**Returns:**
- `bool`: True if sorted, False otherwise.

**Example:**
```python
searcher = BinarySearch()
assert searcher._validate_sorted([1, 2, 3, 4, 5]) is True
assert searcher._validate_sorted([1, 3, 2, 4, 5]) is False
```

### Attributes

#### `max_recursive_depth: int`

Maximum recursion depth allowed, configured from config.yaml.

#### `comparisons: int`

Total number of comparisons made during last search.

#### `recursive_calls: int`

Total number of recursive calls made during last recursive search.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import BinarySearch

# Initialize with default config
searcher = BinarySearch()

# Or with custom config
searcher = BinarySearch(config_path="custom_config.yaml")

# Search using specific method
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = searcher.search_iterative(array, 5)
print(f"Iterative: {result}")

result = searcher.search_recursive(array, 5)
print(f"Recursive: {result}")

# Compare both approaches
comparison = searcher.compare_approaches(array, 5)
print(f"Fastest: {comparison['fastest']}")

# Generate report
report = searcher.generate_report(comparison, output_path="report.txt")
```

### Algorithm Complexity

**Time Complexity:**
- Best Case: O(1) - target at middle
- Average Case: O(log n)
- Worst Case: O(log n) - target at end or not found

**Space Complexity:**
- Iterative: O(1) - constant extra space
- Recursive: O(log n) - call stack depth

**Characteristics:**
- Requires sorted array
- Much faster than linear search for large arrays
- Divide and conquer approach
- Logarithmic time complexity

### Edge Cases Handled

- Empty array: Returns None
- Single element: Handles correctly
- Target not found: Returns None
- Target at first position: Returns 0
- Target at last position: Returns last index
- Target at middle: Returns middle index
- Unsorted array: Raises ValueError
- Large arrays: Handles efficiently
- Duplicate values: Returns first occurrence found

### Performance Notes

- Iterative approach is generally faster and more memory efficient
- Recursive approach may hit stack limits for very large arrays
- Both approaches produce identical results
- Performance differences become more noticeable with larger arrays and more iterations
- Binary search is much faster than linear search for large arrays

### Important Notes

- **Array must be sorted**: Binary search requires a sorted array. The implementation validates this and raises ValueError if array is not sorted.
- **Target not found**: Returns None when target is not found. Always check for None when using the result.
- **Recursion limits**: Recursive approach may fail for very large arrays due to stack limits. Use iterative approach for production code.
- **Duplicate values**: When duplicates exist, the algorithm may return any occurrence. For guaranteed first/last occurrence, use modified binary search.
