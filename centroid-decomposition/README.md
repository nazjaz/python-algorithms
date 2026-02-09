# Centroid Decomposition for Solving Tree Problems with Divide and Conquer

A Python implementation of centroid decomposition that decomposes a tree into a centroid tree for efficient divide and conquer solutions to tree problems. Centroid decomposition achieves O(n log n) time complexity for many tree problems.

## Project Title and Description

The Centroid Decomposition tool implements a tree decomposition technique that recursively finds centroids (nodes whose removal splits the tree into subtrees of size at most n/2) and builds a centroid tree. This enables efficient divide and conquer solutions to many tree problems.

This tool solves the problem of efficiently solving tree problems using divide and conquer, which is fundamental in many applications including competitive programming, tree-based algorithms, and graph problems. Centroid decomposition provides O(n log n) time complexity for many tree problems.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced tree decomposition techniques and divide and conquer algorithms.

## Features

- Centroid decomposition implementation
- O(n log n) time complexity for decomposition
- Divide and conquer problem solving framework
- Path counting with conditions
- Custom problem solver support
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
cd /path/to/python-algorithms/centroid-decomposition
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
- `logging.file`: Path to log file (default: "logs/centroid_decomposition.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/centroid_decomposition.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of centroid decomposition:

```bash
python src/main.py
```

This will:
1. Build a tree from edges
2. Perform centroid decomposition
3. Count paths with conditions
4. Demonstrate divide and conquer solving

### Programmatic Usage

```python
from src.main import (
    TreeNode,
    CentroidDecomposition,
    build_tree_from_edges,
)

# Build tree from edges
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)

# Create centroid decomposition
cd = CentroidDecomposition(root)
cd.decompose()

# Count paths with condition
count = cd.count_paths_with_condition(lambda d: d <= 2)
print(f"Paths with distance <= 2: {count}")

# Custom problem solver
def problem_solver(centroid, distances):
    return sum(1 for _, d in distances if d % 2 == 0)

result = cd.solve_with_divide_conquer(problem_solver)
print(f"Problem result: {result}")
```

### Common Use Cases

**Tree Path Problems:**
1. Count paths satisfying conditions
2. Find paths with specific properties
3. Solve tree-based optimization problems

**Competitive Programming:**
1. Fast solutions to tree problems
2. Divide and conquer on trees
3. Tree-based dynamic programming

**Graph Algorithms:**
1. Tree decomposition
2. Path queries on trees
3. Tree-based graph problems

## Project Structure

```
centroid-decomposition/
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

- `src/main.py`: Contains `CentroidDecomposition` and `TreeNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Centroid Decomposition

**Definition:**
Centroid decomposition recursively finds centroids (nodes whose removal splits the tree into subtrees of size at most n/2) and builds a centroid tree. The centroid tree has height O(log n), enabling efficient divide and conquer.

**Properties:**
1. O(log n) height of centroid tree
2. Each node appears in O(log n) centroids
3. O(n log n) total decomposition time
4. Efficient for divide and conquer

**Structure:**
```
        Centroid1
       /    |    \
   Comp1  Comp2  Comp3
    |      |      |
Centroid2 Centroid3 ...
```

### Centroid Finding

**Algorithm:**
1. Compute subtree sizes using DFS
2. Find node where all subtrees have size <= n/2
3. Such a node always exists and is unique (for tree)

**Selection:**
- Start from arbitrary root
- Move to child with largest subtree if > n/2
- Stop when all subtrees <= n/2

### Decomposition Process

**Steps:**
1. Find centroid of current component
2. Remove centroid, splitting into components
3. Recursively decompose each component
4. Build centroid tree with parent-child relationships

**Time Complexity:** O(n log n)

### Divide and Conquer Framework

**Approach:**
1. For each centroid:
   - Compute distances to all nodes in component
   - Solve problem for this centroid
   - Recursively solve for child centroids
2. Combine results

**Benefits:**
- Each node processed O(log n) times
- Total time: O(n log n)
- Flexible problem-solving framework

### Operations

**Decomposition:**
- Time Complexity: O(n log n)
- Builds centroid tree
- One-time preprocessing

**Problem Solving:**
- Time Complexity: O(n log n)
- Depends on problem-specific operations
- Uses divide and conquer framework

**Path Counting:**
- Time Complexity: O(n log n)
- Counts paths satisfying condition
- Uses divide and conquer

### Edge Cases Handled

- Empty tree
- Single node
- Linear tree (chain)
- Balanced tree
- Unbalanced tree
- Invalid nodes
- Multiple decompositions

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
- TreeNode creation and operations
- Centroid decomposition on various trees
- Path counting with conditions
- Custom problem solving
- Edge cases (empty, single node, invalid inputs)
- Error handling

## Troubleshooting

### Common Issues

**Incorrect decomposition:**
- Verify tree structure is correct
- Check that tree is connected
- Ensure decomposition completed successfully

**Performance issues:**
- Centroid decomposition is O(n log n)
- For single query, naive O(n) might be faster
- Centroid decomposition excels with multiple operations

**Memory issues:**
- Centroid decomposition uses O(n) space
- For very large trees, consider optimizations
- Monitor memory usage

### Error Messages

**"Tree must be decomposed first"**: Attempted to solve problem before decomposition.

**"Invalid edge"**: Edge in build_tree_from_edges has invalid node indices.

**"Root value X not in nodes"**: Root value not found in node list.

### Best Practices

1. **Decompose once** - Decomposition is expensive, reuse for multiple queries
2. **Use for multiple queries** - Centroid decomposition excels with many operations
3. **Validate inputs** - Ensure tree is valid before decomposition
4. **Monitor performance** - Track operation times for your specific use case
5. **Consider alternatives** - For single query, naive approach might be faster

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Decomposition | O(n log n) |
| Problem Solving | O(n log n) |
| Path Counting | O(n log n) |

Where n is the number of nodes in the tree.

### Space Complexity

- Tree structure: O(n)
- Centroid tree: O(n)
- Subtree sizes: O(n)
- Total: O(n)

### Query Performance

- Problem solving: O(n log n) - each node processed O(log n) times
- Path counting: O(n log n) - depends on condition complexity
- Optimal for divide and conquer problems

## Applications

- **Competitive Programming**: Fast solutions to tree problems
- **Tree Algorithms**: Divide and conquer on trees
- **Graph Problems**: Tree-based graph algorithms
- **Path Problems**: Counting paths with conditions
- **Optimization**: Tree-based optimization problems

## Comparison with Other Methods

**Naive Approach:**
- O(n^2) for many problems
- Simple implementation
- Inefficient for large trees

**Centroid Decomposition:**
- O(n log n) for many problems
- O(n log n) preprocessing
- Good for divide and conquer
- Efficient for multiple queries

**Heavy-Light Decomposition:**
- O(log^2 n) per query
- O(n) preprocessing
- Good for path queries
- Less flexible

**Euler Tour:**
- O(log n) per query
- O(n log n) preprocessing
- Good for subtree queries
- Less efficient for path problems

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
