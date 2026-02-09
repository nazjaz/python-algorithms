# Voronoi Diagram Construction using Fortune's Algorithm

A Python implementation of Voronoi diagram construction inspired by Fortune's sweep line algorithm.

## Project Title and Description

This project implements a Voronoi diagram construction algorithm based on Fortune's sweep line algorithm concepts. A Voronoi diagram partitions a plane into regions based on distance to a set of points (sites), where each region contains all points closer to one site than to any other.

**Note**: This is a simplified implementation that demonstrates the core concepts of Fortune's algorithm. A full implementation would require more complex data structures (balanced BST for beach line) and edge handling. The implementation finds Voronoi vertices and constructs edges between them.

**Target Audience**: Developers working with computational geometry, computer graphics, competitive programming, and anyone needing Voronoi diagram computation.

## Features

- Voronoi diagram construction from site points
- Voronoi vertex computation (circumcenters of site triples)
- Edge construction between vertices
- Voronoi cell computation for each site
- Point-in-cell testing
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/voronoi-diagram-fortune
```

### Step 2: Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Note: This project has no external dependencies for core functionality, but pytest is included for testing.

## Configuration

This project does not require configuration files or environment variables. All functionality is available through the command-line interface or by importing the classes directly.

## Usage

### Command-Line Interface

#### Construct Voronoi Diagram

```bash
python src/main.py --sites "0,0;1,1;2,0"
```

Output:
```
Input sites: [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0)]
Number of sites: 3

Voronoi Diagram:
Number of vertices: 1
Number of edges: 0
```

#### Show Voronoi Cells

```bash
python src/main.py --sites "0,0;1,1;2,0" --cells
```

#### Test Point in Cell

```bash
python src/main.py --sites "0,0;1,1;2,0" --test-point "0.5,0.5"
```

### Programmatic Usage

```python
from src.main import VoronoiDiagram

# Create Voronoi diagram
sites = [(0, 0), (1, 1), (2, 0)]
vd = VoronoiDiagram(sites)

# Construct diagram
edges = vd.construct()
print(f"Vertices: {vd.vertices}")
print(f"Edges: {edges}")

# Get Voronoi cells
cells = vd.get_voronoi_cells()
for site, vertices in cells.items():
    print(f"Site {site}: {len(vertices)} vertices")

# Find cell for a point
cell_site = vd.get_cell_for_point((0.5, 0.5))
print(f"Point is in cell of site: {cell_site}")
```

### Common Use Cases

1. **Construct Voronoi diagram**
   ```bash
   python src/main.py --sites "0,0;1,1;2,0;1,-1"
   ```

2. **Find cell for a point**
   ```bash
   python src/main.py --sites "0,0;2,0;1,2" --test-point "1,1"
   ```

## Project Structure

```
voronoi-diagram-fortune/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main Voronoi diagram implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `VoronoiDiagram` class with all core functionality for Voronoi diagram construction.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various site configurations.
- **docs/API.md**: Detailed API documentation for all classes and methods.
- **logs/**: Directory for log files (if logging to files is enabled).

## Testing

### Run All Tests

```bash
pytest tests/
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test

```bash
pytest tests/test_main.py::TestVoronoiDiagram::test_construct_three_sites
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Voronoi diagram construction
- Vertex and edge computation
- Voronoi cell computation
- Point-in-cell testing
- Edge cases (collinear points, single site, etc.)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/voronoi-diagram-fortune"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: No edges are generated

**Solution**: 
- This is a simplified implementation
- Edges are constructed between vertices that share common sites
- For a full implementation, consider using a library like scipy.spatial

**Issue**: Incorrect Voronoi cells

**Solution**: 
- Verify site coordinates are correct
- Check for duplicate sites
- The algorithm finds vertices as circumcenters of site triples

### Error Messages

- **"Each site must have 2 coordinates"**: Sites must be specified as x,y.
- **"Test point must have 2 coordinates"**: Test point must be specified as x,y.

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov
   ```
4. Create a feature branch: `git checkout -b feature/your-feature-name`

### Code Style Guidelines

- Follow PEP 8 strictly
- Maximum line length: 88 characters
- Use type hints for all functions
- Write docstrings for all public functions and classes
- Run tests before committing

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Write clear commit messages following conventional commit format
4. Submit pull request with description of changes

## Algorithm Details

### Simplified Fortune's Algorithm

This implementation uses a simplified approach:

1. **Find Vertices**: For each triple of sites, compute the circumcenter (potential Voronoi vertex)
2. **Validate Vertices**: Check if circumcenter is equidistant from its three sites and not closer to any other site
3. **Construct Edges**: Connect vertices that share two common sites
4. **Compute Cells**: Group vertices by their closest sites

### Fortune's Algorithm (Full)

The full Fortune's algorithm uses:
- **Sweep Line**: Moves from top to bottom (or bottom to top)
- **Beach Line**: Set of parabolic arcs (intersection of plane with cones)
- **Event Queue**: Site events and circle events
- **Data Structures**: Balanced BST for beach line, priority queue for events

**Time Complexity**: O(n log n) where n is number of sites

### Circumcenter Computation

For three points A, B, C, the circumcenter is the center of the circle passing through all three points. It's computed using the perpendicular bisectors of the triangle sides.

### Time Complexity

- **Simplified algorithm**: O(n³) for finding vertices, O(v²) for edges where v is number of vertices
- **Full Fortune's algorithm**: O(n log n) time, O(n) space

### Space Complexity

- **Simplified algorithm**: O(n + v) where v is number of vertices
- **Full Fortune's algorithm**: O(n) space

## Mathematical Background

### Voronoi Diagram

Given a set of sites S = {s₁, s₂, ..., sₙ}, the Voronoi diagram partitions the plane into regions:
- Each region V(sᵢ) contains all points closer to sᵢ than to any other site
- Boundaries are formed by perpendicular bisectors between pairs of sites
- Vertices are points equidistant from three or more sites

### Properties

- Each Voronoi cell is a convex polygon
- Voronoi vertices are circumcenters of Delaunay triangles
- Voronoi diagram is dual to Delaunay triangulation
- Number of vertices ≤ 2n - 5 (for n sites)

## Applications

- **Computer Graphics**: Procedural generation, texture synthesis
- **Geographic Information Systems**: Service area analysis, territory boundaries
- **Robotics**: Path planning, coverage problems
- **Biology**: Cell division modeling, crystal growth
- **Computer Science**: Nearest neighbor queries, clustering

## Limitations

This implementation is simplified and has limitations:
- May not find all Voronoi edges (especially unbounded edges)
- Edge construction is basic
- For production use, consider libraries like:
  - `scipy.spatial.Voronoi`
  - `shapely` for geometric operations
  - Full Fortune's algorithm implementation

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
