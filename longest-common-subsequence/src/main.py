"""Longest Common Subsequence - Dynamic Programming with Backtracking.

This module provides an implementation of the Longest Common Subsequence (LCS)
algorithm using dynamic programming. It includes backtracking to reconstruct
the actual LCS string and visualization of the DP table.
"""

import argparse
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class LCSCalculator:
    """Calculator for Longest Common Subsequence using dynamic programming."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize calculator with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.dp_table: List[List[int]] = []
        self.backtrack_table: List[List[str]] = []

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

    def lcs_length(self, str1: str, str2: str) -> int:
        """Calculate length of LCS using dynamic programming.

        Builds a DP table where dp[i][j] represents the length of LCS
        of first i characters of str1 and first j characters of str2.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Length of longest common subsequence.
        """
        logger.info(f"Calculating LCS length for '{str1}' and '{str2}'")

        m, n = len(str1), len(str2)

        # Initialize DP table: dp[i][j] = LCS length of str1[0:i] and str2[0:j]
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    # Characters match: extend LCS
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    # Characters don't match: take maximum
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        self.dp_table = dp
        result = dp[m][n]
        logger.info(f"LCS length: {result}")
        return result

    def lcs(self, str1: str, str2: str) -> str:
        """Find longest common subsequence using dynamic programming and backtracking.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Longest common subsequence string.
        """
        logger.info(f"Finding LCS for '{str1}' and '{str2}'")

        # First, build DP table to get lengths
        self.lcs_length(str1, str2)

        # Backtrack to reconstruct LCS
        lcs_string = self._backtrack(str1, str2)

        logger.info(f"LCS: '{lcs_string}'")
        return lcs_string

    def _backtrack(self, str1: str, str2: str) -> str:
        """Backtrack through DP table to reconstruct LCS.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Longest common subsequence string.
        """
        m, n = len(str1), len(str2)
        lcs_chars = []

        i, j = m, n
        while i > 0 and j > 0:
            if str1[i - 1] == str2[j - 1]:
                # Characters match: part of LCS
                lcs_chars.append(str1[i - 1])
                i -= 1
                j -= 1
            elif self.dp_table[i - 1][j] > self.dp_table[i][j - 1]:
                # Move up (str1 character not in LCS)
                i -= 1
            else:
                # Move left (str2 character not in LCS)
                j -= 1

        # Reverse to get correct order
        return "".join(reversed(lcs_chars))

    def lcs_all(self, str1: str, str2: str) -> List[str]:
        """Find all longest common subsequences.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            List of all LCS strings (may contain duplicates).
        """
        logger.info(f"Finding all LCS for '{str1}' and '{str2}'")

        # Build DP table
        self.lcs_length(str1, str2)

        # Find all LCS using backtracking
        all_lcs = self._backtrack_all(str1, str2, len(str1), len(str2))

        # Remove duplicates while preserving order
        seen = set()
        unique_lcs = []
        for lcs_str in all_lcs:
            if lcs_str not in seen:
                seen.add(lcs_str)
                unique_lcs.append(lcs_str)

        logger.info(f"Found {len(unique_lcs)} unique LCS")
        return unique_lcs

    def _backtrack_all(
        self, str1: str, str2: str, i: int, j: int
    ) -> List[str]:
        """Backtrack to find all LCS.

        Args:
            str1: First string.
            str2: Second string.
            i: Current position in str1.
            j: Current position in str2.

        Returns:
            List of all LCS strings from current position.
        """
        if i == 0 or j == 0:
            return [""]

        if str1[i - 1] == str2[j - 1]:
            # Characters match: extend all LCS
            sub_lcs = self._backtrack_all(str1, str2, i - 1, j - 1)
            return [lcs + str1[i - 1] for lcs in sub_lcs]

        result = []
        if self.dp_table[i - 1][j] >= self.dp_table[i][j - 1]:
            # Move up
            result.extend(self._backtrack_all(str1, str2, i - 1, j))
        if self.dp_table[i][j - 1] >= self.dp_table[i - 1][j]:
            # Move left
            result.extend(self._backtrack_all(str1, str2, i, j - 1))

        return result

    def visualize_dp_table(self, str1: str, str2: str) -> str:
        """Generate visualization of DP table.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            String representation of DP table.
        """
        if not self.dp_table:
            self.lcs_length(str1, str2)

        lines = []
        lines.append("DP Table:")
        lines.append(" " * 4 + "  " + " ".join(f"{c:3}" for c in " " + str2))

        for i in range(len(self.dp_table)):
            if i == 0:
                prefix = "  "
            else:
                prefix = str1[i - 1] + " "
            row = " ".join(f"{val:3}" for val in self.dp_table[i])
            lines.append(prefix + row)

        return "\n".join(lines)

    def calculate_with_details(
        self, str1: str, str2: str
    ) -> Dict[str, any]:
        """Calculate LCS with detailed information.

        Args:
            str1: First string.
            str2: Second string.

        Returns:
            Dictionary containing detailed LCS information.
        """
        logger.info(f"Calculating LCS with details for '{str1}' and '{str2}'")

        length = self.lcs_length(str1, str2)
        lcs_string = self.lcs(str1, str2)
        dp_visualization = self.visualize_dp_table(str1, str2)

        result = {
            "string1": str1,
            "string2": str2,
            "length": length,
            "lcs": lcs_string,
            "dp_table": [row[:] for row in self.dp_table],
            "dp_visualization": dp_visualization,
            "string1_length": len(str1),
            "string2_length": len(str2),
        }

        logger.info(f"LCS details: length={length}, lcs='{lcs_string}'")
        return result

    def generate_report(
        self, result: Dict[str, any], output_path: Optional[str] = None
    ) -> str:
        """Generate detailed LCS analysis report.

        Args:
            result: Result dictionary from calculate_with_details.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "LONGEST COMMON SUBSEQUENCE (LCS) ANALYSIS REPORT",
            "=" * 80,
            "",
            "INPUT STRINGS",
            "-" * 80,
            f"String 1: {result['string1']} (length: {result['string1_length']})",
            f"String 2: {result['string2']} (length: {result['string2_length']})",
            "",
            "RESULTS",
            "-" * 80,
            f"LCS Length: {result['length']}",
            f"LCS String: '{result['lcs']}'",
            "",
            "DYNAMIC PROGRAMMING TABLE",
            "-" * 80,
            result["dp_visualization"],
            "",
            "ALGORITHM DETAILS",
            "-" * 80,
            "Method: Dynamic Programming with Backtracking",
            "",
            "Dynamic Programming Approach:",
            "  1. Build DP table: dp[i][j] = LCS length of str1[0:i] and str2[0:j]",
            "  2. Recurrence relation:",
            "     - If str1[i-1] == str2[j-1]: dp[i][j] = dp[i-1][j-1] + 1",
            "     - Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])",
            "  3. Backtrack through table to reconstruct LCS",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(m * n) where:",
            "  - m = length of string 1",
            "  - n = length of string 2",
            "  - Filling DP table: O(m * n)",
            "  - Backtracking: O(m + n)",
            "",
            "Space Complexity: O(m * n) for DP table",
            "  - Can be optimized to O(min(m, n)) using space optimization",
            "",
            "PROPERTIES",
            "-" * 80,
            "- Subsequence (not substring): characters don't need to be contiguous",
            "- Multiple LCS may exist for same pair of strings",
            "- LCS is not necessarily unique",
            "- DP table stores optimal substructure solutions",
            "",
            "APPLICATIONS",
            "-" * 80,
            "1. String similarity and comparison",
            "2. DNA sequence alignment (bioinformatics)",
            "3. Version control (diff algorithms)",
            "4. Text comparison and plagiarism detection",
            "5. Spell checking and correction",
            "6. File comparison utilities",
        ]

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
        description="Find longest common subsequence using dynamic programming"
    )
    parser.add_argument(
        "string1",
        type=str,
        nargs="?",
        default=None,
        help="First string",
    )
    parser.add_argument(
        "string2",
        type=str,
        nargs="?",
        default=None,
        help="Second string",
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
        help="Show DP table visualization",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Find all LCS (may be slow for large strings)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example strings",
    )

    args = parser.parse_args()

    try:
        calculator = LCSCalculator(config_path=args.config)

        if args.demo or args.string1 is None or args.string2 is None:
            # Run demonstration
            print("\n=== Longest Common Subsequence Demonstration ===\n")

            examples = [
                ("ABCDGH", "AEDFHR"),
                ("AGGTAB", "GXTXAYB"),
                ("ABCDEF", "ACDF"),
                ("ABCD", "ACBD"),
                ("ABC", "AC"),
            ]

            for str1, str2 in examples:
                print(f"String 1: {str1}")
                print(f"String 2: {str2}")

                if args.all:
                    all_lcs = calculator.lcs_all(str1, str2)
                    print(f"All LCS: {all_lcs}")
                else:
                    lcs = calculator.lcs(str1, str2)
                    length = calculator.lcs_length(str1, str2)
                    print(f"LCS: '{lcs}' (length: {length})")

                if args.visualize:
                    print("\n" + calculator.visualize_dp_table(str1, str2))

                print()

        else:
            # Calculate LCS for provided strings
            if args.all:
                all_lcs = calculator.lcs_all(args.string1, args.string2)
                print(f"\nAll LCS: {all_lcs}")
            else:
                lcs = calculator.lcs(args.string1, args.string2)
                length = calculator.lcs_length(args.string1, args.string2)
                print(f"\nLCS: '{lcs}' (length: {length})")

            if args.visualize:
                print("\n" + calculator.visualize_dp_table(args.string1, args.string2))

            if args.report:
                result = calculator.calculate_with_details(
                    args.string1, args.string2
                )
                report = calculator.generate_report(
                    result, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
