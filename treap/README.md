# Treap (Tree + Heap) Data Structure with Randomized Balancing

A Python implementation of treap data structure that combines binary search tree and heap properties. Treaps use randomized priorities to maintain balanced structure, achieving O(log n) expected time complexity for all operations.

## Project Title and Description

The Treap tool implements a treap (tree + heap) data structure that combines the properties of a binary search tree and a max heap. Each node has both a key (for BST ordering) and a priority (for heap ordering). Randomized priorities ensure balanced tree structure without explicit rebalancing operations.

This tool solves the problem of maintaining a balanced binary search tree without complex rebalancing algorithms. Treaps are simpler to implement than AVL trees or red-black trees while providing similar performance characteristics through randomized priorities.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding randomized data structures and alternatives to balanced trees.

## Features

- Treap implementation with randomized priorities
- O(log n) expected time complexity for all operations
- Binary search tree property (keys in sorted order)
- Max heap property (parent priority > children priorities)
- Insert, delete, and search operations
- Split and merge operations
- Min/max key retrieval
- Sorted key iteration
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
cd /path/to/python-algorithms/treap
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

Run the main script to see a demonstration of treap operations:

```bash
python src/main.py
```

This will:
1. Create a treap
2. Insert keys
3. Search for keys
4. Split treap
5. Merge treaps
6. Delete keys
7. Display min/max keys

### Programmatic Usage

```python
from src.main import Treap

# Create treap
treap = Treap()

# Insert keys
treap.insert(10)
treap.insert(20)
treap.insert(30)

# Search
found = treap.search(20)  # Returns True

# Delete
treap.delete(20)

# Get all keys
all_keys = treap.get_all_keys()  # Returns sorted list

# Split treap
left, right = treap.split(25)

# Merge treaps
merged = left.merge(right)

# Get min/max
min_key = treap.get_min_key()
max_key = treap.get_max_key()
```

### Common Use Cases

**Sorted Data Structure:**
1. Insert keys in any order
2. Keys automatically maintained in sorted order
3. Efficient search, insert, delete operations

**Split and Merge Operations:**
1. Split treap at key
2. Perform operations on subtrees
3. Merge treaps back together

**Alternative to Balanced Trees:**
1. Use treap instead of AVL/Red-Black trees
2. Simpler implementation
3. Similar performance through randomization

## Project Structure

```
treap/
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

- `src/main.py`: Contains `Treap` and `TreapNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Treap

**Definition:**
A treap is a binary search tree where each node has both a key (for BST ordering) and a priority (for heap ordering). The tree satisfies both BST property (left < node < right by key) and max heap property (parent priority > children priorities).

**Properties:**
1. Binary search tree property: keys in sorted order
2. Max heap property: priorities maintain heap structure
3. Randomized priorities for balancing
4. O(log n) expected time complexity

**Structure:**
```
        [30, 50]
       /        \
  [20, 40]    [40, 30]
   /    \       /    \
[10,60] [25,20] [35,10] [50,5]
```

**Key Insight:**
Randomized priorities ensure balanced tree structure. When inserting, maintain BST property, then rotate to maintain heap property. This results in expected O(log n) height.

### Randomized Balancing

**Priority Assignment:**
- Each node gets random priority
- Priorities typically in range [1, 10^9]
- Randomization ensures balanced structure

**Advantages:**
- No explicit rebalancing needed
- Simpler than AVL/Red-Black trees
- Good average-case performance

**Disadvantages:**
- Worst-case can be O(n) height
- Requires random number generation
- Probabilistic guarantees

### Operations

**Insert:**
- Time Complexity: O(log n) expected
- Insert as BST, then rotate up to maintain heap property

**Delete:**
- Time Complexity: O(log n) expected
- Rotate down to leaf, then remove

**Search:**
- Time Complexity: O(log n) expected
- Standard BST search

**Split:**
- Time Complexity: O(log n) expected
- Split treap at key into two treaps

**Merge:**
- Time Complexity: O(log n) expected
- Merge two treaps (all keys in left < all keys in right)

### Rotations

**Right Rotation:**
- Used when left child has higher priority
- Maintains BST and heap properties

**Left Rotation:**
- Used when right child has higher priority
- Maintains BST and heap properties

### Edge Cases Handled

- Empty treap
- Single element
- Duplicate keys (rejected)
- Large number of elements
- Sequential insertions and deletions
- Split at boundaries
- Merge with empty treap

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
- Treap creation
- Insert operations
- Search operations
- Delete operations
- Split and merge operations
- Min/max operations
- Edge cases (empty, single element, duplicates)
- Invalid input handling
- Validation

## Troubleshooting

### Common Issues

**Performance worse than expected:**
- Treaps have O(n) worst-case height
- Consider using larger priority range
- Monitor actual tree height

**Incorrect search results:**
- Verify treap structure is valid
- Check that keys remain sorted
- Ensure proper rotation during insert/delete

**Split/merge not working:**
- Verify split key is valid
- Check that merge treaps have correct key ranges
- Ensure all keys in left < all keys in right for merge

### Error Messages

**"Key already exists"**: Attempted to insert duplicate key.

**"Key not found"**: Attempted to delete non-existent key.

### Best Practices

1. **Use for balanced BST** - Treaps provide good average-case performance
2. **Leverage split/merge** - Powerful operations for range queries
3. **Monitor performance** - Treaps have probabilistic performance
4. **Validate structure** - Use is_valid() to check correctness
5. **Consider alternatives** - For guaranteed O(log n), use AVL/Red-Black trees

## Performance Characteristics

### Time Complexity

| Operation | Expected Case | Worst Case |
|-----------|--------------|------------|
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Search | O(log n) | O(n) |
| Split | O(log n) | O(n) |
| Merge | O(log n) | O(n) |
| Min/Max | O(log n) | O(n) |

Where n is the number of elements.

### Space Complexity

- Node storage: O(n)
- Total: O(n)

### Expected Height

With randomized priorities:
- Expected height: O(log n)
- Probability of height > 3 log n: O(1/n^2)

## Applications

- **Sorted Sets**: Maintain sorted collections efficiently
- **Priority Queues**: Alternative implementation
- **Range Queries**: Split and merge enable range operations
- **Competitive Programming**: Simpler than balanced trees
- **Database Indexing**: Efficient key-value storage
- **Interval Trees**: Base structure for interval operations

## Comparison with Balanced Trees

**Treaps:**
- Simpler implementation
- Randomized balancing
- O(log n) expected
- O(n) worst-case

**AVL/Red-Black Trees:**
- More complex implementation
- Deterministic balancing
- O(log n) guaranteed
- More code to maintain

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
