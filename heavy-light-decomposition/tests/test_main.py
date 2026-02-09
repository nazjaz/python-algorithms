"""Unit tests for heavy-light decomposition module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import (
    HeavyLightDecomposition,
    TreeNode,
    build_tree_from_edges,
)


class TestTreeNode:
    """Test cases for TreeNode class."""

    def test_tree_node_creation(self):
        """Test TreeNode creation."""
        node = TreeNode(5, data=10.0)
        assert node.value == 5
        assert node.data == 10.0
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
        node = TreeNode(42, data=3.14)
        assert "TreeNode" in repr(node)
        assert "42" in repr(node)


class TestHeavyLightDecomposition:
    """Test cases for HeavyLightDecomposition class."""

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
        root.add_child(node1)
        root.add_child(node2)
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

        root.add_child(node1)
        root.add_child(node2)
        node1.add_child(node3)
        node1.add_child(node4)
        node2.add_child(node5)
        node2.add_child(node6)

        return root, node1, node2, node3, node4, node5, node6

    def test_hld_creation(self, simple_tree, config_file):
        """Test HLD creation."""
        root, _, _ = simple_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        assert hld.root == root
        assert hld.n > 0
        assert len(hld.chains) > 0

    def test_query_path_simple(self, simple_tree, config_file):
        """Test path query on simple tree."""
        root, node1, node2 = simple_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        result = hld.query_path(node1, node2)
        assert result >= 0.0

    def test_query_path_complex(self, complex_tree, config_file):
        """Test path query on complex tree."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        result = hld.query_path(node3, node4)
        assert result >= 0.0

        result = hld.query_path(node3, node5)
        assert result >= 0.0

    def test_query_path_same_node(self, complex_tree, config_file):
        """Test path query with same node."""
        root, _, _, node3, _, _, _ = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        result = hld.query_path(node3, node3)
        assert result == node3.data

    def test_update_path(self, complex_tree, config_file):
        """Test path update."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        initial = hld.query_path(node3, node5)
        hld.update_path(node3, node5, 10.0)
        updated = hld.query_path(node3, node5)

        assert updated > initial

    def test_get_lca(self, complex_tree, config_file):
        """Test LCA query."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        lca = hld.get_lca(node3, node4)
        assert lca == node1

        lca = hld.get_lca(node3, node5)
        assert lca == root

    def test_get_distance(self, complex_tree, config_file):
        """Test distance query."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        distance = hld.get_distance(node3, node4)
        assert distance == 2

        distance = hld.get_distance(node3, node5)
        assert distance == 4

    def test_query_subtree(self, complex_tree, config_file):
        """Test subtree query."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        result = hld.query_subtree(node1)
        assert result >= 0.0

        result = hld.query_subtree(root)
        assert result >= 0.0

    def test_multiple_updates(self, complex_tree, config_file):
        """Test multiple path updates."""
        root, node1, node2, node3, node4, node5, node6 = complex_tree
        hld = HeavyLightDecomposition(root, config_path=config_file)

        hld.update_path(node3, node4, 5.0)
        hld.update_path(node5, node6, 3.0)

        result1 = hld.query_path(node3, node4)
        result2 = hld.query_path(node5, node6)

        assert result1 >= 0.0
        assert result2 >= 0.0
