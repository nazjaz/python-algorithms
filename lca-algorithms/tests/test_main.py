"""Unit tests for LCA algorithms module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import (
    LCABinaryLifting,
    LCAEulerTour,
    TreeNode,
    build_tree_from_edges,
)


class TestTreeNode:
    """Test cases for TreeNode class."""

    def test_tree_node_creation(self):
        """Test TreeNode creation."""
        node = TreeNode(5)
        assert node.value == 5
        assert len(node.children) == 0
        assert node.parent is None

    def test_add_child(self):
        """Test adding child node."""
        parent = TreeNode(1)
        child = TreeNode(2)
        parent.add_child(child)

        assert len(parent.children) == 1
        assert child in parent.children
        assert child.parent == parent

    def test_tree_node_repr(self):
        """Test TreeNode string representation."""
        node = TreeNode(42)
        assert "TreeNode" in repr(node)
        assert "42" in repr(node)


class TestLCABinaryLifting:
    """Test cases for LCABinaryLifting class."""

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
        root = TreeNode(0)
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        root.add_child(node1)
        root.add_child(node2)
        return root, node1, node2

    @pytest.fixture
    def complex_tree(self):
        """Create complex tree for testing."""
        root = TreeNode(0)
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        node3 = TreeNode(3)
        node4 = TreeNode(4)
        node5 = TreeNode(5)
        node6 = TreeNode(6)

        root.add_child(node1)
        root.add_child(node2)
        node1.add_child(node3)
        node1.add_child(node4)
        node2.add_child(node5)
        node2.add_child(node6)

        return root, node1, node2, node3, node4, node5, node6

    def test_lca_simple_tree(self, simple_tree, config_file):
        """Test LCA on simple tree."""
        root, node1, node2 = simple_tree
        lca = LCABinaryLifting(root, config_path=config_file)

        result = lca.lca(node1, node2)
        assert result is not None
        assert result.value == 0

    def test_lca_complex_tree(self, complex_tree, config_file):
        """Test LCA on complex tree."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        lca = LCABinaryLifting(root, config_path=config_file)

        result = lca.lca(node3, node4)
        assert result is not None
        assert result.value == 1

        result = lca.lca(node3, node5)
        assert result is not None
        assert result.value == 0

        result = lca.lca(node5, node6)
        assert result is not None
        assert result.value == 2

    def test_lca_same_node(self, complex_tree, config_file):
        """Test LCA of node with itself."""
        root, _, _, node3, _, _, _ = complex_tree
        lca = LCABinaryLifting(root, config_path=config_file)

        result = lca.lca(node3, node3)
        assert result is not None
        assert result.value == 3

    def test_lca_parent_child(self, complex_tree, config_file):
        """Test LCA of parent and child."""
        root, node1, _, node3, _, _, _ = complex_tree
        lca = LCABinaryLifting(root, config_path=config_file)

        result = lca.lca(node1, node3)
        assert result is not None
        assert result.value == 1

    def test_lca_root(self, complex_tree, config_file):
        """Test LCA involving root."""
        root, _, _, node3, _, node5, _ = complex_tree
        lca = LCABinaryLifting(root, config_path=config_file)

        result = lca.lca(root, node3)
        assert result is not None
        assert result.value == 0

        result = lca.lca(node3, root)
        assert result is not None
        assert result.value == 0

    def test_lca_invalid_nodes(self, complex_tree, config_file):
        """Test LCA with invalid nodes."""
        root, _, _, _, _, _, _ = complex_tree
        lca = LCABinaryLifting(root, config_path=config_file)

        invalid_node = TreeNode(99)
        result = lca.lca(invalid_node, root)
        assert result is None


