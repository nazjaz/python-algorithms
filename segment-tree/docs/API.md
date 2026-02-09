# Segment Tree API Documentation

## SegmentTree Class

Main class for segment tree data structure with lazy propagation.

### Constructor

```python
SegmentTree(
    arr: List[float],
    operation: str = "sum",
    config_path: str = "config.yaml"
) -> None
```

Initialize SegmentTree with array and operation.

**Parameters:**
- `arr` (List[float]): Input array
- `operation` (str): Operation type - 'sum', 'min', or 'max'. Default: "sum"
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `ValueError`: If array is empty or operation is invalid
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
arr = [1, 2, 3, 4, 5]
st = SegmentTree(arr, operation="sum")
```

### Methods

#### query

```python
query(left: int, right: int) -> float
```

Query range [left, right].

**Parameters:**
- `left` (int): Left index (0-indexed, inclusive)
- `right` (int): Right index (0-indexed, inclusive)

**Returns:**
- `float`: Result of operation over range

**Raises:**
- `ValueError`: If indices are invalid

**Time Complexity:** O(log n) where n is array size

**Example:**
```python
st = SegmentTree([1, 2, 3, 4, 5], operation="sum")
result = st.query(0, 4)  # Returns 15.0
result = st.query(1, 3)  # Returns 9.0
```

#### update_point

```python
update_point(index: int, value: float) -> None
```

Update single point at index.

**Parameters:**
- `index` (int): Index to update (0-indexed)
- `value` (float): New value

**Raises:**
- `ValueError`: If index is invalid

**Time Complexity:** O(log n) where n is array size

**Example:**
```python
st = SegmentTree([1, 2, 3, 4, 5], operation="sum")
st.update_point(2, 10)  # Updates index 2 to 10
```

#### update_range

```python
update_range(left: int, right: int, value: float) -> None
```

Update range [left, right] with lazy propagation.

**Parameters:**
- `left` (int): Left index (0-indexed, inclusive)
- `right` (int): Right index (0-indexed, inclusive)
- `value` (float): Value to add/update

**Raises:**
- `ValueError`: If indices are invalid

**Time Complexity:** O(log n) where n is array size (with lazy propagation)

**Example:**
```python
st = SegmentTree([1, 2, 3, 4, 5], operation="sum")
st.update_range(1, 3, 5)  # Adds 5 to elements at indices 1, 2, 3
```

#### get_array

```python
get_array() -> List[float]
```

Get current array values.

**Returns:**
- `List[float]`: Copy of current array

**Time Complexity:** O(n) where n is array size

**Example:**
```python
st = SegmentTree([1, 2, 3, 4, 5], operation="sum")
arr = st.get_array()  # Returns [1, 2, 3, 4, 5]
```

#### compare_operations

```python
compare_operations(
    queries: List[tuple],
    iterations: int = 1
) -> Dict[str, any]
```

Compare performance of different operations.

**Parameters:**
- `queries` (List[tuple]): List of query tuples (type, *args)
  - For query: ("query", left, right)
  - For update_point: ("update_point", index, value)
  - For update_range: ("update_range", left, right, value)
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing performance data

**Example:**
```python
st = SegmentTree([1, 2, 3, 4, 5], operation="sum")
queries = [
    ("query", 0, 4),
    ("update_point", 2, 10),
    ("update_range", 1, 3, 5),
]
performance = st.compare_operations(queries, iterations=1000)
```

#### generate_report

```python
generate_report(
    performance_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate performance report for segment tree operations.

**Parameters:**
- `performance_data` (Dict[str, any]): Performance data from `compare_operations()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py NUMBERS [OPTIONS]
```

### Arguments

- `NUMBERS`: (Required) Numbers in the array (space-separated)

### Options

- `-o, --operation`: Operation type - sum, min, or max (default: sum)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-q, --query`: Query range [left, right] (two integers)
- `-u, --update-point`: Update point at index with value (index, value)
- `-r, --update-range`: Update range [left, right] with value (left, right, value)
- `-a, --array`: Display current array

### Examples

```bash
# Create segment tree
python src/main.py 1 2 3 4 5 --operation sum

# Query range
python src/main.py 1 2 3 4 5 --operation sum --query 0 4

# Update point
python src/main.py 1 2 3 4 5 --operation sum --update-point 2 10

# Update range
python src/main.py 1 2 3 4 5 --operation sum --update-range 1 3 5

# Display array
python src/main.py 1 2 3 4 5 --operation sum --array
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (empty array, invalid indices, invalid ranges, invalid operation)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### Time Complexity

- **Build**: O(n) where n is array size
- **Query**: O(log n) for range query
- **Point Update**: O(log n) for single element update
- **Range Update**: O(log n) with lazy propagation (without lazy: O(n log n))

### Space Complexity

- **Overall**: O(n) for tree and lazy arrays
- **Per Operation**: O(log n) for recursion stack

## Lazy Propagation

Lazy propagation is an optimization technique that defers updates until they are needed:

- **How it works**: Updates are stored in a lazy array and applied when querying
- **Benefits**: Reduces range update complexity from O(n log n) to O(log n)
- **When to use**: Essential for efficient range updates
- **Implementation**: Uses `_push_lazy()` method to propagate lazy values

## Notes

- Segment tree is optimal for range operations
- Query and update times are O(log n) independent of range size
- Lazy propagation is essential for efficient range updates
- Supports three operations: sum, min, max
- Array indices are 0-indexed
- All ranges are inclusive [left, right]
- Lazy propagation maintains O(log n) complexity for range updates
- Tree size is O(n) but may use more space for power-of-2 padding
- Operations are performed in-place (array is modified)
- Floating point numbers are supported
