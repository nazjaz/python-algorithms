# LCA (Lowest Common Ancestor) Algorithms using Binary Lifting and Euler Tour

A Python implementation of LCA (Lowest Common Ancestor) algorithms using two different techniques: binary lifting and Euler tour. Both algorithms achieve O(log n) query time complexity with different preprocessing approaches.

## Project Title and Description

The LCA Algorithms tool implements two efficient algorithms for finding the lowest common ancestor of two nodes in a tree: binary lifting and Euler tour. Both techniques preprocess the tree to enable fast LCA queries, making them essential for solving many tree-based problems efficiently.

This tool solves the problem of efficiently finding the lowest common ancestor in trees, which is fundamental in many applications including competitive programming, graph algorithms, and tree-based data structures. Both algorithms provide O(log n) query time complexity with different trade-offs.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced tree algorithms and optimization techniques.

## Features

- Binary lifting LCA implementation with O(log n) queries
- Euler tour LCA implementation with O(log n) queries
- O(n log n) preprocessing for both algorithms
- Support for arbitrary tree structures
- Tree building from edge lists
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
cd /path/to/python-algorithms/lca-algorithms
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
- `logging.file`: Path to log file (default: "logs/lca.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/lca.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of LCA algorithms:

```bash
python src/main.py
```

This will:
1. Build a tree from edges
2. Demonstrate binary lifting LCA
3. Demonstrate Euler tour LCA
4. Show results for various queries

### Programmatic Usage

```python
from src.main import (
    TreeNode,
    LCABinaryLifting,
    LCAEulerTour,
    build_tree_from_edges,
)

# Build tree from edges
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)

# Binary lifting LCA
lca_bl = LCABinaryLifting(root)
node3 = root.children[0].children[0]
node4 = root.children[0].children[1]
result = lca_bl.lca(node3, node4)
print(f"LCA: {result.value}")

# Euler tour LCA
lca_et = LCAEulerTour(root)
result = lca_et.lca(node3, node4)
print(f"LCA: {result.value}")
```

### Common Use Cases

**Tree Queries:**
1. Find LCA of two nodes
2. Calculate distance between nodes
3. Check if one node is ancestor of another
4. Solve tree-based problems efficiently

**Competitive Programming:**
1. Fast LCA queries for tree problems
2. Path queries on trees
3. Tree-based dynamic programming

**Graph Algorithms:**
1. Tree decomposition
2. Lowest common ancestor in DAGs
3. Tree-based graph algorithms

## Project Structure

```
lca-algorithms/
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

- `src/main.py`: Contains `LCABinaryLifting`, `LCAEulerTour`, `TreeNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Binary Lifting

**Definition:**
Binary lifting preprocesses the tree by storing the 2^i-th ancestor of each node for all i. This allows jumping up the tree in powers of 2, enabling O(log n) LCA queries.

**Preprocessing:**
1. Compute depth of each node using DFS
2. Build parent table: parent[node][0] = direct parent
3. For each level i, compute 2^i-th ancestor: parent[node][i] = parent[parent[node][i-1]][i-1]

**Query Algorithm:**
1. Lift deeper node to same depth as shallower node
2. If nodes are same, return that node
3. Lift both nodes up simultaneously until their parents are same
4. Return the common parent

**Time Complexity:**
- Preprocessing: O(n log n)
- Query: O(log n)
- Space: O(n log n)

**Advantages:**
- Simple to understand
- Good for multiple queries
- Can answer other queries (k-th ancestor, distance)

### Euler Tour

**Definition:**
Euler tour technique converts the tree into a sequence by visiting each node when entering and leaving. The LCA of two nodes is the node with minimum depth between their first occurrences in the Euler tour.

**Preprocessing:**
1. Perform Euler tour DFS, recording node values and depths
2. Record first occurrence of each node
3. Build sparse table for range minimum query (RMQ) on depth array

**Query Algorithm:**
1. Find first occurrences of both nodes in Euler tour
2. Query RMQ on depth array between these positions
3. Return node at position with minimum depth

**Time Complexity:**
- Preprocessing: O(n log n)
- Query: O(log n)
- Space: O(n log n)

**Advantages:**
- Can answer range queries on tree
- Useful for subtree queries
- Can be extended for other tree problems

### Comparison

**Binary Lifting:**
- Simpler implementation
- Better for k-th ancestor queries
- More intuitive
- Slightly more memory per node

**Euler Tour:**
- Better for range queries
- Useful for subtree operations
- Can be extended for more queries
- More complex implementation

### Operations

**Preprocessing:**
- Time Complexity: O(n log n) for both
- Builds data structures for fast queries
- One-time cost for multiple queries

**Query:**
- Time Complexity: O(log n) for both
- Finds LCA of two nodes
- Both algorithms give same result

### Edge Cases Handled

- Empty tree
- Single node
- Linear tree (chain)
- Balanced tree
- Unbalanced tree
- Same node query
- Parent-child query
- Root node queries
- Invalid nodes

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
- Binary lifting LCA on various trees
- Euler tour LCA on various trees
- Tree building from edges
- Edge cases (empty, single node, invalid inputs)
- Comparison of both algorithms
- Large trees

## Troubleshooting

### Common Issues

**Incorrect LCA results:**
- Verify tree structure is correct
- Check that nodes are in the tree
- Ensure preprocessing completed successfully

**Performance issues:**
- Both algorithms are O(log n) per query
- Preprocessing is O(n log n) one-time cost
- For single query, naive O(n) might be faster

**Memory issues:**
- Both algorithms use O(n log n) space
- For very large trees, consider optimizations
- Binary lifting uses slightly more memory

### Error Messages

**"One or both nodes not in tree"**: Attempted to query LCA with nodes not in tree.

**"Invalid edge"**: Edge in build_tree_from_edges has invalid node indices.

**"Root value X not in nodes"**: Root value not found in node list.

### Best Practices

1. **Preprocess once** - Preprocessing is expensive, reuse for multiple queries
2. **Choose algorithm** - Binary lifting for simplicity, Euler tour for range queries
3. **Validate inputs** - Ensure nodes are in tree before querying
4. **Consider use case** - Both algorithms have same complexity, choose based on needs
5. **Monitor performance** - Track query times for your specific use case

## Performance Characteristics

### Time Complexity

| Operation | Binary Lifting | Euler Tour |
|-----------|----------------|------------|
| Preprocessing | O(n log n) | O(n log n) |
| Query | O(log n) | O(log n) |
| Space | O(n log n) | O(n log n) |

Where n is the number of nodes in the tree.

### Space Complexity

- Binary Lifting: O(n log n) for parent table
- Euler Tour: O(n log n) for sparse table
- Both: O(n) for tree structure

### Query Performance

- Both algorithms: O(log n) per query
- Independent of tree structure
- Optimal for multiple queries

## Applications

- **Competitive Programming**: Fast LCA queries for tree problems
- **Graph Algorithms**: Tree-based graph algorithms
- **Distance Calculation**: Calculate distance between nodes
- **Tree Queries**: Answer various tree-based queries
- **Dynamic Programming**: Tree DP with LCA
- **Lowest Common Ancestor Problems**: Direct LCA queries

## Comparison with Other Methods

**Naive Approach:**
- O(n) per query
- No preprocessing
- Simple implementation
- Inefficient for multiple queries

**Binary Lifting:**
- O(log n) per query
- O(n log n) preprocessing
- Good for k-th ancestor
- Simple to understand

**Euler Tour:**
- O(log n) per query
- O(n log n) preprocessing
- Good for range queries
- More versatile

**Tarjan's Offline:**
- O(n + q) for q queries
- Requires all queries upfront
- More complex
- Best for offline queries

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
