"""Factorial Calculator - Iterative and recursive implementations.

This module provides functionality to calculate factorials using both iterative
and recursive approaches with performance comparison.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class FactorialCalculator:
    """Calculates factorials using iterative and recursive approaches."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize FactorialCalculator with configuration.

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

    def factorial_iterative(self, n: int) -> int:
        """Calculate factorial using iterative approach.

        Args:
            n: Non-negative integer to calculate factorial for.

        Returns:
            Factorial of n.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")

        if n == 0 or n == 1:
            logger.debug(f"Factorial of {n} is 1 (base case)")
            return 1

        logger.info(f"Calculating factorial of {n} using iterative approach")
        result = 1

        for i in range(2, n + 1):
            result *= i
            logger.debug(f"Step {i-1}: result = {result}")

        logger.info(f"Iterative factorial of {n} = {result}")
        return result

    def factorial_recursive(self, n: int, depth: int = 0) -> int:
        """Calculate factorial using recursive approach.

        Args:
            n: Non-negative integer to calculate factorial for.
            depth: Current recursion depth (for tracking).

        Returns:
            Factorial of n.

        Raises:
            ValueError: If n is negative.
            RecursionError: If recursion depth exceeds maximum.
        """
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")

        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if n == 0 or n == 1:
            logger.debug(
                f"Base case reached: factorial({n}) = 1 (depth: {depth})"
            )
            return 1

        logger.debug(
            f"Recursive call: factorial({n}) = {n} * factorial({n-1}) "
            f"(depth: {depth})"
        )

        result = n * self.factorial_recursive(n - 1, depth + 1)

        logger.debug(f"Returning from depth {depth}: factorial({n}) = {result}")
        return result

    def factorial_memoized(self, n: int, memo: Optional[Dict[int, int]] = None) -> int:
        """Calculate factorial using memoized recursive approach.

        Args:
            n: Non-negative integer to calculate factorial for.
            memo: Dictionary for memoization (optional).

        Returns:
            Factorial of n.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")

        if memo is None:
            memo = {}

        if n in memo:
            logger.debug(f"Memoized result found: factorial({n}) = {memo[n]}")
            return memo[n]

        if n == 0 or n == 1:
            memo[n] = 1
            logger.debug(f"Base case: factorial({n}) = 1")
            return 1

        logger.debug(f"Calculating factorial({n}) and storing in memo")
        memo[n] = n * self.factorial_memoized(n - 1, memo)
        return memo[n]

    def compare_performance(self, n: int) -> Dict[str, any]:
        """Compare performance of different factorial approaches.

        Args:
            n: Non-negative integer to calculate factorial for.

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(f"Comparing performance for factorial({n})")

        results = {
            "input": n,
            "iterative": {},
            "recursive": {},
            "memoized": {},
        }

        # Iterative approach
        try:
            start_time = time.perf_counter()
            iterative_result = self.factorial_iterative(n)
            iterative_time = time.perf_counter() - start_time

            results["iterative"] = {
                "result": iterative_result,
                "time_seconds": iterative_time,
                "time_milliseconds": iterative_time * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Iterative approach failed: {e}")
            results["iterative"] = {"success": False, "error": str(e)}

        # Recursive approach
        try:
            start_time = time.perf_counter()
            recursive_result = self.factorial_recursive(n)
            recursive_time = time.perf_counter() - start_time

            results["recursive"] = {
                "result": recursive_result,
                "time_seconds": recursive_time,
                "time_milliseconds": recursive_time * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Recursive approach failed: {e}")
            results["recursive"] = {"success": False, "error": str(e)}

        # Memoized approach
        try:
            start_time = time.perf_counter()
            memoized_result = self.factorial_memoized(n)
            memoized_time = time.perf_counter() - start_time

            results["memoized"] = {
                "result": memoized_result,
                "time_seconds": memoized_time,
                "time_milliseconds": memoized_time * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Memoized approach failed: {e}")
            results["memoized"] = {"success": False, "error": str(e)}

        # Verify all results match
        if all(
            r.get("success", False)
            for r in [
                results["iterative"],
                results["recursive"],
                results["memoized"],
            ]
        ):
            if (
                results["iterative"]["result"]
                == results["recursive"]["result"]
                == results["memoized"]["result"]
            ):
                logger.info("All approaches produced identical results")
            else:
                logger.warning("Results differ between approaches!")

        # Determine fastest
        successful_results = [
            (name, data)
            for name, data in [
                ("iterative", results["iterative"]),
                ("recursive", results["recursive"]),
                ("memoized", results["memoized"]),
            ]
            if data.get("success", False)
        ]

        if successful_results:
            fastest = min(successful_results, key=lambda x: x[1]["time_seconds"])
            results["fastest"] = fastest[0]
            results["fastest_time"] = fastest[1]["time_seconds"]

        return results

    def generate_report(self, comparison_data: Dict[str, any], output_path: Optional[str] = None) -> str:
        """Generate performance comparison report.

        Args:
            comparison_data: Performance comparison data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "FACTORIAL CALCULATION PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Input: factorial({comparison_data['input']})",
            "",
            "RESULTS",
            "-" * 80,
        ]

        for approach in ["iterative", "recursive", "memoized"]:
            data = comparison_data[approach]
            report_lines.append(f"\n{approach.upper()} APPROACH:")
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
                f"Fastest approach: {comparison_data['fastest']}",
                f"Fastest time: {comparison_data['fastest_time']*1000:.4f} ms",
            ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Iterative: O(n) time, O(1) space",
            "Recursive: O(n) time, O(n) space (call stack)",
            "Memoized: O(n) time, O(n) space (memoization table)",
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
        description="Calculate factorial using iterative and recursive approaches"
    )
    parser.add_argument(
        "number",
        type=int,
        help="Non-negative integer to calculate factorial for",
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
        choices=["iterative", "recursive", "memoized", "compare"],
        default="compare",
        help="Calculation method (default: compare)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for performance report",
    )

    args = parser.parse_args()

    try:
        calculator = FactorialCalculator(config_path=args.config)

        if args.method == "compare":
            comparison = calculator.compare_performance(args.number)

            print(f"\nFactorial({args.number}) Performance Comparison:")
            print("-" * 60)

            for approach in ["iterative", "recursive", "memoized"]:
                data = comparison[approach]
                if data.get("success", False):
                    print(
                        f"{approach.capitalize()}: {data['result']} "
                        f"({data['time_milliseconds']:.4f} ms)"
                    )
                else:
                    print(f"{approach.capitalize()}: Failed - {data.get('error', 'Unknown')}")

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = calculator.generate_report(comparison, output_path=args.report)
                print(f"\nReport saved to {args.report}")

        elif args.method == "iterative":
            result = calculator.factorial_iterative(args.number)
            print(f"Factorial({args.number}) = {result} (iterative)")

        elif args.method == "recursive":
            result = calculator.factorial_recursive(args.number)
            print(f"Factorial({args.number}) = {result} (recursive)")

        elif args.method == "memoized":
            result = calculator.factorial_memoized(args.number)
            print(f"Factorial({args.number}) = {result} (memoized)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
