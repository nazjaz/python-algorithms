# Simulated Annealing API Documentation

## Classes

### SimulatedAnnealing

Main class for running simulated annealing optimization.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize SimulatedAnnealing with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
sa = SimulatedAnnealing(config_path="config.yaml")
```

##### `optimize(objective_function, initial_solution=None, bounds=None, dimension=2, step_size=1.0)`

Run simulated annealing optimization.

**Parameters:**
- `objective_function` (Callable[[np.ndarray], float]): Function to minimize
- `initial_solution` (Optional[np.ndarray]): Starting solution. If None, random
- `bounds` (Optional[List[Tuple[float, float]]]): Bounds for each dimension
- `dimension` (int): Problem dimension (used if initial_solution is None)
- `step_size` (float): Maximum step size for neighbor generation

**Returns:**
Dictionary containing:
- `best_solution` (np.ndarray): Best solution found
- `best_energy` (float): Best energy value
- `iterations` (int): Total iterations performed
- `history` (List[Tuple[int, float, float]]): Iteration history
- `converged` (bool): Whether algorithm converged

**Raises:**
- `ValueError`: If parameters are invalid

**Example:**
```python
def objective(x):
    return np.sum(x ** 2)

result = sa.optimize(
    objective_function=objective,
    dimension=2,
    bounds=[(-10, 10), (-10, 10)],
    step_size=1.0
)
```

### TemperatureScheduler

Manages temperature scheduling for simulated annealing.

#### Methods

##### `__init__(initial_temperature, final_temperature, max_iterations, schedule_type="exponential")`

Initialize temperature scheduler.

**Parameters:**
- `initial_temperature` (float): Starting temperature value
- `final_temperature` (float): Ending temperature value
- `max_iterations` (int): Maximum number of iterations
- `schedule_type` (str): Type of cooling schedule

**Raises:**
- `ValueError`: If temperatures are invalid or schedule_type is unknown

##### `get_temperature(iteration)`

Get temperature for given iteration.

**Parameters:**
- `iteration` (int): Current iteration number (0-indexed)

**Returns:**
- `float`: Current temperature value

**Raises:**
- `ValueError`: If iteration is out of valid range

### AcceptanceCriterion

Manages acceptance criteria for simulated annealing.

#### Static Methods

##### `metropolis(current_energy, candidate_energy, temperature)`

Metropolis acceptance criterion.

**Parameters:**
- `current_energy` (float): Energy of current solution
- `candidate_energy` (float): Energy of candidate solution
- `temperature` (float): Current temperature

**Returns:**
- `bool`: True if candidate should be accepted

**Raises:**
- `ValueError`: If temperature is non-positive

##### `threshold(current_energy, candidate_energy, temperature, threshold=0.5)`

Threshold-based acceptance criterion.

**Parameters:**
- `current_energy` (float): Energy of current solution
- `candidate_energy` (float): Energy of candidate solution
- `temperature` (float): Current temperature (not used)
- `threshold` (float): Acceptance threshold. Default: 0.5

**Returns:**
- `bool`: True if candidate should be accepted

## Configuration

### Configuration File Format

The algorithm uses YAML configuration files with the following structure:

```yaml
simulated_annealing:
  initial_temperature: 100.0
  final_temperature: 0.01
  max_iterations: 1000
  schedule_type: "exponential"
  acceptance_criterion: "metropolis"
  random_seed: 42

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Configuration Parameters

- `initial_temperature` (float): Starting temperature (must be > 0)
- `final_temperature` (float): Ending temperature (must be > 0, < initial)
- `max_iterations` (int): Maximum iterations (must be > 0)
- `schedule_type` (str): One of "exponential", "linear", "logarithmic", "geometric"
- `acceptance_criterion` (str): One of "metropolis", "threshold"
- `random_seed` (int, optional): Random seed for reproducibility
- `threshold` (float): Threshold value for threshold acceptance (default: 0.5)

## Examples

### Basic Optimization

```python
from src.main import SimulatedAnnealing
import numpy as np

sa = SimulatedAnnealing()

def objective(x):
    return np.sum(x ** 2)

result = sa.optimize(
    objective_function=objective,
    dimension=2,
    bounds=[(-10, 10), (-10, 10)]
)

print(f"Best solution: {result['best_solution']}")
print(f"Best energy: {result['best_energy']}")
```

### Custom Configuration

```python
sa = SimulatedAnnealing(config_path="custom_config.yaml")
result = sa.optimize(objective_function=my_function, dimension=3)
```

### Using Initial Solution

```python
initial = np.array([5.0, 5.0, 5.0])
result = sa.optimize(
    objective_function=my_function,
    initial_solution=initial,
    step_size=0.5
)
```
