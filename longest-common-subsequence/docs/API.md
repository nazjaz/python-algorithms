# Longest Common Subsequence API Documentation

## Overview

The LCS Calculator provides an implementation of the Longest Common Subsequence algorithm using dynamic programming with backtracking. It finds the longest subsequence common to two strings, where a subsequence is a sequence that appears in the same relative order but not necessarily contiguous.

## Classes

### LCSCalculator

Main class for calculating Longest Common Subsequence.

#### Constructor

```python
LCSCalculator(config_path: str = "config.yaml") -> None
```

Initialize calculator with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### lcs_length

```python
lcs_length(str1: str, str2: str) -> int
```

Calculate length of LCS using dynamic programming.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `int`: Length of longest common subsequence

**Time Complexity:** O(m * n)
**Space Complexity:** O(m * n)

##### lcs

```python
lcs(str1: str, str2: str) -> str
```

Find longest common subsequence using dynamic programming and backtracking.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `str`: Longest common subsequence string

**Time Complexity:** O(m * n)
**Space Complexity:** O(m * n)

##### lcs_all

```python
lcs_all(str1: str, str2: str) -> List[str]
```

Find all longest common subsequences.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `List[str]`: List of all LCS strings (may contain duplicates)

**Time Complexity:** O(m * n * k) where k is number of LCS

##### visualize_dp_table

```python
visualize_dp_table(str1: str, str2: str) -> str
```

Generate visualization of DP table.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `str`: String representation of DP table

##### calculate_with_details

```python
calculate_with_details(str1: str, str2: str) -> Dict[str, any]
```

Calculate LCS with detailed information.

**Parameters:**
- `str1` (str): First string
- `str2` (str): Second string

**Returns:**
- `Dict[str, any]`: Dictionary containing detailed LCS information

##### generate_report

```python
generate_report(
    result: Dict[str, any], output_path: Optional[str] = None
) -> str
```

Generate detailed LCS analysis report.

**Parameters:**
- `result` (Dict[str, any]): Result dictionary from calculate_with_details
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

## Algorithm Details

### Dynamic Programming Approach

The algorithm uses a 2D DP table where:
- `dp[i][j]` = length of LCS of `str1[0:i]` and `str2[0:j]`

**Recurrence Relation:**
- If `str1[i-1] == str2[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- Else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

### Backtracking

After building the DP table, backtrack to reconstruct the actual LCS:
- Start from `dp[m][n]`
- Move diagonally when characters match
- Move up or left when they don't match

## Usage Examples

### Basic LCS Calculation

```python
from src.main import LCSCalculator

calculator = LCSCalculator()
lcs = calculator.lcs("ABCDGH", "AEDFHR")
print(lcs)  # "ADH"
```

### LCS Length Only

```python
length = calculator.lcs_length("ABCDGH", "AEDFHR")
print(length)  # 3
```

### Visualize DP Table

```python
calculator.lcs_length("ABC", "AC")
visualization = calculator.visualize_dp_table("ABC", "AC")
print(visualization)
```

### Detailed Analysis

```python
result = calculator.calculate_with_details("ABCDGH", "AEDFHR")
print(f"LCS: {result['lcs']}, Length: {result['length']}")
```
