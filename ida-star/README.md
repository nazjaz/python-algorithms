# Iterative Deepening A* (IDA*) Pathfinding Algorithm

A Python implementation of Iterative Deepening A* (IDA*) pathfinding algorithm with memory-efficient depth-first search and configurable heuristics. This tool provides optimal pathfinding with minimal memory usage compared to standard A* algorithm.

## Project Title and Description

The IDA* Pathfinding tool implements the Iterative Deepening A* search algorithm, a memory-efficient variant of A* that uses depth-first search with iterative deepening. It provides configurable heuristics to adapt to different movement patterns while using only O(d) memory space where d is the depth of the solution.

This tool solves the problem of finding optimal paths in memory-constrained environments where standard A* may require too much memory. It offers the same optimality guarantees as A* while using significantly less memory, making it ideal for embedded systems, large-scale pathfinding, and memory-sensitive applications.

**Target Audience**: Game developers implementing pathfinding in memory-constrained environments, robotics engineers working with limited memory, students learning search algorithms, and developers implementing memory-efficient pathfinding solutions.

## Features

- Memory-efficient pathfinding using depth-first search
- Iterative deepening with f-cost limits
- Multiple heuristic functions (Manhattan, Euclidean, Chebyshev, Diagonal, Octile, Zero)
- Support for 4-directional and 8-directional movement
- Configurable movement costs for straight and diagonal moves
- Grid-based graph representation
- Comprehensive logging and iteration tracking
- Configurable algorithm parameters via YAML
- Detailed performance metrics (iterations, nodes explored, path cost)
- Support for obstacles and blocked cells
- Optimal path guarantees (when heuristic is admissible)

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/ida-star
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
ida_star:
  heuristic: "manhattan"
  allow_diagonal: true
  max_iterations: 1000
  movement_cost:
    straight: 1.0
    diagonal: 1.414

logging:
  level: "INFO"
  file: "logs/app.log"
```

### Heuristic Functions

Six heuristic functions are available:

1. **Manhattan Distance (L1 norm)**: `|x1-x2| + |y1-y2|`
   - Best for 4-directional movement (no diagonals)
   - Admissible and consistent
   - Most commonly used

2. **Euclidean Distance (L2 norm)**: `√((x1-x2)² + (y1-y2)²)`
   - Best for continuous movement
   - Admissible but may require more iterations
   - Good for smooth paths

3. **Chebyshev Distance (L∞ norm)**: `max(|x1-x2|, |y1-y2|)`
   - Best for 8-directional movement with equal costs
   - Admissible and consistent
   - Efficient for diagonal movement

4. **Diagonal Distance (Octile)**: Combines straight and diagonal costs
   - Best for 8-directional movement with different costs
   - Admissible and consistent
   - Accounts for diagonal movement cost

5. **Octile Distance**: Optimized for 8-directional movement
   - Similar to diagonal distance
   - Efficient computation
   - Good for grid-based games

6. **Zero Heuristic**: Always returns 0
   - Equivalent to iterative deepening DFS
   - Guaranteed optimal but slower
   - Useful for comparison

### Memory Efficiency

IDA* uses O(d) memory space where d is the depth of the solution:
- Only stores current path in recursion stack
- No open/closed sets like A*
- Memory usage independent of branching factor
- Ideal for memory-constrained environments

### Algorithm Overview

IDA* works by:
1. Starting with f-limit = h(start)
2. Performing depth-first search, pruning nodes with f > f-limit
3. If goal found, return path
4. If not found, set f-limit to minimum f-value that exceeded limit
5. Repeat until goal found or max iterations reached

## Usage

### Basic Usage

```python
from src.main import IDAStar, GridGraph
import numpy as np

# Create grid (0 = walkable, 1 = obstacle)
grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
])

# Initialize
ida = IDAStar(config_path="config.yaml")
graph = GridGraph(grid, allow_diagonal=True)

# Find path
start = (0, 0)
goal = (4, 3)
result = ida.search(graph, start, goal)

if result['found']:
    print(f"Path found: {result['path']}")
    print(f"Cost: {result['cost']}")
    print(f"Iterations: {result['iterations']}")
    print(f"Nodes explored: {result['nodes_explored']}")
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

### Advanced Example: Different Heuristics

