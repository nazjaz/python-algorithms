# Line Sweep Algorithm for Geometric Problems

A Python implementation of line sweep algorithms for solving geometric intersection problems and finding closest pairs of points.

## Project Title and Description

This project implements line sweep algorithms for efficiently solving geometric problems including:
- Line segment intersection detection
- Rectangle intersection detection
- Closest pair of points finding (multiple algorithms)

The line sweep algorithm is a powerful technique in computational geometry that processes geometric objects by sweeping a line across the plane, maintaining an active set of objects and processing events as they occur.

**Target Audience**: Developers working with computational geometry, computer graphics, competitive programming, and anyone needing efficient geometric algorithms.

## Features

- Line segment intersection detection using line sweep
- Rectangle intersection detection using line sweep
- Closest pair finding with multiple algorithms:
  - Naive O(n²) algorithm
  - Line sweep O(n log n) algorithm
  - Divide and conquer O(n log² n) algorithm
- Event-based processing for efficient sweep
- Support for collinear and overlapping segments
- Find all closest pairs functionality
- Command-line interface for interactive use
- Comprehensive test suite

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

No external dependencies are required. The implementation uses only Python standard library.

## Installation

### Step 1: Clone or Navigate to Project Directory

```bash
cd /Users/nasihjaseem/projects/github/python-algorithms/line-sweep-geometric
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

#### Find Line Segment Intersections

```bash
python src/main.py --segments "0,0,2,2;1,1,3,0"
```

Output:
```
Input segments: [((0.0, 0.0), (2.0, 2.0)), ((1.0, 1.0), (3.0, 0.0))]
Number of intersections: 1
  ((1.0, 1.0), (3.0, 0.0)) ∩ ((0.0, 0.0), (2.0, 2.0)) = (1.0, 1.0)
```

#### Find Rectangle Intersections

```bash
python src/main.py --rectangles "0,0,2,2;1,1,3,3"
```

Output:
```
Input rectangles: [((0.0, 0.0), (2.0, 2.0)), ((1.0, 1.0), (3.0, 3.0))]
Number of intersections: 1
  ((0.0, 0.0), (2.0, 2.0)) ∩ ((1.0, 1.0), (3.0, 3.0))
```

#### Find Closest Pair of Points

```bash
python src/main.py --points "0,0;1,1;2,2;3,3" --closest-pair sweep
```

Output:
```
Input points: [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0), (3.0, 3.0)]
Closest pair (sweep):
  Point 1: (1.0, 1.0)
  Point 2: (0.0, 0.0)
  Distance: 1.4142
```

#### Find All Closest Pairs

```bash
python src/main.py --points "0,0;1,1;2,2;3,3" --all-closest
```

#### Use Different Closest Pair Algorithms

```bash
# Naive algorithm
python src/main.py --points "0,0;1,1;2,2" --closest-pair naive

# Line sweep algorithm
python src/main.py --points "0,0;1,1;2,2" --closest-pair sweep

# Divide and conquer algorithm
python src/main.py --points "0,0;1,1;2,2" --closest-pair divide
```

### Programmatic Usage

```python
from src.main import LineSweep

# Create LineSweep instance
ls = LineSweep()

# Line segment intersections
segments = [
    ((0, 0), (2, 2)),
    ((1, 1), (3, 0)),
]
intersections = ls.find_segment_intersections(segments)
for seg1, seg2, point in intersections:
    print(f"{seg1} ∩ {seg2} = {point}")

# Rectangle intersections
rectangles = [
    ((0, 0), (2, 2)),
    ((1, 1), (3, 3)),
]
intersections = ls.find_rectangle_intersections(rectangles)
for rect1, rect2 in intersections:
    print(f"{rect1} ∩ {rect2}")

# Closest pair
points = [(0, 0), (1, 1), (2, 2), (3, 3)]
p1, p2, dist = ls.closest_pair_sweep(points)
print(f"Closest pair: {p1}, {p2}, distance: {dist}")

# All closest pairs
pairs = ls.find_all_closest_pairs(points)
for p1, p2, dist in pairs:
    print(f"{p1} - {p2}: {dist}")
```

### Common Use Cases

1. **Find segment intersections**
   ```bash
   python src/main.py --segments "0,0,2,2;1,1,3,0"
   ```

2. **Find rectangle intersections**
   ```bash
   python src/main.py --rectangles "0,0,2,2;1,1,3,3"
   ```

3. **Find closest pair**
   ```bash
   python src/main.py --points "0,0;1,1;2,2;3,3" --closest-pair sweep
   ```

## Project Structure

```
line-sweep-geometric/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
├── src/
│   └── main.py              # Main line sweep implementation and CLI
├── tests/
│   └── test_main.py         # Comprehensive test suite
├── docs/
│   └── API.md               # API documentation
└── logs/
    └── .gitkeep             # Placeholder for log directory
