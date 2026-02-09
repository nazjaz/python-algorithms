"""Kth Largest Element Finder - Heap and Quickselect Algorithms.

This module provides implementations for finding the kth largest element in an
array using two different approaches: heap data structure and quickselect
algorithm. It includes performance comparison to analyze the efficiency of
each method.
"""

import argparse
import heapq
import logging
import logging.handlers
import random
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class KthLargestFinder:
    """Finder for kth largest element using heap and quickselect algorithms."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize finder with configuration.

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

    def find_kth_largest_heap(self, arr: List[Any], k: int) -> Any:
        """Find kth largest element using heap data structure.

        Uses a min-heap of size k to maintain the k largest elements.
        Time complexity: O(n log k) where n is array length.

        Args:
            arr: Array of elements.
            k: Position of largest element to find (1-indexed).

        Returns:
            Kth largest element.

        Raises:
            ValueError: If k is invalid.
            IndexError: If array is too small.

        Example:
            >>> finder = KthLargestFinder()
            >>> finder.find_kth_largest_heap([3, 1, 4, 1, 5, 9, 2, 6], 3)
            5
        """
        logger.info(f"Finding {k}th largest element using heap (array length: {len(arr)})")

        if k < 1:
            raise ValueError("k must be at least 1")
        if k > len(arr):
            raise IndexError(f"k ({k}) cannot be greater than array length ({len(arr)})")
        if not arr:
            raise ValueError("Array cannot be empty")

        # Use min-heap to maintain k largest elements
        # Python's heapq is a min-heap, so we use negative values
        # or maintain a min-heap of size k
        min_heap = []

        for num in arr:
            if len(min_heap) < k:
                # Add to heap if not full
                heapq.heappush(min_heap, num)
            elif num > min_heap[0]:
                # Replace smallest element if current is larger
                heapq.heapreplace(min_heap, num)

        # Root of min-heap is kth largest
        result = min_heap[0]
        logger.info(f"Kth largest element (heap): {result}")
        return result

    def _partition(
        self,
        arr: List[Any],
        low: int,
        high: int,
        pivot_idx: int,
    ) -> int:
        """Partition array around pivot element.

        Args:
            arr: Array to partition.
            low: Starting index.
            high: Ending index.
            pivot_idx: Index of pivot element.

        Returns:
            Final position of pivot after partitioning.
        """
        # Move pivot to end
        pivot_value = arr[pivot_idx]
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        self.swap_count += 1

        # Partition: elements > pivot go to left, <= pivot go to right
        i = low
        for j in range(low, high):
            self.comparison_count += 1
            if arr[j] > pivot_value:
                arr[i], arr[j] = arr[j], arr[i]
                self.swap_count += 1
                i += 1

        # Place pivot in correct position
        arr[i], arr[high] = arr[high], arr[i]
        self.swap_count += 1

        return i

    def _quickselect_recursive(
        self,
        arr: List[Any],
        low: int,
        high: int,
        k: int,
    ) -> Any:
        """Recursively find kth largest element using quickselect.

        Args:
            arr: Array to search.
            low: Starting index.
            high: Ending index.
            k: Position of largest element (1-indexed from left).

        Returns:
            Kth largest element.
        """
        if low == high:
            return arr[low]

        # Select random pivot
        pivot_idx = random.randint(low, high)

        # Partition and get pivot position
        pivot_pos = self._partition(arr, low, high, pivot_idx)

        # k is 1-indexed, pivot_pos is 0-indexed
        # After partitioning, pivot_pos is the position (0-indexed) of the
        # (pivot_pos - low + 1)th largest element in the subarray
        rank = pivot_pos - low + 1

        if rank == k:
            # Found kth largest
            return arr[pivot_pos]
        elif rank > k:
            # kth largest is in left partition
            return self._quickselect_recursive(arr, low, pivot_pos - 1, k)
        else:
            # kth largest is in right partition
            return self._quickselect_recursive(
                arr, pivot_pos + 1, high, k - rank
            )

    def find_kth_largest_quickselect(
        self, arr: List[Any], k: int, track_stats: bool = False
    ) -> Any:
        """Find kth largest element using quickselect algorithm.

        Quickselect is a selection algorithm to find the kth smallest/largest
        element. It's similar to quicksort but only recurses on one side.
        Time complexity: O(n) average case, O(n²) worst case.

        Args:
            arr: Array of elements.
            k: Position of largest element to find (1-indexed).
            track_stats: If True, track comparison and swap counts.

        Returns:
            Kth largest element.

        Raises:
            ValueError: If k is invalid.
            IndexError: If array is too small.

        Example:
            >>> finder = KthLargestFinder()
            >>> finder.find_kth_largest_quickselect([3, 1, 4, 1, 5, 9, 2, 6], 3)
            5
        """
        logger.info(
            f"Finding {k}th largest element using quickselect "
            f"(array length: {len(arr)})"
        )

        if k < 1:
            raise ValueError("k must be at least 1")
        if k > len(arr):
            raise IndexError(
                f"k ({k}) cannot be greater than array length ({len(arr)})"
            )
        if not arr:
            raise ValueError("Array cannot be empty")

        if track_stats:
            self.comparison_count = 0
            self.swap_count = 0

        # Create copy to avoid modifying original
        arr_copy = arr.copy()

        result = self._quickselect_recursive(arr_copy, 0, len(arr_copy) - 1, k)

        logger.info(f"Kth largest element (quickselect): {result}")
        return result

    def get_stats(self) -> Dict[str, int]:
        """Get algorithm statistics.

        Returns:
            Dictionary with comparison and swap counts.
        """
        return {
            "comparisons": self.comparison_count,
            "swaps": self.swap_count,
        }

    def compare_methods(
        self, arr: List[Any], k: int
    ) -> Dict[str, Dict[str, Any]]:
        """Compare heap and quickselect methods.

        Args:
            arr: Array of elements.
            k: Position of largest element to find.

        Returns:
            Dictionary with performance comparison for each method.
        """
        logger.info(f"Comparing methods for finding {k}th largest element")

        results = {}

        # Test heap method
        logger.info("Testing heap method")
        start_time = time.perf_counter()
        heap_result = self.find_kth_largest_heap(arr, k)
        heap_time = time.perf_counter() - start_time

        results["heap"] = {
            "result": heap_result,
            "execution_time": heap_time,
            "method": "Min-heap of size k",
            "time_complexity": "O(n log k)",
            "space_complexity": "O(k)",
        }

        # Test quickselect method
        logger.info("Testing quickselect method")
        self.comparison_count = 0
        self.swap_count = 0

        start_time = time.perf_counter()
        quickselect_result = self.find_kth_largest_quickselect(
            arr, k, track_stats=True
        )
        quickselect_time = time.perf_counter() - start_time

        stats = self.get_stats()

        results["quickselect"] = {
            "result": quickselect_result,
            "execution_time": quickselect_time,
            "comparisons": stats["comparisons"],
            "swaps": stats["swaps"],
            "method": "Quickselect algorithm",
            "time_complexity": "O(n) average, O(n²) worst",
            "space_complexity": "O(1) iterative, O(log n) recursive",
        }

        # Verify results match
        results["results_match"] = heap_result == quickselect_result

        logger.info(
            f"Comparison complete: heap={heap_time:.10f}s, "
            f"quickselect={quickselect_time:.10f}s"
        )

        return results

    def find_kth_largest_all(
        self, arr: List[Any], k: int
    ) -> List[Any]:
        """Find all k largest elements (not just kth).

        Args:
            arr: Array of elements.
            k: Number of largest elements to find.

        Returns:
            List of k largest elements in descending order.
        """
        logger.info(f"Finding {k} largest elements")

        if k < 1:
            raise ValueError("k must be at least 1")
        if k > len(arr):
            raise IndexError(
                f"k ({k}) cannot be greater than array length ({len(arr)})"
            )
        if not arr:
            raise ValueError("Array cannot be empty")

        # Use heap to find k largest
        min_heap = []

        for num in arr:
            if len(min_heap) < k:
                heapq.heappush(min_heap, num)
            elif num > min_heap[0]:
                heapq.heapreplace(min_heap, num)

        # Sort in descending order
        result = sorted(min_heap, reverse=True)
        logger.info(f"K largest elements: {result}")
        return result

    def generate_report(
        self,
        arr: List[Any],
        k: int,
        comparison_results: Dict[str, Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate detailed analysis report.

        Args:
            arr: Original array.
            k: Value of k.
            comparison_results: Results from compare_methods.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "KTH LARGEST ELEMENT FINDER - ANALYSIS REPORT",
            "=" * 80,
            "",
            "INPUT",
            "-" * 80,
            f"Array length: {len(arr)}",
            f"k: {k}",
            f"Array: {arr[:20]}{'...' if len(arr) > 20 else ''}",
            "",
            "RESULTS",
            "-" * 80,
            f"Kth largest element: {comparison_results['heap']['result']}",
            f"Results match: {comparison_results.get('results_match', False)}",
            "",
            "PERFORMANCE COMPARISON",
            "-" * 80,
        ]

        for method_name, result in [
            ("heap", comparison_results["heap"]),
            ("quickselect", comparison_results["quickselect"]),
        ]:
            report_lines.append(f"\nMethod: {method_name.upper()}")
            report_lines.append(f"  Result: {result['result']}")
            report_lines.append(f"  Execution Time: {result['execution_time']:.10f} seconds")
            report_lines.append(f"  Time Complexity: {result['time_complexity']}")
            report_lines.append(f"  Space Complexity: {result['space_complexity']}")

            if "comparisons" in result:
                report_lines.append(f"  Comparisons: {result['comparisons']}")
            if "swaps" in result:
                report_lines.append(f"  Swaps: {result['swaps']}")

        # Calculate speedup
        heap_time = comparison_results["heap"]["execution_time"]
        quickselect_time = comparison_results["quickselect"]["execution_time"]

        if quickselect_time > 0:
            speedup = heap_time / quickselect_time
            report_lines.append(f"\nSpeedup: {speedup:.2f}x "
                              f"({'heap' if speedup < 1 else 'quickselect'} is faster)")

        report_lines.extend([
            "",
            "ALGORITHM DETAILS",
            "-" * 80,
            "HEAP METHOD:",
            "  - Uses min-heap of size k",
            "  - Maintains k largest elements seen so far",
            "  - Root of heap is kth largest element",
            "  - Time: O(n log k)",
            "  - Space: O(k)",
            "",
            "QUICKSELECT METHOD:",
            "  - Variant of quicksort algorithm",
            "  - Partitions array and recurses on one side",
            "  - Uses random pivot selection",
            "  - Time: O(n) average, O(n²) worst case",
            "  - Space: O(log n) for recursion",
            "",
            "WHEN TO USE EACH METHOD",
            "-" * 80,
            "Heap Method:",
            "  - When k is small relative to n",
            "  - When you need k largest elements (not just kth)",
            "  - When guaranteed O(n log k) is important",
            "  - When memory for k elements is acceptable",
            "",
            "Quickselect Method:",
            "  - When k is close to n/2",
            "  - When you only need the kth element",
            "  - When average O(n) performance is acceptable",
            "  - When memory is limited",
            "",
            "COMPLEXITY ANALYSIS",
            "-" * 80,
            "Heap Method:",
            "  - Time: O(n log k) - process n elements, heap operations O(log k)",
            "  - Space: O(k) - heap storage",
            "",
            "Quickselect Method:",
            "  - Time: O(n) average - each partition reduces problem size",
            "  - Time: O(n²) worst - unbalanced partitions",
            "  - Space: O(log n) - recursion stack depth",
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
        description="Find kth largest element using heap and quickselect"
    )
    parser.add_argument(
        "numbers",
        type=float,
        nargs="*",
        help="Numbers in array (space-separated)",
    )
    parser.add_argument(
        "k",
        type=int,
        nargs="?",
        default=None,
        help="Position of largest element to find (1-indexed)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["heap", "quickselect", "both"],
        default="both",
        help="Method to use (default: both)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Find all k largest elements (not just kth)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example arrays",
    )

    args = parser.parse_args()

    try:
        finder = KthLargestFinder(config_path=args.config)

        if args.demo or not args.numbers or args.k is None:
            # Run demonstration
            print("\n=== Kth Largest Element Finder Demonstration ===\n")

            examples = [
                ([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], 3),
                ([64, 34, 25, 12, 22, 11, 90], 2),
                ([10, 20, 30, 40, 50], 1),
                ([5, 2, 8, 1, 9, 3, 7, 4, 6], 5),
            ]

            for arr, k in examples:
                print(f"Array: {arr}")
                print(f"k: {k}")

                if args.method in ["heap", "both"]:
                    result = finder.find_kth_largest_heap(arr, k)
                    print(f"Heap method: {result}")

                if args.method in ["quickselect", "both"]:
                    result = finder.find_kth_largest_quickselect(arr, k)
                    print(f"Quickselect method: {result}")

                if args.method == "both":
                    comparison = finder.compare_methods(arr, k)
                    print(f"Heap time: {comparison['heap']['execution_time']:.10f}s")
                    print(
                        f"Quickselect time: "
                        f"{comparison['quickselect']['execution_time']:.10f}s"
                    )

                if args.all:
                    all_k = finder.find_kth_largest_all(arr, k)
                    print(f"All {k} largest: {all_k}")

                print()

        else:
            # Find kth largest for provided numbers
            arr = args.numbers
            k = args.k

            if args.method == "both":
                comparison = finder.compare_methods(arr, k)
                print(f"\nKth largest element: {comparison['heap']['result']}")
                print(f"\nMethod Comparison:")
                print(
                    f"  Heap:       {comparison['heap']['execution_time']:.10f}s "
                    f"({comparison['heap']['time_complexity']})"
                )
                print(
                    f"  Quickselect: {comparison['quickselect']['execution_time']:.10f}s "
                    f"({comparison['quickselect']['time_complexity']})"
                )

                if args.report:
                    report = finder.generate_report(
                        arr, k, comparison, output_path=args.report
                    )
                    print(f"\nReport saved to {args.report}")

            elif args.method == "heap":
                result = finder.find_kth_largest_heap(arr, k)
                print(f"\n{k}th largest element (heap): {result}")

            elif args.method == "quickselect":
                result = finder.find_kth_largest_quickselect(arr, k)
                stats = finder.get_stats()
                print(f"\n{k}th largest element (quickselect): {result}")
                print(f"Comparisons: {stats['comparisons']}, Swaps: {stats['swaps']}")

            if args.all:
                all_k = finder.find_kth_largest_all(arr, k)
                print(f"\nAll {k} largest elements: {all_k}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
