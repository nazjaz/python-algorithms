# Extended Euclidean and CRT API Documentation

## Classes

### ExtendedEuclidean

Main class for extended Euclidean algorithm and Chinese Remainder Theorem.

#### Methods

##### `__init__(self) -> None`

Initialize Extended Euclidean calculator.

**Returns**: None

**Example**:
```python
ee = ExtendedEuclidean()
```

---

##### `extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]`

Compute extended GCD and Bézout coefficients.

Finds integers x and y such that: ax + by = gcd(a, b)

**Parameters**:
- `a` (int): First integer.
- `b` (int): Second integer.

**Returns**:
- `Tuple[int, int, int]`: (gcd, x, y) where:
  - gcd is the greatest common divisor of a and b
  - x and y are Bézout coefficients satisfying ax + by = gcd(a, b)

**Example**:
```python
ee = ExtendedEuclidean()
gcd, x, y = ee.extended_gcd(48, 18)
# Returns: (6, -1, 3)
# Verification: 48*(-1) + 18*3 = 6
```

---

##### `gcd(self, a: int, b: int) -> int`

Compute greatest common divisor.

**Parameters**:
- `a` (int): First integer.
- `b` (int): Second integer.

**Returns**:
- `int`: GCD of a and b.

**Example**:
```python
ee = ExtendedEuclidean()
gcd = ee.gcd(48, 18)
# Returns: 6
```

---

##### `modular_inverse(self, a: int, m: int) -> Optional[int]`

Compute modular inverse of a modulo m.

Finds x such that: ax ≡ 1 (mod m)

**Parameters**:
- `a` (int): Number to find inverse for.
- `m` (int): Modulus.

**Returns**:
- `Optional[int]`: Modular inverse of a modulo m, or None if it doesn't exist.

**Raises**:
- `ValueError`: If m <= 0.

**Example**:
```python
ee = ExtendedEuclidean()
inv = ee.modular_inverse(3, 7)
# Returns: 5
# Verification: (3 * 5) % 7 == 1
```

---

##### `solve_congruence(self, a: int, b: int, m: int) -> Optional[List[int]]`

Solve linear congruence ax ≡ b (mod m).

**Parameters**:
- `a` (int): Coefficient.
- `b` (int): Constant term.
- `m` (int): Modulus.

**Returns**:
- `Optional[List[int]]`: List of solutions modulo m, or None if no solution exists.

**Raises**:
- `ValueError`: If m <= 0.

**Example**:
```python
ee = ExtendedEuclidean()
solutions = ee.solve_congruence(3, 1, 7)
# Returns: [5]
# Verification: (3 * 5) % 7 == 1
```

---

##### `chinese_remainder_theorem(self, remainders: List[int], moduli: List[int]) -> Optional[Tuple[int, int]]`

Solve system of congruences using Chinese Remainder Theorem (coprime moduli).

Solves the system:
x ≡ r₁ (mod m₁)
x ≡ r₂ (mod m₂)
...
x ≡ rₙ (mod mₙ)

**Parameters**:
- `remainders` (List[int]): List of remainders [r₁, r₂, ..., rₙ].
- `moduli` (List[int]): List of moduli [m₁, m₂, ..., mₙ] (must be pairwise coprime).

**Returns**:
- `Optional[Tuple[int, int]]`: (solution, M) where:
  - solution is the unique solution modulo M
  - M is the product of all moduli
  Returns None if no solution exists.

**Raises**:
- `ValueError`: If lists have different lengths or moduli are invalid.

**Example**:
```python
ee = ExtendedEuclidean()
result = ee.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
# Returns: (23, 105)
# Verification: 23 % 3 == 2, 23 % 5 == 3, 23 % 7 == 2
```

---

##### `chinese_remainder_theorem_general(self, remainders: List[int], moduli: List[int]) -> Optional[Tuple[int, int]]`

Solve system of congruences (general case, moduli need not be coprime).

**Parameters**:
- `remainders` (List[int]): List of remainders [r₁, r₂, ..., rₙ].
- `moduli` (List[int]): List of moduli [m₁, m₂, ..., mₙ].

**Returns**:
- `Optional[Tuple[int, int]]`: (solution, M) where:
  - solution is a solution modulo M
  - M is the least common multiple of moduli
  Returns None if no solution exists.

**Raises**:
- `ValueError`: If lists have different lengths or moduli are invalid.

**Example**:
```python
ee = ExtendedEuclidean()
result = ee.chinese_remainder_theorem_general([1, 2, 3], [2, 3, 4])
# Returns: (11, 12)
```

---

##### `lcm(self, a: int, b: int) -> int`

Compute least common multiple.

**Parameters**:
- `a` (int): First integer.
- `b` (int): Second integer.

**Returns**:
- `int`: LCM of a and b.

**Example**:
```python
ee = ExtendedEuclidean()
lcm = ee.lcm(4, 6)
# Returns: 12
```

---

##### `lcm_list(self, numbers: List[int]) -> int`

Compute LCM of a list of numbers.

**Parameters**:
- `numbers` (List[int]): List of integers.

**Returns**:
- `int`: LCM of all numbers.

**Raises**:
- `ValueError`: If list is empty.

**Example**:
```python
ee = ExtendedEuclidean()
lcm = ee.lcm_list([4, 6, 8])
# Returns: 24
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_solve_two_congruences(self, r1: int, m1: int, r2: int, m2: int) -> Optional[Tuple[int, int]]`

Solve system of two congruences. Used internally by general CRT.

---

## Usage Examples

### Extended GCD

```python
from src.main import ExtendedEuclidean

ee = ExtendedEuclidean()
gcd, x, y = ee.extended_gcd(48, 18)
print(f"GCD: {gcd}, Coefficients: x={x}, y={y}")
# Output: GCD: 6, Coefficients: x=-1, y=3
```

### Modular Inverse

```python
ee = ExtendedEuclidean()
inv = ee.modular_inverse(3, 7)
print(f"Modular inverse: {inv}")  # 5
print(f"Verification: {(3 * inv) % 7}")  # 1
```

### Solving Congruences

```python
ee = ExtendedEuclidean()
solutions = ee.solve_congruence(3, 1, 7)
print(f"Solutions: {solutions}")  # [5]
```

### Chinese Remainder Theorem

```python
ee = ExtendedEuclidean()
result = ee.chinese_remainder_theorem([2, 3, 2], [3, 5, 7])
if result:
    x, M = result
    print(f"Solution: x ≡ {x} (mod {M})")
    # Output: Solution: x ≡ 23 (mod 105)
```

### LCM

```python
ee = ExtendedEuclidean()
lcm = ee.lcm(4, 6)
print(f"LCM: {lcm}")  # 12
```

---

## Performance Characteristics

- **Extended GCD**: O(log min(a, b))
- **Modular inverse**: O(log min(a, m))
- **CRT (standard)**: O(n × log M) where n is number of equations
- **CRT (general)**: O(n² × log M)
- **LCM**: O(log min(a, b))

---

## Notes

- All operations use efficient recursive algorithms
- Modular inverse exists only when gcd(a, m) = 1
- Standard CRT requires pairwise coprime moduli
- General CRT works with any moduli but may have no solution
- All results are verified mathematically
