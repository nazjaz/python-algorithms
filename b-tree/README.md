# B-Tree Data Structure Optimized for Disk-Based Storage

A Python implementation of B-tree data structure with split and merge operations optimized for disk-based storage. This tool provides efficient insertion, deletion, and search operations with minimal disk I/O, making it ideal for database systems and file systems.

## Project Title and Description

The B-Tree tool implements a self-balancing tree data structure that maintains sorted data and allows efficient insertion, deletion, and search operations. B-trees are specifically designed for systems that read and write large blocks of data, such as databases and file systems, where minimizing disk I/O is critical for performance.

This tool solves the problem of maintaining a balanced tree structure optimized for disk-based storage systems. Unlike binary search trees, B-trees have multiple keys per node and multiple children, which reduces the height of the tree and minimizes the number of disk accesses required for operations.

**Target Audience**: Database engineers, file system developers, students learning advanced data structures, system programmers, database administrators, competitive programmers, and anyone interested in understanding disk-optimized data structures and B-tree algorithms.

## Features

- B-tree implementation with configurable minimum degree
- Insert operation with automatic split when nodes are full
- Delete operation with automatic merge when nodes are underfull
- Search operation with O(log n) time complexity
- Tree traversal (inorder)
- B-tree property validation
- Height and size calculations
- Disk I/O simulation and statistics tracking
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
cd /path/to/python-algorithms/b-tree
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

Run the main script to see a demonstration of B-tree operations:

```bash
python src/main.py
```

This will:
1. Insert a series of keys into the tree
2. Display tree properties (size, height, validity)
3. Show disk I/O statistics
4. Perform traversals
5. Search for a key
6. Delete a key
7. Display final tree state

### Programmatic Usage

```python
from src.main import BTree

# Create tree instance with minimum degree 3
tree = BTree(min_degree=3)

# Insert keys
tree.insert(10)
tree.insert(20)
tree.insert(30)
tree.insert(40)
tree.insert(50)

# Search for key
node, index = tree.search(30)  # Returns (node, index) if found

# Delete key
tree.delete(30)

# Traverse tree
inorder = tree.inorder_traversal()  # Returns sorted list

# Get tree properties
size = tree.get_size()
height = tree.get_height()
is_valid = tree.is_valid()  # Validates B-tree properties

# Get disk I/O statistics
io_stats = tree.get_disk_io_stats()
print(f"Reads: {io_stats['disk_reads']}, Writes: {io_stats['disk_writes']}")
```

### Common Use Cases

**Database Indexing:**
1. Create B-tree with appropriate minimum degree
2. Insert index keys
3. Use search for fast lookups
4. Tree automatically maintains balance

**File System Directory Structure:**
1. Use B-tree to store file metadata
2. Insert file entries
3. Search for files efficiently
4. Delete files as needed

**Large Dataset Management:**
1. Insert large number of keys
2. All operations remain O(log n)
3. Minimal disk I/O required
4. Tree stays balanced automatically

## Project Structure

```
b-tree/
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

- `src/main.py`: Contains `BTree` and `BTreeNode` classes with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### B-Tree

**Definition:**
A B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time. Unlike binary search trees, B-trees can have multiple keys per node and multiple children, which makes them ideal for disk-based storage systems.

**Properties:**
1. All leaves are at the same level
2. Every node (except root) has at least `min_degree - 1` keys
3. Every node has at most `2 * min_degree - 1` keys
4. Root has at least 1 key (unless tree is empty)
5. A node with `k` keys has `k + 1` children
6. All keys in a node are sorted

**Example (min_degree = 3):**
```
        [20, 40]
       /    |    \
   [10]  [30]  [50, 60]
```

**Applications:**
- Database indexing (MySQL, PostgreSQL, Oracle)
- File systems (NTFS, HFS+, ext4)
- Storage systems
- Large-scale data management
- Disk-based sorting

### Split Operation

**When:** A node becomes full (has `2 * min_degree - 1` keys)

**Process:**
1. Create new node
2. Move upper half of keys to new node
3. Move corresponding children to new node
4. Promote middle key to parent
5. Insert new node as child of parent

**Disk I/O:** 3 writes (original node, new node, parent)

### Merge Operation

**When:** A node becomes underfull (has fewer than `min_degree - 1` keys) after deletion

**Process:**
1. Merge node with sibling
2. Move parent key down to merged node
3. Combine keys and children
4. Update parent

**Disk I/O:** 2 writes (merged node, parent)

### Operations

**Insert:**
- Time Complexity: O(log n)
- Space Complexity: O(1) per operation
- Disk I/O: O(log n) reads, O(log n) writes
- Insert like BST, split if node is full

**Delete:**
- Time Complexity: O(log n)
- Space Complexity: O(1) per operation
- Disk I/O: O(log n) reads, O(log n) writes
- Delete like BST, merge if node is underfull

**Search:**
- Time Complexity: O(log n)
- Space Complexity: O(1)
- Disk I/O: O(log n) reads
- Standard BST search

**Traversal:**
- Time Complexity: O(n)
- Space Complexity: O(n)
- Disk I/O: O(n) reads
- Visit all nodes in sorted order

### Edge Cases Handled

- Empty tree
- Single node tree
- Duplicate keys (not inserted)
- Very large trees (tested with 100+ nodes)
- Deletion of root
- Deletion of leaf nodes
- Deletion of internal nodes
- Split operations
- Merge operations
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
- B-tree insertion with split operations
- B-tree deletion with merge operations
- Search operations
- Tree traversals
- B-tree property validation
- Edge cases (empty tree, single node, duplicates)
- Large tree operations
- Sequential operations
- Disk I/O statistics
- Different minimum degrees

## Troubleshooting

### Common Issues

**Tree not valid:**
- This should not happen with correct implementation
- Check split and merge operations
- Verify minimum degree constraints
- Ensure all leaves are at same level

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

**"Key already exists in tree"**: Attempted to insert a duplicate key. This is expected behavior - B-trees typically don't allow duplicates.

**"Key not found in tree"**: Attempted to delete or search for a key that doesn't exist in the tree.

**"Minimum degree must be at least 2"**: The minimum degree must be 2 or greater for a valid B-tree.

### Best Practices

1. **Choose appropriate minimum degree** - Higher degree reduces height but increases node size
2. **Monitor disk I/O** - Use statistics to optimize operations
3. **Trust automatic balancing** - Tree balances itself after operations
4. **Use for large datasets** - B-trees excel with disk-based storage
5. **Handle duplicates** - Duplicate keys are not inserted
6. **Check validity** - Use is_valid() to verify tree state
7. **Use inorder traversal** - Gets sorted order of keys

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Insert    | O(log n)       |
| Delete    | O(log n)       |
| Search    | O(log n)       |
| Traversal | O(n)           |

### Disk I/O Complexity

| Operation | Reads | Writes |
|-----------|-------|--------|
| Insert    | O(log n) | O(log n) |
| Delete    | O(log n) | O(log n) |
| Search    | O(log n) | 0       |
| Traversal | O(n)   | 0       |

Where n is the number of keys in the tree.

### Space Complexity

- Node storage: O(n) total
- Auxiliary space: O(1) per operation
- Tree height: O(log n) with base = min_degree

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