```python
import numpy as np
from src.main import IDAStar, GridGraph

grid = np.zeros((10, 10))
graph = GridGraph(grid, allow_diagonal=True)

# Test different heuristics
heuristics = ['manhattan', 'euclidean', 'chebyshev', 'diagonal', 'octile']

for heuristic_name in heuristics:
    config = {
        'ida_star': {'heuristic': heuristic_name, 'max_iterations': 100},
        'logging': {'level': 'WARNING', 'file': 'logs/test.log'}
    }
    # Save config and test...
```

### Memory Comparison Example

```python
import numpy as np
from src.main import IDAStar, GridGraph

# Large grid to demonstrate memory efficiency
grid = np.zeros((50, 50))
graph = GridGraph(grid, allow_diagonal=True)

ida = IDAStar()
result = ida.search(graph, (0, 0), (49, 49))

print(f"Path found: {result['found']}")
print(f"Iterations: {result['iterations']}")
print(f"Memory efficient: Only stores current path")
```

### Custom Grid Creation

```python
import numpy as np
from src.main import IDAStar, GridGraph

# Create custom grid with obstacles
grid = np.zeros((10, 10))
grid[3:6, 3:6] = 1  # Add obstacle block
grid[7, 2:8] = 1    # Add obstacle line

graph = GridGraph(
    grid,
    allow_diagonal=True,
    movement_cost={'straight': 1.0, 'diagonal': 1.5}
)

ida = IDAStar()
result = ida.search(graph, (0, 0), (9, 9))
```

## Project Structure

```
ida-star/
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

- `src/main.py`: Core implementation containing `IDAStar`, `GridGraph`, and `Heuristic` classes
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
- All heuristic functions
- IDA* search algorithm
- Depth-limited search
- Grid validation and neighbor generation
- Edge cases and error handling
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Start node is not valid`

**Solution**: Ensure start node coordinates are within grid bounds and not an obstacle

**Issue**: `ValueError: Goal node is not valid`

**Solution**: Ensure goal node coordinates are within grid bounds and not an obstacle

**Issue**: Maximum iterations reached

**Solution**: 
- Check if path exists (no obstacles blocking all routes)
- Verify grid has walkable cells (0 values)
- Try different heuristic
- Increase max_iterations in config

**Issue**: Algorithm is slow

**Solution**:
- Use more informed heuristic (Manhattan for grids)
- Reduce grid size if possible
- Check for unnecessary obstacles
- Consider using A* for faster results (if memory allows)

**Issue**: Path is suboptimal

**Solution**:
- Ensure heuristic is admissible (never overestimates)
- Check movement costs are correct
- Verify diagonal costs if using diagonal movement

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid node coordinates or heuristic name
- `yaml.YAMLError`: Invalid YAML syntax - validate config file

## IDA* vs A* Comparison

### Memory Usage
- **IDA***: O(d) where d is solution depth
- **A***: O(b^d) where b is branching factor

### Time Complexity
- **IDA***: O(b^d) - may explore nodes multiple times
- **A***: O(b^d) - explores each node once

### When to Use IDA*
- Memory-constrained environments
- Large search spaces
- Embedded systems
- When memory is more important than speed

### When to Use A*
- Memory is not a constraint
- Need fastest pathfinding
- Small to medium search spaces
- Real-time applications where speed matters

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

### IDA* Algorithm Overview

IDA* is a memory-efficient variant of A* that:
1. Uses iterative deepening with f-cost limits
2. Performs depth-first search up to f-limit
3. Prunes nodes with f > f-limit
4. Increases f-limit and repeats if goal not found
5. Guarantees optimal path if heuristic is admissible

### Depth-Limited Search

The depth-limited search:
- Explores nodes in DFS order
- Tracks f-cost (g + h) for each node
- Prunes when f > f-limit
- Returns minimum f-cost that exceeded limit
- Uses visited set per iteration to avoid cycles

### Iterative Deepening

Iterative deepening:
- Starts with f-limit = h(start)
- Increases f-limit to next minimum exceeded value
- Repeats until goal found or max iterations
- May explore same nodes multiple times
- Trades time for memory efficiency

### Heuristic Admissibility

A heuristic is admissible if it never overestimates the true cost:
- Manhattan: Admissible for 4-directional movement
- Euclidean: Admissible but may require more iterations
- Chebyshev: Admissible for 8-directional with equal costs
- Diagonal/Octile: Admissible for 8-directional with different costs

## Performance Considerations

- Algorithm complexity: O(b^d) worst case
- Memory usage: O(d) where d is solution depth
- For large grids, consider:
  - Using appropriate heuristic
  - Reducing grid resolution if possible
  - Using hierarchical pathfinding for very large maps
  - Switching to A* if memory allows and speed is critical

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
