"""Unit tests for edit distance module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import EditDistance


class TestEditDistance:
    """Test cases for EditDistance class."""

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
    def ed(self, config_file):
        """Create EditDistance instance."""
        return EditDistance(config_path=config_file)

    def test_calculate_dp_identical_strings(self, ed):
        """Test DP calculation with identical strings."""
        distance, dp_table = ed.calculate_dp("hello", "hello")
        assert distance == 0
        assert dp_table[5][5] == 0

    def test_calculate_dp_different_strings(self, ed):
        """Test DP calculation with different strings."""
        distance, dp_table = ed.calculate_dp("kitten", "sitting")
        assert distance == 3

    def test_calculate_dp_empty_strings(self, ed):
        """Test DP calculation with empty strings."""
        distance, dp_table = ed.calculate_dp("", "")
        assert distance == 0

    def test_calculate_dp_one_empty(self, ed):
        """Test DP calculation with one empty string."""
        distance, dp_table = ed.calculate_dp("hello", "")
        assert distance == 5
        distance2, _ = ed.calculate_dp("", "hello")
        assert distance2 == 5

    def test_calculate_dp_single_character(self, ed):
        """Test DP calculation with single characters."""
        distance, dp_table = ed.calculate_dp("a", "b")
        assert distance == 1
        distance2, _ = ed.calculate_dp("a", "a")
        assert distance2 == 0

    def test_calculate_optimized_identical_strings(self, ed):
        """Test optimized calculation with identical strings."""
        distance, last_row = ed.calculate_optimized("hello", "hello")
        assert distance == 0

    def test_calculate_optimized_different_strings(self, ed):
        """Test optimized calculation with different strings."""
        distance, last_row = ed.calculate_optimized("kitten", "sitting")
        assert distance == 3

    def test_calculate_optimized_empty_strings(self, ed):
        """Test optimized calculation with empty strings."""
        distance, last_row = ed.calculate_optimized("", "")
        assert distance == 0

    def test_calculate_optimized_one_empty(self, ed):
        """Test optimized calculation with one empty string."""
        distance, last_row = ed.calculate_optimized("hello", "")
        assert distance == 5
        distance2, _ = ed.calculate_optimized("", "hello")
        assert distance2 == 5

    def test_calculate_optimized_single_character(self, ed):
        """Test optimized calculation with single characters."""
        distance, last_row = ed.calculate_optimized("a", "b")
        assert distance == 1
        distance2, _ = ed.calculate_optimized("a", "a")
        assert distance2 == 0

    def test_dp_vs_optimized_same_result(self, ed):
        """Test that DP and optimized produce same results."""
        test_cases = [
            ("kitten", "sitting"),
            ("hello", "hallo"),
            ("abc", "def"),
            ("", "abc"),
            ("abc", ""),
            ("", ""),
            ("a", "b"),
            ("a", "a"),
        ]
        for str1, str2 in test_cases:
            distance_dp, _ = ed.calculate_dp(str1, str2)
            distance_opt, _ = ed.calculate_optimized(str1, str2)
            assert distance_dp == distance_opt, f"Failed for '{str1}' -> '{str2}'"

    def test_get_distance_dp(self, ed):
        """Test getting distance using DP."""
        distance = ed.get_distance_dp("kitten", "sitting")
        assert distance == 3

    def test_get_distance_optimized(self, ed):
        """Test getting distance using optimized approach."""
        distance = ed.get_distance_optimized("kitten", "sitting")
        assert distance == 3

    def test_get_operations(self, ed):
        """Test getting operation sequence."""
        distance, dp_table = ed.calculate_dp("kitten", "sitting")
        operations = ed.get_operations("kitten", "sitting", dp_table)
        assert len(operations) == distance
        assert all(isinstance(op, str) for op in operations)

    def test_get_operations_identical(self, ed):
        """Test getting operations for identical strings."""
        distance, dp_table = ed.calculate_dp("hello", "hello")
        operations = ed.get_operations("hello", "hello", dp_table)
        assert len(operations) == 0

    def test_get_operations_one_empty(self, ed):
        """Test getting operations with one empty string."""
        distance, dp_table = ed.calculate_dp("hello", "")
        operations = ed.get_operations("hello", "", dp_table)
        assert len(operations) == 5

    def test_compare_approaches(self, ed):
        """Test comparing both approaches."""
        comparison = ed.compare_approaches("kitten", "sitting", iterations=1)
        assert comparison["str1_length"] == 6
        assert comparison["str2_length"] == 7
        assert comparison["dp"]["success"] is True
        assert comparison["optimized"]["success"] is True
        assert comparison["dp"]["distance"] == comparison["optimized"]["distance"]

    def test_compare_approaches_with_iterations(self, ed):
        """Test comparison with multiple iterations."""
        comparison = ed.compare_approaches("kitten", "sitting", iterations=10)
        assert comparison["iterations"] == 10
        assert comparison["dp"]["success"] is True
        assert comparison["optimized"]["success"] is True

    def test_compare_approaches_space_savings(self, ed):
        """Test that optimized approach uses less space."""
        comparison = ed.compare_approaches("kitten", "sitting", iterations=1)
        assert comparison["optimized"]["space_used"] < comparison["dp"]["space_used"]
        assert "space_savings_percent" in comparison

    def test_generate_report_success(self, ed, temp_dir):
        """Test report generation."""
        comparison = ed.compare_approaches("kitten", "sitting")
        report_path = temp_dir / "report.txt"

        report = ed.generate_report(comparison, output_path=str(report_path))

        assert "EDIT DISTANCE" in report
        assert "STANDARD DYNAMIC PROGRAMMING" in report
        assert "SPACE-OPTIMIZED" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, ed):
        """Test report generation without saving to file."""
        comparison = ed.compare_approaches("kitten", "sitting")
        report = ed.generate_report(comparison)

        assert "EDIT DISTANCE" in report
        assert "STANDARD DYNAMIC PROGRAMMING" in report
        assert "SPACE-OPTIMIZED" in report

    def test_long_strings(self, ed):
        """Test with longer strings."""
        str1 = "abcdefghij" * 10
        str2 = "abcdefghij" * 10
        distance_dp, _ = ed.calculate_dp(str1, str2)
        distance_opt, _ = ed.calculate_optimized(str1, str2)
        assert distance_dp == 0
        assert distance_opt == 0

    def test_very_different_strings(self, ed):
        """Test with very different strings."""
        distance_dp, _ = ed.calculate_dp("abc", "xyz")
        distance_opt, _ = ed.calculate_optimized("abc", "xyz")
        assert distance_dp == 3
        assert distance_opt == 3

    def test_substring_case(self, ed):
        """Test with one string being substring of another."""
        distance_dp, _ = ed.calculate_dp("abc", "abcdef")
        distance_opt, _ = ed.calculate_optimized("abc", "abcdef")
        assert distance_dp == 3
        assert distance_opt == 3

    def test_unicode_characters(self, ed):
        """Test with unicode characters."""
        distance_dp, _ = ed.calculate_dp("café", "cafe")
        distance_opt, _ = ed.calculate_optimized("café", "cafe")
        assert distance_dp == distance_opt

    def test_special_characters(self, ed):
        """Test with special characters."""
        distance_dp, _ = ed.calculate_dp("a!@#", "a!@$")
        distance_opt, _ = ed.calculate_optimized("a!@#", "a!@$")
        assert distance_dp == 1
        assert distance_opt == 1

    def test_reversed_strings(self, ed):
        """Test with reversed strings."""
        str1 = "abc"
        str2 = "cba"
        distance_dp, _ = ed.calculate_dp(str1, str2)
        distance_opt, _ = ed.calculate_optimized(str1, str2)
        assert distance_dp == 2
        assert distance_opt == 2

    def test_single_character_difference(self, ed):
        """Test with single character difference."""
        distance_dp, _ = ed.calculate_dp("hello", "hallo")
        distance_opt, _ = ed.calculate_optimized("hello", "hallo")
        assert distance_dp == 1
        assert distance_opt == 1

    def test_operations_accuracy(self, ed):
        """Test that operations sum to distance."""
        test_cases = [
            ("kitten", "sitting"),
            ("hello", "hallo"),
            ("abc", "def"),
        ]
        for str1, str2 in test_cases:
            distance, dp_table = ed.calculate_dp(str1, str2)
            operations = ed.get_operations(str1, str2, dp_table)
            assert len(operations) == distance
