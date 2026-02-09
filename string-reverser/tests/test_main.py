"""Unit tests for string reverser module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import StringReverser


class TestStringReverser:
    """Test cases for StringReverser class."""

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
    def reverser(self, config_file):
        """Create StringReverser instance."""
        return StringReverser(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "recursion": {"max_depth": 500},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        reverser = StringReverser(config_path=str(config_path))
        assert reverser.config["recursion"]["max_depth"] == 500

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            StringReverser(config_path="nonexistent.yaml")

    def test_reverse_slicing(self, reverser):
        """Test slicing reversal method."""
        result = reverser.reverse_slicing("hello")
        assert result == "olleh"

    def test_reverse_slicing_empty(self, reverser):
        """Test slicing reversal with empty string."""
        result = reverser.reverse_slicing("")
        assert result == ""

    def test_reverse_slicing_single_char(self, reverser):
        """Test slicing reversal with single character."""
        result = reverser.reverse_slicing("a")
        assert result == "a"

    def test_reverse_loop(self, reverser):
        """Test loop reversal method."""
        result = reverser.reverse_loop("hello")
        assert result == "olleh"

    def test_reverse_loop_empty(self, reverser):
        """Test loop reversal with empty string."""
        result = reverser.reverse_loop("")
        assert result == ""

    def test_reverse_loop_optimized(self, reverser):
        """Test optimized loop reversal method."""
        result = reverser.reverse_loop_optimized("hello")
        assert result == "olleh"

    def test_reverse_loop_optimized_empty(self, reverser):
        """Test optimized loop reversal with empty string."""
        result = reverser.reverse_loop_optimized("")
        assert result == ""

    def test_reverse_recursive(self, reverser):
        """Test recursive reversal method."""
        result = reverser.reverse_recursive("hello")
        assert result == "olleh"

    def test_reverse_recursive_empty(self, reverser):
        """Test recursive reversal with empty string."""
        result = reverser.reverse_recursive("")
        assert result == ""

    def test_reverse_recursive_single_char(self, reverser):
        """Test recursive reversal with single character."""
        result = reverser.reverse_recursive("a")
        assert result == "a"

    def test_reverse_builtin(self, reverser):
        """Test built-in reversal method."""
        result = reverser.reverse_builtin("hello")
        assert result == "olleh"

    def test_reverse_builtin_empty(self, reverser):
        """Test built-in reversal with empty string."""
        result = reverser.reverse_builtin("")
        assert result == ""

    def test_all_methods_same_result(self, reverser):
        """Test that all methods produce same result."""
        text = "Hello World"
        slicing = reverser.reverse_slicing(text)
        loop = reverser.reverse_loop(text)
        loop_opt = reverser.reverse_loop_optimized(text)
        recursive = reverser.reverse_recursive(text)
        builtin = reverser.reverse_builtin(text)

        assert slicing == loop == loop_opt == recursive == builtin

    def test_compare_performance(self, reverser):
        """Test performance comparison."""
        comparison = reverser.compare_performance("hello")

        assert "input_length" in comparison
        assert "slicing" in comparison
        assert "loop" in comparison
        assert "recursive" in comparison
        assert "builtin" in comparison

        assert comparison["slicing"]["success"] is True
        assert comparison["loop"]["success"] is True
        assert comparison["recursive"]["success"] is True

    def test_compare_performance_multiple_iterations(self, reverser):
        """Test performance comparison with multiple iterations."""
        comparison = reverser.compare_performance("test", iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            method.get("success", False)
            for method in [
                comparison["slicing"],
                comparison["loop"],
                comparison["recursive"],
            ]
        )

    def test_generate_report(self, reverser, temp_dir):
        """Test report generation."""
        comparison = reverser.compare_performance("hello")
        report_path = temp_dir / "report.txt"
        report = reverser.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "STRING REVERSAL PERFORMANCE COMPARISON REPORT" in report
        assert "Slicing Method" in report
        assert "Loop Method" in report
