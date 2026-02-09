"""Greatest Common Divisor Calculator - Euclidean Algorithm Implementation.

This module provides GCD calculation using the Euclidean algorithm and Extended
Euclidean algorithm for finding linear combinations. The Extended Euclidean
algorithm finds coefficients x and y such that gcd(a, b) = ax + by.
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


class GCDCalculator:
    """Calculator for GCD using Euclidean and Extended Euclidean algorithms."""

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

    def gcd(self, a: int, b: int) -> int:
        """Calculate GCD using Euclidean algorithm.

        The Euclidean algorithm is based on the principle that gcd(a, b) =
        gcd(b, a mod b). This is repeated until b becomes 0, at which point
        a is the GCD.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            Greatest common divisor of a and b.

        Raises:
            ValueError: If both a and b are zero.

        Example:
            >>> calculator = GCDCalculator()
            >>> calculator.gcd(48, 18)
            6
            >>> calculator.gcd(17, 13)
            1
        """
        logger.info(f"Calculating GCD of {a} and {b}")

        # Handle zero cases
        if a == 0 and b == 0:
            raise ValueError("GCD of (0, 0) is undefined")

        # GCD is always positive
        a = abs(a)
        b = abs(b)

        # Euclidean algorithm: gcd(a, b) = gcd(b, a mod b)
        while b != 0:
            logger.debug(f"gcd({a}, {b}) = gcd({b}, {a % b})")
            a, b = b, a % b

        result = a
        logger.info(f"GCD result: {result}")
        return result

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """Calculate GCD and coefficients using Extended Euclidean algorithm.

        Finds gcd(a, b) and coefficients x, y such that:
        gcd(a, b) = ax + by

        This is useful for solving linear Diophantine equations and finding
        modular inverses.

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            Tuple (gcd, x, y) where:
                - gcd: Greatest common divisor of a and b
                - x: Coefficient for a in linear combination
                - y: Coefficient for b in linear combination

        Raises:
            ValueError: If both a and b are zero.

        Example:
            >>> calculator = GCDCalculator()
            >>> gcd, x, y = calculator.extended_gcd(48, 18)
            >>> gcd == 48*x + 18*y
            True
        """
        logger.info(f"Calculating extended GCD of {a} and {b}")

        # Handle zero cases
        if a == 0 and b == 0:
            raise ValueError("GCD of (0, 0) is undefined")

        # Store original signs for result adjustment
        original_a = a
        original_b = b

        # Work with absolute values
        a = abs(a)
        b = abs(b)

        # Extended Euclidean algorithm
        # Maintain: a*x1 + b*y1 = r1 and a*x2 + b*y2 = r2
        # Initialize: r1 = a, r2 = b
        x1, y1 = 1, 0  # Coefficients for a
        x2, y2 = 0, 1  # Coefficients for b
        r1, r2 = a, b

        while r2 != 0:
            # Calculate quotient
            q = r1 // r2

            # Update remainders: r1 = r2, r2 = r1 mod r2
            r1, r2 = r2, r1 % r2

            # Update coefficients using matrix multiplication
            # [x1, y1] = [x1, y1] - q * [x2, y2]
            x1, y1, x2, y2 = x2, y2, x1 - q * x2, y1 - q * y2

            logger.debug(
                f"Step: gcd({a}, {b}), coefficients: ({x1}, {y1})"
            )

        # Adjust signs based on original inputs
        if original_a < 0:
            x1 = -x1
        if original_b < 0:
            y1 = -y1

        gcd_result = r1
        logger.info(
            f"Extended GCD result: gcd={gcd_result}, x={x1}, y={y1}"
        )
        logger.info(f"Verification: {original_a}*{x1} + {original_b}*{y1} = {gcd_result}")

        return (gcd_result, x1, y1)

    def gcd_multiple(self, numbers: List[int]) -> int:
        """Calculate GCD of multiple numbers.

        Uses the property: gcd(a, b, c) = gcd(gcd(a, b), c)

        Args:
            numbers: List of integers.

        Returns:
            Greatest common divisor of all numbers.

        Raises:
            ValueError: If list is empty or all numbers are zero.
        """
        logger.info(f"Calculating GCD of multiple numbers: {numbers}")

        if not numbers:
            raise ValueError("Cannot calculate GCD of empty list")

        # Filter out zeros (they don't affect GCD)
        non_zero = [n for n in numbers if n != 0]

        if not non_zero:
            raise ValueError("Cannot calculate GCD when all numbers are zero")

        # Start with first number
        result = abs(non_zero[0])

        # Apply gcd iteratively: gcd(a, b, c) = gcd(gcd(a, b), c)
        for num in non_zero[1:]:
            result = self.gcd(result, abs(num))
            logger.debug(f"Intermediate GCD: {result}")

        logger.info(f"GCD of multiple numbers: {result}")
        return result

    def lcm(self, a: int, b: int) -> int:
        """Calculate Least Common Multiple using GCD.

        Uses the relationship: lcm(a, b) = |a * b| / gcd(a, b)

        Args:
            a: First integer.
            b: Second integer.

        Returns:
            Least common multiple of a and b.

        Raises:
            ValueError: If both a and b are zero.
        """
        logger.info(f"Calculating LCM of {a} and {b}")

        if a == 0 and b == 0:
            raise ValueError("LCM of (0, 0) is undefined")

        gcd_result = self.gcd(a, b)
        lcm_result = abs(a * b) // gcd_result

        logger.info(f"LCM result: {lcm_result}")
        return lcm_result

    def modular_inverse(self, a: int, m: int) -> Optional[int]:
        """Find modular inverse of a modulo m using Extended Euclidean.

        Finds x such that (a * x) mod m = 1, if it exists.
        The modular inverse exists only if gcd(a, m) = 1.

        Args:
            a: Integer to find inverse for.
            m: Modulus.

        Returns:
            Modular inverse of a modulo m, or None if it doesn't exist.

        Example:
            >>> calculator = GCDCalculator()
            >>> calculator.modular_inverse(3, 11)
            4
            >>> calculator.modular_inverse(2, 4)
            None
        """
        logger.info(f"Finding modular inverse of {a} modulo {m}")

        if m <= 0:
            raise ValueError("Modulus must be positive")

        gcd_result, x, _ = self.extended_gcd(a, m)

        if gcd_result != 1:
            logger.warning(
                f"Modular inverse doesn't exist: gcd({a}, {m}) = {gcd_result}"
            )
            return None

        # Ensure result is in range [0, m-1]
        inverse = x % m
        logger.info(f"Modular inverse: {inverse}")
        return inverse

    def verify_linear_combination(
        self, a: int, b: int, gcd_val: int, x: int, y: int
    ) -> bool:
        """Verify that gcd(a, b) = ax + by.

        Args:
            a: First integer.
            b: Second integer.
            gcd_val: GCD value to verify.
            x: Coefficient for a.
            y: Coefficient for b.

        Returns:
            True if linear combination is correct, False otherwise.
        """
        calculated = a * x + b * y
        is_valid = calculated == gcd_val

        logger.info(
            f"Verification: {a}*{x} + {b}*{y} = {calculated}, "
            f"Expected: {gcd_val}, Valid: {is_valid}"
        )

        return is_valid

    def calculate_with_details(
        self, a: int, b: int, use_extended: bool = False
    ) -> Dict[str, any]:
        """Calculate GCD with detailed results.

        Args:
            a: First integer.
            b: Second integer.
            use_extended: If True, use extended algorithm.

        Returns:
            Dictionary containing calculation details.
        """
        logger.info(f"Calculating GCD with details: a={a}, b={b}")

        gcd_result = self.gcd(a, b)
        result: Dict[str, any] = {
            "a": a,
            "b": b,
            "gcd": gcd_result,
            "lcm": self.lcm(a, b),
        }

        if use_extended:
            gcd_ext, x, y = self.extended_gcd(a, b)
            result["extended_gcd"] = {
                "gcd": gcd_ext,
                "x": x,
                "y": y,
                "linear_combination": f"{a}*{x} + {b}*{y} = {gcd_ext}",
                "verified": self.verify_linear_combination(a, b, gcd_ext, x, y),
            }

        logger.info(f"Calculation details: {result}")
        return result

    def generate_report(
        self,
        a: int,
        b: int,
        result: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate calculation report.

        Args:
            a: First integer.
            b: Second integer.
            result: Calculation result dictionary from calculate_with_details.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "GCD CALCULATION REPORT",
            "=" * 80,
            "",
            f"Input: a = {a}, b = {b}",
            f"GCD: {result['gcd']}",
            f"LCM: {result['lcm']}",
            "",
            "EUCLIDEAN ALGORITHM",
            "-" * 80,
            "The Euclidean algorithm finds GCD by repeatedly applying:",
            "  gcd(a, b) = gcd(b, a mod b)",
            "",
            "Algorithm Steps:",
            "1. Start with two numbers a and b",
            "2. While b != 0:",
            "   - Set a = b, b = a mod b",
            "3. When b = 0, a is the GCD",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(log min(a, b))",
            "Space Complexity: O(1)",
            "",
            "PROPERTIES",
            "-" * 80,
            f"GCD({a}, {b}) = {result['gcd']}",
            f"LCM({a}, {b}) = {result['lcm']}",
            f"GCD * LCM = {result['gcd']} * {result['lcm']} = "
            f"{result['gcd'] * result['lcm']}",
            f"a * b = {a} * {b} = {a * b}",
            "",
        ]

        if "extended_gcd" in result:
            ext = result["extended_gcd"]
            report_lines.extend([
                "EXTENDED EUCLIDEAN ALGORITHM",
                "-" * 80,
                "The Extended Euclidean algorithm finds coefficients x and y such that:",
                "  gcd(a, b) = ax + by",
                "",
                "Results:",
                f"  GCD: {ext['gcd']}",
                f"  Coefficient x: {ext['x']}",
                f"  Coefficient y: {ext['y']}",
                f"  Linear combination: {ext['linear_combination']}",
                f"  Verified: {ext['verified']}",
                "",
                "APPLICATIONS",
                "-" * 80,
                "1. Solving linear Diophantine equations",
                "2. Finding modular inverses",
                "3. Cryptography (RSA algorithm)",
                "4. Chinese Remainder Theorem",
                "",
            ])

        report_lines.extend([
            "USE CASES",
            "-" * 80,
            "1. Simplifying fractions",
            "2. Finding common factors",
            "3. Cryptography and number theory",
            "4. Algorithm optimization",
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
    parser = argparse.ArgumentParser(
        description="Calculate GCD using Euclidean algorithm"
    )
    parser.add_argument(
        "a",
        type=int,
        nargs="?",
        default=None,
        help="First integer",
    )
    parser.add_argument(
        "b",
        type=int,
        nargs="?",
        default=None,
        help="Second integer",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-e",
        "--extended",
        action="store_true",
        help="Use Extended Euclidean algorithm",
    )
    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show detailed calculation results",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for calculation report",
    )
    parser.add_argument(
        "--multiple",
        nargs="+",
        type=int,
        help="Calculate GCD of multiple numbers",
    )
    parser.add_argument(
        "--lcm",
        action="store_true",
        help="Calculate LCM instead of GCD",
    )
    parser.add_argument(
        "--modular-inverse",
        metavar="MODULUS",
        type=int,
        help="Find modular inverse (requires --extended)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example calculations",
    )

    args = parser.parse_args()

    try:
        calculator = GCDCalculator(config_path=args.config)

        if args.demo or (args.a is None and args.b is None and not args.multiple):
            # Run demonstration
            print("\n=== GCD Calculator Demonstration ===\n")

            examples = [
                (48, 18),
                (17, 13),
                (100, 25),
                (56, 42),
                (17, 5),
            ]

            for a, b in examples:
                gcd_result = calculator.gcd(a, b)
                print(f"GCD({a}, {b}) = {gcd_result}")

                if args.extended or args.demo:
                    gcd_ext, x, y = calculator.extended_gcd(a, b)
                    print(f"  Extended: {a}*{x} + {b}*{y} = {gcd_ext}")
                print()

        elif args.multiple:
            # Calculate GCD of multiple numbers
            gcd_result = calculator.gcd_multiple(args.multiple)
            print(f"\nGCD({', '.join(map(str, args.multiple))}) = {gcd_result}")

            if args.details:
                print(f"\nCalculation method: gcd(a, b, c) = gcd(gcd(a, b), c)")

        elif args.modular_inverse is not None:
            # Find modular inverse
            if args.a is None:
                print("Error: First number required for modular inverse")
                return

            inverse = calculator.modular_inverse(args.a, args.modular_inverse)
            if inverse is not None:
                print(
                    f"\nModular inverse of {args.a} modulo {args.modular_inverse}: "
                    f"{inverse}"
                )
                print(f"Verification: ({args.a} * {inverse}) mod {args.modular_inverse} = "
                      f"{(args.a * inverse) % args.modular_inverse}")
            else:
                print(
                    f"\nModular inverse of {args.a} modulo {args.modular_inverse} "
                    f"does not exist (gcd != 1)"
                )

        else:
            # Standard GCD calculation
            if args.a is None or args.b is None:
                print("Error: Two numbers required for GCD calculation")
                return

            a, b = args.a, args.b

            if args.lcm:
                result = calculator.lcm(a, b)
                print(f"\nLCM({a}, {b}) = {result}")
            else:
                if args.details or args.extended:
                    result_dict = calculator.calculate_with_details(
                        a, b, use_extended=args.extended
                    )
                    print(f"\nGCD({a}, {b}) = {result_dict['gcd']}")
                    print(f"LCM({a}, {b}) = {result_dict['lcm']}")

                    if args.extended:
                        ext = result_dict["extended_gcd"]
                        print(f"\nExtended Euclidean Algorithm:")
                        print(f"  GCD: {ext['gcd']}")
                        print(f"  Coefficients: x = {ext['x']}, y = {ext['y']}")
                        print(f"  Linear combination: {ext['linear_combination']}")
                        print(f"  Verified: {ext['verified']}")
                else:
                    gcd_result = calculator.gcd(a, b)
                    print(f"\nGCD({a}, {b}) = {gcd_result}")

            if args.report:
                if not args.details and not args.extended:
                    result_dict = calculator.calculate_with_details(
                        a, b, use_extended=args.extended
                    )
                else:
                    result_dict = calculator.calculate_with_details(
                        a, b, use_extended=args.extended
                    )
                report = calculator.generate_report(
                    a, b, result_dict, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
