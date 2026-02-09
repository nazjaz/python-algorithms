# Hungarian Algorithm for Solving Assignment Problem

A Python implementation of the Hungarian algorithm (Kuhn-Munkres algorithm) for solving the assignment problem in bipartite graphs. This tool finds the minimum cost assignment of workers to jobs given a cost matrix.

## Project Title and Description

The Hungarian Algorithm tool implements the Hungarian algorithm to solve the assignment problem efficiently. The assignment problem finds the minimum cost one-to-one assignment between two sets (e.g., workers and jobs) given a cost matrix where each entry represents the cost of assigning an element from the first set to an element from the second set.

This tool solves the assignment problem optimally in polynomial time, with applications in resource allocation, job scheduling, task assignment, and bipartite matching problems. The algorithm guarantees finding the optimal solution.

**Target Audience**: Operations researchers, algorithm students, competitive programmers, resource allocation engineers, optimization researchers, and anyone interested in understanding the Hungarian algorithm and assignment problems.

## Features

- Hungarian algorithm implementation (Kuhn-Munkres algorithm)
- Minimum cost assignment computation
- Maximum value assignment (maximization variant)
- Bipartite graph representation
- Cost matrix to bipartite graph conversion
- Assignment validation
- Comprehensive edge case handling
- Detailed step-by-step logging
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/hungarian-algorithm
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python src/main.py
```

## Configuration

### Configuration File (config.yaml)

The tool uses a YAML configuration file to define logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/app.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of the Hungarian algorithm:

```bash
python src/main.py
```

This will:
1. Create a cost matrix
2. Solve the assignment problem
3. Display optimal assignments and total cost
4. Solve maximization variant
5. Demonstrate bipartite graph usage

### Programmatic Usage

```python
from src.main import HungarianAlgorithm, BipartiteGraph

# Create cost matrix
cost_matrix = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4],
]

# Solve assignment problem
algorithm = HungarianAlgorithm(cost_matrix)
min_cost, assignments = algorithm.solve()

print(f"Minimum cost: {min_cost}")
for worker, job in assignments:
    cost = algorithm.get_assignment_cost(worker, job)
    print(f"Worker {worker} -> Job {job} (cost: {cost})")

# Solve maximization problem
max_value, max_assignments = algorithm.solve_maximization()
print(f"Maximum value: {max_value}")

# Using bipartite graph
graph = BipartiteGraph(4, 4)
for i in range(4):
    for j in range(4):
        graph.add_edge(i, j, cost_matrix[i][j])

graph_cost, graph_assignments = graph.solve_assignment()
```

### Common Use Cases

**Job Assignment:**
1. Create cost matrix with worker-job costs
2. Solve for minimum cost assignment
3. Assign workers to jobs optimally

**Resource Allocation:**
1. Model resources and tasks as bipartite graph
2. Set edge weights to allocation costs
3. Find optimal resource-task matching

**Task Scheduling:**
1. Create cost matrix for task assignments
2. Solve for optimal schedule
3. Minimize total completion cost

## Project Structure

```
hungarian-algorithm/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py           # Main application code
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains `HungarianAlgorithm` and `BipartiteGraph` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Assignment Problem

**Definition:**
Given a cost matrix C where C[i][j] represents the cost of assigning worker i to job j, find the one-to-one assignment that minimizes the total cost.

**Properties:**
1. One-to-one mapping: Each worker assigned to exactly one job
2. Each job assigned to exactly one worker
3. Optimal solution guaranteed by Hungarian algorithm

### Hungarian Algorithm (Kuhn-Munkres)

**Overview:**
The Hungarian algorithm solves the assignment problem in polynomial time using matrix operations and zero covering.

**Steps:**

1. **Row Reduction**: Subtract minimum from each row
   - Creates at least one zero per row
   - Preserves optimal solution

2. **Column Reduction**: Subtract minimum from each column
   - Creates at least one zero per column
   - Preserves optimal solution

3. **Zero Covering**: Cover all zeros with minimum lines
   - Use greedy approach to cover zeros
   - If n lines needed, optimal assignment found

4. **Matrix Adjustment**: If not optimal
   - Find minimum uncovered value
   - Subtract from uncovered elements
   - Add to doubly-covered elements
   - Repeat from step 3

5. **Assignment**: Find optimal assignment from zeros
   - Match zeros to form complete assignment
   - Use greedy matching with DFS backup

**Time Complexity:** O(n^3) where n is matrix size

**Space Complexity:** O(n^2) for matrix storage

**Advantages:**
- Guaranteed optimal solution
- Polynomial time complexity
- Works for both minimization and maximization

### Operations

**Solve:**
- Time Complexity: O(n^3)
- Space Complexity: O(n^2)
- Returns minimum cost and assignments

**Solve Maximization:**
- Time Complexity: O(n^3)
- Converts maximization to minimization
- Returns maximum value and assignments

**Assignment Validation:**
- Time Complexity: O(n)
- Verifies one-to-one mapping

### Edge Cases Handled

- Empty matrix (rejected)
- Non-square matrix (rejected)
- All zero costs
- All same costs
- Large matrices
- Sparse cost matrices
- Invalid vertex indices

## Testing

### Run Tests

```bash
python -m pytest tests/
```

### Run Tests with Coverage

```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite aims for minimum 80% code coverage, testing:
- Hungarian algorithm initialization
- Assignment problem solving
- Maximization problem solving
- Bipartite graph operations
- Assignment validation
- Edge cases (empty, non-square, all zeros)
- Invalid input handling

## Troubleshooting

### Common Issues

**No assignment found:**
- Verify matrix is square
- Check that algorithm completes all steps
- Ensure zeros exist after reduction

**Incorrect cost:**
- Verify original matrix is correct
- Check assignment calculation
- Ensure all assignments are valid

**Algorithm doesn't terminate:**
- This should not happen with correct implementation
- Check zero covering logic
- Verify matrix adjustment

### Error Messages

**"Cost matrix cannot be empty"**: Matrix must have at least one row and column.

**"Cost matrix must be square"**: Matrix must be n x n for n workers and n jobs.

**"Invalid worker/job index"**: Index is out of bounds for matrix size.

### Best Practices

1. **Use square matrices** - Algorithm requires n x n matrices
2. **Check assignments** - Validate one-to-one mapping
3. **Handle large matrices** - O(n^3) complexity for large n
4. **Use maximization variant** - For profit/reward maximization
5. **Validate input** - Ensure matrix is properly formatted

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Solve | O(n^3) |
| Solve Maximization | O(n^3) |
| Assignment Validation | O(n) |
| Get Assignment Cost | O(1) |

Where n is the size of the cost matrix (n x n).

### Space Complexity

- Matrix storage: O(n^2)
- Auxiliary space: O(n^2)
- Total: O(n^2)

## Applications

- **Job Assignment**: Assign workers to jobs optimally
- **Resource Allocation**: Allocate resources to tasks
- **Task Scheduling**: Schedule tasks to machines
- **Bipartite Matching**: Find optimal matching in bipartite graphs
- **Transportation**: Assign vehicles to routes
- **Project Management**: Assign team members to projects

## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes following PEP 8 style guidelines
4. Add tests for new functionality
5. Ensure all tests pass: `pytest tests/`
6. Submit a pull request

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Include docstrings for all public functions and classes
- Use meaningful variable names
- Write tests for all new functionality

### Pull Request Process

1. Ensure code follows project standards
2. Update documentation if needed
3. Add/update tests
4. Ensure all tests pass
5. Submit PR with clear description of changes

## License

This project is part of the python-algorithms collection. Please refer to the parent repository for license information.
