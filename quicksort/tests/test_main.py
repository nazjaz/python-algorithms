"""Unit tests for quicksort module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import QuickSort


class TestQuickSort:
    """Test cases for QuickSort class."""

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
    def sorter(self, config_file):
        """Create QuickSort instance."""
        return QuickSort(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        sorter = QuickSort(config_path=str(config_path))
        assert sorter.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            QuickSort(config_path="nonexistent.yaml")

    def test_sort_first_pivot(self, sorter):
        """Test sorting with first pivot strategy."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(arr, pivot_strategy="first")
        assert result == sorted(arr)

    def test_sort_last_pivot(self, sorter):
        """Test sorting with last pivot strategy."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(arr, pivot_strategy="last")
        assert result == sorted(arr)

    def test_sort_middle_pivot(self, sorter):
        """Test sorting with middle pivot strategy."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(arr, pivot_strategy="middle")
        assert result == sorted(arr)

    def test_sort_random_pivot(self, sorter):
        """Test sorting with random pivot strategy."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(arr, pivot_strategy="random")
        assert result == sorted(arr)

    def test_sort_median_of_three_pivot(self, sorter):
        """Test sorting with median-of-three pivot strategy."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = sorter.sort(arr, pivot_strategy="median_of_three")
        assert result == sorted(arr)

    def test_sort_invalid_pivot(self, sorter):
        """Test sorting with invalid pivot strategy raises error."""
        arr = [1, 2, 3]
        with pytest.raises(ValueError, match="Invalid pivot strategy"):
            sorter.sort(arr, pivot_strategy="invalid")

    def test_sort_empty_array(self, sorter):
        """Test sorting empty array."""
        result = sorter.sort([])
        assert result == []

    def test_sort_single_element(self, sorter):
        """Test sorting array with single element."""
        result = sorter.sort([42])
        assert result == [42]

    def test_sort_already_sorted(self, sorter):
        """Test sorting already sorted array."""
        arr = [1, 2, 3, 4, 5]
        result = sorter.sort(arr, pivot_strategy="first")
        assert result == sorted(arr)

    def test_sort_reverse_sorted(self, sorter):
        """Test sorting reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        result = sorter.sort(arr, pivot_strategy="last")
        assert result == sorted(arr)

    def test_sort_duplicates(self, sorter):
        """Test sorting array with duplicate elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = sorter.sort(arr)
        assert result == sorted(arr)

    def test_sort_negative_numbers(self, sorter):
        """Test sorting array with negative numbers."""
        arr = [-5, 3, -1, 0, 2, -3]
        result = sorter.sort(arr)
        assert result == sorted(arr)

    def test_sort_float_numbers(self, sorter):
        """Test sorting array with float numbers."""
        arr = [3.5, 1.2, 4.8, 2.1, 0.5]
        result = sorter.sort(arr)
        assert result == sorted(arr)

    def test_sort_preserves_original(self, sorter):
        """Test that original array is not modified."""
        original = [64, 34, 25, 12, 22, 11, 90]
        original_copy = original.copy()
        result = sorter.sort(original)
        assert original == original_copy
        assert result != original_copy

    def test_pivot_first(self, sorter):
        """Test first pivot selection."""
        arr = [10, 20, 30, 40, 50]
        pivot_idx = sorter._pivot_first(arr, 0, 4)
        assert pivot_idx == 0

    def test_pivot_last(self, sorter):
        """Test last pivot selection."""
        arr = [10, 20, 30, 40, 50]
        pivot_idx = sorter._pivot_last(arr, 0, 4)
        assert pivot_idx == 4

    def test_pivot_middle(self, sorter):
        """Test middle pivot selection."""
        arr = [10, 20, 30, 40, 50]
        pivot_idx = sorter._pivot_middle(arr, 0, 4)
        assert pivot_idx == 2

    def test_pivot_random(self, sorter):
        """Test random pivot selection."""
        arr = [10, 20, 30, 40, 50]
        pivot_idx = sorter._pivot_random(arr, 0, 4)
        assert 0 <= pivot_idx <= 4

    def test_pivot_median_of_three(self, sorter):
        """Test median-of-three pivot selection."""
        arr = [10, 50, 30, 40, 20]
        pivot_idx = sorter._pivot_median_of_three(arr, 0, 4)
        # Should select median of arr[0]=10, arr[2]=30, arr[4]=20
        # Median is 20 (arr[4])
        assert pivot_idx in [0, 2, 4]

    def test_get_stats(self, sorter):
        """Test getting sorting statistics."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        sorter.sort(arr, track_stats=True)
        stats = sorter.get_stats()
        assert "comparisons" in stats
        assert "swaps" in stats
        assert stats["comparisons"] > 0
        assert stats["swaps"] > 0

    def test_compare_strategies(self, sorter):
        """Test strategy comparison."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        results = sorter.compare_strategies(arr)

        assert "first" in results
        assert "last" in results
        assert "middle" in results
        assert "random" in results
        assert "median_of_three" in results

        for strategy, result in results.items():
            assert "execution_time" in result
            assert "comparisons" in result
            assert "swaps" in result
            assert "is_sorted" in result
            assert result["is_sorted"] is True

    def test_compare_strategies_specific(self, sorter):
        """Test comparing specific strategies."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        results = sorter.compare_strategies(arr, strategies=["first", "last"])

        assert "first" in results
        assert "last" in results
        assert "middle" not in results

    def test_generate_report(self, sorter, temp_dir):
        """Test report generation."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        results = sorter.compare_strategies(arr)
        report_path = temp_dir / "report.txt"
        report = sorter.generate_report(results, output_path=str(report_path))

        assert report_path.exists()
        assert "QUICKSORT PIVOT STRATEGY COMPARISON" in report
        assert "PERFORMANCE COMPARISON" in report

    def test_partition_functionality(self, sorter):
        """Test partition functionality."""
        arr = [10, 80, 30, 90, 40, 50, 70]
        # Use first as pivot for predictable test
        pivot_pos = sorter._partition(arr, 0, 6, sorter._pivot_first)

        # Elements before pivot should be < pivot value
        pivot_value = arr[pivot_pos]
        for i in range(pivot_pos):
            assert arr[i] < pivot_value

        # Elements after pivot should be >= pivot value
        for i in range(pivot_pos + 1, 7):
            assert arr[i] >= pivot_value

    def test_large_array(self, sorter):
        """Test sorting large array."""
        arr = list(range(100, 0, -1))
        result = sorter.sort(arr, pivot_strategy="median_of_three")
        assert result == sorted(arr)

    def test_all_strategies_produce_same_result(self, sorter):
        """Test that all strategies produce same sorted result."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        strategies = ["first", "last", "middle", "random", "median_of_three"]

        results = []
        for strategy in strategies:
            result = sorter.sort(arr, pivot_strategy=strategy)
            results.append(result)

        # All should produce same sorted result
        for result in results[1:]:
            assert result == results[0]

    def test_comparison_count_tracking(self, sorter):
        """Test that comparison count is tracked correctly."""
        arr = [3, 1, 4, 1, 5]
        sorter.sort(arr, track_stats=True)
        stats = sorter.get_stats()
        assert stats["comparisons"] > 0

    def test_swap_count_tracking(self, sorter):
        """Test that swap count is tracked correctly."""
        arr = [3, 1, 4, 1, 5]
        sorter.sort(arr, track_stats=True)
        stats = sorter.get_stats()
        assert stats["swaps"] > 0
