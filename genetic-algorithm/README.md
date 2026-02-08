# Genetic Algorithm for Optimization

A Python implementation of genetic algorithm for global optimization with configurable selection, crossover, and mutation operators. This tool provides comprehensive optimization capabilities for continuous optimization problems with detailed logging and performance tracking.

## Project Title and Description

The Genetic Algorithm tool implements an evolutionary optimization algorithm inspired by natural selection. It provides configurable selection, crossover, and mutation operators to solve global optimization problems, particularly useful for problems with multiple local optima and complex search spaces.

This tool solves the problem of finding global optima in complex, multi-modal optimization landscapes where traditional gradient-based methods may get trapped in local minima. It offers flexibility through multiple selection strategies, crossover operators, and mutation schemes, making it adaptable to various optimization problems.

**Target Audience**: Researchers working on optimization problems, students learning evolutionary algorithms, engineers solving complex optimization problems, and developers implementing global optimization solutions.

## Features

- Multiple selection operators (tournament, roulette wheel, rank-based)
- Multiple crossover operators (single-point, multi-point, uniform, arithmetic)
- Multiple mutation operators (Gaussian, uniform, swap, polynomial)
- Elitism support for preserving best solutions
- Configurable population size and generation count
- Support for bounded and unbounded optimization problems
- Comprehensive logging and generation history tracking
- Configurable algorithm parameters via YAML
- Reproducible results through random seed control
- Detailed performance tracking and convergence monitoring
- Flexible fitness evaluation for arbitrary objective functions

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/genetic-algorithm
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
python src/main.py --test
```

## Configuration

### Configuration File Structure

The algorithm is configured via `config.yaml`:

```yaml
genetic_algorithm:
  population_size: 50
  max_generations: 100
  crossover_rate: 0.8
  mutation_rate: 0.1
  elite_size: 1
  selection_type: "tournament"
  crossover_type: "single_point"
  mutation_type: "gaussian"
  random_seed: 42

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Selection Operators

Three selection operators are available:

1. **Tournament Selection**: Selects best individual from random tournament
   - Parameters: `tournament_size` (default: 3)
   - Good balance of exploration and exploitation
   - Most commonly used

2. **Roulette Wheel Selection**: Probabilistic selection based on fitness
   - Converts minimization to maximization automatically
   - Good for maintaining diversity

3. **Rank-Based Selection**: Selection based on rank rather than absolute fitness
   - Parameters: `selection_pressure` (1.0-2.0, default: 2.0)
   - Reduces premature convergence
   - Good for problems with fitness scaling issues

### Crossover Operators

Four crossover operators are implemented:

1. **Single-Point Crossover**: Splits parents at one point and swaps segments
   - Simple and effective
   - Most commonly used

2. **Multi-Point Crossover**: Multiple crossover points
   - Parameters: `num_points` (default: 2)
   - More exploration

3. **Uniform Crossover**: Each gene independently chosen from parents
   - Parameters: `mixing_ratio` (0.0-1.0, default: 0.5)
   - High diversity

4. **Arithmetic Crossover**: Blends parent genes
   - Parameters: `alpha` (0.0-1.0, default: 0.5)
   - Good for continuous optimization

### Mutation Operators

Four mutation operators are implemented:

1. **Gaussian Mutation**: Adds Gaussian noise to genes
   - Parameters: `mutation_strength` (default: 0.1)
   - Most commonly used for continuous problems

2. **Uniform Mutation**: Adds uniform noise to genes
   - Parameters: `mutation_range` (default: 1.0)
   - Good for exploration

3. **Swap Mutation**: Swaps two genes
   - Useful for permutation problems
   - Discrete optimization

4. **Polynomial Mutation**: Polynomial distribution-based mutation
   - Parameters: `eta` (default: 20.0)
   - Common in multi-objective optimization (NSGA-II)

## Usage

### Basic Usage

```python
from src.main import GeneticAlgorithm
import numpy as np

# Initialize optimizer
ga = GeneticAlgorithm(config_path="config.yaml")

# Define objective function
def objective(x):
    return np.sum(x ** 2)  # Minimize sum of squares

# Run optimization
result = ga.optimize(
    objective_function=objective,
    dimension=2,
    bounds=[(-10, 10), (-10, 10)]
)

print(f"Best solution: {result['best_solution']}")
print(f"Best fitness: {result['best_fitness']}")
```

### Command-Line Usage

Run with test problem:

```bash
python src/main.py --test
```

Specify custom configuration:

```bash
python src/main.py --config custom_config.yaml
```

### Advanced Example: Rastrigin Function

