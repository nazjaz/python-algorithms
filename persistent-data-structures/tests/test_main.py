"""Unit tests for persistent data structures module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import PersistentArray, PersistentList, PersistentNode


class TestPersistentNode:
    """Test cases for PersistentNode class."""

    def test_node_creation(self):
        """Test PersistentNode creation."""
        node = PersistentNode(value=5, size=1)
        assert node.value == 5
        assert node.size == 1
        assert node.left is None
        assert node.right is None

    def test_node_with_children(self):
        """Test PersistentNode with children."""
        left = PersistentNode(value=1, size=1)
        right = PersistentNode(value=2, size=1)
        node = PersistentNode(left=left, right=right, size=2)

        assert node.left == left
        assert node.right == right
        assert node.size == 2

    def test_is_leaf(self):
        """Test is_leaf method."""
        leaf = PersistentNode(value=5, size=1)
        assert leaf.is_leaf() is True

        node = PersistentNode(
            left=PersistentNode(value=1, size=1),
            right=PersistentNode(value=2, size=1),
            size=2,
        )
        assert node.is_leaf() is False

    def test_copy(self):
        """Test copy method."""
        node = PersistentNode(value=5, size=1)
        copied = node.copy()

        assert copied.value == node.value
        assert copied.size == node.size
        assert copied is not node


class TestPersistentArray:
    """Test cases for PersistentArray class."""

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
    def array(self, config_file):
        """Create PersistentArray instance."""
        return PersistentArray([1, 2, 3, 4, 5], config_path=config_file)

    def test_array_creation(self, config_file):
        """Test PersistentArray creation."""
        arr = PersistentArray([1, 2, 3], config_path=config_file)
        assert arr.get_size(0) == 3

    def test_empty_array_creation(self, config_file):
        """Test empty PersistentArray creation."""
        arr = PersistentArray(config_path=config_file)
        assert arr.get_size(0) == 0

    def test_get_operation(self, array):
        """Test get operation."""
        value = array.get(0, 0)
        assert value == 1

        value = array.get(0, 2)
        assert value == 3

    def test_get_out_of_bounds(self, array):
        """Test get with out of bounds index."""
        with pytest.raises(IndexError):
            array.get(0, 10)

    def test_get_invalid_version(self, array):
        """Test get with invalid version."""
        with pytest.raises(IndexError):
            array.get(10, 0)

    def test_set_operation(self, array):
        """Test set operation."""
        v0 = array.get_current_version()
        v1 = array.set(v0, 2, 10)

        assert array.get(v0, 2) == 3
        assert array.get(v1, 2) == 10

    def test_set_preserves_old_version(self, array):
        """Test that set preserves old version."""
        v0 = array.get_current_version()

        original_values = [array.get(v0, i) for i in range(array.get_size(v0))]

        v1 = array.set(v0, 0, 100)

        for i in range(array.get_size(v0)):
            assert array.get(v0, i) == original_values[i]

        assert array.get(v1, 0) == 100

    def test_set_out_of_bounds(self, array):
        """Test set with out of bounds index."""
        v0 = array.get_current_version()
        with pytest.raises(IndexError):
            array.set(v0, 10, 100)

    def test_set_invalid_version(self, array):
        """Test set with invalid version."""
        with pytest.raises(IndexError):
            array.set(10, 0, 100)

    def test_multiple_versions(self, array):
        """Test multiple versions."""
        v0 = array.get_current_version()
        v1 = array.set(v0, 0, 10)
        v2 = array.set(v1, 1, 20)
        v3 = array.set(v2, 2, 30)

        assert array.get(v0, 0) == 1
        assert array.get(v1, 0) == 10
        assert array.get(v2, 1) == 20
        assert array.get(v3, 2) == 30

    def test_get_size(self, array):
        """Test get_size operation."""
        size = array.get_size(0)
        assert size == 5

    def test_get_current_version(self, array):
        """Test get_current_version operation."""
        v0 = array.get_current_version()
        assert v0 == 0

        v1 = array.set(v0, 0, 10)
        assert array.get_current_version() == 1


class TestPersistentList:
    """Test cases for PersistentList class."""

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
    def lst(self, config_file):
        """Create PersistentList instance."""
        return PersistentList([10, 20, 30], config_path=config_file)

    def test_list_creation(self, config_file):
        """Test PersistentList creation."""
        lst = PersistentList([1, 2, 3], config_path=config_file)
        assert lst.get_size(0) == 3

    def test_empty_list_creation(self, config_file):
        """Test empty PersistentList creation."""
        lst = PersistentList(config_path=config_file)
        assert lst.get_size(0) == 0

    def test_get_operation(self, lst):
        """Test get operation."""
        value = lst.get(0, 0)
        assert value == 10

        value = lst.get(0, 2)
        assert value == 30

    def test_get_out_of_bounds(self, lst):
        """Test get with out of bounds index."""
        with pytest.raises(IndexError):
            lst.get(0, 10)

    def test_get_invalid_version(self, lst):
        """Test get with invalid version."""
        with pytest.raises(IndexError):
            lst.get(10, 0)

    def test_set_operation(self, lst):
        """Test set operation."""
        v0 = lst.get_current_version()
        v1 = lst.set(v0, 1, 25)

        assert lst.get(v0, 1) == 20
        assert lst.get(v1, 1) == 25

    def test_set_preserves_old_version(self, lst):
        """Test that set preserves old version."""
        v0 = lst.get_current_version()

        original_values = [lst.get(v0, i) for i in range(lst.get_size(v0))]

        v1 = lst.set(v0, 0, 100)

        for i in range(lst.get_size(v0)):
            assert lst.get(v0, i) == original_values[i]

        assert lst.get(v1, 0) == 100

    def test_append_operation(self, lst):
        """Test append operation."""
        v0 = lst.get_current_version()
        v1 = lst.append(v0, 40)

        assert lst.get_size(v0) == 3
        assert lst.get_size(v1) == 4
        assert lst.get(v1, 3) == 40

    def test_append_preserves_old_version(self, lst):
        """Test that append preserves old version."""
        v0 = lst.get_current_version()

        original_values = [lst.get(v0, i) for i in range(lst.get_size(v0))]

        v1 = lst.append(v0, 40)

        for i in range(lst.get_size(v0)):
            assert lst.get(v0, i) == original_values[i]

        assert lst.get_size(v1) == lst.get_size(v0) + 1

    def test_append_to_empty_list(self, config_file):
        """Test appending to empty list."""
        lst = PersistentList(config_path=config_file)
        v0 = lst.get_current_version()

        v1 = lst.append(v0, 10)
        assert lst.get_size(v1) == 1
        assert lst.get(v1, 0) == 10

    def test_multiple_operations(self, lst):
        """Test multiple operations."""
        v0 = lst.get_current_version()
        v1 = lst.append(v0, 40)
        v2 = lst.set(v1, 1, 25)
        v3 = lst.append(v2, 50)

        assert lst.get_size(v0) == 3
        assert lst.get_size(v1) == 4
        assert lst.get_size(v2) == 4
        assert lst.get_size(v3) == 5

        assert lst.get(v3, 1) == 25
        assert lst.get(v3, 4) == 50

    def test_get_size(self, lst):
        """Test get_size operation."""
        size = lst.get_size(0)
        assert size == 3

    def test_get_current_version(self, lst):
        """Test get_current_version operation."""
        v0 = lst.get_current_version()
        assert v0 == 0

        v1 = lst.append(v0, 40)
        assert lst.get_current_version() == 1

    def test_complex_sequence(self, config_file):
        """Test complex sequence of operations."""
        lst = PersistentList([1, 2, 3], config_path=config_file)
        v0 = lst.get_current_version()

        v1 = lst.append(v0, 4)
        v2 = lst.set(v1, 0, 10)
        v3 = lst.append(v2, 5)
        v4 = lst.set(v3, 2, 20)

        assert lst.get(v0, 0) == 1
        assert lst.get(v1, 3) == 4
        assert lst.get(v2, 0) == 10
        assert lst.get(v3, 4) == 5
        assert lst.get(v4, 2) == 20
