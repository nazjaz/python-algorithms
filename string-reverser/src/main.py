"""String Reverser - Multiple methods with performance comparison.

This module provides functionality to reverse strings using multiple methods
(slicing, loop, recursion) and compares their performance.
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


class StringReverser:
    """Reverses strings using multiple methods and compares performance."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize StringReverser with configuration.

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

    def reverse_slicing(self, text: str) -> str:
        """Reverse string using Python slicing.

        Args:
            text: String to reverse.

        Returns:
            Reversed string.
        """
        logger.debug(f"Reversing '{text}' using slicing method")
        result = text[::-1]
        logger.info(f"Slicing result: '{result}'")
        return result

    def reverse_loop(self, text: str) -> str:
        """Reverse string using loop method.

        Args:
            text: String to reverse.

        Returns:
            Reversed string.
        """
        logger.debug(f"Reversing '{text}' using loop method")
        result = ""
        for char in text:
            result = char + result
        logger.info(f"Loop result: '{result}'")
        return result

    def reverse_loop_optimized(self, text: str) -> str:
        """Reverse string using optimized loop with list.

        Args:
            text: String to reverse.

        Returns:
            Reversed string.
        """
        logger.debug(f"Reversing '{text}' using optimized loop method")
        chars = list(text)
        length = len(chars)
        for i in range(length // 2):
            chars[i], chars[length - 1 - i] = chars[length - 1 - i], chars[i]
        result = "".join(chars)
        logger.info(f"Optimized loop result: '{result}'")
        return result

    def reverse_recursive(self, text: str, depth: int = 0) -> str:
        """Reverse string using recursive method.

        Args:
            text: String to reverse.
            depth: Current recursion depth (for tracking).

        Returns:
            Reversed string.

        Raises:
            RecursionError: If recursion depth exceeds maximum.
        """
        if depth > self.max_recursive_depth:
            raise RecursionError(
                f"Maximum recursion depth ({self.max_recursive_depth}) exceeded"
            )

        if len(text) <= 1:
            logger.debug(
                f"Base case reached: '{text}' (depth: {depth})"
            )
            return text

        logger.debug(
            f"Recursive call: reverse('{text}') = "
            f"reverse('{text[1:]}') + '{text[0]}' (depth: {depth})"
        )

        result = self.reverse_recursive(text[1:], depth + 1) + text[0]

        logger.debug(
            f"Returning from depth {depth}: '{result}'"
        )
        return result

    def reverse_builtin(self, text: str) -> str:
        """Reverse string using built-in reversed() function.

        Args:
            text: String to reverse.

        Returns:
            Reversed string.
        """
        logger.debug(f"Reversing '{text}' using built-in reversed() method")
        result = "".join(reversed(text))
        logger.info(f"Built-in reversed() result: '{result}'")
        return result

    def compare_performance(self, text: str, iterations: int = 1) -> Dict[str, any]:
        """Compare performance of different string reversal methods.

        Args:
            text: String to reverse.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing performance for reversing string of length {len(text)}"
        )

        results = {
            "input_length": len(text),
            "iterations": iterations,
            "slicing": {},
            "loop": {},
            "loop_optimized": {},
            "recursive": {},
            "builtin": {},
        }

        # Slicing method
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                slicing_result = self.reverse_slicing(text)
            slicing_time = time.perf_counter() - start_time

            results["slicing"] = {
                "result": slicing_result,
                "time_seconds": slicing_time / iterations,
                "time_milliseconds": (slicing_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Slicing method failed: {e}")
            results["slicing"] = {"success": False, "error": str(e)}

        # Loop method
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                loop_result = self.reverse_loop(text)
            loop_time = time.perf_counter() - start_time

            results["loop"] = {
                "result": loop_result,
                "time_seconds": loop_time / iterations,
                "time_milliseconds": (loop_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Loop method failed: {e}")
            results["loop"] = {"success": False, "error": str(e)}

        # Optimized loop method
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                loop_opt_result = self.reverse_loop_optimized(text)
            loop_opt_time = time.perf_counter() - start_time

            results["loop_optimized"] = {
                "result": loop_opt_result,
                "time_seconds": loop_opt_time / iterations,
                "time_milliseconds": (loop_opt_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Optimized loop method failed: {e}")
            results["loop_optimized"] = {"success": False, "error": str(e)}

        # Recursive method
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                recursive_result = self.reverse_recursive(text)
            recursive_time = time.perf_counter() - start_time

            results["recursive"] = {
                "result": recursive_result,
                "time_seconds": recursive_time / iterations,
                "time_milliseconds": (recursive_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Recursive method failed: {e}")
            results["recursive"] = {"success": False, "error": str(e)}

        # Built-in method
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                builtin_result = self.reverse_builtin(text)
            builtin_time = time.perf_counter() - start_time

            results["builtin"] = {
                "result": builtin_result,
                "time_seconds": builtin_time / iterations,
                "time_milliseconds": (builtin_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Built-in method failed: {e}")
            results["builtin"] = {"success": False, "error": str(e)}

        # Verify all results match
        successful_results = [
            (name, data)
            for name, data in [
                ("slicing", results["slicing"]),
                ("loop", results["loop"]),
                ("loop_optimized", results["loop_optimized"]),
                ("recursive", results["recursive"]),
                ("builtin", results["builtin"]),
            ]
            if data.get("success", False)
        ]

        if len(successful_results) > 1:
            first_result = successful_results[0][1]["result"]
            all_match = all(
                data["result"] == first_result for _, data in successful_results
            )
            if all_match:
                logger.info("All methods produced identical results")
            else:
                logger.warning("Results differ between methods!")

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
            "STRING REVERSAL PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Input string length: {comparison_data['input_length']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        methods = [
            ("slicing", "Slicing Method"),
            ("loop", "Loop Method"),
            ("loop_optimized", "Optimized Loop Method"),
            ("recursive", "Recursive Method"),
            ("builtin", "Built-in reversed() Method"),
        ]

        for method_key, method_name in methods:
            data = comparison_data[method_key]
            report_lines.append(f"\n{method_name}:")
            if data.get("success", False):
                report_lines.append(
                    f"  Time: {data['time_milliseconds']:.4f} ms "
                    f"({data['time_seconds']:.6f} seconds)"
                )
                report_lines.append(f"  Result: {data['result'][:50]}..." if len(data['result']) > 50 else f"  Result: {data['result']}")
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
            "Slicing: O(n) time, O(n) space",
            "Loop: O(n) time, O(n) space",
            "Optimized Loop: O(n) time, O(1) space (in-place)",
            "Recursive: O(n) time, O(n) space (call stack)",
            "Built-in reversed(): O(n) time, O(n) space",
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
        description="Reverse strings using multiple methods and compare performance"
    )
    parser.add_argument(
        "text",
        help="String to reverse",
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
        choices=["slicing", "loop", "loop_optimized", "recursive", "builtin", "compare"],
        default="compare",
        help="Reversal method (default: compare)",
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
        reverser = StringReverser(config_path=args.config)

        if args.method == "compare":
            comparison = reverser.compare_performance(args.text, args.iterations)

            print(f"\nString Reversal Performance Comparison:")
            print(f"Input: '{args.text}' (length: {len(args.text)})")
            print("-" * 60)

            methods = [
                ("slicing", "Slicing"),
                ("loop", "Loop"),
                ("loop_optimized", "Optimized Loop"),
                ("recursive", "Recursive"),
                ("builtin", "Built-in"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    print(
                        f"{method_name:20s}: {data['time_milliseconds']:8.4f} ms"
                    )
                else:
                    print(f"{method_name:20s}: Failed - {data.get('error', 'Unknown')}")

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = reverser.generate_report(comparison, output_path=args.report)
                print(f"\nReport saved to {args.report}")

        elif args.method == "slicing":
            result = reverser.reverse_slicing(args.text)
            print(f"Reversed: '{result}' (slicing)")

        elif args.method == "loop":
            result = reverser.reverse_loop(args.text)
            print(f"Reversed: '{result}' (loop)")

        elif args.method == "loop_optimized":
            result = reverser.reverse_loop_optimized(args.text)
            print(f"Reversed: '{result}' (optimized loop)")

        elif args.method == "recursive":
            result = reverser.reverse_recursive(args.text)
            print(f"Reversed: '{result}' (recursive)")

        elif args.method == "builtin":
            result = reverser.reverse_builtin(args.text)
            print(f"Reversed: '{result}' (built-in)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
