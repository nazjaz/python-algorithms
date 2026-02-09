"""Unit tests for longest increasing subsequence module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import LongestIncreasingSubsequence


class TestLongestIncreasingSubsequence:
    """Test cases for LongestIncreasingSubsequence class."""

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
    def lis_solver(self, config_file):
        """Create LongestIncreasingSubsequence instance."""
        return LongestIncreasingSubsequence(config_path=config_file)

    def test_find_lis_dp_empty(self, lis_solver):
        """Test finding LIS for empty array."""
        length, sequence = lis_solver.find_lis_dp([])
        assert length == 0
        assert sequence == []

    def test_find_lis_binary_search_empty(self, lis_solver):
        """Test finding LIS for empty array."""
        length, sequence = lis_solver.find_lis_binary_search([])
        assert length == 0
        assert sequence == []

    def test_find_lis_dp_single_element(self, lis_solver):
        """Test finding LIS for single element."""
        length, sequence = lis_solver.find_lis_dp([5])
        assert length == 1
        assert sequence == [5]

    def test_find_lis_binary_search_single_element(self, lis_solver):
        """Test finding LIS for single element."""
        length, sequence = lis_solver.find_lis_binary_search([5])
        assert length == 1
        assert sequence == [5]

    def test_find_lis_dp_simple(self, lis_solver):
        """Test finding LIS for simple array."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length == 4
        assert len(sequence) == 4
        assert sequence == sorted(sequence)
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_binary_search_simple(self, lis_solver):
        """Test finding LIS for simple array."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length == 4
        assert len(sequence) == 4
        assert sequence == sorted(sequence)
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_dp_already_sorted(self, lis_solver):
        """Test finding LIS for already sorted array."""
        arr = [1, 2, 3, 4, 5]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length == 5
        assert sequence == [1, 2, 3, 4, 5]

    def test_find_lis_binary_search_already_sorted(self, lis_solver):
        """Test finding LIS for already sorted array."""
        arr = [1, 2, 3, 4, 5]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length == 5
        assert sequence == [1, 2, 3, 4, 5]

    def test_find_lis_dp_reverse_sorted(self, lis_solver):
        """Test finding LIS for reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length == 1
        assert len(sequence) == 1

    def test_find_lis_binary_search_reverse_sorted(self, lis_solver):
        """Test finding LIS for reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length == 1
        assert len(sequence) == 1

    def test_find_lis_dp_all_equal(self, lis_solver):
        """Test finding LIS for array with all equal elements."""
        arr = [5, 5, 5, 5, 5]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length == 1
        assert len(sequence) == 1

    def test_find_lis_binary_search_all_equal(self, lis_solver):
        """Test finding LIS for array with all equal elements."""
        arr = [5, 5, 5, 5, 5]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length == 1
        assert len(sequence) == 1

    def test_find_lis_dp_duplicates(self, lis_solver):
        """Test finding LIS with duplicate values."""
        arr = [1, 3, 5, 4, 7, 5, 8]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length >= 4
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_binary_search_duplicates(self, lis_solver):
        """Test finding LIS with duplicate values."""
        arr = [1, 3, 5, 4, 7, 5, 8]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length >= 4
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_dp_negative_numbers(self, lis_solver):
        """Test finding LIS with negative numbers."""
        arr = [-5, -2, -8, -1, -9]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length >= 1
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_binary_search_negative_numbers(self, lis_solver):
        """Test finding LIS with negative numbers."""
        arr = [-5, -2, -8, -1, -9]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length >= 1
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_dp_floats(self, lis_solver):
        """Test finding LIS with floating point numbers."""
        arr = [1.5, 2.3, 1.8, 3.1, 2.9, 4.2]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length >= 1
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_binary_search_floats(self, lis_solver):
        """Test finding LIS with floating point numbers."""
        arr = [1.5, 2.3, 1.8, 3.1, 2.9, 4.2]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length >= 1
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_get_lis_length_dp(self, lis_solver):
        """Test getting LIS length using DP."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        length = lis_solver.get_lis_length_dp(arr)
        assert length == 4

    def test_get_lis_length_binary_search(self, lis_solver):
        """Test getting LIS length using binary search."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        length = lis_solver.get_lis_length_binary_search(arr)
        assert length == 4

    def test_get_lis_sequence_dp(self, lis_solver):
        """Test getting LIS sequence using DP."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        sequence = lis_solver.get_lis_sequence_dp(arr)
        assert len(sequence) == 4
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_get_lis_sequence_binary_search(self, lis_solver):
        """Test getting LIS sequence using binary search."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        sequence = lis_solver.get_lis_sequence_binary_search(arr)
        assert len(sequence) == 4
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_compare_approaches(self, lis_solver):
        """Test comparing both approaches."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        comparison = lis_solver.compare_approaches(arr)
        assert comparison["array_length"] == 8
        assert comparison["dp"]["success"] is True
        assert comparison["binary_search"]["success"] is True
        assert comparison["dp"]["length"] == comparison["binary_search"]["length"]

    def test_compare_approaches_with_iterations(self, lis_solver):
        """Test comparison with multiple iterations."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        comparison = lis_solver.compare_approaches(arr, iterations=10)
        assert comparison["iterations"] == 10
        assert comparison["dp"]["success"] is True
        assert comparison["binary_search"]["success"] is True

    def test_generate_report_success(self, lis_solver, temp_dir):
        """Test report generation."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        comparison = lis_solver.compare_approaches(arr)
        report_path = temp_dir / "report.txt"

        report = lis_solver.generate_report(comparison, output_path=str(report_path))

        assert "LONGEST INCREASING" in report
        assert "DYNAMIC PROGRAMMING" in report
        assert "BINARY SEARCH" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, lis_solver):
        """Test report generation without saving to file."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        comparison = lis_solver.compare_approaches(arr)
        report = lis_solver.generate_report(comparison)

        assert "LONGEST INCREASING" in report
        assert "DYNAMIC PROGRAMMING" in report
        assert "BINARY SEARCH" in report

    def test_find_lis_dp_large_array(self, lis_solver):
        """Test finding LIS for larger array."""
        arr = list(range(100, 0, -1))
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length == 1
        assert len(sequence) == 1

    def test_find_lis_binary_search_large_array(self, lis_solver):
        """Test finding LIS for larger array."""
        arr = list(range(100, 0, -1))
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length == 1
        assert len(sequence) == 1

    def test_find_lis_dp_mixed_positive_negative(self, lis_solver):
        """Test finding LIS with mixed positive and negative numbers."""
        arr = [-3, 1, -2, 4, -1, 2, 5]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length >= 1
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_binary_search_mixed_positive_negative(self, lis_solver):
        """Test finding LIS with mixed positive and negative numbers."""
        arr = [-3, 1, -2, 4, -1, 2, 5]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length >= 1
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_dp_known_result(self, lis_solver):
        """Test finding LIS with known result."""
        arr = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        length, sequence = lis_solver.find_lis_dp(arr)
        assert length == 6
        assert len(sequence) == 6
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_find_lis_binary_search_known_result(self, lis_solver):
        """Test finding LIS with known result."""
        arr = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        length, sequence = lis_solver.find_lis_binary_search(arr)
        assert length == 6
        assert len(sequence) == 6
        assert all(sequence[i] < sequence[i + 1] for i in range(len(sequence) - 1))

    def test_compare_approaches_identical_results(self, lis_solver):
        """Test that both approaches produce same length."""
        arr = [10, 9, 2, 5, 3, 7, 101, 18]
        comparison = lis_solver.compare_approaches(arr)
        assert comparison["dp"]["length"] == comparison["binary_search"]["length"]
