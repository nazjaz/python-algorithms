# Bubble Sort Algorithm

A Python implementation of the bubble sort algorithm with detailed visualization of each swap operation and comprehensive comparison counting. This tool helps understand the bubble sort algorithm through step-by-step visualization and performance metrics.

## Project Title and Description

The Bubble Sort Algorithm tool implements the classic bubble sort algorithm with enhanced features including detailed logging of each comparison and swap operation, step-by-step visualization, and comprehensive performance statistics. It provides insights into how bubble sort works and its performance characteristics.

This tool solves the problem of understanding bubble sort algorithm behavior by providing visual representation of each sorting step and detailed metrics about comparisons and swaps.

**Target Audience**: Students learning algorithms, developers studying sorting algorithms, educators teaching computer science concepts, and anyone interested in understanding bubble sort implementation.

## Features

- Complete bubble sort algorithm implementation
- Detailed visualization of each swap operation with color-coded bars
- Comprehensive comparison counting and swap tracking
- Step-by-step logging of algorithm execution
- Performance statistics and analysis
- Configurable visualization output
- Detailed sorting reports with metrics

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Matplotlib for visualization

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/bubble-sort
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

The tool uses a YAML configuration file to define visualization and logging settings. The default configuration file is `config.yaml` in the project root.

#### Key Configuration Options

**Visualization Settings:**
- `visualization.enabled`: Enable or disable visualization (default: true)
- `visualization.output_file`: Path for visualization image (default: "logs/bubble_sort_visualization.png")

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
visualization:
  enabled: true
  output_file: "logs/bubble_sort_visualization.png"

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Environment Variables

No environment variables are currently required. All configuration is managed through the `config.yaml` file.

## Usage

### Basic Usage

Sort a list of numbers:

```bash
python src/main.py 64 34 25 12 22 11 90
```

### With Visualization

Generate visualization of sorting process:

```bash
python src/main.py 64 34 25 12 22 11 90 --visualize
```

### Custom Configuration

```bash
python src/main.py 64 34 25 12 22 11 90 -c custom_config.yaml
```

### Custom Output Paths

```bash
python src/main.py 64 34 25 12 22 11 90 --visualize -o custom_viz.png -r report.txt
```

### Command-Line Arguments

- `numbers`: (Required) One or more integers to sort
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-v, --visualize`: Generate visualization
- `-o, --output`: Custom output path for visualization (overrides config)
- `-r, --report`: Custom output path for report (overrides config)

### Common Use Cases

**Learn Bubble Sort:**
1. Run with small array: `python src/main.py 5 2 8 1 9`
2. Review logs to see each comparison and swap
3. Check visualization to see step-by-step process
4. Review report for performance metrics

**Compare Performance:**
1. Test with different array sizes
2. Compare number of comparisons and swaps
3. Analyze swap ratio and efficiency

**Educational Demonstration:**
1. Use visualization to show sorting process
2. Explain comparisons and swaps using logs
3. Discuss time complexity using statistics

## Project Structure

```
bubble-sort/
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

- `src/main.py`: Contains the `BubbleSort` class and main logic
- `config.yaml`: Configuration file with visualization and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files and visualizations

## Algorithm Details

### Bubble Sort Algorithm

Bubble sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until no swaps are needed, which indicates the list is sorted.

**Time Complexity:**
- Best case: O(n) when array is already sorted
- Average case: O(n²)
- Worst case: O(n²)

**Space Complexity:** O(1)

**Characteristics:**
- Stable sorting algorithm
- In-place sorting
- Adaptive (can detect if array is already sorted)

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
- Sorting functionality with various inputs
- Comparison and swap counting
- Visualization generation
- Report generation
- Edge cases (empty array, single element, already sorted)
- Error handling

## Troubleshooting

### Common Issues

**Visualization Not Generated:**
- Check that visualization is enabled in config.yaml
- Verify matplotlib is installed correctly
- Ensure output directory is writable
- Check logs for detailed error messages

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

**Configuration Errors:**
- Ensure config.yaml exists and is valid YAML
- Check file permissions
- Verify configuration structure matches expected format

### Error Messages

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

**"Empty array provided"**: No numbers were provided to sort. Provide at least one number as argument.

**"Failed to save visualization"**: Cannot write to output directory. Check permissions and disk space.

### Best Practices

1. **Start with small arrays** to understand the algorithm behavior
2. **Review logs** to see detailed step-by-step execution
3. **Use visualization** to understand swap operations visually
4. **Compare performance** with different input sizes
5. **Study the statistics** to understand algorithm efficiency

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
