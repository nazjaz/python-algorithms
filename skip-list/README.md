# Skip List Data Structure with Probabilistic Balancing

A Python implementation of skip list data structure as an alternative to balanced trees. Skip lists use probabilistic balancing to achieve O(log n) average-case performance for search, insertion, and deletion operations.

## Project Title and Description

The Skip List tool implements a skip list data structure that provides an alternative to balanced trees. Skip lists use probabilistic balancing through random level assignment, eliminating the need for complex rebalancing operations while maintaining O(log n) average-case performance.

This tool solves the problem of maintaining a sorted data structure with efficient operations without the complexity of balanced trees. Skip lists are simpler to implement than balanced trees while providing similar performance characteristics, making them ideal for applications requiring sorted data with fast operations.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding probabilistic data structures and alternatives to balanced trees.

## Features

- Skip list implementation with probabilistic balancing
- O(log n) average-case search, insert, and delete operations
- Configurable maximum level and probability
- Range queries
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
cd /path/to/python-algorithms/skip-list
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

Run the main script to see a demonstration of skip list operations:

```bash
python src/main.py
```

This will:
1. Create a skip list
2. Insert keys
3. Search for keys
4. Perform range queries
5. Delete keys
6. Display min/max keys

### Programmatic Usage

```python
from src.main import SkipList

# Create skip list
skip_list = SkipList(max_level=16, probability=0.5)

# Insert keys
skip_list.insert(10, 20)
skip_list.insert(20, 40)
skip_list.insert(30, 60)

# Search
found, value = skip_list.search(20)  # Returns (True, 40)

# Delete
skip_list.delete(20)

# Range query
range_items = skip_list.get_range(10, 30)

# Get all keys
all_keys = skip_list.get_all_keys()  # Returns sorted list

# Get min/max
min_key = skip_list.get_min_key()
max_key = skip_list.get_max_key()
```

### Common Use Cases

**Sorted Data Structure:**
1. Insert keys in any order
2. Keys automatically maintained in sorted order
3. Efficient search, insert, delete operations

**Range Queries:**
1. Insert data
2. Query ranges efficiently
3. Get all items in specified range

**Alternative to Balanced Trees:**
1. Use skip list instead of AVL/Red-Black trees
2. Simpler implementation
3. Similar performance characteristics

## Project Structure

```
skip-list/
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

- `src/main.py`: Contains `SkipList` and `SkipListNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Skip List

**Definition:**
A skip list is a probabilistic data structure that allows O(log n) average-case search, insertion, and deletion operations. It consists of multiple levels of sorted linked lists, with higher levels containing fewer elements.

**Properties:**
1. Multiple levels of linked lists
2. Bottom level contains all elements in sorted order
3. Higher levels contain subsets of elements
4. Probabilistic level assignment
5. O(log n) average-case operations

**Structure:**
```
Level 3:  -inf -> [10] -> [50] -> +inf
Level 2:  -inf -> [10] -> [30] -> [50] -> +inf
Level 1:  -inf -> [10] -> [20] -> [30] -> [40] -> [50] -> +inf
Level 0:  -inf -> [10] -> [20] -> [30] -> [40] -> [50] -> +inf
```

**Key Insight:**
Each element has a random level assigned probabilistically. Higher-level elements act as "express lanes" allowing faster traversal to target elements.

### Probabilistic Balancing

**Level Assignment:**
- Start at level 0
- With probability p, increase level
- Continue until random() >= p or max_level reached
- Expected level: 1/(1-p)

**Advantages:**
- No explicit rebalancing needed
- Simpler than balanced trees
- Good average-case performance

**Disadvantages:**
- Worst-case can be O(n)
- Requires random number generation
- Space overhead for multiple levels

### Operations

**Search:**
- Time Complexity: O(log n) average, O(n) worst-case
- Start from top level, move right if next key < target, else go down
- Continue until found or bottom level reached

**Insert:**
- Time Complexity: O(log n) average, O(n) worst-case
- Find insertion position
- Assign random level to new node
- Insert at all levels up to assigned level

**Delete:**
- Time Complexity: O(log n) average, O(n) worst-case
- Find node to delete
- Remove from all levels
- Update level if necessary

### Edge Cases Handled

- Empty skip list
- Single element
- Duplicate keys (rejected)
- Large number of elements
- Sequential insertions and deletions
- Invalid parameters (rejected)

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
- Skip list creation
- Insert operations
- Search operations
- Delete operations
- Range queries
- Min/max operations
- Edge cases (empty, single element, duplicates)
- Invalid input handling
- Validation

## Troubleshooting

### Common Issues

**Performance worse than expected:**
- Skip lists have O(n) worst-case
- Consider increasing max_level
- Adjust probability parameter

**High memory usage:**
- Each node stores multiple forward pointers
- Consider reducing max_level
- Monitor actual level distribution

**Incorrect search results:**
- Verify skip list structure is valid
- Check that keys remain sorted
- Ensure proper level assignment

### Error Messages

**"Max level must be at least 1"**: Maximum level must be positive integer.

**"Probability must be between 0 and 1"**: Probability must be in range (0, 1).

**"Key already exists"**: Attempted to insert duplicate key.

### Best Practices

1. **Choose appropriate max_level** - Higher for larger datasets
2. **Set probability correctly** - 0.5 is standard, adjust for your needs
3. **Monitor performance** - Skip lists have probabilistic performance
4. **Validate structure** - Use is_valid() to check correctness
5. **Consider alternatives** - For guaranteed O(log n), use balanced trees

## Performance Characteristics

### Time Complexity

| Operation | Average Case | Worst Case |
|-----------|-------------|------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Range Query | O(log n + k) | O(n) |
| Min/Max | O(log n) | O(n) |

Where n is the number of elements and k is the number of elements in range.

### Space Complexity

- Node storage: O(n) average, O(n log n) worst-case
- Forward pointers: O(n) average
- Total: O(n) average, O(n log n) worst-case

### Expected Level Distribution

With probability p = 0.5:
- Level 0: 50% of nodes
- Level 1: 25% of nodes
- Level 2: 12.5% of nodes
- And so on...

## Applications

- **Sorted Sets**: Maintain sorted collections efficiently
- **Databases**: Index structures
- **Priority Queues**: Alternative implementation
- **Range Queries**: Efficient range operations
- **Competitive Programming**: Simpler than balanced trees
- **Caching**: LRU cache implementations

## Comparison with Balanced Trees

**Skip Lists:**
- Simpler implementation
- Probabilistic balancing
- O(log n) average-case
- O(n) worst-case

**Balanced Trees (AVL/Red-Black):**
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
