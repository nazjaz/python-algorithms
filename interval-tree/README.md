# Interval Tree for Efficient Range Overlap Queries and Interval Management

A Python implementation of interval tree data structure that efficiently stores intervals and supports range overlap queries. Interval trees use binary search tree structure with max endpoint tracking to achieve O(log n) time complexity for queries.

## Project Title and Description

The Interval Tree tool implements a data structure designed to store intervals and efficiently answer queries about overlapping intervals. Each node in the tree stores an interval and maintains the maximum endpoint in its subtree, enabling efficient pruning during overlap queries.

This tool solves the problem of efficiently managing and querying intervals, which is fundamental in many applications including scheduling, computational geometry, and database systems. The interval tree provides O(log n) time complexity for insertion, deletion, and overlap queries.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding interval management and range query data structures.

## Features

- Interval tree implementation with max endpoint tracking
- O(log n) time complexity for insert, delete, and query operations
- Efficient overlap queries for intervals and points
- Binary search tree structure for interval ordering
- Automatic max endpoint maintenance
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
cd /path/to/python-algorithms/interval-tree
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
- `logging.file`: Path to log file (default: "logs/interval_tree.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/interval_tree.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of interval tree operations:

```bash
python src/main.py
```

This will:
1. Create an interval tree
2. Insert intervals
3. Find overlapping intervals
4. Find intervals containing a point
5. Delete intervals

### Programmatic Usage

```python
from src.main import IntervalTree

# Create interval tree
tree = IntervalTree()

# Insert intervals
tree.insert(10, 20)
tree.insert(15, 25)
tree.insert(5, 15)

# Find overlapping intervals
overlapping = tree.find_overlapping_intervals(12, 18)
for interval in overlapping:
    print(f"Overlaps: {interval}")

# Find intervals containing a point
containing = tree.find_intervals_containing_point(15)
for interval in containing:
    print(f"Contains point: {interval}")

# Delete interval
tree.delete(10, 20)

# Get all intervals
all_intervals = tree.get_all_intervals()
```

### Common Use Cases

**Scheduling Systems:**
1. Store time intervals for appointments
2. Query for conflicts when scheduling new appointments
3. Find all appointments in a time range

**Computational Geometry:**
1. Store line segments or rectangles
2. Query for overlapping geometric objects
3. Efficient range queries in 2D space

**Database Systems:**
1. Index intervals in database
2. Query for overlapping time periods
3. Efficient range queries on interval data

## Project Structure

```
interval-tree/
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

- `src/main.py`: Contains `IntervalTree`, `IntervalNode`, and `Interval` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Interval Tree

**Definition:**
An interval tree is a binary search tree where each node stores an interval [low, high]. The tree is ordered by the low endpoint of intervals. Each node also maintains the maximum endpoint in its subtree, enabling efficient overlap queries.

**Properties:**
1. Binary search tree property: ordered by low endpoint
2. Max endpoint tracking: each node stores max endpoint in subtree
3. O(log n) time complexity for queries
4. Efficient overlap queries

**Structure:**
```
        [15, 20]
       /         \
  [10, 30]    [30, 40]
   /    \
[5, 20] [12, 15]
```

Each node stores:
- Interval [low, high]
- Max endpoint in subtree
- Left and right children

### Max Endpoint Tracking

**Purpose:**
The max endpoint in each node's subtree allows efficient pruning during overlap queries. If the max endpoint in the left subtree is less than the query's low endpoint, the entire left subtree can be skipped.

**Maintenance:**
After each insert or delete operation, max endpoints are updated recursively from leaves to root.

### Overlap Detection

**Interval Overlap:**
Two intervals [a, b] and [c, d] overlap if: a <= d and c <= b

**Point Containment:**
An interval [a, b] contains point p if: a <= p <= b

### Operations

**Insert:**
- Time Complexity: O(log n)
- Insert interval as BST node ordered by low endpoint
- Update max endpoints along path to root

**Delete:**
- Time Complexity: O(log n)
- Delete interval using BST deletion
- Update max endpoints along path to root

**Find Overlapping Intervals:**
- Time Complexity: O(log n + k) where k is number of results
- Use max endpoint to prune subtrees
- Recursively search both subtrees when needed

**Find Intervals Containing Point:**
- Time Complexity: O(log n + k) where k is number of results
- Similar to interval overlap query
- Check if point is within interval range

### Query Algorithm

**Overlap Query Pseudocode:**
```
function search_overlapping(node, query):
    if node is None:
        return
    
    if node.interval overlaps query:
        add node.interval to results
    
    if node.left.max_endpoint >= query.low:
        search_overlapping(node.left, query)
    
    if node.interval.low <= query.high:
        search_overlapping(node.right, query)
```

**Key Insight:**
The max endpoint property allows pruning: if left subtree's max endpoint < query.low, no interval in left subtree can overlap the query.

### Edge Cases Handled

- Empty tree
- Single interval
- Duplicate intervals (rejected)
- Invalid intervals (low > high)
- Adjacent intervals
- Nested intervals
- Single point intervals
- Large number of intervals
- Queries with no results

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
- Interval creation and validation
- Interval overlap detection
- Interval tree creation
- Insert operations
- Delete operations
- Overlap queries
- Point queries
- Edge cases (empty, duplicates, invalid inputs)
- Max endpoint maintenance
- Complex overlap scenarios

## Troubleshooting

### Common Issues

**Queries returning incorrect results:**
- Verify max endpoints are updated correctly
- Check that intervals are inserted in correct order
- Ensure overlap detection logic is correct

**Performance worse than expected:**
- Interval trees have O(log n) average case
- Worst case can be O(n) if tree is unbalanced
- Consider using balanced BST variant for guaranteed O(log n)

**Invalid interval errors:**
- Ensure low <= high for all intervals
- Validate input before insertion

### Error Messages

**"Invalid interval: low > high"**: Attempted to create interval with low > high.

**"Interval already exists"**: Attempted to insert duplicate interval.

**"Interval not found"**: Attempted to delete non-existent interval.

### Best Practices

1. **Validate intervals** - Always ensure low <= high
2. **Handle duplicates** - Check for existing intervals before insertion
3. **Use for range queries** - Interval trees excel at overlap queries
4. **Consider balancing** - For guaranteed O(log n), use balanced BST
5. **Monitor performance** - Track query times for large datasets

## Performance Characteristics

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Find Overlapping Intervals | O(log n + k) | O(n + k) |
| Find Intervals Containing Point | O(log n + k) | O(n + k) |
| Get All Intervals | O(n) | O(n) |

Where n is the number of intervals and k is the number of results.

### Space Complexity

- Node storage: O(n)
- Total: O(n)

### Query Performance

- Overlap queries: O(log n + k) where k is number of overlapping intervals
- Point queries: O(log n + k) where k is number of containing intervals
- Max endpoint pruning reduces search space significantly

## Applications

- **Scheduling Systems**: Find conflicting appointments or time slots
- **Computational Geometry**: Query overlapping line segments or rectangles
- **Database Indexing**: Efficient range queries on interval data
- **Genomic Analysis**: Find overlapping gene regions or sequences
- **Network Routing**: Manage overlapping time windows or routes
- **Resource Allocation**: Find overlapping resource reservations
- **Event Management**: Query events in time ranges

## Comparison with Other Data Structures

**Interval Tree:**
- O(log n) queries
- Efficient overlap detection
- Requires balanced BST for guaranteed performance
- Good for interval-specific queries

**Segment Tree:**
- O(log n) queries
- Requires fixed range
- More memory overhead
- Better for range sum/max queries

**Brute Force:**
- O(n) queries
- Simple implementation
- No preprocessing needed
- Inefficient for large datasets

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
