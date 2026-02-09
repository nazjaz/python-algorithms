"""Unit tests for red-black tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Color, RedBlackNode, RedBlackTree


class TestRedBlackNode:
    """Test cases for RedBlackNode class."""

    def test_red_black_node_creation(self):
        """Test RedBlackNode creation with default color."""
        node = RedBlackNode(10)
        assert node.key == 10
        assert node.color == Color.RED
        assert node.parent is None
        assert node.left is None
        assert node.right is None

    def test_red_black_node_creation_with_color(self):
        """Test RedBlackNode creation with specified color."""
        node = RedBlackNode(10, Color.BLACK)
        assert node.key == 10
        assert node.color == Color.BLACK

    def test_is_red(self):
        """Test is_red method."""
        red_node = RedBlackNode(10, Color.RED)
        black_node = RedBlackNode(20, Color.BLACK)
        assert red_node.is_red() is True
        assert black_node.is_red() is False

    def test_is_black(self):
        """Test is_black method."""
        red_node = RedBlackNode(10, Color.RED)
        black_node = RedBlackNode(20, Color.BLACK)
        assert red_node.is_black() is False
        assert black_node.is_black() is True


class TestRedBlackTree:
    """Test cases for RedBlackTree class."""

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
        """Create RedBlackTree instance."""
        return RedBlackTree(config_path=config_file)

    def test_insert_single_key(self, tree):
        """Test inserting single key."""
        result = tree.insert(10)
        assert result is True
        assert tree.search(10) is True
        assert tree.height() == 1
        assert tree.is_valid() is True

    def test_insert_multiple_keys(self, tree):
        """Test inserting multiple keys."""
        keys = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]
        for key in keys:
            result = tree.insert(key)
            assert result is True
        assert tree.get_size() == len(keys)
        assert tree.is_valid() is True

    def test_insert_duplicate(self, tree):
        """Test inserting duplicate key."""
        tree.insert(10)
        result = tree.insert(10)
        assert result is False
        assert tree.search(10) is True
        inorder = tree.inorder_traversal()
        assert inorder.count(10) == 1

    def test_search_existing(self, tree):
        """Test searching for existing key."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        assert tree.search(10) is True
        assert tree.search(20) is True
        assert tree.search(30) is True

    def test_search_nonexistent(self, tree):
        """Test searching for nonexistent key."""
        tree.insert(10)
        assert tree.search(20) is False
        assert tree.search(5) is False

    def test_search_empty_tree(self, tree):
        """Test searching in empty tree."""
        assert tree.search(10) is False

    def test_delete_existing(self, tree):
        """Test deleting existing key."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        result = tree.delete(20)
        assert result is True
        assert tree.search(20) is False
        assert tree.search(10) is True
        assert tree.search(30) is True
        assert tree.is_valid() is True

    def test_delete_nonexistent(self, tree):
        """Test deleting nonexistent key."""
        tree.insert(10)
        result = tree.delete(20)
        assert result is False
        assert tree.search(10) is True

    def test_delete_root(self, tree):
        """Test deleting root node."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        result = tree.delete(10)
        assert result is True
        assert tree.search(10) is False
        assert tree.is_valid() is True

    def test_delete_all_nodes(self, tree):
        """Test deleting all nodes."""
        keys = [10, 20, 30]
        for key in keys:
            tree.insert(key)
        for key in keys:
            result = tree.delete(key)
            assert result is True
        assert tree.get_size() == 0
        assert tree.is_valid() is True

    def test_inorder_traversal(self, tree):
        """Test inorder traversal."""
        keys = [10, 5, 15, 3, 7, 12, 18]
        for key in keys:
            tree.insert(key)
        inorder = tree.inorder_traversal()
        assert inorder == sorted(keys)

    def test_preorder_traversal(self, tree):
        """Test preorder traversal."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        preorder = tree.preorder_traversal()
        assert len(preorder) == 3
        assert 10 in preorder
        assert 5 in preorder
        assert 15 in preorder

    def test_postorder_traversal(self, tree):
        """Test postorder traversal."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        postorder = tree.postorder_traversal()
        assert len(postorder) == 3
        assert 10 in postorder
        assert 5 in postorder
        assert 15 in postorder

    def test_height(self, tree):
        """Test height calculation."""
        assert tree.height() == 0
        tree.insert(10)
        assert tree.height() == 1
        tree.insert(5)
        tree.insert(15)
        height = tree.height()
        assert height >= 2

    def test_get_size(self, tree):
        """Test size calculation."""
        assert tree.get_size() == 0
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)
        assert tree.get_size() == len(keys)

    def test_is_valid_empty_tree(self, tree):
        """Test validation of empty tree."""
        assert tree.is_valid() is True

    def test_is_valid_after_insertions(self, tree):
        """Test validation after insertions."""
        keys = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]
        for key in keys:
            tree.insert(key)
        assert tree.is_valid() is True

    def test_is_valid_after_deletions(self, tree):
        """Test validation after deletions."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)
        tree.delete(30)
        tree.delete(10)
        assert tree.is_valid() is True

    def test_large_tree_operations(self, tree):
        """Test operations on large tree."""
        keys = list(range(1, 101))
        for key in keys:
            tree.insert(key)
        assert tree.get_size() == 100
        assert tree.is_valid() is True

        for key in range(1, 51):
            tree.delete(key)
        assert tree.get_size() == 50
        assert tree.is_valid() is True

    def test_sequential_insert_delete(self, tree):
        """Test sequential insert and delete operations."""
        for i in range(1, 21):
            tree.insert(i)
        assert tree.is_valid() is True

        for i in range(1, 21):
            tree.delete(i)
        assert tree.is_valid() is True
        assert tree.get_size() == 0

    def test_root_is_black(self, tree):
        """Test that root is always black."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)
        assert tree.root is not None
        assert tree.root.is_black() is True

    def test_black_height_property(self, tree):
        """Test black height property."""
        keys = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]
        for key in keys:
            tree.insert(key)
        assert tree.is_valid() is True
