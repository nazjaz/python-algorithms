"""Unit tests for binary search tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BSTNode, BST, AVLTree, PerformanceAnalyzer


class TestBSTNode:
    """Test cases for BSTNode class."""

    def test_node_initialization(self):
        """Test node initialization."""
        node = BSTNode(10)
        assert node.value == 10
        assert node.left is None
        assert node.right is None
        assert node.height == 0

    def test_node_repr(self):
        """Test node string representation."""
        node = BSTNode(5)
        assert "BSTNode" in repr(node)
        assert "5" in repr(node)


class TestBST:
    """Test cases for BST class."""

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
    def bst(self, config_file):
        """Create BST instance."""
        return BST(config_path=config_file)

    def test_bst_initialization(self, bst):
        """Test BST initialization."""
        assert bst.root is None

    def test_insert_single_value(self, bst):
        """Test inserting single value."""
        result = bst.insert(10)
        assert result is True
        assert bst.root is not None
        assert bst.root.value == 10

    def test_insert_multiple_values(self, bst):
        """Test inserting multiple values."""
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)

        assert bst.root.value == 10
        assert bst.root.left.value == 5
        assert bst.root.right.value == 15

    def test_insert_duplicate(self, bst):
        """Test inserting duplicate value."""
        bst.insert(10)
        result = bst.insert(10)
        assert result is False

    def test_search_found(self, bst):
        """Test searching for existing value."""
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)

        assert bst.search(10) is True
        assert bst.search(5) is True
        assert bst.search(15) is True

    def test_search_not_found(self, bst):
        """Test searching for non-existent value."""
        bst.insert(10)
        assert bst.search(20) is False

    def test_search_empty_tree(self, bst):
        """Test searching in empty tree."""
        assert bst.search(10) is False

    def test_delete_existing_value(self, bst):
        """Test deleting existing value."""
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)

        result = bst.delete(5)
        assert result is True
        assert bst.search(5) is False

    def test_delete_non_existing_value(self, bst):
        """Test deleting non-existent value."""
        bst.insert(10)
        result = bst.delete(20)
        assert result is False

    def test_delete_root(self, bst):
        """Test deleting root node."""
        bst.insert(10)
        bst.insert(5)
        result = bst.delete(10)
        assert result is True

    def test_inorder_traversal(self, bst):
        """Test inorder traversal produces sorted order."""
        values = [50, 30, 70, 20, 40, 60, 80]
        for val in values:
            bst.insert(val)

        result = bst.inorder_traversal()
        assert result == sorted(values)

    def test_height(self, bst):
        """Test height calculation."""
        bst.insert(10)
        bst.insert(5)
        bst.insert(15)
        bst.insert(3)

        height = bst.height()
        assert height >= 2

    def test_size(self, bst):
        """Test size calculation."""
        values = [10, 5, 15, 3, 7]
        for val in values:
            bst.insert(val)

        assert bst.size() == 5

    def test_get_statistics(self, bst):
        """Test getting statistics."""
        bst.insert(10)
        bst.insert(5)
        bst.search(5)

        stats = bst.get_statistics()
        assert "height" in stats
        assert "size" in stats
        assert "operations" in stats


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

    def test_avl_initialization(self, avl):
        """Test AVL tree initialization."""
        assert avl.root is None

    def test_insert_single_value(self, avl):
        """Test inserting single value."""
        result = avl.insert(10)
        assert result is True
        assert avl.root is not None
        assert avl.root.value == 10

    def test_insert_with_rotation(self, avl):
        """Test insertion triggers rotation."""
        # Insert values that require rotation
        avl.insert(10)
        avl.insert(20)
        avl.insert(30)  # Should trigger rotation

        assert avl.root is not None
        stats = avl.get_statistics()
        assert stats["rotations"] > 0

    def test_search_found(self, avl):
        """Test searching for existing value."""
        avl.insert(10)
        avl.insert(5)
        avl.insert(15)

        assert avl.search(10) is True
        assert avl.search(5) is True
        assert avl.search(15) is True

    def test_search_not_found(self, avl):
        """Test searching for non-existent value."""
        avl.insert(10)
        assert avl.search(20) is False

    def test_delete_existing_value(self, avl):
        """Test deleting existing value."""
        avl.insert(10)
        avl.insert(5)
        avl.insert(15)

        result = avl.delete(5)
        assert result is True
        assert avl.search(5) is False

    def test_inorder_traversal(self, avl):
        """Test inorder traversal produces sorted order."""
        values = [50, 30, 70, 20, 40, 60, 80]
        for val in values:
            avl.insert(val)

        result = avl.inorder_traversal()
        assert result == sorted(values)

    def test_height_balanced(self, avl):
        """Test that AVL tree maintains balanced height."""
        values = [10, 20, 30, 40, 50, 60, 70]
        for val in values:
            avl.insert(val)

        height = avl.height()
        # AVL tree height should be O(log n)
        assert height < len(values)

    def test_get_statistics(self, avl):
        """Test getting statistics."""
        avl.insert(10)
        avl.insert(5)
        avl.search(5)

        stats = avl.get_statistics()
        assert "height" in stats
        assert "size" in stats
        assert "rotations" in stats


class TestPerformanceAnalyzer:
    """Test cases for PerformanceAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        analyzer = PerformanceAnalyzer()
        assert analyzer.results == {}

    def test_compare_trees(self):
        """Test comparing BST vs AVL trees."""
        analyzer = PerformanceAnalyzer()
        values = [50, 30, 70, 20, 40, 60, 80]
        search_values = [20, 50, 80]

        results = analyzer.compare_trees(values, search_values)

        assert "bst" in results
        assert "avl" in results
        assert "improvement" in results
        assert results["bst"]["height"] >= 0
        assert results["avl"]["height"] >= 0

    def test_generate_report(self, tmp_path):
        """Test report generation."""
        analyzer = PerformanceAnalyzer()
        values = [50, 30, 70, 20, 40]
        analyzer.compare_trees(values)

        report_path = tmp_path / "report.txt"
        report = analyzer.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "BINARY SEARCH TREE" in report
        assert "AVL TREE" in report


class TestBalancing:
    """Test cases for tree balancing."""

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
        return str(config_file)

    def test_avl_maintains_balance_sequential(self, config_file):
        """Test AVL maintains balance with sequential insertions."""
        avl = AVLTree(config_path=config_file)
        # Sequential insertions create worst case for BST
        for i in range(1, 11):
            avl.insert(i)

        height = avl.height()
        # AVL should maintain O(log n) height
        assert height <= 4  # log2(10) ≈ 3.32, so height should be around 3-4

    def test_bst_degrades_sequential(self, config_file):
        """Test BST degrades with sequential insertions."""
        bst = BST(config_path=config_file)
        # Sequential insertions create worst case for BST
        for i in range(1, 11):
            bst.insert(i)

        height = bst.height()
        # BST can degrade to O(n) height
        assert height == 9  # Worst case: linear chain

    def test_avl_vs_bst_height_comparison(self, config_file):
        """Test height comparison between AVL and BST."""
        values = list(range(1, 21))  # Sequential values

        bst = BST(config_path=config_file)
        for val in values:
            bst.insert(val)

        avl = AVLTree(config_path=config_file)
        for val in values:
            avl.insert(val)

        bst_height = bst.height()
        avl_height = avl.height()

        # AVL should have significantly lower height
        assert avl_height < bst_height
