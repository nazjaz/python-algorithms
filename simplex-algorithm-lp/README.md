# Simplex Algorithm for Linear Programming

A Python implementation of the simplex algorithm for solving linear programming problems with pivot operations and tableau management.

## Project Title and Description

This project implements the simplex algorithm, a fundamental method for solving linear programming problems. The algorithm uses tableau representation, pivot operations, and iterative improvement to find optimal solutions to linear programming problems.

The simplex algorithm is widely used in operations research, optimization, economics, and engineering for solving resource allocation, scheduling, and planning problems.

**Target Audience**: Developers working with optimization, operations research, mathematical programming, and anyone needing to solve linear programming problems.

## Features

- Simplex algorithm implementation
- Tableau management and representation
- Pivot operations for basis changes
- Support for both maximization and minimization
- Optimality checking
- Unbounded problem detection
- Basic and non-basic variable tracking
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/simplex-algorithm-lp
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

#### Maximize Objective

```bash
python src/main.py --objective "3,2" --constraints "1,1;2,1" --rhs "4,6"
```

Output:
```
Objective: [3.0, 2.0]
Constraints: [[1.0, 1.0], [2.0, 1.0]]
RHS: [4.0, 6.0]
Mode: Maximize

Solution Status: optimal
Objective Value: 10.0000
Solution:
  x1 = 2.0000
  x2 = 2.0000
```

#### Minimize Objective

```bash
python src/main.py --objective "1,1" --constraints "1,0;0,1" --rhs "1,1" --minimize
```

#### Show Final Tableau

```bash
python src/main.py --objective "3,2" --constraints "1,1;2,1" --rhs "4,6" --tableau
```

### Programmatic Usage

```python
from src.main import SimplexAlgorithm, SolutionStatus

# Create linear programming problem
# Maximize 3x + 2y subject to:
# x + y <= 4
# 2x + y <= 6
# x >= 0, y >= 0

objective = [3, 2]
constraints = [[1, 1], [2, 1]]
rhs = [4, 6]

simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
status, solution, obj_value = simplex.solve()

print(f"Status: {status.value}")
print(f"Solution: {solution}")
print(f"Objective Value: {obj_value}")

# Get tableau
tableau = simplex.get_tableau()
print(f"Final Tableau: {tableau}")

# Get basic and non-basic variables
basic_vars = simplex.get_basic_variables()
non_basic_vars = simplex.get_non_basic_variables()
print(f"Basic Variables: {basic_vars}")
print(f"Non-Basic Variables: {non_basic_vars}")
```

### Common Use Cases

1. **Maximize objective**
   ```bash
   python src/main.py --objective "1,1" --constraints "1,0;0,1" --rhs "1,1"
   ```

2. **Minimize objective**
   ```bash
   python src/main.py --objective "1,1" --constraints "1,0;0,1" --rhs "1,1" --minimize
   ```

3. **View tableau**
   ```bash
   python src/main.py --objective "3,2" --constraints "1,1;2,1" --rhs "4,6" --tableau
   ```

## Project Structure

```
simplex-algorithm-lp/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main simplex algorithm implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `SimplexAlgorithm` class with all core functionality for solving linear programming problems.
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
pytest tests/test_main.py::TestSimplexAlgorithm::test_solve_simple_maximize
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Maximization and minimization problems
- Pivot operations
- Optimality checking
- Solution extraction
- Edge cases (unbounded, zero objective, etc.)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/simplex-algorithm-lp"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Algorithm doesn't converge

**Solution**: 
- Check that problem is in standard form (all constraints are <= with non-negative RHS)
- Ensure objective and constraints are correctly specified
- Try increasing max_iterations parameter
- Check for degenerate cases

**Issue**: Incorrect solution

**Solution**: 
- Verify problem formulation is correct
- Check that constraints are properly formatted
- Ensure RHS values are non-negative (for standard form)
- Verify objective function coefficients

### Error Messages

- **"Number of constraints must match number of RHS values"**: Each constraint needs a corresponding RHS value.
- **"Each constraint must have same number of coefficients as objective"**: All constraints must have same dimension as objective.
- **"Pivot element is zero"**: Degenerate case encountered (may need special handling).

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

### Simplex Algorithm

The simplex algorithm solves linear programming problems in standard form:

**Maximize**: cᵀx  
**Subject to**: Ax ≤ b, x ≥ 0

1. **Initial Tableau**: Create tableau with slack variables
2. **Find Entering Variable**: Choose variable with negative reduced cost (maximization) or positive (minimization)
3. **Find Leaving Variable**: Choose variable with minimum ratio (Bland's rule or minimum ratio test)
4. **Pivot**: Perform pivot operation to update tableau
5. **Check Optimality**: If all reduced costs are non-negative (max) or non-positive (min), solution is optimal
6. **Repeat**: Continue until optimal or unbounded

### Pivot Operation

The pivot operation:
1. Normalizes pivot row by dividing by pivot element
2. Eliminates pivot column in all other rows
3. Updates basic and non-basic variable sets
4. Maintains tableau structure

### Tableau Structure

The tableau has the form:
```
[A | I | b]
[--------]
[c | 0 | 0]
```

Where:
- A: Constraint coefficients
- I: Identity matrix (slack variables)
- b: Right-hand side values
- c: Objective function coefficients

### Time Complexity

- **Worst case**: Exponential (though rare in practice)
- **Average case**: O(m × n) per iteration where m is constraints, n is variables
- **Typical iterations**: O(m) to O(m + n)

### Space Complexity

- **Tableau**: O(m × (m + n)) where m is constraints, n is variables
- **Overall**: O(m × (m + n)) space

## Mathematical Background

### Linear Programming

A linear programming problem has:
- **Objective function**: Linear function to optimize
- **Constraints**: Linear inequalities or equations
- **Decision variables**: Non-negative variables

### Standard Form

Maximize: c₁x₁ + c₂x₂ + ... + cₙxₙ

Subject to:
- a₁₁x₁ + a₁₂x₂ + ... + a₁ₙxₙ ≤ b₁
- a₂₁x₁ + a₂₂x₂ + ... + a₂ₙxₙ ≤ b₂
- ...
- x₁, x₂, ..., xₙ ≥ 0

### Optimality Conditions

For maximization:
- All reduced costs (bottom row) are non-negative
- Current solution is feasible
- No improving direction exists

For minimization:
- All reduced costs are non-positive
- Current solution is feasible
- No improving direction exists

## Applications

- **Operations Research**: Resource allocation, production planning
- **Economics**: Cost minimization, profit maximization
- **Engineering**: Network flow, scheduling
- **Business**: Portfolio optimization, supply chain management
- **Transportation**: Route optimization, logistics

## Limitations

This implementation has some limitations:
- Assumes problem is in standard form (≤ constraints, non-negative RHS)
- Does not handle equality constraints directly (requires transformation)
- Does not implement two-phase method for finding initial feasible solution
- May need refinement for degenerate cases
- For production use with large problems, consider:
  - `scipy.optimize.linprog` for optimized implementation
  - Commercial solvers (CPLEX, Gurobi) for large-scale problems
  - More sophisticated pivot rules (Bland's rule, steepest edge)

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
