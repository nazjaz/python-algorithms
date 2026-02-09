# Linked List Data Structure

A Python implementation of a linked list data structure with insertion, deletion, and traversal operations. This tool includes comprehensive visualization capabilities to show the structure and operations of the linked list, making it ideal for understanding how linked lists work.

## Project Title and Description

The Linked List implementation provides a complete singly linked list data structure with all fundamental operations. It demonstrates how linked lists use nodes connected by pointers, enabling dynamic memory allocation and efficient insertion/deletion operations.

This tool solves the problem of understanding linked list data structures by providing a complete implementation with visualization, making it ideal for educational purposes, algorithm study, and as a foundation for more complex data structures.

**Target Audience**: Students learning data structures, developers studying linked list implementations, educators teaching computer science concepts, and anyone interested in understanding how linked lists work.

## Features

- Complete linked list implementation
- Insertion operations (beginning, end, at position)
- Deletion operations (beginning, end, at position, by value)
- Traversal operations
- Search functionality
- Reverse operation
- Comprehensive visualization
- Operation history tracking
- Detailed reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/linked-list
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

Run demonstration with example operations:

```bash
python src/main.py --demo
```

### With Visualization

Show visualization of linked list:

```bash
python src/main.py --demo --visualize
```

### Detailed Visualization

Show detailed visualization with node information:

```bash
python src/main.py --demo --detailed
```

### Generate Report

Generate detailed operations report:

```bash
python src/main.py --demo --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-v, --visualize`: Show visualization of linked list
- `-d, --detailed`: Show detailed visualization
- `-r, --report`: Output path for operations report
- `--demo`: Run demonstration with example operations

### Common Use Cases

**Learn Linked List Operations:**
1. Run: `python src/main.py --demo`
2. Review insertion operations
3. Review deletion operations
4. Understand traversal

**Study Visualization:**
1. Run: `python src/main.py --demo --visualize`
2. Review linked list structure
3. Understand node connections
4. See operation effects

**Generate Documentation:**
1. Run: `python src/main.py --demo --report report.txt`
2. Review detailed report
3. Study operation history

## Project Structure

```
linked-list/
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

- `src/main.py`: Contains the `Node`, `LinkedList`, and `LinkedListVisualizer` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the linked list
- `logs/`: Directory for application log files

## Algorithm Details

### Linked List Structure

A linked list is a linear data structure where elements are stored in nodes. Each node contains:
- **Data**: The value stored in the node
- **Next**: Pointer to the next node (or NULL for the last node)

**Visual Representation:**
```
[Head] -> [Node1] -> [Node2] -> [Node3] -> NULL
          10         20         30
```

### Operations

#### Insertion Operations

**1. Insert at Beginning (O(1)):**
- Create new node
- Set new node's next to current head
- Set head to new node

**2. Insert at End (O(n)):**
- Create new node
- Traverse to last node
- Set last node's next to new node

**3. Insert at Position (O(n)):**
- Create new node
- Traverse to position - 1
- Set new node's next to current node's next
- Set current node's next to new node

#### Deletion Operations

**1. Delete at Beginning (O(1)):**
- Store head's data
- Set head to head's next
- Return stored data

**2. Delete at End (O(n)):**
- Traverse to second-to-last node
- Store last node's data
- Set second-to-last node's next to NULL
- Return stored data

**3. Delete at Position (O(n)):**
- Traverse to position - 1
- Store next node's data
- Set current node's next to next node's next
- Return stored data

**4. Delete by Value (O(n)):**
- Traverse list searching for value
- When found, update previous node's next
- Return success status

#### Traversal Operation

**Traverse (O(n)):**
- Start at head
- Visit each node
- Collect data values
- Return list of values

### Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| Insert at beginning | O(1) |
| Insert at end | O(n) |
| Insert at position | O(n) |
| Delete at beginning | O(1) |
| Delete at end | O(n) |
| Delete at position | O(n) |
| Delete by value | O(n) |
| Search | O(n) |
| Traverse | O(n) |
| Reverse | O(n) |

### Space Complexity

- **O(n)**: Space required for n nodes
- Each node stores data and a pointer

### Properties

- **Dynamic Size**: No fixed capacity, grows as needed
- **Memory Efficient**: Only uses space for actual data
- **Insertion/Deletion**: Efficient at beginning (O(1))
- **No Random Access**: Must traverse to access elements
- **Sequential Access**: Elements accessed in order

### Advantages

- Dynamic size (no fixed capacity)
- Efficient insertion/deletion at beginning
- Memory efficient (only uses needed space)
- Easy to implement
- No memory waste

### Disadvantages

- No random access (must traverse)
- Extra memory for pointers
- Cache performance not optimal
- More complex than arrays for simple cases

## Visualization Features

The visualizer provides:

1. **Basic Visualization**: Shows linked list structure with arrows
   ```
   [0] 10 -> [1] 20 -> [2] 30 -> NULL
   ```

2. **Detailed Visualization**: Shows node details including:
   - Position in list
   - Node data
   - Next node reference
   - List size
   - Head pointer

3. **Operation History**: Tracks all operations with:
   - Operation type
   - List state after operation
   - Operation parameters
   - Success status

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
- Node creation and representation
- Linked list initialization
- All insertion operations
- All deletion operations
- Search and traversal
- Visualization
- Edge cases (empty list, single node, invalid positions)
- Reverse operation
- List conversion operations

## Troubleshooting

### Common Issues

**IndexError or Invalid Position:**
- Position must be within valid range [0, size)
- Check position before operation
- Handle empty list cases

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Check that config.yaml exists and is valid YAML
- Verify logging file path is writable
- Check file permissions

### Error Messages

**"Cannot delete from empty list"**: Attempted deletion from empty list. Check if list is empty before deletion.

**"Invalid position"**: Position is out of valid range. Ensure position is within [0, size).

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use visualization** to understand structure: `--visualize`
2. **Generate reports** for documentation: `--report report.txt`
3. **Check logs** to understand operations
4. **Use demonstration mode** to see examples: `--demo`
5. **Handle edge cases** (empty list, single node)
6. **Validate positions** before operations

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
