"""Fibonacci Calculator - Dynamic programming with memoization.

This module provides functionality to calculate Fibonacci numbers using
both naive recursion and dynamic programming with memoization, with
performance comparison.
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


class FibonacciCalculator:
    """Calculates Fibonacci numbers using multiple approaches."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize FibonacciCalculator with configuration.

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
        self.memo: Dict[int, int] = {}
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

    def fibonacci_naive(self, n: int, depth: int = 0) -> int:
        """Calculate nth Fibonacci number using naive recursion.

        Args:
            n: Position in Fibonacci sequence (0-indexed).
            depth: Current recursion depth (for tracking).

        Returns:
            nth Fibonacci number.

        Raises:
            ValueError: If n is negative.
            RecursionError: If recursion depth exceeds maximum.
        """
        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if n < 0:
            raise ValueError("n must be non-negative")

        self.recursive_calls += 1

        if n == 0:
            logger.debug(f"Base case: fib(0) = 0 (depth: {depth}, calls: {self.recursive_calls})")
            return 0

        if n == 1:
            logger.debug(f"Base case: fib(1) = 1 (depth: {depth}, calls: {self.recursive_calls})")
            return 1

        logger.debug(
            f"Recursive call: fib({n}) = fib({n-1}) + fib({n-2}) "
            f"(depth: {depth}, calls: {self.recursive_calls})"
        )

        result = self.fibonacci_naive(n - 1, depth + 1) + self.fibonacci_naive(
            n - 2, depth + 1
        )

        logger.debug(
            f"Returning from depth {depth}: fib({n}) = {result} "
            f"(calls: {self.recursive_calls})"
        )

        return result

    def fibonacci_memoized(self, n: int, depth: int = 0) -> int:
        """Calculate nth Fibonacci number using memoization.

        Args:
            n: Position in Fibonacci sequence (0-indexed).
            depth: Current recursion depth (for tracking).

        Returns:
            nth Fibonacci number.

        Raises:
            ValueError: If n is negative.
            RecursionError: If recursion depth exceeds maximum.
        """
        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if n < 0:
            raise ValueError("n must be non-negative")

        self.recursive_calls += 1

        # Base cases
        if n == 0:
            logger.debug(f"Base case: fib(0) = 0 (depth: {depth}, calls: {self.recursive_calls})")
            return 0

        if n == 1:
            logger.debug(f"Base case: fib(1) = 1 (depth: {depth}, calls: {self.recursive_calls})")
            return 1

        # Check memoization cache
        if n in self.memo:
            logger.debug(
                f"Cache hit: fib({n}) = {self.memo[n]} "
                f"(depth: {depth}, calls: {self.recursive_calls})"
            )
            return self.memo[n]

        logger.debug(
            f"Recursive call: fib({n}) = fib({n-1}) + fib({n-2}) "
            f"(depth: {depth}, calls: {self.recursive_calls})"
        )

        # Calculate and memoize
        result = self.fibonacci_memoized(n - 1, depth + 1) + self.fibonacci_memoized(
            n - 2, depth + 1
        )
        self.memo[n] = result

        logger.debug(
            f"Memoized fib({n}) = {result} "
            f"(depth: {depth}, calls: {self.recursive_calls})"
        )

        return result

    def fibonacci_iterative(self, n: int) -> int:
        """Calculate nth Fibonacci number using iterative approach.

        Args:
            n: Position in Fibonacci sequence (0-indexed).

        Returns:
            nth Fibonacci number.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        logger.info(f"Calculating fib({n}) using iterative approach")

        if n == 0:
            return 0
        if n == 1:
            return 1

        a, b = 0, 1
        logger.debug(f"Initial: a={a}, b={b}")

        for i in range(2, n + 1):
            a, b = b, a + b
            logger.debug(f"Step {i}: a={a}, b={b}")

        logger.info(f"Iterative result: fib({n}) = {b}")
        return b

    def compare_approaches(
        self, n: int, iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of different Fibonacci calculation approaches.

        Args:
            n: Position in Fibonacci sequence.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(f"Comparing approaches for calculating fib({n})")

        results = {
            "n": n,
            "iterations": iterations,
            "naive_recursion": {},
            "memoized": {},
            "iterative": {},
        }

        # Naive recursion approach
        try:
            self.recursive_calls = 0
            start_time = time.perf_counter()
            for _ in range(iterations):
                self.recursive_calls = 0
                naive_result = self.fibonacci_naive(n)
            naive_time = time.perf_counter() - start_time

            results["naive_recursion"] = {
                "result": naive_result,
                "time_seconds": naive_time / iterations,
                "time_milliseconds": (naive_time / iterations) * 1000,
                "recursive_calls": self.recursive_calls,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Naive recursion approach failed: {e}")
            results["naive_recursion"] = {"success": False, "error": str(e)}

        # Memoized approach
        try:
            self.memo = {}
            self.recursive_calls = 0
            start_time = time.perf_counter()
            for _ in range(iterations):
                self.memo = {}
                self.recursive_calls = 0
                memoized_result = self.fibonacci_memoized(n)
            memoized_time = time.perf_counter() - start_time

            results["memoized"] = {
                "result": memoized_result,
                "time_seconds": memoized_time / iterations,
                "time_milliseconds": (memoized_time / iterations) * 1000,
                "recursive_calls": self.recursive_calls,
                "memo_size": len(self.memo),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Memoized approach failed: {e}")
            results["memoized"] = {"success": False, "error": str(e)}

        # Iterative approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                iterative_result = self.fibonacci_iterative(n)
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

        # Verify all results match
        successful_results = [
            (name, data)
            for name, data in [
                ("naive_recursion", results["naive_recursion"]),
                ("memoized", results["memoized"]),
                ("iterative", results["iterative"]),
            ]
            if data.get("success", False)
        ]

        if len(successful_results) > 1:
            first_result = successful_results[0][1]["result"]
            all_match = all(
                data["result"] == first_result for _, data in successful_results
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
            comparison_data: Performance comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "FIBONACCI CALCULATION PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Calculating fib({comparison_data['n']})",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        methods = [
            ("naive_recursion", "Naive Recursion"),
            ("memoized", "Memoized (Dynamic Programming)"),
            ("iterative", "Iterative"),
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
                if "recursive_calls" in data:
                    report_lines.append(f"  Recursive calls: {data['recursive_calls']}")
                if "memo_size" in data:
                    report_lines.append(f"  Memo entries: {data['memo_size']}")
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

        # Calculate speedup
        if (
            comparison_data["naive_recursion"].get("success", False)
            and comparison_data["memoized"].get("success", False)
        ):
            naive_time = comparison_data["naive_recursion"]["time_seconds"]
            memoized_time = comparison_data["memoized"]["time_seconds"]
            if memoized_time > 0:
                speedup = naive_time / memoized_time
                report_lines.extend([
                    "",
                    "MEMOIZATION SPEEDUP",
                    "-" * 80,
                    f"Naive recursion time: {naive_time*1000:.4f} ms",
                    f"Memoized time: {memoized_time*1000:.4f} ms",
                    f"Speedup: {speedup:.2f}x",
                ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Naive Recursion:",
            "  Time: O(2^n) - exponential",
            "  Space: O(n) - call stack",
            "",
            "Memoized (Dynamic Programming):",
            "  Time: O(n) - linear",
            "  Space: O(n) - memoization cache + call stack",
            "",
            "Iterative:",
            "  Time: O(n) - linear",
            "  Space: O(1) - constant",
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
        description="Calculate Fibonacci numbers using multiple approaches"
    )
    parser.add_argument(
        "n",
        type=int,
        help="Position in Fibonacci sequence (0-indexed)",
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
        choices=["naive", "memoized", "iterative", "compare"],
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
        calculator = FibonacciCalculator(config_path=args.config)

        if args.method == "compare":
            comparison = calculator.compare_approaches(args.n, args.iterations)

            print(f"\nFibonacci Calculation Performance Comparison:")
            print(f"Calculating fib({args.n})")
            print("-" * 60)

            methods = [
                ("naive_recursion", "Naive Recursion"),
                ("memoized", "Memoized"),
                ("iterative", "Iterative"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    calls_info = ""
                    if "recursive_calls" in data:
                        calls_info = f", {data['recursive_calls']} calls"
                    if "memo_size" in data:
                        calls_info += f", {data['memo_size']} memo entries"
                    print(
                        f"{method_name:20s}: {data['result']:15d} "
                        f"({data['time_milliseconds']:8.4f} ms{calls_info})"
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

        elif args.method == "naive":
            result = calculator.fibonacci_naive(args.n)
            print(f"fib({args.n}) = {result} (naive recursion)")
            print(f"Recursive calls: {calculator.recursive_calls}")

        elif args.method == "memoized":
            calculator.memo = {}
            calculator.recursive_calls = 0
            result = calculator.fibonacci_memoized(args.n)
            print(f"fib({args.n}) = {result} (memoized)")
            print(f"Recursive calls: {calculator.recursive_calls}")
            print(f"Memo entries: {len(calculator.memo)}")

        elif args.method == "iterative":
            result = calculator.fibonacci_iterative(args.n)
            print(f"fib({args.n}) = {result} (iterative)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