```python
import numpy as np
from src.main import GeneticAlgorithm

def rastrigin(x):
    """Rastrigin function: global minimum at origin."""
    n = len(x)
    A = 10
    return A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))

ga = GeneticAlgorithm()
result = ga.optimize(
    rastrigin,
    dimension=2,
    bounds=[(-5.12, 5.12), (-5.12, 5.12)]
)

print(f"Optimal solution: {result['best_solution']}")
print(f"Optimal value: {result['best_fitness']:.6f}")
```

### Custom Operator Configuration

```python
# Custom config with specific operators
config = {
    "genetic_algorithm": {
        "population_size": 100,
        "max_generations": 200,
        "selection_type": "rank",
        "selection_params": {"selection_pressure": 1.5},
        "crossover_type": "uniform",
        "crossover_params": {"mixing_ratio": 0.6},
        "mutation_type": "polynomial",
        "mutation_params": {"eta": 15.0}
    }
}

# Save to file and use
ga = GeneticAlgorithm(config_path="custom_config.yaml")
```

### Custom Objective Functions

The optimizer accepts any callable that takes a numpy array and returns a float:

```python
def custom_objective(x):
    # Your optimization function here
    # Must return a single float value
    return some_complex_function(x)

result = ga.optimize(custom_objective, dimension=3)
```

## Project Structure

```
genetic-algorithm/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── config.yaml              # Configuration file
├── .gitignore               # Git ignore rules
├── src/
│   └── main.py              # Main implementation
├── tests/
│   └── test_main.py         # Unit tests
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Log directory
```

### File Descriptions

- `src/main.py`: Core implementation containing `GeneticAlgorithm`, `SelectionOperator`, `CrossoverOperator`, and `MutationOperator` classes
- `config.yaml`: Configuration file for algorithm parameters
- `tests/test_main.py`: Comprehensive unit tests
- `docs/API.md`: Detailed API documentation
- `logs/`: Directory for application logs

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Test Structure

Tests cover:
- Selection operators (tournament, roulette, rank-based)
- Crossover operators (single-point, multi-point, uniform, arithmetic)
- Mutation operators (Gaussian, uniform, swap, polynomial)
- Optimization on benchmark functions
- Edge cases and error handling
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Bounds length doesn't match dimension`

**Solution**: Ensure `len(bounds) == dimension` when providing bounds

**Issue**: Algorithm not converging

**Solution**: 
- Increase `population_size` for more diversity
- Increase `max_generations` for more evolution
- Adjust `crossover_rate` and `mutation_rate`
- Try different operator combinations
- Increase `elite_size` to preserve more good solutions

**Issue**: Poor solution quality

**Solution**:
- Increase `population_size` for better exploration
- Increase `max_generations` for more evolution time
- Adjust `mutation_rate` and `mutation_strength`
- Try different selection operators
- Experiment with different crossover types

**Issue**: Premature convergence

**Solution**:
- Increase `mutation_rate` for more diversity
- Use rank-based selection instead of tournament
- Increase `population_size`
- Decrease `elite_size`
- Use uniform crossover for more exploration

**Issue**: Configuration file not found

**Solution**: Ensure `config.yaml` exists in project root or specify path with `--config` flag

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid parameter values - check config.yaml
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## Contributing

### Development Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Install development dependencies: `pip install pytest pytest-cov`
5. Run tests: `pytest tests/`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Include docstrings for all public functions and classes
- Write tests for all new functionality

### Pull Request Process

1. Create feature branch
2. Implement changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit pull request with clear description

## Algorithm Details

### Genetic Algorithm Overview

Genetic algorithm is an evolutionary optimization algorithm that:
1. Maintains a population of candidate solutions
2. Evaluates fitness of each individual
3. Selects parents based on fitness
4. Creates offspring through crossover
5. Applies mutation to maintain diversity
6. Replaces population with new generation
7. Repeats until convergence or max generations

### Selection

Selection determines which individuals become parents:
- Tournament: Competitive selection, good balance
- Roulette: Probabilistic, maintains diversity
- Rank-based: Reduces fitness scaling issues

### Crossover

Crossover combines parent genes to create offspring:
- Single-point: Simple, effective
- Multi-point: More exploration
- Uniform: High diversity
- Arithmetic: Good for continuous spaces

### Mutation

Mutation introduces random changes:
- Gaussian: Smooth perturbations
- Uniform: Bounded random changes
- Swap: Discrete changes
- Polynomial: Controlled distribution

### Elitism

Elitism preserves best individuals across generations:
- Prevents loss of good solutions
- Speeds up convergence
- Can reduce diversity if overused

## Performance Considerations

- Algorithm complexity: O(max_generations × population_size × dimension)
- Memory usage: O(population_size × dimension)
- For large problems, consider:
  - Reducing `population_size` if memory constrained
  - Using more efficient operators (single-point crossover)
  - Adjusting `max_generations` based on convergence
  - Using elitism to preserve good solutions

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
