"""Unit tests for palindrome checker module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import PalindromeChecker


class TestPalindromeChecker:
    """Test cases for PalindromeChecker class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "options": {
                "case_sensitive": False,
                "ignore_spaces": False,
                "ignore_punctuation": False,
            },
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def checker(self, config_file):
        """Create PalindromeChecker instance."""
        return PalindromeChecker(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "options": {"case_sensitive": True},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        checker = PalindromeChecker(config_path=str(config_path))
        assert checker.config["options"]["case_sensitive"] is True

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            PalindromeChecker(config_path="nonexistent.yaml")

    def test_is_palindrome_two_pointer_simple(self, checker):
        """Test two-pointer with simple palindrome."""
        assert checker.is_palindrome_two_pointer("racecar") is True

    def test_is_palindrome_two_pointer_not_palindrome(self, checker):
        """Test two-pointer with non-palindrome."""
        assert checker.is_palindrome_two_pointer("hello") is False

    def test_is_palindrome_two_pointer_single_char(self, checker):
        """Test two-pointer with single character."""
        assert checker.is_palindrome_two_pointer("a") is True

    def test_is_palindrome_two_pointer_empty(self, checker):
        """Test two-pointer with empty string."""
        assert checker.is_palindrome_two_pointer("") is True

    def test_is_palindrome_two_pointer_case_insensitive(self, checker):
        """Test two-pointer with case-insensitive checking."""
        assert checker.is_palindrome_two_pointer("RaceCar") is True

    def test_is_palindrome_reverse_simple(self, checker):
        """Test reverse comparison with simple palindrome."""
        assert checker.is_palindrome_reverse("racecar") is True

    def test_is_palindrome_reverse_not_palindrome(self, checker):
        """Test reverse comparison with non-palindrome."""
        assert checker.is_palindrome_reverse("hello") is False

    def test_is_palindrome_reverse_single_char(self, checker):
        """Test reverse comparison with single character."""
        assert checker.is_palindrome_reverse("a") is True

    def test_is_palindrome_reverse_empty(self, checker):
        """Test reverse comparison with empty string."""
        assert checker.is_palindrome_reverse("") is True

    def test_is_palindrome_reverse_case_insensitive(self, checker):
        """Test reverse comparison with case-insensitive checking."""
        assert checker.is_palindrome_reverse("RaceCar") is True

    def test_is_palindrome_stack_simple(self, checker):
        """Test stack-based with simple palindrome."""
        assert checker.is_palindrome_stack("racecar") is True

    def test_is_palindrome_stack_not_palindrome(self, checker):
        """Test stack-based with non-palindrome."""
        assert checker.is_palindrome_stack("hello") is False

    def test_is_palindrome_stack_single_char(self, checker):
        """Test stack-based with single character."""
        assert checker.is_palindrome_stack("a") is True

    def test_is_palindrome_stack_empty(self, checker):
        """Test stack-based with empty string."""
        assert checker.is_palindrome_stack("") is True

    def test_is_palindrome_stack_case_insensitive(self, checker):
        """Test stack-based with case-insensitive checking."""
        assert checker.is_palindrome_stack("RaceCar") is True

    def test_all_methods_same_result(self, checker):
        """Test that all methods produce same result."""
        test_cases = ["racecar", "hello", "a", "", "RaceCar", "madam"]

        for text in test_cases:
            two_pointer = checker.is_palindrome_two_pointer(text)
            reverse = checker.is_palindrome_reverse(text)
            stack = checker.is_palindrome_stack(text)

            assert two_pointer == reverse == stack, f"Failed for: {text}"

    def test_compare_algorithms(self, checker):
        """Test performance comparison."""
        comparison = checker.compare_algorithms("racecar")

        assert "text" in comparison
        assert "two_pointer" in comparison
        assert "reverse" in comparison
        assert "stack" in comparison

        assert comparison["two_pointer"]["success"] is True
        assert comparison["reverse"]["success"] is True
        assert comparison["stack"]["success"] is True

        assert (
            comparison["two_pointer"]["result"]
            == comparison["reverse"]["result"]
            == comparison["stack"]["result"]
        )

    def test_compare_algorithms_multiple_iterations(self, checker):
        """Test performance comparison with multiple iterations."""
        comparison = checker.compare_algorithms("racecar", iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            method.get("success", False)
            for method in [
                comparison["two_pointer"],
                comparison["reverse"],
                comparison["stack"],
            ]
        )

    def test_generate_report(self, checker, temp_dir):
        """Test report generation."""
        comparison = checker.compare_algorithms("racecar")
        report_path = temp_dir / "report.txt"
        report = checker.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "PALINDROME CHECK PERFORMANCE COMPARISON REPORT" in report
        assert "Two-Pointer Method" in report
        assert "Reverse Comparison Method" in report
        assert "Stack-Based Method" in report

    def test_normalize_string_ignore_spaces(self, temp_dir):
        """Test string normalization with ignore_spaces."""
        config = {
            "options": {
                "case_sensitive": False,
                "ignore_spaces": True,
                "ignore_punctuation": False,
            },
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        checker = PalindromeChecker(config_path=str(config_path))
        assert checker.is_palindrome_two_pointer("race car") is True

    def test_normalize_string_ignore_punctuation(self, temp_dir):
        """Test string normalization with ignore_punctuation."""
        config = {
            "options": {
                "case_sensitive": False,
                "ignore_spaces": False,
                "ignore_punctuation": True,
            },
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        checker = PalindromeChecker(config_path=str(config_path))
        assert checker.is_palindrome_two_pointer("race,car!") is True
