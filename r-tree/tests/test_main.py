"""Unit tests for R-tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Rectangle, RTreeNode, RTree


class TestRectangle:
    """Test cases for Rectangle class."""

    def test_rectangle_creation(self):
        """Test Rectangle creation."""
        rect = Rectangle(1, 2, 3, 4)
        assert rect.min_x == 1
        assert rect.min_y == 2
        assert rect.max_x == 3
        assert rect.max_y == 4

    def test_rectangle_invalid(self):
        """Test Rectangle with invalid coordinates."""
        with pytest.raises(ValueError):
            Rectangle(3, 2, 1, 4)

        with pytest.raises(ValueError):
            Rectangle(1, 4, 3, 2)

    def test_rectangle_area(self):
        """Test rectangle area calculation."""
        rect = Rectangle(0, 0, 5, 10)
        assert rect.area() == 50

    def test_rectangle_intersects(self):
        """Test rectangle intersection."""
        rect1 = Rectangle(1, 1, 3, 3)
        rect2 = Rectangle(2, 2, 4, 4)
        rect3 = Rectangle(5, 5, 7, 7)

        assert rect1.intersects(rect2) is True
        assert rect1.intersects(rect3) is False

    def test_rectangle_contains(self):
        """Test rectangle containment."""
        rect1 = Rectangle(0, 0, 10, 10)
        rect2 = Rectangle(2, 2, 5, 5)
        rect3 = Rectangle(2, 2, 15, 15)

        assert rect1.contains(rect2) is True
        assert rect1.contains(rect3) is False

    def test_rectangle_union(self):
        """Test rectangle union."""
        rect1 = Rectangle(1, 1, 3, 3)
        rect2 = Rectangle(2, 2, 4, 4)
        union = rect1.union(rect2)

        assert union.min_x == 1
        assert union.min_y == 1
        assert union.max_x == 4
        assert union.max_y == 4

    def test_rectangle_expansion_area(self):
        """Test expansion area calculation."""
        rect1 = Rectangle(1, 1, 3, 3)
        rect2 = Rectangle(2, 2, 5, 5)
        expansion = rect1.expansion_area(rect2)

        assert expansion > 0

    def test_rectangle_repr(self):
        """Test Rectangle string representation."""
        rect = Rectangle(1, 2, 3, 4)
        assert "Rectangle" in repr(rect)


class TestRTreeNode:
    """Test cases for RTreeNode class."""

    def test_r_tree_node_creation_leaf(self):
        """Test RTreeNode creation as leaf."""
        node = RTreeNode(is_leaf=True)
        assert node.is_leaf is True
        assert len(node.entries) == 0
        assert node.mbr is None

    def test_r_tree_node_creation_internal(self):
        """Test RTreeNode creation as internal."""
        node = RTreeNode(is_leaf=False)
        assert node.is_leaf is False
        assert len(node.entries) == 0

    def test_update_mbr(self):
        """Test MBR update."""
        node = RTreeNode(is_leaf=True)
        rect1 = Rectangle(1, 1, 3, 3)
        rect2 = Rectangle(2, 2, 4, 4)
        node.entries.append((rect1, None, None))
        node.entries.append((rect2, None, None))
        node.update_mbr()

        assert node.mbr is not None
        assert node.mbr.min_x == 1
        assert node.mbr.max_x == 4


class TestRTree:
    """Test cases for RTree class."""

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
        """Create RTree instance."""
        return RTree(max_entries=4, min_entries=2, config_path=config_file)

    def test_tree_creation(self, tree):
        """Test RTree creation."""
        assert tree.get_size() == 0
        assert tree.is_empty() is True
        assert tree.root is None

    def test_tree_creation_invalid_config(self, config_file):
        """Test RTree creation with invalid config."""
        with pytest.raises(ValueError):
            RTree(max_entries=2, min_entries=4, config_path=config_file)

    def test_insert_single_rectangle(self, tree):
        """Test inserting single rectangle."""
        tree.insert(1, 1, 3, 3)
        assert tree.get_size() == 1
        assert tree.is_empty() is False

    def test_insert_multiple_rectangles(self, tree):
        """Test inserting multiple rectangles."""
        rectangles = [
            (1, 1, 3, 3),
            (2, 2, 4, 4),
            (5, 5, 7, 7),
            (6, 6, 8, 8),
        ]
        for min_x, min_y, max_x, max_y in rectangles:
            tree.insert(min_x, min_y, max_x, max_y)
        assert tree.get_size() == len(rectangles)

    def test_insert_invalid_rectangle(self, tree):
        """Test inserting invalid rectangle."""
        with pytest.raises(ValueError):
            tree.insert(3, 3, 1, 1)

    def test_insert_with_data(self, tree):
        """Test inserting rectangle with data."""
        tree.insert(1, 1, 3, 3, data="test_data")
        results = tree.range_query(0, 0, 10, 10)
        assert len(results) == 1
        assert results[0][1] == "test_data"

    def test_range_query_single_result(self, tree):
        """Test range query with single result."""
        tree.insert(1, 1, 3, 3)
        results = tree.range_query(0, 0, 5, 5)
        assert len(results) == 1

    def test_range_query_multiple_results(self, tree):
        """Test range query with multiple results."""
        rectangles = [
            (1, 1, 3, 3),
            (2, 2, 4, 4),
            (5, 5, 7, 7),
            (6, 6, 8, 8),
        ]
        for min_x, min_y, max_x, max_y in rectangles:
            tree.insert(min_x, min_y, max_x, max_y)

        results = tree.range_query(2, 2, 6, 6)
        assert len(results) >= 2

    def test_range_query_no_results(self, tree):
        """Test range query with no results."""
        tree.insert(1, 1, 3, 3)
        results = tree.range_query(10, 10, 20, 20)
        assert len(results) == 0

    def test_range_query_empty(self, config_file):
        """Test range query on empty tree."""
        tree = RTree(config_path=config_file)
        results = tree.range_query(0, 0, 10, 10)
        assert results == []

    def test_range_query_invalid(self, tree):
        """Test range query with invalid rectangle."""
        tree.insert(1, 1, 3, 3)
        with pytest.raises(ValueError):
            tree.range_query(10, 10, 5, 5)

    def test_get_all_rectangles(self, tree):
        """Test getting all rectangles."""
        rectangles = [
            (1, 1, 3, 3),
            (2, 2, 4, 4),
            (5, 5, 7, 7),
        ]
        for min_x, min_y, max_x, max_y in rectangles:
            tree.insert(min_x, min_y, max_x, max_y)

        all_rects = tree.get_all_rectangles()
        assert len(all_rects) == len(rectangles)

    def test_clear(self, tree):
        """Test clearing tree."""
        tree.insert(1, 1, 3, 3)
        tree.insert(2, 2, 4, 4)
        tree.clear()
        assert tree.get_size() == 0
        assert tree.is_empty() is True

    def test_large_insertions(self, config_file):
        """Test with large number of insertions."""
        tree = RTree(max_entries=4, min_entries=2, config_path=config_file)
        for i in range(50):
            tree.insert(i, i, i + 1, i + 1)
        assert tree.get_size() == 50

        results = tree.range_query(10, 10, 30, 30)
        assert len(results) > 0

    def test_node_splitting(self, config_file):
        """Test node splitting with many insertions."""
        tree = RTree(max_entries=3, min_entries=1, config_path=config_file)
        for i in range(10):
            tree.insert(i, i, i + 1, i + 1)
        assert tree.get_size() == 10

        all_rects = tree.get_all_rectangles()
        assert len(all_rects) == 10

    def test_overlapping_rectangles(self, tree):
        """Test with overlapping rectangles."""
        tree.insert(1, 1, 5, 5)
        tree.insert(2, 2, 6, 6)
        tree.insert(3, 3, 7, 7)

        results = tree.range_query(2, 2, 6, 6)
        assert len(results) >= 2

    def test_adjacent_rectangles(self, tree):
        """Test with adjacent rectangles."""
        tree.insert(1, 1, 3, 3)
        tree.insert(3, 1, 5, 3)
        tree.insert(1, 3, 3, 5)

        results = tree.range_query(0, 0, 6, 6)
        assert len(results) == 3

    def test_nested_rectangles(self, tree):
        """Test with nested rectangles."""
        tree.insert(1, 1, 10, 10)
        tree.insert(2, 2, 5, 5)
        tree.insert(3, 3, 4, 4)

        results = tree.range_query(0, 0, 15, 15)
        assert len(results) == 3

    def test_point_rectangles(self, tree):
        """Test with point rectangles."""
        tree.insert(1, 1, 1, 1)
        tree.insert(2, 2, 2, 2)
        tree.insert(3, 3, 3, 3)

        results = tree.range_query(0, 0, 5, 5)
        assert len(results) == 3

    def test_sequential_operations(self, tree):
        """Test sequential insert and query operations."""
        for i in range(10):
            tree.insert(i, i, i + 1, i + 1)

        for i in range(0, 10, 2):
            results = tree.range_query(i - 0.5, i - 0.5, i + 1.5, i + 1.5)
            assert len(results) > 0

    def test_query_after_clear(self, tree):
        """Test queries after clearing."""
        tree.insert(1, 1, 3, 3)
        tree.clear()
        results = tree.range_query(0, 0, 10, 10)
        assert results == []

    def test_different_max_entries(self, config_file):
        """Test with different max_entries values."""
        tree = RTree(max_entries=2, min_entries=1, config_path=config_file)
        for i in range(5):
            tree.insert(i, i, i + 1, i + 1)
        assert tree.get_size() == 5

        results = tree.range_query(0, 0, 10, 10)
        assert len(results) == 5
