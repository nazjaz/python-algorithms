"""Test suite for line sweep algorithm implementation."""

import pytest

from src.main import EventType, LineSweep


class TestLineSweep:
    """Test cases for LineSweep class."""

    def test_initialization(self) -> None:
        """Test LineSweep initialization."""
        ls = LineSweep()
        assert ls is not None

    def test_cross_product(self) -> None:
        """Test cross product computation."""
        ls = LineSweep()
        o = (0, 0)
        a = (1, 0)
        b = (0, 1)
        cross = ls._cross_product(o, a, b)
        assert cross > 0

    def test_orientation(self) -> None:
        """Test orientation computation."""
        ls = LineSweep()
        p = (0, 0)
        q = (1, 0)
        r = (0, 1)
        orient = ls._orientation(p, q, r)
        assert orient == 1

    def test_on_segment(self) -> None:
        """Test on_segment check."""
        ls = LineSweep()
        p = (0, 0)
        q = (2, 2)
        r = (1, 1)
        assert ls._on_segment(p, q, r) is True

    def test_segments_intersect_intersecting(self) -> None:
        """Test segments_intersect with intersecting segments."""
        ls = LineSweep()
        seg1 = ((0, 0), (2, 2))
        seg2 = ((1, 1), (3, 0))
        intersection = ls.segments_intersect(seg1, seg2)
        assert intersection is not None
        assert abs(intersection[0] - 1.0) < 1e-9
        assert abs(intersection[1] - 1.0) < 1e-9

    def test_segments_intersect_non_intersecting(self) -> None:
        """Test segments_intersect with non-intersecting segments."""
        ls = LineSweep()
        seg1 = ((0, 0), (1, 1))
        seg2 = ((2, 2), (3, 3))
        intersection = ls.segments_intersect(seg1, seg2)
        assert intersection is None

    def test_segments_intersect_collinear(self) -> None:
        """Test segments_intersect with collinear segments."""
        ls = LineSweep()
        seg1 = ((0, 0), (2, 2))
        seg2 = ((1, 1), (3, 3))
        intersection = ls.segments_intersect(seg1, seg2)
        assert intersection is not None

    def test_segments_intersect_endpoint(self) -> None:
        """Test segments_intersect with endpoint intersection."""
        ls = LineSweep()
        seg1 = ((0, 0), (2, 2))
        seg2 = ((2, 2), (3, 3))
        intersection = ls.segments_intersect(seg1, seg2)
        assert intersection == (2, 2)

    def test_find_segment_intersections_empty(self) -> None:
        """Test find_segment_intersections with empty list."""
        ls = LineSweep()
        intersections = ls.find_segment_intersections([])
        assert intersections == []

    def test_find_segment_intersections_single(self) -> None:
        """Test find_segment_intersections with single segment."""
        ls = LineSweep()
        segments = [((0, 0), (2, 2))]
        intersections = ls.find_segment_intersections(segments)
        assert intersections == []

    def test_find_segment_intersections_multiple(self) -> None:
        """Test find_segment_intersections with multiple segments."""
        ls = LineSweep()
        segments = [
            ((0, 0), (2, 2)),
            ((1, 1), (3, 0)),
            ((0, 2), (2, 0)),
        ]
        intersections = ls.find_segment_intersections(segments)
        assert len(intersections) > 0

    def test_rectangles_intersect_intersecting(self) -> None:
        """Test rectangles_intersect with intersecting rectangles."""
        ls = LineSweep()
        rect1 = ((0, 0), (2, 2))
        rect2 = ((1, 1), (3, 3))
        assert ls.rectangles_intersect(rect1, rect2) is True

    def test_rectangles_intersect_non_intersecting(self) -> None:
        """Test rectangles_intersect with non-intersecting rectangles."""
        ls = LineSweep()
        rect1 = ((0, 0), (1, 1))
        rect2 = ((2, 2), (3, 3))
        assert ls.rectangles_intersect(rect1, rect2) is False

    def test_rectangles_intersect_touching(self) -> None:
        """Test rectangles_intersect with touching rectangles."""
        ls = LineSweep()
        rect1 = ((0, 0), (1, 1))
        rect2 = ((1, 0), (2, 1))
        assert ls.rectangles_intersect(rect1, rect2) is True

    def test_find_rectangle_intersections_empty(self) -> None:
        """Test find_rectangle_intersections with empty list."""
        ls = LineSweep()
        intersections = ls.find_rectangle_intersections([])
        assert intersections == []

    def test_find_rectangle_intersections_single(self) -> None:
        """Test find_rectangle_intersections with single rectangle."""
        ls = LineSweep()
        rectangles = [((0, 0), (2, 2))]
        intersections = ls.find_rectangle_intersections(rectangles)
        assert intersections == []

    def test_find_rectangle_intersections_multiple(self) -> None:
        """Test find_rectangle_intersections with multiple rectangles."""
        ls = LineSweep()
        rectangles = [
            ((0, 0), (2, 2)),
            ((1, 1), (3, 3)),
            ((4, 4), (5, 5)),
        ]
        intersections = ls.find_rectangle_intersections(rectangles)
        assert len(intersections) > 0

    def test_distance_squared(self) -> None:
        """Test distance_squared computation."""
        ls = LineSweep()
        p1 = (0, 0)
        p2 = (3, 4)
        dist_sq = ls._distance_squared(p1, p2)
        assert abs(dist_sq - 25.0) < 1e-9

    def test_distance(self) -> None:
        """Test distance computation."""
        ls = LineSweep()
        p1 = (0, 0)
        p2 = (3, 4)
        dist = ls._distance(p1, p2)
        assert abs(dist - 5.0) < 1e-9

    def test_closest_pair_naive(self) -> None:
        """Test closest_pair_naive."""
        ls = LineSweep()
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        p1, p2, dist = ls.closest_pair_naive(points)
        assert dist > 0
        assert p1 in points
        assert p2 in points

    def test_closest_pair_naive_insufficient_points(self) -> None:
        """Test closest_pair_naive with insufficient points."""
        ls = LineSweep()
        with pytest.raises(ValueError, match="Need at least 2 points"):
            ls.closest_pair_naive([(0, 0)])

    def test_closest_pair_sweep(self) -> None:
        """Test closest_pair_sweep."""
        ls = LineSweep()
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        p1, p2, dist = ls.closest_pair_sweep(points)
        assert dist > 0
        assert p1 in points
        assert p2 in points

    def test_closest_pair_sweep_two_points(self) -> None:
        """Test closest_pair_sweep with two points."""
        ls = LineSweep()
        points = [(0, 0), (1, 1)]
        p1, p2, dist = ls.closest_pair_sweep(points)
        assert abs(dist - 1.4142135623730951) < 1e-9

    def test_closest_pair_sweep_insufficient_points(self) -> None:
        """Test closest_pair_sweep with insufficient points."""
        ls = LineSweep()
        with pytest.raises(ValueError, match="Need at least 2 points"):
            ls.closest_pair_sweep([(0, 0)])

    def test_closest_pair_divide_conquer(self) -> None:
        """Test closest_pair_divide_conquer."""
        ls = LineSweep()
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        p1, p2, dist = ls.closest_pair_divide_conquer(points)
        assert dist > 0
        assert p1 in points
        assert p2 in points

    def test_closest_pair_divide_conquer_two_points(self) -> None:
        """Test closest_pair_divide_conquer with two points."""
        ls = LineSweep()
        points = [(0, 0), (1, 1)]
        p1, p2, dist = ls.closest_pair_divide_conquer(points)
        assert abs(dist - 1.4142135623730951) < 1e-9

    def test_closest_pair_divide_conquer_three_points(self) -> None:
        """Test closest_pair_divide_conquer with three points."""
        ls = LineSweep()
        points = [(0, 0), (1, 1), (2, 0)]
        p1, p2, dist = ls.closest_pair_divide_conquer(points)
        assert dist > 0

    def test_closest_pair_divide_conquer_insufficient_points(self) -> None:
        """Test closest_pair_divide_conquer with insufficient points."""
        ls = LineSweep()
        with pytest.raises(ValueError, match="Need at least 2 points"):
            ls.closest_pair_divide_conquer([(0, 0)])

    def test_find_all_closest_pairs(self) -> None:
        """Test find_all_closest_pairs."""
        ls = LineSweep()
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]
        pairs = ls.find_all_closest_pairs(points)
        assert len(pairs) > 0
        for p1, p2, dist in pairs:
            assert dist > 0

    def test_find_all_closest_pairs_empty(self) -> None:
        """Test find_all_closest_pairs with empty list."""
        ls = LineSweep()
        pairs = ls.find_all_closest_pairs([])
        assert pairs == []

    def test_find_all_closest_pairs_single(self) -> None:
        """Test find_all_closest_pairs with single point."""
        ls = LineSweep()
        pairs = ls.find_all_closest_pairs([(0, 0)])
        assert pairs == []

    def test_closest_pair_consistency(self) -> None:
        """Test that all closest pair algorithms produce same distance."""
        ls = LineSweep()
        points = [(0, 0), (1, 1), (2, 2), (3, 3)]

        _, _, dist_naive = ls.closest_pair_naive(points)
        _, _, dist_sweep = ls.closest_pair_sweep(points)
        _, _, dist_divide = ls.closest_pair_divide_conquer(points)

        assert abs(dist_naive - dist_sweep) < 1e-9
        assert abs(dist_sweep - dist_divide) < 1e-9

    def test_segment_intersection_parallel(self) -> None:
        """Test segment intersection with parallel segments."""
        ls = LineSweep()
        seg1 = ((0, 0), (2, 0))
        seg2 = ((0, 1), (2, 1))
        intersection = ls.segments_intersect(seg1, seg2)
        assert intersection is None

    def test_segment_intersection_perpendicular(self) -> None:
        """Test segment intersection with perpendicular segments."""
        ls = LineSweep()
        seg1 = ((0, 0), (2, 0))
        seg2 = ((1, -1), (1, 1))
        intersection = ls.segments_intersect(seg1, seg2)
        assert intersection == (1, 0)

    def test_rectangle_intersection_contained(self) -> None:
        """Test rectangle intersection with one contained in other."""
        ls = LineSweep()
        rect1 = ((0, 0), (4, 4))
        rect2 = ((1, 1), (3, 3))
        assert ls.rectangles_intersect(rect1, rect2) is True

    def test_rectangle_intersection_disjoint(self) -> None:
        """Test rectangle intersection with disjoint rectangles."""
        ls = LineSweep()
        rect1 = ((0, 0), (1, 1))
        rect2 = ((2, 2), (3, 3))
        assert ls.rectangles_intersect(rect1, rect2) is False

    def test_closest_pair_square(self) -> None:
        """Test closest pair with square of points."""
        ls = LineSweep()
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        p1, p2, dist = ls.closest_pair_sweep(points)
        assert abs(dist - 1.0) < 1e-9

    def test_closest_pair_equidistant(self) -> None:
        """Test closest pair with equidistant points."""
        ls = LineSweep()
        points = [(0, 0), (1, 0), (0, 1), (1, 1)]
        pairs = ls.find_all_closest_pairs(points)
        assert len(pairs) >= 2
