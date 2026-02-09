"""Unit tests for link-cut tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import LinkCutNode, LinkCutTree


class TestLinkCutNode:
    """Test cases for LinkCutNode class."""

    def test_node_creation(self):
        """Test LinkCutNode creation."""
        node = LinkCutNode(5, data=10.0)
        assert node.value == 5
        assert node.data == 10.0
        assert node.path_parent is None
        assert node.left is None
        assert node.right is None
        assert node.parent is None
        assert node.reversed is False

    def test_is_root(self):
        """Test is_root method."""
        node = LinkCutNode(1)
        assert node.is_root() is True

        parent = LinkCutNode(2)
        node.parent = parent
        assert node.is_root() is False

    def test_node_repr(self):
        """Test LinkCutNode string representation."""
        node = LinkCutNode(42, data=3.14)
        assert "LinkCutNode" in repr(node)
        assert "42" in repr(node)


class TestLinkCutTree:
    """Test cases for LinkCutTree class."""

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
        """Create LinkCutTree instance."""
        return LinkCutTree(config_path=config_file)

    @pytest.fixture
    def nodes(self, tree):
        """Create nodes for testing."""
        return [tree.create_node(i, data=float(i)) for i in range(7)]

    def test_tree_creation(self, tree):
        """Test LinkCutTree creation."""
        assert len(tree.nodes) == 0

    def test_create_node(self, tree):
        """Test creating node."""
        node = tree.create_node(5, data=10.0)
        assert node.value == 5
        assert node.data == 10.0
        assert node in tree.nodes

    def test_find_root_single_node(self, tree, nodes):
        """Test finding root of single node."""
        root = tree.find_root(nodes[0])
        assert root == nodes[0]

    def test_find_root_after_link(self, tree, nodes):
        """Test finding root after linking."""
        tree.link(nodes[1], nodes[0])
        root1 = tree.find_root(nodes[0])
        root2 = tree.find_root(nodes[1])
        assert root1 == root2

    def test_link_operation(self, tree, nodes):
        """Test link operation."""
        result = tree.link(nodes[1], nodes[0])
        assert result is True

        root1 = tree.find_root(nodes[0])
        root2 = tree.find_root(nodes[1])
        assert root1 == root2

    def test_link_already_connected(self, tree, nodes):
        """Test linking already connected nodes."""
        tree.link(nodes[1], nodes[0])
        result = tree.link(nodes[0], nodes[1])
        assert result is False

    def test_cut_operation(self, tree, nodes):
        """Test cut operation."""
        tree.link(nodes[1], nodes[0])
        result = tree.cut(nodes[1])
        assert result is True

        root1 = tree.find_root(nodes[0])
        root2 = tree.find_root(nodes[1])
        assert root1 != root2

    def test_cut_root_node(self, tree, nodes):
        """Test cutting root node."""
        result = tree.cut(nodes[0])
        assert result is False

    def test_are_connected(self, tree, nodes):
        """Test connectivity check."""
        assert tree.are_connected(nodes[0], nodes[1]) is False

        tree.link(nodes[1], nodes[0])
        assert tree.are_connected(nodes[0], nodes[1]) is True

        tree.cut(nodes[1])
        assert tree.are_connected(nodes[0], nodes[1]) is False

    def test_path_query_single_node(self, tree, nodes):
        """Test path query on single node."""
        result = tree.path_query(nodes[0], nodes[0])
        assert result == nodes[0].data

    def test_path_query_connected(self, tree, nodes):
        """Test path query on connected nodes."""
        tree.link(nodes[1], nodes[0])
        result = tree.path_query(nodes[0], nodes[1])
        assert result >= 0.0

    def test_path_query_not_connected(self, tree, nodes):
        """Test path query on disconnected nodes."""
        result = tree.path_query(nodes[0], nodes[1])
        assert result == 0.0

    def test_path_update_connected(self, tree, nodes):
        """Test path update on connected nodes."""
        tree.link(nodes[1], nodes[0])
        initial = tree.path_query(nodes[0], nodes[1])
        tree.path_update(nodes[0], nodes[1], 10.0)
        updated = tree.path_query(nodes[0], nodes[1])
        assert updated > initial

    def test_path_update_not_connected(self, tree, nodes):
        """Test path update on disconnected nodes."""
        tree.path_update(nodes[0], nodes[1], 10.0)
        result = tree.path_query(nodes[0], nodes[1])
        assert result == 0.0

    def test_get_path_nodes(self, tree, nodes):
        """Test getting path nodes."""
        tree.link(nodes[1], nodes[0])
        path = tree.get_path_nodes(nodes[0], nodes[1])
        assert len(path) > 0
        assert nodes[0] in path
        assert nodes[1] in path

    def test_complex_operations(self, tree, nodes):
        """Test complex sequence of operations."""
        tree.link(nodes[1], nodes[0])
        tree.link(nodes[2], nodes[0])
        tree.link(nodes[3], nodes[1])
        tree.link(nodes[4], nodes[1])

        assert tree.are_connected(nodes[3], nodes[4]) is True
        assert tree.are_connected(nodes[3], nodes[2]) is True

        tree.cut(nodes[1])
        assert tree.are_connected(nodes[3], nodes[0]) is False
        assert tree.are_connected(nodes[3], nodes[4]) is True

    def test_multiple_trees(self, tree, nodes):
        """Test maintaining multiple trees."""
        tree.link(nodes[1], nodes[0])
        tree.link(nodes[2], nodes[0])
        tree.link(nodes[4], nodes[3])
        tree.link(nodes[5], nodes[3])

        assert tree.are_connected(nodes[0], nodes[1]) is True
        assert tree.are_connected(nodes[3], nodes[4]) is True
        assert tree.are_connected(nodes[0], nodes[3]) is False

        tree.link(nodes[0], nodes[3])
        assert tree.are_connected(nodes[0], nodes[3]) is True

    def test_find_root_after_cut(self, tree, nodes):
        """Test finding root after cut."""
        tree.link(nodes[1], nodes[0])
        tree.link(nodes[2], nodes[0])

        root_before = tree.find_root(nodes[2])
        tree.cut(nodes[1])
        root_after = tree.find_root(nodes[2])

        assert root_before == root_after

    def test_path_query_after_updates(self, tree, nodes):
        """Test path query after multiple updates."""
        tree.link(nodes[1], nodes[0])
        tree.path_update(nodes[0], nodes[1], 5.0)
        tree.path_update(nodes[0], nodes[1], 3.0)

        result = tree.path_query(nodes[0], nodes[1])
        assert result >= 8.0
