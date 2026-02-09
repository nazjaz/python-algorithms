"""Longest Increasing Subsequence (LIS) Problem Solver.

This module provides functionality to find the longest increasing subsequence
in an array using both dynamic programming and binary search optimization
approaches.
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


class LongestIncreasingSubsequence:
    """Finds longest increasing subsequence using DP and binary search."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize LongestIncreasingSubsequence with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()

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

    def find_lis_dp(self, arr: List[float]) -> Tuple[int, List[float]]:
        """Find LIS using dynamic programming approach.

        Uses O(n²) dynamic programming where dp[i] represents the length
        of LIS ending at index i. For each element, check all previous
        elements to find the longest subsequence that can be extended.

        Args:
            arr: Input array of numbers.

        Returns:
            Tuple containing:
                - Length of LIS
                - One example of LIS

        Raises:
            ValueError: If array is invalid.
        """
        if not arr:
            logger.info("Empty array: returning empty LIS")
            return 0, []

        logger.info(f"Finding LIS (DP): {len(arr)} elements")

        n = len(arr)
        dp = [1] * n
        parent = [-1] * n

        # Build DP table
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
                    logger.debug(
                        f"  dp[{i}] = {dp[i]}, parent = {j} "
                        f"(arr[{j}]={arr[j]} < arr[{i}]={arr[i]})"
                    )

        # Find maximum length and its index
        max_length = max(dp)
        max_index = dp.index(max_length)

        # Reconstruct LIS
        lis = []
        current = max_index
        while current != -1:
            lis.append(arr[current])
            current = parent[current]

        lis.reverse()

        logger.info(
            f"LIS found: length={max_length}, sequence={lis}"
        )

        return max_length, lis

    def _binary_search(
        self, tails: List[float], target: float, left: int, right: int
    ) -> int:
        """Binary search helper to find insertion position.

        Finds the leftmost position where target can be inserted in
        sorted array tails to maintain sorted order.

        Args:
            tails: Sorted array of tail elements.
            target: Value to find position for.
            left: Left boundary.
            right: Right boundary.

        Returns:
            Insertion position index.
        """
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < target:
                left = mid + 1
            else:
                right = mid
        return left

    def find_lis_binary_search(
        self, arr: List[float]
    ) -> Tuple[int, List[float]]:
        """Find LIS using binary search optimization.

        Uses O(n log n) approach with binary search. Maintains an array
        `tails` where tails[i] is the smallest tail element of all
        increasing subsequences of length i+1. This allows us to use
        binary search to find where to extend subsequences.

        Args:
            arr: Input array of numbers.

        Returns:
            Tuple containing:
                - Length of LIS
                - One example of LIS

        Raises:
            ValueError: If array is invalid.
        """
        if not arr:
            logger.info("Empty array: returning empty LIS")
            return 0, []

        logger.info(f"Finding LIS (Binary Search): {len(arr)} elements")

        n = len(arr)
        tails: List[float] = []
        indices: List[int] = []
        parent: List[int] = [-1] * n

        for i in range(n):
            # Binary search for position to insert arr[i]
            pos = self._binary_search(tails, arr[i], 0, len(tails))

            if pos == len(tails):
                tails.append(arr[i])
                indices.append(i)
            else:
                tails[pos] = arr[i]
                indices[pos] = i

            # Track parent for reconstruction
            if pos > 0:
                parent[i] = indices[pos - 1]

            logger.debug(
                f"  arr[{i}]={arr[i]}, pos={pos}, "
                f"tails={tails}, indices={indices}"
            )

        # Reconstruct LIS
        lis_length = len(tails)
        if lis_length == 0:
            return 0, []

        lis: List[float] = []
        current = indices[-1]
        while current != -1:
            lis.append(arr[current])
            current = parent[current]

        lis.reverse()

        logger.info(
            f"LIS found: length={lis_length}, sequence={lis}"
        )

        return lis_length, lis

    def get_lis_length_dp(self, arr: List[float]) -> int:
        """Get LIS length using dynamic programming.

        Args:
            arr: Input array of numbers.

        Returns:
            Length of LIS.
        """
        length, _ = self.find_lis_dp(arr)
        return length

    def get_lis_length_binary_search(self, arr: List[float]) -> int:
        """Get LIS length using binary search optimization.

        Args:
            arr: Input array of numbers.

        Returns:
            Length of LIS.
        """
        length, _ = self.find_lis_binary_search(arr)
        return length

    def get_lis_sequence_dp(self, arr: List[float]) -> List[float]:
        """Get LIS sequence using dynamic programming.

        Args:
            arr: Input array of numbers.

        Returns:
            One example of LIS.
        """
        _, sequence = self.find_lis_dp(arr)
        return sequence

    def get_lis_sequence_binary_search(self, arr: List[float]) -> List[float]:
        """Get LIS sequence using binary search optimization.

        Args:
            arr: Input array of numbers.

        Returns:
            One example of LIS.
        """
        _, sequence = self.find_lis_binary_search(arr)
        return sequence

    def compare_approaches(
        self, arr: List[float], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare DP and binary search approaches.

        Args:
            arr: Input array of numbers.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing comparison data.
        """
        logger.info(
            f"Comparing approaches: {len(arr)} elements, "
            f"iterations={iterations}"
        )

        results = {
            "array_length": len(arr),
            "iterations": iterations,
            "dp": {},
            "binary_search": {},
        }

        # DP approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                length_dp, sequence_dp = self.find_lis_dp(arr)
            dp_time = time.perf_counter() - start_time

            results["dp"] = {
                "length": length_dp,
                "sequence": sequence_dp,
                "time_seconds": dp_time / iterations,
                "time_milliseconds": (dp_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"DP approach failed: {e}")
            results["dp"] = {"success": False, "error": str(e)}

        # Binary search approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                length_bs, sequence_bs = self.find_lis_binary_search(arr)
            bs_time = time.perf_counter() - start_time

            results["binary_search"] = {
                "length": length_bs,
                "sequence": sequence_bs,
                "time_seconds": bs_time / iterations,
                "time_milliseconds": (bs_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Binary search approach failed: {e}")
            results["binary_search"] = {"success": False, "error": str(e)}

        # Verify results match
        if (
            results["dp"].get("success", False)
            and results["binary_search"].get("success", False)
        ):
            if results["dp"]["length"] == results["binary_search"]["length"]:
                logger.info("Both approaches produced identical LIS lengths")
            else:
                logger.warning("LIS lengths differ between approaches!")

            # Determine fastest
            dp_time = results["dp"]["time_seconds"]
            bs_time = results["binary_search"]["time_seconds"]
            if dp_time < bs_time:
                results["fastest"] = "dp"
                results["fastest_time"] = dp_time
            else:
                results["fastest"] = "binary_search"
                results["fastest_time"] = bs_time

        return results

    def generate_report(
        self,
        comparison_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate comparison report for LIS approaches.

        Args:
            comparison_data: Comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "LONGEST INCREASING SUBSEQUENCE COMPARISON REPORT",
            "=" * 80,
            "",
            f"Array length: {comparison_data['array_length']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # DP results
        report_lines.append("\nDYNAMIC PROGRAMMING APPROACH:")
        dp_data = comparison_data["dp"]
        if dp_data.get("success", False):
            report_lines.append(f"  LIS length: {dp_data['length']}")
            report_lines.append(f"  LIS sequence: {dp_data['sequence']}")
            report_lines.append(
                f"  Time: {dp_data['time_milliseconds']:.4f} ms "
                f"({dp_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {dp_data.get('error', 'Unknown')}")

        # Binary search results
        report_lines.append("\nBINARY SEARCH OPTIMIZATION APPROACH:")
        bs_data = comparison_data["binary_search"]
        if bs_data.get("success", False):
            report_lines.append(f"  LIS length: {bs_data['length']}")
            report_lines.append(f"  LIS sequence: {bs_data['sequence']}")
            report_lines.append(
                f"  Time: {bs_data['time_milliseconds']:.4f} ms "
                f"({bs_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {bs_data.get('error', 'Unknown')}")

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
            "Dynamic Programming:",
            "  Time Complexity: O(n²) where n=array length",
            "  Space Complexity: O(n) for DP table",
            "  Approach: For each element, check all previous elements",
            "",
            "Binary Search Optimization:",
            "  Time Complexity: O(n log n) where n=array length",
            "  Space Complexity: O(n) for tails array",
            "  Approach: Maintain smallest tail elements, use binary search",
            "",
            "Note: Binary search is faster for large arrays, but DP is",
            "simpler and may be faster for small arrays due to overhead.",
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
        description="Find longest increasing subsequence using dynamic "
        "programming and binary search optimization"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers in the array",
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
        choices=["dp", "binary", "compare"],
        default="compare",
        help="Solution method (default: compare)",
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
        lis_solver = LongestIncreasingSubsequence(config_path=args.config)

        numbers = args.numbers

        logger.info(f"Input: {len(numbers)} numbers")

        if args.method == "compare":
            comparison = lis_solver.compare_approaches(
                numbers, args.iterations
            )

            print(f"\nLongest Increasing Subsequence Comparison:")
            print(f"Array length: {comparison['array_length']}")
            print(f"Iterations: {comparison['iterations']}")
            print("-" * 60)

            # DP approach
            dp_data = comparison["dp"]
            if dp_data.get("success", False):
                seq_str = (
                    str(dp_data["sequence"][:10]) + "..."
                    if len(dp_data["sequence"]) > 10
                    else str(dp_data["sequence"])
                )
                print(
                    f"DP:            "
                    f"length={dp_data['length']:3d}, "
                    f"sequence={seq_str:30s}  "
                    f"({dp_data['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"DP:            Failed - "
                    f"{dp_data.get('error', 'Unknown')}"
                )

            # Binary search approach
            bs_data = comparison["binary_search"]
            if bs_data.get("success", False):
                seq_str = (
                    str(bs_data["sequence"][:10]) + "..."
                    if len(bs_data["sequence"]) > 10
                    else str(bs_data["sequence"])
                )
                print(
                    f"Binary Search: "
                    f"length={bs_data['length']:3d}, "
                    f"sequence={seq_str:30s}  "
                    f"({bs_data['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"Binary Search: Failed - "
                    f"{bs_data.get('error', 'Unknown')}"
                )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = lis_solver.generate_report(
                    comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.method == "dp":
            length, sequence = lis_solver.find_lis_dp(numbers)
            print(f"LIS (DP): length={length}, sequence={sequence}")

        elif args.method == "binary":
            length, sequence = lis_solver.find_lis_binary_search(numbers)
            print(f"LIS (Binary Search): length={length}, sequence={sequence}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
