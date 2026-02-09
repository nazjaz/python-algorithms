# API Documentation

## PrimeChecker Class

The main class for checking if numbers are prime using optimized trial division.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the PrimeChecker with configuration.

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

#### `is_prime(n: int) -> bool`

Check if a number is prime using optimized trial division.

**Parameters:**
- `n` (int): Integer to check for primality.

**Returns:**
- `bool`: True if n is prime, False otherwise.

**Algorithm:**
1. Reject numbers less than 2
2. Accept 2 as prime
3. Reject even numbers (except 2)
4. Test divisibility by odd numbers from 3 to √n
5. Return True if no divisor found

**Optimizations:**
- Early even number check (except 2)
- Only test odd divisors
- Only test up to square root

**Time Complexity:** O(√n)
**Space Complexity:** O(1)

**Example:**
```python
checker = PrimeChecker()
result = checker.is_prime(17)
print(result)  # True
```

#### `find_primes_in_range(start: int, end: int) -> List[int]`

Find all prime numbers in a given range.

**Parameters:**
- `start` (int): Start of range (inclusive).
- `end` (int): End of range (inclusive).

**Returns:**
- `List[int]`: List of prime numbers in the range.

**Note:**
- Automatically adjusts start to 2 if less than 2
- Uses is_prime() for each number in range

**Example:**
```python
checker = PrimeChecker()
primes = checker.find_primes_in_range(1, 20)
print(primes)  # [2, 3, 5, 7, 11, 13, 17, 19]
```

#### `get_analysis() -> dict`

Get detailed analysis of the last prime check.

**Returns:**
- `dict`: Dictionary containing analysis data with keys:
  - `number`: Number that was checked
  - `is_prime`: Whether number is prime
  - `divisions_performed`: Number of divisions performed
  - `square_root`: Square root of the number
  - `factors_found`: List of factors if composite (empty if prime)
  - `total_divisions`: Total divisions performed
  - `optimization_benefit`: Percentage benefit from optimizations

**Example:**
```python
checker.is_prime(17)
analysis = checker.get_analysis()
print(f"Divisions: {analysis['divisions_performed']}")
print(f"Optimization benefit: {analysis['optimization_benefit']:.2f}%")
```

#### `generate_report(output_path: Optional[str] = None) -> str`

Generate analysis report.

**Parameters:**
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Report Contents:**
- Result (number and primality)
- Performance metrics (divisions, optimization benefit)
- Factors if composite
- Algorithm details and complexity

**Example:**
```python
checker.is_prime(17)
report = checker.generate_report(output_path="report.txt")
print(report)
```

### Attributes

#### `divisions: int`

Total number of divisions performed during last prime check. Incremented for each divisor tested.

#### `analysis_data: dict`

Dictionary containing detailed analysis data about the last prime check, including number, result, divisions, factors, and performance metrics.

#### `config: dict`

Configuration dictionary loaded from YAML file.

### Example Usage

```python
from src.main import PrimeChecker

# Initialize with default config
checker = PrimeChecker()

# Or with custom config
checker = PrimeChecker(config_path="custom_config.yaml")

# Check if number is prime
is_prime = checker.is_prime(17)
print(f"17 is prime: {is_prime}")

# Find primes in range
primes = checker.find_primes_in_range(1, 100)
print(f"Found {len(primes)} primes")

# Get analysis
analysis = checker.get_analysis()
print(f"Divisions: {analysis['divisions_performed']}")

# Generate report
report = checker.generate_report(output_path="analysis.txt")
```

### Algorithm Complexity

**Time Complexity:**
- Best case: O(1) - for even numbers or numbers < 2
- Average case: O(√n) - for odd numbers
- Worst case: O(√n) - for large primes

**Space Complexity:** O(1) - only uses constant extra space

**Optimization Benefits:**
- Even number check: ~50% reduction for even numbers
- Odd divisor testing: ~50% reduction in tests
- Square root limit: Reduces from O(n) to O(√n)
- Combined: Significant improvement over naive approach

### Performance Notes

- Algorithm is efficient for numbers up to ~10^12
- For very large numbers, consider probabilistic methods
- Optimizations provide substantial performance gains
- Division count is approximately √n/2 for odd numbers
- Works correctly for all integer inputs
