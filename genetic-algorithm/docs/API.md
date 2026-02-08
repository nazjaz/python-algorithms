# Genetic Algorithm API Documentation

## Classes

### GeneticAlgorithm

Main class for running genetic algorithm optimization.

#### Methods

##### `__init__(config_path: str = "config.yaml")`

Initialize GeneticAlgorithm with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Default: "config.yaml"

**Raises:**
- `FileNotFoundError`: If config file doesn't exist
- `yaml.YAMLError`: If config file is invalid YAML

**Example:**
```python
ga = GeneticAlgorithm(config_path="config.yaml")
```

##### `optimize(objective_function, dimension, bounds=None, initial_population=None)`

Run genetic algorithm optimization.

**Parameters:**
- `objective_function` (Callable[[np.ndarray], float]): Function to minimize
- `dimension` (int): Problem dimension
- `bounds` (Optional[List[Tuple[float, float]]]): Bounds for each dimension
- `initial_population` (Optional[np.ndarray]): Initial population

**Returns:**
Dictionary containing:
- `best_solution` (np.ndarray): Best solution found
- `best_fitness` (float): Best fitness value
- `generations` (int): Total generations evolved
- `history` (List[Tuple[int, float, float]]): Generation history
- `final_population` (np.ndarray): Final population
- `final_fitness` (np.ndarray): Final fitness values

**Raises:**
- `ValueError`: If parameters are invalid

**Example:**
```python
def objective(x):
    return np.sum(x ** 2)

result = ga.optimize(
    objective_function=objective,
    dimension=2,
    bounds=[(-10, 10), (-10, 10)]
)
```

### SelectionOperator

Implements selection operators for genetic algorithm.

#### Static Methods

##### `tournament_selection(population, fitness, tournament_size=3)`

Select parents using tournament selection.

**Parameters:**
- `population` (np.ndarray): Population array
- `fitness` (np.ndarray): Fitness values
- `tournament_size` (int): Tournament size

**Returns:**
- Tuple of (selected_parents, selected_indices)

##### `roulette_wheel_selection(population, fitness)`

Select parents using roulette wheel selection.

**Parameters:**
- `population` (np.ndarray): Population array
- `fitness` (np.ndarray): Fitness values

**Returns:**
- Tuple of (selected_parents, selected_indices)

##### `rank_based_selection(population, fitness, selection_pressure=2.0)`

Select parents using rank-based selection.

**Parameters:**
- `population` (np.ndarray): Population array
- `fitness` (np.ndarray): Fitness values
- `selection_pressure` (float): Selection pressure (1.0-2.0)

**Returns:**
- Tuple of (selected_parents, selected_indices)

##### `elitism_selection(population, fitness, elite_size=1)`

Select best individuals using elitism.

**Parameters:**
- `population` (np.ndarray): Population array
- `fitness` (np.ndarray): Fitness values
- `elite_size` (int): Number of elite individuals

**Returns:**
- Tuple of (selected_parents, selected_indices)

### CrossoverOperator

Implements crossover operators for genetic algorithm.

#### Static Methods

##### `single_point_crossover(parent1, parent2, crossover_rate=0.8)`

Perform single-point crossover.

**Parameters:**
- `parent1` (np.ndarray): First parent
- `parent2` (np.ndarray): Second parent
- `crossover_rate` (float): Probability of crossover

**Returns:**
- Tuple of (offspring1, offspring2)

##### `multi_point_crossover(parent1, parent2, num_points=2, crossover_rate=0.8)`

Perform multi-point crossover.

**Parameters:**
- `parent1` (np.ndarray): First parent
- `parent2` (np.ndarray): Second parent
- `num_points` (int): Number of crossover points
- `crossover_rate` (float): Probability of crossover

**Returns:**
- Tuple of (offspring1, offspring2)

##### `uniform_crossover(parent1, parent2, crossover_rate=0.8, mixing_ratio=0.5)`

Perform uniform crossover.

