# API Documentation

## InsertionSort Class

The main class for sorting arrays using the insertion sort algorithm with visualization and comparison capabilities.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the InsertionSort with configuration.

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

#### `sort(array: List[float], enable_visualization: bool = False) -> List[float]`

Sort array using insertion sort algorithm.

**Parameters:**
- `array` (List[float]): Array to sort (will be copied, original not modified).
- `enable_visualization` (bool): Whether to collect data for visualization. Default: False.

**Returns:**
- `List[float]`: Sorted array.

**Time Complexity:** O(n²) average/worst, O(n) best
**Space Complexity:** O(1)

**Algorithm:**
1. Start with second element (index 1)
2. Compare with previous elements
3. Shift larger elements one position to the right
4. Insert current element at correct position
5. Repeat for all elements

**Example:**
```python
sorter = InsertionSort()
result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
print(result)  # [11, 12, 22, 25, 34, 64, 90]
```

#### `bubble_sort(array: List[float]) -> Tuple[List[float], Dict[str, int]]`

Sort array using bubble sort for comparison.

**Parameters:**
- `array` (List[float]): Array to sort.

**Returns:**
- `Tuple[List[float], Dict[str, int]]`: Tuple of (sorted_array, statistics_dict).

**Example:**
```python
sorter = InsertionSort()
result, stats = sorter.bubble_sort([64, 34, 25, 12, 22, 11, 90])
print(f"Sorted: {result}")
print(f"Comparisons: {stats['comparisons']}, Swaps: {stats['swaps']}")
```

#### `selection_sort(array: List[float]) -> Tuple[List[float], Dict[str, int]]`

Sort array using selection sort for comparison.

**Parameters:**
- `array` (List[float]): Array to sort.

**Returns:**
- `Tuple[List[float], Dict[str, int]]`: Tuple of (sorted_array, statistics_dict).

**Example:**
```python
sorter = InsertionSort()
result, stats = sorter.selection_sort([64, 34, 25, 12, 22, 11, 90])
print(f"Sorted: {result}")
print(f"Comparisons: {stats['comparisons']}, Swaps: {stats['swaps']}")
```

#### `compare_algorithms(array: List[float], iterations: int = 1) -> Dict[str, any]`

Compare performance of insertion sort with other sorting algorithms.

**Parameters:**
- `array` (List[float]): Array to sort.
- `iterations` (int): Number of iterations for timing. Default: 1.

**Returns:**
- `Dict[str, any]`: Dictionary containing performance comparison data with keys:
  - `array_length`: Length of input array
  - `iterations`: Number of iterations performed
  - `insertion_sort`: Dictionary with result, time, comparisons, swaps, and success status
  - `bubble_sort`: Dictionary with result, time, comparisons, swaps, and success status
  - `selection_sort`: Dictionary with result, time, comparisons, swaps, and success status
  - `fastest`: Name of fastest algorithm (if all succeeded)
  - `fastest_time`: Time of fastest algorithm

**Example:**
```python
sorter = InsertionSort()
comparison = sorter.compare_algorithms([64, 34, 25, 12, 22, 11, 90], iterations=100)
print(f"Fastest: {comparison['fastest']}")
print(f"Time: {comparison['fastest_time']*1000:.4f} ms")
```

#### `visualize_sorting(array: List[float], output_path: Optional[str] = None) -> None`

Create visualization of insertion sort process.

**Parameters:**
- `array` (List[float]): Array to sort and visualize.
- `output_path` (Optional[str]): Optional path to save visualization (GIF file).

**Raises:**
- `ImportError`: If matplotlib is not available.

**Example:**
```python
sorter = InsertionSort()
sorter.visualize_sorting([64, 34, 25, 12, 22, 11, 90])
# Or save to file:
sorter.visualize_sorting([64, 34, 25, 12, 22, 11, 90], output_path="sort.gif")
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
sorter = InsertionSort()
sorter.sort([64, 34, 25, 12, 22, 11, 90])
stats = sorter.get_statistics()
print(f"Comparisons: {stats['comparisons']}")
print(f"Swaps: {stats['swaps']}")
```

#### `generate_report(original: List[float], sorted_array: List[float], comparison_data: Optional[Dict[str, any]] = None, output_path: Optional[str] = None) -> str`

Generate detailed sorting report.

**Parameters:**
- `original` (List[float]): Original unsorted array.
- `sorted_array` (List[float]): Sorted array.
- `comparison_data` (Optional[Dict[str, any]]): Optional comparison data from compare_algorithms().
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Original and sorted arrays
- Statistics (comparisons, swaps, iterations)
- Algorithm comparison (if provided)
- Algorithm complexity information

**Example:**
```python
sorter = InsertionSort()
original = [64, 34, 25, 12, 22, 11, 90]
sorted_arr = sorter.sort(original)
comparison = sorter.compare_algorithms(original)
report = sorter.generate_report(original, sorted_arr, comparison, output_path="report.txt")
print(report)
```

### Attributes

#### `comparisons: int`

Total number of comparisons made during last sort.

#### `swaps: int`

Total number of swaps performed during last sort.

#### `iterations: List[Dict]`

List of dictionaries containing detailed information for each iteration.

#### `visualization_data: List[List[float]]`

List of array states collected during sorting for visualization.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import InsertionSort

# Initialize with default config
sorter = InsertionSort()

# Or with custom config
sorter = InsertionSort(config_path="custom_config.yaml")

# Sort array
original = [64, 34, 25, 12, 22, 11, 90]
sorted_array = sorter.sort(original)
print(f"Sorted: {sorted_array}")

# Get statistics
stats = sorter.get_statistics()
print(f"Comparisons: {stats['comparisons']}")
print(f"Swaps: {stats['swaps']}")

# Compare with other algorithms
comparison = sorter.compare_algorithms(original)
print(f"Fastest: {comparison['fastest']}")

# Create visualization
sorter.visualize_sorting(original, output_path="sort.gif")

# Generate report
report = sorter.generate_report(original, sorted_array, comparison, output_path="report.txt")
```

### Algorithm Complexity

**Time Complexity:**
- Best Case: O(n) - already sorted
- Average Case: O(n²)
- Worst Case: O(n²) - reverse sorted

**Space Complexity:**
- O(1) - in-place sorting

**Characteristics:**
- Stable sorting algorithm (preserves relative order)
- Adaptive (efficient for nearly sorted arrays)
- In-place sorting
- Simple to understand and implement
- Efficient for small arrays

### Comparison with Other Algorithms

**vs Bubble Sort:**
- Insertion sort is generally faster
- Both are O(n²) but insertion sort has better constants
- Insertion sort is adaptive (better for nearly sorted data)
- Insertion sort is stable

**vs Selection Sort:**
- Insertion sort is generally faster
- Both are O(n²) but insertion sort has better constants
- Insertion sort is stable, selection sort is not
- Insertion sort is adaptive

### Visualization

The visualization feature creates an animated GIF showing the sorting process:
- Blue bars represent unsorted elements
- Green bars represent elements being moved
- Light green bars represent sorted portion
- Animation shows step-by-step progression

### Performance Notes

- Insertion sort is adaptive: performs well on nearly sorted arrays
- Best case O(n) makes it efficient for already sorted or nearly sorted data
- Generally faster than bubble sort and selection sort in practice
- All comparisons and swaps are logged for educational purposes
- Visualization helps understand the algorithm's step-by-step process

### Edge Cases

- Empty arrays return empty array
- Single element arrays are already sorted
- Already sorted arrays perform in O(n) time
- Reverse sorted arrays require maximum comparisons and swaps
- Arrays with duplicates are handled correctly (stable sorting)
