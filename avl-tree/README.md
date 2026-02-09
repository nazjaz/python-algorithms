# AVL Tree (Self-Balancing Binary Search Tree)

A Python implementation of AVL tree data structure with rotation operations for self-balancing. This tool provides O(log n) operations for insert, delete, and search while maintaining tree balance automatically.

## Project Title and Description

The AVL Tree tool implements a self-balancing binary search tree that maintains balance by ensuring the height difference between left and right subtrees is at most 1 for all nodes. It includes all rotation operations (left, right, left-right, right-left) to maintain balance after insertions and deletions.

This tool solves the problem of maintaining a balanced binary search tree to ensure O(log n) operations even in worst-case scenarios. AVL trees are widely used in databases, file systems, and applications requiring efficient sorted data structures.

**Target Audience**: Students learning data structures, developers studying self-balancing trees, database engineers, competitive programmers, educators teaching computer science concepts, and anyone interested in understanding balanced tree structures and rotation operations.

## Features

- AVL tree implementation with automatic balancing
- Insert operation with rotation support
- Delete operation with rotation support
- Search operation
- Tree traversal (inorder, preorder, postorder)
- Balance checking
- Height calculation
- All rotation types (left, right, left-right, right-left)
- Performance comparison and analysis
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/avl-tree
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
python src/main.py --help
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

### Insert Keys

Insert keys into AVL tree:

```bash
python src/main.py 10 20 30 40 50 --operation insert
```

### Search for Key

Search for key in tree:

```bash
python src/main.py 10 20 30 40 50 --operation search --key 30
```

### Delete Key

Delete key from tree:

```bash
python src/main.py 10 20 30 40 50 --operation delete --key 30
```

### Traverse Tree

Traverse tree in different orders:

```bash
python src/main.py 10 20 30 40 50 --operation traverse --traversal inorder
python src/main.py 10 20 30 40 50 --operation traverse --traversal preorder
python src/main.py 10 20 30 40 50 --operation traverse --traversal postorder
```

### All Operations

Perform all operations:

```bash
python src/main.py 10 20 30 40 50 --operation all --key 30
```

### Performance Comparison

Compare performance of operations:

```bash
python src/main.py 10 20 30 40 50 --operation compare --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py 10 20 30 40 50 --operation compare --report report.txt
```

### Command-Line Arguments

- `keys`: (Required) Keys to insert into AVL tree (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-o, --operation`: Operation to perform - insert, search, delete, traverse, compare, or all (default: all)
- `-k, --key`: Key for search or delete operation
- `-t, --traversal`: Traversal type - inorder, preorder, or postorder (default: inorder)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Maintain Sorted Data:**
1. Insert keys: `python src/main.py 10 20 30 40 50 --operation insert`
2. Get sorted order: `python src/main.py 10 20 30 40 50 --operation traverse`
3. Maintain balance automatically

**Efficient Search:**
1. Build tree: `python src/main.py 10 20 30 40 50 --operation insert`
2. Search: `python src/main.py 10 20 30 40 50 --operation search --key 30`
3. O(log n) search time guaranteed

**Dynamic Data Structure:**
1. Insert and delete: `python src/main.py 10 20 30 --operation delete --key 20`
2. Tree remains balanced
3. Operations remain O(log n)

## Project Structure

```
avl-tree/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main application code
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains `AVLTree` and `AVLNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### AVL Tree

**Definition:**
An AVL tree is a self-balancing binary search tree where the height difference between left and right subtrees (balance factor) is at most 1 for all nodes. This ensures the tree remains balanced and operations are O(log n).

**Properties:**
- Binary search tree property (left < root < right)
- Balance property (|height(left) - height(right)| ≤ 1)
- Height is O(log n) where n is number of nodes

**Example:**
```
       30
      /  \
    20    40
   /  \
 10   25
```

**Applications:**
- Database indexing
- File systems
- Priority queues
- Sorted data structures
- Range queries

### Rotation Operations

**Left Rotation:**
- Used when right subtree is too tall
- Rotates node and its right child
- Maintains BST property

**Right Rotation:**
- Used when left subtree is too tall
- Rotates node and its left child
- Maintains BST property

**Left-Right Rotation:**
- Used for left-right imbalance
- First left rotation on left child
- Then right rotation on root

**Right-Left Rotation:**
- Used for right-left imbalance
- First right rotation on right child
- Then left rotation on root

### Operations

**Insert:**
- Time Complexity: O(log n)
- Space Complexity: O(log n) for recursion
- Insert like BST, then balance if needed

**Delete:**
- Time Complexity: O(log n)
- Space Complexity: O(log n) for recursion
- Delete like BST, then balance if needed

**Search:**
- Time Complexity: O(log n)
- Space Complexity: O(log n) for recursion
- Standard BST search

**Traversal:**
- Time Complexity: O(n)
- Space Complexity: O(n)
- Visit all nodes in order

### Edge Cases Handled

- Empty tree
- Single node tree
- Duplicate keys (not inserted)
- Very unbalanced insertions (automatically balanced)
- Deletion of root
- Deletion of leaf nodes
- Deletion of nodes with one child
- Deletion of nodes with two children
- Large trees

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
- AVL tree insertion with rotations
- AVL tree deletion with rotations
- Search operations
- Tree traversals
- Balance checking
- Edge cases (empty tree, single node, duplicates)
- Performance comparison functionality
- Error handling
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**Tree not balanced:**
- This should not happen with correct implementation
- Check rotation operations
- Verify balance factor calculation

**Duplicate keys:**
- Duplicate keys are not inserted
- This is expected behavior
- Use different keys

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use AVL tree for sorted data** - Maintains sorted order efficiently
2. **Trust automatic balancing** - Tree balances itself after operations
3. **Use for frequent searches** - O(log n) search time guaranteed
4. **Handle duplicates** - Duplicate keys are not inserted
5. **Check balance** - Use is_balanced() to verify tree state
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