**Parameters:**
- `parent1` (np.ndarray): First parent
- `parent2` (np.ndarray): Second parent
- `crossover_rate` (float): Probability of crossover
- `mixing_ratio` (float): Probability of taking gene from parent1

**Returns:**
- Tuple of (offspring1, offspring2)

##### `arithmetic_crossover(parent1, parent2, crossover_rate=0.8, alpha=0.5)`

Perform arithmetic crossover.

**Parameters:**
- `parent1` (np.ndarray): First parent
- `parent2` (np.ndarray): Second parent
- `crossover_rate` (float): Probability of crossover
- `alpha` (float): Blend parameter (0.0-1.0)

**Returns:**
- Tuple of (offspring1, offspring2)

### MutationOperator

Implements mutation operators for genetic algorithm.

#### Static Methods

##### `gaussian_mutation(individual, mutation_rate=0.1, mutation_strength=0.1, bounds=None)`

Apply Gaussian mutation to individual.

**Parameters:**
- `individual` (np.ndarray): Individual to mutate
- `mutation_rate` (float): Probability of mutating each gene
- `mutation_strength` (float): Standard deviation of Gaussian noise
- `bounds` (Optional[List[Tuple[float, float]]]): Bounds for each dimension

**Returns:**
- Mutated individual

##### `uniform_mutation(individual, mutation_rate=0.1, mutation_range=1.0, bounds=None)`

Apply uniform mutation to individual.

**Parameters:**
- `individual` (np.ndarray): Individual to mutate
- `mutation_rate` (float): Probability of mutating each gene
- `mutation_range` (float): Range of uniform mutation
- `bounds` (Optional[List[Tuple[float, float]]]): Bounds for each dimension

**Returns:**
- Mutated individual

##### `swap_mutation(individual, mutation_rate=0.1)`

Apply swap mutation to individual.

**Parameters:**
- `individual` (np.ndarray): Individual to mutate
- `mutation_rate` (float): Probability of mutation occurring

**Returns:**
- Mutated individual

##### `polynomial_mutation(individual, mutation_rate=0.1, eta=20.0, bounds=None)`

Apply polynomial mutation to individual.

**Parameters:**
- `individual` (np.ndarray): Individual to mutate
- `mutation_rate` (float): Probability of mutating each gene
- `eta` (float): Distribution index
- `bounds` (Optional[List[Tuple[float, float]]]): Bounds for each dimension

**Returns:**
- Mutated individual

**Raises:**
- `ValueError`: If bounds is None

## Configuration

### Configuration File Format

The algorithm uses YAML configuration files with the following structure:

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

### Configuration Parameters

- `population_size` (int): Population size (must be > 0)
- `max_generations` (int): Maximum generations (must be > 0)
- `crossover_rate` (float): Crossover probability (0.0-1.0)
- `mutation_rate` (float): Mutation probability (0.0-1.0)
- `elite_size` (int): Number of elite individuals (>= 0)
- `selection_type` (str): One of "tournament", "roulette", "rank"
- `crossover_type` (str): One of "single_point", "multi_point", "uniform", "arithmetic"
- `mutation_type` (str): One of "gaussian", "uniform", "swap", "polynomial"
- `random_seed` (int, optional): Random seed for reproducibility

## Examples

### Basic Optimization

```python
from src.main import GeneticAlgorithm
import numpy as np

ga = GeneticAlgorithm()

def objective(x):
    return np.sum(x ** 2)

result = ga.optimize(
    objective_function=objective,
    dimension=2,
    bounds=[(-10, 10), (-10, 10)]
)

print(f"Best solution: {result['best_solution']}")
print(f"Best fitness: {result['best_fitness']}")
```

### Custom Configuration

```python
ga = GeneticAlgorithm(config_path="custom_config.yaml")
result = ga.optimize(objective_function=my_function, dimension=3)
```

### Using Initial Population

```python
initial_pop = np.random.uniform(-10, 10, size=(50, 3))
result = ga.optimize(
    objective_function=my_function,
    dimension=3,
    initial_population=initial_pop
)
```