```

### File Descriptions

- **src/main.py**: Contains the `LineSweep` class with all core functionality for geometric intersections and closest pair finding.
- **tests/test_main.py**: Comprehensive test suite covering all functionality including edge cases and various geometric configurations.
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
pytest tests/test_main.py::TestLineSweep::test_segments_intersect_intersecting
```

### Test Coverage

The test suite aims for comprehensive coverage including:
- Line segment intersection detection
- Rectangle intersection detection
- All closest pair algorithms
- Edge cases (collinear points, parallel segments, etc.)
- Error handling

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Ensure you're running commands from the project root directory, or add the project root to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/line-sweep-geometric"
```

**Issue**: Tests fail with import errors

**Solution**: Make sure you've installed pytest:
```bash
pip install pytest pytest-cov
```

**Issue**: Incorrect intersection results

**Solution**: 
- Check that segment/rectangle coordinates are correct
- Ensure segments are specified as ((x1, y1), (x2, y2))
- For rectangles, use (bottom-left, top-right) format

**Issue**: Closest pair returns unexpected results

**Solution**: 
- Verify point coordinates are correct
- Check for duplicate points (may affect results)
- Try different algorithms (naive, sweep, divide) to compare

### Error Messages

- **"Need at least 2 points"**: Closest pair algorithms require at least 2 points.
- **"Each segment must have 4 coordinates"**: Segments must be specified as x1,y1,x2,y2.
- **"Each rectangle must have 4 coordinates"**: Rectangles must be specified as x1,y1,x2,y2.

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

### Line Sweep Algorithm

The line sweep algorithm processes geometric objects by:
1. **Creating events**: Generate events for start/end points of objects
2. **Sorting events**: Sort events by x-coordinate (and type)
3. **Sweeping**: Process events in order, maintaining active set
4. **Processing**: Check intersections/relationships in active set

### Segment Intersection

For line segments:
- Events: Start and end points of segments
- Active set: Segments currently intersected by sweep line
- Check: When adding segment, check against all active segments

**Time Complexity**: O(n log n + k) where n is number of segments, k is number of intersections

### Rectangle Intersection

For rectangles:
- Events: Left and right edges of rectangles
- Active set: Rectangles currently intersected by sweep line
- Check: When adding rectangle, check against all active rectangles

**Time Complexity**: O(n log n + k) where n is number of rectangles, k is number of intersections

### Closest Pair Algorithms

1. **Naive**: O(n²) - Check all pairs
2. **Line Sweep**: O(n log n) - Sort by x, maintain active set sorted by y
3. **Divide and Conquer**: O(n log² n) - Divide points, solve recursively, merge

**Line Sweep Approach**:
- Sort points by x-coordinate
- Maintain active set of points within current minimum distance
- For each point, only check points in active set
- Update active set as sweep line moves

### Time Complexity

- **Segment intersection**: O(n log n + k) where k is number of intersections
- **Rectangle intersection**: O(n log n + k) where k is number of intersections
- **Closest pair (naive)**: O(n²)
- **Closest pair (sweep)**: O(n log n)
- **Closest pair (divide)**: O(n log² n)

### Space Complexity

- **Segment intersection**: O(n) for events and active set
- **Rectangle intersection**: O(n) for events and active set
- **Closest pair**: O(n) for storing points and active set

## Mathematical Background

### Orientation Test

Given three points p, q, r:
- Cross product (q-p) × (r-p) determines orientation
- Positive: Counter-clockwise
- Negative: Clockwise
- Zero: Collinear

### Segment Intersection

Two segments intersect if:
1. General case: Orientations of endpoints are different
2. Special case: Endpoints are collinear and on segments

### Closest Pair

The closest pair problem finds the two points with minimum Euclidean distance:
- Brute force: Check all pairs O(n²)
- Optimized: Use geometric properties to reduce comparisons

## Applications

- **Computer Graphics**: Collision detection, rendering
- **Geographic Information Systems**: Overlay analysis, spatial queries
- **Computational Geometry**: Range queries, proximity problems
- **Competitive Programming**: Efficient geometric problem solving
- **Robotics**: Path planning, obstacle avoidance

## License

This project is provided as-is for educational and practical use. Please refer to the LICENSE file in the parent directory for license information.