class TestLCAEulerTour:
    """Test cases for LCAEulerTour class."""

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
        root = TreeNode(0)
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        root.add_child(node1)
        root.add_child(node2)
        return root, node1, node2

    @pytest.fixture
    def complex_tree(self):
        """Create complex tree for testing."""
        root = TreeNode(0)
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        node3 = TreeNode(3)
        node4 = TreeNode(4)
        node5 = TreeNode(5)
        node6 = TreeNode(6)

        root.add_child(node1)
        root.add_child(node2)
        node1.add_child(node3)
        node1.add_child(node4)
        node2.add_child(node5)
        node2.add_child(node6)

        return root, node1, node2, node3, node4, node5, node6

    def test_lca_simple_tree(self, simple_tree, config_file):
        """Test LCA on simple tree."""
        root, node1, node2 = simple_tree
        lca = LCAEulerTour(root, config_path=config_file)

        result = lca.lca(node1, node2)
        assert result is not None
        assert result.value == 0

    def test_lca_complex_tree(self, complex_tree, config_file):
        """Test LCA on complex tree."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        lca = LCAEulerTour(root, config_path=config_file)

        result = lca.lca(node3, node4)
        assert result is not None
        assert result.value == 1

        result = lca.lca(node3, node5)
        assert result is not None
        assert result.value == 0

        result = lca.lca(node5, node6)
        assert result is not None
        assert result.value == 2

    def test_lca_same_node(self, complex_tree, config_file):
        """Test LCA of node with itself."""
        root, _, _, node3, _, _, _ = complex_tree
        lca = LCAEulerTour(root, config_path=config_file)

        result = lca.lca(node3, node3)
        assert result is not None
        assert result.value == 3

    def test_lca_parent_child(self, complex_tree, config_file):
        """Test LCA of parent and child."""
        root, node1, _, node3, _, _, _ = complex_tree
        lca = LCAEulerTour(root, config_path=config_file)

        result = lca.lca(node1, node3)
        assert result is not None
        assert result.value == 1

    def test_lca_root(self, complex_tree, config_file):
        """Test LCA involving root."""
        root, _, _, node3, _, node5, _ = complex_tree
        lca = LCAEulerTour(root, config_path=config_file)

        result = lca.lca(root, node3)
        assert result is not None
        assert result.value == 0

        result = lca.lca(node3, root)
        assert result is not None
        assert result.value == 0

    def test_lca_invalid_nodes(self, complex_tree, config_file):
        """Test LCA with invalid nodes."""
        root, _, _, _, _, _, _ = complex_tree
        lca = LCAEulerTour(root, config_path=config_file)

        invalid_node = TreeNode(99)
        result = lca.lca(invalid_node, root)
        assert result is None


class TestBuildTreeFromEdges:
    """Test cases for build_tree_from_edges function."""

    def test_build_simple_tree(self):
        """Test building simple tree."""
        n = 3
        edges = [(0, 1), (0, 2)]
        root = build_tree_from_edges(n, edges, 0)

        assert root.value == 0
        assert len(root.children) == 2
        assert root.children[0].value == 1
        assert root.children[1].value == 2

    def test_build_complex_tree(self):
        """Test building complex tree."""
        n = 7
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
        root = build_tree_from_edges(n, edges, 0)

        assert root.value == 0
        assert len(root.children) == 2
        assert root.children[0].value == 1
        assert root.children[1].value == 2

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


class TestComparison:
    """Test cases comparing both LCA algorithms."""

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
    def test_tree(self):
        """Create test tree."""
        root = TreeNode(0)
        node1 = TreeNode(1)
        node2 = TreeNode(2)
        node3 = TreeNode(3)
        node4 = TreeNode(4)
        node5 = TreeNode(5)
        node6 = TreeNode(6)

        root.add_child(node1)
        root.add_child(node2)
        node1.add_child(node3)
        node1.add_child(node4)
        node2.add_child(node5)
        node2.add_child(node6)

        return root, node1, node2, node3, node4, node5, node6

    def test_same_results(self, test_tree, config_file):
        """Test that both algorithms give same results."""
        root, node1, node2, node3, node4, node5, node6 = test_tree

        lca_bl = LCABinaryLifting(root, config_path=config_file)
        lca_et = LCAEulerTour(root, config_path=config_file)

        test_cases = [
            (node3, node4),
            (node3, node5),
            (node5, node6),
            (node1, node3),
            (root, node3),
            (node3, node3),
        ]

        for u, v in test_cases:
            result_bl = lca_bl.lca(u, v)
            result_et = lca_et.lca(u, v)
            assert result_bl is not None
            assert result_et is not None
            assert result_bl.value == result_et.value

    def test_large_tree(self, config_file):
        """Test with larger tree."""
        root = TreeNode(0)
        nodes = [root]

        for i in range(1, 20):
            parent_idx = (i - 1) // 2
            node = TreeNode(i)
            nodes[parent_idx].add_child(node)
            nodes.append(node)

        lca_bl = LCABinaryLifting(root, config_path=config_file)
        lca_et = LCAEulerTour(root, config_path=config_file)

        result_bl = lca_bl.lca(nodes[10], nodes[15])
        result_et = lca_et.lca(nodes[10], nodes[15])

        assert result_bl is not None
        assert result_et is not None
        assert result_bl.value == result_et.value
