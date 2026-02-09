"""Unit tests for B-tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BTree, BTreeNode


class TestBTreeNode:
    """Test cases for BTreeNode class."""

    def test_b_tree_node_creation_leaf(self):
        """Test BTreeNode creation as leaf."""
        node = BTreeNode(is_leaf=True)
        assert node.is_leaf is True
        assert len(node.keys) == 0
        assert len(node.children) == 0
        assert node.parent is None

    def test_b_tree_node_creation_internal(self):
        """Test BTreeNode creation as internal node."""
        node = BTreeNode(is_leaf=False)
        assert node.is_leaf is False
        assert len(node.keys) == 0
        assert len(node.children) == 0

    def test_is_full(self):
        """Test is_full method."""
        node = BTreeNode(is_leaf=True)
        min_degree = 3
        for i in range(2 * min_degree - 1):
            node.keys.append(i)
        assert node.is_full(min_degree) is True

        node.keys.pop()
        assert node.is_full(min_degree) is False

    def test_is_underfull(self):
        """Test is_underfull method."""
        node = BTreeNode(is_leaf=True)
        min_degree = 3
        assert node.is_underfull(min_degree) is True

        for i in range(min_degree - 1):
            node.keys.append(i)
        assert node.is_underfull(min_degree) is False


class TestBTree:
    """Test cases for BTree class."""

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
        """Create BTree instance."""
        return BTree(min_degree=3, config_path=config_file)

    def test_b_tree_creation(self, tree):
        """Test BTree creation."""
        assert tree.min_degree == 3
        assert tree.root is None
        assert tree.get_size() == 0

    def test_b_tree_invalid_min_degree(self):
        """Test BTree creation with invalid min_degree."""
        with pytest.raises(ValueError):
            BTree(min_degree=1)

    def test_insert_single_key(self, tree):
        """Test inserting single key."""
        result = tree.insert(10)
        assert result is True
        assert tree.search(10)[0] is not None
        assert tree.get_size() == 1
        assert tree.get_height() == 1

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
        assert tree.get_size() == 1

    def test_search_existing(self, tree):
        """Test searching for existing key."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        node, index = tree.search(20)
        assert node is not None
        assert index is not None
        assert node.keys[index] == 20

    def test_search_nonexistent(self, tree):
        """Test searching for nonexistent key."""
        tree.insert(10)
        node, index = tree.search(20)
        assert node is None
        assert index is None

    def test_search_empty_tree(self, tree):
        """Test searching in empty tree."""
        node, index = tree.search(10)
        assert node is None
        assert index is None

    def test_delete_existing(self, tree):
        """Test deleting existing key."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        result = tree.delete(20)
        assert result is True
        node, index = tree.search(20)
        assert node is None
        assert tree.is_valid() is True

    def test_delete_nonexistent(self, tree):
        """Test deleting nonexistent key."""
        tree.insert(10)
        result = tree.delete(20)
        assert result is False
        assert tree.search(10)[0] is not None

    def test_delete_root(self, tree):
        """Test deleting root node."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        result = tree.delete(10)
        assert result is True
        assert tree.search(10)[0] is None
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
        assert tree.root is None

    def test_inorder_traversal(self, tree):
        """Test inorder traversal."""
        keys = [10, 5, 15, 3, 7, 12, 18]
        for key in keys:
            tree.insert(key)
        inorder = tree.inorder_traversal()
        assert inorder == sorted(keys)

    def test_get_height(self, tree):
        """Test height calculation."""
        assert tree.get_height() == 0
        tree.insert(10)
        assert tree.get_height() == 1
        tree.insert(5)
        tree.insert(15)
        height = tree.get_height()
        assert height >= 1

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

    def test_split_operation(self, tree):
        """Test that split occurs when node is full."""
        min_degree = tree.min_degree
        max_keys = 2 * min_degree - 1

        for i in range(max_keys + 1):
            tree.insert(i * 10)

        assert tree.is_valid() is True
        assert tree.get_size() == max_keys + 1

    def test_merge_operation(self, tree):
        """Test that merge occurs during deletion."""
        keys = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]
        for key in keys:
            tree.insert(key)

        initial_size = tree.get_size()
        tree.delete(5)
        assert tree.get_size() == initial_size - 1
        assert tree.is_valid() is True

    def test_disk_io_stats(self, tree):
        """Test disk I/O statistics tracking."""
        stats = tree.get_disk_io_stats()
        assert "disk_reads" in stats
        assert "disk_writes" in stats

        tree.insert(10)
        tree.insert(20)
        tree.search(10)

        stats = tree.get_disk_io_stats()
        assert stats["disk_reads"] > 0
        assert stats["disk_writes"] > 0

    def test_reset_disk_io_stats(self, tree):
        """Test resetting disk I/O statistics."""
        tree.insert(10)
        tree.insert(20)

        stats_before = tree.get_disk_io_stats()
        assert stats_before["disk_reads"] > 0

        tree.reset_disk_io_stats()
        stats_after = tree.get_disk_io_stats()
        assert stats_after["disk_reads"] == 0
        assert stats_after["disk_writes"] == 0

    def test_different_min_degrees(self):
        """Test B-tree with different minimum degrees."""
        for min_degree in [2, 3, 4, 5]:
            tree = BTree(min_degree=min_degree)
            keys = list(range(1, 21))
            for key in keys:
                tree.insert(key)
            assert tree.is_valid() is True
            assert tree.get_size() == len(keys)

    def test_delete_from_leaf(self, tree):
        """Test deletion from leaf node."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            tree.insert(key)

        tree.delete(50)
        assert tree.search(50)[0] is None
        assert tree.is_valid() is True

    def test_delete_from_internal_node(self, tree):
        """Test deletion from internal node."""
        keys = [10, 20, 30, 40, 50, 5, 15, 25, 35, 45]
        for key in keys:
            tree.insert(key)

        tree.delete(30)
        assert tree.search(30)[0] is None
        assert tree.is_valid() is True

    def test_inorder_traversal_large(self, tree):
        """Test inorder traversal on large tree."""
        keys = list(range(1, 51))
        for key in keys:
            tree.insert(key)

        inorder = tree.inorder_traversal()
        assert inorder == sorted(keys)
        assert len(inorder) == len(keys)
