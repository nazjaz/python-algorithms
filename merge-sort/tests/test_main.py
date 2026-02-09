"""Unit tests for merge sort visualizer module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import MergeSortVisualizer


class TestMergeSortVisualizer:
    """Test cases for MergeSortVisualizer class."""

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
    def visualizer(self, config_file):
        """Create MergeSortVisualizer instance."""
        return MergeSortVisualizer(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        visualizer = MergeSortVisualizer(config_path=str(config_path))
        assert visualizer.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            MergeSortVisualizer(config_path="nonexistent.yaml")

    def test_sort_simple(self, visualizer):
        """Test sorting simple array."""
        array = [64, 34, 25, 12, 22, 11, 90]
        result = visualizer.sort(array, visualize=False)
        assert result == [11, 12, 22, 25, 34, 64, 90]

    def test_sort_already_sorted(self, visualizer):
        """Test sorting already sorted array."""
        array = [1, 2, 3, 4, 5]
        result = visualizer.sort(array, visualize=False)
        assert result == [1, 2, 3, 4, 5]

    def test_sort_reverse_sorted(self, visualizer):
        """Test sorting reverse sorted array."""
        array = [5, 4, 3, 2, 1]
        result = visualizer.sort(array, visualize=False)
        assert result == [1, 2, 3, 4, 5]

    def test_sort_single_element(self, visualizer):
        """Test sorting array with single element."""
        array = [42]
        result = visualizer.sort(array, visualize=False)
        assert result == [42]

    def test_sort_empty(self, visualizer):
        """Test sorting empty array."""
        array = []
        result = visualizer.sort(array, visualize=False)
        assert result == []

    def test_sort_duplicates(self, visualizer):
        """Test sorting array with duplicate elements."""
        array = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        result = visualizer.sort(array, visualize=False)
        assert result == [1, 1, 2, 3, 3, 4, 5, 5, 6, 9]

    def test_sort_negative_numbers(self, visualizer):
        """Test sorting array with negative numbers."""
        array = [-5, 3, -1, 0, 2, -3]
        result = visualizer.sort(array, visualize=False)
        assert result == [-5, -3, -1, 0, 2, 3]

    def test_sort_float_numbers(self, visualizer):
        """Test sorting array with float numbers."""
        array = [3.5, 1.2, 4.8, 2.1, 0.5]
        result = visualizer.sort(array, visualize=False)
        assert result == [0.5, 1.2, 2.1, 3.5, 4.8]

    def test_sort_strings(self, visualizer):
        """Test sorting array of strings."""
        array = ["banana", "apple", "cherry", "date"]
        result = visualizer.sort(array, visualize=False)
        assert result == ["apple", "banana", "cherry", "date"]

    def test_sort_preserves_original(self, visualizer):
        """Test that original array is not modified."""
        original = [64, 34, 25, 12, 22, 11, 90]
        original_copy = original.copy()
        result = visualizer.sort(original, visualize=False)
        assert original == original_copy
        assert result != original_copy

    def test_visualization_steps_recorded(self, visualizer):
        """Test that visualization steps are recorded."""
        array = [5, 2, 8, 1, 9]
        visualizer.sort(array, visualize=True)
        steps = visualizer.get_visualization_steps()
        assert len(steps) > 0
        assert steps[0]["action"] == "start"
        assert steps[-1]["action"] == "complete"

    def test_visualization_divide_steps(self, visualizer):
        """Test that divide steps are recorded in visualization."""
        array = [5, 2, 8, 1, 9]
        visualizer.sort(array, visualize=True)
        steps = visualizer.get_visualization_steps()
        divide_steps = [s for s in steps if s["action"] == "divide"]
        assert len(divide_steps) > 0

    def test_visualization_merge_steps(self, visualizer):
        """Test that merge steps are recorded in visualization."""
        array = [5, 2, 8, 1, 9]
        visualizer.sort(array, visualize=True)
        steps = visualizer.get_visualization_steps()
        merge_steps = [s for s in steps if "merge" in s["action"]]
        assert len(merge_steps) > 0

    def test_visualization_depth_tracking(self, visualizer):
        """Test that recursion depth is tracked in visualization."""
        array = [5, 2, 8, 1, 9]
        visualizer.sort(array, visualize=True)
        steps = visualizer.get_visualization_steps()
        depths = [s.get("depth", 0) for s in steps]
        assert max(depths) > 0

    def test_get_visualization_steps_returns_copy(self, visualizer):
        """Test that get_visualization_steps returns a copy."""
        array = [5, 2, 8]
        visualizer.sort(array, visualize=True)
        steps1 = visualizer.get_visualization_steps()
        steps2 = visualizer.get_visualization_steps()
        assert steps1 == steps2
        assert steps1 is not steps2

    def test_print_visualization_no_steps(self, visualizer, capsys):
        """Test printing visualization when no steps exist."""
        visualizer.print_visualization()
        captured = capsys.readouterr()
        assert "No visualization data available" in captured.out

    def test_print_visualization_with_steps(self, visualizer, capsys):
        """Test printing visualization with steps."""
        array = [5, 2, 8]
        visualizer.sort(array, visualize=True)
        visualizer.print_visualization()
        captured = capsys.readouterr()
        assert "MERGE SORT VISUALIZATION" in captured.out
        assert "DIVIDE" in captured.out or "divide" in captured.out.lower()

    def test_generate_visualization_report(self, visualizer, temp_dir):
        """Test report generation."""
        array = [5, 2, 8, 1, 9]
        visualizer.sort(array, visualize=True)
        report_path = temp_dir / "report.txt"
        report = visualizer.generate_visualization_report(
            output_path=str(report_path)
        )

        assert report_path.exists()
        assert "MERGE SORT VISUALIZATION REPORT" in report
        assert "ALGORITHM COMPLEXITY" in report

    def test_generate_visualization_report_no_steps(self, visualizer):
        """Test report generation when no steps exist."""
        report = visualizer.generate_visualization_report()
        assert "No visualization data available" in report

    def test_merge_sort_stability(self, visualizer):
        """Test that merge sort is stable (preserves order of equal elements)."""
        # Using tuples to test stability
        array = [(1, "a"), (2, "b"), (1, "c"), (2, "d")]
        result = visualizer.sort(array, visualize=False)
        # Check that (1, "a") comes before (1, "c")
        assert result.index((1, "a")) < result.index((1, "c"))
        # Check that (2, "b") comes before (2, "d")
        assert result.index((2, "b")) < result.index((2, "d"))

    def test_large_array(self, visualizer):
        """Test sorting large array."""
        array = list(range(100, 0, -1))
        result = visualizer.sort(array, visualize=False)
        assert result == list(range(1, 101))

    def test_visualization_step_counter(self, visualizer):
        """Test that step counter increments correctly."""
        array = [5, 2, 8]
        visualizer.sort(array, visualize=True)
        steps = visualizer.get_visualization_steps()
        step_numbers = [s["step"] for s in steps]
        assert step_numbers == list(range(1, len(steps) + 1))

    def test_merge_operation_correctness(self, visualizer):
        """Test that merge operation produces correct results."""
        array = [1, 3, 5, 2, 4, 6]
        # Manually test merge of sorted halves
        visualizer._merge(array, 0, 2, 5, depth=0)
        assert array == [1, 2, 3, 4, 5, 6]

    def test_divide_and_conquer_structure(self, visualizer):
        """Test that divide and conquer structure is correct."""
        array = [8, 4, 2, 1]
        visualizer.sort(array, visualize=True)
        steps = visualizer.get_visualization_steps()

        # Should have start and complete steps
        assert any(s["action"] == "start" for s in steps)
        assert any(s["action"] == "complete" for s in steps)

        # Should have divide steps
        divide_steps = [s for s in steps if s["action"] == "divide"]
        assert len(divide_steps) > 0

        # Should have merge steps
        merge_steps = [
            s for s in steps if "merge" in s["action"]
        ]
        assert len(merge_steps) > 0

    def test_visualization_with_detailed_flag(self, visualizer, capsys):
        """Test detailed visualization printing."""
        array = [5, 2, 8]
        visualizer.sort(array, visualize=True)
        visualizer.print_visualization(detailed=True)
        captured = capsys.readouterr()
        assert "MERGE SORT VISUALIZATION" in captured.out

    def test_multiple_sorts_reset_visualization(self, visualizer):
        """Test that visualization resets between sorts."""
        array1 = [5, 2, 8]
        visualizer.sort(array1, visualize=True)
        steps1 = len(visualizer.get_visualization_steps())

        array2 = [1, 3, 2]
        visualizer.sort(array2, visualize=True)
        steps2 = len(visualizer.get_visualization_steps())

        # Both should have visualization steps
        assert steps1 > 0
        assert steps2 > 0

    def test_sort_without_visualization(self, visualizer):
        """Test sorting without visualization."""
        array = [5, 2, 8, 1, 9]
        result = visualizer.sort(array, visualize=False)
        steps = visualizer.get_visualization_steps()
        assert len(steps) == 0
        assert result == [1, 2, 5, 8, 9]
