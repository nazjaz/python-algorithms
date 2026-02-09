# Knapsack Problem Solver API Documentation

## KnapsackSolver Class

Main class for solving knapsack problems using dynamic programming and greedy algorithms.

### Constructor

```python
KnapsackSolver(config_path: str = "config.yaml") -> None
```

Initialize the solver with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

### Methods

#### solve_01_knapsack

```python
solve_01_knapsack(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Tuple[float, List[int]]
```

Solve 0-1 knapsack problem using dynamic programming.

Each item can be taken at most once (0 or 1). Uses bottom-up dynamic programming with O(n*W) time complexity where n is number of items and W is capacity.

**Parameters:**
- `weights` (List[float]): List of item weights
- `values` (List[float]): List of item values
- `capacity` (float): Maximum knapsack capacity

**Returns:**
- `Tuple[float, List[int]]`: Maximum value achievable and list of item indices selected (0-indexed)

**Raises:**
- `ValueError`: If inputs are invalid (empty lists, mismatched lengths, invalid values)

**Example:**
```python
solver = KnapsackSolver()
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
value, items = solver.solve_01_knapsack(weights, values, capacity)
# value = 220.0
# items = [1, 2]
```

#### solve_fractional_knapsack

```python
solve_fractional_knapsack(
    weights: List[float],
    values: List[float],
    capacity: float
) -> Tuple[float, List[Tuple[int, float]]]
```

Solve fractional knapsack problem using greedy algorithm.

Items can be taken in fractions. Uses greedy approach by selecting items with highest value-to-weight ratio first. This is optimal for fractional knapsack with O(n log n) time complexity.

**Parameters:**
- `weights` (List[float]): List of item weights
- `values` (List[float]): List of item values
- `capacity` (float): Maximum knapsack capacity

**Returns:**
- `Tuple[float, List[Tuple[int, float]]]`: Maximum value achievable and list of tuples (item_index, fraction_taken) where fraction_taken is between 0 and 1

**Raises:**
- `ValueError`: If inputs are invalid (empty lists, mismatched lengths, invalid values)

**Example:**
```python
solver = KnapsackSolver()
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
value, items = solver.solve_fractional_knapsack(weights, values, capacity)
# value = 240.0
# items = [(0, 1.0), (2, 1.0)]
```

#### compare_approaches

```python
compare_approaches(
    weights: List[float],
    values: List[float],
    capacity: float,
    iterations: int = 1
) -> Dict[str, any]
```

Compare 0-1 and fractional knapsack solutions.

**Parameters:**
- `weights` (List[float]): List of item weights
- `values` (List[float]): List of item values
- `capacity` (float): Maximum knapsack capacity
- `iterations` (int): Number of iterations for timing. Default: 1

**Returns:**
- `Dict[str, any]`: Dictionary containing comparison data with keys:
  - `num_items`: Number of items
  - `capacity`: Knapsack capacity
  - `iterations`: Number of iterations
  - `zero_one`: Dictionary with solution details (value, items, time, success)
  - `fractional`: Dictionary with solution details (value, items, time, success)
  - `value_difference`: Difference between fractional and 0-1 values (if both successful)
  - `fractional_better`: Boolean indicating if fractional yields higher value

**Example:**
```python
solver = KnapsackSolver()
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
results = solver.compare_approaches(weights, values, capacity)
print(results["zero_one"]["value"])
print(results["fractional"]["value"])
```

#### generate_report

```python
generate_report(
    comparison_data: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate comparison report for knapsack solutions.

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
solver = KnapsackSolver()
weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
results = solver.compare_approaches(weights, values, capacity)
report = solver.generate_report(results, output_path="report.txt")
```

### Private Methods

#### _validate_inputs

```python
_validate_inputs(
    weights: List[float],
    values: List[float],
    capacity: float
) -> None
```

Validate input parameters for knapsack problem.

**Raises:**
- `ValueError`: If inputs are invalid

## Command-Line Interface

The module can be run as a script with the following interface:

```bash
python src/main.py CAPACITY --weights W1 W2 ... --values V1 V2 ... [OPTIONS]
```

### Arguments

- `CAPACITY`: Maximum knapsack capacity (required)

### Options

- `-w, --weights`: Item weights (space-separated, required)
- `-v, --values`: Item values (space-separated, required)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - 01, fractional, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Examples

```bash
# Compare both approaches
python src/main.py 50 --weights 10 20 30 --values 60 100 120

# Use 0-1 knapsack only
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --method 01

# Use fractional knapsack only
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --method fractional

# Generate report
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --report report.txt
```

## Error Handling

All methods validate inputs and raise appropriate exceptions:

- `ValueError`: Invalid input parameters (empty lists, mismatched lengths, invalid values)
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML in configuration file
- `IOError`: File I/O errors when saving reports
- `PermissionError`: Insufficient permissions for file operations

## Algorithm Complexity

### 0-1 Knapsack

- **Time Complexity**: O(n * W) where n = number of items, W = capacity
- **Space Complexity**: O(W) for DP table, O(n * W) for item selection tracking
- **Approach**: Dynamic Programming (bottom-up)

### Fractional Knapsack

- **Time Complexity**: O(n log n) for sorting items by value-to-weight ratio
- **Space Complexity**: O(n) for sorting
- **Approach**: Greedy Algorithm (optimal for fractional variant)

## Notes

- Fractional knapsack typically yields higher or equal value compared to 0-1 knapsack since items can be partially taken
- 0-1 knapsack is NP-hard in general but can be solved efficiently with dynamic programming when capacity is not too large
- Fractional knapsack can always be solved optimally with greedy algorithm
- Both implementations handle edge cases like empty lists, invalid inputs, and boundary conditions
