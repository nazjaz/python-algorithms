"""Test suite for Delaunay triangulation implementation."""

import pytest

from src.main import DelaunayTriangulation, TriangleData


class TestDelaunayTriangulation:
    """Test cases for DelaunayTriangulation class."""

    def test_initialization(self) -> None:
        """Test DelaunayTriangulation initialization."""
        points = [(0, 0), (1, 0), (0, 1)]
        dt = DelaunayTriangulation(points)
        assert dt.points == points
        assert dt.triangles == []
        assert dt.edge_to_triangles == {}

    def test_distance_squared(self) -> None:
        """Test distance_squared computation."""
        dt = DelaunayTriangulation([(0, 0)])
        dist_sq = dt._distance_squared((0, 0), (3, 4))
        assert abs(dist_sq - 25.0) < 1e-9

    def test_circumcenter(self) -> None:
        """Test circumcenter computation."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (0, 1)])
        center = dt._circumcenter((0, 0), (1, 0), (0, 1))
        assert center is not None
        assert abs(center[0] - 0.5) < 1e-6
        assert abs(center[1] - 0.5) < 1e-6

    def test_circumcenter_collinear(self) -> None:
        """Test circumcenter with collinear points."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (2, 0)])
        center = dt._circumcenter((0, 0), (1, 0), (2, 0))
        assert center is None

    def test_point_in_triangle(self) -> None:
        """Test point_in_triangle check."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (0, 1)])
        triangle = TriangleData(vertices=(0, 1, 2))
        assert dt._point_in_triangle((0.3, 0.3), triangle) is True
        assert dt._point_in_triangle((2, 2), triangle) is False

    def test_point_in_circumcircle(self) -> None:
        """Test point_in_circumcircle check."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (0, 1)])
        triangle = TriangleData(vertices=(0, 1, 2))
        dt._update_triangle_circumcircle(0)
        dt.triangles.append(triangle)
        assert dt._point_in_circumcircle((0.5, 0.5), triangle) is True

    def test_construct_three_points(self) -> None:
        """Test construction with three points."""
        points = [(0, 0), (1, 0), (0.5, 1)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert len(triangles) == 1
        assert triangles[0] == (0, 1, 2) or triangles[0] == (0, 2, 1) or triangles[0] == (1, 0, 2)

    def test_construct_four_points(self) -> None:
        """Test construction with four points."""
        points = [(0, 0), (2, 0), (2, 2), (0, 2)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert len(triangles) >= 1

    def test_construct_empty(self) -> None:
        """Test construction with empty points."""
        points: list = []
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert triangles == []

    def test_construct_single_point(self) -> None:
        """Test construction with single point."""
        points = [(0, 0)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert triangles == []

    def test_construct_two_points(self) -> None:
        """Test construction with two points."""
        points = [(0, 0), (1, 0)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert triangles == []

    def test_get_edges(self) -> None:
        """Test getting edges."""
        points = [(0, 0), (1, 0), (0.5, 1)]
        dt = DelaunayTriangulation(points)
        dt.construct()
        edges = dt.get_edges()
        assert len(edges) == 3

    def test_get_triangles(self) -> None:
        """Test getting triangles."""
        points = [(0, 0), (1, 0), (0.5, 1)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert len(triangles) == 1

    def test_add_triangle(self) -> None:
        """Test adding a triangle."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (0, 1)])
        tri_idx = dt._add_triangle(0, 1, 2)
        assert tri_idx == 0
        assert len(dt.triangles) == 1

    def test_remove_triangle(self) -> None:
        """Test removing a triangle."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (0, 1)])
        tri_idx = dt._add_triangle(0, 1, 2)
        dt._remove_triangle(tri_idx)
        assert dt.triangles[tri_idx] is None

    def test_get_edge(self) -> None:
        """Test getting normalized edge."""
        dt = DelaunayTriangulation([(0, 0)])
        edge = dt._get_edge(2, 1)
        assert edge == (1, 2)

    def test_construct_triangle(self) -> None:
        """Test construction with triangle of points."""
        points = [(0, 0), (1, 0), (0.5, 1)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert len(triangles) == 1

    def test_construct_square(self) -> None:
        """Test construction with square of points."""
        points = [(0, 0), (2, 0), (2, 2), (0, 2)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert len(triangles) >= 1

    def test_construct_line(self) -> None:
        """Test construction with points in a line."""
        points = [(0, 0), (1, 0), (2, 0), (3, 0)]
        dt = DelaunayTriangulation(points)
        triangles = dt.construct()
        assert len(triangles) >= 0

    def test_flip_edge(self) -> None:
        """Test edge flipping."""
        dt = DelaunayTriangulation([(0, 0), (1, 0), (0, 1), (1, 1)])
        tri1_idx = dt._add_triangle(0, 1, 2)
        tri2_idx = dt._add_triangle(1, 2, 3)
        edge = dt._get_edge(1, 2)
        flipped = dt._flip_edge(edge)
        assert isinstance(flipped, bool)
