# Hash Table Data Structure

A Python implementation of hash table data structure with two collision handling methods: chaining (separate chaining) and open addressing (linear probing). This tool demonstrates how different collision resolution strategies affect hash table performance and behavior.

## Project Title and Description

The Hash Table implementation provides complete hash table data structures with two collision handling approaches. It demonstrates how chaining and open addressing solve the collision problem differently, each with its own advantages and trade-offs in terms of time complexity, space complexity, and implementation complexity.

This tool solves the problem of understanding hash table collision resolution, which is fundamental to understanding how hash-based data structures work in practice. It's essential for implementing dictionaries, sets, and many other data structures.

**Target Audience**: Students learning data structures, developers studying hash tables, educators teaching collision resolution, and anyone interested in understanding how hash tables handle collisions.

## Features

- Hash table with chaining (separate chaining)
- Hash table with open addressing (linear probing)
- Automatic resizing based on load factor
- Insert, get, delete, and contains operations
- Load factor tracking
- Hash table visualization
- Method comparison functionality
- Comprehensive logging
- Detailed analysis reports
- Error handling for edge cases
- Command-line interface
- Demonstration mode with examples

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/hash-table
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

Show hash table visualization:

```bash
python src/main.py --demo --visualize
```

### Compare Methods

Compare chaining and open addressing:

```bash
python src/main.py --demo --method both
```

### Generate Report

Generate detailed comparison report:

```bash
python src/main.py --demo --method both --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Collision handling method (chaining, open_addressing, both)
- `-v, --visualize`: Show hash table visualization
- `-r, --report`: Output path for comparison report
- `--demo`: Run demonstration with example operations

### Common Use Cases

**Learn Hash Table Operations:**
1. Run: `python src/main.py --demo`
2. Review insert, get, delete operations
3. Understand collision handling

**Study Collision Resolution:**
1. Run: `python src/main.py --demo --visualize`
2. Review hash table structure
3. Understand chaining vs open addressing

**Compare Methods:**
1. Run: `python src/main.py --demo --method both`
2. Review performance differences
3. Understand trade-offs

## Project Structure

```
hash-table/
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

- `src/main.py`: Contains `HashTableChaining`, `HashTableOpenAddressing`, and `HashTableVisualizer` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `docs/API.md`: API documentation for the hash tables
- `logs/`: Directory for application log files

## Algorithm Details

### Hash Table Basics

A hash table is a data structure that implements an associative array, mapping keys to values using a hash function.

**Components:**
- **Hash Function**: Maps keys to array indices
- **Buckets/Slots**: Array positions where key-value pairs are stored
- **Collision**: When two keys hash to the same index

### Chaining (Separate Chaining)

Each bucket contains a list (chain) of key-value pairs.

**How It Works:**
1. Hash key to get bucket index
2. If bucket is empty: create new list with key-value pair
3. If bucket has items: add to existing list (handle collision)
4. Search: traverse list in bucket to find key

**Example:**
```
Index 0: (key1:value1) -> (key5:value5)
Index 1: (empty)
Index 2: (key2:value2)
Index 3: (key3:value3) -> (key7:value7) -> (key11:value11)
```

**Advantages:**
- Simple implementation
- No clustering issues
- Can handle high load factors
- Easy deletion

**Disadvantages:**
- Extra memory for pointers/lists
- Cache performance not optimal
- Worst case: all keys hash to same bucket

### Open Addressing (Linear Probing)

All elements stored directly in table, collisions handled by probing.

**How It Works:**
1. Hash key to get initial index
2. If slot is empty: insert key-value pair
3. If slot is occupied: probe to next slot (linear: index + 1)
4. Continue until empty slot found
5. Search: start at hash index, probe until found or empty slot

**Example:**
```
Index 0: (key1:value1)
Index 1: (key5:value5)  [collision, probed from index 0]
Index 2: (key2:value2)
Index 3: (key3:value3)
Index 4: (key7:value7)  [collision, probed from index 3]
```

**Advantages:**
- Better cache performance
- No extra memory for pointers
- Predictable memory usage

**Disadvantages:**
- Clustering can degrade performance
- More complex deletion (tombstone markers)
- Requires careful load factor management
- Worst case: long probe sequences

### Hash Function

Uses Python's built-in `hash()` function with modulo:
```python
hash_value = hash(key) % capacity
```

### Load Factor and Resizing

**Load Factor:** `size / capacity`

**Resizing:**
- When load factor > threshold (0.75), double capacity
- Rehash all existing key-value pairs
- Maintains O(1) average performance

### Time Complexity

| Operation | Chaining (Average) | Chaining (Worst) | Open Addressing (Average) | Open Addressing (Worst) |
|-----------|-------------------|------------------|---------------------------|------------------------|
| Insert | O(1) | O(n) | O(1) | O(n) |
| Get | O(1) | O(n) | O(1) | O(n) |
| Delete | O(1) | O(n) | O(1) | O(n) |

**Worst Case Scenarios:**
- **Chaining**: All keys hash to same bucket
- **Open Addressing**: Clustering causes long probe sequences

### Space Complexity

- **Chaining**: O(n + m) where n = number of elements, m = capacity
- **Open Addressing**: O(m) where m = capacity

## Applications

### Data Structures

- **Dictionaries/Maps**: Key-value storage
- **Sets**: Unique element storage
- **Caches**: Fast lookups
- **Database Indexing**: Fast record access

### Algorithms

- **Frequency Counting**: Count occurrences
- **Lookup Tables**: Fast data retrieval
- **Symbol Tables**: Compiler/interpreter symbol storage
- **Graph Algorithms**: Adjacency representation

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
- Insert operations
- Get operations
- Delete operations
- Contains operations
- Collision handling
- Resizing functionality
- Load factor calculation
- Visualization
- Method comparison

## Troubleshooting

### Common Issues

**High Load Factor:**
- Table may need resizing
- Check load factor threshold
- Consider increasing initial capacity

**Poor Performance:**
- May indicate clustering (open addressing)
- Or many collisions in one bucket (chaining)
- Consider better hash function or different method

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Hash table is full"**: Open addressing table is full. Should not happen with proper resizing. Check load factor management.

**"Configuration file not found"**: Config file doesn't exist at specified path. Check file path or create config.yaml.

### Best Practices

1. **Use chaining** for simplicity and high load factors
2. **Use open addressing** for better cache performance
3. **Monitor load factor** to maintain performance
4. **Choose appropriate capacity** based on expected size
5. **Use visualization** to understand structure: `--visualize`
6. **Compare methods** to see differences: `--method both`

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
