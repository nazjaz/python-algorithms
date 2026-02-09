# Red-Black Tree Data Structure

A Python implementation of red-black tree data structure with insertion, deletion, and rebalancing operations. This tool provides O(log n) operations for insert, delete, and search while maintaining tree balance through color coding and rotation operations.

## Project Title and Description

The Red-Black Tree tool implements a self-balancing binary search tree that maintains balance through color coding (red and black nodes) and rotation operations. Red-black trees ensure that the longest path from root to leaf is at most twice the shortest path, guaranteeing O(log n) operations for all tree operations.

This tool solves the problem of maintaining a balanced binary search tree to ensure O(log n) operations even in worst-case scenarios. Red-black trees are widely used in many standard library implementations (such as C++ STL map/set, Java TreeMap/TreeSet) and are preferred over AVL trees in scenarios where insertions and deletions are more frequent than lookups.

**Target Audience**: Students learning data structures, developers studying self-balancing trees, database engineers, competitive programmers, educators teaching computer science concepts, and anyone interested in understanding balanced tree structures, color-based balancing, and rotation operations.

## Features

- Red-black tree implementation with automatic balancing
- Insert operation with color fixing and rotation support
- Delete operation with color fixing and rotation support
- Search operation
- Tree traversal (inorder, preorder, postorder)
- Red-black property validation
- Height calculation
- All rotation types (left, right)
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
cd /path/to/python-algorithms/red-black-tree
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

Run the main script to see a demonstration of red-black tree operations:

```bash
python src/main.py
```

This will:
1. Insert a series of keys into the tree
2. Display tree properties (size, height, validity)
3. Perform traversals
4. Search for a key
5. Delete a key
6. Display final tree state

### Programmatic Usage

```python
from src.main import RedBlackTree

# Create tree instance
tree = RedBlackTree()

# Insert keys
tree.insert(10)
tree.insert(20)
tree.insert(30)
tree.insert(40)
tree.insert(50)

# Search for key
found = tree.search(30)  # Returns True

# Delete key
tree.delete(30)

# Traverse tree
inorder = tree.inorder_traversal()  # Returns sorted list
preorder = tree.preorder_traversal()
postorder = tree.postorder_traversal()

# Get tree properties
size = tree.get_size()
height = tree.height()
is_valid = tree.is_valid()  # Validates red-black properties
```

### Common Use Cases

**Maintain Sorted Data:**
1. Insert keys into tree
2. Use inorder traversal to get sorted order
3. Tree automatically maintains balance

**Efficient Search:**
1. Build tree with insertions
2. Search for keys in O(log n) time
3. Guaranteed logarithmic performance

**Dynamic Data Structure:**
1. Insert and delete keys as needed
2. Tree remains balanced automatically
3. All operations remain O(log n)

## Project Structure

```
red-black-tree/
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

- `src/main.py`: Contains `RedBlackTree` and `RedBlackNode` classes with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Red-Black Tree

**Definition:**
A red-black tree is a self-balancing binary search tree where each node has an extra bit for color (red or black). The tree maintains balance by enforcing five properties that ensure the longest path from root to leaf is at most twice the shortest path.

**Properties:**
1. Every node is either red or black
2. The root is always black
3. All leaves (NIL nodes) are black
4. If a node is red, both its children are black (no two consecutive red nodes)
5. Every path from a node to its descendant leaves contains the same number of black nodes (black height property)

**Example:**
```
       30(B)
      /     \
   20(R)    40(B)
   /  \     /  \
 10(B) 25(B) 35(B) 50(B)
```

**Applications:**
- C++ STL map and set containers
- Java TreeMap and TreeSet
- Linux kernel process scheduler
- Database indexing
- File systems
- Priority queues
- Sorted data structures

### Rotation Operations

**Left Rotation:**
- Used when right subtree needs restructuring
- Rotates node and its right child
- Maintains BST property
- Preserves inorder traversal order

**Right Rotation:**
- Used when left subtree needs restructuring
- Rotates node and its left child
- Maintains BST property
- Preserves inorder traversal order

### Operations

**Insert:**
- Time Complexity: O(log n)
- Space Complexity: O(1) iterative, O(log n) for recursion
- Insert like BST, then fix colors and rotate if needed
- At most 2 rotations needed

**Delete:**
- Time Complexity: O(log n)
- Space Complexity: O(1) iterative, O(log n) for recursion
- Delete like BST, then fix colors and rotate if needed
- At most 3 rotations needed

**Search:**
- Time Complexity: O(log n)
- Space Complexity: O(1) iterative, O(log n) for recursion
- Standard BST search

**Traversal:**
- Time Complexity: O(n)
- Space Complexity: O(n)
- Visit all nodes in specified order

### Edge Cases Handled

- Empty tree
- Single node tree
- Duplicate keys (not inserted)
- Very unbalanced insertions (automatically balanced)
- Deletion of root
- Deletion of leaf nodes
- Deletion of nodes with one child
- Deletion of nodes with two children
- Large trees (tested with 100+ nodes)
- Sequential insert and delete operations

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
- Red-black tree insertion with color fixing
- Red-black tree deletion with color fixing
- Search operations
- Tree traversals
- Red-black property validation
- Edge cases (empty tree, single node, duplicates)
- Large tree operations
- Sequential operations
- Root deletion
- Property validation (root is black, no double red, black height)

## Troubleshooting

### Common Issues

**Tree not valid:**
- This should not happen with correct implementation
- Check rotation operations
- Verify color fixing logic
- Ensure root is always black

**Duplicate keys:**
- Duplicate keys are not inserted
- This is expected behavior
- Use different keys

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. The tool will use default settings, but you can create a config.yaml file for custom logging configuration.

**"Key already exists in tree"**: Attempted to insert a duplicate key. This is expected behavior - red-black trees typically don't allow duplicates.

**"Key not found in tree"**: Attempted to delete or search for a key that doesn't exist in the tree.

### Best Practices

1. **Use red-black tree for sorted data** - Maintains sorted order efficiently
2. **Trust automatic balancing** - Tree balances itself after operations
3. **Use for frequent insertions/deletions** - Better than AVL for mixed workloads
4. **Handle duplicates** - Duplicate keys are not inserted
5. **Check validity** - Use is_valid() to verify tree state
6. **Use inorder traversal** - Gets sorted order of keys
7. **Consider tree height** - Height should be O(log n)

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
