# Van Emde Boas Tree for Integer Priority Queues with O(log log U) Operations

A Python implementation of van Emde Boas (vEB) tree data structure that efficiently supports priority queue operations on integers from universe [0, U-1]. Van Emde Boas trees achieve O(log log U) time complexity for insert, delete, and search operations, and O(1) for min/max operations.

## Project Title and Description

The Van Emde Boas Tree tool implements a data structure that maintains a set of integers from a bounded universe [0, U-1] where U must be a power of 2. It uses a recursive structure that splits the universe into clusters, achieving O(log log U) time complexity for most operations.

This tool solves the problem of efficiently maintaining integer priority queues with fast predecessor/successor queries, which is fundamental in many applications including competitive programming, graph algorithms, and network routing. Van Emde Boas trees provide O(log log U) time complexity for insert, delete, search, predecessor, and successor operations, and O(1) for min/max.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding advanced priority queue data structures.

## Features

- Van Emde Boas tree implementation with recursive structure
- O(log log U) time complexity for insert, delete, search, predecessor, successor
- O(1) time complexity for min/max operations
- Universe size must be power of 2
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
cd /path/to/python-algorithms/van-emde-boas-tree
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
- `logging.file`: Path to log file (default: "logs/van_emde_boas_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/van_emde_boas_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of van Emde Boas tree operations:

```bash
python src/main.py
```

This will:
1. Create a vEB tree with universe size 16
2. Insert values
3. Perform min/max queries
4. Perform search operations
5. Perform predecessor/successor queries
6. Delete values

### Programmatic Usage

```python
from src.main import VanEmdeBoasTree

# Create vEB tree with universe size 16
tree = VanEmdeBoasTree(universe_size=16)

# Insert values
tree.insert(2)
tree.insert(5)
tree.insert(7)

# Get min/max (O(1))
min_val = tree.get_min()  # 2
max_val = tree.get_max()  # 7

# Search (O(log log U))
exists = tree.contains(5)  # True

# Predecessor/Successor (O(log log U))
pred = tree.predecessor(7)  # 5
succ = tree.successor(2)   # 5

# Delete (O(log log U))
tree.delete(5)
```

### Common Use Cases

**Integer Priority Queues:**
1. Fast min/max operations
2. Efficient predecessor/successor queries
3. Bounded universe integer sets

**Competitive Programming:**
1. Fast integer set operations
2. Priority queue with predecessor/successor
3. Bounded universe problems

**Graph Algorithms:**
1. Priority queues for graph algorithms
2. Integer-based data structures
3. Network routing

## Project Structure

```
van-emde-boas-tree/
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

- `src/main.py`: Contains `VanEmdeBoasTree` and `VEBNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Van Emde Boas Tree

**Definition:**
A van Emde Boas tree maintains a set of integers from universe [0, U-1] where U is a power of 2. It uses a recursive structure that splits the universe into clusters, achieving O(log log U) time complexity.

**Properties:**
1. Universe size U must be power of 2
2. O(log log U) height
3. Recursive structure with clusters and summary
4. O(1) min/max operations

**Structure:**
```
        Root (U = 16)
       /              \
   Clusters[0..3]    Summary
   (U = 4 each)      (U = 4)
```

### Recursive Structure

**Universe Splitting:**
- Universe U split into sqrt(U) clusters
- Each cluster has size sqrt(U)
- Summary tree tracks which clusters are non-empty
- Recursively applied

**High/Low Decomposition:**
- Value x = high(x) * sqrt(U) + low(x)
- high(x): cluster index
- low(x): position in cluster

### Operations

**Insert:**
- Time Complexity: O(log log U)
- Recursively insert into appropriate cluster
- Update summary if cluster was empty
- Handle min/max updates

**Delete:**
- Time Complexity: O(log log U)
- Recursively delete from cluster
- Update summary if cluster becomes empty
- Handle min/max updates

**Search (Contains):**
- Time Complexity: O(log log U)
- Recursively search in appropriate cluster
- Check min/max for early termination

**Min/Max:**
- Time Complexity: O(1)
- Stored directly in root node
- Constant time access

**Predecessor:**
- Time Complexity: O(log log U)
- Check current cluster first
- If not found, check previous clusters via summary
- Recursively find predecessor

**Successor:**
- Time Complexity: O(log log U)
- Check current cluster first
- If not found, check next clusters via summary
- Recursively find successor

### Edge Cases Handled

- Empty tree
- Single element
- Universe size 2 (base case)
- Out of bounds values
- Duplicate insertions
- Deleting non-existent values
- Predecessor/successor of min/max

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
- VEBNode creation and operations
- VanEmdeBoasTree creation
- Insert operations
- Delete operations
- Search operations
- Min/max operations
- Predecessor/successor operations
- Edge cases (empty, single element, invalid inputs)
- Different universe sizes

## Troubleshooting

### Common Issues

**"Universe size must be a power of 2"**: Universe size must be 2^k for some k.

**Incorrect query results:**
- Verify universe size is power of 2
- Check that values are in range [0, U-1]
- Ensure operations completed successfully

**Performance issues:**
- vEB trees are O(log log U) per operation
- For small U, overhead may be significant
- For large U, performance is excellent

**Memory issues:**
- vEB trees use O(U) space
- For very large U, consider alternatives
- Monitor memory usage

### Error Messages

**"Universe size X must be a power of 2"**: Universe size not valid.

**"Value X out of universe range"**: Value not in [0, U-1].

### Best Practices

1. **Choose appropriate universe size** - Must be power of 2, choose smallest that fits
2. **Use for bounded universes** - vEB trees excel with bounded integer sets
3. **Validate inputs** - Check values are in range before operations
4. **Monitor performance** - Track operation times for your specific use case
5. **Consider alternatives** - For small universes, arrays might be better

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Insert | O(log log U) |
| Delete | O(log log U) |
| Search (Contains) | O(log log U) |
| Min | O(1) |
| Max | O(1) |
| Predecessor | O(log log U) |
| Successor | O(log log U) |

Where U is the universe size.

### Space Complexity

- Tree structure: O(U)
- Clusters: O(U)
- Summary: O(sqrt(U))
- Total: O(U)

### Query Performance

- Insert/Delete/Search: O(log log U) - excellent for large U
- Min/Max: O(1) - constant time
- Predecessor/Successor: O(log log U) - efficient queries
- Optimal for bounded universe integer sets

## Applications

- **Integer Priority Queues**: Fast min/max with predecessor/successor
- **Competitive Programming**: Fast integer set operations
- **Graph Algorithms**: Priority queues for graph algorithms
- **Network Routing**: Integer-based routing tables
- **Database Systems**: Integer indexing and queries

## Comparison with Other Data Structures

**Van Emde Boas Tree:**
- O(log log U) operations
- O(U) space
- Requires power of 2 universe
- Excellent for large bounded universes

**Binary Search Tree:**
- O(log n) operations
- O(n) space
- No universe restriction
- Better for small sets

**Hash Table:**
- O(1) average operations
- O(n) space
- No predecessor/successor
- Different use case

**Fenwick Tree:**
- O(log n) operations
- O(n) space
- Good for prefix sums
- Less efficient for predecessor/successor

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
