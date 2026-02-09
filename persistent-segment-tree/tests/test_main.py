"""Unit tests for persistent segment tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import PersistentSegmentTree


class TestPersistentSegmentTree:
    """Test cases for PersistentSegmentTree class."""

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
    def simple_tree(self, config_file):
        """Create simple persistent segment tree."""
        return PersistentSegmentTree([1, 2, 3, 4, 5], config_path=config_file)

    def test_creation(self, config_file):
        """Test tree creation."""
        tree = PersistentSegmentTree([1, 2, 3], config_path=config_file)
        assert tree.get_size() == 3
        assert tree.get_version_count() == 1

    def test_creation_empty_array(self):
        """Test creation with empty array."""
        with pytest.raises(ValueError):
            PersistentSegmentTree([])

    def test_query_sum_single_element(self, config_file):
        """Test query sum for single element."""
        tree = PersistentSegmentTree([10], config_path=config_file)
        assert tree.query_sum(0, 0, 0) == 10

    def test_query_sum_range(self, simple_tree):
        """Test query sum for range."""
        assert simple_tree.query_sum(0, 0, 2) == 6
        assert simple_tree.query_sum(0, 1, 3) == 9
        assert simple_tree.query_sum(0, 0, 4) == 15

    def test_query_sum_invalid_version(self, simple_tree):
        """Test query sum with invalid version."""
        with pytest.raises(ValueError):
            simple_tree.query_sum(-1, 0, 2)
        with pytest.raises(ValueError):
            simple_tree.query_sum(10, 0, 2)

    def test_query_sum_invalid_indices(self, simple_tree):
        """Test query sum with invalid indices."""
        with pytest.raises(ValueError):
            simple_tree.query_sum(0, -1, 2)
        with pytest.raises(ValueError):
            simple_tree.query_sum(0, 0, 10)
        with pytest.raises(ValueError):
            simple_tree.query_sum(0, 3, 2)

    def test_query_min(self, config_file):
        """Test query minimum."""
        tree = PersistentSegmentTree([5, 2, 8, 1, 9], config_path=config_file)
        assert tree.query_min(0, 0, 4) == 1
        assert tree.query_min(0, 0, 2) == 2
        assert tree.query_min(0, 2, 4) == 1

    def test_query_max(self, config_file):
        """Test query maximum."""
        tree = PersistentSegmentTree([5, 2, 8, 1, 9], config_path=config_file)
        assert tree.query_max(0, 0, 4) == 9
        assert tree.query_max(0, 0, 2) == 8
        assert tree.query_max(0, 1, 3) == 8

    def test_update_creates_new_version(self, simple_tree):
        """Test that update creates new version."""
        initial_version_count = simple_tree.get_version_count()
        new_version = simple_tree.update(0, 2, 10)
        assert simple_tree.get_version_count() == initial_version_count + 1
        assert new_version == 1

    def test_update_preserves_old_version(self, simple_tree):
        """Test that update preserves old version."""
        sum_before = simple_tree.query_sum(0, 0, 4)
        simple_tree.update(0, 2, 10)
        sum_after = simple_tree.query_sum(0, 0, 4)
        assert sum_before == sum_after

    def test_update_new_version_has_new_value(self, simple_tree):
        """Test that new version has updated value."""
        new_version = simple_tree.update(0, 2, 10)
        sum_v0 = simple_tree.query_sum(0, 0, 4)
        sum_v1 = simple_tree.query_sum(new_version, 0, 4)
        assert sum_v1 == sum_v0 + 7

    def test_update_invalid_version(self, simple_tree):
        """Test update with invalid version."""
        with pytest.raises(ValueError):
            simple_tree.update(-1, 0, 10)
        with pytest.raises(ValueError):
            simple_tree.update(10, 0, 10)

    def test_update_invalid_index(self, simple_tree):
        """Test update with invalid index."""
        with pytest.raises(ValueError):
            simple_tree.update(0, -1, 10)
        with pytest.raises(ValueError):
            simple_tree.update(0, 10, 10)

    def test_multiple_updates(self, config_file):
        """Test multiple updates creating multiple versions."""
        tree = PersistentSegmentTree([1, 2, 3, 4, 5], config_path=config_file)
        v1 = tree.update(0, 0, 10)
        v2 = tree.update(v1, 1, 20)
        v3 = tree.update(v2, 2, 30)

        assert tree.get_version_count() == 4
        assert tree.query_sum(0, 0, 4) == 15
        assert tree.query_sum(v1, 0, 4) == 24
        assert tree.query_sum(v2, 0, 4) == 42
        assert tree.query_sum(v3, 0, 4) == 69

    def test_query_different_versions(self, config_file):
        """Test querying different versions."""
        tree = PersistentSegmentTree([1, 2, 3, 4, 5], config_path=config_file)
        v1 = tree.update(0, 0, 10)
        v2 = tree.update(v1, 2, 20)

        assert tree.query_sum(0, 0, 2) == 6
        assert tree.query_sum(v1, 0, 2) == 15
        assert tree.query_sum(v2, 0, 2) == 32

    def test_get_version_array(self, config_file):
        """Test getting array representation of version."""
        tree = PersistentSegmentTree([1, 2, 3], config_path=config_file)
        arr_v0 = tree.get_version_array(0)
        assert arr_v0 == [1, 2, 3]

        v1 = tree.update(0, 1, 10)
        arr_v1 = tree.get_version_array(v1)
        assert arr_v1 == [1, 10, 3]

        arr_v0_again = tree.get_version_array(0)
        assert arr_v0_again == [1, 2, 3]

    def test_get_version_array_invalid(self, simple_tree):
        """Test get_version_array with invalid version."""
        with pytest.raises(ValueError):
            simple_tree.get_version_array(-1)
        with pytest.raises(ValueError):
            simple_tree.get_version_array(10)

    def test_get_version_count(self, simple_tree):
        """Test getting version count."""
        assert simple_tree.get_version_count() == 1
        simple_tree.update(0, 0, 10)
        assert simple_tree.get_version_count() == 2

    def test_get_size(self, config_file):
        """Test getting size."""
        tree = PersistentSegmentTree([1, 2, 3, 4, 5], config_path=config_file)
        assert tree.get_size() == 5

    def test_large_array(self, config_file):
        """Test with large array."""
        array = list(range(1, 101))
        tree = PersistentSegmentTree(array, config_path=config_file)
        assert tree.query_sum(0, 0, 99) == sum(array)
        assert tree.query_min(0, 0, 99) == 1
        assert tree.query_max(0, 0, 99) == 100

    def test_sequential_updates(self, config_file):
        """Test sequential updates."""
        tree = PersistentSegmentTree([0] * 10, config_path=config_file)
        current_version = 0

        for i in range(10):
            current_version = tree.update(current_version, i, i + 1)

        assert tree.get_version_count() == 11
        final_sum = tree.query_sum(current_version, 0, 9)
        assert final_sum == 55

    def test_query_all_versions(self, config_file):
        """Test querying all versions."""
        tree = PersistentSegmentTree([1, 2, 3], config_path=config_file)
        v1 = tree.update(0, 0, 10)
        v2 = tree.update(v1, 1, 20)

        for version in range(tree.get_version_count()):
            total = tree.query_sum(version, 0, 2)
            assert total >= 0

    def test_min_max_queries_all_versions(self, config_file):
        """Test min/max queries across versions."""
        tree = PersistentSegmentTree([5, 2, 8, 1, 9], config_path=config_file)
        v1 = tree.update(0, 1, 0)
        v2 = tree.update(v1, 3, 10)

        assert tree.query_min(0, 0, 4) == 1
        assert tree.query_min(v1, 0, 4) == 0
        assert tree.query_min(v2, 0, 4) == 0

        assert tree.query_max(0, 0, 4) == 9
        assert tree.query_max(v1, 0, 4) == 9
        assert tree.query_max(v2, 0, 4) == 10

    def test_range_queries_after_updates(self, config_file):
        """Test range queries after updates."""
        tree = PersistentSegmentTree([1, 2, 3, 4, 5], config_path=config_file)
        v1 = tree.update(0, 2, 10)

        assert tree.query_sum(0, 1, 3) == 9
        assert tree.query_sum(v1, 1, 3) == 16

    def test_single_element_updates(self, config_file):
        """Test updates on single element array."""
        tree = PersistentSegmentTree([10], config_path=config_file)
        v1 = tree.update(0, 0, 20)

        assert tree.query_sum(0, 0, 0) == 10
        assert tree.query_sum(v1, 0, 0) == 20
