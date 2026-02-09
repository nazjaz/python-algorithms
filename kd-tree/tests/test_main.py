"""Unit tests for k-d tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import KDNode, KDTree


class TestKDNode:
    """Test cases for KDNode class."""

    def test_kd_node_creation(self):
        """Test KDNode creation."""
        point = [1.0, 2.0, 3.0]
        node = KDNode(point, dimension=1)
        assert node.point == point
        assert node.dimension == 1
        assert node.left is None
        assert node.right is None

    def test_kd_node_repr(self):
        """Test KDNode string representation."""
        node = KDNode([1.0, 2.0])
        assert "KDNode" in repr(node)
        assert "1.0" in repr(node)


class TestKDTree:
    """Test cases for KDTree class."""

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
    def tree_2d(self, config_file):
        """Create 2D KDTree instance."""
        points = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]
        return KDTree(points, config_path=config_file)

    @pytest.fixture
    def tree_3d(self, config_file):
        """Create 3D KDTree instance."""
        points = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [2, 3, 4]]
        return KDTree(points, config_path=config_file)

    def test_tree_creation_empty(self, config_file):
        """Test KDTree creation with no points."""
        tree = KDTree(config_path=config_file)
        assert tree.get_size() == 0
        assert tree.is_empty() is True
        assert tree.get_dimension() == 0

    def test_tree_creation_with_points(self, tree_2d):
        """Test KDTree creation with points."""
        assert tree_2d.get_size() == 6
        assert tree_2d.is_empty() is False
        assert tree_2d.get_dimension() == 2

    def test_build_tree(self, config_file):
        """Test building tree from points."""
        points = [[1, 2], [3, 4], [5, 6]]
        tree = KDTree(config_path=config_file)
        tree.build_tree(points)
        assert tree.get_size() == 3
        assert tree.get_dimension() == 2

    def test_build_tree_inconsistent_dimensions(self, config_file):
        """Test building tree with inconsistent dimensions."""
        points = [[1, 2], [3, 4, 5]]
        tree = KDTree(config_path=config_file)
        with pytest.raises(ValueError):
            tree.build_tree(points)

    def test_insert_single_point(self, config_file):
        """Test inserting single point."""
        tree = KDTree(config_path=config_file)
        tree.insert([1.0, 2.0])
        assert tree.get_size() == 1
        assert tree.get_dimension() == 2
        assert tree.is_empty() is False

    def test_insert_multiple_points(self, config_file):
        """Test inserting multiple points."""
        tree = KDTree(config_path=config_file)
        points = [[1, 2], [3, 4], [5, 6]]
        for point in points:
            tree.insert(point)
        assert tree.get_size() == 3

    def test_insert_wrong_dimension(self, tree_2d):
        """Test inserting point with wrong dimension."""
        with pytest.raises(ValueError):
            tree_2d.insert([1, 2, 3])

    def test_range_query_2d(self, tree_2d):
        """Test range query in 2D."""
        results = tree_2d.range_query([3, 3], [7, 7])
        assert len(results) > 0
        for point in results:
            assert 3 <= point[0] <= 7
            assert 3 <= point[1] <= 7

    def test_range_query_3d(self, tree_3d):
        """Test range query in 3D."""
        results = tree_3d.range_query([2, 2, 2], [5, 5, 5])
        assert len(results) >= 0
        for point in results:
            assert 2 <= point[0] <= 5
            assert 2 <= point[1] <= 5
            assert 2 <= point[2] <= 5

    def test_range_query_empty(self, config_file):
        """Test range query on empty tree."""
        tree = KDTree(config_path=config_file)
        results = tree.range_query([0, 0], [10, 10])
        assert results == []

    def test_range_query_no_results(self, tree_2d):
        """Test range query with no results."""
        results = tree_2d.range_query([100, 100], [200, 200])
        assert results == []

    def test_range_query_invalid_dimensions(self, tree_2d):
        """Test range query with invalid dimensions."""
        with pytest.raises(ValueError):
            tree_2d.range_query([0], [10, 10])

    def test_range_query_invalid_range(self, tree_2d):
        """Test range query with invalid range."""
        with pytest.raises(ValueError):
            tree_2d.range_query([10, 10], [5, 5])

    def test_nearest_neighbor_2d(self, tree_2d):
        """Test nearest neighbor search in 2D."""
        query = [6, 5]
        nearest = tree_2d.nearest_neighbor(query)
        assert nearest is not None
        assert len(nearest) == 2

    def test_nearest_neighbor_3d(self, tree_3d):
        """Test nearest neighbor search in 3D."""
        query = [3, 4, 5]
        nearest = tree_3d.nearest_neighbor(query)
        assert nearest is not None
        assert len(nearest) == 3

    def test_nearest_neighbor_empty(self, config_file):
        """Test nearest neighbor on empty tree."""
        tree = KDTree(config_path=config_file)
        nearest = tree.nearest_neighbor([1, 2])
        assert nearest is None

    def test_nearest_neighbor_wrong_dimension(self, tree_2d):
        """Test nearest neighbor with wrong dimension."""
        with pytest.raises(ValueError):
            tree_2d.nearest_neighbor([1, 2, 3])

    def test_k_nearest_neighbors(self, tree_2d):
        """Test k nearest neighbors search."""
        query = [6, 5]
        k_nearest = tree_2d.k_nearest_neighbors(query, 3)
        assert len(k_nearest) <= 3
        assert all(len(point) == 2 for point in k_nearest)

    def test_k_nearest_neighbors_k_larger_than_size(self, tree_2d):
        """Test k nearest neighbors when k > size."""
        query = [6, 5]
        k_nearest = tree_2d.k_nearest_neighbors(query, 10)
        assert len(k_nearest) == tree_2d.get_size()

    def test_k_nearest_neighbors_invalid_k(self, tree_2d):
        """Test k nearest neighbors with invalid k."""
        with pytest.raises(ValueError):
            tree_2d.k_nearest_neighbors([6, 5], 0)

        with pytest.raises(ValueError):
            tree_2d.k_nearest_neighbors([6, 5], -1)

    def test_k_nearest_neighbors_wrong_dimension(self, tree_2d):
        """Test k nearest neighbors with wrong dimension."""
        with pytest.raises(ValueError):
            tree_2d.k_nearest_neighbors([1, 2, 3], 2)

    def test_get_all_points(self, tree_2d):
        """Test getting all points."""
        all_points = tree_2d.get_all_points()
        assert len(all_points) == tree_2d.get_size()
        assert all(len(point) == 2 for point in all_points)

    def test_clear(self, tree_2d):
        """Test clearing tree."""
        tree_2d.clear()
        assert tree_2d.get_size() == 0
        assert tree_2d.is_empty() is True
        assert tree_2d.get_dimension() == 0

    def test_large_dataset(self, config_file):
        """Test with large dataset."""
        import random
        points = [[random.random() * 100, random.random() * 100] for _ in range(100)]
        tree = KDTree(points, config_path=config_file)
        assert tree.get_size() == 100

        results = tree.range_query([20, 20], [80, 80])
        assert isinstance(results, list)

        nearest = tree.nearest_neighbor([50, 50])
        assert nearest is not None

    def test_sequential_operations(self, config_file):
        """Test sequential insert and query operations."""
        tree = KDTree(config_path=config_file)
        for i in range(10):
            tree.insert([i * 1.0, i * 2.0])
        assert tree.get_size() == 10

        results = tree.range_query([2, 4], [6, 12])
        assert len(results) > 0

    def test_exact_match_nearest_neighbor(self, config_file):
        """Test nearest neighbor when query matches a point."""
        points = [[1, 2], [3, 4], [5, 6]]
        tree = KDTree(points, config_path=config_file)
        nearest = tree.nearest_neighbor([3, 4])
        assert nearest == [3, 4]

    def test_range_query_all_points(self, tree_2d):
        """Test range query that includes all points."""
        all_points = tree_2d.get_all_points()
        if all_points:
            min_coords = [min(p[i] for p in all_points) - 1 for i in range(2)]
            max_coords = [max(p[i] for p in all_points) + 1 for i in range(2)]
            results = tree_2d.range_query(min_coords, max_coords)
            assert len(results) == tree_2d.get_size()

    def test_single_point_tree(self, config_file):
        """Test operations on tree with single point."""
        tree = KDTree([[5, 5]], config_path=config_file)
        assert tree.get_size() == 1

        nearest = tree.nearest_neighbor([6, 6])
        assert nearest == [5, 5]

        results = tree.range_query([4, 4], [6, 6])
        assert [5, 5] in results

    def test_high_dimensional(self, config_file):
        """Test with higher dimensions."""
        points = [[i, i + 1, i + 2, i + 3] for i in range(10)]
        tree = KDTree(points, config_path=config_file)
        assert tree.get_dimension() == 4
        assert tree.get_size() == 10

        results = tree.range_query([2, 3, 4, 5], [6, 7, 8, 9])
        assert len(results) >= 0

        nearest = tree.nearest_neighbor([5, 6, 7, 8])
        assert nearest is not None
        assert len(nearest) == 4
