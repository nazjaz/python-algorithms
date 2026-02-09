# Branch and Bound Algorithm for Integer Linear Programming

A Python implementation of the branch and bound algorithm for solving integer linear programming (ILP) and mixed-integer linear programming (MILP) problems.

## Project Title and Description

This project implements the branch and bound algorithm, a fundamental method for solving integer programming problems. The algorithm uses linear programming (LP) relaxation, tree search, branching on fractional variables, and bounding/pruning to find optimal integer solutions.

Branch and bound is widely used in operations research, combinatorial optimization, scheduling, and resource allocation problems where variables must take integer values.

**Target Audience**: Developers working with optimization, operations research, integer programming, and anyone needing to solve problems with integer constraints.

## Features

- Branch and bound algorithm implementation
- LP relaxation solving using simplex method
- Branching on fractional variables
- Bounding and pruning of search tree
- Support for both maximization and minimization
- Support for mixed-integer problems (some variables integer, some continuous)
- Depth-first search strategy
- Node exploration tracking
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/branch-and-bound-ilp
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Note: This project has no external dependencies for core functionality, but pytest is included for testing.

## Configuration

This project does not require configuration files or environment variables. All functionality is available through the command-line interface or by importing the classes directly.

## Usage

### Command-Line Interface

#### Solve Integer Programming Problem

```bash
python src/main.py --objective "1,1" --constraints "1,0;0,1" --rhs "1.5,1.5"
```

Output:
```
Objective: [1.0, 1.0]
Constraints: [[1.0, 0.0], [0.0, 1.0]]
RHS: [1.5, 1.5]
Mode: Maximize
Integer Variables: All

Solution Found:
  Objective Value: 2.0000
  Solution:
    x1 = 1
    x2 = 1
  Nodes Explored: 2
```

#### Minimize Objective

```bash
python src/main.py --objective "1,1" --constraints "1,0;0,1" --rhs "1.5,1.5" --minimize
```

#### Specify Integer Variables

```bash
python src/main.py --objective "1,1,1" --constraints "1,0,0;0,1,0" --rhs "1.5,1.5" --integer-vars "0,1"
```

#### Limit Node Exploration

```bash
python src/main.py --objective "1,1" --constraints "1,0;0,1" --rhs "1.5,1.5" --max-nodes 100
```

### Programmatic Usage

```python
from src.main import BranchAndBound

# Create integer programming problem
# Maximize x + y subject to:
# x <= 1.5
# y <= 1.5
# x, y integer

objective = [1, 1]
constraints = [[1, 0], [0, 1]]
rhs = [1.5, 1.5]

bb = BranchAndBound(objective, constraints, rhs, maximize=True)
solution, obj_value = bb.solve()

print(f"Solution: {solution}")
print(f"Objective Value: {obj_value}")
print(f"Nodes Explored: {bb.nodes_explored}")

# Mixed-integer problem
bb2 = BranchAndBound(
    [1, 1, 1],
    [[1, 0, 0], [0, 1, 0]],
    [1.5, 1.5],
    integer_vars=[0, 1]  # Only first two variables are integer
)
solution2, obj_value2 = bb2.solve()
```

### Common Use Cases

1. **Solve integer programming problem**
   ```bash
   python src/main.py --objective "3,2" --constraints "1,1;2,1" --rhs "4.5,6.5"
   ```

2. **Mixed-integer problem**
   ```bash
   python src/main.py --objective "1,1,1" --constraints "1,0,0;0,1,0" --rhs "1.5,1.5" --integer-vars "0"
   ```

## Project Structure

```
branch-and-bound-ilp/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main branch and bound implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `BranchAndBound` class with all core functionality for solving integer programming problems.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various problem types.
- **docs/API.md**: Detailed API documentation for all classes and methods.
- **logs/**: Directory for log files (if logging to files is enabled).

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestBranchAndBound::test_solve_with_branching
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- LP relaxation solving
- Branching logic
- Bounding and pruning
- Integer solution detection
- Mixed-integer problems
- Edge cases (infeasible, etc.)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/branch-and-bound-ilp"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Algorithm doesn't find solution

**Solution**: 
- Check that problem is feasible
- Increase max_nodes parameter
- Verify constraints are correctly specified
- Check for numerical issues

**Issue**: Too many nodes explored

**Solution**: 
- Problem may be large or difficult
- Consider using better branching strategies
- For production use, consider commercial solvers
- Try different variable ordering

### Error Messages

- **"Number of constraints must match number of RHS values"**: Each constraint needs a corresponding RHS value.
- **"Each constraint must have same number of coefficients as objective"**: All constraints must have same dimension as objective.

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```
4. Create a feature branch: `git checkout -b feature/your-feature-name`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Run tests before committing

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Write clear commit messages following conventional commit format
4. Submit pull request with description of changes

## Algorithm Details

### Branch and Bound Algorithm

The branch and bound algorithm solves integer programming problems by:

1. **LP Relaxation**: Solve linear programming relaxation (ignore integer constraints)
2. **Check Integer**: If solution is integer, we're done
3. **Branch**: Choose fractional variable, create two subproblems:
   - One with variable ≤ floor(value)
   - One with variable ≥ ceil(value)
4. **Bound**: Use LP relaxation value as bound
5. **Prune**: Discard nodes that can't improve best solution
6. **Repeat**: Continue until all nodes explored or pruned

### Branching Strategy

- **Variable Selection**: Choose first fractional variable (can be improved with better heuristics)
- **Value Selection**: Branch on floor and ceiling of fractional value
- **Search Strategy**: Depth-first search (can be changed to best-first)

### Bounding and Pruning

- **Upper Bound (Maximization)**: LP relaxation value
- **Lower Bound (Maximization)**: Best integer solution found
- **Pruning**: If LP bound < best integer solution, prune node

### Time Complexity

- **Worst case**: Exponential (2^n where n is number of integer variables)
- **Average case**: Depends on problem structure
- **Space complexity**: O(n) for search tree (depth-first)

### Space Complexity

- **Search tree**: O(depth) for depth-first search
- **Tableau storage**: O(m × (m + n)) per node
- **Overall**: Depends on search strategy

## Mathematical Background

### Integer Linear Programming

An integer linear programming problem has:
- **Objective function**: Linear function to optimize
- **Constraints**: Linear inequalities
- **Decision variables**: Some or all variables must be integer

### LP Relaxation

The LP relaxation removes integer constraints:
- If all variables are continuous, solve with simplex
- Optimal value provides bound for integer problem
- If LP solution is integer, it's optimal for ILP

### Branching

When LP solution has fractional variable x = k.f (k integer, 0 < f < 1):
- Create two subproblems:
  - x ≤ k (left branch)
  - x ≥ k + 1 (right branch)
- Each subproblem is solved recursively

### Pruning

A node can be pruned if:
- **Bound pruning**: LP bound worse than best integer solution
- **Infeasibility**: LP relaxation is infeasible
- **Optimality**: LP solution is integer

## Applications

- **Operations Research**: Production planning, scheduling
- **Combinatorial Optimization**: Knapsack, set covering
- **Network Design**: Facility location, routing
- **Resource Allocation**: Budget allocation, capacity planning
- **Scheduling**: Job scheduling, project management

## Limitations

This implementation has some limitations:
- Uses simple branching strategy (first fractional variable)
- Depth-first search (may explore many nodes)
- No advanced cutting planes
- For production use with large problems, consider:
  - Commercial solvers (CPLEX, Gurobi, XPRESS)
  - Better branching heuristics (strong branching, pseudo-costs)
  - Cutting plane methods (Gomory cuts)
  - Preprocessing techniques

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
