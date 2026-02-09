# API Documentation

## BubbleSort Class

The main class for implementing bubble sort algorithm with visualization and statistics.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the BubbleSort with configuration.

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

#### `sort(array: List[int]) -> List[int]`

Sort array using bubble sort algorithm.

**Parameters:**
- `array` (List[int]): List of integers to sort.

**Returns:**
- `List[int]`: Sorted list of integers.

**Side Effects:**
- Resets comparison and swap counters
- Records steps for visualization (if enabled)
- Logs algorithm execution details

**Algorithm:**
1. Iterate through array from start to end
2. For each iteration, compare adjacent elements
3. Swap if elements are in wrong order
4. Continue until no swaps occur in a complete pass

**Example:**
```python
sorter = BubbleSort()
result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
print(result)  # [11, 12, 22, 25, 34, 64, 90]
```

#### `visualize(output_path: str = None) -> None`

Generate visualization of sorting process.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save visualization image. If None, uses default from config.

**Side Effects:**
- Creates visualization image file
- Logs visualization generation

**Visualization Features:**
- Shows array state at each step
- Highlights elements being compared (red)
- Highlights swapped elements (green)
- Displays step numbers

**Example:**
```python
sorter.sort([3, 1, 2])
sorter.visualize(output_path="sorting_steps.png")
```

#### `generate_report(output_path: str = None) -> str`

Generate sorting report with statistics.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save report file. If None, report is only returned.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Total comparisons count
- Total swaps count
- Number of steps recorded
- Average comparisons per element
- Swap ratio percentage

**Example:**
```python
sorter.sort([3, 1, 2])
report = sorter.generate_report(output_path="report.txt")
print(report)
```

### Attributes

#### `comparisons: int`

Total number of comparisons made during sorting. Incremented for each comparison between array elements.

#### `swaps: int`

Total number of swaps performed during sorting. Incremented when two elements are swapped.

#### `steps: List[Dict[str, Any]]`

List of recorded steps for visualization. Each step contains:
- `array`: Current state of the array
- `outer_index`: Current outer loop index
- `inner_index`: Current inner loop index
- `swapped`: Whether a swap occurred

#### `visualization_enabled: bool`

Whether visualization is enabled based on configuration.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import BubbleSort

# Initialize with default config
sorter = BubbleSort()

# Or with custom config
sorter = BubbleSort(config_path="custom_config.yaml")

# Sort an array
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = sorter.sort(numbers)

# Access statistics
print(f"Comparisons: {sorter.comparisons}")
print(f"Swaps: {sorter.swaps}")

# Generate visualization
sorter.visualize(output_path="bubble_sort.png")

# Generate report
report = sorter.generate_report(output_path="report.txt")
```

### Algorithm Complexity

**Time Complexity:**
- Best case: O(n) - when array is already sorted
- Average case: O(n²)
- Worst case: O(n²) - when array is reverse sorted

**Space Complexity:** O(1) - only uses constant extra space

**Characteristics:**
- Stable: Maintains relative order of equal elements
- In-place: Sorts array without requiring additional memory
- Adaptive: Can detect if array is already sorted and stop early

### Performance Notes

- Bubble sort is not efficient for large arrays
- Best suited for educational purposes and small datasets
- Early termination optimization stops when no swaps occur
- Comparison and swap counts provide insight into algorithm behavior
