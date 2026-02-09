# GCD Calculator API Documentation

## Overview

The GCD Calculator provides implementations of the Euclidean algorithm and Extended Euclidean algorithm for finding the greatest common divisor (GCD) of integers. The Extended Euclidean algorithm also finds coefficients for linear combinations.

## Classes

### GCDCalculator

Main class for calculating GCD using Euclidean and Extended Euclidean algorithms.

#### Constructor

```python
GCDCalculator(config_path: str = "config.yaml") -> None
```

Initialize calculator with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

#### Methods

##### gcd

```python
gcd(a: int, b: int) -> int
```

Calculate GCD using Euclidean algorithm.

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer

**Returns:**
- `int`: Greatest common divisor of a and b

**Raises:**
- `ValueError`: If both a and b are zero

**Example:**
```python
calculator = GCDCalculator()
result = calculator.gcd(48, 18)
# Returns: 6
```

##### extended_gcd

```python
extended_gcd(a: int, b: int) -> Tuple[int, int, int]
```

Calculate GCD and coefficients using Extended Euclidean algorithm.

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer

**Returns:**
- `Tuple[int, int, int]`: (gcd, x, y) where:
  - `gcd`: Greatest common divisor of a and b
  - `x`: Coefficient for a in linear combination
  - `y`: Coefficient for b in linear combination
  - Satisfies: gcd(a, b) = ax + by

**Raises:**
- `ValueError`: If both a and b are zero

**Example:**
```python
gcd, x, y = calculator.extended_gcd(48, 18)
# Returns: (6, 1, -2)
# Verification: 48*1 + 18*(-2) = 6
```

##### gcd_multiple

```python
gcd_multiple(numbers: List[int]) -> int
```

Calculate GCD of multiple numbers.

**Parameters:**
- `numbers` (List[int]): List of integers

**Returns:**
- `int`: Greatest common divisor of all numbers

**Raises:**
- `ValueError`: If list is empty or all numbers are zero

**Example:**
```python
result = calculator.gcd_multiple([48, 18, 12])
# Returns: 6
```

##### lcm

```python
lcm(a: int, b: int) -> int
```

Calculate Least Common Multiple using GCD.

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer

**Returns:**
- `int`: Least common multiple of a and b

**Raises:**
- `ValueError`: If both a and b are zero

**Example:**
```python
result = calculator.lcm(4, 6)
# Returns: 12
```

##### modular_inverse

```python
modular_inverse(a: int, m: int) -> Optional[int]
```

Find modular inverse of a modulo m using Extended Euclidean.

**Parameters:**
- `a` (int): Integer to find inverse for
- `m` (int): Modulus

**Returns:**
- `Optional[int]`: Modular inverse of a modulo m, or None if it doesn't exist

**Raises:**
- `ValueError`: If modulus is not positive

**Example:**
```python
inverse = calculator.modular_inverse(3, 11)
# Returns: 4
# Verification: (3 * 4) % 11 = 1
```

##### verify_linear_combination

```python
verify_linear_combination(
    a: int, b: int, gcd_val: int, x: int, y: int
) -> bool
```

Verify that gcd(a, b) = ax + by.

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer
- `gcd_val` (int): GCD value to verify
- `x` (int): Coefficient for a
- `y` (int): Coefficient for b

**Returns:**
- `bool`: True if linear combination is correct, False otherwise

**Example:**
```python
is_valid = calculator.verify_linear_combination(48, 18, 6, 1, -2)
# Returns: True
```

##### calculate_with_details

```python
calculate_with_details(
    a: int, b: int, use_extended: bool = False
) -> Dict[str, any]
```

Calculate GCD with detailed results.

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer
- `use_extended` (bool): If True, use extended algorithm

**Returns:**
- `Dict[str, any]`: Dictionary containing calculation details

**Example:**
```python
result = calculator.calculate_with_details(48, 18, use_extended=True)
# Returns: {
#   'a': 48, 'b': 18, 'gcd': 6, 'lcm': 144,
#   'extended_gcd': {'gcd': 6, 'x': 1, 'y': -2, ...}
# }
```

##### generate_report

```python
generate_report(
    a: int,
    b: int,
    result: Dict[str, any],
    output_path: Optional[str] = None
) -> str
```

Generate calculation report.

**Parameters:**
- `a` (int): First integer
- `b` (int): Second integer
- `result` (Dict[str, any]): Calculation result dictionary
- `output_path` (Optional[str]): Optional path to save report file

**Returns:**
- `str`: Report content as string

**Raises:**
- `IOError`: If file cannot be written
- `PermissionError`: If insufficient permissions to write file

## Algorithm Complexity

- **Time Complexity**: O(log min(a, b)) for both algorithms
- **Space Complexity**: O(1) for Euclidean, O(1) for Extended Euclidean

## Mathematical Properties

### Euclidean Algorithm

Based on the property: gcd(a, b) = gcd(b, a mod b)

### Extended Euclidean Algorithm

Finds coefficients x and y such that: gcd(a, b) = ax + by

### Relationship with LCM

lcm(a, b) * gcd(a, b) = |a * b|

## Applications

1. **Simplifying fractions**: gcd(numerator, denominator)
2. **Cryptography**: RSA algorithm, modular arithmetic
3. **Number theory**: Solving linear Diophantine equations
4. **Chinese Remainder Theorem**: Finding solutions to systems of congruences
5. **Modular inverses**: Finding multiplicative inverses in modular arithmetic

## Usage Examples

### Basic GCD Calculation

```python
from src.main import GCDCalculator

calculator = GCDCalculator()
print(calculator.gcd(48, 18))  # 6
```

### Extended Euclidean Algorithm

```python
gcd, x, y = calculator.extended_gcd(48, 18)
print(f"gcd(48, 18) = {gcd}")
print(f"48*{x} + 18*{y} = {gcd}")
```

### Modular Inverse

```python
inverse = calculator.modular_inverse(3, 11)
if inverse:
    print(f"Modular inverse: {inverse}")
```

### Multiple Numbers

```python
result = calculator.gcd_multiple([48, 18, 12])
print(f"GCD: {result}")
```
