# A* Pathfinding Algorithm

A Python implementation of A* pathfinding algorithm with customizable heuristics and visualization capabilities. This tool provides efficient pathfinding on grid-based maps with support for multiple heuristics and movement patterns.

## Project Title and Description

The A* Pathfinding tool implements the A* search algorithm for finding optimal paths in grid-based environments. It supports multiple heuristics (Manhattan, Euclidean, Chebyshev, Diagonal) and provides visualization capabilities to understand pathfinding behavior. The algorithm guarantees optimal paths when using admissible heuristics.

This tool solves the problem of finding the shortest path from a start position to a goal position while avoiding obstacles. A* is widely used in game development, robotics, navigation systems, and route planning applications.

**Target Audience**: Students learning pathfinding algorithms, developers studying A* and heuristic search, game developers, robotics engineers, educators teaching computer science concepts, and anyone interested in understanding pathfinding algorithms and their applications.

## Features

- A* algorithm implementation with priority queue
- Multiple heuristic functions (Manhattan, Euclidean, Chebyshev, Diagonal)
- 4-directional and 8-directional (diagonal) movement support
- Grid-based pathfinding with obstacle avoidance
- Path visualization (ASCII-based)
- Performance comparison between heuristics
- Comprehensive edge case handling
- Detailed step-by-step logging
- Multiple iterations support for accurate timing
- Input validation for grid and positions
- Error handling for invalid inputs

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation

### Step 1: Navigate to Project Directory

```bash
cd /path/to/python-algorithms/a-star-pathfinding
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

### Find Path

Find path from start to goal:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 --heuristic manhattan --mode find
```

### Find Path with Obstacles

Find path avoiding obstacles:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 -o 1-1 2-2 3-3 --mode find
```

### Find Path with Diagonal Movement

Allow diagonal movement:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 --diagonal --mode find
```

### Visualize Path

Visualize grid and path:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode visualize
```

### Compare Heuristics

Compare different heuristics:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode compare
```

### Multiple Iterations

Run multiple iterations for timing:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode compare --iterations 1000
```

### Generate Report

Generate performance report:

```bash
python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode compare --report report.txt
```

### Command-Line Arguments

- `-g, --grid`: Grid size as 'rows-cols' (e.g., '10x10')
- `-s, --start`: Start position as 'x-y' (e.g., '0-0')
- `-e, --end`: End position as 'x-y' (e.g., '9-9')
- `-o, --obstacles`: Obstacles as 'x-y' pairs (e.g., '1-1 2-2')
- `-h, --heuristic`: Heuristic function - manhattan, euclidean, chebyshev, or diagonal (default: manhattan)
- `-d, --diagonal`: Allow diagonal movement
- `-c, --config`: Path to configuration file (default: config.yaml)
- `-m, --mode`: Operation mode - find, compare, or visualize (default: find)
- `-i, --iterations`: Number of iterations for timing (default: 1)
- `-r, --report`: Output path for performance report

### Common Use Cases

**Basic Pathfinding:**
1. Run: `python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode find`
2. Review path and statistics
3. Understand algorithm behavior

**Pathfinding with Obstacles:**
1. Define obstacles: `python src/main.py -g 10x10 -s 0-0 -e 9-9 -o 1-1 2-2 --mode find`
2. Review how algorithm navigates around obstacles
3. Verify optimal path

**Heuristic Comparison:**
1. Compare heuristics: `python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode compare`
2. Review performance differences
3. Choose optimal heuristic for your use case

**Visualization:**
1. Visualize path: `python src/main.py -g 10x10 -s 0-0 -e 9-9 --mode visualize`
2. See grid with path marked
3. Understand path structure

## Project Structure

```
a-star-pathfinding/
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

- `src/main.py`: Contains `AStarPathfinder` and `Node` classes
- `config.yaml`: Configuration file with logging settings
- `requirements.txt`: Python package dependencies
- `tests/test_main.py`: Unit tests for the main module
- `logs/`: Directory for application log files

## Algorithm Details

### A* Algorithm

