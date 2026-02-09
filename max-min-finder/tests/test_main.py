"""Unit tests for max-min finder module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import MaxMinFinder


class TestMaxMinFinder:
    """Test cases for MaxMinFinder class."""

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
        """Create MaxMinFinder instance."""
        return MaxMinFinder(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {"logging": {"level": "INFO"}}
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        finder = MaxMinFinder(config_path=str(config_path))
        assert finder.config["logging"]["level"] == "INFO"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            MaxMinFinder(config_path="nonexistent.yaml")

    def test_find_max_min_single_element(self, finder):
        """Test finding max/min in single element array."""
        min_val, max_val = finder.find_max_min([5])
        assert min_val == 5
        assert max_val == 5

    def test_find_max_min_two_elements(self, finder):
        """Test finding max/min in two element array."""
        min_val, max_val = finder.find_max_min([3, 7])
        assert min_val == 3
        assert max_val == 7

    def test_find_max_min_unsorted_array(self, finder):
        """Test finding max/min in unsorted array."""
        min_val, max_val = finder.find_max_min([64, 34, 25, 12, 22, 11, 90])
        assert min_val == 11
        assert max_val == 90

    def test_find_max_min_sorted_ascending(self, finder):
        """Test finding max/min in ascending sorted array."""
        min_val, max_val = finder.find_max_min([1, 2, 3, 4, 5])
        assert min_val == 1
        assert max_val == 5

    def test_find_max_min_sorted_descending(self, finder):
        """Test finding max/min in descending sorted array."""
        min_val, max_val = finder.find_max_min([5, 4, 3, 2, 1])
        assert min_val == 1
        assert max_val == 5

    def test_find_max_min_with_duplicates(self, finder):
        """Test finding max/min with duplicate values."""
        min_val, max_val = finder.find_max_min([3, 1, 3, 2, 1])
        assert min_val == 1
        assert max_val == 3

    def test_find_max_min_negative_numbers(self, finder):
        """Test finding max/min with negative numbers."""
        min_val, max_val = finder.find_max_min([-5, 3, -1, 0, 2])
        assert min_val == -5
        assert max_val == 3

    def test_find_max_min_float_numbers(self, finder):
        """Test finding max/min with floating point numbers."""
        min_val, max_val = finder.find_max_min([3.5, 1.2, 4.8, 2.1])
        assert min_val == 1.2
        assert max_val == 4.8

    def test_find_max_min_all_same(self, finder):
        """Test finding max/min when all elements are same."""
        min_val, max_val = finder.find_max_min([5, 5, 5, 5])
        assert min_val == 5
        assert max_val == 5

    def test_find_max_min_empty_array(self, finder):
        """Test ValueError when array is empty."""
        with pytest.raises(ValueError, match="empty array"):
            finder.find_max_min([])

    def test_comparison_counting(self, finder):
        """Test that comparisons are counted correctly."""
        finder.find_max_min([3, 1, 2, 4])
        assert finder.comparisons > 0

    def test_analysis_data(self, finder):
        """Test that analysis data is populated."""
        finder.find_max_min([3, 1, 2])
        assert "min_value" in finder.analysis_data
        assert "max_value" in finder.analysis_data
        assert "min_index" in finder.analysis_data
        assert "max_index" in finder.analysis_data

    def test_get_analysis(self, finder):
        """Test getting analysis data."""
        finder.find_max_min([3, 1, 2])
        analysis = finder.get_analysis()

        assert "total_comparisons" in analysis
        assert "comparisons_per_element" in analysis
        assert "efficiency_ratio" in analysis

    def test_generate_report(self, finder, temp_dir):
        """Test report generation."""
        finder.find_max_min([3, 1, 2])
        report_path = temp_dir / "report.txt"
        report = finder.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "MAX-MIN FINDER ALGORITHM ANALYSIS REPORT" in report
        assert "Minimum value" in report
        assert "Maximum value" in report

    def test_generate_report_no_data(self, finder):
        """Test report generation without analysis data."""
        report = finder.generate_report()
        assert "No analysis data available" in report
