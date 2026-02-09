# Link-Cut Tree (Dynamic Tree) for Maintaining Forests with Link and Cut Operations

A Python implementation of link-cut tree data structure that maintains a forest of trees and supports efficient link, cut, and path operations. Link-cut trees achieve O(log n) amortized time complexity for all operations using splay trees.

## Project Title and Description

The Link-Cut Tree tool implements a dynamic tree data structure that maintains a forest of trees and supports efficient link (add edge), cut (remove edge), and path operations. Link-cut trees use splay trees internally to achieve O(log n) amortized time complexity for all operations.

This tool solves the problem of efficiently maintaining dynamic forests and performing operations on paths, which is fundamental in many applications including competitive programming, graph algorithms, and network flow problems. Link-cut trees provide O(log n) amortized time complexity for link, cut, and path operations.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced dynamic tree data structures.

## Features

- Link-cut tree implementation with splay tree operations
- O(log n) amortized time complexity for all operations
- Link operation to add edges between trees
- Cut operation to remove edges
- Find root operation
- Path queries and updates
- Connectivity checking
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
cd /path/to/python-algorithms/link-cut-tree
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
- `logging.file`: Path to log file (default: "logs/link_cut_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/link_cut_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of link-cut tree operations:

```bash
python src/main.py
```

This will:
1. Create nodes
2. Link nodes to form trees
3. Perform find root operations
4. Check connectivity
5. Perform path queries
6. Cut edges

### Programmatic Usage

```python
from src.main import LinkCutTree

# Create link-cut tree
tree = LinkCutTree()

# Create nodes
node0 = tree.create_node(0, data=1.0)
node1 = tree.create_node(1, data=2.0)
node2 = tree.create_node(2, data=3.0)

# Link nodes
tree.link(node1, node0)
tree.link(node2, node0)

# Find root
root = tree.find_root(node1)
print(f"Root: {root.value}")

# Check connectivity
connected = tree.are_connected(node1, node2)
print(f"Connected: {connected}")

# Path query
result = tree.path_query(node1, node2)
print(f"Path sum: {result}")

# Path update
tree.path_update(node1, node2, 10.0)

# Cut edge
tree.cut(node1)
```

### Common Use Cases

**Dynamic Forest Maintenance:**
1. Maintain multiple trees
2. Add edges with link
3. Remove edges with cut
4. Query connectivity

**Path Operations:**
1. Query paths between nodes
2. Update paths efficiently
3. Find paths in dynamic trees

**Competitive Programming:**
1. Fast dynamic tree operations
2. Path queries and updates
3. Connectivity queries

## Project Structure

```
link-cut-tree/
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

- `src/main.py`: Contains `LinkCutTree` and `LinkCutNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Link-Cut Tree

**Definition:**
A link-cut tree maintains a forest of trees and supports efficient link, cut, and path operations. It uses splay trees internally to represent preferred paths, achieving O(log n) amortized time complexity.

**Properties:**
1. Maintains forest of trees
2. O(log n) amortized operations
3. Uses splay trees for preferred paths
4. Efficient path queries and updates

**Structure:**
- Each tree decomposed into preferred paths
- Each path stored in splay tree
- Path-parent pointers connect paths
- Access operation exposes paths

### Splay Tree Operations

**Splay:**
- Moves node to root of its splay tree
- Uses rotations (zig, zig-zig, zig-zag)
- Amortized O(log n) time

**Access:**
- Makes node root of its auxiliary tree
- Exposes path from node to root
- O(log n) amortized time

### Operations

**Link:**
- Time Complexity: O(log n) amortized
- Links two trees by making child a child of parent
- Requires nodes in different trees

**Cut:**
- Time Complexity: O(log n) amortized
- Removes edge from node to parent
- Splits tree into two trees

**Find Root:**
- Time Complexity: O(log n) amortized
- Finds root of tree containing node
- Uses access operation

**Path Query:**
- Time Complexity: O(log n) amortized
- Queries path between two nodes
- Requires nodes in same tree

**Path Update:**
- Time Complexity: O(log n) amortized
- Updates path between two nodes
- Requires nodes in same tree

### Edge Cases Handled

- Empty forest
- Single node trees
- Already connected nodes
- Cutting root nodes
- Disconnected nodes
- Invalid operations

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
- LinkCutNode creation and operations
- LinkCutTree creation
- Link operations
- Cut operations
- Find root operations
- Path queries and updates
- Connectivity checking
- Edge cases (empty, single node, invalid inputs)
- Complex operation sequences

## Troubleshooting

### Common Issues

**Incorrect connectivity results:**
- Verify link/cut operations completed successfully
- Check that nodes are in correct trees
- Ensure access operations work correctly

**Performance issues:**
- Link-cut trees are O(log n) amortized
- Individual operations may be O(n) worst case
- Amortized analysis applies to sequences

**Memory issues:**
- Link-cut trees use O(n) space
- For very large forests, monitor memory usage

### Error Messages

**"Nodes X and Y already connected"**: Attempted to link nodes in same tree.

**"Node X has no parent to cut"**: Attempted to cut root node.

### Best Practices

1. **Use for dynamic trees** - Link-cut trees excel with link/cut operations
2. **Check connectivity** - Verify nodes are connected before path operations
3. **Monitor performance** - Track operation times for your specific use case
4. **Handle errors** - Check return values of link/cut operations
5. **Consider alternatives** - For static trees, other structures may be better

## Performance Characteristics

### Time Complexity

| Operation | Amortized | Worst Case |
|-----------|-----------|------------|
| Link | O(log n) | O(n) |
| Cut | O(log n) | O(n) |
| Find Root | O(log n) | O(n) |
| Path Query | O(log n) | O(n) |
| Path Update | O(log n) | O(n) |
| Are Connected | O(log n) | O(n) |

Where n is the number of nodes in the forest.

### Space Complexity

- Node storage: O(n)
- Splay trees: O(n)
- Total: O(n)

### Amortized Analysis

**Theorem:**
Sequence of m operations on link-cut tree with n nodes takes O(m log n) time.

**Implications:**
- Average cost per operation: O(log n)
- Individual operations may be O(n)
- Performance improves with operation sequences

## Applications

- **Dynamic Connectivity**: Maintain connectivity in dynamic graphs
- **Network Flow**: Dynamic tree operations in flow algorithms
- **Competitive Programming**: Fast dynamic tree operations
- **Graph Algorithms**: Dynamic tree-based graph algorithms
- **Path Problems**: Efficient path queries and updates

## Comparison with Other Data Structures

**Link-Cut Tree:**
- O(log n) amortized operations
- Supports link and cut
- Good for dynamic trees
- More complex implementation

**Euler Tour Tree:**
- O(log n) operations
- Supports link and cut
- Different approach
- Similar complexity

**Heavy-Light Decomposition:**
- O(log^2 n) path queries
- No link/cut support
- Good for static trees
- Simpler implementation

**Union-Find:**
- O(α(n)) operations
- No path queries
- Simpler
- Less functionality

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
