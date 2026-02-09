# Line Sweep Algorithm API Documentation

## Classes

### LineSweep

Main class for line sweep geometric algorithms.

#### Type Aliases

- `Point`: `Tuple[float, float]` - 2D point (x, y)
- `Segment`: `Tuple[Point, Point]` - Line segment
- `Rectangle`: `Tuple[Point, Point]` - Rectangle (bottom-left, top-right)

#### Methods

##### `__init__(self) -> None`

Initialize line sweep calculator.

**Returns**: None

**Example**:
```python
ls = LineSweep()
```

---

##### `segments_intersect(self, seg1: Segment, seg2: Segment) -> Optional[Point]`

Check if two line segments intersect and return intersection point.

**Parameters**:
- `seg1` (Segment): First line segment ((x1, y1), (x2, y2)).
- `seg2` (Segment): Second line segment ((x3, y3), (x4, y4)).

**Returns**:
- `Optional[Point]`: Intersection point if segments intersect, None otherwise.

**Example**:
```python
ls = LineSweep()
seg1 = ((0, 0), (2, 2))
seg2 = ((1, 1), (3, 0))
intersection = ls.segments_intersect(seg1, seg2)
# Returns: (1.0, 1.0)
```

---

##### `find_segment_intersections(self, segments: List[Segment]) -> List[Tuple[Segment, Segment, Point]]`

Find all intersections between line segments using line sweep.

**Parameters**:
- `segments` (List[Segment]): List of line segments.

**Returns**:
- `List[Tuple[Segment, Segment, Point]]`: List of tuples (seg1, seg2, intersection_point).

**Example**:
```python
ls = LineSweep()
segments = [
    ((0, 0), (2, 2)),
    ((1, 1), (3, 0)),
]
intersections = ls.find_segment_intersections(segments)
```

---

##### `rectangles_intersect(self, rect1: Rectangle, rect2: Rectangle) -> bool`

Check if two rectangles intersect.

**Parameters**:
- `rect1` (Rectangle): First rectangle ((x1, y1), (x2, y2)) where (x1,y1) is bottom-left and (x2,y2) is top-right.
- `rect2` (Rectangle): Second rectangle.

**Returns**:
- `bool`: True if rectangles intersect, False otherwise.

**Example**:
```python
ls = LineSweep()
rect1 = ((0, 0), (2, 2))
rect2 = ((1, 1), (3, 3))
intersects = ls.rectangles_intersect(rect1, rect2)
# Returns: True
```

---

##### `find_rectangle_intersections(self, rectangles: List[Rectangle]) -> List[Tuple[Rectangle, Rectangle]]`

Find all intersecting rectangles using line sweep.

**Parameters**:
- `rectangles` (List[Rectangle]): List of rectangles.

**Returns**:
- `List[Tuple[Rectangle, Rectangle]]`: List of tuples of intersecting rectangles.

**Example**:
```python
ls = LineSweep()
rectangles = [
    ((0, 0), (2, 2)),
    ((1, 1), (3, 3)),
]
intersections = ls.find_rectangle_intersections(rectangles)
```

---

##### `closest_pair_naive(self, points: List[Point]) -> Tuple[Point, Point, float]`

Find closest pair of points using naive O(n²) algorithm.

**Parameters**:
- `points` (List[Point]): List of points.

**Returns**:
- `Tuple[Point, Point, float]`: Tuple (point1, point2, distance).

**Raises**:
- `ValueError`: If points list has less than 2 points.

**Example**:
```python
ls = LineSweep()
points = [(0, 0), (1, 1), (2, 2)]
p1, p2, dist = ls.closest_pair_naive(points)
```

---

##### `closest_pair_sweep(self, points: List[Point]) -> Tuple[Point, Point, float]`

Find closest pair of points using line sweep algorithm.

**Parameters**:
- `points` (List[Point]): List of points.

**Returns**:
- `Tuple[Point, Point, float]`: Tuple (point1, point2, distance).

**Raises**:
- `ValueError`: If points list has less than 2 points.

