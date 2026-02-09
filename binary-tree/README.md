# Binary Tree Data Structure

A Python implementation of a binary tree data structure with insertion, deletion, and three traversal methods: inorder, preorder, and postorder. The binary tree maintains the property that each node has at most two children.

## Project Title and Description

The Binary Tree implementation provides a complete binary tree data structure with fundamental operations including insertion, deletion, and multiple traversal methods. It demonstrates how binary trees organize data hierarchically and how different traversal orders serve different purposes.

This tool solves the problem of understanding and working with binary tree data structures, which are fundamental to many computer science concepts including binary search trees, heaps, expression trees, and decision trees.

**Target Audience**: Students learning data structures, developers studying tree algorithms, educators teaching binary trees, and anyone interested in understanding hierarchical data organization.

## Features

- Binary tree data structure with TreeNode class
- Insertion using level-order (breadth-first) approach
- Deletion with structure maintenance
- Search functionality
- Inorder traversal (Left, Root, Right)
- Preorder traversal (Root, Left, Right)
- Postorder traversal (Left, Right, Root)
- Level-order traversal (breadth-first)
- Tree visualization
- Height and size calculation
- Comprehensive logging
- Detailed analysis reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/binary-tree
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

### Demonstration Mode

Run demonstration with example tree:

```bash
python src/main.py --demo
```

### With Tree Visualization

Show tree structure:

```bash
python src/main.py --demo --visualize
```

### Insert Values

Insert values into tree:

```bash
python src/main.py --insert 10 5 15 3 7
```

### Delete Value

Delete value from tree:

```bash
python src/main.py --insert 10 5 15 --delete 5
```

### Search Value

Search for value in tree:

```bash
python src/main.py --insert 10 5 15 --search 5
```

### Perform Traversals

Perform different traversals:

```bash
# Inorder traversal
python src/main.py --insert 10 5 15 --inorder

# Preorder traversal
python src/main.py --insert 10 5 15 --preorder

# Postorder traversal
python src/main.py --insert 10 5 15 --postorder

# Level-order traversal
python src/main.py --insert 10 5 15 --levelorder
```

### Generate Report

Generate detailed analysis report:

```bash
python src/main.py --demo --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-i, --insert`: Values to insert into tree
- `-d, --delete`: Value to delete from tree
- `-s, --search`: Value to search for in tree
- `--inorder`: Perform inorder traversal
- `--preorder`: Perform preorder traversal
- `--postorder`: Perform postorder traversal
- `--levelorder`: Perform level-order traversal
- `-v, --visualize`: Show tree visualization
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example tree

### Common Use Cases

**Learn Binary Tree:**
1. Run: `python src/main.py --demo`
2. Review tree structure
3. Understand traversal orders

**Study Traversals:**
1. Run: `python src/main.py --demo --visualize`
2. Review all traversal methods
3. Understand traversal order differences

**Practice Operations:**
1. Run: `python src/main.py --insert 10 5 15 3 7`
2. Perform traversals
3. Delete and search values

**Analyze Tree:**
1. Run: `python src/main.py --demo --report report.txt`
2. Review tree properties
3. Understand tree structure

## Project Structure

```
binary-tree/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
├── .env.example             # Environment variables template
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

- `src/main.py`: Contains `TreeNode` and `BinaryTree` classes with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the binary tree implementation
- `logs/`: Directory for application log files

## Algorithm Details

### Binary Tree Structure

A binary tree is a tree data structure where each node has at most two children, referred to as left child and right child.

**Properties:**
- Each node has at most 2 children
- Root node has no parent
- Leaf nodes have no children
- Height: longest path from root to leaf
- Size: total number of nodes

### Insertion Algorithm

**Level-Order Insertion:**
```
1. Create new node with value
2. If tree is empty, set as root
3. Otherwise, find first available position using level-order
4. Insert at first available left or right child position
```

**Example:**
```
Insert: 10, 5, 15, 3, 7

Step 1: Insert 10 (root)
    10

Step 2: Insert 5 (left child of 10)
    10
   /
  5

Step 3: Insert 15 (right child of 10)
    10
   /  \
  5   15

Step 4: Insert 3 (left child of 5)
    10
   /  \
  5   15
 /
3

