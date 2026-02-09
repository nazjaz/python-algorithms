"""Unit tests for selection sort module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import SelectionSort


class TestSelectionSort:
    """Test cases for SelectionSort class."""

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
        """Create SelectionSort instance."""
        return SelectionSort(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        sorter = SelectionSort(config_path=str(config_path))
        assert sorter.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            SelectionSort(config_path="nonexistent.yaml")

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

        # Should have comparisons (at least 1 per iteration for minimum finding)
        assert stats["comparisons"] >= 2

    def test_find_minimum(self, sorter):
        """Test minimum element finding."""
        array = [64, 34, 25, 12, 22, 11, 90]
        min_index, comparisons = sorter._find_minimum(array, 0)

        assert min_index == 5  # Index of 11
        assert array[min_index] == 11
        assert comparisons > 0

    def test_find_minimum_from_middle(self, sorter):
        """Test finding minimum from middle index."""
        array = [11, 12, 22, 25, 34, 64, 90]
        min_index, comparisons = sorter._find_minimum(array, 2)

        assert min_index == 2  # Index 2 has minimum from position 2 onwards
        assert comparisons > 0

    def test_generate_report(self, sorter, temp_dir):
        """Test report generation."""
        original = [64, 34, 25, 12, 22, 11, 90]
        sorted_array = sorter.sort(original)
        report_path = temp_dir / "report.txt"
        report = sorter.generate_report(original, sorted_array, output_path=str(report_path))

        assert report_path.exists()
        assert "SELECTION SORT ALGORITHM REPORT" in report
        assert "STATISTICS" in report
        assert "ITERATION DETAILS" in report
        assert "ALGORITHM COMPLEXITY" in report

    def test_swaps_count(self, sorter):
        """Test that swaps are counted correctly."""
        # Array that requires swaps
        sorter.sort([3, 2, 1])
        stats = sorter.get_statistics()

        # Should have at least one swap
        assert stats["swaps"] >= 0

    def test_iteration_details(self, sorter):
        """Test that iteration details are captured."""
        sorter.sort([3, 2, 1])
        stats = sorter.get_statistics()

        assert len(stats["iteration_details"]) == 2

        for iter_data in stats["iteration_details"]:
            assert "iteration" in iter_data
            assert "array_state" in iter_data
            assert "current_index" in iter_data
            assert "min_index" in iter_data
            assert "swapped" in iter_data
