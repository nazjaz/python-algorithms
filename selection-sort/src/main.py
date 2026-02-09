"""Selection Sort Algorithm - Detailed logging implementation.

This module provides functionality to sort arrays using selection sort algorithm
with detailed logging of minimum element selection and swap operations.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class SelectionSort:
    """Implements selection sort algorithm with detailed logging."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize SelectionSort with configuration.

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
        self.iterations = []

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

    def _find_minimum(
        self, array: List[float], start_index: int
    ) -> Tuple[int, int]:
        """Find minimum element in array starting from given index.

        Args:
            array: Array to search.
            start_index: Starting index for search.

        Returns:
            Tuple of (minimum_index, comparisons_made).
        """
        min_index = start_index
        comparisons = 0

        logger.info(
            f"Finding minimum element starting from index {start_index} "
            f"(value: {array[start_index]})"
        )

        for i in range(start_index + 1, len(array)):
            comparisons += 1
            self.comparisons += 1

            logger.debug(
                f"  Comparison {comparisons}: array[{i}]={array[i]} vs "
                f"array[{min_index}]={array[min_index]}"
            )

            if array[i] < array[min_index]:
                logger.debug(
                    f"  New minimum found: array[{i}]={array[i]} "
                    f"(was array[{min_index}]={array[min_index]})"
                )
                min_index = i

        logger.info(
            f"Minimum element found at index {min_index} "
            f"(value: {array[min_index]}) after {comparisons} comparisons"
        )

        return min_index, comparisons

    def sort(self, array: List[float]) -> List[float]:
        """Sort array using selection sort algorithm.

        Args:
            array: Array to sort (will be copied, original not modified).

        Returns:
            Sorted array.
        """
        if not array:
            logger.warning("Empty array provided")
            return []

        if len(array) == 1:
            logger.info("Single element array, already sorted")
            return array.copy()

        # Reset statistics
        self.comparisons = 0
        self.swaps = 0
        self.iterations = []

        arr = array.copy()
        n = len(arr)

        logger.info(f"Starting selection sort on array of length {n}")
        logger.info(f"Initial array: {arr}")

        for i in range(n - 1):
            iteration_data = {
                "iteration": i + 1,
                "array_state": arr.copy(),
                "current_index": i,
                "comparisons_before": self.comparisons,
                "swaps_before": self.swaps,
            }

            logger.info(f"\n--- Iteration {i + 1} ---")
            logger.info(f"Current position: index {i} (value: {arr[i]})")

            # Find minimum element in remaining unsorted portion
            min_index, comps = self._find_minimum(arr, i)

            iteration_data["min_index"] = min_index
            iteration_data["min_value"] = arr[min_index]
            iteration_data["comparisons_for_min"] = comps

            # Swap if minimum is not at current position
            if min_index != i:
                logger.info(
                    f"Swapping array[{i}]={arr[i]} with "
                    f"array[{min_index}]={arr[min_index]}"
                )

                arr[i], arr[min_index] = arr[min_index], arr[i]
                self.swaps += 1

                logger.info(
                    f"After swap: array[{i}]={arr[i]}, "
                    f"array[{min_index}]={arr[min_index]}"
                )
                logger.info(f"Array state: {arr}")
            else:
                logger.info(
                    f"No swap needed: minimum element already at position {i}"
                )

            iteration_data["array_state_after"] = arr.copy()
            iteration_data["comparisons_after"] = self.comparisons
            iteration_data["swaps_after"] = self.swaps
            iteration_data["swapped"] = min_index != i

            self.iterations.append(iteration_data)

        logger.info(f"\n--- Sorting Complete ---")
        logger.info(f"Final sorted array: {arr}")
        logger.info(f"Total comparisons: {self.comparisons}")
        logger.info(f"Total swaps: {self.swaps}")

        return arr

    def get_statistics(self) -> Dict[str, any]:
        """Get sorting statistics.

        Returns:
            Dictionary containing sorting statistics.
        """
        return {
            "comparisons": self.comparisons,
            "swaps": self.swaps,
            "iterations": len(self.iterations),
            "iteration_details": self.iterations,
        }

    def generate_report(
        self, original: List[float], sorted_array: List[float],
        output_path: Optional[str] = None
    ) -> str:
        """Generate detailed sorting report.

        Args:
            original: Original unsorted array.
            sorted_array: Sorted array.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        stats = self.get_statistics()

        report_lines = [
            "=" * 80,
            "SELECTION SORT ALGORITHM REPORT",
            "=" * 80,
            "",
            f"Original array: {original}",
            f"Sorted array: {sorted_array}",
            f"Array length: {len(original)}",
            "",
            "STATISTICS",
            "-" * 80,
            f"Total comparisons: {stats['comparisons']}",
            f"Total swaps: {stats['swaps']}",
            f"Total iterations: {stats['iterations']}",
            "",
            "ITERATION DETAILS",
            "-" * 80,
        ]

        for iter_data in stats["iteration_details"]:
            report_lines.extend([
                f"\nIteration {iter_data['iteration']}:",
                f"  Current position: index {iter_data['current_index']} "
                f"(value: {iter_data['array_state'][iter_data['current_index']]})",
                f"  Minimum found: index {iter_data['min_index']} "
                f"(value: {iter_data['min_value']})",
                f"  Comparisons for minimum: {iter_data['comparisons_for_min']}",
                f"  Swap performed: {'Yes' if iter_data['swapped'] else 'No'}",
                f"  Array before: {iter_data['array_state']}",
                f"  Array after: {iter_data['array_state_after']}",
            ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(n²) - nested loops",
            "Space Complexity: O(1) - in-place sorting",
            "Best Case: O(n²) - still requires full scan",
            "Worst Case: O(n²) - same as average",
            "Average Case: O(n²)",
        ])

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


def main() -> None:
    """Main entry point for the script."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sort array using selection sort algorithm with detailed logging"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers to sort",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for sorting report",
    )

    args = parser.parse_args()

    try:
        sorter = SelectionSort(config_path=args.config)

        original = args.numbers
        logger.info(f"Input array: {original}")

        sorted_array = sorter.sort(original)

        print(f"\nOriginal array: {original}")
        print(f"Sorted array: {sorted_array}")

        stats = sorter.get_statistics()
        print(f"\nStatistics:")
        print(f"  Comparisons: {stats['comparisons']}")
        print(f"  Swaps: {stats['swaps']}")
        print(f"  Iterations: {stats['iterations']}")

        if args.report:
            report = sorter.generate_report(
                original, sorted_array, output_path=args.report
            )
            print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
