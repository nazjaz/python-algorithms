# Convex Hull API Documentation

## Classes

### ConvexHull

Main class for convex hull computation.

#### Type Aliases

- `Point2D`: `Tuple[float, float]` - 2D point (x, y)
- `Point3D`: `Tuple[float, float, float]` - 3D point (x, y, z)

#### Methods

##### `__init__(self) -> None`

Initialize convex hull calculator.

**Returns**: None

**Example**:
```python
ch = ConvexHull()
```

---

##### `graham_scan_2d(self, points: List[Point2D]) -> List[Point2D]`

Compute 2D convex hull using Graham scan algorithm.

**Parameters**:
- `points` (List[Point2D]): List of 2D points.

**Returns**:
- `List[Point2D]`: List of points forming the convex hull in counter-clockwise order.

**Raises**:
- `ValueError`: If points list is empty or has less than 3 points (returns all points if < 3).

**Example**:
```python
ch = ConvexHull()
points = [(0, 0), (1, 1), (2, 0), (1, 0.5)]
hull = ch.graham_scan_2d(points)
# Returns: [(0, 0), (2, 0), (1, 1)]
```

---

##### `andrews_monotone_chain_2d(self, points: List[Point2D]) -> List[Point2D]`

Compute 2D convex hull using Andrew's monotone chain algorithm.

**Parameters**:
- `points` (List[Point2D]): List of 2D points.

**Returns**:
- `List[Point2D]`: List of points forming the convex hull in counter-clockwise order.

**Raises**:
- `ValueError`: If points list is empty.

**Example**:
```python
ch = ConvexHull()
points = [(0, 0), (1, 1), (2, 0), (1, 0.5)]
hull = ch.andrews_monotone_chain_2d(points)
# Returns: [(0, 0), (2, 0), (1, 1)]
```

---

##### `convex_hull_2d(self, points: List[Point2D], algorithm: str = "graham") -> List[Point2D]`

Compute 2D convex hull using specified algorithm.

**Parameters**:
- `points` (List[Point2D]): List of 2D points.
- `algorithm` (str): Algorithm to use ("graham" or "andrews"). Default: "graham".

**Returns**:
- `List[Point2D]`: List of points forming the convex hull.

**Raises**:
- `ValueError`: If algorithm name is invalid.

**Example**:
```python
ch = ConvexHull()
points = [(0, 0), (1, 1), (2, 0)]
hull = ch.convex_hull_2d(points, algorithm="andrews")
```

---

##### `gift_wrapping_3d(self, points: List[Point3D]) -> List[Tuple[int, int, int]]`

Compute 3D convex hull using gift wrapping algorithm.

**Parameters**:
- `points` (List[Point3D]): List of 3D points.

**Returns**:
- `List[Tuple[int, int, int]]`: List of triangular faces (indices of points forming triangles).

**Raises**:
- `ValueError`: If points list has less than 4 points.

**Example**:
```python
ch = ConvexHull()
points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
faces = ch.gift_wrapping_3d(points)
# Returns: [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
```

---

##### `convex_hull_3d(self, points: List[Point3D]) -> List[Tuple[int, int, int]]`

Compute 3D convex hull using gift wrapping algorithm.

**Parameters**:
- `points` (List[Point3D]): List of 3D points.

**Returns**:
- `List[Tuple[int, int, int]]`: List of triangular faces (indices).

**Example**:
```python
ch = ConvexHull()
points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
faces = ch.convex_hull_3d(points)
```

---

##### `hull_area_2d(self, hull_points: List[Point2D]) -> float`

Compute area of 2D convex hull using shoelace formula.

**Parameters**:
- `hull_points` (List[Point2D]): Points forming the convex hull in order.

**Returns**:
- `float`: Area of the convex hull polygon.

**Example**:
```python
ch = ConvexHull()
hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
area = ch.hull_area_2d(hull)
# Returns: 1.0
```

---

##### `hull_perimeter_2d(self, hull_points: List[Point2D]) -> float`

Compute perimeter of 2D convex hull.

**Parameters**:
- `hull_points` (List[Point2D]): Points forming the convex hull in order.

**Returns**:
- `float`: Perimeter of the convex hull polygon.

**Example**:
```python
ch = ConvexHull()
hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
perimeter = ch.hull_perimeter_2d(hull)
# Returns: 4.0
```

---

##### `hull_volume_3d(self, points: List[Point3D], faces: List[Tuple[int, int, int]]) -> float`

