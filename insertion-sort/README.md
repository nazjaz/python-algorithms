# Insertion Sort Algorithm

A Python implementation of the insertion sort algorithm with visualization capabilities and comparison with other sorting algorithms (bubble sort and selection sort). This tool provides comprehensive step-by-step analysis, visual representation, and performance comparison.

## Project Title and Description

The Insertion Sort tool implements the insertion sort algorithm with detailed logging, visualization capabilities, and performance comparison with bubble sort and selection sort. It provides comprehensive statistics, iteration-by-iteration analysis, and visual representation to help understand how the algorithm works.

This tool solves the problem of understanding insertion sort implementation by providing detailed logging, visualization, and side-by-side performance comparison with other sorting algorithms, making it ideal for educational purposes and algorithm analysis.

**Target Audience**: Students learning sorting algorithms, developers studying algorithm implementation, educators teaching computer science concepts, and anyone interested in understanding insertion sort and its performance characteristics compared to other algorithms.

## Features

- Insertion sort algorithm implementation
- Visualization of sorting process (animated GIF)
- Performance comparison with bubble sort and selection sort
- Detailed logging of each step
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
cd /path/to/python-algorithms/insertion-sort
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
- `visualization.enabled`: Enable visualization by default (default: false)
- `visualization.animation_speed`: Animation speed in milliseconds (default: 500)
- `visualization.output_format`: Output format - gif, mp4, or show (default: gif)

**Logging Settings:**
- `logging.level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `logging.file`: Path to log file (default: "logs/app.log")

### Example Configuration

```yaml
visualization:
  enabled: false
  animation_speed: 500
  output_format: "gif"

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

### Create Visualization

Create animated visualization:

```bash
python src/main.py --visualize 64 34 25 12 22 11 90
```

Save visualization to file:

```bash
python src/main.py --visualize --visualization-output sort.gif 64 34 25 12 22 11 90
```

### Compare with Other Algorithms

Compare insertion sort with bubble sort and selection sort:

```bash
python src/main.py --compare 64 34 25 12 22 11 90
```

### Generate Report

Generate detailed sorting report:

```bash
python src/main.py --compare --report report.txt 64 34 25 12 22 11 90
```

### Command-Line Arguments

- `numbers`: (Required) One or more numbers to sort
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-v, --visualize`: Create visualization of sorting process
- `--visualization-output`: Output path for visualization (GIF file)
- `--compare`: Compare with other sorting algorithms
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for sorting report

### Common Use Cases

**Learn Insertion Sort:**
1. Run: `python src/main.py 64 34 25 12 22 11 90`
2. Review console output for step-by-step process
3. Check logs for detailed information

**Visualize Sorting Process:**
1. Run: `python src/main.py --visualize 64 34 25 12 22 11 90`
2. Watch animated visualization
3. Save to file: `python src/main.py --visualize --visualization-output sort.gif 64 34 25 12 22 11 90`

**Compare Algorithms:**
1. Run: `python src/main.py --compare 64 34 25 12 22 11 90`
2. Review timing for each algorithm
3. Compare comparisons and swaps

**Generate Detailed Report:**
1. Run: `python src/main.py --compare --report report.txt 64 34 25 12 22 11 90`
2. Review report file for complete analysis
3. Study algorithm comparison

## Project Structure

```
insertion-sort/
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

- `src/main.py`: Contains the `InsertionSort` class and main logic
- `config.yaml`: Configuration file with visualization and logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### Insertion Sort Algorithm

**How It Works:**
1. Start with second element (index 1)
2. Compare with previous elements
3. Shift larger elements one position to the right
4. Insert current element at correct position
5. Repeat for all elements

**Time Complexity:**
- Best Case: O(n) - already sorted
- Average Case: O(n²)
- Worst Case: O(n²) - reverse sorted

**Space Complexity:**
- O(1) - in-place sorting

**Characteristics:**
- Stable sorting algorithm (preserves relative order)
- Adaptive (efficient for nearly sorted arrays)
- In-place sorting
- Simple to understand and implement
- Efficient for small arrays

### Comparison with Other Algorithms

**vs Bubble Sort:**
- Insertion sort is generally faster
- Both are O(n²) but insertion sort has better constants
- Insertion sort is adaptive (better for nearly sorted data)

**vs Selection Sort:**
- Insertion sort is generally faster
- Both are O(n²) but insertion sort has better constants
- Insertion sort is stable, selection sort is not
- Insertion sort is adaptive

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
- Visualization functionality
- Algorithm comparison

## Troubleshooting

### Common Issues

**Matplotlib Import Error:**
- Install matplotlib: `pip install matplotlib`
- Install pillow for GIF support: `pip install pillow`
- Verify installation: `python -c "import matplotlib; print('OK')"`

**Visualization Not Working:**
- Ensure matplotlib and pillow are installed
- Check that array size is reasonable (very large arrays may be slow)
- Try saving to file instead of displaying

**Empty Array:**
- Empty arrays return empty array
- This is expected behavior

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"matplotlib is required for visualization"**: Install matplotlib with `pip install matplotlib pillow`.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use for learning** insertion sort algorithm
2. **Visualize small arrays** (10-20 elements) for best visualization experience
3. **Compare algorithms** to understand performance differences
4. **Review logs** to understand algorithm execution
5. **Generate reports** for detailed analysis
6. **Test with different inputs** to see algorithm behavior

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
