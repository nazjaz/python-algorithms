# Persistent Segment Tree for Range Queries Across Multiple Versions

A Python implementation of persistent segment tree data structure that supports range queries across multiple versions of an array. Each update creates a new version while preserving all previous versions, enabling efficient querying of historical states.

## Project Title and Description

The Persistent Segment Tree tool implements a persistent segment tree that maintains multiple versions of an array, allowing queries on any historical version. Unlike regular segment trees that modify the original structure, persistent segment trees create new nodes when updating, preserving all previous versions.

This tool solves the problem of querying historical versions of an array efficiently. It's particularly useful for problems requiring time-travel queries, version control systems, and scenarios where you need to query past states without losing current data.

**Target Audience**: Competitive programmers, algorithm students, data structure researchers, software engineers working with versioned data, and anyone interested in understanding persistent data structures.

## Features

- Persistent segment tree implementation
- Multiple version management
- Range sum queries across versions
- Range minimum queries across versions
- Range maximum queries across versions
- Point updates that create new versions
- Version array reconstruction
- O(log n) query and update operations
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
cd /path/to/python-algorithms/persistent-segment-tree
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

Run the main script to see a demonstration of persistent segment tree operations:

```bash
python src/main.py
```

This will:
1. Create a persistent segment tree from an array
2. Query version 0
3. Create new versions with updates
4. Query different versions
5. Display all versions

### Programmatic Usage

```python
from src.main import PersistentSegmentTree

# Create tree from array
array = [1, 3, 5, 7, 9, 11]
tree = PersistentSegmentTree(array)

# Query version 0
sum_v0 = tree.query_sum(0, 1, 4)  # Sum in range [1, 4]
min_v0 = tree.query_min(0, 0, 5)  # Min in range [0, 5]
max_v0 = tree.query_max(0, 0, 5)  # Max in range [0, 5]

# Create new version by updating
version_1 = tree.update(0, 2, 10)  # Update index 2 to 10 in version 0

# Query new version
sum_v1 = tree.query_sum(version_1, 1, 4)

# Query old version (unchanged)
sum_v0_again = tree.query_sum(0, 1, 4)  # Same as before

# Get array representation of version
arr_v0 = tree.get_version_array(0)
arr_v1 = tree.get_version_array(version_1)

# Get version count
version_count = tree.get_version_count()
```

### Common Use Cases

**Time-Travel Queries:**
1. Create tree from initial array
2. Perform updates creating new versions
3. Query any historical version

**Version Control:**
1. Each update creates new version
2. Query past states
3. Compare different versions

**Historical Data Analysis:**
1. Track changes over time
2. Query specific time points
3. Analyze evolution of data

## Project Structure

```
persistent-segment-tree/
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

- `src/main.py`: Contains `PersistentSegmentTree` and `SegmentTreeNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Persistent Segment Tree

**Definition:**
A persistent segment tree is a data structure that maintains multiple versions of a segment tree. Each update creates a new version by copying only the nodes that change, preserving all previous versions.

**Properties:**
1. O(log n) query operations
2. O(log n) update operations (creates new version)
3. O(n log n) space for all versions
4. All versions remain accessible

**Key Insight:**
Instead of modifying nodes in place, persistent segment trees create new nodes when updating. Only nodes on the path from root to updated leaf are copied, sharing unchanged subtrees with previous versions.

**Example:**
```
Version 0: [1, 3, 5, 7]
Update index 2 to 10 → Version 1: [1, 3, 10, 7]
Update index 0 to 20 → Version 2: [20, 3, 10, 7]

All versions remain queryable.
```

### Operations

**Query Sum:**
- Time Complexity: O(log n)
- Query sum in range [left, right] for specified version

**Query Min:**
- Time Complexity: O(log n)
- Query minimum in range [left, right] for specified version

**Query Max:**
- Time Complexity: O(log n)
- Query maximum in range [left, right] for specified version

**Update:**
- Time Complexity: O(log n)
- Creates new version with updated value
- Preserves all previous versions

**Get Version Array:**
- Time Complexity: O(n)
- Reconstructs array representation of version

### Edge Cases Handled

- Empty array (rejected)
- Single element array
- Large arrays (tested with 100+ elements)
- Invalid version numbers
- Invalid indices
- Multiple sequential updates
- Querying all versions

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
- Tree creation
- Range sum queries
- Range min/max queries
- Version creation through updates
- Version preservation
- Array reconstruction
- Edge cases (empty, single element, large arrays)
- Invalid input handling

## Troubleshooting

### Common Issues

**High memory usage:**
- Each version stores modified nodes
- Consider version cleanup for very long histories
- Monitor version count

**Incorrect query results:**
- Verify version number is correct
- Check indices are within bounds
- Ensure updates were applied correctly

**Performance issues:**
- Queries are O(log n) - should be fast
- Updates create new nodes - consider space trade-off
- Check for excessive logging

### Error Messages

**"Array cannot be empty"**: Must provide non-empty array when creating tree.

**"Version out of range"**: Version number must be in [0, version_count-1].

**"Index out of range"**: Index must be in [0, n-1] where n is array size.

### Best Practices

1. **Track version numbers** - Keep track of version numbers for queries
2. **Query efficiently** - All queries are O(log n)
3. **Monitor versions** - Each update creates new version
4. **Use appropriate version** - Query the correct version for your needs
5. **Consider space** - Multiple versions use more memory

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Construction | O(n log n) |
| Query Sum | O(log n) |
| Query Min | O(log n) |
| Query Max | O(log n) |
| Update | O(log n) |
| Get Version Array | O(n) |

Where n is the number of elements.

### Space Complexity

- Single version: O(n)
- All versions: O(n log n + m log n) where m is number of updates
- Each update creates O(log n) new nodes

## Applications

- **Time-Travel Queries**: Query historical states of data
- **Version Control**: Track changes over time
- **Rollback Operations**: Access previous versions
- **Competitive Programming**: Problems requiring version queries
- **Data Analysis**: Analyze evolution of data
- **Audit Trails**: Maintain history of changes

## Comparison with Other Structures

**vs. Regular Segment Tree:**
- Persistent: Maintains all versions
- Regular: Only current state

**vs. Array with Snapshots:**
- Persistent: O(log n) queries, O(log n) updates
- Snapshots: O(n) queries, O(n) updates

**vs. Fenwick Tree:**
- Persistent: Supports multiple versions
- Fenwick: Only current version

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
