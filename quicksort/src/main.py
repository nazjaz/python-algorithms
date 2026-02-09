"""Quick Sort Algorithm - Multiple Pivot Selection Strategies.

This module provides a quicksort implementation with different pivot selection
strategies: first, last, middle, random, and median-of-three. It includes
performance comparison to analyze the impact of pivot selection on sorting
performance.
"""

import argparse
import logging
import logging.handlers
import random
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class QuickSort:
    """Quick sort implementation with multiple pivot selection strategies."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize sorter with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.comparison_count = 0
        self.swap_count = 0

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

    def _pivot_first(self, arr: List[Any], low: int, high: int) -> int:
        """Select first element as pivot.

        Args:
            arr: Array to sort.
            low: Starting index.
            high: Ending index.

        Returns:
            Pivot index.
        """
        return low

    def _pivot_last(self, arr: List[Any], low: int, high: int) -> int:
        """Select last element as pivot.

        Args:
            arr: Array to sort.
            low: Starting index.
            high: Ending index.

        Returns:
            Pivot index.
        """
        return high

    def _pivot_middle(self, arr: List[Any], low: int, high: int) -> int:
        """Select middle element as pivot.

        Args:
            arr: Array to sort.
            low: Starting index.
            high: Ending index.

        Returns:
            Pivot index.
        """
        return (low + high) // 2

    def _pivot_random(self, arr: List[Any], low: int, high: int) -> int:
        """Select random element as pivot.

        Args:
            arr: Array to sort.
            low: Starting index.
            high: Ending index.

        Returns:
            Pivot index.
        """
        return random.randint(low, high)

    def _pivot_median_of_three(
        self, arr: List[Any], low: int, high: int
    ) -> int:
        """Select median of first, middle, and last elements as pivot.

        Args:
            arr: Array to sort.
            low: Starting index.
            high: Ending index.

        Returns:
            Pivot index.
        """
        mid = (low + high) // 2

        # Find median of three
        if arr[low] <= arr[mid] <= arr[high] or arr[high] <= arr[mid] <= arr[low]:
            return mid
        elif arr[mid] <= arr[low] <= arr[high] or arr[high] <= arr[low] <= arr[mid]:
            return low
        else:
            return high

    def _partition(
        self,
        arr: List[Any],
        low: int,
        high: int,
        pivot_func: Callable[[List[Any], int, int], int],
    ) -> int:
        """Partition array around pivot.

        Args:
            arr: Array to partition.
            low: Starting index.
            high: Ending index.
            pivot_func: Function to select pivot.

        Returns:
            Final position of pivot.
        """
        # Select pivot using provided function
        pivot_idx = pivot_func(arr, low, high)

        # Move pivot to end
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        self.swap_count += 1

        pivot_value = arr[high]
        i = low - 1

        # Partition: elements < pivot go to left, >= pivot go to right
        for j in range(low, high):
            self.comparison_count += 1
            if arr[j] < pivot_value:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swap_count += 1

        # Place pivot in correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swap_count += 1

        return i + 1

    def _quicksort_recursive(
        self,
        arr: List[Any],
        low: int,
        high: int,
        pivot_func: Callable[[List[Any], int, int], int],
    ) -> None:
        """Recursively sort array using quicksort.

        Args:
            arr: Array to sort.
            low: Starting index.
            high: Ending index.
            pivot_func: Function to select pivot.
        """
        if low < high:
            # Partition array and get pivot position
            pivot_pos = self._partition(arr, low, high, pivot_func)

            # Recursively sort elements before and after partition
            self._quicksort_recursive(arr, low, pivot_pos - 1, pivot_func)
            self._quicksort_recursive(arr, pivot_pos + 1, high, pivot_func)

    def sort(
        self,
        arr: List[Any],
        pivot_strategy: str = "median_of_three",
        track_stats: bool = False,
    ) -> List[Any]:
        """Sort array using quicksort with specified pivot strategy.

        Args:
            arr: Array to sort.
            pivot_strategy: Pivot selection strategy:
                - 'first': First element
                - 'last': Last element
                - 'middle': Middle element
                - 'random': Random element
                - 'median_of_three': Median of first, middle, last

        Returns:
            Sorted array.

        Raises:
            ValueError: If pivot strategy is invalid.
        """
        logger.info(
            f"Sorting array of length {len(arr)} using pivot strategy: "
            f"{pivot_strategy}"
        )

        if track_stats:
            self.comparison_count = 0
            self.swap_count = 0

        # Create copy to avoid modifying original
        sorted_arr = arr.copy()

        if len(sorted_arr) <= 1:
            return sorted_arr

        # Select pivot function based on strategy
        pivot_functions = {
            "first": self._pivot_first,
            "last": self._pivot_last,
            "middle": self._pivot_middle,
            "random": self._pivot_random,
            "median_of_three": self._pivot_median_of_three,
        }

        if pivot_strategy not in pivot_functions:
            raise ValueError(
                f"Invalid pivot strategy: {pivot_strategy}. "
                f"Must be one of: {list(pivot_functions.keys())}"
            )

        pivot_func = pivot_functions[pivot_strategy]

        # Sort array
        self._quicksort_recursive(sorted_arr, 0, len(sorted_arr) - 1, pivot_func)

        logger.info(f"Sorting complete. Array length: {len(sorted_arr)}")
        return sorted_arr

    def get_stats(self) -> Dict[str, int]:
        """Get sorting statistics.

        Returns:
            Dictionary with comparison and swap counts.
        """
        return {
            "comparisons": self.comparison_count,
            "swaps": self.swap_count,
        }

    def compare_strategies(
        self,
        arr: List[Any],
        strategies: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """Compare performance of different pivot strategies.

        Args:
            arr: Array to sort.
            strategies: List of strategies to compare. If None, compares all.

        Returns:
            Dictionary with performance comparison for each strategy.
        """
        logger.info(f"Comparing pivot strategies for array of length {len(arr)}")

        if strategies is None:
            strategies = [
                "first",
                "last",
                "middle",
                "random",
                "median_of_three",
            ]

        results = {}

        for strategy in strategies:
            logger.info(f"Testing strategy: {strategy}")

            # Reset stats
            self.comparison_count = 0
            self.swap_count = 0

            # Measure execution time
            start_time = time.perf_counter()
            sorted_arr = self.sort(arr, pivot_strategy=strategy, track_stats=True)
            end_time = time.perf_counter()

            execution_time = end_time - start_time
            stats = self.get_stats()

            # Verify sorting correctness
            is_sorted = sorted_arr == sorted(arr)

            results[strategy] = {
                "execution_time": execution_time,
                "comparisons": stats["comparisons"],
                "swaps": stats["swaps"],
                "is_sorted": is_sorted,
                "result": sorted_arr,
            }

            logger.info(
                f"Strategy {strategy}: {execution_time:.10f}s, "
                f"{stats['comparisons']} comparisons, {stats['swaps']} swaps"
            )

        return results

    def generate_report(
        self,
        comparison_results: Dict[str, Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance comparison report.

        Args:
            comparison_results: Results from compare_strategies.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "QUICKSORT PIVOT STRATEGY COMPARISON REPORT",
            "=" * 80,
            "",
            "PERFORMANCE COMPARISON",
            "-" * 80,
        ]

        # Sort strategies by execution time
        sorted_strategies = sorted(
            comparison_results.items(),
            key=lambda x: x[1]["execution_time"],
        )

        for strategy, result in sorted_strategies:
            report_lines.append(f"\nStrategy: {strategy.upper()}")
            report_lines.append(f"  Execution Time: {result['execution_time']:.10f} seconds")
            report_lines.append(f"  Comparisons: {result['comparisons']}")
            report_lines.append(f"  Swaps: {result['swaps']}")
            report_lines.append(f"  Correctly Sorted: {result['is_sorted']}")

        # Find best strategy
        best_strategy = sorted_strategies[0][0]
        best_time = sorted_strategies[0][1]["execution_time"]

        report_lines.extend([
            "",
            "BEST STRATEGY",
            "-" * 80,
            f"Fastest: {best_strategy.upper()} ({best_time:.10f} seconds)",
            "",
            "ALGORITHM DETAILS",
            "-" * 80,
            "Algorithm: Quick Sort (Partition-Exchange Sort)",
            "",
            "Pivot Selection Strategies:",
            "  1. FIRST: Select first element as pivot",
            "     - Simple but can lead to O(n²) worst case for sorted arrays",
            "",
            "  2. LAST: Select last element as pivot",
            "     - Similar to first, O(n²) worst case for reverse sorted arrays",
            "",
            "  3. MIDDLE: Select middle element as pivot",
            "     - Better than first/last for some cases",
            "",
            "  4. RANDOM: Select random element as pivot",
            "     - Expected O(n log n) performance",
            "     - Avoids worst case for most inputs",
            "",
            "  5. MEDIAN_OF_THREE: Select median of first, middle, last",
            "     - Good balance between simplicity and performance",
            "     - Reduces chance of worst case",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity:",
            "  - Best Case: O(n log n) - balanced partitions",
            "  - Average Case: O(n log n) - random pivot",
            "  - Worst Case: O(n²) - unbalanced partitions (first/last on sorted)",
            "",
            "Space Complexity:",
            "  - Best Case: O(log n) - balanced recursion stack",
            "  - Average Case: O(log n)",
            "  - Worst Case: O(n) - unbalanced recursion stack",
            "",
            "PROPERTIES",
            "-" * 80,
            "- In-place sorting (with some modifications)",
            "- Not stable (relative order of equal elements may change)",
            "- Divide and conquer algorithm",
            "- Pivot selection significantly affects performance",
            "",
            "PIVOT STRATEGY ANALYSIS",
            "-" * 80,
            "First/Last:",
            "  - Simple but poor performance on sorted/reverse-sorted arrays",
            "  - Worst case: O(n²) time",
            "",
            "Middle:",
            "  - Better than first/last for many cases",
            "  - Still can have worst case scenarios",
            "",
            "Random:",
            "  - Expected O(n log n) performance",
            "  - Avoids worst case with high probability",
            "  - Requires random number generation",
            "",
            "Median of Three:",
            "  - Good practical performance",
            "  - Reduces worst case probability",
            "  - No random number generation needed",
            "  - Often best choice for general-purpose sorting",
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
    parser = argparse.ArgumentParser(
        description="Quick sort with multiple pivot selection strategies"
    )
    parser.add_argument(
        "numbers",
        type=float,
        nargs="*",
        help="Numbers to sort (space-separated)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-p",
        "--pivot",
        choices=["first", "last", "middle", "random", "median_of_three"],
        default="median_of_three",
        help="Pivot selection strategy (default: median_of_three)",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare all pivot strategies",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for comparison report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example arrays",
    )

    args = parser.parse_args()

    try:
        sorter = QuickSort(config_path=args.config)

        if args.demo or not args.numbers:
            # Run demonstration
            print("\n=== Quick Sort Demonstration ===\n")

            examples = [
                [64, 34, 25, 12, 22, 11, 90],
                [5, 2, 8, 1, 9],
                [1, 2, 3, 4, 5],  # Already sorted
                [5, 4, 3, 2, 1],  # Reverse sorted
                [3, 1, 4, 1, 5, 9, 2, 6, 5, 3],
            ]

            for example in examples:
                print(f"Original array: {example}")

                if args.compare:
                    results = sorter.compare_strategies(example)
                    print("\nStrategy Comparison:")
                    for strategy, result in sorted(
                        results.items(), key=lambda x: x[1]["execution_time"]
                    ):
                        print(
                            f"  {strategy:15} - "
                            f"{result['execution_time']:.10f}s, "
                            f"{result['comparisons']} comparisons, "
                            f"{result['swaps']} swaps"
                        )
                else:
                    sorted_arr = sorter.sort(example, pivot_strategy=args.pivot)
                    print(f"Sorted array:  {sorted_arr} (pivot: {args.pivot})")

                print()

        else:
            # Sort provided numbers
            numbers = args.numbers

            if args.compare:
                results = sorter.compare_strategies(numbers)
                print("\nStrategy Comparison:")
                for strategy, result in sorted(
                    results.items(), key=lambda x: x[1]["execution_time"]
                ):
                    print(
                        f"{strategy:15} - "
                        f"{result['execution_time']:.10f}s, "
                        f"{result['comparisons']} comparisons, "
                        f"{result['swaps']} swaps"
                    )

                if args.report:
                    report = sorter.generate_report(
                        results, output_path=args.report
                    )
                    print(f"\nReport saved to {args.report}")
            else:
                sorted_arr = sorter.sort(numbers, pivot_strategy=args.pivot)
                print(f"\nOriginal: {numbers}")
                print(f"Sorted:   {sorted_arr} (pivot: {args.pivot})")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
