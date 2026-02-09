"""Palindrome Checker - Multiple algorithm implementations.

This module provides functionality to check if a string is a palindrome
using multiple algorithms: two-pointer, reverse comparison, and stack-based.
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


class PalindromeChecker:
    """Checks if strings are palindromes using multiple algorithms."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize PalindromeChecker with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.case_sensitive = self.config.get("options", {}).get(
            "case_sensitive", False
        )
        self.ignore_spaces = self.config.get("options", {}).get(
            "ignore_spaces", False
        )
        self.ignore_punctuation = self.config.get("options", {}).get(
            "ignore_punctuation", False
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

    def _normalize_string(self, text: str) -> str:
        """Normalize string based on configuration options.

        Args:
            text: Input string to normalize.

        Returns:
            Normalized string.
        """
        normalized = text

        if not self.case_sensitive:
            normalized = normalized.lower()
            logger.debug(f"Converted to lowercase: {normalized}")

        if self.ignore_spaces:
            normalized = normalized.replace(" ", "")
            logger.debug(f"Removed spaces: {normalized}")

        if self.ignore_punctuation:
            normalized = "".join(c for c in normalized if c.isalnum())
            logger.debug(f"Removed punctuation: {normalized}")

        return normalized

    def is_palindrome_two_pointer(self, text: str) -> bool:
        """Check if string is palindrome using two-pointer approach.

        Uses two pointers starting from both ends, moving towards center.

        Args:
            text: String to check.

        Returns:
            True if palindrome, False otherwise.
        """
        normalized = self._normalize_string(text)
        logger.info(
            f"Checking palindrome (two-pointer): '{text}' -> '{normalized}'"
        )

        if not normalized:
            logger.warning("Empty string after normalization")
            return True

        left = 0
        right = len(normalized) - 1
        comparisons = 0

        while left < right:
            comparisons += 1
            logger.debug(
                f"Comparison {comparisons}: '{normalized[left]}' "
                f"vs '{normalized[right]}' (indices {left}, {right})"
            )

            if normalized[left] != normalized[right]:
                logger.info(
                    f"Not a palindrome: mismatch at positions {left} and {right}"
                )
                return False

            left += 1
            right -= 1

        logger.info(f"Palindrome confirmed after {comparisons} comparisons")
        return True

    def is_palindrome_reverse(self, text: str) -> bool:
        """Check if string is palindrome using reverse comparison.

        Compares original string with its reverse.

        Args:
            text: String to check.

        Returns:
            True if palindrome, False otherwise.
        """
        normalized = self._normalize_string(text)
        logger.info(
            f"Checking palindrome (reverse): '{text}' -> '{normalized}'"
        )

        if not normalized:
            logger.warning("Empty string after normalization")
            return True

        reversed_text = normalized[::-1]
        logger.debug(f"Original: '{normalized}', Reversed: '{reversed_text}'")

        result = normalized == reversed_text
        logger.info(f"Palindrome check result: {result}")
        return result

    def is_palindrome_stack(self, text: str) -> bool:
        """Check if string is palindrome using stack-based approach.

        Uses stack to reverse first half and compare with second half.

        Args:
            text: String to check.

        Returns:
            True if palindrome, False otherwise.
        """
        normalized = self._normalize_string(text)
        logger.info(f"Checking palindrome (stack): '{text}' -> '{normalized}'")

        if not normalized:
            logger.warning("Empty string after normalization")
            return True

        length = len(normalized)
        stack: List[str] = []
        mid = length // 2

        # Push first half onto stack
        for i in range(mid):
            stack.append(normalized[i])
            logger.debug(f"Pushed '{normalized[i]}' onto stack")

        # Start comparing from middle (or after middle for odd length)
        start = mid + 1 if length % 2 == 1 else mid

        # Compare second half with stack
        for i in range(start, length):
            if not stack:
                logger.warning("Stack empty before comparison complete")
                return False

            popped = stack.pop()
            logger.debug(
                f"Comparing '{normalized[i]}' with popped '{popped}' "
                f"(index {i})"
            )

            if normalized[i] != popped:
                logger.info(
                    f"Not a palindrome: mismatch at position {i} "
                    f"('{normalized[i]}' vs '{popped}')"
                )
                return False

        if stack:
            logger.warning("Stack not empty after comparison")
            return False

        logger.info("Palindrome confirmed using stack method")
        return True

    def compare_algorithms(
        self, text: str, iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of different palindrome checking algorithms.

        Args:
            text: String to check.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance comparison data.
        """
        logger.info(
            f"Comparing algorithms for checking palindrome: '{text}' "
            f"({len(text)} characters)"
        )

        results = {
            "text": text,
            "text_length": len(text),
            "normalized_length": len(self._normalize_string(text)),
            "iterations": iterations,
            "two_pointer": {},
            "reverse": {},
            "stack": {},
        }

        # Two-pointer approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                two_pointer_result = self.is_palindrome_two_pointer(text)
            two_pointer_time = time.perf_counter() - start_time

            results["two_pointer"] = {
                "result": two_pointer_result,
                "time_seconds": two_pointer_time / iterations,
                "time_milliseconds": (two_pointer_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Two-pointer approach failed: {e}")
            results["two_pointer"] = {"success": False, "error": str(e)}

        # Reverse comparison approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                reverse_result = self.is_palindrome_reverse(text)
            reverse_time = time.perf_counter() - start_time

            results["reverse"] = {
                "result": reverse_result,
                "time_seconds": reverse_time / iterations,
                "time_milliseconds": (reverse_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Reverse approach failed: {e}")
            results["reverse"] = {"success": False, "error": str(e)}

        # Stack-based approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                stack_result = self.is_palindrome_stack(text)
            stack_time = time.perf_counter() - start_time

            results["stack"] = {
                "result": stack_result,
                "time_seconds": stack_time / iterations,
                "time_milliseconds": (stack_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Stack approach failed: {e}")
            results["stack"] = {"success": False, "error": str(e)}

        # Verify all results match
        successful_results = [
            (name, data)
            for name, data in [
                ("two_pointer", results["two_pointer"]),
                ("reverse", results["reverse"]),
                ("stack", results["stack"]),
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

    def generate_report(
        self, comparison_data: Dict[str, any], output_path: Optional[str] = None
    ) -> str:
        """Generate performance comparison report.

        Args:
            comparison_data: Performance comparison data from compare_algorithms().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "PALINDROME CHECK PERFORMANCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Input text: {comparison_data['text']}",
            f"Text length: {comparison_data['text_length']}",
            f"Normalized length: {comparison_data['normalized_length']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        methods = [
            ("two_pointer", "Two-Pointer Method"),
            ("reverse", "Reverse Comparison Method"),
            ("stack", "Stack-Based Method"),
        ]

        for method_key, method_name in methods:
            data = comparison_data[method_key]
            report_lines.append(f"\n{method_name}:")
            if data.get("success", False):
                status = "Palindrome" if data["result"] else "Not Palindrome"
                report_lines.append(f"  Result: {status}")
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
            "Two-Pointer: O(n) time, O(1) space",
            "Reverse Comparison: O(n) time, O(n) space",
            "Stack-Based: O(n) time, O(n) space",
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
        description="Check if string is palindrome using multiple algorithms"
    )
    parser.add_argument(
        "text",
        type=str,
        help="Text to check for palindrome",
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
        choices=["two_pointer", "reverse", "stack", "compare"],
        default="compare",
        help="Checking method (default: compare)",
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
        checker = PalindromeChecker(config_path=args.config)

        if args.method == "compare":
            comparison = checker.compare_algorithms(args.text, args.iterations)

            print(f"\nPalindrome Check Performance Comparison:")
            print(f"Text: '{args.text}'")
            print("-" * 60)

            methods = [
                ("two_pointer", "Two-Pointer"),
                ("reverse", "Reverse"),
                ("stack", "Stack"),
            ]

            for method_key, method_name in methods:
                data = comparison[method_key]
                if data.get("success", False):
                    status = "✓ Palindrome" if data["result"] else "✗ Not Palindrome"
                    print(
                        f"{method_name:15s}: {status:20s} "
                        f"({data['time_milliseconds']:8.4f} ms)"
                    )
                else:
                    print(
                        f"{method_name:15s}: Failed - {data.get('error', 'Unknown')}"
                    )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = checker.generate_report(comparison, output_path=args.report)
                print(f"\nReport saved to {args.report}")

        elif args.method == "two_pointer":
            result = checker.is_palindrome_two_pointer(args.text)
            status = "is a palindrome" if result else "is not a palindrome"
            print(f"'{args.text}' {status} (two-pointer)")

        elif args.method == "reverse":
            result = checker.is_palindrome_reverse(args.text)
            status = "is a palindrome" if result else "is not a palindrome"
            print(f"'{args.text}' {status} (reverse)")

        elif args.method == "stack":
            result = checker.is_palindrome_stack(args.text)
            status = "is a palindrome" if result else "is not a palindrome"
            print(f"'{args.text}' {status} (stack)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
