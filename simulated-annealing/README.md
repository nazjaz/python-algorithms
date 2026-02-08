# Simulated Annealing for Global Optimization

A Python implementation of simulated annealing algorithm for global optimization with configurable temperature scheduling and acceptance criteria. This tool provides comprehensive optimization capabilities for continuous optimization problems with detailed logging and performance tracking.

## Project Title and Description

The Simulated Annealing tool implements a probabilistic optimization algorithm inspired by the annealing process in metallurgy. It provides configurable temperature scheduling strategies and acceptance criteria to solve global optimization problems, particularly useful for problems with multiple local optima.

This tool solves the problem of finding global optima in complex, multi-modal optimization landscapes where gradient-based methods may get trapped in local minima. It offers flexibility through multiple cooling schedules and acceptance criteria, making it adaptable to various optimization problems.

**Target Audience**: Researchers working on optimization problems, students learning metaheuristic algorithms, engineers solving complex optimization problems, and developers implementing global optimization solutions.

## Features

- Multiple temperature scheduling strategies (exponential, linear, logarithmic, geometric)
- Configurable acceptance criteria (Metropolis, threshold-based)
- Support for bounded and unbounded optimization problems
- Comprehensive logging and iteration history tracking
- Configurable algorithm parameters via YAML
- Reproducible results through random seed control
- Detailed performance tracking and convergence monitoring
- Flexible neighbor generation with customizable step sizes
- Support for arbitrary objective functions

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/simulated-annealing
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
simulated_annealing:
  initial_temperature: 100.0      # Starting temperature
  final_temperature: 0.01         # Stopping temperature
  max_iterations: 1000            # Maximum iterations
  schedule_type: "exponential"     # Cooling schedule type
  acceptance_criterion: "metropolis"  # Acceptance method
  random_seed: 42                 # For reproducibility

logging:
  level: "INFO"                   # Logging level
  file: "logs/app.log"            # Log file path
```

### Temperature Scheduling

Four cooling schedule types are available:

1. **Exponential**: `T(k) = T0 * α^k` where α = (Tf/T0)^(1/max_iter)
   - Smooth, gradual cooling
   - Most commonly used

2. **Geometric**: Similar to exponential with different interpretation
   - Good for problems requiring slow cooling

3. **Linear**: `T(k) = T0 - k * (T0 - Tf) / max_iter`
   - Constant cooling rate
   - Simple and predictable

4. **Logarithmic**: `T(k) = T0 / (1 + log(1 + k))`
   - Very slow initial cooling
   - Useful for complex landscapes

### Acceptance Criteria

Two acceptance criteria are implemented:

1. **Metropolis**: Standard simulated annealing acceptance
   - Accepts better solutions always
   - Accepts worse solutions with probability exp(-ΔE/T)
   - Most widely used criterion

2. **Threshold**: Threshold-based acceptance
   - Accepts based on improvement ratio
   - More deterministic behavior

## Usage

### Basic Usage

```python
from src.main import SimulatedAnnealing
import numpy as np

# Initialize optimizer
sa = SimulatedAnnealing(config_path="config.yaml")

# Define objective function
def objective(x):
    return np.sum(x ** 2)  # Minimize sum of squares

# Run optimization
result = sa.optimize(
    objective_function=objective,
    dimension=2,
    bounds=[(-10, 10), (-10, 10)],
    step_size=1.0
)

print(f"Best solution: {result['best_solution']}")
print(f"Best energy: {result['best_energy']}")
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
from src.main import SimulatedAnnealing

def rastrigin(x):
    """Rastrigin function: global minimum at origin."""
    n = len(x)
    A = 10
    return A * n + np.sum(x ** 2 - A * np.cos(2 * np.pi * x))

sa = SimulatedAnnealing()
result = sa.optimize(
    rastrigin,
    dimension=2,
    bounds=[(-5.12, 5.12), (-5.12, 5.12)],
    step_size=0.5
)

print(f"Optimal solution: {result['best_solution']}")
print(f"Optimal value: {result['best_energy']:.6f}")
```

### Custom Objective Functions

The optimizer accepts any callable that takes a numpy array and returns a float:

```python
def custom_objective(x):
    # Your optimization function here
    # Must return a single float value
    return some_complex_function(x)

result = sa.optimize(custom_objective, dimension=3)
```

## Project Structure

```
simulated-annealing/
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

- `src/main.py`: Core implementation containing `SimulatedAnnealing`, `TemperatureScheduler`, and `AcceptanceCriterion` classes
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
- Temperature scheduling for all schedule types
- Acceptance criteria (Metropolis and threshold)
- Optimization on benchmark functions
- Edge cases and error handling
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Initial temperature must be greater than final temperature`

**Solution**: Ensure `initial_temperature > final_temperature` in config.yaml

**Issue**: Algorithm not converging

**Solution**: 
- Increase `max_iterations`
- Adjust `initial_temperature` and `final_temperature`
- Try different `schedule_type`
- Adjust `step_size` parameter

**Issue**: Poor solution quality

**Solution**:
- Increase `initial_temperature` for more exploration
- Decrease `final_temperature` for better convergence
- Try different cooling schedules
- Adjust `step_size` for better neighbor generation

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

### Simulated Annealing Overview

Simulated annealing is a probabilistic optimization algorithm that:
1. Starts with a high temperature allowing exploration
2. Gradually cools (reduces temperature) to focus on exploitation
3. Accepts worse solutions probabilistically to escape local optima
4. Converges to global optimum as temperature approaches zero

### Temperature Scheduling

Temperature controls the balance between exploration and exploitation:
- High temperature: More exploration, accepts worse solutions
- Low temperature: More exploitation, accepts only better solutions

### Acceptance Criteria

The Metropolis criterion accepts worse solutions with probability:
```
P(accept) = exp(-(E_new - E_old) / T)
```

This probability decreases as:
- Temperature decreases
- Energy difference increases

## Performance Considerations

- Algorithm complexity: O(max_iterations × dimension)
- Memory usage: O(max_iterations) for history storage
- For large problems, consider:
  - Reducing `max_iterations` if convergence is fast
  - Using logarithmic schedule for slow cooling
  - Adjusting `step_size` for better neighbor generation

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
