# Kth Largest Element Finder API Documentation

## Overview

The Kth Largest Element Finder provides implementations for finding the kth largest element in an array using two different approaches: heap data structure and quickselect algorithm. It includes performance comparison to analyze the efficiency of each method.

## Classes

### KthLargestFinder

Main class for finding kth largest element using heap and quickselect.

#### Constructor

```python
KthLargestFinder(config_path: str = "config.yaml") -> None
```

Initialize finder with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### find_kth_largest_heap

```python
find_kth_largest_heap(arr: List[Any], k: int) -> Any
```

Find kth largest element using heap data structure.

**Parameters:**
- `arr` (List[Any]): Array of elements
- `k` (int): Position of largest element to find (1-indexed)

**Returns:**
- `Any`: Kth largest element

**Time Complexity:** O(n log k)
**Space Complexity:** O(k)

##### find_kth_largest_quickselect

```python
find_kth_largest_quickselect(
    arr: List[Any], k: int, track_stats: bool = False
) -> Any
```

Find kth largest element using quickselect algorithm.

**Parameters:**
- `arr` (List[Any]): Array of elements
- `k` (int): Position of largest element to find (1-indexed)
- `track_stats` (bool): If True, track comparison and swap counts

**Returns:**
- `Any`: Kth largest element

**Time Complexity:** O(n) average, O(n²) worst case
**Space Complexity:** O(log n) for recursion

##### find_kth_largest_all

```python
find_kth_largest_all(arr: List[Any], k: int) -> List[Any]
```

Find all k largest elements (not just kth).

**Parameters:**
- `arr` (List[Any]): Array of elements
- `k` (int): Number of largest elements to find

**Returns:**
- `List[Any]`: List of k largest elements in descending order

##### compare_methods

```python
compare_methods(arr: List[Any], k: int) -> Dict[str, Dict[str, Any]]
```

Compare heap and quickselect methods.

**Parameters:**
- `arr` (List[Any]): Array of elements
- `k` (int): Position of largest element to find

**Returns:**
- `Dict[str, Dict[str, Any]]`: Dictionary with performance comparison

##### get_stats

```python
get_stats() -> Dict[str, int]
```

Get algorithm statistics.

**Returns:**
- `Dict[str, int]`: Dictionary with comparison and swap counts

## Algorithm Details

### Heap Method

Uses a min-heap of size k to maintain the k largest elements:
- Process each element
- If heap size < k: add element
- If element > heap minimum: replace minimum
- Root of heap is kth largest

### Quickselect Method

Variant of quicksort that only recurses on one side:
- Partition array around pivot
- If pivot is kth largest: return it
- Otherwise: recurse on appropriate side

## Usage Examples

### Heap Method

```python
from src.main import KthLargestFinder

finder = KthLargestFinder()
result = finder.find_kth_largest_heap([3, 1, 4, 1, 5, 9, 2, 6], 3)
print(result)  # 5
```

### Quickselect Method

```python
finder = KthLargestFinder()
result = finder.find_kth_largest_quickselect([3, 1, 4, 1, 5, 9, 2, 6], 3)
print(result)  # 5
```

### Compare Methods

```python
finder = KthLargestFinder()
results = finder.compare_methods([3, 1, 4, 1, 5, 9, 2, 6], 3)
print(results["heap"]["execution_time"])
print(results["quickselect"]["execution_time"])
```
