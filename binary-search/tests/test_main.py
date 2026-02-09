"""Unit tests for binary search module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BinarySearch


class TestBinarySearch:
    """Test cases for BinarySearch class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "recursion": {"max_depth": 1000},
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def searcher(self, config_file):
        """Create BinarySearch instance."""
        return BinarySearch(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "recursion": {"max_depth": 500},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        searcher = BinarySearch(config_path=str(config_path))
        assert searcher.config["recursion"]["max_depth"] == 500

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            BinarySearch(config_path="nonexistent.yaml")

    def test_search_iterative_found(self, searcher):
        """Test iterative search when target is found."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = searcher.search_iterative(array, 5)
        assert result == 4

    def test_search_iterative_not_found(self, searcher):
        """Test iterative search when target is not found."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = searcher.search_iterative(array, 25)
        assert result is None

    def test_search_iterative_empty(self, searcher):
        """Test iterative search with empty array."""
        result = searcher.search_iterative([], 5)
        assert result is None

    def test_search_iterative_single_element_found(self, searcher):
        """Test iterative search with single element found."""
        result = searcher.search_iterative([5], 5)
        assert result == 0

    def test_search_iterative_single_element_not_found(self, searcher):
        """Test iterative search with single element not found."""
        result = searcher.search_iterative([5], 3)
        assert result is None

    def test_search_iterative_first_element(self, searcher):
        """Test iterative search for first element."""
        array = [1, 2, 3, 4, 5]
        result = searcher.search_iterative(array, 1)
        assert result == 0

    def test_search_iterative_last_element(self, searcher):
        """Test iterative search for last element."""
        array = [1, 2, 3, 4, 5]
        result = searcher.search_iterative(array, 5)
        assert result == 4

    def test_search_iterative_unsorted(self, searcher):
        """Test iterative search with unsorted array raises error."""
        with pytest.raises(ValueError, match="must be sorted"):
            searcher.search_iterative([3, 1, 2], 2)

    def test_search_recursive_found(self, searcher):
        """Test recursive search when target is found."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = searcher.search_recursive(array, 5)
        assert result == 4

    def test_search_recursive_not_found(self, searcher):
        """Test recursive search when target is not found."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = searcher.search_recursive(array, 25)
        assert result is None

    def test_search_recursive_empty(self, searcher):
        """Test recursive search with empty array."""
        result = searcher.search_recursive([], 5)
        assert result is None

    def test_search_recursive_single_element_found(self, searcher):
        """Test recursive search with single element found."""
        result = searcher.search_recursive([5], 5)
        assert result == 0

    def test_search_recursive_single_element_not_found(self, searcher):
        """Test recursive search with single element not found."""
        result = searcher.search_recursive([5], 3)
        assert result is None

    def test_search_recursive_first_element(self, searcher):
        """Test recursive search for first element."""
        array = [1, 2, 3, 4, 5]
        result = searcher.search_recursive(array, 1)
        assert result == 0

    def test_search_recursive_last_element(self, searcher):
        """Test recursive search for last element."""
        array = [1, 2, 3, 4, 5]
        result = searcher.search_recursive(array, 5)
        assert result == 4

    def test_search_recursive_unsorted(self, searcher):
        """Test recursive search with unsorted array raises error."""
        with pytest.raises(ValueError, match="must be sorted"):
            searcher.search_recursive([3, 1, 2], 2)

    def test_all_methods_same_result(self, searcher):
        """Test that all methods produce same result."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        targets = [1, 5, 10, 25]

        for target in targets:
            iterative = searcher.search_iterative(array, target)
            recursive = searcher.search_recursive(array, target)
            assert iterative == recursive, f"Failed for target: {target}"

    def test_compare_approaches(self, searcher):
        """Test performance comparison."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        comparison = searcher.compare_approaches(array, 5)

        assert "array_length" in comparison
        assert "iterative" in comparison
        assert "recursive" in comparison

        assert comparison["iterative"]["success"] is True
        assert comparison["recursive"]["success"] is True

        assert comparison["iterative"]["result"] == comparison["recursive"]["result"]

    def test_compare_approaches_multiple_iterations(self, searcher):
        """Test performance comparison with multiple iterations."""
        array = [1, 2, 3, 4, 5]
        comparison = searcher.compare_approaches(array, 3, iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            method.get("success", False)
            for method in [
                comparison["iterative"],
                comparison["recursive"],
            ]
        )

    def test_generate_report(self, searcher, temp_dir):
        """Test report generation."""
        array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        comparison = searcher.compare_approaches(array, 5)
        report_path = temp_dir / "report.txt"
        report = searcher.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "BINARY SEARCH PERFORMANCE COMPARISON REPORT" in report
        assert "Iterative Method" in report
        assert "Recursive Method" in report

    def test_validate_sorted(self, searcher):
        """Test sorted array validation."""
        assert searcher._validate_sorted([1, 2, 3, 4, 5]) is True
        assert searcher._validate_sorted([1, 3, 2, 4, 5]) is False
        assert searcher._validate_sorted([]) is True
        assert searcher._validate_sorted([1]) is True

    def test_duplicate_values(self, searcher):
        """Test search with duplicate values."""
        array = [1, 2, 2, 3, 4, 5]
        result = searcher.search_iterative(array, 2)
        assert result in [1, 2]  # May return either occurrence

    def test_large_array(self, searcher):
        """Test search with large array."""
        array = list(range(1000))
        result = searcher.search_iterative(array, 500)
        assert result == 500

        result = searcher.search_recursive(array, 500)
        assert result == 500