Step 5: Insert 7 (right child of 5)
    10
   /  \
  5   15
 / \
3   7
```

### Deletion Algorithm

**Deletion Strategy:**
```
1. Find node to delete
2. Find rightmost node at deepest level
3. Replace node to delete with rightmost node's value
4. Remove rightmost node
```

**Example:**
```
Delete 5 from:
    10
   /  \
  5   15
 / \
3   7

Step 1: Find node 5
Step 2: Find rightmost deepest node (7)
Step 3: Replace 5 with 7
Step 4: Remove node 7

Result:
    10
   /  \
  7   15
 /
3
```

### Traversal Algorithms

#### Inorder Traversal (Left, Root, Right)

**Algorithm:**
```
1. Traverse left subtree
2. Visit root
3. Traverse right subtree
```

**Example:**
```
Tree:
    10
   /  \
  5   15
 / \
3   7

Inorder: 3, 5, 7, 10, 15
```

**Use Cases:**
- Binary Search Tree: produces sorted order
- Expression trees: infix notation

#### Preorder Traversal (Root, Left, Right)

**Algorithm:**
```
1. Visit root
2. Traverse left subtree
3. Traverse right subtree
```

**Example:**
```
Tree:
    10
   /  \
  5   15
 / \
3   7

Preorder: 10, 5, 3, 7, 15
```

**Use Cases:**
- Copying tree structure
- Prefix notation in expression trees
- Creating tree from traversal

#### Postorder Traversal (Left, Right, Root)

**Algorithm:**
```
1. Traverse left subtree
2. Traverse right subtree
3. Visit root
```

**Example:**
```
Tree:
    10
   /  \
  5   15
 / \
3   7

Postorder: 3, 7, 5, 15, 10
```

**Use Cases:**
- Deleting tree
- Postfix notation in expression trees
- Calculating directory sizes

#### Level-Order Traversal (Breadth-First)

**Algorithm:**
```
1. Use queue data structure
2. Enqueue root
3. While queue not empty:
   a. Dequeue node
   b. Visit node
   c. Enqueue left child (if exists)
   d. Enqueue right child (if exists)
```

**Example:**
```
Tree:
    10
   /  \
  5   15
 / \
3   7

Level-order: 10, 5, 15, 3, 7
```

**Use Cases:**
- Printing tree level by level
- Finding level of node
- Breadth-first search

### Time Complexity

- **Insertion:** O(n) where n is number of nodes
- **Deletion:** O(n) where n is number of nodes
- **Search:** O(n) where n is number of nodes
- **Traversals:** O(n) where n is number of nodes
- **Height:** O(n) where n is number of nodes
- **Size:** O(n) where n is number of nodes

### Space Complexity

- **Traversals (recursive):** O(h) where h is height (recursion stack)
- **Level-order:** O(n) for queue
- **Overall:** O(n) for storing tree structure

## Applications

### Expression Trees

- Represent arithmetic expressions
- Evaluate expressions
- Convert between notations

### Binary Search Trees

- Efficient search, insert, delete
- Maintain sorted order
- Range queries

### Heaps

- Priority queues
- Heap sort
- Graph algorithms (Dijkstra's)

### Decision Trees

- Machine learning
- Classification
- Regression

### Other Applications

- File system hierarchies
- Parse trees (compilers)
- Game trees
- Organizational hierarchies
- Huffman coding trees

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
- TreeNode operations
- Insertion operations
- Deletion operations
- Search operations
- All traversal methods
- Height and size calculations
- Tree visualization
- Edge cases (empty tree, single node)
- Different data types (int, string, float)

## Troubleshooting

### Common Issues

**Value not found when deleting:**
- Value doesn't exist in tree
- Check value exists before deletion
- Use search to verify value presence

**Empty tree operations:**
- Tree is empty
- Insert values before other operations
- Check tree size before operations

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Cannot delete from empty tree"**: Tree is empty. Insert values before deletion.

**"Value not found in tree"**: Value doesn't exist. Use search to verify.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use level-order insertion** for complete tree structure
2. **Understand traversal orders** for different use cases
3. **Use visualization** to understand tree: `--visualize`
4. **Generate reports** for documentation: `--report report.txt`
5. **Use demonstration mode** to see examples: `--demo`
6. **Check tree size** before operations on empty tree

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
