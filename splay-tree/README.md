# Splay Tree with Amortized Analysis and Self-Adjusting Operations

A Python implementation of splay tree data structure that automatically moves recently accessed elements to the root through splay operations. Splay trees achieve O(log n) amortized time complexity for all operations through self-adjusting rotations.

## Project Title and Description

The Splay Tree tool implements a self-adjusting binary search tree that automatically reorganizes itself by moving recently accessed elements to the root. This self-adjusting property ensures that frequently accessed elements are near the root, providing excellent amortized performance for access patterns with locality of reference.

This tool solves the problem of maintaining an efficient binary search tree without explicit balancing operations. Splay trees automatically adapt to access patterns, making them ideal for scenarios where recently accessed elements are likely to be accessed again.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding self-adjusting data structures and amortized analysis.

## Features

- Splay tree implementation with self-adjusting operations
- O(log n) amortized time complexity for all operations
- Binary search tree property (keys in sorted order)
- Automatic reorganization through splay operations
- Insert, delete, and search operations
- Min/max key retrieval
- Multiple traversal methods (inorder, preorder, postorder)
- Comprehensive amortized analysis tracking
- Detailed step-by-step logging
- Input validation
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/splay-tree
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
- `logging.file`: Path to log file (default: "logs/splay_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/splay_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of splay tree operations:

```bash
python src/main.py
```

This will:
1. Create a splay tree
2. Insert keys
3. Search for keys (automatically splaying to root)
4. Find min/max keys
5. Delete keys
6. Display amortized analysis statistics

### Programmatic Usage

```python
from src.main import SplayTree

# Create splay tree
tree = SplayTree()

# Insert keys
tree.insert(10)
tree.insert(20)
tree.insert(30)

# Search (automatically splays to root)
node = tree.search(20)  # Returns node, splays to root

# Delete
tree.delete(20)

# Get traversals
inorder = tree.inorder_traversal()  # Returns sorted list
preorder = tree.preorder_traversal()
postorder = tree.postorder_traversal()

# Find min/max (automatically splays)
min_key = tree.find_min()
max_key = tree.find_max()

# Get amortized analysis
analysis = tree.get_amortized_analysis()
print(f"Total operations: {analysis['total_operations']}")
print(f"Average rotations per splay: {analysis['average_rotations_per_splay']}")
```

### Common Use Cases

**Locality of Reference:**
1. Frequently accessed elements move to root
2. Subsequent accesses are faster
3. Ideal for caching and LRU-like behavior

**Self-Adjusting Structure:**
1. No explicit balancing needed
2. Tree adapts to access patterns
3. Good amortized performance

**Simple Implementation:**
1. Simpler than AVL/Red-Black trees
2. No balance factors or colors
3. Only rotations needed

## Project Structure

```
splay-tree/
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

- `src/main.py`: Contains `SplayTree` and `SplayNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Splay Tree

**Definition:**
A splay tree is a self-adjusting binary search tree that automatically moves recently accessed elements to the root through splay operations. The tree maintains binary search tree property while reorganizing itself based on access patterns.

**Properties:**
1. Binary search tree property: keys in sorted order
2. Self-adjusting: accessed nodes move to root
3. Amortized O(log n) time complexity
4. Locality of reference: frequently accessed nodes near root

**Structure:**
```
        [30]
       /    \
    [20]    [40]
   /    \      \
[10]   [25]   [50]
```

After accessing 25, it moves to root:
```
        [25]
       /    \
    [20]    [30]
   /        /    \
[10]     [28]   [40]
                      \
                      [50]
```

**Key Insight:**
Splay operations move accessed nodes to root through rotations. This ensures frequently accessed elements are near the root, providing good amortized performance for access patterns with locality.

### Splay Operations

**Zig Rotation:**
- Single rotation when node is child of root
- Moves node directly to root
- Used when parent is root

**Zig-Zig Rotation:**
- Two rotations in same direction
- Used when node and parent are both left or both right children
- More efficient than two separate zig rotations

**Zig-Zag Rotation:**
- Two rotations in opposite directions
- Used when node is left child and parent is right child (or vice versa)
- Restructures tree more efficiently

### Amortized Analysis

**Potential Function:**
Splay trees use amortized analysis to prove O(log n) average performance. The analysis uses a potential function based on tree structure.

**Amortized Cost:**
- Each operation has amortized cost O(log n)
- Sequence of m operations: O(m log n)
- Individual operations may be O(n) worst-case
- Average over sequence is O(log n)

**Tracking:**
The implementation tracks:
- Total operations performed
- Total splay operations
- Total rotations performed
- Average rotations per splay
- Amortized cost per operation

### Operations

**Insert:**
- Time Complexity: O(log n) amortized
- Insert as BST, then splay new node to root

**Delete:**
- Time Complexity: O(log n) amortized
- Splay node to root, then remove and merge subtrees

**Search:**
- Time Complexity: O(log n) amortized
- Standard BST search, then splay found node (or last visited) to root

**Find Min/Max:**
- Time Complexity: O(log n) amortized
- Find node, then splay to root

**Traversal:**
- Time Complexity: O(n)
- Standard tree traversal (inorder, preorder, postorder)

### Rotations

**Zig (Single Rotation):**
- Used when node is direct child of root
- One rotation to move node to root

**Zig-Zig (Double Same-Direction):**
- Used when node and parent are both left or both right children
- Two rotations in same direction
- More efficient than two separate zigs

**Zig-Zag (Double Opposite-Direction):**
- Used when node and parent are on opposite sides
- Two rotations in opposite directions
- Restructures tree efficiently

### Edge Cases Handled

- Empty tree
- Single element
- Duplicate keys (rejected)
- Large number of elements
- Sequential insertions and deletions
- Search for non-existent keys
- Delete from empty tree
- Operations on empty tree

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
- Splay tree creation
- Insert operations
- Search operations (with splaying)
- Delete operations
- Min/max operations
- Traversal methods
- Amortized analysis tracking
- Edge cases (empty, single element, duplicates)
- Invalid input handling
- Splay operation correctness

## Troubleshooting

### Common Issues

**Performance worse than expected:**
- Splay trees have O(n) worst-case for individual operations
- Amortized analysis applies to sequences of operations
- Consider access patterns - locality helps performance

**Tree structure seems unbalanced:**
- This is normal for splay trees
- Tree reorganizes based on access patterns
- Amortized performance is still O(log n)

**Search not splaying correctly:**
- Verify splay operation is called after search
- Check that root is updated after splay
- Ensure parent pointers are maintained correctly

### Error Messages

**"Key already exists"**: Attempted to insert duplicate key.

**"Key not found"**: Attempted to delete non-existent key.

### Best Practices

1. **Use for locality** - Splay trees excel with access patterns showing locality
2. **Monitor amortized cost** - Use get_amortized_analysis() to track performance
3. **Consider access patterns** - Frequently accessed elements will be near root
4. **Validate structure** - Use traversals to verify BST property maintained
5. **Consider alternatives** - For guaranteed O(log n), use AVL/Red-Black trees

## Performance Characteristics

### Time Complexity

| Operation | Amortized | Worst Case |
|-----------|-----------|------------|
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Search | O(log n) | O(n) |
| Find Min/Max | O(log n) | O(n) |
| Traversal | O(n) | O(n) |

Where n is the number of elements.

### Space Complexity

- Node storage: O(n)
- Total: O(n)

### Amortized Analysis

**Theorem:**
Sequence of m operations on splay tree with n elements takes O(m log n) time.

**Implications:**
- Average cost per operation: O(log n)
- Individual operations may be O(n)
- Performance improves with locality of reference

## Applications

- **Caching**: Frequently accessed items move to root
- **Locality of Reference**: Good for access patterns with temporal locality
- **Simple Implementation**: Easier than AVL/Red-Black trees
- **Competitive Programming**: Useful for self-adjusting structures
- **Database Indexing**: Adaptive to query patterns
- **Network Routing**: Frequently used routes near root

## Comparison with Balanced Trees

**Splay Trees:**
- Simpler implementation
- Self-adjusting based on access
- O(log n) amortized
- O(n) worst-case per operation
- Good for locality of reference

**AVL/Red-Black Trees:**
- More complex implementation
- Explicit balancing
- O(log n) guaranteed per operation
- More code to maintain
- Consistent performance

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
