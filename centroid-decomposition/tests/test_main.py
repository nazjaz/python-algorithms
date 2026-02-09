"""Unit tests for centroid decomposition module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import CentroidDecomposition, TreeNode, build_tree_from_edges


class TestTreeNode:
    """Test cases for TreeNode class."""

    def test_tree_node_creation(self):
        """Test TreeNode creation."""
        node = TreeNode(5, data=10.0)
        assert node.value == 5
        assert node.data == 10.0
        assert len(node.neighbors) == 0
        assert node.parent is None

    def test_add_neighbor(self):
        """Test adding neighbor node."""
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        node1.add_neighbor(node2)

        assert node2 in node1.neighbors
        assert node1 in node2.neighbors

    def test_tree_node_repr(self):
        """Test TreeNode string representation."""
        node = TreeNode(42, data=3.14)
        assert "TreeNode" in repr(node)
        assert "42" in repr(node)


class TestCentroidDecomposition:
    """Test cases for CentroidDecomposition class."""

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
    def simple_tree(self):
        """Create simple tree for testing."""
        root = TreeNode(0, data=1.0)
        node1 = TreeNode(1, data=2.0)
        node2 = TreeNode(2, data=3.0)
        root.add_neighbor(node1)
        root.add_neighbor(node2)
        return root, node1, node2

    @pytest.fixture
    def complex_tree(self):
        """Create complex tree for testing."""
        root = TreeNode(0, data=1.0)
        node1 = TreeNode(1, data=2.0)
        node2 = TreeNode(2, data=3.0)
        node3 = TreeNode(3, data=4.0)
        node4 = TreeNode(4, data=5.0)
        node5 = TreeNode(5, data=6.0)
        node6 = TreeNode(6, data=7.0)

        root.add_neighbor(node1)
        root.add_neighbor(node2)
        node1.add_neighbor(node3)
        node1.add_neighbor(node4)
        node2.add_neighbor(node5)
        node2.add_neighbor(node6)

        return root, node1, node2, node3, node4, node5, node6

    def test_cd_creation(self, simple_tree, config_file):
        """Test CentroidDecomposition creation."""
        root, _, _ = simple_tree
        cd = CentroidDecomposition(root, config_path=config_file)

        assert cd.root == root
        assert cd.n > 0
        assert cd.decomposed is False

    def test_decompose_simple(self, simple_tree, config_file):
        """Test decomposition on simple tree."""
        root, _, _ = simple_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        assert cd.decomposed is True
        assert cd.centroid_tree_root is not None

    def test_decompose_complex(self, complex_tree, config_file):
        """Test decomposition on complex tree."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        assert cd.decomposed is True
        assert cd.centroid_tree_root is not None

    def test_get_centroid_tree_root(self, complex_tree, config_file):
        """Test getting centroid tree root."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        centroid_root = cd.get_centroid_tree_root()
        assert centroid_root is not None

    def test_get_centroid_parent(self, complex_tree, config_file):
        """Test getting centroid parent."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        centroid_root = cd.get_centroid_tree_root()
        if centroid_root:
            parent = cd.get_centroid_parent(centroid_root)
            assert parent is None

    def test_count_paths_with_condition(self, complex_tree, config_file):
        """Test counting paths with condition."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        count = cd.count_paths_with_condition(lambda d: d <= 2)
        assert count >= 0

    def test_solve_with_divide_conquer(self, complex_tree, config_file):
        """Test solving with divide and conquer."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        def problem_solver(centroid, distances):
            return sum(1 for _, d in distances if d <= 2)

        result = cd.solve_with_divide_conquer(problem_solver)
        assert result >= 0

    def test_solve_without_decomposition(self, complex_tree, config_file):
        """Test solving without decomposition raises error."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)

        def problem_solver(centroid, distances):
            return 0.0

        with pytest.raises(ValueError):
            cd.solve_with_divide_conquer(problem_solver)

    def test_count_paths_without_decomposition(self, complex_tree, config_file):
        """Test counting paths without decomposition raises error."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)

        with pytest.raises(ValueError):
            cd.count_paths_with_condition(lambda d: d <= 2)

    def test_double_decomposition(self, complex_tree, config_file):
        """Test decomposing twice."""
        root, _, _, _, _, _, _ = complex_tree
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()
        cd.decompose()

        assert cd.decomposed is True

    def test_single_node_tree(self, config_file):
        """Test decomposition on single node tree."""
        root = TreeNode(0)
        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        assert cd.decomposed is True
        assert cd.centroid_tree_root is not None

    def test_linear_tree(self, config_file):
        """Test decomposition on linear tree."""
        root = TreeNode(0)
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        node3 = TreeNode(3)

        root.add_neighbor(node1)
        node1.add_neighbor(node2)
        node2.add_neighbor(node3)

        cd = CentroidDecomposition(root, config_path=config_file)
        cd.decompose()

        assert cd.decomposed is True
        assert cd.centroid_tree_root is not None


class TestBuildTreeFromEdges:
    """Test cases for build_tree_from_edges function."""

    def test_build_simple_tree(self):
        """Test building simple tree."""
        n = 3
        edges = [(0, 1), (0, 2)]
        root = build_tree_from_edges(n, edges, 0)

        assert root.value == 0
        assert len(root.neighbors) == 2

    def test_build_complex_tree(self):
        """Test building complex tree."""
        n = 7
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        root = build_tree_from_edges(n, edges, 0)

        assert root.value == 0
        assert len(root.neighbors) == 2

    def test_build_tree_invalid_edge(self):
        """Test building tree with invalid edge."""
        n = 3
        edges = [(0, 1), (0, 10)]
        with pytest.raises(ValueError):
            build_tree_from_edges(n, edges, 0)

    def test_build_tree_invalid_root(self):
        """Test building tree with invalid root."""
        n = 3
        edges = [(0, 1), (0, 2)]
        with pytest.raises(ValueError):
            build_tree_from_edges(n, edges, 10)
