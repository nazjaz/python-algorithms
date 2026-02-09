# Convex Hull Algorithms

A Python implementation of convex hull algorithms including Graham scan, Andrew's monotone chain for 2D, and gift wrapping algorithm for 3D convex hull computation.

## Project Title and Description

This project implements multiple convex hull algorithms for computing the smallest convex polygon (2D) or polyhedron (3D) that contains all given points. The implementation includes Graham scan and Andrew's monotone chain algorithms for 2D convex hulls, and a gift wrapping algorithm for 3D convex hulls.

Convex hull algorithms are fundamental in computational geometry with applications in computer graphics, pattern recognition, geographic information systems, and optimization problems.

**Target Audience**: Developers working with computational geometry, computer graphics, competitive programming, and anyone needing efficient convex hull computation.

## Features

- Graham scan algorithm for 2D convex hull (O(n log n))
- Andrew's monotone chain algorithm for 2D convex hull (O(n log n))
- Gift wrapping algorithm for 3D convex hull
- 2D hull area and perimeter computation
- 3D hull volume and surface area computation
- Point-in-hull testing for 2D
- Support for collinear and coplanar points
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/convex-hull-algorithms
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

#### 2D Convex Hull (Graham Scan)

```bash
python src/main.py --points-2d "0,0;1,1;2,0;1,0.5" --algorithm graham
```

Output:
```
Input points (2D): [(0.0, 0.0), (1.0, 1.0), (2.0, 0.0), (1.0, 0.5)]
Algorithm: graham
Convex hull points: [(0.0, 0.0), (2.0, 0.0), (1.0, 1.0)]
```

#### 2D Convex Hull (Andrew's Monotone Chain)

```bash
python src/main.py --points-2d "0,0;1,1;2,0;1,0.5" --algorithm andrews
```

#### Compute Area and Perimeter

```bash
python src/main.py --points-2d "0,0;1,0;1,1;0,1" --area --perimeter
```

Output:
```
Convex hull points: [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
Area: 1.00
Perimeter: 4.00
```

#### Check if Point is Inside Hull

```bash
python src/main.py --points-2d "0,0;1,0;1,1;0,1" --check-point "0.5,0.5"
```

#### 3D Convex Hull

```bash
python src/main.py --points-3d "0,0,0;1,0,0;0,1,0;0,0,1" --volume --surface-area
```

Output:
```
Input points (3D): [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]
Convex hull faces: [(0, 1, 2), (0, 1, 3), (1, 2, 3), ...]
Number of faces: 4
Volume: 0.17
Surface area: 1.87
```

### Programmatic Usage

```python
from src.main import ConvexHull

# Create ConvexHull instance
ch = ConvexHull()

# 2D convex hull (Graham scan)
points_2d = [(0, 0), (1, 1), (2, 0), (1, 0.5)]
hull = ch.graham_scan_2d(points_2d)
print(f"Hull points: {hull}")

# 2D convex hull (Andrew's monotone chain)
hull = ch.andrews_monotone_chain_2d(points_2d)
print(f"Hull points: {hull}")

# Compute area and perimeter
area = ch.hull_area_2d(hull)
perimeter = ch.hull_perimeter_2d(hull)
print(f"Area: {area}, Perimeter: {perimeter}")

# Check if point is inside
is_inside = ch.is_point_inside_2d((0.5, 0.5), hull)
print(f"Point inside: {is_inside}")

# 3D convex hull
points_3d = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
faces = ch.gift_wrapping_3d(points_3d)
print(f"Hull faces: {faces}")

# Compute volume and surface area
volume = ch.hull_volume_3d(points_3d, faces)
surface_area = ch.hull_surface_area_3d(points_3d, faces)
print(f"Volume: {volume}, Surface area: {surface_area}")
```

### Common Use Cases

1. **Compute 2D Convex Hull**
   ```bash
   python src/main.py --points-2d "0,0;1,1;2,0" --algorithm graham
   ```

2. **Compute Area and Perimeter**
   ```bash
   python src/main.py --points-2d "0,0;1,0;1,1;0,1" --area --perimeter
   ```

3. **3D Convex Hull**
   ```bash
   python src/main.py --points-3d "0,0,0;1,0,0;0,1,0;0,0,1" --volume
   ```

