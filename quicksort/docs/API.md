# Quick Sort API Documentation

## Overview

The Quick Sort implementation provides a complete quicksort algorithm with multiple pivot selection strategies. It includes performance comparison functionality to analyze the impact of different pivot selection methods on sorting performance.

## Classes

### QuickSort

Main class for quicksort with multiple pivot selection strategies.

#### Constructor

```python
QuickSort(config_path: str = "config.yaml") -> None
```

Initialize sorter with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### sort

```python
sort(
    arr: List[Any],
    pivot_strategy: str = "median_of_three",
    track_stats: bool = False,
) -> List[Any]
```

Sort array using quicksort with specified pivot strategy.

**Parameters:**
- `arr` (List[Any]): Array to sort
- `pivot_strategy` (str): Pivot selection strategy:
  - 'first': First element
  - 'last': Last element
  - 'middle': Middle element
  - 'random': Random element
  - 'median_of_three': Median of first, middle, last
- `track_stats` (bool): If True, track comparison and swap counts

**Returns:**
- `List[Any]`: Sorted array

**Raises:**
- `ValueError`: If pivot strategy is invalid

**Time Complexity:** O(n log n) average, O(n²) worst case

##### compare_strategies

```python
compare_strategies(
    arr: List[Any],
    strategies: Optional[List[str]] = None,
) -> Dict[str, Dict[str, Any]]
```

Compare performance of different pivot strategies.

**Parameters:**
- `arr` (List[Any]): Array to sort
- `strategies` (Optional[List[str]]): List of strategies to compare

**Returns:**
- `Dict[str, Dict[str, Any]]`: Dictionary with performance comparison

##### get_stats

```python
get_stats() -> Dict[str, int]
```

Get sorting statistics.

**Returns:**
- `Dict[str, int]`: Dictionary with comparison and swap counts

##### generate_report

```python
generate_report(
    comparison_results: Dict[str, Dict[str, Any]],
    output_path: Optional[str] = None,
) -> str
```

Generate performance comparison report.

**Parameters:**
- `comparison_results` (Dict[str, Dict[str, Any]]): Results from compare_strategies
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

## Pivot Selection Strategies

### First Element
- Selects first element as pivot
- Simple but can lead to O(n²) worst case for sorted arrays

### Last Element
- Selects last element as pivot
- Similar to first, O(n²) worst case for reverse sorted arrays

### Middle Element
- Selects middle element as pivot
- Better than first/last for some cases

### Random Element
- Selects random element as pivot
- Expected O(n log n) performance
- Avoids worst case with high probability

### Median of Three
- Selects median of first, middle, and last elements
- Good balance between simplicity and performance
- Reduces chance of worst case
- Often best choice for general-purpose sorting

## Usage Examples

### Basic Sorting

```python
from src.main import QuickSort

sorter = QuickSort()
result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
print(result)
```

### With Specific Pivot Strategy

```python
sorter = QuickSort()
result = sorter.sort([64, 34, 25], pivot_strategy="random")
print(result)
```

### Compare Strategies

```python
sorter = QuickSort()
results = sorter.compare_strategies([64, 34, 25, 12, 22, 11, 90])
for strategy, result in results.items():
    print(f"{strategy}: {result['execution_time']:.10f}s")
```
