"""Unit tests for segment tree module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import SegmentTree


class TestSegmentTree:
    """Test cases for SegmentTree class."""

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

    def test_init_sum(self, config_file):
        """Test initializing segment tree with sum operation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        assert st.n == 5
        assert st.operation == "sum"

    def test_init_min(self, config_file):
        """Test initializing segment tree with min operation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="min", config_path=config_file)
        assert st.operation == "min"

    def test_init_max(self, config_file):
        """Test initializing segment tree with max operation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="max", config_path=config_file)
        assert st.operation == "max"

    def test_init_empty_array(self, config_file):
        """Test initializing with empty array."""
        with pytest.raises(ValueError, match="cannot be empty"):
            SegmentTree([], config_path=config_file)

    def test_init_invalid_operation(self, config_file):
        """Test initializing with invalid operation."""
        with pytest.raises(ValueError, match="Invalid operation"):
            SegmentTree([1, 2, 3], operation="invalid", config_path=config_file)

    def test_query_sum(self, config_file):
        """Test query with sum operation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.query(0, 4)
        assert result == 15.0

    def test_query_sum_range(self, config_file):
        """Test query with sum operation for range."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.query(1, 3)
        assert result == 9.0

    def test_query_min(self, config_file):
        """Test query with min operation."""
        arr = [5, 2, 8, 1, 9]
        st = SegmentTree(arr, operation="min", config_path=config_file)
        result = st.query(0, 4)
        assert result == 1.0

    def test_query_max(self, config_file):
        """Test query with max operation."""
        arr = [5, 2, 8, 1, 9]
        st = SegmentTree(arr, operation="max", config_path=config_file)
        result = st.query(0, 4)
        assert result == 9.0

    def test_query_single_element(self, config_file):
        """Test query for single element."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.query(2, 2)
        assert result == 3.0

    def test_query_invalid_range(self, config_file):
        """Test query with invalid range."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        with pytest.raises(ValueError, match="Invalid range"):
            st.query(3, 2)
        with pytest.raises(ValueError, match="Invalid range"):
            st.query(-1, 2)
        with pytest.raises(ValueError, match="Invalid range"):
            st.query(0, 10)

    def test_update_point_sum(self, config_file):
        """Test point update with sum operation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        st.update_point(2, 10)
        assert st.arr[2] == 10.0
        result = st.query(0, 4)
        assert result == 22.0

    def test_update_point_min(self, config_file):
        """Test point update with min operation."""
        arr = [5, 2, 8, 1, 9]
        st = SegmentTree(arr, operation="min", config_path=config_file)
        st.update_point(0, 0)
        result = st.query(0, 4)
        assert result == 0.0

    def test_update_point_max(self, config_file):
        """Test point update with max operation."""
        arr = [5, 2, 8, 1, 9]
        st = SegmentTree(arr, operation="max", config_path=config_file)
        st.update_point(1, 20)
        result = st.query(0, 4)
        assert result == 20.0

    def test_update_point_invalid_index(self, config_file):
        """Test point update with invalid index."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        with pytest.raises(ValueError, match="Invalid index"):
            st.update_point(-1, 10)
        with pytest.raises(ValueError, match="Invalid index"):
            st.update_point(10, 10)

    def test_update_range_sum(self, config_file):
        """Test range update with sum operation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        st.update_range(1, 3, 5)
        result = st.query(0, 4)
        assert result == 30.0

    def test_update_range_min(self, config_file):
        """Test range update with min operation."""
        arr = [5, 2, 8, 1, 9]
        st = SegmentTree(arr, operation="min", config_path=config_file)
        st.update_range(1, 3, -1)
        result = st.query(1, 3)
        assert result == 0.0

    def test_update_range_max(self, config_file):
        """Test range update with max operation."""
        arr = [5, 2, 8, 1, 9]
        st = SegmentTree(arr, operation="max", config_path=config_file)
        st.update_range(0, 2, 10)
        result = st.query(0, 2)
        assert result == 18.0

    def test_update_range_invalid(self, config_file):
        """Test range update with invalid range."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        with pytest.raises(ValueError, match="Invalid range"):
            st.update_range(3, 2, 5)
        with pytest.raises(ValueError, match="Invalid range"):
            st.update_range(-1, 2, 5)

    def test_get_array(self, config_file):
        """Test getting array."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.get_array()
        assert result == [1, 2, 3, 4, 5]

    def test_multiple_queries(self, config_file):
        """Test multiple queries."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        assert st.query(0, 0) == 1.0
        assert st.query(0, 1) == 3.0
        assert st.query(0, 2) == 6.0
        assert st.query(0, 3) == 10.0
        assert st.query(0, 4) == 15.0

    def test_multiple_updates(self, config_file):
        """Test multiple point updates."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        st.update_point(0, 10)
        st.update_point(4, 20)
        result = st.query(0, 4)
        assert result == 39.0

    def test_range_update_then_query(self, config_file):
        """Test range update followed by query."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        st.update_range(1, 3, 5)
        assert st.query(1, 1) == 7.0
        assert st.query(2, 2) == 8.0
        assert st.query(3, 3) == 9.0

    def test_single_element_array(self, config_file):
        """Test with single element array."""
        arr = [5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        assert st.query(0, 0) == 5.0
        st.update_point(0, 10)
        assert st.query(0, 0) == 10.0

    def test_large_array(self, config_file):
        """Test with larger array."""
        arr = list(range(1, 101))
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.query(0, 99)
        assert result == sum(range(1, 101))

    def test_negative_numbers(self, config_file):
        """Test with negative numbers."""
        arr = [-5, -2, -8, -1, -9]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.query(0, 4)
        assert result == -25.0

    def test_floating_point_numbers(self, config_file):
        """Test with floating point numbers."""
        arr = [1.5, 2.5, 3.5, 4.5, 5.5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        result = st.query(0, 4)
        assert abs(result - 17.5) < 0.001

    def test_compare_operations(self, config_file):
        """Test performance comparison."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        queries = [
            ("query", 0, 4),
            ("update_point", 2, 10),
            ("update_range", 1, 3, 5),
        ]
        performance = st.compare_operations(queries, iterations=1)
        assert performance["array_size"] == 5
        assert performance["operation"] == "sum"
        assert performance["query"]["success"] is True

    def test_generate_report_success(self, config_file, temp_dir):
        """Test report generation."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        queries = [("query", 0, 4)]
        performance = st.compare_operations(queries)
        report_path = temp_dir / "report.txt"

        report = st.generate_report(performance, output_path=str(report_path))

        assert "SEGMENT TREE" in report
        assert "query()" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, config_file):
        """Test report generation without saving to file."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        queries = [("query", 0, 4)]
        performance = st.compare_operations(queries)
        report = st.generate_report(performance)

        assert "SEGMENT TREE" in report
        assert "query()" in report

    def test_lazy_propagation(self, config_file):
        """Test lazy propagation with multiple range updates."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        st.update_range(0, 4, 5)
        st.update_range(1, 3, 2)
        result = st.query(0, 4)
        assert result == 35.0

    def test_query_after_range_update(self, config_file):
        """Test query after range update."""
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr, operation="sum", config_path=config_file)
        st.update_range(1, 3, 10)
        assert st.query(0, 0) == 1.0
        assert st.query(1, 1) == 12.0
        assert st.query(4, 4) == 5.0
