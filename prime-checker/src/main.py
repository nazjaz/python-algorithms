"""Prime Checker - Trial division method with optimizations.

This module provides functionality to check if a number is prime using trial
division method with optimization for even numbers.
"""

import logging
import logging.handlers
import math
from pathlib import Path
from typing import List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class PrimeChecker:
    """Checks if numbers are prime using optimized trial division."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize PrimeChecker with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.divisions = 0
        self.analysis_data: dict = {}

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

    def is_prime(self, n: int) -> bool:
        """Check if a number is prime using optimized trial division.

        Args:
            n: Integer to check for primality.

        Returns:
            True if n is prime, False otherwise.
        """
        if n < 2:
            logger.debug(f"{n} is not prime (less than 2)")
            return False

        if n == 2:
            logger.debug(f"{n} is prime (smallest prime)")
            return True

        # Optimization: Check if even (except 2)
        if n % 2 == 0:
            logger.debug(f"{n} is not prime (even number, divisible by 2)")
            return False

        self.divisions = 1  # Count the even check
        self.analysis_data = {
            "number": n,
            "is_prime": False,
            "divisions_performed": 0,
            "factors_found": [],
            "square_root": int(math.sqrt(n)),
        }

        # Only check odd divisors up to sqrt(n)
        sqrt_n = int(math.sqrt(n))
        logger.info(
            f"Checking primality of {n} using trial division up to {sqrt_n}"
        )

        for i in range(3, sqrt_n + 1, 2):  # Step by 2 for odd numbers only
            self.divisions += 1
            if n % i == 0:
                self.analysis_data["is_prime"] = False
                self.analysis_data["factors_found"] = [i, n // i]
                logger.info(
                    f"{n} is not prime (divisible by {i} and {n // i})"
                )
                self.analysis_data["divisions_performed"] = self.divisions
                return False
            logger.debug(f"Checked divisor {i}: {n} % {i} != 0")

        self.analysis_data["is_prime"] = True
        self.analysis_data["divisions_performed"] = self.divisions
        logger.info(f"{n} is prime (no divisors found up to {sqrt_n})")
        return True

    def find_primes_in_range(self, start: int, end: int) -> List[int]:
        """Find all prime numbers in a given range.

        Args:
            start: Start of range (inclusive).
            end: End of range (inclusive).

        Returns:
            List of prime numbers in the range.
        """
        if start < 2:
            start = 2

        logger.info(f"Finding primes in range [{start}, {end}]")
        primes = []

        for num in range(start, end + 1):
            if self.is_prime(num):
                primes.append(num)

        logger.info(f"Found {len(primes)} primes in range [{start}, {end}]")
        return primes

    def get_analysis(self) -> dict:
        """Get detailed analysis of the last prime check.

        Returns:
            Dictionary containing analysis data.
        """
        analysis = self.analysis_data.copy()
        analysis["total_divisions"] = self.divisions
        if self.analysis_data.get("number"):
            n = self.analysis_data["number"]
            analysis["optimization_benefit"] = (
                (n - 1) - self.divisions
            ) / max(1, n - 1) * 100 if n > 1 else 0

        return analysis

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate analysis report.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        if not self.analysis_data:
            return "No analysis data available. Run is_prime() first."

        analysis = self.get_analysis()

        report_lines = [
            "=" * 80,
            "PRIME CHECKER ALGORITHM ANALYSIS REPORT",
            "=" * 80,
            "",
            "RESULT",
            "-" * 80,
            f"Number: {analysis['number']}",
            f"Is Prime: {analysis['is_prime']}",
            "",
            "PERFORMANCE METRICS",
            "-" * 80,
            f"Total divisions performed: {analysis['divisions_performed']:,}",
            f"Square root of number: {analysis['square_root']}",
            f"Optimization benefit: {analysis.get('optimization_benefit', 0):.2f}%",
            "",
        ]

        if analysis.get("factors_found"):
            report_lines.extend([
                "FACTORS",
                "-" * 80,
                f"Found factors: {analysis['factors_found']}",
                "",
            ])

        report_lines.extend([
            "ALGORITHM DETAILS",
            "-" * 80,
            "Method: Trial Division with Optimizations",
            "Optimizations:",
            "  - Early check for even numbers (except 2)",
            "  - Only test odd divisors",
            "  - Only test up to square root of number",
            "",
            "COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(√n)",
            "Space Complexity: O(1)",
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
        description="Check if numbers are prime using trial division"
    )
    parser.add_argument(
        "number",
        type=int,
        nargs="?",
        help="Number to check for primality",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-r",
        "--range",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        help="Find all primes in range [START, END]",
    )
    parser.add_argument(
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--analysis",
        action="store_true",
        help="Show detailed analysis",
    )

    args = parser.parse_args()

    try:
        checker = PrimeChecker(config_path=args.config)

        if args.range:
            start, end = args.range
            primes = checker.find_primes_in_range(start, end)
            print(f"\nPrimes in range [{start}, {end}]:")
            print(f"Found {len(primes)} primes: {primes}")

        elif args.number is not None:
            is_prime = checker.is_prime(args.number)

            print(f"\nNumber: {args.number}")
            print(f"Is Prime: {is_prime}")
            print(f"Divisions performed: {checker.divisions}")

            if args.analysis:
                analysis = checker.get_analysis()
                print("\nDetailed Analysis:")
                print(f"  Square root: {analysis['square_root']}")
                print(f"  Optimization benefit: {analysis.get('optimization_benefit', 0):.2f}%")
                if analysis.get("factors_found"):
                    print(f"  Factors: {analysis['factors_found']}")

            if args.report:
                report = checker.generate_report(output_path=args.report)
                print(f"\nReport saved to {args.report}")

        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
