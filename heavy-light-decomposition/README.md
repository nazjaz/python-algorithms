# Heavy-Light Decomposition for Efficient Path Queries and Updates on Trees

A Python implementation of heavy-light decomposition (HLD) that decomposes a tree into chains for efficient path queries and updates. HLD achieves O(log^2 n) time complexity for path operations using segment trees.

## Project Title and Description

The Heavy-Light Decomposition tool implements a tree decomposition technique that breaks a tree into chains such that any path from root to leaf contains at most O(log n) chains. Each chain is stored in a segment tree, enabling efficient range queries and updates on paths.

This tool solves the problem of efficiently querying and updating paths in trees, which is fundamental in many applications including competitive programming, tree-based algorithms, and graph problems. HLD provides O(log^2 n) time complexity for path operations.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced tree decomposition techniques.

## Features

- Heavy-light decomposition implementation
- O(log^2 n) time complexity for path queries and updates
- Segment tree support for chain operations
- Path query operations (sum, min, max, etc.)
- Path update operations (add, set, etc.)
- LCA and distance queries
- Subtree queries
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
cd /path/to/python-algorithms/heavy-light-decomposition
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
- `logging.file`: Path to log file (default: "logs/hld.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/hld.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of heavy-light decomposition:

```bash
python src/main.py
```

This will:
1. Build a tree from edges
2. Perform heavy-light decomposition
3. Execute path queries
4. Execute path updates
5. Show LCA and distance queries

### Programmatic Usage

```python
from src.main import (
    TreeNode,
    HeavyLightDecomposition,
    build_tree_from_edges,
)

# Build tree from edges
n = 7
edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
root = build_tree_from_edges(n, edges, 0)

# Create HLD
hld = HeavyLightDecomposition(root)

# Get nodes
node3 = root.children[0].children[0]
node5 = root.children[1].children[0]

# Path query
result = hld.query_path(node3, node5)
print(f"Path sum: {result}")

# Path update
hld.update_path(node3, node5, 10.0)

# LCA query
lca = hld.get_lca(node3, node5)
print(f"LCA: {lca.value}")

# Distance query
distance = hld.get_distance(node3, node5)
print(f"Distance: {distance}")
```

### Common Use Cases

**Tree Path Queries:**
1. Query sum/min/max along path
2. Update values along path
3. Efficient path operations

**Competitive Programming:**
1. Fast path queries for tree problems
2. Path updates in tree DP
3. Tree-based range queries

**Graph Algorithms:**
1. Tree decomposition
2. Path queries on trees
3. Tree-based graph problems

## Project Structure

```
heavy-light-decomposition/
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

- `src/main.py`: Contains `HeavyLightDecomposition`, `TreeNode`, and `SegmentTree` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Heavy-Light Decomposition

**Definition:**
Heavy-light decomposition decomposes a tree into chains such that:
1. Each path from root to leaf contains at most O(log n) chains
2. Each chain is a contiguous path in the tree
3. Heavy edges connect nodes in same chain
4. Light edges connect different chains

**Properties:**
1. O(log n) chains in any root-to-leaf path
2. Each chain stored in segment tree
3. O(log^2 n) time for path queries/updates
4. Efficient for tree path operations

**Structure:**
```
        Root
       /    \
    Chain1  Chain2
     /  \     /  \
   ...  ... ...  ...
```

Heavy edges form chains, light edges connect chains.

### Heavy Child Selection

**Algorithm:**
For each node, the heavy child is the child with largest subtree size. This ensures balanced chain lengths.

**Selection:**
- Compute subtree sizes using DFS
- For each node, choose child with max subtree size
- Heavy edges form chains

### Chain Construction

**Algorithm:**
1. Start DFS from root
2. Follow heavy edges to form chains
3. Light edges start new chains
4. Store chains in arrays
5. Build segment trees for each chain

### Segment Tree

**Purpose:**
Each chain is stored in a segment tree for efficient range queries and updates.

**Operations:**
- Range query: O(log n)
- Range update: O(log n)
- Lazy propagation for updates

### Path Query Algorithm

**Steps:**
1. Find LCA of two nodes
2. Query path from u to LCA:
   - While in different chain, query chain and move up
   - When in same chain, query range
3. Query path from v to LCA similarly
4. Combine results

**Time Complexity:** O(log^2 n)

### Path Update Algorithm

**Steps:**
1. Find LCA of two nodes
2. Update path from u to LCA:
   - While in different chain, update chain and move up
   - When in same chain, update range
3. Update path from v to LCA similarly
4. Update LCA node

**Time Complexity:** O(log^2 n)

### Operations

**Decomposition:**
- Time Complexity: O(n)
- Computes chains
- One-time preprocessing

**Path Query:**
- Time Complexity: O(log^2 n)
- Queries O(log n) chains, each O(log n)

**Path Update:**
- Time Complexity: O(log^2 n)
- Updates O(log n) chains, each O(log n)

**LCA:**
- Time Complexity: O(log n)
- Uses chain information

**Distance:**
- Time Complexity: O(log n)
- Uses depth and LCA

### Edge Cases Handled

- Empty tree
- Single node
- Linear tree (chain)
- Balanced tree
- Unbalanced tree
- Same node query
- Parent-child path
- Root node paths
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
- HLD creation and decomposition
- Path queries on various trees
- Path updates
- LCA and distance queries
- Subtree queries
- Edge cases (empty, single node, invalid inputs)
- Multiple operations

## Troubleshooting

### Common Issues

**Incorrect query results:**
- Verify tree structure is correct
- Check that nodes are in the tree
- Ensure decomposition completed successfully

**Performance issues:**
- HLD is O(log^2 n) per query
- For single query, naive O(n) might be faster
- HLD excels with multiple queries

**Memory issues:**
- HLD uses O(n log n) space
- Segment trees for each chain
- For very large trees, consider optimizations

### Error Messages

**"Invalid edge"**: Edge in build_tree_from_edges has invalid node indices.

**"Root value X not in nodes"**: Root value not found in node list.

### Best Practices

1. **Preprocess once** - Decomposition is expensive, reuse for multiple queries
2. **Use for multiple queries** - HLD excels with many path operations
3. **Validate inputs** - Ensure nodes are in tree before querying
4. **Monitor performance** - Track query times for your specific use case
5. **Consider alternatives** - For single query, naive approach might be faster

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Decomposition | O(n) |
| Path Query | O(log^2 n) |
| Path Update | O(log^2 n) |
| LCA | O(log n) |
| Distance | O(log n) |
| Subtree Query | O(log^2 n) |

Where n is the number of nodes in the tree.

### Space Complexity

- Tree structure: O(n)
- Chains: O(n)
- Segment trees: O(n log n)
- Total: O(n log n)

### Query Performance

- Path queries: O(log^2 n) - queries O(log n) chains
- Each chain query: O(log n) using segment tree
- Optimal for multiple path operations

## Applications

- **Competitive Programming**: Fast path queries for tree problems
- **Tree Algorithms**: Path queries and updates on trees
- **Graph Problems**: Tree-based graph algorithms
- **Dynamic Programming**: Tree DP with path operations
- **Network Algorithms**: Path queries in tree networks

## Comparison with Other Methods

**Naive Approach:**
- O(n) per query
- No preprocessing
- Simple implementation
- Inefficient for multiple queries

**Heavy-Light Decomposition:**
- O(log^2 n) per query
- O(n) preprocessing
- Good for path operations
- Efficient for multiple queries

**Euler Tour + Segment Tree:**
- O(log n) per query
- O(n log n) preprocessing
- Good for subtree queries
- Less efficient for path queries

**Link-Cut Trees:**
- O(log n) per query
- More complex
- Dynamic trees
- Overkill for static trees

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
