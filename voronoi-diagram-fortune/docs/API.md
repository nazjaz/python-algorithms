# Voronoi Diagram API Documentation

## Classes

### VoronoiDiagram

Main class for Voronoi diagram construction.

#### Type Aliases

- `Point`: `Tuple[float, float]` - 2D point (x, y)
- `Edge`: `Tuple[Point, Point]` - Edge between two points

#### Methods

##### `__init__(self, sites: List[Point]) -> None`

Initialize Voronoi diagram with sites.

**Parameters**:
- `sites` (List[Point]): List of site points.

**Example**:
```python
vd = VoronoiDiagram([(0, 0), (1, 1), (2, 0)])
```

---

##### `construct(self) -> List[Edge]`

Construct Voronoi diagram.

This is a wrapper that calls the simplified construction method.

**Returns**:
- `List[Edge]`: List of edges in the Voronoi diagram.

**Example**:
```python
vd = VoronoiDiagram([(0, 0), (1, 1), (2, 0)])
edges = vd.construct()
```

---

##### `construct_simple(self) -> List[Edge]`

Construct Voronoi diagram using simplified method.

For each pair of sites, compute perpendicular bisector.
For each triple of sites, compute circumcenter (Voronoi vertex).
Connect vertices to form edges.

**Returns**:
- `List[Edge]`: List of edges in the Voronoi diagram.

**Example**:
```python
vd = VoronoiDiagram([(0, 0), (1, 1), (2, 0)])
edges = vd.construct_simple()
```

---

##### `get_voronoi_cells(self) -> Dict[Point, List[Point]]`

Get Voronoi cells for each site.

**Returns**:
- `Dict[Point, List[Point]]`: Dictionary mapping sites to their Voronoi cell vertices.

**Example**:
```python
vd = VoronoiDiagram([(0, 0), (1, 1), (2, 0)])
vd.construct()
cells = vd.get_voronoi_cells()
```

---

##### `get_cell_for_point(self, point: Point) -> Optional[Point]`

Get the Voronoi cell (site) that contains a given point.

**Parameters**:
- `point` (Point): Point to find cell for.

**Returns**:
- `Optional[Point]`: Site point of the containing cell, or None if not found.

**Example**:
```python
vd = VoronoiDiagram([(0, 0), (1, 1), (2, 0)])
cell_site = vd.get_cell_for_point((0.5, 0.5))
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_distance_squared(self, p1: Point, p2: Point) -> float`

Compute squared distance between two points.

##### `_distance(self, p1: Point, p2: Point) -> float`

Compute Euclidean distance between two points.

##### `_circumcenter(self, p1: Point, p2: Point, p3: Point) -> Optional[Point]`

Compute circumcenter of three points.

##### `_perpendicular_bisector(self, p1: Point, p2: Point) -> Tuple[float, float, float]`

Compute perpendicular bisector line (ax + by + c = 0).

##### `_line_intersection(self, line1: Tuple[float, float, float], line2: Tuple[float, float, float]) -> Optional[Point]`

Find intersection of two lines.

---

## Usage Examples

### Basic Construction

```python
from src.main import VoronoiDiagram

sites = [(0, 0), (1, 1), (2, 0)]
vd = VoronoiDiagram(sites)
edges = vd.construct()
print(f"Vertices: {vd.vertices}")
print(f"Edges: {edges}")
```

### Get Voronoi Cells

```python
vd = VoronoiDiagram([(0, 0), (1, 1), (2, 0)])
vd.construct()
cells = vd.get_voronoi_cells()
for site, vertices in cells.items():
    print(f"Site {site}: {vertices}")
```

### Find Cell for Point

```python
vd = VoronoiDiagram([(0, 0), (2, 0), (1, 2)])
cell_site = vd.get_cell_for_point((1, 1))
print(f"Point is in cell of site: {cell_site}")
```

---

## Performance Characteristics

- **Time Complexity**: O(n³) for finding vertices, O(v²) for edges where n is number of sites, v is number of vertices
- **Space Complexity**: O(n + v) where v is number of vertices
- **Note**: This is a simplified implementation. Full Fortune's algorithm is O(n log n)

---

## Notes

- This is a simplified implementation based on Fortune's algorithm concepts
- For production use, consider using scipy.spatial.Voronoi
- The algorithm finds vertices as circumcenters of site triples
- Edges connect vertices that share two common sites
- Unbounded edges (extending to infinity) are not handled in this simplified version
