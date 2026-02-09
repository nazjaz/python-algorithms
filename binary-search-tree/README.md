# Binary Search Tree with Balancing and Performance Analysis

A Python implementation of binary search tree (BST) with AVL tree balancing and comprehensive performance analysis. This tool demonstrates the importance of tree balancing by comparing unbalanced BST against self-balancing AVL tree, showing how balancing ensures optimal O(log n) performance.

## Project Title and Description

The Binary Search Tree implementation provides both unbalanced BST and balanced AVL tree implementations with detailed performance analysis. It demonstrates how tree balancing prevents performance degradation and ensures consistent O(log n) operations even with worst-case input sequences.

This tool solves the problem of understanding when and why tree balancing is necessary, showing real-world performance differences between balanced and unbalanced trees through comprehensive analysis and metrics.

**Target Audience**: Students learning data structures, developers studying tree algorithms, educators teaching BST and balancing, and anyone interested in understanding performance implications of tree balancing.

## Features

- Binary Search Tree (unbalanced) implementation
- AVL Tree (self-balancing) implementation
- Insert, delete, and search operations
- Inorder traversal (produces sorted order)
- Automatic balancing with rotations (AVL)
- Performance statistics tracking
- Comparative performance analysis
- Height and size calculations
- Operation counting (comparisons, rotations)
- Comprehensive logging
- Detailed performance reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/binary-search-tree
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

Run demonstration with example trees:

```bash
python src/main.py --demo
```

### Compare Performance

Compare BST vs AVL performance:

```bash
python src/main.py --demo --compare
```

### Generate Performance Report

Generate detailed performance analysis report:

```bash
python src/main.py --demo --compare --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-i, --insert`: Values to insert into tree
- `-d, --delete`: Value to delete from tree
- `-s, --search`: Value to search for in tree
- `--type`: Tree type to use (bst, avl, both) - default: both
- `--compare`: Compare BST vs AVL performance
- `-r, --report`: Output path for analysis report
- `--demo`: Run demonstration with example trees

### Common Use Cases

**Learn BST and Balancing:**
1. Run: `python src/main.py --demo`
2. Review BST and AVL tree operations
3. Understand balancing benefits

**Compare Performance:**
1. Run: `python src/main.py --demo --compare`
2. Review height differences
3. Understand performance improvements

**Analyze Performance:**
1. Run: `python src/main.py --demo --compare --report report.txt`
2. Review detailed metrics
3. Understand when to use each tree type

## Project Structure

```
binary-search-tree/
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
│   └── API.md              # API documentation
└── logs/
    └── .gitkeep             # Placeholder for logs directory
```

### File Descriptions

- `src/main.py`: Contains `BSTNode`, `BST`, `AVLTree`, and `PerformanceAnalyzer` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the BST implementation
- `logs/`: Directory for application log files

## Algorithm Details

### Binary Search Tree (BST)

A binary search tree is a binary tree where:
- Left subtree contains values less than root
- Right subtree contains values greater than root
- Both subtrees are also BSTs

**Properties:**
- Inorder traversal produces sorted order
- Search, insert, delete operations
- No balancing guarantee

**Time Complexity:**
- Best case: O(log n) for balanced tree
- Average case: O(log n) for random data
- Worst case: O(n) for sorted/sequential data

### AVL Tree (Self-Balancing)

An AVL tree is a self-balancing BST where:
- Height difference between left and right subtrees is at most 1
- Automatically rebalances after insertions and deletions
- Maintains O(log n) height guarantee

**Properties:**
- Balance factor: height(left) - height(right) ∈ {-1, 0, 1}
- Rotations maintain balance
- Guaranteed O(log n) operations

**Time Complexity:**
- All operations: O(log n) guaranteed

### Balancing Operations

**Rotations:**
1. **Right Rotation (RR)**: Fixes left-heavy tree
2. **Left Rotation (LL)**: Fixes right-heavy tree
3. **Left-Right Rotation (LR)**: Fixes left-right imbalance
4. **Right-Left Rotation (RL)**: Fixes right-left imbalance

**Rotation Cases:**
- **Left Left**: Right rotation on unbalanced node
- **Right Right**: Left rotation on unbalanced node
- **Left Right**: Left rotation on left child, then right rotation
- **Right Left**: Right rotation on right child, then left rotation

### Performance Analysis

**Metrics Tracked:**
- Tree height (critical for performance)
- Operation counts (comparisons, insertions, deletions, searches)
- Execution time (insert, search operations)
- Rotations performed (AVL only)
- Average comparisons per search

**Key Comparisons:**
- Height reduction: AVL vs BST
- Search time improvement
- Consistency of performance
- Overhead of balancing

### Time Complexity Comparison

| Operation | BST (Best) | BST (Worst) | AVL (All Cases) |
|-----------|-----------|-------------|-----------------|
| Search    | O(log n)  | O(n)        | O(log n)        |
| Insert    | O(log n)  | O(n)        | O(log n)        |
| Delete    | O(log n)  | O(n)        | O(log n)        |

### Space Complexity

- **Both:** O(n) for storing n nodes
- **AVL:** Additional O(1) per node for height tracking

### When to Use Each

**Use BST when:**
- Data is randomly ordered
- Simplicity is preferred
- Worst-case performance is acceptable
- Memory is constrained

**Use AVL when:**
- Data may be sorted or sequential
- Guaranteed O(log n) performance is critical
- Consistent performance is required
- Worst-case scenarios must be avoided

## Applications

### Database Indexing

- Efficient data retrieval
- Range queries
- Sorted data access

### Search Engines

- Fast lookups
- Ranking algorithms
- Index maintenance

### Other Applications

- Symbol tables (compilers)
- Priority queues
- Expression evaluation
- File system organization
- Network routing tables

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
- BSTNode operations
- BST operations (insert, delete, search)
- AVL tree operations with rotations
- Performance analyzer
- Balancing verification
- Edge cases (empty tree, single node, sequential data)
- Height and size calculations
- Statistics tracking

## Troubleshooting

### Common Issues

**Tree becomes unbalanced:**
- Use AVL tree for automatic balancing
- Check input data ordering
- Monitor tree height

**Performance degradation:**
- Use AVL tree for guaranteed O(log n)
- Analyze with performance analyzer
- Check for sequential data insertion

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

**Performance warnings**: Tree height is high. Consider using AVL tree for better performance.

### Best Practices

1. **Use AVL for critical applications** requiring guaranteed performance
2. **Use BST for simple cases** with random data
3. **Monitor tree height** to detect imbalance
4. **Use performance analyzer** to compare implementations
5. **Generate reports** for documentation: `--report report.txt`
6. **Use demonstration mode** to see examples: `--demo`

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
