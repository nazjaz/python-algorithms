"""Unit tests for binary tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import TreeNode, BinaryTree


class TestTreeNode:
    """Test cases for TreeNode class."""

    def test_node_initialization(self):
        """Test node initialization."""
        node = TreeNode(10)
        assert node.value == 10
        assert node.left is None
        assert node.right is None

    def test_node_repr(self):
        """Test node string representation."""
        node = TreeNode(5)
        assert "TreeNode" in repr(node)
        assert "5" in repr(node)


class TestBinaryTree:
    """Test cases for BinaryTree class."""

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
        """Create BinaryTree instance."""
        return BinaryTree(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        tree = BinaryTree(config_path=str(config_path))
        assert tree.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            BinaryTree(config_path="nonexistent.yaml")

    def test_tree_initialization(self, tree):
        """Test tree initialization."""
        assert tree.root is None

    def test_insert_single_value(self, tree):
        """Test inserting single value."""
        tree.insert(10)
        assert tree.root is not None
        assert tree.root.value == 10

    def test_insert_multiple_values(self, tree):
        """Test inserting multiple values."""
        values = [10, 5, 15]
        for value in values:
            tree.insert(value)

        assert tree.root is not None
        assert tree.root.value == 10
        assert tree.root.left is not None
        assert tree.root.left.value == 5
        assert tree.root.right is not None
        assert tree.root.right.value == 15

    def test_insert_empty_tree(self, tree):
        """Test inserting into empty tree."""
        tree.insert(10)
        assert tree.root.value == 10

    def test_search_found(self, tree):
        """Test searching for existing value."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        assert tree.search(10) is True
        assert tree.search(5) is True
        assert tree.search(15) is True

    def test_search_not_found(self, tree):
        """Test searching for non-existent value."""
        tree.insert(10)
        assert tree.search(20) is False

    def test_search_empty_tree(self, tree):
        """Test searching in empty tree."""
        assert tree.search(10) is False

    def test_delete_existing_value(self, tree):
        """Test deleting existing value."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        result = tree.delete(5)
        assert result is True
        assert tree.search(5) is False

    def test_delete_non_existing_value(self, tree):
        """Test deleting non-existent value."""
        tree.insert(10)
        result = tree.delete(20)
        assert result is False

    def test_delete_empty_tree(self, tree):
        """Test deleting from empty tree."""
        result = tree.delete(10)
        assert result is False

    def test_delete_root(self, tree):
        """Test deleting root node."""
        tree.insert(10)
        tree.insert(5)
        result = tree.delete(10)
        assert result is True
        assert tree.root is not None

    def test_inorder_traversal(self, tree):
        """Test inorder traversal."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)

        result = tree.inorder_traversal()
        # Inorder should be: 3, 5, 7, 10, 15
        assert result == [3, 5, 7, 10, 15]

    def test_inorder_empty_tree(self, tree):
        """Test inorder traversal on empty tree."""
        result = tree.inorder_traversal()
        assert result == []

    def test_preorder_traversal(self, tree):
        """Test preorder traversal."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        result = tree.preorder_traversal()
        # Preorder should be: 10, 5, 15
        assert result == [10, 5, 15]

    def test_preorder_empty_tree(self, tree):
        """Test preorder traversal on empty tree."""
        result = tree.preorder_traversal()
        assert result == []

    def test_postorder_traversal(self, tree):
        """Test postorder traversal."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        result = tree.postorder_traversal()
        # Postorder should be: 5, 15, 10
        assert result == [5, 15, 10]

    def test_postorder_empty_tree(self, tree):
        """Test postorder traversal on empty tree."""
        result = tree.postorder_traversal()
        assert result == []

    def test_level_order_traversal(self, tree):
        """Test level-order traversal."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)

        result = tree.level_order_traversal()
        # Level-order should be: 10, 5, 15, 3, 7
        assert result == [10, 5, 15, 3, 7]

    def test_level_order_empty_tree(self, tree):
        """Test level-order traversal on empty tree."""
        result = tree.level_order_traversal()
        assert result == []

    def test_height_empty_tree(self, tree):
        """Test height of empty tree."""
        assert tree.height() == -1

    def test_height_single_node(self, tree):
        """Test height of tree with single node."""
        tree.insert(10)
        assert tree.height() == 0

    def test_height_multiple_levels(self, tree):
        """Test height of tree with multiple levels."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        # Height should be 2 (10 -> 5 -> 3)
        assert tree.height() == 2

    def test_size_empty_tree(self, tree):
        """Test size of empty tree."""
        assert tree.size() == 0

    def test_size_single_node(self, tree):
        """Test size of tree with single node."""
        tree.insert(10)
        assert tree.size() == 1

    def test_size_multiple_nodes(self, tree):
        """Test size of tree with multiple nodes."""
        values = [10, 5, 15, 3, 7]
        for value in values:
            tree.insert(value)
        assert tree.size() == 5

    def test_visualize_empty_tree(self, tree):
        """Test visualization of empty tree."""
        visualization = tree.visualize()
        assert "empty" in visualization.lower()

    def test_visualize_non_empty_tree(self, tree):
        """Test visualization of non-empty tree."""
        tree.insert(10)
        tree.insert(5)
        visualization = tree.visualize()
        assert "Binary Tree" in visualization
        assert "10" in visualization

    def test_complex_tree_operations(self, tree):
        """Test complex tree operations."""
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        # Verify all values are present
        for value in values:
            assert tree.search(value) is True

        # Verify traversals
        inorder = tree.inorder_traversal()
        assert len(inorder) == len(values)

        # Delete a value
        tree.delete(5)
        assert tree.search(5) is False
        assert tree.size() == len(values) - 1

    def test_string_values(self, tree):
        """Test tree with string values."""
        tree.insert("A")
        tree.insert("B")
        tree.insert("C")

        assert tree.search("A") is True
        assert tree.search("B") is True
        assert tree.search("C") is True

        inorder = tree.inorder_traversal()
        assert "A" in inorder
        assert "B" in inorder
        assert "C" in inorder

    def test_mixed_type_values(self, tree):
        """Test tree with mixed type values."""
        tree.insert(10)
        tree.insert("hello")
        tree.insert(3.14)

        assert tree.search(10) is True
        assert tree.search("hello") is True
        assert tree.search(3.14) is True

    def test_generate_report(self, tree, temp_dir):
        """Test report generation."""
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)

        report_path = temp_dir / "report.txt"
        report = tree.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "BINARY TREE" in report
        assert "INORDER" in report
        assert "PREORDER" in report
        assert "POSTORDER" in report

    def test_delete_maintains_structure(self, tree):
        """Test that deletion maintains tree structure."""
        values = [10, 5, 15, 3, 7, 12, 18]
        for value in values:
            tree.insert(value)

        original_size = tree.size()
        tree.delete(5)
        assert tree.size() == original_size - 1

        # Tree should still be valid
        inorder = tree.inorder_traversal()
        assert len(inorder) == original_size - 1
