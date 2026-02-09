"""Bubble Sort Algorithm - Implementation with visualization.

This module provides functionality to implement bubble sort algorithm with
detailed visualization of each swap operation and comparison counting.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BubbleSort:
    """Implements bubble sort algorithm with visualization and statistics."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BubbleSort with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.comparisons = 0
        self.swaps = 0
        self.steps = []
        self.visualization_enabled = self.config.get("visualization", {}).get(
            "enabled", True
        )

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Dictionary containing configuration settings.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            if not config:
                raise ValueError("Configuration file is empty")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in configuration file: {e}")
            raise

    def _setup_logging(self) -> None:
        """Configure logging based on configuration settings."""
        log_level = self.config.get("logging", {}).get("level", "INFO")
        log_file = self.config.get("logging", {}).get("file", "logs/app.log")
        log_format = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(message)s"
        )

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format=log_format,
            handlers=[
                logging.handlers.RotatingFileHandler(
                    log_file, maxBytes=10485760, backupCount=5
                ),
                logging.StreamHandler(),
            ],
        )

    def _record_step(
        self, array: List[int], i: int, j: int, swapped: bool
    ) -> None:
        """Record a sorting step for visualization.

        Args:
            array: Current state of the array.
            i: Outer loop index.
            j: Inner loop index.
            swapped: Whether a swap occurred.
        """
        if self.visualization_enabled:
            self.steps.append(
                {
                    "array": array.copy(),
                    "outer_index": i,
                    "inner_index": j,
                    "swapped": swapped,
                }
            )

    def sort(self, array: List[int]) -> List[int]:
        """Sort array using bubble sort algorithm.

        Args:
            array: List of integers to sort.

        Returns:
            Sorted list of integers.
        """
        if not array:
            logger.warning("Empty array provided")
            return array

        arr = array.copy()
        n = len(arr)
        self.comparisons = 0
        self.swaps = 0
        self.steps = []

        logger.info(f"Starting bubble sort on array of length {n}")

        for i in range(n):
            swapped = False
            logger.debug(f"Outer loop iteration {i + 1}/{n}")

            for j in range(0, n - i - 1):
                self.comparisons += 1
                logger.debug(
                    f"Comparing elements at indices {j} and {j + 1}: "
                    f"{arr[j]} vs {arr[j + 1]}"
                )

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    swapped = True
                    logger.info(
                        f"Swapped elements at indices {j} and {j + 1}: "
                        f"{arr[j + 1]} <-> {arr[j]}"
                    )
                    self._record_step(arr, i, j, True)
                else:
                    self._record_step(arr, i, j, False)

            if not swapped:
                logger.info(
                    f"No swaps in iteration {i + 1}, array is sorted"
                )
                break

        logger.info(
            f"Sorting completed: {self.comparisons} comparisons, "
            f"{self.swaps} swaps"
        )

        return arr

    def _create_visualization(self, output_path: Path) -> None:
        """Create visualization of sorting process.

        Args:
            output_path: Path to save visualization image.
        """
        if not self.steps:
            logger.warning("No steps recorded for visualization")
            return

        num_steps = len(self.steps)
        cols = min(8, num_steps)
        rows = (num_steps + cols - 1) // cols

        fig, axes = plt.subplots(rows, cols, figsize=(16, 2 * rows))
        if rows == 1 and cols == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes
        else:
            axes = axes.flatten()

        for idx, step in enumerate(self.steps):
            ax = axes[idx] if idx < len(axes) else None
            if ax is None:
                break

            arr = step["array"]
            colors = ["red" if i == step["inner_index"] else "lightblue" for i in range(len(arr))]
            if step["swapped"] and step["inner_index"] + 1 < len(arr):
                colors[step["inner_index"] + 1] = "green"

            ax.bar(range(len(arr)), arr, color=colors)
            ax.set_title(f"Step {idx + 1}", fontsize=8)
            ax.set_xticks(range(len(arr)))
            ax.set_xticklabels([str(x) for x in arr], fontsize=6)
            ax.tick_params(labelsize=6)

        for idx in range(len(self.steps), len(axes)):
            axes[idx].axis("off")

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"Visualization saved to {output_path}")

    def generate_report(self, output_path: str = None) -> str:
        """Generate sorting report with statistics.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "BUBBLE SORT ALGORITHM REPORT",
            "=" * 80,
            "",
            "STATISTICS",
            "-" * 80,
            f"Total comparisons: {self.comparisons:,}",
            f"Total swaps: {self.swaps:,}",
            f"Steps recorded: {len(self.steps):,}",
            "",
            "PERFORMANCE ANALYSIS",
            "-" * 80,
            f"Average comparisons per element: "
            f"{self.comparisons / max(1, len(self.steps)):.2f}",
            f"Swap ratio: {self.swaps / max(1, self.comparisons):.2%}",
        ]

        report_content = "\n".join(report_lines)

        if output_path:
            try:
                output_file = Path(output_path)
                output_file.parent.mkdir(parents=True, exist_ok=True)
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(report_content)
                logger.info(f"Report saved to {output_path}")
            except (IOError, PermissionError) as e:
                logger.error(f"Failed to save report: {e}")
                raise

        return report_content

    def visualize(self, output_path: str = None) -> None:
        """Generate visualization of sorting process.

        Args:
            output_path: Optional path to save visualization image.
        """
        if not self.visualization_enabled:
            logger.warning("Visualization is disabled")
            return

        default_output = self.config.get("visualization", {}).get(
            "output_file", "logs/bubble_sort_visualization.png"
        )
        output_file = Path(output_path or default_output)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        self._create_visualization(output_file)


def main() -> None:
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Bubble sort algorithm with visualization"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=int,
        help="Numbers to sort",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Generate visualization",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output path for visualization (overrides config)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for report (overrides config)",
    )

    args = parser.parse_args()

    try:
        sorter = BubbleSort(config_path=args.config)
        sorted_array = sorter.sort(args.numbers)

        print(f"\nOriginal array: {args.numbers}")
        print(f"Sorted array: {sorted_array}")
        print(f"\nComparisons: {sorter.comparisons}")
        print(f"Swaps: {sorter.swaps}")

        if args.visualize or sorter.visualization_enabled:
            sorter.visualize(output_path=args.output)

        report = sorter.generate_report(output_path=args.report)
        if args.report:
            print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
