# Branch and Bound API Documentation

## Classes

### BranchAndBound

Main class for branch and bound algorithm implementation.

#### Methods

##### `__init__(self, objective: List[float], constraints: List[List[float]], rhs: List[float], maximize: bool = True, integer_vars: Optional[List[int]] = None) -> None`

Initialize branch and bound algorithm.

**Parameters**:
- `objective` (List[float]): Objective function coefficients.
- `constraints` (List[List[float]]): Constraint matrix.
- `rhs` (List[float]): Right-hand side values.
- `maximize` (bool): True to maximize, False to minimize. Default: True.
- `integer_vars` (Optional[List[int]]): List of variable indices that must be integer. If None, all variables are integer.

**Example**:
```python
objective = [1, 1]
constraints = [[1, 0], [0, 1]]
rhs = [1.5, 1.5]
bb = BranchAndBound(objective, constraints, rhs, maximize=True)
```

---

##### `solve(self, max_nodes: int = 10000) -> Tuple[Optional[Dict[int, float]], float]`

Solve integer linear programming problem using branch and bound.

**Parameters**:
- `max_nodes` (int): Maximum number of nodes to explore. Default: 10000.

**Returns**:
- `Tuple[Optional[Dict[int, float]], float]`: Tuple (solution, objective_value).

**Example**:
```python
solution, obj_value = bb.solve()
# Returns: ({0: 1.0, 1: 1.0}, 2.0)
```

---

## Data Classes

### BBNode

Branch and bound node data structure.

**Attributes**:
- `lower_bounds` (List[Optional[float]]): Lower bounds for each variable.
- `upper_bounds` (List[Optional[float]]): Upper bounds for each variable.
- `lp_solution` (Optional[Dict[int, float]]): LP relaxation solution.
- `lp_objective` (float): LP relaxation objective value.
- `status` (NodeStatus): Node status.
- `depth` (int): Depth in search tree.

---

## Enums

### NodeStatus

Status of branch and bound node.

**Values**:
- `OPEN`: Node is open for exploration
- `PRUNED`: Node has been pruned
- `SOLVED`: Node contains integer solution
- `INFEASIBLE`: Node is infeasible

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_solve_lp_relaxation(self, lower_bounds: List[Optional[float]], upper_bounds: List[Optional[float]]) -> Tuple[Optional[Dict[int, float]], float, bool]`

Solve LP relaxation with bounds.

##### `_simple_simplex(self, objective: List[float], constraints: List[List[float]], rhs: List[float], maximize: bool) -> Tuple[Optional[Dict[int, float]], float]`

Simple simplex solver for LP relaxation.

##### `_is_integer_solution(self, solution: Dict[int, float]) -> bool`

Check if solution is integer for integer variables.

##### `_round_solution(self, solution: Dict[int, float]) -> Dict[int, float]`

Round solution to integers.

##### `_find_branching_variable(self, solution: Dict[int, float]) -> Optional[int]`

Find variable to branch on.

##### `_should_prune(self, lp_objective: float) -> bool`

Check if node should be pruned.

##### `_update_best_solution(self, solution: Dict[int, float], objective: float) -> None`

Update best solution if better.

---

## Usage Examples

### Basic Usage

```python
from src.main import BranchAndBound

objective = [1, 1]
constraints = [[1, 0], [0, 1]]
rhs = [1.5, 1.5]

bb = BranchAndBound(objective, constraints, rhs, maximize=True)
solution, obj_value = bb.solve()

if solution:
    print(f"Solution: {solution}")
    print(f"Objective: {obj_value}")
    print(f"Nodes explored: {bb.nodes_explored}")
```

### Mixed-Integer Problem

```python
bb = BranchAndBound(
    [1, 1, 1],
    [[1, 0, 0], [0, 1, 0]],
    [1.5, 1.5],
    integer_vars=[0, 1]  # Only first two are integer
)
solution, obj_value = bb.solve()
```

### Minimization

```python
bb = BranchAndBound(objective, constraints, rhs, maximize=False)
solution, obj_value = bb.solve()
```

---

## Performance Characteristics

- **Time Complexity**: Exponential in worst case (2^n where n is number of integer variables)
- **Space Complexity**: O(depth) for depth-first search
- **Typical Performance**: Depends heavily on problem structure
- **Node Exploration**: Can be controlled with max_nodes parameter

---

## Notes

- Algorithm uses depth-first search strategy
- Simple branching heuristic (first fractional variable)
- LP relaxation solved using simplex method
- For large problems, consider commercial solvers
- All floating-point comparisons use tolerance (1e-6, 1e-9)