**Definition:**
A* is an informed search algorithm that finds the shortest path from a start node to a goal node. It uses a best-first search approach, evaluating nodes by combining the cost to reach the node (g) and an estimate of the cost to reach the goal (h).

**Formula:**
- f(n) = g(n) + h(n)
  - g(n): Actual cost from start to node n
  - h(n): Heuristic estimate from node n to goal
  - f(n): Estimated total cost through node n

**How It Works:**
1. Initialize open set with start node
2. While open set is not empty:
   - Select node with minimum f-value
   - If node is goal, reconstruct and return path
   - Add node to closed set
   - Explore neighbors, update costs, add to open set
3. If open set empty, no path exists

**Properties:**
- Optimal: Guarantees shortest path if heuristic is admissible
- Complete: Will find path if one exists
- Efficient: Explores fewer nodes than Dijkstra's algorithm

**Applications:**
- Game development (NPC pathfinding)
- Robotics (navigation)
- GPS navigation systems
- Network routing
- Puzzle solving

### Heuristic Functions

**Manhattan Distance:**
- Formula: |x1 - x2| + |y1 - y2|
- Best for: 4-directional movement (up, down, left, right)
- Admissible: Yes
- Consistent: Yes

**Euclidean Distance:**
- Formula: sqrt((x1 - x2)² + (y1 - y2)²)
- Best for: Continuous movement, real-world distances
- Admissible: Yes
- Consistent: Yes

**Chebyshev Distance:**
- Formula: max(|x1 - x2|, |y1 - y2|)
- Best for: 8-directional movement (including diagonals)
- Admissible: Yes
- Consistent: Yes

**Diagonal Distance:**
- Formula: (dx + dy) + (√2 - 2) * min(dx, dy)
- Best for: 8-directional movement with different costs
- Admissible: Yes
- Consistent: Yes

### Edge Cases Handled

- Empty grid
- Start equals goal
- No path exists (blocked by obstacles)
- Start or goal is obstacle
- Invalid positions (out of bounds)
- Large grids
- Many obstacles
- Diagonal vs non-diagonal movement

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
- A* algorithm with various grids
- All heuristic functions
- Pathfinding with and without obstacles
- Edge cases (no path, start=goal, invalid positions)
- Performance comparison functionality
- Error handling (invalid inputs, obstacles at start/goal)
- Report generation
- Visualization
- Input validation

## Troubleshooting

### Common Issues

**No path found:**
- Goal may be unreachable due to obstacles
- Check that start and goal are not obstacles
- Verify grid connectivity

**ValueError: Start/Goal position out of grid bounds:**
- Positions must be within grid dimensions
- Grid is 0-indexed
- Check position coordinates

**ValueError: Start/Goal position is an obstacle:**
- Start and goal must be free cells (value 0)
- Remove obstacles from start/goal positions

**Invalid heuristic:**
- Choose from: manhattan, euclidean, chebyshev, diagonal
- Check spelling and case

**Import Errors:**
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version (requires 3.8+)
- Verify virtual environment is activated

### Error Messages

**"Grid cannot be empty"**: Grid must have at least one row and column.

**"Start position X out of grid bounds"**: Start position must be within grid dimensions.

**"Goal position X out of grid bounds"**: Goal position must be within grid dimensions.

**"Start position is an obstacle"**: Start position must be a free cell (0).

**"Goal position is an obstacle"**: Goal position must be a free cell (0).

**"Unknown heuristic"**: Heuristic must be one of: manhattan, euclidean, chebyshev, diagonal.

**"Configuration file not found"**: The config.yaml file doesn't exist. Create it or specify path with `-c` option.

### Best Practices

1. **Choose appropriate heuristic** based on movement type
2. **Use Manhattan** for 4-directional movement
3. **Use Chebyshev or Diagonal** for 8-directional movement
4. **Use Euclidean** for continuous/real-world distances
5. **Compare heuristics** to find optimal for your use case
6. **Use diagonal movement** when appropriate (may find shorter paths)
7. **Visualize paths** to understand algorithm behavior
8. **Handle no-path cases** gracefully in applications

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
