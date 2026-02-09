"""Knapsack Problem Solver - 0-1 and Fractional variants.

This module provides functionality to solve the knapsack problem using
dynamic programming for 0-1 knapsack and greedy algorithm for fractional
knapsack. Both variants find the optimal way to pack items with given
weights and values into a knapsack with limited capacity.
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


class KnapsackSolver:
    """Solves knapsack problem using dynamic programming and greedy algorithms."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize KnapsackSolver with configuration.

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

    def _validate_inputs(
        self, weights: List[float], values: List[float], capacity: float
    ) -> None:
        """Validate input parameters for knapsack problem.

        Args:
            weights: List of item weights.
            values: List of item values.
            capacity: Maximum knapsack capacity.

        Raises:
            ValueError: If inputs are invalid.
        """
        if not weights or not values:
            raise ValueError("Weights and values lists cannot be empty")
        if len(weights) != len(values):
            raise ValueError(
                f"Weights length ({len(weights)}) must match "
                f"values length ({len(values)})"
            )
        if capacity <= 0:
            raise ValueError(f"Capacity must be positive, got {capacity}")
        if any(w <= 0 for w in weights):
            raise ValueError("All weights must be positive")
        if any(v < 0 for v in values):
            raise ValueError("All values must be non-negative")

    def solve_01_knapsack(
        self, weights: List[float], values: List[float], capacity: float
    ) -> Tuple[float, List[int]]:
        """Solve 0-1 knapsack problem using dynamic programming.

        Each item can be taken at most once (0 or 1). Uses bottom-up
        dynamic programming with O(n*W) time complexity where n is number
        of items and W is capacity.

        Args:
            weights: List of item weights.
            values: List of item values.
            capacity: Maximum knapsack capacity.

        Returns:
            Tuple containing:
                - Maximum value achievable
                - List of item indices selected (0-indexed)

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(weights, values, capacity)

        n = len(weights)
        # Convert capacity to integer for DP table indexing
        int_capacity = int(capacity)

        logger.info(
            f"Solving 0-1 knapsack: {n} items, capacity={capacity}"
        )

        # DP table: dp[i][w] = max value using first i items with weight w
        # Using 1D array for space optimization
        dp = [0.0] * (int_capacity + 1)
        # Track which items were selected
        item_selection = [[False] * (int_capacity + 1) for _ in range(n)]

        # Build DP table
        for i in range(n):
            # Process backwards to avoid overwriting values we need
            for w in range(int_capacity, int(weights[i]) - 1, -1):
                # Option 1: Don't take item i
                value_without = dp[w]
                # Option 2: Take item i
                value_with = (
                    dp[int(w - weights[i])] + values[i]
                    if w >= weights[i]
                    else 0
                )

                if value_with > value_without:
                    dp[w] = value_with
                    item_selection[i][w] = True
                else:
                    dp[w] = value_without

        # Reconstruct solution
        selected_items = []
        remaining_capacity = int_capacity

        for i in range(n - 1, -1, -1):
            if item_selection[i][remaining_capacity]:
                selected_items.append(i)
                remaining_capacity -= int(weights[i])

        selected_items.reverse()
        max_value = dp[int_capacity]

        logger.info(
            f"0-1 knapsack solution: value={max_value:.2f}, "
            f"items={selected_items}"
        )

        return max_value, selected_items

    def solve_fractional_knapsack(
        self, weights: List[float], values: List[float], capacity: float
    ) -> Tuple[float, List[Tuple[int, float]]]:
        """Solve fractional knapsack problem using greedy algorithm.

        Items can be taken in fractions. Uses greedy approach by selecting
        items with highest value-to-weight ratio first. This is optimal
        for fractional knapsack with O(n log n) time complexity.

        Args:
            weights: List of item weights.
            values: List of item values.
            capacity: Maximum knapsack capacity.

        Returns:
            Tuple containing:
                - Maximum value achievable
                - List of tuples (item_index, fraction_taken) where
                  fraction_taken is between 0 and 1

        Raises:
            ValueError: If inputs are invalid.
        """
        self._validate_inputs(weights, values, capacity)

        n = len(weights)

        logger.info(
            f"Solving fractional knapsack: {n} items, capacity={capacity}"
        )

        # Calculate value-to-weight ratios and sort by ratio (descending)
        items_with_ratios = [
            (i, values[i] / weights[i], weights[i], values[i])
            for i in range(n)
        ]
        items_with_ratios.sort(key=lambda x: x[1], reverse=True)

        total_value = 0.0
        remaining_capacity = capacity
        selected_items = []

        # Greedily select items with highest value-to-weight ratio
        for item_idx, ratio, weight, value in items_with_ratios:
            if remaining_capacity <= 0:
                break

            if weight <= remaining_capacity:
                # Take entire item
                total_value += value
                remaining_capacity -= weight
                selected_items.append((item_idx, 1.0))
                logger.debug(
                    f"  Taking full item {item_idx}: weight={weight}, "
                    f"value={value}, ratio={ratio:.4f}"
                )
            else:
                # Take fraction of item
                fraction = remaining_capacity / weight
                total_value += value * fraction
                selected_items.append((item_idx, fraction))
                logger.debug(
                    f"  Taking {fraction:.4f} of item {item_idx}: "
                    f"weight={weight}, value={value}, ratio={ratio:.4f}"
                )
                remaining_capacity = 0

        logger.info(
            f"Fractional knapsack solution: value={total_value:.2f}, "
            f"items={selected_items}"
        )

        return total_value, selected_items

    def compare_approaches(
        self,
        weights: List[float],
        values: List[float],
        capacity: float,
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare 0-1 and fractional knapsack solutions.

        Args:
            weights: List of item weights.
            values: List of item values.
            capacity: Maximum knapsack capacity.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing comparison data for both approaches.
        """
        logger.info(
            f"Comparing approaches: {len(weights)} items, "
            f"capacity={capacity}"
        )

        results = {
            "num_items": len(weights),
            "capacity": capacity,
            "iterations": iterations,
            "zero_one": {},
            "fractional": {},
        }

        # 0-1 Knapsack
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                value_01, items_01 = self.solve_01_knapsack(
                    weights, values, capacity
                )
            time_01 = time.perf_counter() - start_time

            results["zero_one"] = {
                "value": value_01,
                "items": items_01,
                "time_seconds": time_01 / iterations,
                "time_milliseconds": (time_01 / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"0-1 knapsack failed: {e}")
            results["zero_one"] = {"success": False, "error": str(e)}

        # Fractional Knapsack
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                value_frac, items_frac = self.solve_fractional_knapsack(
                    weights, values, capacity
                )
            time_frac = time.perf_counter() - start_time

            results["fractional"] = {
                "value": value_frac,
                "items": items_frac,
                "time_seconds": time_frac / iterations,
                "time_milliseconds": (time_frac / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Fractional knapsack failed: {e}")
            results["fractional"] = {"success": False, "error": str(e)}

        # Compare values
        if (
            results["zero_one"].get("success", False)
            and results["fractional"].get("success", False)
        ):
            value_diff = (
                results["fractional"]["value"] - results["zero_one"]["value"]
            )
            results["value_difference"] = value_diff
            results["fractional_better"] = value_diff > 0
            logger.info(
                f"Value difference: fractional is {value_diff:.2f} "
                f"higher than 0-1"
            )

        return results

    def generate_report(
        self,
        comparison_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate comparison report for knapsack solutions.

        Args:
            comparison_data: Comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "KNAPSACK PROBLEM SOLUTION COMPARISON REPORT",
            "=" * 80,
            "",
            f"Number of items: {comparison_data['num_items']}",
            f"Capacity: {comparison_data['capacity']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # 0-1 Knapsack results
        report_lines.append("\n0-1 KNAPSACK (Dynamic Programming):")
        data_01 = comparison_data["zero_one"]
        if data_01.get("success", False):
            report_lines.append(f"  Maximum value: {data_01['value']:.2f}")
            report_lines.append(f"  Selected items: {data_01['items']}")
            report_lines.append(
                f"  Time: {data_01['time_milliseconds']:.4f} ms "
                f"({data_01['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {data_01.get('error', 'Unknown')}")

        # Fractional Knapsack results
        report_lines.append("\nFRACTIONAL KNAPSACK (Greedy Algorithm):")
        data_frac = comparison_data["fractional"]
        if data_frac.get("success", False):
            report_lines.append(f"  Maximum value: {data_frac['value']:.2f}")
            items_str = ", ".join(
                [
                    f"item {idx} ({frac:.2%})"
                    for idx, frac in data_frac["items"]
                ]
            )
            report_lines.append(f"  Selected items: {items_str}")
            report_lines.append(
                f"  Time: {data_frac['time_milliseconds']:.4f} ms "
                f"({data_frac['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {data_frac.get('error', 'Unknown')}"
            )

        # Comparison
        if "value_difference" in comparison_data:
            report_lines.extend([
                "",
                "COMPARISON",
                "-" * 80,
                f"Value difference: {comparison_data['value_difference']:.2f}",
                f"Fractional better: {comparison_data['fractional_better']}",
            ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "0-1 Knapsack:",
            "  Time Complexity: O(n * W) where n=items, W=capacity",
            "  Space Complexity: O(W) with space optimization",
            "  Approach: Dynamic Programming (bottom-up)",
            "",
            "Fractional Knapsack:",
            "  Time Complexity: O(n log n) for sorting",
            "  Space Complexity: O(n) for sorting",
            "  Approach: Greedy Algorithm (optimal for fractional)",
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
        description="Solve knapsack problem using dynamic programming "
        "and greedy algorithms"
    )
    parser.add_argument(
        "capacity",
        type=float,
        help="Maximum knapsack capacity",
    )
    parser.add_argument(
        "-w",
        "--weights",
        nargs="+",
        type=float,
        required=True,
        help="Item weights (space-separated)",
    )
    parser.add_argument(
        "-v",
        "--values",
        nargs="+",
        type=float,
        required=True,
        help="Item values (space-separated)",
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
        choices=["01", "fractional", "compare"],
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
        help="Output path for comparison report",
    )

    args = parser.parse_args()

    try:
        solver = KnapsackSolver(config_path=args.config)

        weights = args.weights
        values = args.values
        capacity = args.capacity

        logger.info(
            f"Input: capacity={capacity}, "
            f"weights={weights}, values={values}"
        )

        if args.method == "compare":
            comparison = solver.compare_approaches(
                weights, values, capacity, args.iterations
            )

            print(f"\nKnapsack Problem Solution Comparison:")
            print(f"Capacity: {capacity}")
            print(f"Items: {len(weights)}")
            print("-" * 60)

            # 0-1 Knapsack
            data_01 = comparison["zero_one"]
            if data_01.get("success", False):
                print(
                    f"0-1 Knapsack:     "
                    f"Value={data_01['value']:8.2f}  "
                    f"Items={data_01['items']}  "
                    f"({data_01['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"0-1 Knapsack:     Failed - "
                    f"{data_01.get('error', 'Unknown')}"
                )

            # Fractional Knapsack
            data_frac = comparison["fractional"]
            if data_frac.get("success", False):
                items_str = ", ".join(
                    [
                        f"{idx}({frac:.1%})"
                        for idx, frac in data_frac["items"]
                    ]
                )
                print(
                    f"Fractional:        "
                    f"Value={data_frac['value']:8.2f}  "
                    f"Items={items_str}  "
                    f"({data_frac['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"Fractional:        Failed - "
                    f"{data_frac.get('error', 'Unknown')}"
                )

            if "value_difference" in comparison:
                print(
                    f"\nDifference: Fractional is "
                    f"{comparison['value_difference']:.2f} higher"
                )

            if args.report:
                report = solver.generate_report(
                    comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.method == "01":
            value, items = solver.solve_01_knapsack(
                weights, values, capacity
            )
            print(
                f"0-1 Knapsack Solution: Value={value:.2f}, "
                f"Items={items}"
            )

        elif args.method == "fractional":
            value, items = solver.solve_fractional_knapsack(
                weights, values, capacity
            )
            items_str = ", ".join(
                [f"item {idx} ({frac:.1%})" for idx, frac in items]
            )
            print(
                f"Fractional Knapsack Solution: Value={value:.2f}, "
                f"Items={items_str}"
            )

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
