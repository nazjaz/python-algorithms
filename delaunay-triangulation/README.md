# Delaunay Triangulation with Incremental Insertion and Edge Flipping

A Python implementation of Delaunay triangulation using incremental insertion and Lawson's edge flipping algorithm.

## Project Title and Description

This project implements Delaunay triangulation, a fundamental algorithm in computational geometry that creates a triangulation of a set of points such that no point is inside the circumcircle of any triangle. The implementation uses incremental insertion to add points one by one and Lawson's edge flipping algorithm to maintain the Delaunay property (empty circle property).

Delaunay triangulation has applications in computer graphics, mesh generation, terrain modeling, and finite element analysis.

**Target Audience**: Developers working with computational geometry, computer graphics, mesh generation, and anyone needing efficient triangulation algorithms.

## Features

- Incremental insertion algorithm for adding points one by one
- Lawson's edge flipping algorithm to maintain Delaunay property
- Empty circle property verification
- Triangle and edge data structures
- Circumcircle computation for triangles
- Point location in triangles
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/delaunay-triangulation
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

#### Construct Delaunay Triangulation

```bash
python src/main.py --points "0,0;1,0;0.5,1"
```

Output:
```
Input points: [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
Number of points: 3

Delaunay Triangulation:
Number of triangles: 1
  Triangle 1: (0, 1, 2) -> (0.0, 0.0), (1.0, 0.0), (0.5, 1.0)
```

#### Show Edges

```bash
python src/main.py --points "0,0;1,0;0.5,1" --edges
```

Output:
```
Edges: 3
  Edge 1: (0, 1) -> (0.0, 0.0), (1.0, 0.0)
  Edge 2: (0, 2) -> (0.0, 0.0), (0.5, 1.0)
  Edge 3: (1, 2) -> (1.0, 0.0), (0.5, 1.0)
```

### Programmatic Usage

```python
from src.main import DelaunayTriangulation

# Create Delaunay triangulation
points = [(0, 0), (1, 0), (0.5, 1)]
dt = DelaunayTriangulation(points)

# Construct triangulation
triangles = dt.construct()
print(f"Triangles: {triangles}")

# Get edges
edges = dt.get_edges()
print(f"Edges: {edges}")

# Get triangles
triangles = dt.get_triangles()
print(f"Triangles: {triangles}")
```

### Common Use Cases

1. **Construct triangulation**
   ```bash
   python src/main.py --points "0,0;1,0;0.5,1;1,1"
   ```

2. **View edges**
   ```bash
   python src/main.py --points "0,0;1,0;0.5,1" --edges
   ```

## Project Structure

```
delaunay-triangulation/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main Delaunay triangulation implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `DelaunayTriangulation` class with all core functionality for triangulation.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various point configurations.
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
pytest tests/test_main.py::TestDelaunayTriangulation::test_construct_three_points
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Triangulation construction
- Edge flipping
- Circumcircle computation
- Point location
- Edge cases (collinear points, degenerate cases, etc.)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/delaunay-triangulation"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Incorrect triangulation results

**Solution**: 
- Check that points are not all collinear
- Ensure at least 3 points for triangulation
- Verify point coordinates are correct
- The algorithm may need refinement for complex cases

**Issue**: Missing triangles

**Solution**: 
- The incremental insertion algorithm may need refinement for edge cases
- For production use, consider using libraries like scipy.spatial.Delaunay

### Error Messages

- **"Each point must have 2 coordinates"**: Points must be specified as x,y.

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

### Incremental Insertion Algorithm

1. **Sort points**: Sort points by x-coordinate (or use random order)
2. **Initial triangle**: Create first triangle from first three points
3. **Insert points**: For each remaining point:
   - Find triangles whose circumcircles contain the point (bad triangles)
   - Remove bad triangles, creating a cavity
   - Fill cavity by connecting point to boundary edges
   - Legalize edges using edge flipping

### Lawson's Edge Flipping Algorithm

For each edge that might violate Delaunay property:
1. Check if edge is shared by two triangles
2. Check if opposite vertex of one triangle is inside circumcircle of other
3. If so, flip the edge (swap diagonal in quadrilateral)
4. Recursively check new edges

### Empty Circle Property

A triangulation is Delaunay if no point lies inside the circumcircle of any triangle. This property ensures:
- Maximizes minimum angle (avoids skinny triangles)
- Uniqueness (for points in general position)
- Optimal for many applications

### Time Complexity

- **Incremental insertion**: O(n²) worst case, O(n log n) expected
- **Edge flipping**: O(n) per point insertion in practice
- **Overall**: O(n²) worst case, O(n log n) expected for random points

### Space Complexity

- **Triangles**: O(n) where n is number of points
- **Edges**: O(n) edges
- **Overall**: O(n) space

## Mathematical Background

### Delaunay Triangulation

Given a set of points P, a Delaunay triangulation is a triangulation DT(P) such that:
- No point in P is inside the circumcircle of any triangle in DT(P)
- Maximizes the minimum angle of all triangles
- Dual to Voronoi diagram

### Properties

- **Empty circle property**: No point lies inside any triangle's circumcircle
- **Max-min angle property**: Maximizes minimum angle among all triangulations
- **Uniqueness**: Unique for points in general position (no four cocircular points)
- **Convex hull**: Outer boundary is the convex hull of points

### Circumcircle

The circumcircle of a triangle is the unique circle passing through all three vertices. Its center (circumcenter) is the intersection of perpendicular bisectors.

## Applications

- **Computer Graphics**: Mesh generation, terrain modeling
- **Finite Element Analysis**: Mesh generation for numerical methods
- **Geographic Information Systems**: Spatial analysis, interpolation
- **Computer Vision**: Feature matching, image processing
- **Robotics**: Path planning, obstacle representation

## Limitations

This implementation has some limitations:
- May need refinement for degenerate cases (collinear points, cocircular points)
- Edge case handling could be improved
- For production use with large point sets, consider:
  - `scipy.spatial.Delaunay` for optimized implementation
  - More sophisticated point location algorithms
  - Better handling of boundary cases

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
