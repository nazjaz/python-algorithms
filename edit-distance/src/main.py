"""Edit Distance (Levenshtein Distance) Problem Solver.

This module provides functionality to calculate edit distance between two
strings using dynamic programming with both standard and space-optimized
approaches. Edit distance is the minimum number of operations (insert,
delete, replace) needed to transform one string into another.
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


class EditDistance:
    """Calculates edit distance using dynamic programming."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize EditDistance with configuration.

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

    def calculate_dp(
        self, str1: str, str2: str
    ) -> Tuple[int, List[List[int]]]:
        """Calculate edit distance using standard dynamic programming.

        Uses O(m*n) space for DP table where m and n are string lengths.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Tuple containing:
                - Edit distance (minimum operations)
                - DP table for visualization

        Time Complexity: O(m*n) where m=len(str1), n=len(str2)
        Space Complexity: O(m*n)
        """
        m, n = len(str1), len(str2)

        logger.info(f"Calculating edit distance (DP): '{str1}' -> '{str2}'")

        # DP table: dp[i][j] = edit distance between str1[0:i] and str2[0:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        logger.debug("  Initialized base cases")

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    # Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Take minimum of three operations
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # Delete from str1
                        dp[i][j - 1],      # Insert into str1
                        dp[i - 1][j - 1],  # Replace in str1
                    )
                logger.debug(
                    f"    dp[{i}][{j}] = {dp[i][j]} "
                    f"(str1[{i-1}]='{str1[i-1]}', "
                    f"str2[{j-1}]='{str2[j-1]}')"
                )

        distance = dp[m][n]
        logger.info(f"Edit distance: {distance}")
        return distance, dp

    def calculate_optimized(
        self, str1: str, str2: str
    ) -> Tuple[int, List[int]]:
        """Calculate edit distance using space-optimized DP.

        Uses O(min(m,n)) space by keeping only two rows of DP table.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Tuple containing:
                - Edit distance (minimum operations)
                - Last row of DP table (for verification)

        Time Complexity: O(m*n) where m=len(str1), n=len(str2)
        Space Complexity: O(min(m,n))
        """
        m, n = len(str1), len(str2)

        # Use shorter string for column dimension to minimize space
        if m < n:
            str1, str2 = str2, str1
            m, n = n, m

        logger.info(
            f"Calculating edit distance (Optimized): '{str1}' -> '{str2}' "
            f"(space: O({n}))"
        )

        # Only need two rows: previous and current
        prev = list(range(n + 1))
        curr = [0] * (n + 1)

        logger.debug("  Initialized base row")

        # Fill DP table row by row
        for i in range(1, m + 1):
            curr[0] = i  # Base case: delete all characters from str1
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    # Characters match, no operation needed
                    curr[j] = prev[j - 1]
                else:
                    # Take minimum of three operations
                    curr[j] = 1 + min(
                        prev[j],        # Delete from str1
                        curr[j - 1],    # Insert into str1
                        prev[j - 1],    # Replace in str1
                    )
                logger.debug(
                    f"    curr[{j}] = {curr[j]} "
                    f"(str1[{i-1}]='{str1[i-1]}', "
                    f"str2[{j-1}]='{str2[j-1]}')"
                )

            # Swap rows for next iteration
            prev, curr = curr, prev

        distance = prev[n]
        logger.info(f"Edit distance: {distance}")
        return distance, prev

    def get_distance_dp(self, str1: str, str2: str) -> int:
        """Get edit distance using standard DP.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Edit distance.
        """
        distance, _ = self.calculate_dp(str1, str2)
        return distance

    def get_distance_optimized(self, str1: str, str2: str) -> int:
        """Get edit distance using space-optimized DP.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Edit distance.
        """
        distance, _ = self.calculate_optimized(str1, str2)
        return distance

    def get_operations(
        self, str1: str, str2: str, dp: List[List[int]]
    ) -> List[str]:
        """Get sequence of operations to transform str1 to str2.

        Args:
            str1: First string.
            str2: Second string.
            dp: DP table from calculate_dp().

        Returns:
            List of operation descriptions.
        """
        m, n = len(str1), len(str2)
        operations: List[str] = []
        i, j = m, n

        logger.debug("Reconstructing operations")

        while i > 0 or j > 0:
            if i > 0 and j > 0 and str1[i - 1] == str2[j - 1]:
                # Characters match, no operation
                i -= 1
                j -= 1
                logger.debug(f"  Match: '{str1[i]}' == '{str2[j]}'")
            elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                # Replace operation
                operations.append(
                    f"Replace '{str1[i-1]}' at position {i-1} with '{str2[j-1]}'"
                )
                i -= 1
                j -= 1
                logger.debug(f"  Replace: '{str1[i]}' -> '{str2[j]}'")
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                # Delete operation
                operations.append(f"Delete '{str1[i-1]}' at position {i-1}")
                i -= 1
                logger.debug(f"  Delete: '{str1[i]}'")
            elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
                # Insert operation
                operations.append(
                    f"Insert '{str2[j-1]}' at position {i}"
                )
                j -= 1
                logger.debug(f"  Insert: '{str2[j]}' at position {i}")
            else:
                # Fallback (should not happen)
                if i > 0:
                    i -= 1
                if j > 0:
                    j -= 1

        operations.reverse()
        return operations

    def compare_approaches(
        self, str1: str, str2: str, iterations: int = 1
    ) -> Dict[str, any]:
        """Compare standard DP and space-optimized approaches.

        Args:
            str1: First string.
            str2: Second string.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing comparison data.
        """
        logger.info(
            f"Comparing approaches: '{str1}' -> '{str2}', "
            f"iterations={iterations}"
        )

        results = {
            "str1_length": len(str1),
            "str2_length": len(str2),
            "iterations": iterations,
            "dp": {},
            "optimized": {},
        }

        # Standard DP approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                distance_dp, dp_table = self.calculate_dp(str1, str2)
            dp_time = time.perf_counter() - start_time

            results["dp"] = {
                "distance": distance_dp,
                "space_used": len(str1) * len(str2),
                "time_seconds": dp_time / iterations,
                "time_milliseconds": (dp_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"DP approach failed: {e}")
            results["dp"] = {"success": False, "error": str(e)}

        # Space-optimized approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                distance_opt, last_row = self.calculate_optimized(str1, str2)
            opt_time = time.perf_counter() - start_time

            results["optimized"] = {
                "distance": distance_opt,
                "space_used": min(len(str1), len(str2)) + 1,
                "time_seconds": opt_time / iterations,
                "time_milliseconds": (opt_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Optimized approach failed: {e}")
            results["optimized"] = {"success": False, "error": str(e)}

        # Verify results match
        if (
            results["dp"].get("success", False)
            and results["optimized"].get("success", False)
        ):
            if results["dp"]["distance"] == results["optimized"]["distance"]:
                logger.info("Both approaches produced identical distances")
            else:
                logger.warning("Distances differ between approaches!")

            # Calculate space savings
            space_savings = (
                (results["dp"]["space_used"] - results["optimized"]["space_used"])
                / results["dp"]["space_used"]
                * 100
            )
            results["space_savings_percent"] = space_savings

            # Determine fastest
            dp_time = results["dp"]["time_seconds"]
            opt_time = results["optimized"]["time_seconds"]
            if dp_time < opt_time:
                results["fastest"] = "dp"
                results["fastest_time"] = dp_time
            else:
                results["fastest"] = "optimized"
                results["fastest_time"] = opt_time

        return results

    def generate_report(
        self,
        comparison_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate comparison report for edit distance approaches.

        Args:
            comparison_data: Comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "EDIT DISTANCE (LEVENSHTEIN DISTANCE) COMPARISON REPORT",
            "=" * 80,
            "",
            f"String 1 length: {comparison_data['str1_length']}",
            f"String 2 length: {comparison_data['str2_length']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # DP results
        report_lines.append("\nSTANDARD DYNAMIC PROGRAMMING:")
        dp_data = comparison_data["dp"]
        if dp_data.get("success", False):
            report_lines.append(f"  Edit distance: {dp_data['distance']}")
            report_lines.append(f"  Space used: {dp_data['space_used']} cells")
            report_lines.append(
                f"  Time: {dp_data['time_milliseconds']:.4f} ms "
                f"({dp_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {dp_data.get('error', 'Unknown')}")

        # Optimized results
        report_lines.append("\nSPACE-OPTIMIZED DYNAMIC PROGRAMMING:")
        opt_data = comparison_data["optimized"]
        if opt_data.get("success", False):
            report_lines.append(f"  Edit distance: {opt_data['distance']}")
            report_lines.append(f"  Space used: {opt_data['space_used']} cells")
            report_lines.append(
                f"  Time: {opt_data['time_milliseconds']:.4f} ms "
                f"({opt_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {opt_data.get('error', 'Unknown')}")

        if "space_savings_percent" in comparison_data:
            report_lines.extend([
                "",
                "SPACE OPTIMIZATION",
                "-" * 80,
                f"Space savings: {comparison_data['space_savings_percent']:.2f}%",
            ])

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
            "Standard DP:",
            "  Time Complexity: O(m*n) where m=len(str1), n=len(str2)",
            "  Space Complexity: O(m*n) for DP table",
            "  Operations: Insert, Delete, Replace (all cost 1)",
            "",
            "Space-Optimized DP:",
            "  Time Complexity: O(m*n) where m=len(str1), n=len(str2)",
            "  Space Complexity: O(min(m,n)) using two rows",
            "  Operations: Insert, Delete, Replace (all cost 1)",
            "",
            "Note: Space-optimized version uses O(min(m,n)) space by keeping",
            "only two rows of the DP table, significantly reducing memory",
            "usage for large strings while maintaining same time complexity.",
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
        description="Calculate edit distance (Levenshtein distance) using "
        "dynamic programming with space optimization"
    )
    parser.add_argument(
        "str1",
        type=str,
        help="First string",
    )
    parser.add_argument(
        "str2",
        type=str,
        help="Second string",
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
        choices=["dp", "optimized", "compare"],
        default="compare",
        help="Solution method (default: compare)",
    )
    parser.add_argument(
        "-o",
        "--operations",
        action="store_true",
        help="Show sequence of operations",
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
        ed = EditDistance(config_path=args.config)

        logger.info(f"Input: '{args.str1}' -> '{args.str2}'")

        if args.method == "compare":
            comparison = ed.compare_approaches(
                args.str1, args.str2, args.iterations
            )

            print(f"\nEdit Distance Comparison:")
            print(f"String 1: '{args.str1}' (length: {comparison['str1_length']})")
            print(f"String 2: '{args.str2}' (length: {comparison['str2_length']})")
            print("-" * 60)

            # DP approach
            dp_data = comparison["dp"]
            if dp_data.get("success", False):
                print(
                    f"DP:            "
                    f"distance={dp_data['distance']:3d}, "
                    f"space={dp_data['space_used']:6d}  "
                    f"({dp_data['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"DP:            Failed - "
                    f"{dp_data.get('error', 'Unknown')}"
                )

            # Optimized approach
            opt_data = comparison["optimized"]
            if opt_data.get("success", False):
                print(
                    f"Optimized:     "
                    f"distance={opt_data['distance']:3d}, "
                    f"space={opt_data['space_used']:6d}  "
                    f"({opt_data['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"Optimized:     Failed - "
                    f"{opt_data.get('error', 'Unknown')}"
                )

            if "space_savings_percent" in comparison:
                print(
                    f"\nSpace savings: "
                    f"{comparison['space_savings_percent']:.2f}%"
                )

            if "fastest" in comparison:
                print(f"Fastest: {comparison['fastest']}")

            if args.operations:
                distance, dp_table = ed.calculate_dp(args.str1, args.str2)
                operations = ed.get_operations(args.str1, args.str2, dp_table)
                print(f"\nOperations to transform '{args.str1}' -> '{args.str2}':")
                for i, op in enumerate(operations, 1):
                    print(f"  {i}. {op}")

            if args.report:
                report = ed.generate_report(
                    comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.method == "dp":
            distance, dp_table = ed.calculate_dp(args.str1, args.str2)
            print(f"Edit distance (DP): {distance}")
            if args.operations:
                operations = ed.get_operations(args.str1, args.str2, dp_table)
                print("\nOperations:")
                for i, op in enumerate(operations, 1):
                    print(f"  {i}. {op}")

        elif args.method == "optimized":
            distance, _ = ed.calculate_optimized(args.str1, args.str2)
            print(f"Edit distance (Optimized): {distance}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
