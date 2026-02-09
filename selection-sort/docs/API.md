# API Documentation

## SelectionSort Class

The main class for sorting arrays using the selection sort algorithm with detailed logging.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the SelectionSort with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.
- `ValueError`: If configuration file is empty.

**Side Effects:**
- Loads configuration
- Sets up logging
- Initializes statistics tracking

#### `sort(array: List[float]) -> List[float]`

Sort array using selection sort algorithm.

**Parameters:**
- `array` (List[float]): Array to sort (will be copied, original not modified).

**Returns:**
- `List[float]`: Sorted array.

**Time Complexity:** O(n²)
**Space Complexity:** O(1)

**Algorithm:**
1. For each position i from 0 to n-2:
   - Find minimum element in unsorted portion (from i to end)
   - Swap minimum with element at position i
2. Array is now sorted

**Example:**
```python
sorter = SelectionSort()
result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
print(result)  # [11, 12, 22, 25, 34, 64, 90]
```

#### `get_statistics() -> Dict[str, any]`

Get sorting statistics.

**Returns:**
- `Dict[str, any]`: Dictionary containing:
  - `comparisons`: Total number of comparisons made
  - `swaps`: Total number of swaps performed
  - `iterations`: Number of iterations (n-1 for array of length n)
  - `iteration_details`: List of detailed information for each iteration

**Example:**
```python
sorter = SelectionSort()
sorter.sort([64, 34, 25, 12, 22, 11, 90])
stats = sorter.get_statistics()
print(f"Comparisons: {stats['comparisons']}")
print(f"Swaps: {stats['swaps']}")
```

#### `generate_report(original: List[float], sorted_array: List[float], output_path: Optional[str] = None) -> str`

Generate detailed sorting report.

**Parameters:**
- `original` (List[float]): Original unsorted array.
- `sorted_array` (List[float]): Sorted array.
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Original and sorted arrays
- Statistics (comparisons, swaps, iterations)
- Detailed iteration-by-iteration breakdown
- Algorithm complexity information

**Example:**
```python
sorter = SelectionSort()
original = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = sorter.sort(original)
report = sorter.generate_report(original, sorted_arr, output_path="report.txt")
print(report)
```

### Internal Methods

#### `_find_minimum(array: List[float], start_index: int) -> Tuple[int, int]`

Find minimum element in array starting from given index.

**Parameters:**
- `array` (List[float]): Array to search.
- `start_index` (int): Starting index for search.

**Returns:**
- `Tuple[int, int]`: Tuple of (minimum_index, comparisons_made).

**Time Complexity:** O(n)
**Space Complexity:** O(1)

**Example:**
```python
sorter = SelectionSort()
array = [64, 34, 25, 12, 22, 11, 90]
min_index, comparisons = sorter._find_minimum(array, 0)
print(f"Minimum at index {min_index}")  # 5 (value 11)
```

### Attributes

#### `comparisons: int`

Total number of comparisons made during sorting.

#### `swaps: int`

Total number of swaps performed during sorting.

#### `iterations: List[Dict]`

List of dictionaries containing detailed information for each iteration.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import SelectionSort

# Initialize with default config
sorter = SelectionSort()

# Or with custom config
sorter = SelectionSort(config_path="custom_config.yaml")

# Sort array
original = [64, 34, 25, 12, 22, 11, 90]
sorted_array = sorter.sort(original)
print(f"Sorted: {sorted_array}")

# Get statistics
stats = sorter.get_statistics()
print(f"Comparisons: {stats['comparisons']}")
print(f"Swaps: {stats['swaps']}")

# Generate report
report = sorter.generate_report(original, sorted_array, output_path="report.txt")
```

### Algorithm Complexity

**Time Complexity:**
- Best Case: O(n²) - still requires full scan
- Average Case: O(n²)
- Worst Case: O(n²)

**Space Complexity:**
- O(1) - in-place sorting

**Characteristics:**
- In-place sorting (modifies copy, not original)
- Not stable (may change relative order of equal elements)
- Always performs O(n²) comparisons
- Performs at most n-1 swaps
- Simple to understand and implement

### Logging Details

The implementation provides detailed logging for:
- Each iteration of the outer loop
- Minimum element finding process
- Each comparison during minimum search
- Swap operations (when and what is swapped)
- Array state after each iteration
- Final statistics

### Performance Notes

- Selection sort always performs O(n²) comparisons regardless of input
- Number of swaps is at most n-1
- Best for small arrays or when memory writes are expensive
- Not recommended for large arrays due to O(n²) time complexity
- All comparisons and swaps are logged for educational purposes

### Edge Cases

- Empty arrays return empty array
- Single element arrays are already sorted
- Already sorted arrays still perform full algorithm
- Reverse sorted arrays require maximum swaps
- Arrays with duplicates are handled correctly
