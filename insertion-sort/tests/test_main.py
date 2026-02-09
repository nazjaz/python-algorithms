"""Unit tests for insertion sort module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import InsertionSort


class TestInsertionSort:
    """Test cases for InsertionSort class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "visualization": {"enabled": False},
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def sorter(self, config_file):
        """Create InsertionSort instance."""
        return InsertionSort(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "visualization": {"enabled": True},
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        sorter = InsertionSort(config_path=str(config_path))
        assert sorter.config["visualization"]["enabled"] is True

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            InsertionSort(config_path="nonexistent.yaml")

    def test_sort_empty_array(self, sorter):
        """Test sorting empty array."""
        result = sorter.sort([])
        assert result == []

    def test_sort_single_element(self, sorter):
        """Test sorting single element array."""
        result = sorter.sort([5])
        assert result == [5]

    def test_sort_already_sorted(self, sorter):
        """Test sorting already sorted array."""
        result = sorter.sort([1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]

    def test_sort_reverse_sorted(self, sorter):
        """Test sorting reverse sorted array."""
        result = sorter.sort([5, 4, 3, 2, 1])
        assert result == [1, 2, 3, 4, 5]

    def test_sort_unsorted(self, sorter):
        """Test sorting unsorted array."""
        result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
        assert result == [11, 12, 22, 25, 34, 64, 90]

    def test_sort_with_duplicates(self, sorter):
        """Test sorting array with duplicate values."""
        result = sorter.sort([3, 1, 3, 2, 1])
        assert result == [1, 1, 2, 3, 3]

    def test_sort_negative_numbers(self, sorter):
        """Test sorting array with negative numbers."""
        result = sorter.sort([-5, 3, -1, 0, 2])
        assert result == [-5, -1, 0, 2, 3]

    def test_sort_floats(self, sorter):
        """Test sorting array with floating point numbers."""
        result = sorter.sort([3.5, 1.2, 4.7, 2.1])
        assert result == [1.2, 2.1, 3.5, 4.7]

    def test_sort_original_not_modified(self, sorter):
        """Test that original array is not modified."""
        original = [64, 34, 25, 12, 22, 11, 90]
        original_copy = original.copy()
        sorter.sort(original)
        assert original == original_copy

    def test_get_statistics(self, sorter):
        """Test statistics retrieval."""
        sorter.sort([64, 34, 25, 12, 22, 11, 90])
        stats = sorter.get_statistics()

        assert "comparisons" in stats
        assert "swaps" in stats
        assert "iterations" in stats
        assert "iteration_details" in stats

        assert stats["comparisons"] > 0
        assert stats["swaps"] >= 0
        assert stats["iterations"] > 0

    def test_statistics_accuracy(self, sorter):
        """Test that statistics are accurate."""
        sorter.sort([3, 2, 1])
        stats = sorter.get_statistics()

        # For array of length 3, should have 2 iterations
        assert stats["iterations"] == 2

        # Should have comparisons
        assert stats["comparisons"] >= 0

    def test_bubble_sort(self, sorter):
        """Test bubble sort implementation."""
        array = [64, 34, 25, 12, 22, 11, 90]
        result, stats = sorter.bubble_sort(array)

        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert "comparisons" in stats
        assert "swaps" in stats

    def test_selection_sort(self, sorter):
        """Test selection sort implementation."""
        array = [64, 34, 25, 12, 22, 11, 90]
        result, stats = sorter.selection_sort(array)

        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert "comparisons" in stats
        assert "swaps" in stats

    def test_compare_algorithms(self, sorter):
        """Test algorithm comparison."""
        comparison = sorter.compare_algorithms([64, 34, 25, 12, 22, 11, 90])

        assert "array_length" in comparison
        assert "insertion_sort" in comparison
        assert "bubble_sort" in comparison
        assert "selection_sort" in comparison

        assert comparison["insertion_sort"]["success"] is True
        assert comparison["bubble_sort"]["success"] is True
        assert comparison["selection_sort"]["success"] is True

        # All should produce same sorted result
        assert (
            comparison["insertion_sort"]["result"]
            == comparison["bubble_sort"]["result"]
            == comparison["selection_sort"]["result"]
        )

    def test_compare_algorithms_multiple_iterations(self, sorter):
        """Test algorithm comparison with multiple iterations."""
        comparison = sorter.compare_algorithms([3, 2, 1], iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            algo.get("success", False)
            for algo in [
                comparison["insertion_sort"],
                comparison["bubble_sort"],
                comparison["selection_sort"],
            ]
        )

    def test_generate_report(self, sorter, temp_dir):
        """Test report generation."""
        original = [64, 34, 25, 12, 22, 11, 90]
        sorted_array = sorter.sort(original)
        comparison = sorter.compare_algorithms(original)
        report_path = temp_dir / "report.txt"
        report = sorter.generate_report(
            original, sorted_array, comparison, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "INSERTION SORT ALGORITHM REPORT" in report
        assert "STATISTICS" in report
        assert "ALGORITHM COMPARISON" in report

    def test_visualization_data_collection(self, sorter):
        """Test that visualization data is collected."""
        sorter.sort([3, 2, 1], enable_visualization=True)
        assert len(sorter.visualization_data) > 0

    def test_visualization_not_collected_by_default(self, sorter):
        """Test that visualization data is not collected by default."""
        sorter.sort([3, 2, 1], enable_visualization=False)
        assert len(sorter.visualization_data) == 0
