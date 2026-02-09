# Persistent Data Structures (Persistent Arrays, Lists) with Path Copying Technique

A Python implementation of persistent arrays and lists using path copying technique. Persistent data structures maintain all previous versions when modified, enabling efficient time-travel queries and undo operations. Path copying achieves O(log n) time and space complexity per operation.

## Project Title and Description

The Persistent Data Structures tool implements arrays and lists that preserve all previous versions when modified. Using path copying technique, modifications create new versions by copying only the path from root to the modified node, while sharing unchanged subtrees.

This tool solves the problem of maintaining multiple versions of data structures efficiently, which is fundamental in many applications including version control systems, undo/redo functionality, functional programming, and time-travel queries. Path copying provides O(log n) time and space complexity per operation.

**Target Audience**: Algorithm students, competitive programmers, data structure researchers, software engineers, and anyone interested in understanding persistent data structures and functional programming techniques.

## Features

- Persistent array implementation with path copying
- Persistent list implementation with path copying
- O(log n) time and space complexity per operation
- All previous versions remain accessible
- Get, set, and append operations
- Version management and querying
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
cd /path/to/python-algorithms/persistent-data-structures
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
- `logging.file`: Path to log file (default: "logs/persistent_data_structures.log")

### Example Configuration

```yaml
logging:
  level: "INFO"
  file: "logs/persistent_data_structures.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Run the main script to see a demonstration of persistent data structures:

```bash
python src/main.py
```

This will:
1. Create persistent arrays and lists
2. Perform modifications creating new versions
3. Demonstrate that old versions remain intact
4. Show version management

### Programmatic Usage

```python
from src.main import PersistentArray, PersistentList

# Persistent Array
arr = PersistentArray([1, 2, 3, 4, 5])
v0 = arr.get_current_version()

# Create new version by modifying
v1 = arr.set(v0, 2, 10)

# Old version still accessible
print(arr.get(v0, 2))  # 3
print(arr.get(v1, 2))  # 10

# Persistent List
lst = PersistentList([10, 20, 30])
v0 = lst.get_current_version()

# Append creates new version
v1 = lst.append(v0, 40)

# Old version still accessible
print(lst.get_size(v0))  # 3
print(lst.get_size(v1))  # 4
```

### Common Use Cases

**Version Control:**
1. Maintain multiple versions of data
2. Time-travel queries
3. Undo/redo functionality

**Functional Programming:**
1. Immutable data structures
2. Persistent state management
3. Functional data structures

**Competitive Programming:**
1. Efficient version management
2. Time-travel queries
3. Persistent state problems

## Project Structure

```
persistent-data-structures/
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

- `src/main.py`: Contains `PersistentArray`, `PersistentList`, and `PersistentNode` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Path Copying Technique

**Definition:**
Path copying is a technique for creating persistent data structures where modifications create new versions by copying only the path from root to the modified node, while sharing unchanged subtrees.

**Properties:**
1. O(log n) time per operation
2. O(log n) space per operation
3. All versions remain accessible
4. Unchanged subtrees are shared

**Structure:**
```
        Root (Version 0)
       /              \
   Left            Right
   /    \          /    \
Leaf1  Leaf2    Leaf3  Leaf4

After modifying Leaf3:
        Root (Version 1) [NEW]
       /              \
   Left [SHARED]   Right [NEW]
   /    \          /    \
Leaf1  Leaf2    Leaf3  Leaf4
[SHARED][SHARED] [NEW] [SHARED]
```

### Tree Structure

**Binary Tree:**
- Each node represents a range
- Leaf nodes store actual values
- Internal nodes split ranges
- Balanced tree structure

**Path Copying:**
- When modifying, copy path from root
- Share unchanged subtrees
- Create new root for new version

### Operations

**Get:**
- Time Complexity: O(log n)
- Traverse tree to find element
- No modification, no copying

**Set:**
- Time Complexity: O(log n)
- Copy path from root to modified node
- Create new version
- Share unchanged subtrees

**Append (List only):**
- Time Complexity: O(log n)
- Add new element at end
- Copy path to insertion point
- Create new version

### Edge Cases Handled

- Empty arrays/lists
- Single element
- Out of bounds indices
- Invalid versions
- Multiple consecutive modifications
- Large sequences

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
- PersistentNode creation and operations
- PersistentArray operations
- PersistentList operations
- Get, set, append operations
- Version management
- Edge cases (empty, single element, invalid inputs)
- Multiple versions and modifications

## Troubleshooting

### Common Issues

**Incorrect version results:**
- Verify version numbers are correct
- Check that operations completed successfully
- Ensure old versions are not modified

**Performance issues:**
- Path copying is O(log n) per operation
- For many operations, space usage grows
- Consider alternatives for very large sequences

**Memory issues:**
- Each version uses O(log n) space
- Many versions may use significant memory
- Consider version cleanup strategies

### Error Messages

**"Version X does not exist"**: Invalid version number.

**"Index X out of bounds"**: Index not in valid range.

**"Array/List is empty"**: Attempted operation on empty structure.

### Best Practices

1. **Use for version management** - Persistent structures excel with multiple versions
2. **Monitor memory** - Many versions use significant space
3. **Validate inputs** - Check versions and indices before operations
4. **Consider alternatives** - For single version, regular arrays are better
5. **Version cleanup** - Consider removing old versions if not needed

## Performance Characteristics

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Get | O(log n) |
| Set | O(log n) |
| Append | O(log n) |
| Get Size | O(1) |

Where n is the size of the array/list.

### Space Complexity

- Per operation: O(log n)
- Total for k operations: O(k log n)
- Unchanged subtrees are shared
- Only modified paths are copied

### Query Performance

- Get: O(log n) - traverse tree
- Set: O(log n) - copy path
- Append: O(log n) - add at end
- Optimal for version management

## Applications

- **Version Control**: Maintain multiple versions of data
- **Undo/Redo**: Efficient undo/redo functionality
- **Functional Programming**: Immutable data structures
- **Time-Travel Queries**: Query past states
- **Competitive Programming**: Persistent state problems

## Comparison with Other Methods

**Path Copying:**
- O(log n) per operation
- O(log n) space per operation
- All versions accessible
- Good for moderate number of versions

**Full Copying:**
- O(n) per operation
- O(n) space per operation
- Simple but inefficient
- Not recommended

**Fat Nodes:**
- O(1) per operation
- O(1) space per operation
- More complex implementation
- Better for many versions

**Copy-on-Write:**
- O(log n) per operation
- O(log n) space per operation
- Similar to path copying
- Different implementation

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