**Example**:
```python
ls = LineSweep()
points = [(0, 0), (1, 1), (2, 2)]
p1, p2, dist = ls.closest_pair_sweep(points)
```

---

##### `closest_pair_divide_conquer(self, points: List[Point]) -> Tuple[Point, Point, float]`

Find closest pair using divide and conquer algorithm.

**Parameters**:
- `points` (List[Point]): List of points.

**Returns**:
- `Tuple[Point, Point, float]`: Tuple (point1, point2, distance).

**Raises**:
- `ValueError`: If points list has less than 2 points.

**Example**:
```python
ls = LineSweep()
points = [(0, 0), (1, 1), (2, 2)]
p1, p2, dist = ls.closest_pair_divide_conquer(points)
```

---

##### `find_all_closest_pairs(self, points: List[Point]) -> List[Tuple[Point, Point, float]]`

Find all pairs of points with minimum distance.

**Parameters**:
- `points` (List[Point]): List of points.

**Returns**:
- `List[Tuple[Point, Point, float]]`: List of tuples (point1, point2, distance) for all closest pairs.

**Example**:
```python
ls = LineSweep()
points = [(0, 0), (1, 1), (2, 2)]
pairs = ls.find_all_closest_pairs(points)
```

---

## Internal Methods

The following methods are used internally and are not part of the public API, but are documented for completeness:

##### `_cross_product(self, o: Point, a: Point, b: Point) -> float`

Compute 2D cross product (OA × OB).

##### `_orientation(self, p: Point, q: Point, r: Point) -> int`

Find orientation of ordered triplet (p, q, r).

##### `_on_segment(self, p: Point, q: Point, r: Point) -> bool`

Check if point r lies on segment pq.

##### `_distance_squared(self, p1: Point, p2: Point) -> float`

Compute squared Euclidean distance between two points.

##### `_distance(self, p1: Point, p2: Point) -> float`

Compute Euclidean distance between two points.

---

## Usage Examples

### Segment Intersections

```python
from src.main import LineSweep

ls = LineSweep()
segments = [
    ((0, 0), (2, 2)),
    ((1, 1), (3, 0)),
]
intersections = ls.find_segment_intersections(segments)
for seg1, seg2, point in intersections:
    print(f"{seg1} ∩ {seg2} = {point}")
```

### Rectangle Intersections

```python
ls = LineSweep()
rectangles = [
    ((0, 0), (2, 2)),
    ((1, 1), (3, 3)),
]
intersections = ls.find_rectangle_intersections(rectangles)
for rect1, rect2 in intersections:
    print(f"{rect1} ∩ {rect2}")
```

### Closest Pair

```python
ls = LineSweep()
points = [(0, 0), (1, 1), (2, 2), (3, 3)]

# Using line sweep
p1, p2, dist = ls.closest_pair_sweep(points)
print(f"Closest pair: {p1}, {p2}, distance: {dist}")

# Using divide and conquer
p1, p2, dist = ls.closest_pair_divide_conquer(points)
print(f"Closest pair: {p1}, {p2}, distance: {dist}")
```

### All Closest Pairs

```python
ls = LineSweep()
points = [(0, 0), (1, 1), (2, 2)]
pairs = ls.find_all_closest_pairs(points)
for p1, p2, dist in pairs:
    print(f"{p1} - {p2}: {dist}")
```

---

## Performance Characteristics

- **Segment intersection**: O(n log n + k) time where n is number of segments, k is number of intersections
- **Rectangle intersection**: O(n log n + k) time where n is number of rectangles, k is number of intersections
- **Closest pair (naive)**: O(n²) time
- **Closest pair (sweep)**: O(n log n) time
- **Closest pair (divide)**: O(n log² n) time
- **Space complexity**: O(n) for all algorithms

---

## Notes

- All algorithms use floating-point arithmetic with tolerance checks
- Segment intersection handles collinear and overlapping cases
- Rectangle intersection uses axis-aligned rectangles
- Closest pair algorithms may return different point pairs but same distance
- All algorithms are deterministic and stable
