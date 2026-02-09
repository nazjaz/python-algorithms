# Queue Data Structure

A Python implementation of queue data structure using both array-based and linked list approaches with comprehensive performance analysis. This tool provides complete queue operations and detailed performance comparison.

## Project Title and Description

The Queue Data Structure tool implements queues using two different approaches: array-based (using Python list) and linked list-based. It provides comprehensive performance analysis, detailed logging, and practical demonstrations to help understand the trade-offs between different implementation strategies.

This tool solves the problem of understanding queue data structures and their implementations by providing side-by-side performance comparison and detailed analysis of different implementation approaches, making it ideal for educational purposes and algorithm analysis.

**Target Audience**: Students learning data structures, developers studying queue implementations, educators teaching computer science concepts, and anyone interested in understanding queues and performance analysis.

## Features

- Array-based queue implementation
- Linked list-based queue implementation
- Complete queue operations (enqueue, dequeue, front, rear)
- Performance comparison and analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Error handling for edge cases
- Interactive demonstrations

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/queue-data-structure
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

### Queue Operations Demonstration

Demonstrate basic queue operations:

```bash
python src/main.py --demo
```

### Use Specific Implementation

Use array-based queue:

```bash
python src/main.py --implementation array
```

Use linked list-based queue:

```bash
python src/main.py --implementation linked
```

Use both implementations:

```bash
python src/main.py --implementation both
```

### Performance Comparison

Compare implementations with custom operations:

```bash
python src/main.py --compare --operations "enqueue 1" "enqueue 2" "dequeue" "enqueue 3" "dequeue"
```

Compare with multiple iterations:

```bash
python src/main.py --compare --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py --compare --report report.txt
```

### Command-Line Arguments

- `-c, --config`: Path to configuration file (default: config.yaml)
- `-i, --implementation`: Queue implementation - array, linked, both, or compare (default: both)
- `--operations`: Operations to perform (e.g., 'enqueue 1' 'enqueue 2' 'dequeue')
- `--iterations`: Number of iterations for performance testing (default: 1)
- `-r, --report`: Output path for performance report
- `--demo`: Run queue operations demonstration

### Common Use Cases

**Learn Queue Operations:**
1. Run: `python src/main.py --demo`
2. Observe enqueue and dequeue operations
3. Understand FIFO behavior

**Compare Implementations:**
1. Run: `python src/main.py --compare`
2. Review timing for each implementation
3. Understand performance differences

**Performance Analysis:**
1. Test with different operation patterns
2. Use multiple iterations: `python src/main.py --compare --iterations 1000`
3. Generate reports for detailed metrics

**Study Data Structures:**
1. Use specific implementation: `python src/main.py --implementation array`
2. Review logs to see operations
3. Understand implementation details

## Project Structure

```
queue-data-structure/
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

- `src/main.py`: Contains the `ArrayQueue`, `LinkedListQueue`, and `QueuePerformanceAnalyzer` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Queue Data Structure

**Operations:**
- `enqueue(item)`: Add item to rear of queue
- `dequeue()`: Remove and return item from front of queue
- `front()`: View front item without removing - O(1)
- `rear()`: View rear item without removing - O(1)
- `is_empty()`: Check if queue is empty - O(1)
- `size()`: Get number of items - O(1)

**Characteristics:**
- FIFO (First In, First Out) data structure
- Two implementations: array-based and linked list-based
- Different time complexities for operations

### Array-Based Queue

**Time Complexity:**
- Enqueue: O(1) amortized, O(n) worst case (list resizing)
- Dequeue: O(n) - requires shifting all elements
- Front/Rear: O(1)
- Space: O(n)

**Characteristics:**
- Implemented using Python list
- Fast enqueue (append is efficient)
- Slow dequeue (pop(0) requires shifting)
- Better for mostly enqueue operations

### Linked List-Based Queue

**Time Complexity:**
- Enqueue: O(1) - constant time
- Dequeue: O(1) - constant time
- Front/Rear: O(1)
- Space: O(n) - one node per element

**Characteristics:**
- Implemented using linked list with front and rear pointers
- Fast enqueue and dequeue
- More memory overhead per element
- Better for mixed operations

### Performance Comparison

**Array Queue:**
- Fast enqueue operations
- Slow dequeue operations (O(n))
- Better for scenarios with mostly enqueue

**Linked List Queue:**
- Fast enqueue and dequeue (both O(1))
- More memory overhead
- Better for mixed operations

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
- Queue operations (enqueue, dequeue, front, rear, is_empty, size)
- Edge cases (empty queue, invalid operations)
- Both implementations (array and linked list)
- Performance comparison functionality
- Error handling
- Report generation

## Troubleshooting

### Common Issues

**IndexError: Queue is empty:**
- Attempted to dequeue or peek from empty queue
- Check that queue has items before operations

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Queue is empty"**: Attempted to dequeue or peek from empty queue. Ensure queue has items.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use linked list queue** for mixed enqueue/dequeue operations
2. **Use array queue** for mostly enqueue operations
3. **Check queue size** before operations in custom code
4. **Review logs** to understand queue operations
5. **Compare performance** to choose appropriate implementation
6. **Use multiple iterations** for accurate timing measurements

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
