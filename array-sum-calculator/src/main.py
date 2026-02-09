"""Array Sum Calculator - Iterative and recursive approaches.

This module provides functionality to find the sum of all elements in an array
using both iterative and recursive approaches with performance comparison.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ArraySumCalculator:
    """Calculates sum of array elements using iterative and recursive approaches."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize ArraySumCalculator with configuration.

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

    def sum_iterative(self, array: List[float]) -> float:
        """Calculate sum using iterative approach.

        Args:
            array: List of numbers to sum.

        Returns:
            Sum of all elements in array.
        """
        if not array:
            logger.warning("Empty array provided")
            return 0.0

        logger.info(f"Calculating sum iteratively for array of length {len(array)}")
        total = 0.0

        for idx, value in enumerate(array):
            total += value
            logger.debug(f"Step {idx + 1}: total = {total} (added {value})")

        logger.info(f"Iterative sum: {total}")
        return total

    def sum_recursive(self, array: List[float], depth: int = 0) -> float:
        """Calculate sum using recursive approach.

        Args:
            array: List of numbers to sum.
            depth: Current recursion depth (for tracking).

        Returns:
            Sum of all elements in array.

        Raises:
            RecursionError: If recursion depth exceeds maximum.
        """
        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if not array:
            logger.debug(f"Base case reached: empty array (depth: {depth})")
            return 0.0

        if len(array) == 1:
            logger.debug(
                f"Base case reached: single element {array[0]} (depth: {depth})"
            )
            return array[0]

        logger.debug(
            f"Recursive call: sum({array}) = {array[0]} + sum({array[1:]}) "
            f"(depth: {depth})"
        )

        result = array[0] + self.sum_recursive(array[1:], depth + 1)

        logger.debug(f"Returning from depth {depth}: sum = {result}")
        return result

    def sum_recursive_indexed(
        self, array: List[float], index: int = 0, depth: int = 0
    ) -> float:
        """Calculate sum using recursive approach with index parameter.

        Args:
            array: List of numbers to sum.
            index: Current index in array.
            depth: Current recursion depth (for tracking).

        Returns:
            Sum of all elements from index to end.

        Raises:
            RecursionError: If recursion depth exceeds maximum.
        """
        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if index >= len(array):
            logger.debug(
                f"Base case reached: index {index} >= length {len(array)} "
                f"(depth: {depth})"
            )
            return 0.0

        logger.debug(
            f"Recursive call: sum from index {index} = {array[index]} + "
            f"sum from index {index + 1} (depth: {depth})"
        )

        result = array[index] + self.sum_recursive_indexed(
            array, index + 1, depth + 1
        )

        logger.debug(
            f"Returning from depth {depth}: sum from index {index} = {result}"
        )
        return result

    def compare_performance(
        self, array: List[float], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of different sum calculation approaches.

        Args:
            array: List of numbers to sum.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing performance for summing array of length {len(array)}"
        )

        results = {
            "array_length": len(array),
            "iterations": iterations,
            "iterative": {},
            "recursive": {},
            "recursive_indexed": {},
        }

        # Iterative approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                iterative_result = self.sum_iterative(array)
            iterative_time = time.perf_counter() - start_time

            results["iterative"] = {
                "result": iterative_result,
                "time_seconds": iterative_time / iterations,
                "time_milliseconds": (iterative_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Iterative approach failed: {e}")
            results["iterative"] = {"success": False, "error": str(e)}

        # Recursive approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                recursive_result = self.sum_recursive(array)
            recursive_time = time.perf_counter() - start_time

            results["recursive"] = {
                "result": recursive_result,
                "time_seconds": recursive_time / iterations,
                "time_milliseconds": (recursive_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Recursive approach failed: {e}")
            results["recursive"] = {"success": False, "error": str(e)}

        # Recursive indexed approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                recursive_idx_result = self.sum_recursive_indexed(array)
            recursive_idx_time = time.perf_counter() - start_time

            results["recursive_indexed"] = {
                "result": recursive_idx_result,
                "time_seconds": recursive_idx_time / iterations,
                "time_milliseconds": (recursive_idx_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Recursive indexed approach failed: {e}")
            results["recursive_indexed"] = {"success": False, "error": str(e)}

        # Verify all results match
        successful_results = [
            (name, data)
            for name, data in [
                ("iterative", results["iterative"]),
                ("recursive", results["recursive"]),
                ("recursive_indexed", results["recursive_indexed"]),
            ]
            if data.get("success", False)
        ]

        if len(successful_results) > 1:
            first_result = successful_results[0][1]["result"]
            all_match = all(
                abs(data["result"] - first_result) < 1e-10
                for _, data in successful_results
            )
            if all_match:
                logger.info("All approaches produced identical results")
            else:
                logger.warning("Results differ between approaches!")

        # Determine fastest
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
            comparison_data: Performance comparison data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "ARRAY SUM CALCULATION PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Array length: {comparison_data['array_length']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        methods = [
            ("iterative", "Iterative Method"),
            ("recursive", "Recursive Method"),
            ("recursive_indexed", "Recursive Indexed Method"),
        ]

        for method_key, method_name in methods:
            data = comparison_data[method_key]
            report_lines.append(f"\n{method_name}:")
            if data.get("success", False):
                report_lines.append(f"  Result: {data['result']}")
                report_lines.append(
                    f"  Time: {data['time_milliseconds']:.4f} ms "
                    f"({data['time_seconds']:.6f} seconds)"
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
            "Iterative: O(n) time, O(1) space",
            "Recursive: O(n) time, O(n) space (call stack)",
            "Recursive Indexed: O(n) time, O(n) space (call stack)",
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
        description="Calculate sum of array elements using iterative and recursive approaches"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers to sum",
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
        choices=["iterative", "recursive", "recursive_indexed", "compare"],
        default="compare",
        help="Calculation method (default: compare)",
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
        calculator = ArraySumCalculator(config_path=args.config)

        if args.method == "compare":
            comparison = calculator.compare_performance(args.numbers, args.iterations)

            print(f"\nArray Sum Performance Comparison:")
            print(f"Array: {args.numbers}")
            print("-" * 60)

            methods = [
                ("iterative", "Iterative"),
                ("recursive", "Recursive"),
                ("recursive_indexed", "Recursive Indexed"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    print(
                        f"{method_name:20s}: {data['result']:10.2f} "
                        f"({data['time_milliseconds']:8.4f} ms)"
                    )
                else:
                    print(
                        f"{method_name:20s}: Failed - {data.get('error', 'Unknown')}"
                    )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = calculator.generate_report(comparison, output_path=args.report)
                print(f"\nReport saved to {args.report}")

        elif args.method == "iterative":
            result = calculator.sum_iterative(args.numbers)
            print(f"Sum: {result} (iterative)")

        elif args.method == "recursive":
            result = calculator.sum_recursive(args.numbers)
            print(f"Sum: {result} (recursive)")

        elif args.method == "recursive_indexed":
            result = calculator.sum_recursive_indexed(args.numbers)
            print(f"Sum: {result} (recursive indexed)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
