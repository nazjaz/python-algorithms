# Merge Sort Visualizer API Documentation

## Overview

The Merge Sort Visualizer provides a complete implementation of the merge sort algorithm with detailed visualization of the divide and conquer process. It shows how the algorithm recursively divides arrays and merges sorted subarrays.

## Classes

### MergeSortVisualizer

Main class for merge sort with visualization capabilities.

#### Constructor

```python
MergeSortVisualizer(config_path: str = "config.yaml") -> None
```

Initialize visualizer with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### sort

```python
sort(array: List[Any], visualize: bool = True) -> List[Any]
```

Sort array using merge sort algorithm.

**Parameters:**
- `array` (List[Any]): Array to sort
- `visualize` (bool): If True, record visualization steps

**Returns:**
- `List[Any]`: Sorted array

**Example:**
```python
visualizer = MergeSortVisualizer()
result = visualizer.sort([64, 34, 25, 12, 22, 11, 90])
# Returns: [11, 12, 22, 25, 34, 64, 90]
```

##### get_visualization_steps

```python
get_visualization_steps() -> List[Dict[str, Any]]
```

Get list of visualization steps.

**Returns:**
- `List[Dict[str, Any]]`: List of visualization step dictionaries

**Example:**
```python
visualizer.sort([5, 2, 8], visualize=True)
steps = visualizer.get_visualization_steps()
# Returns list of step dictionaries
```

##### print_visualization

```python
print_visualization(detailed: bool = False) -> None
```

Print visualization of merge sort process.

**Parameters:**
- `detailed` (bool): If True, print detailed information for each step

**Example:**
```python
visualizer.sort([5, 2, 8], visualize=True)
visualizer.print_visualization(detailed=True)
```

##### generate_visualization_report

```python
generate_visualization_report(output_path: Optional[str] = None) -> str
```

Generate detailed visualization report.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If insufficient permissions to write file

**Example:**
```python
visualizer.sort([5, 2, 8], visualize=True)
report = visualizer.generate_visualization_report("report.txt")
```

## Algorithm Details

### Merge Sort Algorithm

Merge sort is a divide and conquer algorithm that works as follows:

1. **Divide**: Split the array into two halves
2. **Conquer**: Recursively sort both halves
3. **Combine**: Merge the sorted halves

### Time Complexity

- **Best Case**: O(n log n)
- **Average Case**: O(n log n)
- **Worst Case**: O(n log n)

### Space Complexity

- **O(n)**: Requires temporary arrays for merging

### Properties

- **Stable**: Maintains relative order of equal elements
- **Not in-place**: Requires O(n) extra space
- **Guaranteed performance**: Always O(n log n)
- **Well-suited for**: Linked lists, external sorting

## Visualization Features

The visualizer tracks:
- **Divide steps**: When array is split into subarrays
- **Merge steps**: When subarrays are merged back together
- **Recursion depth**: Level of recursion for each operation
- **Array states**: Complete array state at each step
- **Subarray information**: Left and right subarrays during merge

## Usage Examples

### Basic Sorting

```python
from src.main import MergeSortVisualizer

visualizer = MergeSortVisualizer()
result = visualizer.sort([64, 34, 25, 12, 22, 11, 90])
print(result)  # [11, 12, 22, 25, 34, 64, 90]
```

### With Visualization

```python
visualizer = MergeSortVisualizer()
visualizer.sort([5, 2, 8, 1, 9], visualize=True)
visualizer.print_visualization()
```

### Generate Report

```python
visualizer = MergeSortVisualizer()
visualizer.sort([5, 2, 8, 1, 9], visualize=True)
visualizer.generate_visualization_report("report.txt")
```
