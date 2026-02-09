# Knapsack Problem Solver

A Python implementation of the knapsack problem solver with both 0-1 and fractional variants. This tool provides dynamic programming solution for 0-1 knapsack and greedy algorithm solution for fractional knapsack, with comprehensive performance comparison and detailed analysis.

## Project Title and Description

The Knapsack Problem Solver implements solutions for two variants of the classic knapsack optimization problem: 0-1 knapsack (using dynamic programming) and fractional knapsack (using greedy algorithm). It provides detailed logging, performance comparison, and comprehensive edge case handling to help understand how different algorithms solve similar optimization problems.

This tool solves the problem of finding the optimal way to pack items with given weights and values into a knapsack with limited capacity, demonstrating the difference between dynamic programming and greedy approaches for different problem variants.

**Target Audience**: Students learning optimization algorithms, developers studying dynamic programming and greedy algorithms, educators teaching computer science concepts, and anyone interested in understanding knapsack problem solutions and their performance characteristics.

## Features

- 0-1 knapsack implementation using dynamic programming
- Fractional knapsack implementation using greedy algorithm
- Comprehensive edge case handling
- Performance comparison with timing analysis
- Detailed step-by-step logging
- Comprehensive performance reports
- Multiple iterations support for accurate timing
- Input validation for weights, values, and capacity
- Error handling for invalid inputs
- Space-optimized dynamic programming solution

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/knapsack-problem
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

### Performance Comparison (Default)

Compare both approaches:

```bash
python src/main.py 50 --weights 10 20 30 --values 60 100 120
```

### Specific Method

Use a specific solution method:

```bash
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --method 01
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --method fractional
```

### Multiple Iterations

Run multiple iterations for more accurate timing:

```bash
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py 50 --weights 10 20 30 --values 60 100 120 --report report.txt
```

### Command-Line Arguments

- `capacity`: (Required) Maximum knapsack capacity
- `-w, --weights`: (Required) Item weights (space-separated)
- `-v, --values`: (Required) Item values (space-separated)
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --method`: Solution method - 01, fractional, or compare (default: compare)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Compare Approaches:**
1. Run: `python src/main.py 50 --weights 10 20 30 --values 60 100 120`
2. Review timing and value for each approach
3. Understand when fractional provides better solutions

**Study Algorithms:**
1. Use specific method: `python src/main.py 50 --weights 10 20 30 --values 60 100 120 --method 01`
2. Review logs to see algorithm execution
3. Understand different approaches

**Performance Analysis:**
1. Test with different problem sizes
2. Use multiple iterations: `python src/main.py 50 --weights 10 20 30 --values 60 100 120 --iterations 1000`
3. Generate reports for detailed metrics

**Edge Case Testing:**
1. Test with capacity smaller than all items
2. Test with capacity larger than sum of all items
3. Test with single item
4. Test with items of equal value-to-weight ratio

## Project Structure

```
knapsack-problem/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore patterns
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

- `src/main.py`: Contains the `KnapsackSolver` class and main logic
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### 0-1 Knapsack Problem

**Problem Definition:**
Given items with weights and values, select items to maximize total value without exceeding capacity. Each item can be taken at most once (0 or 1).

**How It Works:**
1. Build a DP table where `dp[w]` represents maximum value achievable with weight `w`
2. For each item, consider taking it or not
3. Update DP table by comparing value with and without current item
4. Reconstruct solution by backtracking through DP table

**Time Complexity:**
- Best Case: O(n * W) where n=items, W=capacity
- Average Case: O(n * W)
- Worst Case: O(n * W)

**Space Complexity:**
- O(W) with space optimization (1D array instead of 2D)

**Characteristics:**
- Dynamic programming approach
- Optimal solution guaranteed
- Pseudo-polynomial time complexity
- Space-optimized implementation

### Fractional Knapsack Problem

**Problem Definition:**
Given items with weights and values, select items (or fractions) to maximize total value without exceeding capacity. Items can be taken in fractions.

**How It Works:**
1. Calculate value-to-weight ratio for each item
2. Sort items by ratio in descending order
3. Greedily select items with highest ratio first
4. Take full item if capacity allows, otherwise take fraction

**Time Complexity:**
- Best Case: O(n log n) for sorting
- Average Case: O(n log n)
- Worst Case: O(n log n)

**Space Complexity:**
- O(n) for sorting

**Characteristics:**
- Greedy algorithm approach
- Optimal solution guaranteed (for fractional variant)
- Polynomial time complexity
- Simpler than 0-1 knapsack

### Key Differences

- **0-1 Knapsack**: Items are indivisible (take all or nothing)
- **Fractional Knapsack**: Items can be divided (take partial amounts)
- **0-1 Solution**: Dynamic programming (more complex, handles indivisible items)
- **Fractional Solution**: Greedy algorithm (simpler, optimal for divisible items)
- **Fractional typically yields higher value** since items can be partially taken

### Edge Cases Handled

- Empty item lists
- Mismatched weights and values arrays
- Zero or negative capacity
- Zero or negative weights
- Negative values
- Capacity smaller than all items
- Capacity larger than sum of all items
- Single item
- Items with equal value-to-weight ratios
- Large problem sizes

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
- 0-1 knapsack with various inputs
- Fractional knapsack with various inputs
- Edge cases (empty lists, invalid inputs, boundary conditions)
- Performance comparison functionality
- Error handling (invalid inputs, mismatched arrays)
- Report generation
- Both implementation approaches
- Input validation

## Troubleshooting

### Common Issues

**ValueError: Weights and values lists cannot be empty:**
- Ensure both weights and values arrays are provided
- Check that arrays are not empty

**ValueError: Weights length must match values length:**
- Ensure weights and values arrays have the same length
- Count items in both arrays

**ValueError: Capacity must be positive:**
- Capacity must be greater than zero
- Check that capacity value is correct

**ValueError: All weights must be positive:**
- All item weights must be greater than zero
- Check for zero or negative weights

**ValueError: All values must be non-negative:**
- All item values must be zero or positive
- Check for negative values

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Weights and values lists cannot be empty"**: Both arrays must contain at least one item.

**"Weights length must match values length"**: The number of weights must equal the number of values.

**"Capacity must be positive"**: The knapsack capacity must be greater than zero.

**"All weights must be positive"**: Each item weight must be greater than zero.

**"All values must be non-negative"**: Each item value must be zero or positive.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Use 0-1 knapsack** when items are indivisible (e.g., electronics, furniture)
2. **Use fractional knapsack** when items can be divided (e.g., liquids, grains)
3. **Compare both approaches** to understand trade-offs
4. **Use multiple iterations** for accurate timing measurements
5. **Review logs** to see algorithm execution details
6. **Validate inputs** before solving to catch errors early
7. **Consider problem size** - 0-1 knapsack can be slow for large capacities

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
