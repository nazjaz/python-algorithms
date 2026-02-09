# Simplex Algorithm API Documentation

## Classes

### SimplexAlgorithm

Main class for simplex algorithm implementation.

#### Methods

##### `__init__(self, objective: List[float], constraints: List[List[float]], rhs: List[float], maximize: bool = True) -> None`

Initialize simplex algorithm.

**Parameters**:
- `objective` (List[float]): Objective function coefficients (c).
- `constraints` (List[List[float]]): Constraint matrix (A).
- `rhs` (List[float]): Right-hand side values (b).
- `maximize` (bool): True to maximize, False to minimize. Default: True.

**Example**:
```python
objective = [3, 2]
constraints = [[1, 1], [2, 1]]
rhs = [4, 6]
simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
```

---

##### `solve(self, max_iterations: int = 1000) -> Tuple[SolutionStatus, Dict[str, float], float]`

Solve linear programming problem using simplex algorithm.

**Parameters**:
- `max_iterations` (int): Maximum number of iterations. Default: 1000.

**Returns**:
- `Tuple[SolutionStatus, Dict[str, float], float]`: Tuple (status, solution_dict, objective_value).

**Example**:
```python
status, solution, obj_value = simplex.solve()
# Returns: (SolutionStatus.OPTIMAL, {'x1': 2.0, 'x2': 2.0}, 10.0)
```

---

##### `get_tableau(self) -> List[List[float]]`

Get current tableau.

**Returns**:
- `List[List[float]]`: Current tableau matrix.

**Example**:
```python
tableau = simplex.get_tableau()
```

---

##### `get_basic_variables(self) -> List[int]`

Get list of basic variables.

**Returns**:
- `List[int]`: List of basic variable indices.

**Example**:
```python
basic_vars = simplex.get_basic_variables()
```

---

##### `get_non_basic_variables(self) -> List[int]`

Get list of non-basic variables.

**Returns**:
- `List[int]`: List of non-basic variable indices.

**Example**:
```python
non_basic_vars = simplex.get_non_basic_variables()
```

---

## Enums

### SolutionStatus

Status of linear programming solution.

**Values**:
- `OPTIMAL`: Optimal solution found
- `UNBOUNDED`: Problem is unbounded
- `INFEASIBLE`: Problem is infeasible
- `UNKNOWN`: Status unknown (may need more iterations)

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_create_tableau(self) -> None`

Create initial simplex tableau.

##### `_find_entering_variable(self) -> Optional[int]`

Find entering variable (pivot column).

##### `_find_leaving_variable(self, entering_col: int) -> Optional[int]`

Find leaving variable (pivot row).

##### `_pivot(self, pivot_row: int, pivot_col: int) -> None`

Perform pivot operation.

##### `_is_optimal(self) -> bool`

Check if current solution is optimal.

##### `_extract_solution(self) -> Tuple[SolutionStatus, Dict[str, float], float]`

Extract solution from tableau.

---

## Usage Examples

### Basic Usage

```python
from src.main import SimplexAlgorithm, SolutionStatus

objective = [3, 2]
constraints = [[1, 1], [2, 1]]
rhs = [4, 6]

simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
status, solution, obj_value = simplex.solve()

if status == SolutionStatus.OPTIMAL:
    print(f"Optimal solution: {solution}")
    print(f"Objective value: {obj_value}")
```

### Minimization

```python
simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=False)
status, solution, obj_value = simplex.solve()
```

### Access Tableau

```python
simplex = SimplexAlgorithm(objective, constraints, rhs)
simplex._create_tableau()
tableau = simplex.get_tableau()
print(f"Tableau: {tableau}")
```

### Check Variables

```python
simplex = SimplexAlgorithm(objective, constraints, rhs)
simplex.solve()
basic_vars = simplex.get_basic_variables()
non_basic_vars = simplex.get_non_basic_variables()
print(f"Basic: {basic_vars}, Non-basic: {non_basic_vars}")
```

---

## Performance Characteristics

- **Time Complexity**: O(m × n) per iteration where m is constraints, n is variables
- **Typical Iterations**: O(m) to O(m + n)
- **Worst Case**: Exponential (rare in practice)
- **Space Complexity**: O(m × (m + n)) for tableau

---

## Notes

- Problem must be in standard form (≤ constraints, non-negative RHS)
- Algorithm assumes initial feasible solution exists
- For problems without initial feasible solution, two-phase method may be needed
- Degenerate cases may require special handling
- All floating-point comparisons use tolerance (1e-9)
