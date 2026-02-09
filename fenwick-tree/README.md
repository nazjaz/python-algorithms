# Fenwick Tree (Binary Indexed Tree) for Range Sum Queries

A Python implementation of Fenwick tree (Binary Indexed Tree) data structure for efficient range sum queries and point updates. This tool provides O(log n) operations for both updates and queries.

## Project Title and Description

The Fenwick Tree tool implements a Fenwick tree (also known as Binary Indexed Tree) data structure that supports efficient range sum queries and point updates. Fenwick trees are particularly useful when you need to frequently query range sums and update individual elements in an array.

This tool solves the problem of efficiently computing range sums and performing point updates on arrays. Unlike naive approaches that require O(n) time for range queries, Fenwick trees achieve O(log n) time for both updates and queries, making them ideal for problems involving frequent range sum queries and point updates.

**Target Audience**: Competitive programmers, algorithm students, data structure researchers, software engineers working with range queries, and anyone interested in understanding efficient range query data structures.

## Features

- Fenwick tree implementation with O(log n) operations
- Point updates (add delta to element)
- Set value operations (set element to specific value)
- Prefix sum queries (sum from index 0 to i)
- Range sum queries (sum from index i to j)
- Construction from array or empty initialization
- Tree validation
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
cd /path/to/python-algorithms/fenwick-tree
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

Run the main script to see a demonstration of Fenwick tree operations:

```bash
python src/main.py
```

This will:
1. Create a Fenwick tree from an array
2. Display prefix sums
3. Display range sums
4. Perform point updates
5. Set values
6. Validate tree structure

### Programmatic Usage

```python
from src.main import FenwickTree

# Create tree from array
array = [1, 3, 5, 7, 9, 11]
tree = FenwickTree(array=array)

# Or create empty tree
tree = FenwickTree(size=10)

# Point update (add delta)
tree.update(2, 5)  # Add 5 to element at index 2

# Set value
tree.set_value(3, 20)  # Set element at index 3 to 20

# Prefix sum query
prefix = tree.prefix_sum(4)  # Sum from index 0 to 4

# Range sum query
range_sum = tree.range_sum(1, 4)  # Sum from index 1 to 4

# Get value at index
value = tree.get_value(2)

# Get all values
all_values = tree.get_all_values()

# Validate tree
is_valid = tree.is_valid()
```

### Common Use Cases

**Range Sum Queries:**
1. Create tree from array
2. Query range sums efficiently
3. Update elements as needed

**Dynamic Array Sums:**
1. Initialize empty tree
2. Update elements dynamically
3. Query ranges in O(log n) time

**Frequency Counting:**
1. Use tree to count frequencies
2. Update counts efficiently
3. Query frequency ranges

## Project Structure

```
fenwick-tree/
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

- `src/main.py`: Contains `FenwickTree` class with all operations
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Fenwick Tree (Binary Indexed Tree)

**Definition:**
A Fenwick tree is a data structure that supports efficient range sum queries and point updates. It uses a 1-indexed array where each element stores the sum of a specific range based on the binary representation of its index.

**Properties:**
1. O(log n) point updates
2. O(log n) range sum queries
3. O(n) space complexity
4. Uses bit manipulation for efficiency

**Key Insight:**
Each index i is responsible for a range determined by the least significant bit (LSB). The LSB determines how many elements an index covers.

**Example:**
For array [1, 3, 5, 7, 9, 11]:
- Index 1 (binary: 001) covers 1 element
- Index 2 (binary: 010) covers 2 elements
- Index 4 (binary: 100) covers 4 elements

### Operations

**Update:**
- Time Complexity: O(log n)
- Add delta to element at index
- Update all affected tree nodes

**Prefix Sum:**
- Time Complexity: O(log n)
- Sum elements from index 0 to i
- Traverse tree using LSB

**Range Sum:**
- Time Complexity: O(log n)
- Sum elements from index i to j
- Uses prefix_sum(j) - prefix_sum(i-1)

**Set Value:**
- Time Complexity: O(log n)
- Set element to specific value
- Computes delta and calls update

### Edge Cases Handled

- Empty array (rejected)
- Single element array
- Large arrays (tested with 100+ elements)
- Negative values
- Zero values
- Sequential updates
- Invalid indices (rejected)

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
- Tree creation (from array and from size)
- Point updates
- Set value operations
- Prefix sum queries
- Range sum queries
- Edge cases (empty, single element, large arrays, negative values)
- Invalid input handling
- Tree validation

## Troubleshooting

### Common Issues

**Incorrect range sums:**
- Verify tree was built correctly from array
- Check update operations are correct
- Validate tree structure

**Update not working:**
- Ensure index is within bounds
- Check delta value is correct
- Verify tree structure after update

**Performance issues:**
- Fenwick trees are O(log n) - should be fast
- Check for excessive logging
- Verify array size is reasonable

### Error Messages

**"Either size or array must be provided"**: Must provide either size or array when creating tree.

**"Index out of bounds"**: Index must be in range [0, n-1] where n is array size.

**"Left index must be <= right index"**: Range query requires left <= right.

### Best Practices

1. **Use for frequent queries** - Fenwick trees excel with many queries
2. **Initialize properly** - Choose array or size initialization
3. **Validate indices** - Always check bounds before operations
4. **Use range_sum efficiently** - O(log n) for any range
5. **Consider space** - O(n) space for n elements

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Construction | O(n log n) |
| Update | O(log n) |
| Set Value | O(log n) |
| Prefix Sum | O(log n) |
| Range Sum | O(log n) |
| Get Value | O(1) |

Where n is the number of elements.

### Space Complexity

- Tree storage: O(n)
- Original array: O(n)
- Total: O(n)

## Applications

- **Range Sum Queries**: Efficiently query sum of ranges
- **Inversion Count**: Count inversions in arrays
- **Frequency Arrays**: Track and query frequencies
- **Dynamic Arrays**: Maintain sums with updates
- **Competitive Programming**: Common in programming contests
- **Data Structures**: Foundation for advanced structures

## Comparison with Other Structures

**vs. Segment Tree:**
- Fenwick tree: Simpler, less memory, only supports range sum
- Segment tree: More general, supports any associative operation

**vs. Naive Array:**
- Fenwick tree: O(log n) queries and updates
- Naive array: O(n) queries, O(1) updates

**vs. Prefix Sum Array:**
- Fenwick tree: O(log n) updates, O(log n) queries
- Prefix sum: O(n) updates, O(1) queries

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
