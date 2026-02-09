"""Unit tests for splay tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import SplayNode, SplayTree


class TestSplayNode:
    """Test cases for SplayNode class."""

    def test_splay_node_creation(self):
        """Test SplayNode creation."""
        node = SplayNode(10)
        assert node.key == 10
        assert node.left is None
        assert node.right is None
        assert node.parent is None

    def test_splay_node_repr(self):
        """Test SplayNode string representation."""
        node = SplayNode(42)
        assert "SplayNode" in repr(node)
        assert "42" in repr(node)


class TestSplayTree:
    """Test cases for SplayTree class."""

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
        """Create SplayTree instance."""
        return SplayTree(config_path=config_file)

    def test_tree_creation(self, tree):
        """Test SplayTree creation."""
        assert tree.size() == 0
        assert tree.is_empty() is True
        assert tree.root is None

    def test_insert_single_key(self, tree):
        """Test inserting single key."""
        result = tree.insert(10)
        assert result is True
        assert tree.size() == 1
        assert tree.is_empty() is False
        assert tree.root is not None
        assert tree.root.key == 10

    def test_insert_multiple_keys(self, tree):
        """Test inserting multiple keys."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            result = tree.insert(key)
            assert result is True
        assert tree.size() == len(keys)

    def test_insert_duplicate(self, tree):
        """Test inserting duplicate key."""
        tree.insert(10)
        result = tree.insert(10)
        assert result is False
        assert tree.size() == 1

    def test_search_existing(self, tree):
        """Test searching for existing key."""
        tree.insert(10)
        tree.insert(20)
        result = tree.search(10)
        assert result is not None
        assert result.key == 10
        assert tree.root.key == 10

    def test_search_nonexistent(self, tree):
        """Test searching for nonexistent key."""
        tree.insert(10)
        result = tree.search(20)
        assert result is None

    def test_search_empty(self, tree):
        """Test searching in empty tree."""
        result = tree.search(10)
        assert result is None

    def test_delete_existing(self, tree):
        """Test deleting existing key."""
        tree.insert(10)
        tree.insert(20)
        result = tree.delete(10)
        assert result is True
        assert tree.size() == 1
        assert tree.search(10) is None

    def test_delete_nonexistent(self, tree):
        """Test deleting nonexistent key."""
        tree.insert(10)
        result = tree.delete(20)
        assert result is False
        assert tree.size() == 1

    def test_delete_empty(self, tree):
        """Test deleting from empty tree."""
        result = tree.delete(10)
        assert result is False

    def test_inorder_traversal(self, tree):
        """Test inorder traversal."""
        keys = [30, 10, 50, 20, 40]
        for key in keys:
            tree.insert(key)
        traversal = tree.inorder_traversal()
        assert traversal == sorted(keys)

    def test_preorder_traversal(self, tree):
        """Test preorder traversal."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)
        preorder = tree.preorder_traversal()
        assert len(preorder) == 3
        assert set(preorder) == {10, 20, 5}

    def test_postorder_traversal(self, tree):
        """Test postorder traversal."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)
        postorder = tree.postorder_traversal()
        assert len(postorder) == 3
        assert set(postorder) == {10, 20, 5}

    def test_find_min(self, tree):
        """Test finding minimum key."""
        assert tree.find_min() is None
        tree.insert(30)
        tree.insert(10)
        tree.insert(20)
        assert tree.find_min() == 10
        assert tree.root.key == 10

    def test_find_max(self, tree):
        """Test finding maximum key."""
        assert tree.find_max() is None
        tree.insert(10)
        tree.insert(30)
        tree.insert(20)
        assert tree.find_max() == 30
        assert tree.root.key == 30

    def test_amortized_analysis(self, tree):
        """Test amortized analysis tracking."""
        for i in range(10):
            tree.insert(i)
            tree.search(i)

        analysis = tree.get_amortized_analysis()
        assert analysis["total_operations"] > 0
        assert analysis["total_splay_operations"] > 0
        assert analysis["total_rotations"] >= 0
        assert "average_rotations_per_splay" in analysis
        assert "amortized_cost_per_operation" in analysis

    def test_reset_statistics(self, tree):
        """Test resetting statistics."""
        tree.insert(10)
        tree.search(10)
        tree.reset_statistics()
        analysis = tree.get_amortized_analysis()
        assert analysis["total_operations"] == 0
        assert analysis["total_splay_operations"] == 0
        assert analysis["total_rotations"] == 0

    def test_large_insertions(self, config_file):
        """Test with large number of insertions."""
        tree = SplayTree(config_path=config_file)
        for i in range(100):
            tree.insert(i)
        assert tree.size() == 100
        traversal = tree.inorder_traversal()
        assert traversal == list(range(100))

    def test_sequential_operations(self, tree):
        """Test sequential insert and delete operations."""
        for i in range(20):
            tree.insert(i)
        assert tree.size() == 20

        for i in range(0, 20, 2):
            tree.delete(i)
        assert tree.size() == 10

        for i in range(1, 20, 2):
            result = tree.search(i)
            assert result is not None
            assert result.key == i

    def test_sorted_order(self, tree):
        """Test that keys remain in sorted order after operations."""
        keys = [50, 10, 30, 20, 40, 5, 15, 25, 35, 45]
        for key in keys:
            tree.insert(key)

        traversal = tree.inorder_traversal()
        assert traversal == sorted(keys)

    def test_search_after_deletion(self, tree):
        """Test search after deletion."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)

        tree.delete(20)
        assert tree.search(20) is None

        assert tree.search(10) is not None
        assert tree.search(30) is not None

    def test_splay_operation(self, tree):
        """Test that splay operation moves accessed node to root."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        tree.insert(40)

        original_root = tree.root.key
        tree.search(10)
        assert tree.root.key == 10

        tree.search(40)
        assert tree.root.key == 40

    def test_delete_root_node(self, tree):
        """Test deleting root node."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)

        root_key = tree.root.key
        tree.delete(root_key)
        assert tree.search(root_key) is None
        assert tree.size() == 2

    def test_delete_leaf_node(self, tree):
        """Test deleting leaf node."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)

        tree.delete(5)
        assert tree.search(5) is None
        assert tree.size() == 2

    def test_delete_node_with_one_child(self, tree):
        """Test deleting node with one child."""
        tree.insert(10)
        tree.insert(20)
        tree.insert(5)
        tree.insert(15)

        tree.delete(20)
        assert tree.search(20) is None
        assert tree.size() == 3

    def test_multiple_operations_amortized(self, tree):
        """Test amortized analysis with multiple operations."""
        for i in range(50):
            tree.insert(i)
            if i % 2 == 0:
                tree.search(i)

        analysis = tree.get_amortized_analysis()
        assert analysis["total_operations"] == 75
        assert analysis["total_splay_operations"] > 0

    def test_empty_tree_operations(self, tree):
        """Test operations on empty tree."""
        assert tree.find_min() is None
        assert tree.find_max() is None
        assert tree.inorder_traversal() == []
        assert tree.preorder_traversal() == []
        assert tree.postorder_traversal() == []
        assert tree.delete(10) is False
        assert tree.search(10) is None
