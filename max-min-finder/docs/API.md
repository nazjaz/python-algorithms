# API Documentation

## MaxMinFinder Class

The main class for finding maximum and minimum values using a single-pass algorithm.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the MaxMinFinder with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.
- `ValueError`: If configuration file is empty.

**Side Effects:**
- Loads configuration
- Sets up logging
- Initializes statistics counters

#### `find_max_min(array: List[float]) -> Tuple[float, float]`

Find maximum and minimum values using single pass algorithm.

**Parameters:**
- `array` (List[float]): List of numbers to analyze.

**Returns:**
- `Tuple[float, float]`: Tuple of (minimum, maximum) values.

**Raises:**
- `ValueError`: If array is empty.

**Side Effects:**
- Resets comparison counter
- Records analysis data
- Logs algorithm execution details

**Algorithm:**
1. Initialize min and max with first element
2. Process remaining elements in pairs when possible
3. Compare pair elements first, then compare smaller with min and larger with max
4. Handle last element separately if array length is odd

**Optimization:**
- Processes elements in pairs to reduce comparisons
- Reduces comparisons from 2(n-1) to approximately 3n/2
- Significant improvement for large arrays

**Example:**
```python
finder = MaxMinFinder()
min_val, max_val = finder.find_max_min([64, 34, 25, 12, 22, 11, 90])
print(f"Min: {min_val}, Max: {max_val}")  # Min: 11, Max: 90
```

#### `get_analysis() -> Dict[str, any]`

Get detailed analysis of the algorithm execution.

**Returns:**
- `Dict[str, any]`: Dictionary containing analysis data with keys:
  - `array_length`: Length of input array
  - `min_value`: Minimum value found
  - `max_value`: Maximum value found
  - `min_index`: Index of minimum value
  - `max_index`: Index of maximum value
  - `total_comparisons`: Total number of comparisons made
  - `comparisons_per_element`: Average comparisons per element
  - `efficiency_ratio`: Efficiency compared to naive approach
  - `min_updates`: Number of times minimum was updated
  - `max_updates`: Number of times maximum was updated
  - `elements_processed`: Number of elements processed

**Example:**
```python
finder.find_max_min([3, 1, 2, 4])
analysis = finder.get_analysis()
print(f"Comparisons: {analysis['total_comparisons']}")
print(f"Efficiency: {analysis['efficiency_ratio']:.2%}")
```

#### `generate_report(output_path: Optional[str] = None) -> str`

Generate detailed analysis report.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save report file. If None, report is only returned.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Results (min, max, range)
- Performance metrics (comparisons, efficiency)
- Algorithm statistics (updates, elements processed)
- Complexity analysis

**Example:**
```python
finder.find_max_min([3, 1, 2])
report = finder.generate_report(output_path="report.txt")
print(report)
```

### Attributes

#### `comparisons: int`

Total number of comparisons made during algorithm execution. Incremented for each comparison operation.

#### `analysis_data: Dict[str, any]`

Dictionary containing detailed analysis data about algorithm execution, including values, indices, update counts, and performance metrics.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import MaxMinFinder

# Initialize with default config
finder = MaxMinFinder()

# Or with custom config
finder = MaxMinFinder(config_path="custom_config.yaml")

# Find max and min
numbers = [64, 34, 25, 12, 22, 11, 90]
min_val, max_val = finder.find_max_min(numbers)

# Access statistics
print(f"Comparisons: {finder.comparisons}")
print(f"Min: {min_val}, Max: {max_val}")

# Get detailed analysis
analysis = finder.get_analysis()
print(f"Efficiency: {analysis['efficiency_ratio']:.2%}")

# Generate report
report = finder.generate_report(output_path="analysis_report.txt")
```

### Algorithm Complexity

**Time Complexity:**
- Best case: O(n) - single pass through array
- Average case: O(n) - single pass through array
- Worst case: O(n) - single pass through array

**Space Complexity:** O(1) - only uses constant extra space

**Comparison Count:**
- Naive approach: 2(n-1) comparisons
- Optimized approach: ~3n/2 comparisons (when n is even)
- Improvement: ~25% reduction in comparisons

**Characteristics:**
- Single pass: Processes array only once
- In-place: Uses constant extra space
- Optimized: Processes elements in pairs when possible
- Efficient: Reduces comparisons compared to naive approach

### Performance Notes

- Algorithm is optimal for finding both max and min simultaneously
- Pair-wise processing provides significant efficiency gains
- Comparison count is approximately 3n/2 for even-length arrays
- Works with integers, floats, and mixed numeric types
- Handles edge cases like single element, duplicates, and negative numbers