## Project Structure

```
convex-hull-algorithms/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main convex hull implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `ConvexHull` class with all core functionality for 2D and 3D convex hull computation.
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
pytest tests/test_main.py::TestConvexHull::test_graham_scan_2d_simple
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Both 2D algorithms (Graham scan and Andrew's)
- 3D convex hull computation
- Area, perimeter, volume, and surface area calculations
- Point-in-hull testing
- Edge cases (collinear points, coplanar points, insufficient points)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/convex-hull-algorithms"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: 3D convex hull returns empty or incorrect faces

**Solution**: 
- Ensure at least 4 non-coplanar points for 3D hull
- Check that points are not all on the same plane
- The gift wrapping algorithm may produce duplicate faces with different orientations

**Issue**: Incorrect area/perimeter/volume

**Solution**: 
- Ensure hull points are in correct order (counter-clockwise for 2D)
- For 3D, ensure faces have consistent orientation
- Check for numerical precision issues with very small or large coordinates

### Error Messages

- **"Points list cannot be empty"**: Provide at least one point.
- **"Unknown algorithm"**: Use "graham" or "andrews" for 2D algorithms.
- **"Each point must have 2 coordinates"**: 2D points require (x, y) format.
- **"Each point must have 3 coordinates"**: 3D points require (x, y, z) format.

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

### Graham Scan Algorithm

1. **Find bottom-left point**: Point with minimum y (and minimum x if tie)
2. **Sort by polar angle**: Sort all other points by angle from bottom-left point
3. **Build hull**: Use stack to build convex hull, removing points that create clockwise turns

**Time Complexity**: O(n log n) for sorting + O(n) for building hull = O(n log n)

### Andrew's Monotone Chain Algorithm

1. **Sort points**: Sort by x-coordinate (and y-coordinate if tie)
2. **Build lower hull**: Process points in sorted order, maintaining lower convex chain
3. **Build upper hull**: Process points in reverse order, maintaining upper convex chain
4. **Combine**: Merge lower and upper hulls

**Time Complexity**: O(n log n) for sorting + O(n) for building hull = O(n log n)

**Advantages**: 
- More numerically stable than Graham scan
- Simpler to implement
- Handles collinear points better

### Gift Wrapping Algorithm (3D)

1. **Find initial face**: Find a face on the convex hull
2. **Wrap around edges**: For each edge with only one face, find the next point to form a new face
3. **Continue**: Repeat until all edges have two faces

**Time Complexity**: O(n × f) where n is number of points, f is number of faces (typically O(n²) in worst case)

**Note**: The 3D algorithm is a simplified implementation. For production use with large point sets, consider more advanced algorithms like QuickHull or incremental algorithms.

### Time Complexity

- **Graham scan (2D)**: O(n log n)
- **Andrew's monotone chain (2D)**: O(n log n)
- **Gift wrapping (3D)**: O(n × f) where f is number of faces
- **Area/Perimeter (2D)**: O(n) where n is number of hull points
- **Volume/Surface area (3D)**: O(f) where f is number of faces

### Space Complexity

- **2D algorithms**: O(n) for storing points and hull
- **3D algorithm**: O(n + f) for storing points and faces

## Mathematical Background

### Convex Hull Definition

The convex hull of a set of points is the smallest convex set containing all the points. In 2D, this is a convex polygon. In 3D, this is a convex polyhedron.

### Cross Product

The cross product is used to determine orientation:
- **2D**: Cross product of vectors OA and OB determines if point B is to the left, right, or collinear with vector OA
- **3D**: Cross product gives normal vector to plane defined by three points

### Shoelace Formula

Area of polygon with vertices (x₁, y₁), ..., (xₙ, yₙ):
```
Area = ½ |Σ(xᵢyᵢ₊₁ - xᵢ₊₁yᵢ)|
```

### Volume of Polyhedron

Volume can be computed using divergence theorem or by summing signed volumes of tetrahedra formed with an origin point.

## Applications

- **Computer Graphics**: Rendering, collision detection
- **Pattern Recognition**: Shape analysis, object detection
- **Geographic Information Systems**: Territory boundaries, service areas
- **Optimization**: Facility location, resource allocation
- **Robotics**: Path planning, obstacle avoidance

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
