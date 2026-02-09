"""Insertion Sort Algorithm - Visualization and comparison implementation.

This module provides functionality to sort arrays using insertion sort algorithm
with visualization capabilities and comparison with other sorting algorithms.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class InsertionSort:
    """Implements insertion sort algorithm with visualization and comparison."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize InsertionSort with configuration.

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
        self.visualization_data = []

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

    def sort(self, array: List[float], enable_visualization: bool = False) -> List[float]:
        """Sort array using insertion sort algorithm.

        Args:
            array: Array to sort (will be copied, original not modified).
            enable_visualization: Whether to collect data for visualization.

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
        self.visualization_data = []

        arr = array.copy()
        n = len(arr)

        logger.info(f"Starting insertion sort on array of length {n}")
        logger.info(f"Initial array: {arr}")

        if enable_visualization:
            self.visualization_data.append(arr.copy())

        for i in range(1, n):
            iteration_data = {
                "iteration": i,
                "array_state": arr.copy(),
                "current_index": i,
                "current_value": arr[i],
                "comparisons_before": self.comparisons,
                "swaps_before": self.swaps,
            }

            logger.info(f"\n--- Iteration {i} ---")
            logger.info(f"Processing element at index {i}: {arr[i]}")

            key = arr[i]
            j = i - 1

            # Move elements greater than key one position ahead
            while j >= 0 and arr[j] > key:
                self.comparisons += 1
                logger.debug(
                    f"  Comparison: array[{j}]={arr[j]} > key={key}, "
                    f"shifting array[{j}] to position {j+1}"
                )

                arr[j + 1] = arr[j]
                self.swaps += 1
                j -= 1

                if enable_visualization:
                    self.visualization_data.append(arr.copy())

            # Insert key at correct position
            if j + 1 != i:
                logger.info(
                    f"Inserting {key} at position {j + 1} "
                    f"(was at position {i})"
                )
                arr[j + 1] = key
                self.swaps += 1
            else:
                logger.info(f"Element {key} already in correct position")

            iteration_data["array_state_after"] = arr.copy()
            iteration_data["comparisons_after"] = self.comparisons
            iteration_data["swaps_after"] = self.swaps
            iteration_data["insertion_position"] = j + 1

            self.iterations.append(iteration_data)

            if enable_visualization:
                self.visualization_data.append(arr.copy())

        logger.info(f"\n--- Sorting Complete ---")
        logger.info(f"Final sorted array: {arr}")
        logger.info(f"Total comparisons: {self.comparisons}")
        logger.info(f"Total swaps: {self.swaps}")

        if enable_visualization:
            self.visualization_data.append(arr.copy())

        return arr

    def bubble_sort(self, array: List[float]) -> Tuple[List[float], Dict[str, int]]:
        """Sort array using bubble sort for comparison.

        Args:
            array: Array to sort.

        Returns:
            Tuple of (sorted_array, statistics_dict).
        """
        arr = array.copy()
        n = len(arr)
        comparisons = 0
        swaps = 0

        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1

        return arr, {"comparisons": comparisons, "swaps": swaps}

    def selection_sort(self, array: List[float]) -> Tuple[List[float], Dict[str, int]]:
        """Sort array using selection sort for comparison.

        Args:
            array: Array to sort.

        Returns:
            Tuple of (sorted_array, statistics_dict).
        """
        arr = array.copy()
        n = len(arr)
        comparisons = 0
        swaps = 0

        for i in range(n - 1):
            min_idx = i
            for j in range(i + 1, n):
                comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j

            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1

        return arr, {"comparisons": comparisons, "swaps": swaps}

    def compare_algorithms(
        self, array: List[float], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of insertion sort with other sorting algorithms.

        Args:
            array: Array to sort.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing sorting algorithms for array of length {len(array)}"
        )

        results = {
            "array_length": len(array),
            "iterations": iterations,
            "insertion_sort": {},
            "bubble_sort": {},
            "selection_sort": {},
        }

        # Insertion sort
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                insertion_result = self.sort(array.copy())
            insertion_time = time.perf_counter() - start_time

            results["insertion_sort"] = {
                "result": insertion_result,
                "time_seconds": insertion_time / iterations,
                "time_milliseconds": (insertion_time / iterations) * 1000,
                "comparisons": self.comparisons,
                "swaps": self.swaps,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Insertion sort failed: {e}")
            results["insertion_sort"] = {"success": False, "error": str(e)}

        # Bubble sort
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                bubble_result, bubble_stats = self.bubble_sort(array.copy())
            bubble_time = time.perf_counter() - start_time

            results["bubble_sort"] = {
                "result": bubble_result,
                "time_seconds": bubble_time / iterations,
                "time_milliseconds": (bubble_time / iterations) * 1000,
                "comparisons": bubble_stats["comparisons"],
                "swaps": bubble_stats["swaps"],
                "success": True,
            }
        except Exception as e:
            logger.error(f"Bubble sort failed: {e}")
            results["bubble_sort"] = {"success": False, "error": str(e)}

        # Selection sort
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                selection_result, selection_stats = self.selection_sort(array.copy())
            selection_time = time.perf_counter() - start_time

            results["selection_sort"] = {
                "result": selection_result,
                "time_seconds": selection_time / iterations,
                "time_milliseconds": (selection_time / iterations) * 1000,
                "comparisons": selection_stats["comparisons"],
                "swaps": selection_stats["swaps"],
                "success": True,
            }
        except Exception as e:
            logger.error(f"Selection sort failed: {e}")
            results["selection_sort"] = {"success": False, "error": str(e)}

        # Verify all results match
        successful_results = [
            (name, data)
            for name, data in [
                ("insertion_sort", results["insertion_sort"]),
                ("bubble_sort", results["bubble_sort"]),
                ("selection_sort", results["selection_sort"]),
            ]
            if data.get("success", False)
        ]

        if len(successful_results) > 1:
            first_result = successful_results[0][1]["result"]
            all_match = all(
                data["result"] == first_result for _, data in successful_results
            )
            if all_match:
                logger.info("All algorithms produced identical results")
            else:
                logger.warning("Results differ between algorithms!")

        # Determine fastest
        if successful_results:
            fastest = min(successful_results, key=lambda x: x[1]["time_seconds"])
            results["fastest"] = fastest[0]
            results["fastest_time"] = fastest[1]["time_seconds"]

        return results

    def visualize_sorting(
        self, array: List[float], output_path: Optional[str] = None
    ) -> None:
        """Create visualization of insertion sort process.

        Args:
            array: Array to sort and visualize.
            output_path: Optional path to save visualization.

        Raises:
            ImportError: If matplotlib is not available.
        """
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError(
                "matplotlib is required for visualization. "
                "Install it with: pip install matplotlib"
            )

        logger.info("Creating visualization of insertion sort process")
        self.sort(array.copy(), enable_visualization=True)

        if not self.visualization_data:
            logger.warning("No visualization data collected")
            return

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_title("Insertion Sort Visualization", fontsize=14, fontweight="bold")
        ax.set_xlabel("Array Index", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)

        # Create initial bar chart
        bars = ax.bar(
            range(len(self.visualization_data[0])),
            self.visualization_data[0],
            color="lightblue",
        )

        def animate(frame):
            """Update animation frame."""
            if frame < len(self.visualization_data):
                ax.clear()
                ax.set_title(
                    f"Insertion Sort - Step {frame + 1}/{len(self.visualization_data)}",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.set_xlabel("Array Index", fontsize=12)
                ax.set_ylabel("Value", fontsize=12)

                data = self.visualization_data[frame]
                colors = ["lightblue"] * len(data)

                # Highlight sorted portion
                if frame > 0:
                    prev_data = self.visualization_data[frame - 1]
                    for i in range(len(data)):
                        if i < len(prev_data) and data[i] != prev_data[i]:
                            colors[i] = "green"
                        elif i < len(prev_data) and data[i] == prev_data[i]:
                            # Check if this position is in sorted order
                            is_sorted = True
                            for j in range(i):
                                if data[j] > data[i]:
                                    is_sorted = False
                                    break
                            if is_sorted:
                                colors[i] = "lightgreen"

                ax.bar(range(len(data)), data, color=colors)
                ax.set_ylim(0, max(data) * 1.1 if data else 1)

        anim = animation.FuncAnimation(
            fig, animate, frames=len(self.visualization_data), interval=500, repeat=True
        )

        if output_path:
            try:
                anim.save(output_path, writer="pillow", fps=2)
                logger.info(f"Visualization saved to {output_path}")
            except Exception as e:
                logger.error(f"Failed to save visualization: {e}")
        else:
            plt.show()

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
        comparison_data: Optional[Dict[str, any]] = None,
        output_path: Optional[str] = None
    ) -> str:
        """Generate detailed sorting report.

        Args:
            original: Original unsorted array.
            sorted_array: Sorted array.
            comparison_data: Optional comparison data from compare_algorithms().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        stats = self.get_statistics()

        report_lines = [
            "=" * 80,
            "INSERTION SORT ALGORITHM REPORT",
            "=" * 80,
            "",
            f"Original array: {original}",
            f"Sorted array: {sorted_array}",
            f"Array length: {len(original)}",
            "",
            "INSERTION SORT STATISTICS",
            "-" * 80,
            f"Total comparisons: {stats['comparisons']}",
            f"Total swaps: {stats['swaps']}",
            f"Total iterations: {stats['iterations']}",
        ]

        if comparison_data:
            report_lines.extend([
                "",
                "ALGORITHM COMPARISON",
                "-" * 80,
            ])

            algorithms = [
                ("insertion_sort", "Insertion Sort"),
                ("bubble_sort", "Bubble Sort"),
                ("selection_sort", "Selection Sort"),
            ]

            for algo_key, algo_name in algorithms:
                if algo_key in comparison_data:
                    data = comparison_data[algo_key]
                    if data.get("success", False):
                        report_lines.extend([
                            f"\n{algo_name}:",
                            f"  Time: {data['time_milliseconds']:.4f} ms",
                            f"  Comparisons: {data['comparisons']}",
                            f"  Swaps: {data['swaps']}",
                        ])

            if "fastest" in comparison_data:
                report_lines.extend([
                    "",
                    f"Fastest algorithm: {comparison_data['fastest']}",
                    f"Fastest time: {comparison_data['fastest_time']*1000:.4f} ms",
                ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity:",
            "  Best Case: O(n) - already sorted",
            "  Average Case: O(n²)",
            "  Worst Case: O(n²) - reverse sorted",
            "Space Complexity: O(1) - in-place sorting",
            "",
            "Characteristics:",
            "  - Stable sorting algorithm",
            "  - Adaptive (efficient for nearly sorted arrays)",
            "  - In-place sorting",
            "  - Simple to implement",
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
        description="Sort array using insertion sort with visualization and comparison"
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
        "-v",
        "--visualize",
        action="store_true",
        help="Create visualization of sorting process",
    )
    parser.add_argument(
        "--visualization-output",
        help="Output path for visualization (GIF file)",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare with other sorting algorithms",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=1,
        help="Number of iterations for timing (default: 1)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for sorting report",
    )

    args = parser.parse_args()

    try:
        sorter = InsertionSort(config_path=args.config)

        original = args.numbers
        logger.info(f"Input array: {original}")

        if args.visualize:
            if args.visualization_output:
                sorter.visualize_sorting(
                    original, output_path=args.visualization_output
                )
            else:
                sorter.visualize_sorting(original)
        else:
            sorted_array = sorter.sort(original)

            print(f"\nOriginal array: {original}")
            print(f"Sorted array: {sorted_array}")

            stats = sorter.get_statistics()
            print(f"\nStatistics:")
            print(f"  Comparisons: {stats['comparisons']}")
            print(f"  Swaps: {stats['swaps']}")
            print(f"  Iterations: {stats['iterations']}")

            comparison_data = None
            if args.compare:
                comparison = sorter.compare_algorithms(original, args.iterations)
                comparison_data = comparison

                print(f"\nAlgorithm Comparison:")
                print("-" * 60)

                algorithms = [
                    ("insertion_sort", "Insertion Sort"),
                    ("bubble_sort", "Bubble Sort"),
                    ("selection_sort", "Selection Sort"),
                ]

                for algo_key, algo_name in algorithms:
                    if algo_key in comparison:
                        data = comparison[algo_key]
                        if data.get("success", False):
                            print(
                                f"{algo_name:20s}: "
                                f"{data['time_milliseconds']:8.4f} ms, "
                                f"{data['comparisons']} comparisons, "
                                f"{data['swaps']} swaps"
                            )

                if "fastest" in comparison:
                    print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = sorter.generate_report(
                    original, sorted_array, comparison_data, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
