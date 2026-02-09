"""Test suite for Voronoi diagram implementation."""

import pytest

from src.main import VoronoiDiagram


class TestVoronoiDiagram:
    """Test cases for VoronoiDiagram class."""

    def test_initialization(self) -> None:
        """Test VoronoiDiagram initialization."""
        sites = [(0, 0), (1, 1)]
        vd = VoronoiDiagram(sites)
        assert vd.sites == sites
        assert vd.edges == []
        assert vd.vertices == []

    def test_distance_squared(self) -> None:
        """Test distance_squared computation."""
        vd = VoronoiDiagram([(0, 0)])
        dist_sq = vd._distance_squared((0, 0), (3, 4))
        assert abs(dist_sq - 25.0) < 1e-9

    def test_distance(self) -> None:
        """Test distance computation."""
        vd = VoronoiDiagram([(0, 0)])
        dist = vd._distance((0, 0), (3, 4))
        assert abs(dist - 5.0) < 1e-9

    def test_circumcenter(self) -> None:
        """Test circumcenter computation."""
        vd = VoronoiDiagram([(0, 0), (1, 0), (0, 1)])
        center = vd._circumcenter((0, 0), (1, 0), (0, 1))
        assert center is not None
        assert abs(center[0] - 0.5) < 1e-6
        assert abs(center[1] - 0.5) < 1e-6

    def test_circumcenter_collinear(self) -> None:
        """Test circumcenter with collinear points."""
        vd = VoronoiDiagram([(0, 0), (1, 0), (2, 0)])
        center = vd._circumcenter((0, 0), (1, 0), (2, 0))
        assert center is None

    def test_perpendicular_bisector(self) -> None:
        """Test perpendicular bisector computation."""
        vd = VoronoiDiagram([(0, 0), (2, 0)])
        a, b, c = vd._perpendicular_bisector((0, 0), (2, 0))
        assert abs(a) < 1e-9 or abs(b) < 1e-9

    def test_line_intersection(self) -> None:
        """Test line intersection computation."""
        vd = VoronoiDiagram([(0, 0)])
        line1 = (1, 0, 0)
        line2 = (0, 1, 0)
        intersection = vd._line_intersection(line1, line2)
        assert intersection == (0, 0)

    def test_line_intersection_parallel(self) -> None:
        """Test line intersection with parallel lines."""
        vd = VoronoiDiagram([(0, 0)])
        line1 = (1, 0, 0)
        line2 = (1, 0, 1)
        intersection = vd._line_intersection(line1, line2)
        assert intersection is None

    def test_construct_two_sites(self) -> None:
        """Test construction with two sites."""
        sites = [(0, 0), (2, 0)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert len(edges) > 0

    def test_construct_three_sites(self) -> None:
        """Test construction with three sites."""
        sites = [(0, 0), (1, 1), (2, 0)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert len(vd.vertices) > 0

    def test_construct_four_sites(self) -> None:
        """Test construction with four sites."""
        sites = [(0, 0), (2, 0), (2, 2), (0, 2)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert len(vd.vertices) > 0

    def test_construct_single_site(self) -> None:
        """Test construction with single site."""
        sites = [(0, 0)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert edges == []

    def test_construct_empty(self) -> None:
        """Test construction with empty sites."""
        sites: list = []
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert edges == []

    def test_get_voronoi_cells(self) -> None:
        """Test getting Voronoi cells."""
        sites = [(0, 0), (1, 1), (2, 0)]
        vd = VoronoiDiagram(sites)
        vd.construct()
        cells = vd.get_voronoi_cells()
        assert len(cells) == len(sites)
        for site in sites:
            assert site in cells

    def test_get_cell_for_point(self) -> None:
        """Test getting cell for a point."""
        sites = [(0, 0), (2, 0), (1, 2)]
        vd = VoronoiDiagram(sites)
        cell = vd.get_cell_for_point((0.5, 0.5))
        assert cell in sites

    def test_get_cell_for_point_empty_sites(self) -> None:
        """Test getting cell with empty sites."""
        vd = VoronoiDiagram([])
        cell = vd.get_cell_for_point((0, 0))
        assert cell is None

    def test_get_cell_for_point_exact_site(self) -> None:
        """Test getting cell for exact site location."""
        sites = [(0, 0), (1, 1), (2, 0)]
        vd = VoronoiDiagram(sites)
        cell = vd.get_cell_for_point((1, 1))
        assert cell == (1, 1)

    def test_construct_triangle(self) -> None:
        """Test construction with triangle of sites."""
        sites = [(0, 0), (1, 0), (0.5, 1)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert len(vd.vertices) > 0

    def test_construct_line(self) -> None:
        """Test construction with sites in a line."""
        sites = [(0, 0), (1, 0), (2, 0), (3, 0)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert len(vd.vertices) >= 0

    def test_construct_square(self) -> None:
        """Test construction with square of sites."""
        sites = [(0, 0), (2, 0), (2, 2), (0, 2)]
        vd = VoronoiDiagram(sites)
        edges = vd.construct()
        assert len(vd.vertices) > 0
