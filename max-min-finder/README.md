# Max-Min Finder Algorithm

A Python implementation of a single-pass algorithm to find maximum and minimum values in an array with detailed analysis. This tool demonstrates an optimized approach that processes elements efficiently while providing comprehensive performance metrics.

## Project Title and Description

The Max-Min Finder tool implements an optimized single-pass algorithm to find both maximum and minimum values in an array simultaneously. It uses a clever optimization technique that processes elements in pairs when possible, reducing the number of comparisons needed while providing detailed analysis of the algorithm's execution.

This tool solves the problem of efficiently finding both extreme values in an array with minimal comparisons, demonstrating algorithmic optimization techniques and providing insights into algorithm performance.

**Target Audience**: Students learning algorithms, developers studying optimization techniques, educators teaching computer science concepts, and anyone interested in efficient algorithm design.

## Features

- Single-pass algorithm for finding max and min simultaneously
- Optimized pair-wise comparison approach
- Detailed comparison counting and analysis
- Comprehensive performance metrics
- Step-by-step logging of algorithm execution
- Detailed analysis reports with statistics
- Index tracking for both max and min values

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/max-min-finder
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

### Basic Usage

Find max and min in a list of numbers:

```bash
python src/main.py 64 34 25 12 22 11 90
```

### With Detailed Analysis

Show detailed analysis:

```bash
python src/main.py 64 34 25 12 22 11 90 --analysis
```

### Generate Report

Generate analysis report:

```bash
python src/main.py 64 34 25 12 22 11 90 -r report.txt
```

### Custom Configuration

```bash
python src/main.py 64 34 25 12 22 11 90 -c custom_config.yaml
```

### Command-Line Arguments

- `numbers`: (Required) One or more numbers to analyze
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-r, --report`: Output path for analysis report
- `--analysis`: Show detailed analysis information

### Common Use Cases

**Find Extremes in Data:**
1. Provide list of numbers: `python src/main.py 10 5 20 15 8`
2. Get min, max, and range immediately
3. Review comparisons and efficiency

**Algorithm Analysis:**
1. Run with `--analysis` flag
2. Study comparison counts and efficiency ratios
3. Understand optimization benefits

**Performance Study:**
1. Test with different array sizes
2. Compare actual comparisons with theoretical bounds
3. Analyze efficiency improvements from pair-wise processing

## Project Structure

```
max-min-finder/
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

- `src/main.py`: Contains the `MaxMinFinder` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Single-Pass Max-Min Algorithm

The algorithm finds both maximum and minimum values in a single pass through the array using an optimization technique that processes elements in pairs.

**Algorithm Steps:**
1. Initialize min and max with first element
2. Process remaining elements in pairs when possible
3. Compare pair elements first, then compare smaller with min and larger with max
4. Handle last element separately if array length is odd

**Optimization:**
- By comparing pairs first, we reduce comparisons from 2n-2 to approximately 3n/2
- Each pair requires 3 comparisons instead of 4
- Significant improvement for large arrays

**Time Complexity:**
- Best case: O(n)
- Average case: O(n)
- Worst case: O(n)

**Space Complexity:** O(1)

**Comparison Count:**
- Naive approach: 2(n-1) comparisons
- Optimized approach: ~3n/2 comparisons (when n is even)
- Improvement: ~25% reduction in comparisons

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
- Finding max and min in various arrays
- Edge cases (single element, two elements, all same values)
- Comparison counting accuracy
- Analysis data correctness
- Report generation
- Error handling

## Troubleshooting

### Common Issues

**Empty Array Error:**
- Ensure at least one number is provided as argument
- Check input format and parsing

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Ensure config.yaml exists and is valid YAML
- Check file permissions
- Verify configuration structure matches expected format

### Error Messages

**"Cannot find max/min in empty array"**: No numbers were provided. Provide at least one number as argument.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

**"Failed to save report"**: Cannot write to output directory. Check permissions and disk space.

### Best Practices

1. **Start with small arrays** to understand the algorithm behavior
2. **Use --analysis flag** to see detailed performance metrics
3. **Compare with naive approach** to appreciate optimization benefits
4. **Study comparison counts** to understand algorithm efficiency
5. **Test with different array sizes** to see scalability

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
