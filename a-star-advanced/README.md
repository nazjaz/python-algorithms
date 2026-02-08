# A* Pathfinding Algorithm with Multiple Heuristics and Bidirectional Search

A Python implementation of A* pathfinding algorithm with configurable heuristics and bidirectional search optimization. This tool provides comprehensive pathfinding capabilities for grid-based navigation with detailed logging and performance tracking.

## Project Title and Description

The A* Pathfinding tool implements the A* search algorithm with multiple heuristic functions and bidirectional search optimization. It provides configurable heuristics to adapt to different movement patterns and uses bidirectional search to reduce the search space for faster pathfinding.

This tool solves the problem of finding optimal paths in grid-based environments, particularly useful for game development, robotics, and navigation systems. It offers flexibility through multiple heuristic functions and optimization through bidirectional search, making it adaptable to various pathfinding scenarios.

**Target Audience**: Game developers implementing pathfinding, robotics engineers planning robot navigation, students learning search algorithms, and developers implementing pathfinding solutions.

## Features

- Multiple heuristic functions (Manhattan, Euclidean, Chebyshev, Diagonal, Octile, Zero)
- Bidirectional search optimization for faster pathfinding
- Support for 4-directional and 8-directional movement
- Configurable movement costs for straight and diagonal moves
- Grid-based graph representation
- Comprehensive logging and path tracking
- Configurable algorithm parameters via YAML
- Detailed performance metrics (nodes explored, path cost, path length)
- Support for obstacles and blocked cells
- Path reconstruction and visualization support

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/a-star-advanced
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
a_star:
  heuristic: "manhattan"
  allow_diagonal: true
  bidirectional: false
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
   - Admissible but may explore more nodes
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
   - Equivalent to Dijkstra's algorithm
   - Guaranteed optimal but slower
   - Useful for comparison

### Bidirectional Search

Bidirectional search runs two A* searches simultaneously:
- Forward search from start to goal
- Backward search from goal to start
- Stops when searches meet
- Reduces search space significantly
- Faster for long paths

## Usage

### Basic Usage

```python
from src.main import AStar, GridGraph
import numpy as np

# Create grid (0 = walkable, 1 = obstacle)
grid = np.array([
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
])

# Initialize
astar = AStar(config_path="config.yaml")
graph = GridGraph(grid, allow_diagonal=True)

# Find path
start = (0, 0)
goal = (4, 3)
result = astar.search(graph, start, goal)

if result['found']:
    print(f"Path found: {result['path']}")
    print(f"Cost: {result['cost']}")
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
from src.main import AStar, GridGraph

grid = np.zeros((10, 10))
graph = GridGraph(grid, allow_diagonal=True)

# Test different heuristics
heuristics = ['manhattan', 'euclidean', 'chebyshev', 'diagonal', 'octile']

for heuristic_name in heuristics:
    config = {
        'a_star': {'heuristic': heuristic_name, 'bidirectional': False},
        'logging': {'level': 'WARNING', 'file': 'logs/test.log'}
    }
    # Save config and test...
```

### Bidirectional Search Example

```python
import numpy as np
from src.main import AStar, GridGraph

grid = np.zeros((20, 20))
graph = GridGraph(grid, allow_diagonal=True)

# Enable bidirectional search
astar = AStar(config_path="config.yaml")
# Set bidirectional=True in config or modify code

result = astar.search(graph, (0, 0), (19, 19))
print(f"Nodes explored: {result['nodes_explored']}")
```

### Custom Grid Creation

```python
import numpy as np
from src.main import AStar, GridGraph

# Create custom grid with obstacles
grid = np.zeros((10, 10))
grid[3:6, 3:6] = 1  # Add obstacle block
grid[7, 2:8] = 1    # Add obstacle line

graph = GridGraph(
    grid,
    allow_diagonal=True,
    movement_cost={'straight': 1.0, 'diagonal': 1.5}
)

astar = AStar()
result = astar.search(graph, (0, 0), (9, 9))
```

## Project Structure

```
a-star-advanced/
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

- `src/main.py`: Core implementation containing `AStar`, `GridGraph`, and `Heuristic` classes
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
- Unidirectional A* search
- Bidirectional A* search
- Grid validation and neighbor generation
- Edge cases and error handling
- Configuration loading and validation

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Start node is not valid`

**Solution**: Ensure start node coordinates are within grid bounds and not an obstacle

**Issue**: `ValueError: Goal node is not valid`

**Solution**: Ensure goal node coordinates are within grid bounds and not an obstacle

**Issue**: No path found

**Solution**: 
- Check if path exists (no obstacles blocking all routes)
- Verify grid has walkable cells (0 values)
- Try different heuristic
- Enable bidirectional search

**Issue**: Path is suboptimal

**Solution**:
- Ensure heuristic is admissible (never overestimates)
- Check movement costs are correct
- Verify diagonal costs if using diagonal movement

**Issue**: Algorithm is slow

**Solution**:
- Enable bidirectional search
- Use more informed heuristic (Manhattan for grids)
- Reduce grid size if possible
- Check for unnecessary obstacles

### Error Messages

- `FileNotFoundError`: Configuration file missing - check file path
- `ValueError`: Invalid node coordinates or heuristic name
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

### A* Algorithm Overview

A* is an informed search algorithm that:
1. Uses f(n) = g(n) + h(n) where:
   - g(n) = cost from start to current node
   - h(n) = estimated cost from current to goal (heuristic)
   - f(n) = estimated total cost
2. Maintains priority queue ordered by f(n)
3. Explores most promising nodes first
4. Guarantees optimal path if heuristic is admissible

### Heuristic Admissibility

A heuristic is admissible if it never overestimates the true cost:
- Manhattan: Admissible for 4-directional movement
- Euclidean: Admissible but may explore more nodes
- Chebyshev: Admissible for 8-directional with equal costs
- Diagonal/Octile: Admissible for 8-directional with different costs

### Bidirectional Search Benefits

Bidirectional search:
- Reduces search space from O(b^d) to O(b^(d/2))
- Where b = branching factor, d = depth
- Meets in the middle for faster convergence
- Particularly effective for long paths

### Performance Considerations

- Algorithm complexity: O(b^d) worst case, O(b^(d/2)) with bidirectional
- Memory usage: O(b^d) for unidirectional, O(2*b^(d/2)) for bidirectional
- For large grids, consider:
  - Using bidirectional search
  - Choosing appropriate heuristic
  - Reducing grid resolution if possible
  - Using hierarchical pathfinding for very large maps

## License

This project is part of the python-algorithms collection. See LICENSE file in parent directory for details.
