# Fast Exponentiation API Documentation

## Overview

The Fast Exponentiation Calculator provides efficient power calculation using the exponentiation by squaring algorithm. It calculates a^n in O(log n) time complexity instead of O(n) time, with support for both iterative and recursive implementations, modular exponentiation, and comprehensive time complexity analysis.

## Classes

### FastExponentiationCalculator

Main class for fast exponentiation calculations with time complexity analysis.

#### Constructor

```python
FastExponentiationCalculator(config_path: str = "config.yaml") -> None
```

Initialize calculator with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### power_naive

```python
power_naive(base: float, exponent: int) -> float
```

Calculate power using naive method (O(n) time).

**Parameters:**
- `base` (float): Base number
- `exponent` (int): Exponent (must be non-negative integer)

**Returns:**
- `float`: Result of base raised to exponent

**Time Complexity:** O(n)

##### power_fast_recursive

```python
power_fast_recursive(
    base: float, exponent: int, track_steps: bool = False
) -> float
```

Calculate power using fast exponentiation (recursive, O(log n)).

**Parameters:**
- `base` (float): Base number
- `exponent` (int): Exponent (must be non-negative integer)
- `track_steps` (bool): If True, track algorithm steps

**Returns:**
- `float`: Result of base raised to exponent

**Time Complexity:** O(log n)
**Space Complexity:** O(log n) due to recursion

##### power_fast_iterative

```python
power_fast_iterative(
    base: float, exponent: int, track_steps: bool = False
) -> float
```

Calculate power using fast exponentiation (iterative, O(log n)).

**Parameters:**
- `base` (float): Base number
- `exponent` (int): Exponent (must be non-negative integer)
- `track_steps` (bool): If True, track algorithm steps

**Returns:**
- `float`: Result of base raised to exponent

**Time Complexity:** O(log n)
**Space Complexity:** O(1)

##### power_modular

```python
power_modular(
    base: int, exponent: int, modulus: int, track_steps: bool = False
) -> int
```

Calculate modular exponentiation (base^exponent mod modulus).

**Parameters:**
- `base` (int): Base number (integer)
- `exponent` (int): Exponent (must be non-negative integer)
- `modulus` (int): Modulus for modular arithmetic
- `track_steps` (bool): If True, track algorithm steps

**Returns:**
- `int`: Result of (base^exponent) mod modulus

**Time Complexity:** O(log n)

##### calculate_with_analysis

```python
calculate_with_analysis(
    base: float,
    exponent: int,
    method: str = "fast_iterative",
    track_steps: bool = False,
) -> Dict[str, Any]
```

Calculate power with time complexity analysis.

**Parameters:**
- `base` (float): Base number
- `exponent` (int): Exponent (must be non-negative integer)
- `method` (str): Method to use ('naive', 'fast_recursive', 'fast_iterative')
- `track_steps` (bool): If True, track algorithm steps

**Returns:**
- `Dict[str, Any]`: Dictionary containing result and analysis

##### compare_methods

```python
compare_methods(
    base: float, exponent: int, track_steps: bool = False
) -> Dict[str, Any]
```

Compare naive and fast exponentiation methods.

**Parameters:**
- `base` (float): Base number
- `exponent` (int): Exponent (must be non-negative integer)
- `track_steps` (bool): If True, track algorithm steps

**Returns:**
- `Dict[str, Any]`: Dictionary with comparison results

## Algorithm Details

### Fast Exponentiation (Exponentiation by Squaring)

The algorithm uses the following properties:
- If exponent is even: base^exponent = (base^(exponent/2))^2
- If exponent is odd: base^exponent = base * (base^((exponent-1)/2))^2

### Time Complexity

- **Naive Method**: O(n) - n multiplications
- **Fast Exponentiation**: O(log n) - approximately log2(n) multiplications

### Example

For 2^10:
- Naive: 10 operations
- Fast: 4 operations (2^10 = (2^5)^2 = ((2^2)^2 * 2)^2)

## Usage Examples

### Basic Fast Exponentiation

```python
from src.main import FastExponentiationCalculator

calculator = FastExponentiationCalculator()
result = calculator.power_fast_iterative(2, 10)
print(result)  # 1024.0
```

### With Analysis

```python
analysis = calculator.calculate_with_analysis(2, 10, "fast_iterative")
print(f"Result: {analysis['result']}")
print(f"Time Complexity: {analysis['time_complexity']}")
```

### Modular Exponentiation

```python
result = calculator.power_modular(2, 10, 7)
print(result)  # 2^10 mod 7
```

### Compare Methods

```python
comparison = calculator.compare_methods(2, 20)
print(f"Speedup: {comparison['speedup']}x")
```
