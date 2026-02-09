"""Unit tests for union-find module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import UnionFind


class TestUnionFind:
    """Test cases for UnionFind class."""

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
    def uf(self, config_file):
        """Create UnionFind instance."""
        return UnionFind(10, config_path=config_file)

    def test_init_zero_elements(self, config_file):
        """Test initialization with zero elements."""
        uf = UnionFind(0, config_path=config_file)
        assert uf.num_elements == 0
        assert uf.get_component_count() == 0

    def test_init_negative_elements(self, config_file):
        """Test initialization with negative elements."""
        with pytest.raises(ValueError, match="non-negative"):
            UnionFind(-1, config_path=config_file)

    def test_find_single_element(self, uf):
        """Test find operation on single element."""
        assert uf.find(0) == 0

    def test_find_multiple_elements(self, uf):
        """Test find operation on multiple elements."""
        for i in range(10):
            assert uf.find(i) == i

    def test_find_invalid_element(self, uf):
        """Test find operation with invalid element."""
        with pytest.raises(ValueError, match="out of range"):
            uf.find(10)

    def test_find_negative_element(self, uf):
        """Test find operation with negative element."""
        with pytest.raises(ValueError, match="out of range"):
            uf.find(-1)

    def test_union_two_elements(self, uf):
        """Test union of two elements."""
        result = uf.union(0, 1)
        assert result is True
        assert uf.connected(0, 1)
        assert uf.get_component_count() == 9

    def test_union_already_connected(self, uf):
        """Test union of already connected elements."""
        uf.union(0, 1)
        result = uf.union(0, 1)
        assert result is False
        assert uf.get_component_count() == 9

    def test_union_transitive(self, uf):
        """Test transitive union."""
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.connected(0, 2)
        assert uf.get_component_count() == 8

    def test_union_invalid_elements(self, uf):
        """Test union with invalid elements."""
        with pytest.raises(ValueError, match="out of range"):
            uf.union(0, 10)
        with pytest.raises(ValueError, match="out of range"):
            uf.union(-1, 0)

    def test_connected_same_element(self, uf):
        """Test connectivity of element with itself."""
        assert uf.connected(0, 0)

    def test_connected_different_elements(self, uf):
        """Test connectivity of different elements."""
        assert not uf.connected(0, 1)

    def test_connected_after_union(self, uf):
        """Test connectivity after union."""
        uf.union(0, 1)
        assert uf.connected(0, 1)

    def test_connected_invalid_elements(self, uf):
        """Test connectivity with invalid elements."""
        with pytest.raises(ValueError, match="out of range"):
            uf.connected(0, 10)

    def test_get_component_count_initial(self, uf):
        """Test component count initially."""
        assert uf.get_component_count() == 10

    def test_get_component_count_after_union(self, uf):
        """Test component count after union."""
        uf.union(0, 1)
        assert uf.get_component_count() == 9

    def test_get_component_count_all_connected(self, uf):
        """Test component count when all connected."""
        for i in range(9):
            uf.union(i, i + 1)
        assert uf.get_component_count() == 1

    def test_get_component_single(self, uf):
        """Test getting component of single element."""
        component = uf.get_component(0)
        assert component == [0]

    def test_get_component_after_union(self, uf):
        """Test getting component after union."""
        uf.union(0, 1)
        uf.union(1, 2)
        component = uf.get_component(0)
        assert set(component) == {0, 1, 2}

    def test_get_component_invalid_element(self, uf):
        """Test getting component with invalid element."""
        with pytest.raises(ValueError, match="out of range"):
            uf.get_component(10)

    def test_get_all_components_initial(self, uf):
        """Test getting all components initially."""
        components = uf.get_all_components()
        assert len(components) == 10
        for i in range(10):
            assert [i] in components.values()

    def test_get_all_components_after_union(self, uf):
        """Test getting all components after union."""
        uf.union(0, 1)
        uf.union(2, 3)
        components = uf.get_all_components()
        assert len(components) == 8

    def test_get_largest_component_initial(self, uf):
        """Test getting largest component initially."""
        largest = uf.get_largest_component()
        assert len(largest) == 1

    def test_get_largest_component_after_union(self, uf):
        """Test getting largest component after union."""
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)
        largest = uf.get_largest_component()
        assert len(largest) == 3

    def test_get_largest_component_empty(self, config_file):
        """Test getting largest component with empty union-find."""
        uf = UnionFind(0, config_path=config_file)
        largest = uf.get_largest_component()
        assert largest is None

    def test_get_component_statistics_initial(self, uf):
        """Test component statistics initially."""
        stats = uf.get_component_statistics()
        assert stats["count"] == 10
        assert stats["largest_size"] == 1
        assert stats["smallest_size"] == 1
        assert stats["average_size"] == 1.0

    def test_get_component_statistics_after_union(self, uf):
        """Test component statistics after union."""
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)
        stats = uf.get_component_statistics()
        assert stats["count"] == 8
        assert stats["largest_size"] == 3
        assert stats["smallest_size"] == 1

    def test_get_component_statistics_empty(self, config_file):
        """Test component statistics with empty union-find."""
        uf = UnionFind(0, config_path=config_file)
        stats = uf.get_component_statistics()
        assert stats["count"] == 0
        assert stats["largest_size"] == 0

    def test_union_all(self, uf):
        """Test unioning multiple pairs."""
        pairs = [(0, 1), (1, 2), (3, 4), (4, 5)]
        unions = uf.union_all(pairs)
        assert unions == 4
        assert uf.get_component_count() == 6

    def test_union_all_duplicates(self, uf):
        """Test unioning with duplicate pairs."""
        pairs = [(0, 1), (1, 2), (0, 1), (1, 2)]
        unions = uf.union_all(pairs)
        assert unions == 2
        assert uf.get_component_count() == 9

    def test_reset(self, uf):
        """Test resetting union-find."""
        uf.union(0, 1)
        uf.union(2, 3)
        assert uf.get_component_count() == 8
        uf.reset()
        assert uf.get_component_count() == 10
        assert not uf.connected(0, 1)

    def test_path_compression(self, uf):
        """Test that path compression works."""
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(2, 3)
        # After path compression, all should point directly to root
        root = uf.find(0)
        assert uf.find(1) == root
        assert uf.find(2) == root
        assert uf.find(3) == root

    def test_union_by_rank(self, uf):
        """Test that union by rank works."""
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(0, 2)
        # Check that ranks are maintained correctly
        assert uf.connected(0, 1)
        assert uf.connected(2, 3)
        assert uf.connected(0, 2)

    def test_compare_performance(self, uf):
        """Test performance comparison."""
        pairs = [(0, 1), (1, 2), (2, 3), (3, 4)]
        performance = uf.compare_performance(pairs)
        assert performance["num_elements"] == 10
        assert performance["num_pairs"] == 4
        assert performance["union_all"]["success"] is True
        assert performance["find_operations"]["success"] is True
        assert performance["connected_checks"]["success"] is True

    def test_compare_performance_with_iterations(self, uf):
        """Test performance comparison with multiple iterations."""
        pairs = [(0, 1), (1, 2)]
        performance = uf.compare_performance(pairs, iterations=10)
        assert performance["iterations"] == 10
        assert performance["union_all"]["success"] is True

    def test_generate_report_success(self, uf, temp_dir):
        """Test report generation."""
        pairs = [(0, 1), (1, 2), (2, 3)]
        performance = uf.compare_performance(pairs)
        report_path = temp_dir / "report.txt"

        report = uf.generate_report(performance, output_path=str(report_path))

        assert "UNION-FIND" in report
        assert "union_all" in report
        assert "find_operations" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, uf):
        """Test report generation without saving to file."""
        pairs = [(0, 1), (1, 2), (2, 3)]
        performance = uf.compare_performance(pairs)
        report = uf.generate_report(performance)

        assert "UNION-FIND" in report
        assert "union_all" in report
        assert "find_operations" in report

    def test_large_union_find(self, config_file):
        """Test union-find with large number of elements."""
        uf = UnionFind(1000, config_path=config_file)
        for i in range(999):
            uf.union(i, i + 1)
        assert uf.get_component_count() == 1
        assert uf.connected(0, 999)

    def test_multiple_components(self, uf):
        """Test multiple separate components."""
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)
        uf.union(4, 5)
        uf.union(6, 7)
        components = uf.get_all_components()
        assert len(components) == 5
        assert uf.connected(0, 2)
        assert uf.connected(3, 5)
        assert not uf.connected(0, 3)

    def test_complex_connectivity(self, uf):
        """Test complex connectivity scenario."""
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(4, 5)
        uf.union(0, 2)
        uf.union(4, 6)
        assert uf.connected(0, 3)
        assert uf.connected(4, 6)
        assert not uf.connected(0, 4)
        assert uf.get_component_count() == 4
