"""Fast Exponentiation Calculator - Exponentiation by Squaring.

This module provides fast exponentiation using the exponentiation by squaring
algorithm, which calculates a^n in O(log n) time complexity instead of
O(n) time. It includes both iterative and recursive implementations with
modular exponentiation support and time complexity analysis.
"""

import argparse
import logging
import logging.handlers
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class FastExponentiationCalculator:
    """Calculator for fast exponentiation with time complexity analysis."""

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
        self.operation_steps: List[Dict[str, Any]] = []

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

    def power_naive(self, base: float, exponent: int) -> float:
        """Calculate power using naive method (O(n) time).

        Args:
            base: Base number.
            exponent: Exponent (must be non-negative integer).

        Returns:
            Result of base raised to exponent.

        Raises:
            ValueError: If exponent is negative.
        """
        if exponent < 0:
            raise ValueError("Exponent must be non-negative for naive method")

        logger.info(f"Calculating {base}^{exponent} using naive method")
        result = 1.0
        for _ in range(exponent):
            result *= base
        logger.debug(f"Naive result: {result}")
        return result

    def power_fast_recursive(
        self, base: float, exponent: int, track_steps: bool = False
    ) -> float:
        """Calculate power using fast exponentiation (recursive, O(log n)).

        Uses exponentiation by squaring:
        - If exponent is even: base^exponent = (base^(exponent/2))^2
        - If exponent is odd: base^exponent = base * (base^((exponent-1)/2))^2

        Args:
            base: Base number.
            exponent: Exponent (must be non-negative integer).
            track_steps: If True, track algorithm steps.

        Returns:
            Result of base raised to exponent.

        Raises:
            ValueError: If exponent is negative.
        """
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")

        logger.info(f"Calculating {base}^{exponent} using fast recursive method")

        def _power_recursive(b: float, exp: int, depth: int = 0) -> float:
            """Recursive helper function."""
            if exp == 0:
                if track_steps:
                    self.operation_steps.append({
                        "base": b,
                        "exponent": exp,
                        "result": 1.0,
                        "operation": "base case",
                        "depth": depth,
                    })
                return 1.0

            if exp == 1:
                if track_steps:
                    self.operation_steps.append({
                        "base": b,
                        "exponent": exp,
                        "result": b,
                        "operation": "base case",
                        "depth": depth,
                    })
                return b

            # Recursive case: use exponentiation by squaring
            if exp % 2 == 0:
                # Even exponent: (base^(exp/2))^2
                half_power = _power_recursive(b, exp // 2, depth + 1)
                result = half_power * half_power
                if track_steps:
                    self.operation_steps.append({
                        "base": b,
                        "exponent": exp,
                        "half_exponent": exp // 2,
                        "half_result": half_power,
                        "result": result,
                        "operation": "even: square",
                        "depth": depth,
                    })
                return result
            else:
                # Odd exponent: base * (base^((exp-1)/2))^2
                half_power = _power_recursive(b, (exp - 1) // 2, depth + 1)
                result = b * half_power * half_power
                if track_steps:
                    self.operation_steps.append({
                        "base": b,
                        "exponent": exp,
                        "half_exponent": (exp - 1) // 2,
                        "half_result": half_power,
                        "result": result,
                        "operation": "odd: base * square",
                        "depth": depth,
                    })
                return result

        result = _power_recursive(base, exponent)
        logger.info(f"Fast recursive result: {result}")
        return result

    def power_fast_iterative(
        self, base: float, exponent: int, track_steps: bool = False
    ) -> float:
        """Calculate power using fast exponentiation (iterative, O(log n)).

        Uses exponentiation by squaring iteratively:
        - Process exponent bits from right to left
        - Square result and multiply by base when bit is 1

        Args:
            base: Base number.
            exponent: Exponent (must be non-negative integer).
            track_steps: If True, track algorithm steps.

        Returns:
            Result of base raised to exponent.

        Raises:
            ValueError: If exponent is negative.
        """
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")

        logger.info(f"Calculating {base}^{exponent} using fast iterative method")

        if exponent == 0:
            return 1.0

        result = 1.0
        current_base = base
        current_exp = exponent
        step = 0

        while current_exp > 0:
            if track_steps:
                self.operation_steps.append({
                    "step": step,
                    "exponent": current_exp,
                    "exponent_binary": bin(current_exp),
                    "current_base": current_base,
                    "result": result,
                    "bit": current_exp % 2,
                })

            if current_exp % 2 == 1:
                result *= current_base
                if track_steps:
                    self.operation_steps[-1]["operation"] = "multiply"
                    self.operation_steps[-1]["result_after"] = result

            current_base *= current_base
            current_exp //= 2
            step += 1

            if track_steps and current_exp > 0:
                self.operation_steps[-1]["next_base"] = current_base
                self.operation_steps[-1]["next_exponent"] = current_exp

        logger.info(f"Fast iterative result: {result}")
        return result

    def power_modular(
        self, base: int, exponent: int, modulus: int, track_steps: bool = False
    ) -> int:
        """Calculate modular exponentiation (base^exponent mod modulus).

        Uses fast exponentiation with modular arithmetic to handle large numbers.

        Args:
            base: Base number (integer).
            exponent: Exponent (must be non-negative integer).
            modulus: Modulus for modular arithmetic.
            track_steps: If True, track algorithm steps.

        Returns:
            Result of (base^exponent) mod modulus.

        Raises:
            ValueError: If exponent is negative or modulus <= 0.
        """
        if exponent < 0:
            raise ValueError("Exponent must be non-negative")
        if modulus <= 0:
            raise ValueError("Modulus must be positive")

        logger.info(
            f"Calculating {base}^{exponent} mod {modulus} using modular exponentiation"
        )

        if exponent == 0:
            return 1 % modulus

        result = 1
        current_base = base % modulus
        current_exp = exponent
        step = 0

        while current_exp > 0:
            if track_steps:
                self.operation_steps.append({
                    "step": step,
                    "exponent": current_exp,
                    "current_base": current_base,
                    "result": result,
                    "bit": current_exp % 2,
                })

            if current_exp % 2 == 1:
                result = (result * current_base) % modulus
                if track_steps:
                    self.operation_steps[-1]["operation"] = "multiply"
                    self.operation_steps[-1]["result_after"] = result

            current_base = (current_base * current_base) % modulus
            current_exp //= 2
            step += 1

        logger.info(f"Modular exponentiation result: {result}")
        return result

    def calculate_with_analysis(
        self,
        base: float,
        exponent: int,
        method: str = "fast_iterative",
        track_steps: bool = False,
    ) -> Dict[str, Any]:
        """Calculate power with time complexity analysis.

        Args:
            base: Base number.
            exponent: Exponent (must be non-negative integer).
            method: Method to use ('naive', 'fast_recursive', 'fast_iterative').
            track_steps: If True, track algorithm steps.

        Returns:
            Dictionary containing result and analysis.
        """
        logger.info(f"Calculating {base}^{exponent} with analysis (method: {method})")

        if track_steps:
            self.operation_steps = []

        start_time = time.perf_counter()

        if method == "naive":
            result = self.power_naive(base, exponent)
            expected_operations = exponent
        elif method == "fast_recursive":
            result = self.power_fast_recursive(base, exponent, track_steps)
            expected_operations = self._calculate_log_operations(exponent)
        elif method == "fast_iterative":
            result = self.power_fast_iterative(base, exponent, track_steps)
            expected_operations = self._calculate_log_operations(exponent)
        else:
            raise ValueError(f"Unknown method: {method}")

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        analysis = {
            "base": base,
            "exponent": exponent,
            "result": result,
            "method": method,
            "execution_time": execution_time,
            "expected_operations": expected_operations,
            "actual_operations": len(self.operation_steps) if track_steps else None,
            "time_complexity": "O(n)" if method == "naive" else "O(log n)",
            "space_complexity": (
                "O(1)" if method == "fast_iterative" else "O(log n)"
            ),
            "steps": self.operation_steps.copy() if track_steps else None,
        }

        logger.info(f"Analysis complete: {analysis}")
        return analysis

    def _calculate_log_operations(self, exponent: int) -> int:
        """Calculate expected number of operations for fast exponentiation.

        Args:
            exponent: Exponent value.

        Returns:
            Expected number of operations (approximately log2(exponent)).
        """
        if exponent == 0:
            return 1
        import math
        return int(math.ceil(math.log2(exponent + 1)))

    def compare_methods(
        self, base: float, exponent: int, track_steps: bool = False
    ) -> Dict[str, Any]:
        """Compare naive and fast exponentiation methods.

        Args:
            base: Base number.
            exponent: Exponent (must be non-negative integer).
            track_steps: If True, track algorithm steps.

        Returns:
            Dictionary with comparison results.
        """
        logger.info(f"Comparing methods for {base}^{exponent}")

        naive_analysis = self.calculate_with_analysis(
            base, exponent, "naive", track_steps=False
        )
        fast_analysis = self.calculate_with_analysis(
            base, exponent, "fast_iterative", track_steps=track_steps
        )

        speedup = (
            naive_analysis["execution_time"] / fast_analysis["execution_time"]
            if fast_analysis["execution_time"] > 0
            else float("inf")
        )

        comparison = {
            "base": base,
            "exponent": exponent,
            "naive": {
                "result": naive_analysis["result"],
                "time": naive_analysis["execution_time"],
                "operations": naive_analysis["expected_operations"],
                "complexity": naive_analysis["time_complexity"],
            },
            "fast": {
                "result": fast_analysis["result"],
                "time": fast_analysis["execution_time"],
                "operations": fast_analysis["expected_operations"],
                "complexity": fast_analysis["time_complexity"],
            },
            "speedup": speedup,
            "results_match": abs(naive_analysis["result"] - fast_analysis["result"]) < 1e-10,
        }

        logger.info(f"Comparison complete: speedup = {speedup:.2f}x")
        return comparison

    def generate_report(
        self, analysis: Dict[str, Any], output_path: Optional[str] = None
    ) -> str:
        """Generate detailed analysis report.

        Args:
            analysis: Analysis dictionary from calculate_with_analysis.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "FAST EXPONENTIATION ANALYSIS REPORT",
            "=" * 80,
            "",
            f"Calculation: {analysis['base']}^{analysis['exponent']}",
            f"Result: {analysis['result']}",
            f"Method: {analysis['method']}",
            "",
            "TIME COMPLEXITY ANALYSIS",
            "-" * 80,
            f"Time Complexity: {analysis['time_complexity']}",
            f"Space Complexity: {analysis['space_complexity']}",
            f"Expected Operations: {analysis['expected_operations']}",
            f"Execution Time: {analysis['execution_time']:.10f} seconds",
            "",
            "ALGORITHM DETAILS",
            "-" * 80,
        ]

        if analysis["method"] == "naive":
            report_lines.extend([
                "Naive Method:",
                "  - Multiply base by itself exponent times",
                "  - Time: O(n) where n = exponent",
                "  - Space: O(1)",
                "  - Simple but inefficient for large exponents",
            ])
        else:
            report_lines.extend([
                "Fast Exponentiation (Exponentiation by Squaring):",
                "  - Uses divide and conquer approach",
                "  - Time: O(log n) where n = exponent",
                "  - Space: O(1) for iterative, O(log n) for recursive",
                "  - Efficient for large exponents",
                "",
                "Algorithm:",
                "  - If exponent is even: base^exp = (base^(exp/2))^2",
                "  - If exponent is odd: base^exp = base * (base^((exp-1)/2))^2",
                "  - Process continues until exponent is 0 or 1",
            ])

        if analysis.get("steps"):
            report_lines.extend([
                "",
                "ALGORITHM STEPS",
                "-" * 80,
            ])
            for step in analysis["steps"]:
                report_lines.append(f"Step: {step}")

        report_lines.extend([
            "",
            "COMPLEXITY COMPARISON",
            "-" * 80,
            "Naive Method:",
            "  - Time: O(n) - linear",
            "  - Operations: n multiplications",
            "  - Example: 2^10 requires 10 operations",
            "",
            "Fast Exponentiation:",
            "  - Time: O(log n) - logarithmic",
            "  - Operations: approximately log2(n) multiplications",
            "  - Example: 2^10 requires 4 operations",
            "",
            "SPEEDUP ANALYSIS",
            "-" * 80,
            "For exponent n:",
            f"  - Naive: {analysis['exponent']} operations",
            f"  - Fast: {analysis['expected_operations']} operations",
            f"  - Speedup: ~{analysis['exponent'] // max(analysis['expected_operations'], 1)}x",
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
        description="Fast exponentiation calculator with time complexity analysis"
    )
    parser.add_argument(
        "base",
        type=float,
        nargs="?",
        default=None,
        help="Base number",
    )
    parser.add_argument(
        "exponent",
        type=int,
        nargs="?",
        default=None,
        help="Exponent (non-negative integer)",
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
        choices=["naive", "fast_recursive", "fast_iterative"],
        default="fast_iterative",
        help="Method to use (default: fast_iterative)",
    )
    parser.add_argument(
        "--modular",
        type=int,
        metavar="MODULUS",
        help="Calculate modular exponentiation (base^exponent mod modulus)",
    )
    parser.add_argument(
        "-s",
        "--steps",
        action="store_true",
        help="Track and show algorithm steps",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        dest="compare_methods",
        help="Compare naive and fast methods",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example calculations",
    )

    args = parser.parse_args()

    try:
        calculator = FastExponentiationCalculator(config_path=args.config)

        if args.demo or (args.base is None or args.exponent is None):
            # Run demonstration
            print("\n=== Fast Exponentiation Demonstration ===\n")

            examples = [
                (2, 10),
                (3, 5),
                (5, 13),
                (2, 20),
                (10, 5),
            ]

            for base, exp in examples:
                print(f"Calculating {base}^{exp}:")
                if args.compare_methods:
                    comparison = calculator.compare_methods(base, exp, track_steps=args.steps)
                    print(f"  Naive: {comparison['naive']['result']} "
                          f"({comparison['naive']['time']:.10f}s, "
                          f"{comparison['naive']['operations']} ops)")
                    print(f"  Fast:  {comparison['fast']['result']} "
                          f"({comparison['fast']['time']:.10f}s, "
                          f"{comparison['fast']['operations']} ops)")
                    print(f"  Speedup: {comparison['speedup']:.2f}x")
                else:
                    analysis = calculator.calculate_with_analysis(
                        base, exp, method=args.method, track_steps=args.steps
                    )
                    print(f"  Result: {analysis['result']}")
                    print(f"  Method: {analysis['method']}")
                    print(f"  Time: {analysis['execution_time']:.10f}s")
                    print(f"  Complexity: {analysis['time_complexity']}")
                    print(f"  Operations: {analysis['expected_operations']}")

                    if args.steps and analysis.get("steps"):
                        print("  Steps:")
                        for step in analysis["steps"][:5]:  # Show first 5 steps
                            print(f"    {step}")
                print()

        elif args.modular:
            # Modular exponentiation
            if args.base is None or args.exponent is None:
                print("Error: Base and exponent required for modular exponentiation")
                return

            result = calculator.power_modular(
                int(args.base), args.exponent, args.modular, track_steps=args.steps
            )
            print(f"\n{int(args.base)}^{args.exponent} mod {args.modular} = {result}")

            if args.steps and calculator.operation_steps:
                print("\nSteps:")
                for step in calculator.operation_steps:
                    print(f"  {step}")

        else:
            # Standard calculation
            analysis = calculator.calculate_with_analysis(
                args.base, args.exponent, method=args.method, track_steps=args.steps
            )

            print(f"\n{args.base}^{args.exponent} = {analysis['result']}")
            print(f"Method: {analysis['method']}")
            print(f"Time Complexity: {analysis['time_complexity']}")
            print(f"Execution Time: {analysis['execution_time']:.10f} seconds")
            print(f"Expected Operations: {analysis['expected_operations']}")

            if args.steps and analysis.get("steps"):
                print("\nAlgorithm Steps:")
                for step in analysis["steps"]:
                    print(f"  {step}")

            if args.report:
                report = calculator.generate_report(analysis, output_path=args.report)
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
