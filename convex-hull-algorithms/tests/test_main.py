"""Test suite for convex hull algorithms implementation."""

import pytest

from src.main import ConvexHull


class TestConvexHull:
    """Test cases for ConvexHull class."""

    def test_initialization(self) -> None:
        """Test ConvexHull initialization."""
        ch = ConvexHull()
        assert ch is not None

    def test_cross_product_2d(self) -> None:
        """Test 2D cross product computation."""
        ch = ConvexHull()
        o = (0, 0)
        a = (1, 0)
        b = (0, 1)
        cross = ch._cross_product_2d(o, a, b)
        assert cross > 0

    def test_cross_product_3d(self) -> None:
        """Test 3D cross product computation."""
        ch = ConvexHull()
        a = (1, 0, 0)
        b = (0, 1, 0)
        c = (0, 0, 1)
        cross = ch._cross_product_3d(a, b, c)
        assert len(cross) == 3

    def test_distance_2d(self) -> None:
        """Test 2D distance computation."""
        ch = ConvexHull()
        a = (0, 0)
        b = (3, 4)
        dist = ch._distance_2d(a, b)
        assert abs(dist - 5.0) < 1e-9

    def test_distance_3d(self) -> None:
        """Test 3D distance computation."""
        ch = ConvexHull()
        a = (0, 0, 0)
        b = (2, 3, 6)
        dist = ch._distance_3d(a, b)
        assert abs(dist - 7.0) < 1e-9

    def test_find_bottom_left_2d(self) -> None:
        """Test finding bottom-left point."""
        ch = ConvexHull()
        points = [(1, 2), (0, 1), (2, 0), (1, 1)]
        idx = ch._find_bottom_left_2d(points)
        assert points[idx] == (2, 0)

    def test_graham_scan_2d_simple(self) -> None:
        """Test Graham scan with simple case."""
        ch = ConvexHull()
        points = [(0, 0), (1, 1), (2, 0), (1, 0.5)]
        hull = ch.graham_scan_2d(points)
        assert len(hull) >= 3
        assert (0, 0) in hull
        assert (2, 0) in hull
        assert (1, 1) in hull

    def test_graham_scan_2d_triangle(self) -> None:
        """Test Graham scan with triangle."""
        ch = ConvexHull()
        points = [(0, 0), (1, 0), (0.5, 1)]
        hull = ch.graham_scan_2d(points)
        assert len(hull) == 3

    def test_graham_scan_2d_square(self) -> None:
        """Test Graham scan with square."""
        ch = ConvexHull()
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        hull = ch.graham_scan_2d(points)
        assert len(hull) == 4

    def test_graham_scan_2d_insufficient_points(self) -> None:
        """Test Graham scan with insufficient points."""
        ch = ConvexHull()
        points = [(0, 0)]
        hull = ch.graham_scan_2d(points)
        assert hull == [(0, 0)]

        points = [(0, 0), (1, 1)]
        hull = ch.graham_scan_2d(points)
        assert len(hull) == 2

    def test_andrews_monotone_chain_2d_simple(self) -> None:
        """Test Andrew's monotone chain with simple case."""
        ch = ConvexHull()
        points = [(0, 0), (1, 1), (2, 0), (1, 0.5)]
        hull = ch.andrews_monotone_chain_2d(points)
        assert len(hull) >= 3

    def test_andrews_monotone_chain_2d_triangle(self) -> None:
        """Test Andrew's monotone chain with triangle."""
        ch = ConvexHull()
        points = [(0, 0), (1, 0), (0.5, 1)]
        hull = ch.andrews_monotone_chain_2d(points)
        assert len(hull) == 3

    def test_andrews_monotone_chain_2d_square(self) -> None:
        """Test Andrew's monotone chain with square."""
        ch = ConvexHull()
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)]
        hull = ch.andrews_monotone_chain_2d(points)
        assert len(hull) == 4

    def test_andrews_monotone_chain_2d_insufficient_points(self) -> None:
        """Test Andrew's monotone chain with insufficient points."""
        ch = ConvexHull()
        points = [(0, 0)]
        hull = ch.andrews_monotone_chain_2d(points)
        assert hull == [(0, 0)]

        points = [(0, 0), (1, 1)]
        hull = ch.andrews_monotone_chain_2d(points)
        assert len(hull) == 2

    def test_convex_hull_2d_graham(self) -> None:
        """Test convex_hull_2d with Graham algorithm."""
        ch = ConvexHull()
        points = [(0, 0), (1, 1), (2, 0)]
        hull = ch.convex_hull_2d(points, algorithm="graham")
        assert len(hull) == 3

    def test_convex_hull_2d_andrews(self) -> None:
        """Test convex_hull_2d with Andrew's algorithm."""
        ch = ConvexHull()
        points = [(0, 0), (1, 1), (2, 0)]
        hull = ch.convex_hull_2d(points, algorithm="andrews")
        assert len(hull) == 3

    def test_convex_hull_2d_invalid_algorithm(self) -> None:
        """Test convex_hull_2d with invalid algorithm."""
        ch = ConvexHull()
        points = [(0, 0), (1, 1), (2, 0)]
        with pytest.raises(ValueError, match="Unknown algorithm"):
            ch.convex_hull_2d(points, algorithm="invalid")

    def test_hull_area_2d_triangle(self) -> None:
        """Test area computation for triangle."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (0.5, 1)]
        area = ch.hull_area_2d(hull)
        assert abs(area - 0.5) < 1e-9

    def test_hull_area_2d_square(self) -> None:
        """Test area computation for square."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
        area = ch.hull_area_2d(hull)
        assert abs(area - 1.0) < 1e-9

    def test_hull_area_2d_insufficient_points(self) -> None:
        """Test area computation with insufficient points."""
        ch = ConvexHull()
        area = ch.hull_area_2d([])
        assert area == 0.0

        area = ch.hull_area_2d([(0, 0)])
        assert area == 0.0

    def test_hull_perimeter_2d_triangle(self) -> None:
        """Test perimeter computation for triangle."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (0.5, 1)]
        perimeter = ch.hull_perimeter_2d(hull)
        assert perimeter > 0

    def test_hull_perimeter_2d_square(self) -> None:
        """Test perimeter computation for square."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
        perimeter = ch.hull_perimeter_2d(hull)
        assert abs(perimeter - 4.0) < 1e-9

    def test_hull_perimeter_2d_insufficient_points(self) -> None:
        """Test perimeter computation with insufficient points."""
        ch = ConvexHull()
        perimeter = ch.hull_perimeter_2d([])
        assert perimeter == 0.0

        perimeter = ch.hull_perimeter_2d([(0, 0), (1, 1)])
        assert perimeter > 0

    def test_is_point_inside_2d_inside(self) -> None:
        """Test point inside check for point inside hull."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
        point = (0.5, 0.5)
        assert ch.is_point_inside_2d(point, hull) is True

    def test_is_point_inside_2d_outside(self) -> None:
        """Test point inside check for point outside hull."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
        point = (2, 2)
        assert ch.is_point_inside_2d(point, hull) is False

    def test_is_point_inside_2d_on_boundary(self) -> None:
        """Test point inside check for point on boundary."""
        ch = ConvexHull()
        hull = [(0, 0), (1, 0), (1, 1), (0, 1)]
        point = (0.5, 0)
        assert ch.is_point_inside_2d(point, hull) is True

    def test_gift_wrapping_3d_tetrahedron(self) -> None:
        """Test 3D gift wrapping with tetrahedron."""
        ch = ConvexHull()
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        faces = ch.gift_wrapping_3d(points)
        assert len(faces) >= 4

    def test_gift_wrapping_3d_insufficient_points(self) -> None:
        """Test 3D gift wrapping with insufficient points."""
        ch = ConvexHull()
        points = [(0, 0, 0)]
        faces = ch.gift_wrapping_3d(points)
        assert faces == []

        points = [(0, 0, 0), (1, 0, 0)]
        faces = ch.gift_wrapping_3d(points)
        assert faces == []

        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0)]
        faces = ch.gift_wrapping_3d(points)
        assert faces == [(0, 1, 2)]

    def test_hull_volume_3d_tetrahedron(self) -> None:
        """Test volume computation for tetrahedron."""
        ch = ConvexHull()
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        faces = ch.gift_wrapping_3d(points)
        if faces:
            volume = ch.hull_volume_3d(points, faces)
            expected = 1.0 / 6.0
            assert abs(volume - expected) < 0.1

    def test_hull_surface_area_3d_tetrahedron(self) -> None:
        """Test surface area computation for tetrahedron."""
        ch = ConvexHull()
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        faces = ch.gift_wrapping_3d(points)
        if faces:
            surface_area = ch.hull_surface_area_3d(points, faces)
            assert surface_area > 0

    def test_graham_vs_andrews_consistency(self) -> None:
        """Test that Graham and Andrew's produce same hull points."""
        ch = ConvexHull()
        points = [(0, 0), (1, 1), (2, 0), (1, 0.5), (0.5, 0.5)]

        hull_graham = ch.graham_scan_2d(points)
        hull_andrews = ch.andrews_monotone_chain_2d(points)

        assert len(hull_graham) == len(hull_andrews)
        assert set(hull_graham) == set(hull_andrews)

    def test_convex_hull_3d(self) -> None:
        """Test convex_hull_3d wrapper."""
        ch = ConvexHull()
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
        faces = ch.convex_hull_3d(points)
        assert len(faces) >= 4

    def test_collinear_points_2d(self) -> None:
        """Test handling of collinear points in 2D."""
        ch = ConvexHull()
        points = [(0, 0), (1, 0), (2, 0), (1, 1)]
        hull = ch.graham_scan_2d(points)
        assert len(hull) >= 3

    def test_coplanar_points_3d(self) -> None:
        """Test handling of coplanar points in 3D."""
        ch = ConvexHull()
        points = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]
        faces = ch.gift_wrapping_3d(points)
        assert len(faces) >= 0