Compute volume of 3D convex hull.

**Parameters**:
- `points` (List[Point3D]): List of 3D points.
- `faces` (List[Tuple[int, int, int]]): List of triangular faces (indices).

**Returns**:
- `float`: Volume of the 3D convex hull.

**Example**:
```python
ch = ConvexHull()
points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
faces = ch.gift_wrapping_3d(points)
volume = ch.hull_volume_3d(points, faces)
# Returns: ~0.1667 (1/6 for unit tetrahedron)
```

---

##### `hull_surface_area_3d(self, points: List[Point3D], faces: List[Tuple[int, int, int]]) -> float`

Compute surface area of 3D convex hull.

**Parameters**:
- `points` (List[Point3D]): List of 3D points.
- `faces` (List[Tuple[int, int, int]]): List of triangular faces (indices).

**Returns**:
- `float`: Surface area of the 3D convex hull.

**Example**:
```python
ch = ConvexHull()
points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
faces = ch.gift_wrapping_3d(points)
surface_area = ch.hull_surface_area_3d(points, faces)
```

---

##### `is_point_inside_2d(self, point: Point2D, hull_points: List[Point2D]) -> bool`

Check if a point is inside 2D convex hull.

**Parameters**:
- `point` (Point2D): Point to check.
- `hull_points` (List[Point2D]): Points forming the convex hull in order.

**Returns**:
- `bool`: True if point is inside or on the hull, False otherwise.

**Example**:
```python
ch = ConvexHull()
hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
is_inside = ch.is_point_inside_2d((0.5, 0.5), hull)
# Returns: True
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_cross_product_2d(self, o: Point2D, a: Point2D, b: Point2D) -> float`

Compute 2D cross product (OA × OB).

##### `_cross_product_3d(self, a: Point3D, b: Point3D, c: Point3D) -> Tuple[float, float, float]`

Compute 3D cross product (AB × AC).

##### `_dot_product_3d(self, a: Point3D, b: Point3D) -> float`

Compute 3D dot product.

##### `_distance_2d(self, a: Point2D, b: Point2D) -> float`

Compute Euclidean distance between two 2D points.

##### `_distance_3d(self, a: Point3D, b: Point3D) -> float`

Compute Euclidean distance between two 3D points.

##### `_find_bottom_left_2d(self, points: List[Point2D]) -> int`

Find bottom-left point (lowest y, then leftmost x).

---

## Usage Examples

### 2D Convex Hull

```python
from src.main import ConvexHull

ch = ConvexHull()
points = [(0, 0), (1, 1), (2, 0), (1, 0.5)]

# Graham scan
hull_graham = ch.graham_scan_2d(points)

# Andrew's monotone chain
hull_andrews = ch.andrews_monotone_chain_2d(points)

# Using wrapper
hull = ch.convex_hull_2d(points, algorithm="graham")
```

### Area and Perimeter

```python
ch = ConvexHull()
hull = [(0, 0), (1, 0), (1, 1), (0, 1)]

area = ch.hull_area_2d(hull)
perimeter = ch.hull_perimeter_2d(hull)
print(f"Area: {area}, Perimeter: {perimeter}")
```

### Point-in-Hull Testing

```python
ch = ConvexHull()
hull = [(0, 0), (1, 0), (1, 1), (0, 1)]

is_inside = ch.is_point_inside_2d((0.5, 0.5), hull)
print(f"Point inside: {is_inside}")
```

### 3D Convex Hull

```python
ch = ConvexHull()
points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]

faces = ch.gift_wrapping_3d(points)
volume = ch.hull_volume_3d(points, faces)
surface_area = ch.hull_surface_area_3d(points, faces)
print(f"Volume: {volume}, Surface area: {surface_area}")
```

---

## Performance Characteristics

- **Graham scan (2D)**: O(n log n) time, O(n) space
- **Andrew's monotone chain (2D)**: O(n log n) time, O(n) space
- **Gift wrapping (3D)**: O(n × f) time where f is number of faces, O(n + f) space
- **Area/Perimeter (2D)**: O(n) time
- **Volume/Surface area (3D)**: O(f) time where f is number of faces

---

## Notes

- Both 2D algorithms produce the same set of hull points (may differ in order)
- Andrew's algorithm is more numerically stable
- 3D gift wrapping may produce duplicate faces with different orientations
- For production use with large 3D point sets, consider more advanced algorithms
- All geometric operations use floating-point arithmetic with tolerance checks
