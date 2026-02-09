"""Unit tests for kth largest element finder module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import KthLargestFinder


class TestKthLargestFinder:
    """Test cases for KthLargestFinder class."""

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
    def finder(self, config_file):
        """Create KthLargestFinder instance."""
        return KthLargestFinder(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        finder = KthLargestFinder(config_path=str(config_path))
        assert finder.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            KthLargestFinder(config_path="nonexistent.yaml")

    def test_find_kth_largest_heap_simple(self, finder):
        """Test finding kth largest using heap with simple array."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_heap(arr, 3)
        assert result == 5

    def test_find_kth_largest_heap_first(self, finder):
        """Test finding 1st largest (maximum) using heap."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_heap(arr, 1)
        assert result == 9

    def test_find_kth_largest_heap_last(self, finder):
        """Test finding last largest (minimum) using heap."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_heap(arr, 8)
        assert result == 1

    def test_find_kth_largest_heap_invalid_k(self, finder):
        """Test heap method with invalid k."""
        arr = [3, 1, 4, 5]
        with pytest.raises(ValueError, match="at least 1"):
            finder.find_kth_largest_heap(arr, 0)

        with pytest.raises(IndexError):
            finder.find_kth_largest_heap(arr, 5)

    def test_find_kth_largest_heap_empty(self, finder):
        """Test heap method with empty array."""
        with pytest.raises(ValueError, match="empty"):
            finder.find_kth_largest_heap([], 1)

    def test_find_kth_largest_quickselect_simple(self, finder):
        """Test finding kth largest using quickselect with simple array."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_quickselect(arr, 3)
        assert result == 5

    def test_find_kth_largest_quickselect_first(self, finder):
        """Test finding 1st largest (maximum) using quickselect."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_quickselect(arr, 1)
        assert result == 9

    def test_find_kth_largest_quickselect_last(self, finder):
        """Test finding last largest (minimum) using quickselect."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_quickselect(arr, 8)
        assert result == 1

    def test_find_kth_largest_quickselect_invalid_k(self, finder):
        """Test quickselect method with invalid k."""
        arr = [3, 1, 4, 5]
        with pytest.raises(ValueError, match="at least 1"):
            finder.find_kth_largest_quickselect(arr, 0)

        with pytest.raises(IndexError):
            finder.find_kth_largest_quickselect(arr, 5)

    def test_find_kth_largest_quickselect_empty(self, finder):
        """Test quickselect method with empty array."""
        with pytest.raises(ValueError, match="empty"):
            finder.find_kth_largest_quickselect([], 1)

    def test_heap_vs_quickselect_same_result(self, finder):
        """Test that heap and quickselect produce same result."""
        test_cases = [
            ([3, 1, 4, 1, 5, 9, 2, 6], 3),
            ([64, 34, 25, 12, 22, 11, 90], 2),
            ([10, 20, 30, 40, 50], 1),
            ([5, 2, 8, 1, 9, 3, 7, 4, 6], 5),
        ]

        for arr, k in test_cases:
            heap_result = finder.find_kth_largest_heap(arr, k)
            quickselect_result = finder.find_kth_largest_quickselect(arr, k)
            assert heap_result == quickselect_result

    def test_compare_methods(self, finder):
        """Test method comparison."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 3
        results = finder.compare_methods(arr, k)

        assert "heap" in results
        assert "quickselect" in results
        assert results["heap"]["result"] == results["quickselect"]["result"]
        assert results["results_match"] is True

    def test_compare_methods_execution_time(self, finder):
        """Test that comparison includes execution time."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        results = finder.compare_methods(arr, 3)

        assert "execution_time" in results["heap"]
        assert "execution_time" in results["quickselect"]
        assert results["heap"]["execution_time"] >= 0
        assert results["quickselect"]["execution_time"] >= 0

    def test_find_kth_largest_all(self, finder):
        """Test finding all k largest elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        result = finder.find_kth_largest_all(arr, 3)
        assert len(result) == 3
        assert result == [9, 6, 5]

    def test_find_kth_largest_all_sorted(self, finder):
        """Test finding all k largest from sorted array."""
        arr = [1, 2, 3, 4, 5]
        result = finder.find_kth_largest_all(arr, 3)
        assert result == [5, 4, 3]

    def test_find_kth_largest_all_invalid_k(self, finder):
        """Test finding all k largest with invalid k."""
        arr = [3, 1, 4, 5]
        with pytest.raises(ValueError, match="at least 1"):
            finder.find_kth_largest_all(arr, 0)

        with pytest.raises(IndexError):
            finder.find_kth_largest_all(arr, 5)

    def test_get_stats(self, finder):
        """Test getting algorithm statistics."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        finder.find_kth_largest_quickselect(arr, 3, track_stats=True)
        stats = finder.get_stats()

        assert "comparisons" in stats
        assert "swaps" in stats
        assert stats["comparisons"] >= 0
        assert stats["swaps"] >= 0

    def test_generate_report(self, finder, temp_dir):
        """Test report generation."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 3
        comparison = finder.compare_methods(arr, k)
        report_path = temp_dir / "report.txt"
        report = finder.generate_report(
            arr, k, comparison, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "KTH LARGEST ELEMENT FINDER" in report
        assert "PERFORMANCE COMPARISON" in report

    def test_partition_functionality(self, finder):
        """Test partition functionality."""
        arr = [10, 80, 30, 90, 40, 50, 70]
        pivot_idx = 0
        pivot_pos = finder._partition(arr, 0, 6, pivot_idx)

        # Elements before pivot should be > pivot value
        pivot_value = arr[pivot_pos]
        for i in range(pivot_pos):
            assert arr[i] > pivot_value

        # Elements after pivot should be <= pivot value
        for i in range(pivot_pos + 1, 7):
            assert arr[i] <= pivot_value

    def test_large_array_heap(self, finder):
        """Test heap method with large array."""
        arr = list(range(100, 0, -1))
        result = finder.find_kth_largest_heap(arr, 10)
        assert result == 91

    def test_large_array_quickselect(self, finder):
        """Test quickselect method with large array."""
        arr = list(range(100, 0, -1))
        result = finder.find_kth_largest_quickselect(arr, 10)
        assert result == 91

    def test_duplicate_elements(self, finder):
        """Test with duplicate elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        heap_result = finder.find_kth_largest_heap(arr, 3)
        quickselect_result = finder.find_kth_largest_quickselect(arr, 3)
        assert heap_result == quickselect_result

    def test_single_element(self, finder):
        """Test with single element array."""
        arr = [42]
        assert finder.find_kth_largest_heap(arr, 1) == 42
        assert finder.find_kth_largest_quickselect(arr, 1) == 42

    def test_negative_numbers(self, finder):
        """Test with negative numbers."""
        arr = [-5, 3, -1, 0, 2, -3]
        heap_result = finder.find_kth_largest_heap(arr, 2)
        quickselect_result = finder.find_kth_largest_quickselect(arr, 2)
        assert heap_result == quickselect_result == 2

    def test_float_numbers(self, finder):
        """Test with float numbers."""
        arr = [3.5, 1.2, 4.8, 2.1, 0.5]
        heap_result = finder.find_kth_largest_heap(arr, 2)
        quickselect_result = finder.find_kth_largest_quickselect(arr, 2)
        assert abs(heap_result - quickselect_result) < 1e-10

    def test_sorted_array(self, finder):
        """Test with sorted array."""
        arr = [1, 2, 3, 4, 5]
        heap_result = finder.find_kth_largest_heap(arr, 3)
        quickselect_result = finder.find_kth_largest_quickselect(arr, 3)
        assert heap_result == quickselect_result == 3

    def test_reverse_sorted_array(self, finder):
        """Test with reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        heap_result = finder.find_kth_largest_heap(arr, 3)
        quickselect_result = finder.find_kth_largest_quickselect(arr, 3)
        assert heap_result == quickselect_result == 3

    def test_k_equals_length(self, finder):
        """Test when k equals array length (minimum element)."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        heap_result = finder.find_kth_largest_heap(arr, len(arr))
        quickselect_result = finder.find_kth_largest_quickselect(arr, len(arr))
        assert heap_result == quickselect_result == min(arr)

    def test_k_equals_one(self, finder):
        """Test when k equals 1 (maximum element)."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        heap_result = finder.find_kth_largest_heap(arr, 1)
        quickselect_result = finder.find_kth_largest_quickselect(arr, 1)
        assert heap_result == quickselect_result == max(arr)
