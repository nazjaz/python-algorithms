# Segment Tree Data Structure

A Python implementation of segment tree data structure for efficient range queries and point/range updates with lazy propagation. This tool provides O(log n) operations for range queries and updates on arrays.

## Project Title and Description

The Segment Tree tool implements a binary tree data structure that allows efficient range queries (sum, min, max) and point/range updates in O(log n) time. It includes lazy propagation for efficient range updates, making it ideal for problems requiring frequent range operations.

This tool solves the problem of efficiently performing range queries and updates on arrays. Segment trees are widely used in competitive programming, database systems, and applications requiring fast range operations.

**Target Audience**: Students learning advanced data structures, competitive programmers, developers studying range query problems, educators teaching computer science concepts, and anyone interested in understanding efficient range operations and lazy propagation.

## Features

- Segment tree implementation with O(log n) operations
- Range queries (sum, min, max)
- Point updates
- Range updates with lazy propagation
- Support for multiple operations (sum, min, max)
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
cd /path/to/python-algorithms/segment-tree
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

### Create Segment Tree

Create segment tree with array:

```bash
python src/main.py 1 2 3 4 5 --operation sum
```

### Query Range

Query range [left, right]:

```bash
python src/main.py 1 2 3 4 5 --operation sum --query 0 4
```

### Update Point

Update single point:

```bash
python src/main.py 1 2 3 4 5 --operation sum --update-point 2 10
```

### Update Range

Update range with lazy propagation:

```bash
python src/main.py 1 2 3 4 5 --operation sum --update-range 1 3 5
```

### Display Array

Display current array:

```bash
python src/main.py 1 2 3 4 5 --operation sum --array
```

### Different Operations

Use min operation:

```bash
python src/main.py 1 2 3 4 5 --operation min --query 0 4
```

Use max operation:

```bash
python src/main.py 1 2 3 4 5 --operation max --query 0 4
```

### Command-Line Arguments

- `numbers`: (Required) Numbers in the array (space-separated)
- `-o, --operation`: Operation type - sum, min, or max (default: sum)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-q, --query`: Query range [left, right] (two integers)
- `-u, --update-point`: Update point at index with value (index, value)
- `-r, --update-range`: Update range [left, right] with value (left, right, value)
- `-a, --array`: Display current array

### Common Use Cases

**Range Sum Queries:**
1. Create tree: `python src/main.py 1 2 3 4 5 --operation sum`
2. Query range: `python src/main.py 1 2 3 4 5 --operation sum --query 1 3`
3. Get sum of subarray

**Range Minimum Queries:**
1. Create tree: `python src/main.py 1 2 3 4 5 --operation min`
2. Query range: `python src/main.py 1 2 3 4 5 --operation min --query 1 3`
3. Get minimum in range

**Range Updates:**
1. Create tree: `python src/main.py 1 2 3 4 5 --operation sum`
2. Update range: `python src/main.py 1 2 3 4 5 --operation sum --update-range 1 3 5`
3. All elements in range updated efficiently

**Point Updates:**
1. Create tree: `python src/main.py 1 2 3 4 5 --operation sum`
2. Update point: `python src/main.py 1 2 3 4 5 --operation sum --update-point 2 10`
3. Single element updated

## Project Structure

```
segment-tree/
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

- `src/main.py`: Contains the `SegmentTree` class
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Segment Tree

**Definition:**
A segment tree is a binary tree data structure used for storing information about intervals/segments. It allows querying which segments contain a given point and updating segments efficiently.

**Structure:**
- Binary tree where each node represents a segment
- Root represents entire array [0, n-1]
- Each leaf represents single element
- Internal nodes represent segments

**Example:**
```
Array: [1, 2, 3, 4]
Tree structure (for sum):
        [0-3: 10]
       /         \
  [0-1: 3]    [2-3: 7]
  /     \      /     \
[0:1] [1:2] [2:3] [3:4]
```

**Applications:**
- Range sum/min/max queries
- Range updates
- Inversion count
- Longest increasing subsequence
- Range GCD/LCM queries

### Lazy Propagation

**Definition:**
Lazy propagation is an optimization technique that defers updates until they are needed. Instead of updating all nodes immediately, updates are stored in a lazy array and applied when querying.

**How It Works:**
1. When updating a range, mark nodes as lazy
2. Store update value in lazy array
3. When querying, push lazy values to children
4. Apply lazy values when needed

**Benefits:**
- Reduces update complexity from O(n log n) to O(log n)
- Essential for efficient range updates
- Maintains O(log n) query time

### Operations

**Build:**
- Time Complexity: O(n)
- Space Complexity: O(n)
- Constructs tree from array

**Query:**
- Time Complexity: O(log n)
- Space Complexity: O(log n) for recursion
- Returns result for range [left, right]

**Point Update:**
- Time Complexity: O(log n)
- Space Complexity: O(log n) for recursion
- Updates single element

**Range Update:**
- Time Complexity: O(log n) with lazy propagation
- Space Complexity: O(log n) for recursion
- Updates all elements in range

### Edge Cases Handled

- Empty array (error)
- Single element array
- Invalid indices (out of bounds)
- Invalid ranges (left > right)
- Large arrays
- Multiple consecutive updates
- Mixed queries and updates

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
- Segment tree construction
- Range queries (sum, min, max)
- Point updates
- Range updates with lazy propagation
- Edge cases (empty array, invalid indices, single element)
- Performance comparison functionality
- Error handling
- Report generation
- Input validation

## Troubleshooting

### Common Issues

**ValueError: Array cannot be empty:**
- Array must have at least one element
- Check input array

**ValueError: Invalid range:**
- Indices must be within [0, n-1]
- Left must be <= right
- Check index values

**ValueError: Invalid index:**
- Index must be within [0, n-1]
- Check index value

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Array cannot be empty"**: Array must have at least one element.

**"Invalid range: [left, right]"**: Range indices must be valid and left <= right.

**"Invalid index: X"**: Index must be within array bounds.

**"Invalid operation"**: Operation must be one of: sum, min, max.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use segment tree for range operations** - More efficient than naive approach
2. **Use lazy propagation for range updates** - Essential for efficiency
3. **Choose appropriate operation** - sum, min, or max based on needs
4. **Handle edge cases** - Empty arrays, invalid indices
5. **Consider space complexity** - Segment tree uses O(n) space
6. **Use for frequent queries** - Segment tree excels with many queries
7. **Understand lazy propagation** - Critical for range updates

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
