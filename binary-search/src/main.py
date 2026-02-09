"""Binary Search Algorithm - Recursive and iterative implementations.

This module provides functionality to search for elements in sorted arrays
using binary search algorithm with both recursive and iterative approaches.
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


class BinarySearch:
    """Implements binary search algorithm with recursive and iterative approaches."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BinarySearch with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.max_recursive_depth = self.config.get("recursion", {}).get(
            "max_depth", 1000
        )
        self.comparisons = 0
        self.recursive_calls = 0

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

    def _validate_sorted(self, array: List[float]) -> bool:
        """Validate that array is sorted in ascending order.

        Args:
            array: Array to validate.

        Returns:
            True if sorted, False otherwise.
        """
        for i in range(len(array) - 1):
            if array[i] > array[i + 1]:
                return False
        return True

    def search_iterative(
        self, array: List[float], target: float
    ) -> Optional[int]:
        """Search for target in sorted array using iterative binary search.

        Args:
            array: Sorted array to search.
            target: Value to search for.

        Returns:
            Index of target if found, None otherwise.

        Raises:
            ValueError: If array is not sorted.
        """
        if not array:
            logger.warning("Empty array provided")
            return None

        if not self._validate_sorted(array):
            raise ValueError("Array must be sorted in ascending order")

        self.comparisons = 0
        left = 0
        right = len(array) - 1

        logger.info(
            f"Starting iterative binary search for {target} "
            f"in array of length {len(array)}"
        )

        while left <= right:
            mid = (left + right) // 2
            self.comparisons += 1

            logger.debug(
                f"  Comparison {self.comparisons}: "
                f"left={left}, right={right}, mid={mid}, "
                f"array[{mid}]={array[mid]}"
            )

            if array[mid] == target:
                logger.info(
                    f"Target {target} found at index {mid} "
                    f"after {self.comparisons} comparisons"
                )
                return mid

            elif array[mid] < target:
                logger.debug(
                    f"  array[{mid}]={array[mid]} < {target}, "
                    f"searching right half"
                )
                left = mid + 1
            else:
                logger.debug(
                    f"  array[{mid}]={array[mid]} > {target}, "
                    f"searching left half"
                )
                right = mid - 1

        logger.info(
            f"Target {target} not found after {self.comparisons} comparisons"
        )
        return None

    def search_recursive(
        self, array: List[float], target: float, left: int = 0,
        right: Optional[int] = None, depth: int = 0
    ) -> Optional[int]:
        """Search for target in sorted array using recursive binary search.

        Args:
            array: Sorted array to search.
            target: Value to search for.
            left: Left boundary of search range (default: 0).
            right: Right boundary of search range (default: len(array) - 1).
            depth: Current recursion depth (for tracking).

        Returns:
            Index of target if found, None otherwise.

        Raises:
            ValueError: If array is not sorted.
            RecursionError: If recursion depth exceeds maximum.
        """
        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if right is None:
            right = len(array) - 1

        if not array:
            logger.warning("Empty array provided")
            return None

        if left == 0 and right == len(array) - 1:
            if not self._validate_sorted(array):
                raise ValueError("Array must be sorted in ascending order")
            self.comparisons = 0
            self.recursive_calls = 0

        if left > right:
            logger.debug(
                f"Base case: left={left} > right={right}, "
                f"target not found (depth: {depth})"
            )
            return None

        self.recursive_calls += 1
        mid = (left + right) // 2
        self.comparisons += 1

        logger.debug(
            f"Recursive call {self.recursive_calls} (depth {depth}): "
            f"left={left}, right={right}, mid={mid}, "
            f"array[{mid}]={array[mid]}"
        )

        if array[mid] == target:
            logger.info(
                f"Target {target} found at index {mid} "
                f"after {self.comparisons} comparisons "
                f"and {self.recursive_calls} recursive calls"
            )
            return mid

        elif array[mid] < target:
            logger.debug(
                f"  array[{mid}]={array[mid]} < {target}, "
                f"recursing right (depth: {depth})"
            )
            return self.search_recursive(
                array, target, mid + 1, right, depth + 1
            )
        else:
            logger.debug(
                f"  array[{mid}]={array[mid]} > {target}, "
                f"recursing left (depth: {depth})"
            )
            return self.search_recursive(
                array, target, left, mid - 1, depth + 1
            )

    def compare_approaches(
        self, array: List[float], target: float, iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of iterative and recursive binary search.

        Args:
            array: Sorted array to search.
            target: Value to search for.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing approaches for searching {target} "
            f"in array of length {len(array)}"
        )

        results = {
            "array_length": len(array),
            "target": target,
            "iterations": iterations,
            "iterative": {},
            "recursive": {},
        }

        # Iterative approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                iterative_result = self.search_iterative(array, target)
            iterative_time = time.perf_counter() - start_time

            results["iterative"] = {
                "result": iterative_result,
                "time_seconds": iterative_time / iterations,
                "time_milliseconds": (iterative_time / iterations) * 1000,
                "comparisons": self.comparisons,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Iterative approach failed: {e}")
            results["iterative"] = {"success": False, "error": str(e)}

        # Recursive approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                recursive_result = self.search_recursive(array, target)
            recursive_time = time.perf_counter() - start_time

            results["recursive"] = {
                "result": recursive_result,
                "time_seconds": recursive_time / iterations,
                "time_milliseconds": (recursive_time / iterations) * 1000,
                "comparisons": self.comparisons,
                "recursive_calls": self.recursive_calls,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Recursive approach failed: {e}")
            results["recursive"] = {"success": False, "error": str(e)}

        # Verify results match
        if (
            results["iterative"].get("success", False)
            and results["recursive"].get("success", False)
        ):
            if results["iterative"]["result"] == results["recursive"]["result"]:
                logger.info("Both approaches produced identical results")
            else:
                logger.warning("Results differ between approaches!")

        # Determine fastest
        successful_results = [
            (name, data)
            for name, data in [
                ("iterative", results["iterative"]),
                ("recursive", results["recursive"]),
            ]
            if data.get("success", False)
        ]

        if successful_results:
            fastest = min(successful_results, key=lambda x: x[1]["time_seconds"])
            results["fastest"] = fastest[0]
            results["fastest_time"] = fastest[1]["time_seconds"]

        return results

    def generate_report(
        self, comparison_data: Dict[str, any], output_path: Optional[str] = None
    ) -> str:
        """Generate performance comparison report.

        Args:
            comparison_data: Performance comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "BINARY SEARCH PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Array length: {comparison_data['array_length']}",
            f"Target: {comparison_data['target']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        methods = [
            ("iterative", "Iterative Method"),
            ("recursive", "Recursive Method"),
        ]

        for method_key, method_name in methods:
            data = comparison_data[method_key]
            report_lines.append(f"\n{method_name}:")
            if data.get("success", False):
                result = data["result"]
                if result is not None:
                    report_lines.append(f"  Result: Found at index {result}")
                else:
                    report_lines.append(f"  Result: Not found")
                report_lines.append(
                    f"  Time: {data['time_milliseconds']:.4f} ms "
                    f"({data['time_seconds']:.6f} seconds)"
                )
                report_lines.append(f"  Comparisons: {data['comparisons']}")
                if "recursive_calls" in data:
                    report_lines.append(
                        f"  Recursive calls: {data['recursive_calls']}"
                    )
            else:
                report_lines.append(f"  Status: Failed")
                report_lines.append(f"  Error: {data.get('error', 'Unknown error')}")

        if "fastest" in comparison_data:
            report_lines.extend([
                "",
                "PERFORMANCE SUMMARY",
                "-" * 80,
                f"Fastest method: {comparison_data['fastest']}",
                f"Fastest time: {comparison_data['fastest_time']*1000:.4f} ms",
            ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(log n)",
            "Space Complexity:",
            "  Iterative: O(1)",
            "  Recursive: O(log n) due to call stack",
            "Best Case: O(1) - target at middle",
            "Worst Case: O(log n) - target at end or not found",
            "Average Case: O(log n)",
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
        description="Search for element in sorted array using binary search"
    )
    parser.add_argument(
        "target",
        type=float,
        help="Target value to search for",
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Sorted array of numbers",
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
        choices=["iterative", "recursive", "compare"],
        default="compare",
        help="Search method (default: compare)",
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
        help="Output path for performance report",
    )

    args = parser.parse_args()

    try:
        searcher = BinarySearch(config_path=args.config)

        array = sorted(args.numbers)
        logger.info(f"Input array (sorted): {array}")

        if args.method == "compare":
            comparison = searcher.compare_approaches(
                array, args.target, args.iterations
            )

            print(f"\nBinary Search Performance Comparison:")
            print(f"Array: {array}")
            print(f"Target: {args.target}")
            print("-" * 60)

            methods = [
                ("iterative", "Iterative"),
                ("recursive", "Recursive"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    result = data["result"]
                    status = f"Found at index {result}" if result is not None else "Not found"
                    print(
                        f"{method_name:15s}: {status:20s} "
                        f"({data['time_milliseconds']:8.4f} ms, "
                        f"{data['comparisons']} comparisons)"
                    )
                else:
                    print(
                        f"{method_name:15s}: Failed - {data.get('error', 'Unknown')}"
                    )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = searcher.generate_report(comparison, output_path=args.report)
                print(f"\nReport saved to {args.report}")

        elif args.method == "iterative":
            result = searcher.search_iterative(array, args.target)
            if result is not None:
                print(f"Target {args.target} found at index {result} (iterative)")
            else:
                print(f"Target {args.target} not found (iterative)")

        elif args.method == "recursive":
            result = searcher.search_recursive(array, args.target)
            if result is not None:
                print(f"Target {args.target} found at index {result} (recursive)")
            else:
                print(f"Target {args.target} not found (recursive)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
