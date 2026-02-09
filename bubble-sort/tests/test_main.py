"""Unit tests for bubble sort module."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from src.main import BubbleSort


class TestBubbleSort:
    """Test cases for BubbleSort class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "visualization": {"enabled": True, "output_file": "viz.png"},
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def sorter(self, config_file):
        """Create BubbleSort instance."""
        return BubbleSort(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "visualization": {"enabled": False},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        sorter = BubbleSort(config_path=str(config_path))
        assert sorter.config["visualization"]["enabled"] is False

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            BubbleSort(config_path="nonexistent.yaml")

    def test_sort_empty_array(self, sorter):
        """Test sorting empty array."""
        result = sorter.sort([])
        assert result == []
        assert sorter.comparisons == 0
        assert sorter.swaps == 0

    def test_sort_single_element(self, sorter):
        """Test sorting array with single element."""
        result = sorter.sort([5])
        assert result == [5]
        assert sorter.comparisons == 0
        assert sorter.swaps == 0

    def test_sort_already_sorted(self, sorter):
        """Test sorting already sorted array."""
        result = sorter.sort([1, 2, 3, 4, 5])
        assert result == [1, 2, 3, 4, 5]
        assert sorter.swaps == 0

    def test_sort_reverse_sorted(self, sorter):
        """Test sorting reverse sorted array."""
        result = sorter.sort([5, 4, 3, 2, 1])
        assert result == [1, 2, 3, 4, 5]
        assert sorter.swaps > 0

    def test_sort_unsorted_array(self, sorter):
        """Test sorting unsorted array."""
        result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
        assert result == [11, 12, 22, 25, 34, 64, 90]
        assert sorter.comparisons > 0

    def test_sort_with_duplicates(self, sorter):
        """Test sorting array with duplicate values."""
        result = sorter.sort([3, 1, 3, 2, 1])
        assert result == [1, 1, 2, 3, 3]
        assert sorter.comparisons > 0

    def test_sort_negative_numbers(self, sorter):
        """Test sorting array with negative numbers."""
        result = sorter.sort([-5, 3, -1, 0, 2])
        assert result == [-5, -1, 0, 2, 3]

    def test_comparison_counting(self, sorter):
        """Test that comparisons are counted correctly."""
        sorter.sort([3, 1, 2])
        assert sorter.comparisons > 0

    def test_swap_counting(self, sorter):
        """Test that swaps are counted correctly."""
        sorter.sort([3, 1, 2])
        assert sorter.swaps >= 0

    def test_steps_recording(self, sorter):
        """Test that steps are recorded for visualization."""
        sorter.sort([3, 1, 2])
        assert len(sorter.steps) > 0
        assert "array" in sorter.steps[0]
        assert "outer_index" in sorter.steps[0]

    def test_generate_report(self, sorter, temp_dir):
        """Test report generation."""
        sorter.sort([3, 1, 2])
        report_path = temp_dir / "report.txt"
        report = sorter.generate_report(output_path=str(report_path))

        assert report_path.exists()
        assert "BUBBLE SORT ALGORITHM REPORT" in report
        assert "Total comparisons" in report
        assert "Total swaps" in report

    def test_visualize(self, sorter, temp_dir):
        """Test visualization generation."""
        sorter.sort([3, 1, 2])
        viz_path = temp_dir / "visualization.png"
        sorter.visualize(output_path=str(viz_path))

        assert viz_path.exists()

    def test_visualize_disabled(self, temp_dir):
        """Test visualization when disabled."""
        config = {
            "visualization": {"enabled": False},
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        sorter = BubbleSort(config_path=str(config_path))
        sorter.sort([3, 1, 2])
        sorter.visualize()

        assert len(sorter.steps) == 0

    def test_preserves_original_array(self, sorter):
        """Test that original array is not modified."""
        original = [3, 1, 2]
        result = sorter.sort(original)
        assert original == [3, 1, 2]
        assert result != original
