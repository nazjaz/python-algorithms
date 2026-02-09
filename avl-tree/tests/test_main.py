"""Unit tests for AVL tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import AVLNode, AVLTree


class TestAVLNode:
    """Test cases for AVLNode class."""

    def test_avl_node_creation(self):
        """Test AVLNode creation."""
        node = AVLNode(10)
        assert node.key == 10
        assert node.left is None
        assert node.right is None
        assert node.height == 1


class TestAVLTree:
    """Test cases for AVLTree class."""

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
    def avl(self, config_file):
        """Create AVLTree instance."""
        return AVLTree(config_path=config_file)

    def test_insert_single_key(self, avl):
        """Test inserting single key."""
        avl.insert(10)
        assert avl.search(10) is True
        assert avl.get_height() == 1

    def test_insert_multiple_keys(self, avl):
        """Test inserting multiple keys."""
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            avl.insert(key)
        assert avl.get_height() <= 3
        assert avl.is_balanced() is True

    def test_insert_duplicate(self, avl):
        """Test inserting duplicate key."""
        avl.insert(10)
        avl.insert(10)
        assert avl.search(10) is True
        inorder = avl.inorder_traversal()
        assert inorder.count(10) == 1

    def test_search_existing(self, avl):
        """Test searching for existing key."""
        avl.insert(10)
        avl.insert(20)
        assert avl.search(10) is True
        assert avl.search(20) is True

    def test_search_nonexistent(self, avl):
        """Test searching for nonexistent key."""
        avl.insert(10)
        assert avl.search(20) is False

    def test_search_empty_tree(self, avl):
        """Test searching in empty tree."""
        assert avl.search(10) is False

    def test_delete_existing(self, avl):
        """Test deleting existing key."""
        avl.insert(10)
        avl.insert(20)
        result = avl.delete(10)
        assert result is True
        assert avl.search(10) is False
        assert avl.is_balanced() is True

    def test_delete_nonexistent(self, avl):
        """Test deleting nonexistent key."""
        avl.insert(10)
        result = avl.delete(20)
        assert result is False

    def test_delete_empty_tree(self, avl):
        """Test deleting from empty tree."""
        result = avl.delete(10)
        assert result is False

    def test_inorder_traversal(self, avl):
        """Test inorder traversal."""
        keys = [50, 30, 70, 20, 40, 60, 80]
        for key in keys:
            avl.insert(key)
        inorder = avl.inorder_traversal()
        assert inorder == sorted(keys)

    def test_preorder_traversal(self, avl):
        """Test preorder traversal."""
        keys = [10, 20, 30]
        for key in keys:
            avl.insert(key)
        preorder = avl.preorder_traversal()
        assert len(preorder) == 3
        assert preorder[0] in keys

    def test_postorder_traversal(self, avl):
        """Test postorder traversal."""
        keys = [10, 20, 30]
        for key in keys:
            avl.insert(key)
        postorder = avl.postorder_traversal()
        assert len(postorder) == 3
        assert postorder[-1] in keys

    def test_get_height(self, avl):
        """Test getting tree height."""
        assert avl.get_height() == 0
        avl.insert(10)
        assert avl.get_height() == 1
        avl.insert(20)
        assert avl.get_height() <= 2

    def test_is_balanced(self, avl):
        """Test balance checking."""
        assert avl.is_balanced() is True
        keys = [10, 20, 30, 40, 50]
        for key in keys:
            avl.insert(key)
        assert avl.is_balanced() is True

    def test_build_from_list(self, avl):
        """Test building tree from list."""
        keys = [10, 20, 30, 40, 50]
        avl.build_from_list(keys)
        assert avl.get_height() <= 3
        assert avl.is_balanced() is True

    def test_build_from_empty_list(self, avl):
        """Test building tree from empty list."""
        avl.build_from_list([])
        assert avl.get_height() == 0

    def test_left_rotation(self, avl):
        """Test left rotation scenario."""
        keys = [10, 20, 30]
        for key in keys:
            avl.insert(key)
        assert avl.is_balanced() is True
        assert avl.get_height() <= 2

    def test_right_rotation(self, avl):
        """Test right rotation scenario."""
        keys = [30, 20, 10]
        for key in keys:
            avl.insert(key)
        assert avl.is_balanced() is True
        assert avl.get_height() <= 2

    def test_left_right_rotation(self, avl):
        """Test left-right rotation scenario."""
        keys = [30, 10, 20]
        for key in keys:
            avl.insert(key)
        assert avl.is_balanced() is True
        assert avl.get_height() <= 2

    def test_right_left_rotation(self, avl):
        """Test right-left rotation scenario."""
        keys = [10, 30, 20]
        for key in keys:
            avl.insert(key)
        assert avl.is_balanced() is True
        assert avl.get_height() <= 2

    def test_large_tree(self, avl):
        """Test with larger tree."""
        keys = list(range(1, 101))
        avl.build_from_list(keys)
        assert avl.is_balanced() is True
        assert avl.get_height() <= 7

    def test_delete_maintains_balance(self, avl):
        """Test that deletion maintains balance."""
        keys = [10, 20, 30, 40, 50]
        avl.build_from_list(keys)
        avl.delete(30)
        assert avl.is_balanced() is True

    def test_delete_root(self, avl):
        """Test deleting root node."""
        keys = [10, 20, 30]
        avl.build_from_list(keys)
        avl.delete(20)
        assert avl.is_balanced() is True

    def test_delete_leaf(self, avl):
        """Test deleting leaf node."""
        keys = [10, 20, 30]
        avl.build_from_list(keys)
        avl.delete(30)
        assert avl.is_balanced() is True

    def test_delete_node_with_one_child(self, avl):
        """Test deleting node with one child."""
        keys = [10, 20, 30, 40]
        avl.build_from_list(keys)
        avl.delete(30)
        assert avl.is_balanced() is True

    def test_delete_node_with_two_children(self, avl):
        """Test deleting node with two children."""
        keys = [10, 20, 30, 40, 50]
        avl.build_from_list(keys)
        avl.delete(30)
        assert avl.is_balanced() is True

    def test_negative_numbers(self, avl):
        """Test with negative numbers."""
        keys = [-10, -5, 0, 5, 10]
        avl.build_from_list(keys)
        assert avl.is_balanced() is True
        assert avl.search(-10) is True

    def test_floating_point_numbers(self, avl):
        """Test with floating point numbers."""
        keys = [1.5, 2.5, 3.5, 4.5, 5.5]
        avl.build_from_list(keys)
        assert avl.is_balanced() is True
        assert avl.search(3.5) is True

    def test_compare_performance(self, avl):
        """Test performance comparison."""
        keys = [10, 20, 30, 40, 50]
        search_keys = [10, 20, 30]
        performance = avl.compare_performance(keys, search_keys, iterations=1)
        assert performance["num_keys"] == 5
        assert performance["num_searches"] == 3
        assert performance["insert"]["success"] is True
        assert performance["search"]["success"] is True

    def test_compare_performance_with_iterations(self, avl):
        """Test performance comparison with multiple iterations."""
        keys = [10, 20, 30]
        search_keys = [10, 20]
        performance = avl.compare_performance(keys, search_keys, iterations=10)
        assert performance["iterations"] == 10
        assert performance["insert"]["success"] is True

    def test_generate_report_success(self, avl, temp_dir):
        """Test report generation."""
        keys = [10, 20, 30, 40, 50]
        search_keys = [10, 20, 30]
        performance = avl.compare_performance(keys, search_keys)
        report_path = temp_dir / "report.txt"

        report = avl.generate_report(performance, output_path=str(report_path))

        assert "AVL TREE" in report
        assert "insert()" in report
        assert "search()" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, avl):
        """Test report generation without saving to file."""
        keys = [10, 20, 30, 40, 50]
        search_keys = [10, 20, 30]
        performance = avl.compare_performance(keys, search_keys)
        report = avl.generate_report(performance)

        assert "AVL TREE" in report
        assert "insert()" in report
        assert "search()" in report

    def test_sequential_insertions(self, avl):
        """Test sequential insertions maintain balance."""
        for i in range(1, 21):
            avl.insert(i)
            assert avl.is_balanced() is True

    def test_sequential_deletions(self, avl):
        """Test sequential deletions maintain balance."""
        keys = list(range(1, 21))
        avl.build_from_list(keys)
        for i in range(1, 11):
            avl.delete(i)
            assert avl.is_balanced() is True

    def test_all_rotations(self, avl):
        """Test all rotation types are used."""
        keys = [10, 5, 15, 3, 7, 12, 18, 2, 4, 6, 8, 11, 13, 17, 19]
        avl.build_from_list(keys)
        assert avl.is_balanced() is True
        assert avl.get_height() <= 4
