# Edit Distance API Documentation

## EditDistance Class

Main class for calculating edit distance (Levenshtein distance) using dynamic programming.

### Constructor

```python
EditDistance(config_path: str = "config.yaml") -> None
```

Initialize EditDistance with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### calculate_dp

```python
calculate_dp(str1: str, str2: str) -> Tuple[int, List[List[int]]]
```

Calculate edit distance using standard dynamic programming.

Uses O(m*n) space for DP table where m and n are string lengths.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `Tuple[int, List[List[int]]]`: Edit distance and DP table

**Time Complexity:** O(m*n) where m=len(str1), n=len(str2)

**Space Complexity:** O(m*n)

**Example:**
```python
ed = EditDistance()
distance, dp_table = ed.calculate_dp("kitten", "sitting")
# distance = 3
# dp_table = [[0, 1, 2, ...], [1, 1, 2, ...], ...]
```

#### calculate_optimized

```python
calculate_optimized(str1: str, str2: str) -> Tuple[int, List[int]]
```

Calculate edit distance using space-optimized DP.

Uses O(min(m,n)) space by keeping only two rows of DP table.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `Tuple[int, List[int]]`: Edit distance and last row of DP table

**Time Complexity:** O(m*n) where m=len(str1), n=len(str2)

**Space Complexity:** O(min(m,n))

**Example:**
```python
ed = EditDistance()
distance, last_row = ed.calculate_optimized("kitten", "sitting")
# distance = 3
```

#### get_distance_dp

```python
get_distance_dp(str1: str, str2: str) -> int
```

Get edit distance using standard DP.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `int`: Edit distance

**Example:**
```python
ed = EditDistance()
distance = ed.get_distance_dp("kitten", "sitting")
# distance = 3
```

#### get_distance_optimized

```python
get_distance_optimized(str1: str, str2: str) -> int
```

Get edit distance using space-optimized DP.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `int`: Edit distance

**Example:**
```python
ed = EditDistance()
distance = ed.get_distance_optimized("kitten", "sitting")
# distance = 3
```

#### get_operations

```python
get_operations(
    str1: str,
    str2: str,
    dp: List[List[int]]
) -> List[str]
```

Get sequence of operations to transform str1 to str2.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string
- `dp` (List[List[int]]): DP table from calculate_dp()

**Returns:**
- `List[str]`: List of operation descriptions

**Example:**
```python
ed = EditDistance()
distance, dp_table = ed.calculate_dp("kitten", "sitting")
operations = ed.get_operations("kitten", "sitting", dp_table)
# operations = ["Replace 'k' at position 0 with 's'", ...]
```

#### compare_approaches

```python
compare_approaches(
    str1: str,
    str2: str,
    iterations: int = 1
) -> Dict[str, any]
```

Compare standard DP and space-optimized approaches.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing comparison data with keys:
    - `str1_length`: Length of first string
    - `str2_length`: Length of second string
    - `dp`: Dictionary with DP results (distance, space_used, time, success)
    - `optimized`: Dictionary with optimized results (distance, space_used, time, success)
    - `space_savings_percent`: Percentage of space saved (if both successful)
    - `fastest`: Fastest approach name (if both successful)
    - `fastest_time`: Time of fastest approach

**Example:**
```python
ed = EditDistance()
comparison = ed.compare_approaches("kitten", "sitting", iterations=1000)
print(comparison["dp"]["time_milliseconds"])
print(comparison["optimized"]["time_milliseconds"])
```

#### generate_report

```python
generate_report(
    comparison_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate comparison report for edit distance approaches.

**Parameters:**
- `comparison_data` (Dict[str, any]): Comparison data from `compare_approaches()`
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If file is not writable

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py STR1 STR2 [OPTIONS]
```

### Arguments

- `STR1`: (Required) First string
- `STR2`: (Required) Second string

### Options

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - dp, optimized, or compare (default: compare)
- `-o, --operations`: Show sequence of operations
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Compare both approaches
python src/main.py "kitten" "sitting" --method compare

# Use DP approach only
python src/main.py "kitten" "sitting" --method dp

# Use optimized approach only
python src/main.py "kitten" "sitting" --method optimized

# Show operations
python src/main.py "kitten" "sitting" --method compare --operations

# Generate report
python src/main.py "kitten" "sitting" --method compare --report report.txt
```

## Error Handling

All methods handle edge cases gracefully:

- Empty strings return distance equal to length of non-empty string
- Identical strings return distance 0
- Both approaches produce identical results
- Unicode and special characters are supported

## Algorithm Complexity

### Standard Dynamic Programming

- **Time Complexity**: O(m*n) where m=len(str1), n=len(str2)
- **Space Complexity**: O(m*n) for DP table
- **Best For**: When operation sequence is needed

### Space-Optimized Dynamic Programming

- **Time Complexity**: O(m*n) where m=len(str1), n=len(str2)
- **Space Complexity**: O(min(m,n)) using two rows
- **Best For**: Large strings or memory-constrained environments

## Notes

- Edit distance measures minimum operations (insert, delete, replace)
- All operations have cost 1
- Both approaches produce identical results
- Space-optimized version uses O(min(m,n)) space
- Operation sequence can only be reconstructed from standard DP
- Empty strings are handled correctly
- Unicode and special characters are supported
- Time complexity is same for both approaches
- Space savings can be significant for large strings
