# Longest Increasing Subsequence API Documentation

## LongestIncreasingSubsequence Class

Main class for finding longest increasing subsequence using dynamic programming and binary search optimization.

### Constructor

```python
LongestIncreasingSubsequence(config_path: str = "config.yaml") -> None
```

Initialize LongestIncreasingSubsequence with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### find_lis_dp

```python
find_lis_dp(arr: List[float]) -> Tuple[int, List[float]]
```

Find LIS using dynamic programming approach.

Uses O(n²) dynamic programming where dp[i] represents the length of LIS ending at index i. For each element, check all previous elements to find the longest subsequence that can be extended.

**Parameters:**
- `arr` (List[float]): Input array of numbers

**Returns:**
- `Tuple[int, List[float]]`: Length of LIS and one example of LIS

**Time Complexity:** O(n²) where n is array length

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
length, sequence = lis_solver.find_lis_dp(arr)
# length = 4
# sequence = [2, 3, 7, 18] or [2, 5, 7, 101]
```

#### find_lis_binary_search

```python
find_lis_binary_search(arr: List[float]) -> Tuple[int, List[float]]
```

Find LIS using binary search optimization.

Uses O(n log n) approach with binary search. Maintains an array `tails` where tails[i] is the smallest tail element of all increasing subsequences of length i+1. This allows us to use binary search to find where to extend subsequences.

**Parameters:**
- `arr` (List[float]): Input array of numbers

**Returns:**
- `Tuple[int, List[float]]`: Length of LIS and one example of LIS

**Time Complexity:** O(n log n) where n is array length

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
length, sequence = lis_solver.find_lis_binary_search(arr)
# length = 4
# sequence = [2, 3, 7, 18] or [2, 5, 7, 101]
```

#### get_lis_length_dp

```python
get_lis_length_dp(arr: List[float]) -> int
```

Get LIS length using dynamic programming.

**Parameters:**
- `arr` (List[float]): Input array of numbers

**Returns:**
- `int`: Length of LIS

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
length = lis_solver.get_lis_length_dp(arr)
# length = 4
```

#### get_lis_length_binary_search

```python
get_lis_length_binary_search(arr: List[float]) -> int
```

Get LIS length using binary search optimization.

**Parameters:**
- `arr` (List[float]): Input array of numbers

**Returns:**
- `int`: Length of LIS

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
length = lis_solver.get_lis_length_binary_search(arr)
# length = 4
```

#### get_lis_sequence_dp

```python
get_lis_sequence_dp(arr: List[float]) -> List[float]
```

Get LIS sequence using dynamic programming.

**Parameters:**
- `arr` (List[float]): Input array of numbers

**Returns:**
- `List[float]`: One example of LIS

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
sequence = lis_solver.get_lis_sequence_dp(arr)
# sequence = [2, 3, 7, 18] or [2, 5, 7, 101]
```

#### get_lis_sequence_binary_search

```python
get_lis_sequence_binary_search(arr: List[float]) -> List[float]
```

Get LIS sequence using binary search optimization.

**Parameters:**
- `arr` (List[float]): Input array of numbers

**Returns:**
- `List[float]`: One example of LIS

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
sequence = lis_solver.get_lis_sequence_binary_search(arr)
# sequence = [2, 3, 7, 18] or [2, 5, 7, 101]
```

#### compare_approaches

```python
compare_approaches(
    arr: List[float],
    iterations: int = 1
) -> Dict[str, any]
```

Compare DP and binary search approaches.

**Parameters:**
- `arr` (List[float]): Input array of numbers
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing comparison data with keys:
    - `array_length`: Length of input array
    - `iterations`: Number of iterations
    - `dp`: Dictionary with DP results (length, sequence, time, success)
    - `binary_search`: Dictionary with binary search results (length, sequence, time, success)
    - `fastest`: Fastest approach name (if both successful)
    - `fastest_time`: Time of fastest approach

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
comparison = lis_solver.compare_approaches(arr, iterations=1000)
print(comparison["dp"]["time_milliseconds"])
print(comparison["binary_search"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    comparison_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate comparison report for LIS approaches.

**Parameters:**
- `comparison_data` (Dict[str, any]): Comparison data from `compare_approaches()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

**Example:**
```python
lis_solver = LongestIncreasingSubsequence()
arr = [10, 9, 2, 5, 3, 7, 101, 18]
comparison = lis_solver.compare_approaches(arr)
report = lis_solver.generate_report(comparison, output_path="report.txt")
```

### Private Methods

#### _binary_search

```python
_binary_search(
    tails: List[float],
    target: float,
    left: int,
    right: int
) -> int
```

Binary search helper to find insertion position.

Finds the leftmost position where target can be inserted in sorted array tails to maintain sorted order.

**Parameters:**
- `tails`: Sorted array of tail elements
- `target`: Value to find position for
- `left`: Left boundary
- `right`: Right boundary

**Returns:**
- `int`: Insertion position index

**Time Complexity:** O(log n)

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py NUMBERS [OPTIONS]
```

### Arguments

- `NUMBERS`: (Required) Numbers in the array (space-separated)

### Options

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - dp, binary, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Compare both approaches
python src/main.py 10 9 2 5 3 7 101 18 --method compare

# Use DP approach only
python src/main.py 10 9 2 5 3 7 101 18 --method dp

# Use binary search approach only
python src/main.py 10 9 2 5 3 7 101 18 --method binary

# Generate report
python src/main.py 10 9 2 5 3 7 101 18 --method compare --report report.txt
```

## Error Handling

All methods handle edge cases gracefully:

- Empty arrays return length 0 and empty sequence
- Single element arrays return length 1
- All equal elements return length 1
- Negative numbers and floats are supported
- Both approaches produce identical LIS lengths

## Algorithm Complexity

### Dynamic Programming Approach

- **Time Complexity**: O(n²) where n is array length
- **Space Complexity**: O(n) for DP table and parent array
- **Best For**: Small arrays, when simplicity is preferred

### Binary Search Optimization Approach

- **Time Complexity**: O(n log n) where n is array length
- **Space Complexity**: O(n) for tails array and parent array
- **Best For**: Large arrays, when performance is critical

## Notes

- Subsequence means elements don't need to be consecutive
- Increasing means strictly increasing (no equal values)
- LIS may not be unique - algorithm returns one valid LIS
- Both approaches produce same length but may return different sequences
- Binary search approach is optimal for comparison-based algorithms
- DP approach is simpler and may be faster for small arrays
- Empty arrays return empty LIS
- Single element arrays return that element as LIS
- All equal elements result in LIS length 1
- Negative numbers and floating point numbers are supported
