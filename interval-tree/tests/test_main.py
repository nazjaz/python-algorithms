"""Unit tests for interval tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Interval, IntervalNode, IntervalTree


class TestInterval:
    """Test cases for Interval class."""

    def test_interval_creation(self):
        """Test Interval creation."""
        interval = Interval(10, 20)
        assert interval.low == 10
        assert interval.high == 20

    def test_interval_invalid(self):
        """Test Interval with invalid range."""
        with pytest.raises(ValueError):
            Interval(20, 10)

    def test_interval_equality(self):
        """Test Interval equality."""
        interval1 = Interval(10, 20)
        interval2 = Interval(10, 20)
        interval3 = Interval(10, 30)
        assert interval1 == interval2
        assert interval1 != interval3

    def test_interval_overlaps(self):
        """Test interval overlap detection."""
        interval1 = Interval(10, 20)
        interval2 = Interval(15, 25)
        interval3 = Interval(25, 30)
        assert interval1.overlaps(interval2) is True
        assert interval1.overlaps(interval3) is False

    def test_interval_overlaps_point(self):
        """Test point overlap detection."""
        interval = Interval(10, 20)
        assert interval.overlaps_point(15) is True
        assert interval.overlaps_point(10) is True
        assert interval.overlaps_point(20) is True
        assert interval.overlaps_point(5) is False
        assert interval.overlaps_point(25) is False

    def test_interval_repr(self):
        """Test Interval string representation."""
        interval = Interval(10, 20)
        assert "Interval" in repr(interval)
        assert "10" in repr(interval)
        assert "20" in repr(interval)


class TestIntervalNode:
    """Test cases for IntervalNode class."""

    def test_interval_node_creation(self):
        """Test IntervalNode creation."""
        interval = Interval(10, 20)
        node = IntervalNode(interval)
        assert node.interval == interval
        assert node.max_endpoint == 20
        assert node.left is None
        assert node.right is None

    def test_update_max_endpoint(self):
        """Test max endpoint update."""
        node = IntervalNode(Interval(10, 20))
        node.left = IntervalNode(Interval(5, 25))
        node.right = IntervalNode(Interval(15, 30))
        node.update_max_endpoint()
        assert node.max_endpoint == 30


class TestIntervalTree:
    """Test cases for IntervalTree class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def tree(self, config_file):
        """Create IntervalTree instance."""
        return IntervalTree(config_path=config_file)

    def test_tree_creation(self, tree):
        """Test IntervalTree creation."""
        assert tree.get_size() == 0
        assert tree.is_empty() is True
        assert tree.root is None

    def test_insert_single_interval(self, tree):
        """Test inserting single interval."""
        result = tree.insert(10, 20)
        assert result is True
        assert tree.get_size() == 1
        assert tree.is_empty() is False

    def test_insert_multiple_intervals(self, tree):
        """Test inserting multiple intervals."""
        intervals = [(10, 20), (15, 25), (5, 15), (20, 30)]
        for low, high in intervals:
            result = tree.insert(low, high)
            assert result is True
        assert tree.get_size() == len(intervals)

    def test_insert_duplicate(self, tree):
        """Test inserting duplicate interval."""
        tree.insert(10, 20)
        result = tree.insert(10, 20)
        assert result is False
        assert tree.get_size() == 1

    def test_insert_invalid_interval(self, tree):
        """Test inserting invalid interval."""
        with pytest.raises(ValueError):
            tree.insert(20, 10)

    def test_delete_existing(self, tree):
        """Test deleting existing interval."""
        tree.insert(10, 20)
        tree.insert(15, 25)
        result = tree.delete(10, 20)
        assert result is True
        assert tree.get_size() == 1

    def test_delete_nonexistent(self, tree):
        """Test deleting nonexistent interval."""
        tree.insert(10, 20)
        result = tree.delete(15, 25)
        assert result is False
        assert tree.get_size() == 1

    def test_delete_empty(self, tree):
        """Test deleting from empty tree."""
        result = tree.delete(10, 20)
        assert result is False

    def test_find_overlapping_intervals(self, tree):
        """Test finding overlapping intervals."""
        tree.insert(10, 20)
        tree.insert(15, 25)
        tree.insert(5, 15)
        tree.insert(30, 40)

        overlapping = tree.find_overlapping_intervals(12, 18)
        assert len(overlapping) == 3
        assert Interval(10, 20) in overlapping
        assert Interval(15, 25) in overlapping
        assert Interval(5, 15) in overlapping

    def test_find_overlapping_intervals_none(self, tree):
        """Test finding overlapping intervals when none exist."""
        tree.insert(10, 20)
        tree.insert(30, 40)

        overlapping = tree.find_overlapping_intervals(50, 60)
        assert len(overlapping) == 0

    def test_find_intervals_containing_point(self, tree):
        """Test finding intervals containing a point."""
        tree.insert(10, 20)
        tree.insert(15, 25)
        tree.insert(5, 15)
        tree.insert(30, 40)

        containing = tree.find_intervals_containing_point(15)
        assert len(containing) == 3
        assert Interval(10, 20) in containing
        assert Interval(15, 25) in containing
        assert Interval(5, 15) in containing

    def test_find_intervals_containing_point_none(self, tree):
        """Test finding intervals containing point when none exist."""
        tree.insert(10, 20)
        tree.insert(30, 40)

        containing = tree.find_intervals_containing_point(50)
        assert len(containing) == 0

    def test_get_all_intervals(self, tree):
        """Test getting all intervals."""
        intervals = [(30, 40), (10, 20), (50, 60), (5, 15)]
        for low, high in intervals:
            tree.insert(low, high)

        all_intervals = tree.get_all_intervals()
        assert len(all_intervals) == 4
        assert all_intervals[0].low == 5
        assert all_intervals[-1].low == 50

    def test_clear(self, tree):
        """Test clearing tree."""
        tree.insert(10, 20)
        tree.insert(15, 25)
        tree.clear()
        assert tree.get_size() == 0
        assert tree.is_empty() is True

    def test_large_insertions(self, config_file):
        """Test with large number of insertions."""
        tree = IntervalTree(config_path=config_file)
        for i in range(100):
            tree.insert(i * 10, i * 10 + 5)
        assert tree.get_size() == 100

    def test_overlapping_query_edge_cases(self, tree):
        """Test overlapping queries with edge cases."""
        tree.insert(10, 20)
        tree.insert(15, 25)

        overlapping = tree.find_overlapping_intervals(20, 20)
        assert Interval(10, 20) in overlapping
        assert Interval(15, 25) in overlapping

        overlapping = tree.find_overlapping_intervals(10, 10)
        assert Interval(10, 20) in overlapping

    def test_point_query_edge_cases(self, tree):
        """Test point queries with edge cases."""
        tree.insert(10, 20)
        tree.insert(15, 25)

        containing = tree.find_intervals_containing_point(10)
        assert Interval(10, 20) in containing

        containing = tree.find_intervals_containing_point(20)
        assert Interval(10, 20) in containing
        assert Interval(15, 25) in containing

    def test_adjacent_intervals(self, tree):
        """Test with adjacent intervals."""
        tree.insert(10, 20)
        tree.insert(20, 30)

        overlapping = tree.find_overlapping_intervals(15, 25)
        assert Interval(10, 20) in overlapping
        assert Interval(20, 30) in overlapping

    def test_nested_intervals(self, tree):
        """Test with nested intervals."""
        tree.insert(10, 30)
        tree.insert(15, 25)

        overlapping = tree.find_overlapping_intervals(20, 20)
        assert len(overlapping) == 2

    def test_single_point_intervals(self, tree):
        """Test with single point intervals."""
        tree.insert(10, 10)
        tree.insert(15, 15)
        tree.insert(20, 20)

        containing = tree.find_intervals_containing_point(10)
        assert Interval(10, 10) in containing

        overlapping = tree.find_overlapping_intervals(10, 10)
        assert Interval(10, 10) in overlapping

    def test_sequential_operations(self, tree):
        """Test sequential insert and delete operations."""
        for i in range(20):
            tree.insert(i * 10, i * 10 + 5)
        assert tree.get_size() == 20

        for i in range(0, 20, 2):
            tree.delete(i * 10, i * 10 + 5)
        assert tree.get_size() == 10

    def test_query_after_deletion(self, tree):
        """Test queries after deletion."""
        tree.insert(10, 20)
        tree.insert(15, 25)
        tree.insert(30, 40)

        tree.delete(15, 25)
        overlapping = tree.find_overlapping_intervals(15, 25)
        assert Interval(15, 25) not in overlapping
        assert Interval(10, 20) in overlapping

    def test_empty_tree_operations(self, tree):
        """Test operations on empty tree."""
        assert tree.find_overlapping_intervals(10, 20) == []
        assert tree.find_intervals_containing_point(15) == []
        assert tree.get_all_intervals() == []
        assert tree.delete(10, 20) is False

    def test_invalid_query_interval(self, tree):
        """Test query with invalid interval."""
        tree.insert(10, 20)
        with pytest.raises(ValueError):
            tree.find_overlapping_intervals(20, 10)

    def test_max_endpoint_maintenance(self, tree):
        """Test that max endpoint is maintained correctly."""
        tree.insert(10, 20)
        tree.insert(5, 25)
        tree.insert(15, 30)
        tree.insert(20, 35)

        overlapping = tree.find_overlapping_intervals(22, 28)
        assert Interval(5, 25) in overlapping
        assert Interval(15, 30) in overlapping

    def test_complex_overlap_scenario(self, tree):
        """Test complex overlap scenario."""
        intervals = [
            (15, 20),
            (10, 30),
            (17, 19),
            (5, 20),
            (12, 15),
            (30, 40),
        ]
        for low, high in intervals:
            tree.insert(low, high)

        overlapping = tree.find_overlapping_intervals(14, 16)
        assert len(overlapping) >= 3

        containing = tree.find_intervals_containing_point(18)
        assert len(containing) >= 3
