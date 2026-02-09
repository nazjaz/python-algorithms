# Selection Sort Algorithm

A Python implementation of the selection sort algorithm with detailed logging of minimum element selection and swap operations. This tool provides comprehensive step-by-step analysis of the sorting process.

## Project Title and Description

The Selection Sort tool implements the selection sort algorithm with detailed logging of each step, including minimum element finding and swap operations. It provides comprehensive statistics, iteration-by-iteration analysis, and detailed reports to help understand how the algorithm works.

This tool solves the problem of understanding selection sort implementation by providing detailed logging and analysis of the sorting process, making it ideal for educational purposes and algorithm analysis.

**Target Audience**: Students learning sorting algorithms, developers studying algorithm implementation, educators teaching computer science concepts, and anyone interested in understanding selection sort and its performance characteristics.

## Features

- Selection sort algorithm implementation
- Detailed logging of minimum element selection
- Detailed logging of swap operations
- Step-by-step iteration tracking
- Comprehensive statistics (comparisons, swaps, iterations)
- Detailed sorting reports
- Performance metrics
- Error handling for edge cases

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/selection-sort
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

### Basic Sorting

Sort an array of numbers:

```bash
python src/main.py 64 34 25 12 22 11 90
```

### Generate Report

Generate detailed sorting report:

```bash
python src/main.py 64 34 25 12 22 11 90 --report report.txt
```

### Command-Line Arguments

- `numbers`: (Required) One or more numbers to sort
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-r, --report`: Output path for sorting report

### Common Use Cases

**Learn Selection Sort:**
1. Run: `python src/main.py 64 34 25 12 22 11 90`
2. Review console output for step-by-step process
3. Check logs for detailed information

**Generate Detailed Report:**
1. Run: `python src/main.py 64 34 25 12 22 11 90 --report report.txt`
2. Review report file for complete analysis
3. Study iteration-by-iteration details

**Study Algorithm Performance:**
1. Test with different array sizes
2. Review statistics (comparisons, swaps)
3. Understand time complexity in practice

## Project Structure

```
selection-sort/
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

- `src/main.py`: Contains the `SelectionSort` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Selection Sort Algorithm

**How It Works:**
1. Find the minimum element in the unsorted portion of the array
2. Swap it with the first element of the unsorted portion
3. Move the boundary of sorted/unsorted portions one position to the right
4. Repeat until entire array is sorted

**Time Complexity:**
- Best Case: O(n²)
- Average Case: O(n²)
- Worst Case: O(n²)

**Space Complexity:**
- O(1) - in-place sorting

**Characteristics:**
- In-place sorting algorithm
- Not stable (may change relative order of equal elements)
- Simple to understand and implement
- Always performs O(n²) comparisons regardless of input
- Performs at most n-1 swaps

### Logging Details

The implementation provides detailed logging for:
- Each iteration of the outer loop
- Minimum element finding process
- Each comparison during minimum search
- Swap operations (when and what is swapped)
- Array state after each iteration
- Final statistics

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
- Sorting with various inputs
- Edge cases (empty array, single element, already sorted, reverse sorted)
- Statistics accuracy
- Report generation
- Error handling
- Minimum element finding
- Swap operations

## Troubleshooting

### Common Issues

**Empty Array:**
- Empty arrays return empty array
- This is expected behavior

**Single Element:**
- Single element arrays are already sorted
- Algorithm handles this case

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

**"Invalid YAML"**: The config.yaml file has syntax errors. Check YAML syntax.

### Best Practices

1. **Use for learning** selection sort algorithm
2. **Review logs** to understand algorithm execution
3. **Generate reports** for detailed analysis
4. **Test with different inputs** to see algorithm behavior
5. **Study statistics** to understand performance characteristics

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
