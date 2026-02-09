# Delaunay Triangulation API Documentation

## Classes

### DelaunayTriangulation

Main class for Delaunay triangulation computation.

#### Type Aliases

- `Point`: `Tuple[float, float]` - 2D point (x, y)
- `Triangle`: `Tuple[int, int, int]` - Triangle (vertex indices)
- `Edge`: `Tuple[int, int]` - Edge (vertex index pair)

#### Methods

##### `__init__(self, points: List[Point]) -> None`

Initialize Delaunay triangulation with points.

**Parameters**:
- `points` (List[Point]): List of points to triangulate.

**Example**:
```python
dt = DelaunayTriangulation([(0, 0), (1, 0), (0.5, 1)])
```

---

##### `construct(self) -> List[Triangle]`

Construct Delaunay triangulation using incremental insertion.

**Returns**:
- `List[Triangle]`: List of triangles (vertex indices).

**Example**:
```python
dt = DelaunayTriangulation([(0, 0), (1, 0), (0.5, 1)])
triangles = dt.construct()
# Returns: [(0, 1, 2)]
```

---

##### `get_edges(self) -> List[Edge]`

Get all edges in the triangulation.

**Returns**:
- `List[Edge]`: List of edges (vertex index pairs).

**Example**:
```python
dt = DelaunayTriangulation([(0, 0), (1, 0), (0.5, 1)])
dt.construct()
edges = dt.get_edges()
# Returns: [(0, 1), (0, 2), (1, 2)]
```

---

##### `get_triangles(self) -> List[Triangle]`

Get all triangles in the triangulation.

**Returns**:
- `List[Triangle]`: List of triangles (vertex index triples).

**Example**:
```python
dt = DelaunayTriangulation([(0, 0), (1, 0), (0.5, 1)])
triangles = dt.get_triangles()
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_distance_squared(self, p1: Point, p2: Point) -> float`

Compute squared distance between two points.

##### `_circumcenter(self, p1: Point, p2: Point, p3: Point) -> Optional[Point]`

Compute circumcenter of three points.

##### `_point_in_circumcircle(self, point: Point, triangle: TriangleData) -> bool`

Check if point is inside triangle's circumcircle.

##### `_point_in_triangle(self, point: Point, triangle: TriangleData) -> bool`

Check if point is inside triangle using barycentric coordinates.

##### `_find_triangle_containing(self, point: Point) -> Optional[int]`

Find triangle containing a point.

##### `_flip_edge(self, edge: Edge) -> bool`

Flip an edge if it violates Delaunay property.

##### `_legalize_edges(self, point_idx: int, bad_triangles: List[int]) -> None`

Legalize edges after point insertion using edge flipping.

##### `_add_triangle(self, v0: int, v1: int, v2: int) -> int`

Add a triangle to the triangulation.

##### `_remove_triangle(self, tri_idx: int) -> None`

Remove a triangle from the triangulation.

---

## Usage Examples

### Basic Construction

```python
from src.main import DelaunayTriangulation

points = [(0, 0), (1, 0), (0.5, 1)]
dt = DelaunayTriangulation(points)
triangles = dt.construct()
print(f"Triangles: {triangles}")
```

### Get Edges

```python
dt = DelaunayTriangulation([(0, 0), (1, 0), (0.5, 1)])
dt.construct()
edges = dt.get_edges()
print(f"Edges: {edges}")
```

### Multiple Points

```python
points = [(0, 0), (1, 0), (1, 1), (0, 1)]
dt = DelaunayTriangulation(points)
triangles = dt.construct()
print(f"Number of triangles: {len(triangles)}")
```

---

## Performance Characteristics

- **Time Complexity**: O(n²) worst case, O(n log n) expected for random points
- **Space Complexity**: O(n) where n is number of points
- **Edge Flipping**: O(n) per point insertion in practice

---

## Notes

- The algorithm uses incremental insertion with edge flipping
- Empty circle property is maintained throughout
- For production use with large point sets, consider scipy.spatial.Delaunay
- The implementation may need refinement for degenerate cases
