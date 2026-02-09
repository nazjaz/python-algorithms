"""Max-Min Finder - Single pass algorithm for finding max and min values.

This module provides functionality to find maximum and minimum values in an
array using a single pass algorithm with detailed analysis.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class MaxMinFinder:
    """Finds maximum and minimum values using single pass algorithm."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize MaxMinFinder with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.comparisons = 0
        self.analysis_data: Dict[str, any] = {}

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

    def find_max_min(self, array: List[float]) -> Tuple[float, float]:
        """Find maximum and minimum values using single pass algorithm.

        Args:
            array: List of numbers to analyze.

        Returns:
            Tuple of (minimum, maximum) values.

        Raises:
            ValueError: If array is empty.
        """
        if not array:
            raise ValueError("Cannot find max/min in empty array")

        self.comparisons = 0
        self.analysis_data = {
            "array_length": len(array),
            "elements_processed": 0,
            "max_updates": 0,
            "min_updates": 0,
            "comparison_details": [],
        }

        logger.info(f"Starting max-min search on array of length {len(array)}")

        # Initialize with first element
        min_val = array[0]
        max_val = array[0]
        min_index = 0
        max_index = 0

        logger.debug(f"Initial values: min={min_val} (index {min_index}), max={max_val} (index {max_index})")

        # Process remaining elements in pairs for optimization
        i = 1
        while i < len(array):
            self.analysis_data["elements_processed"] += 1

            if i + 1 < len(array):
                # Compare two elements at once
                if array[i] < array[i + 1]:
                    self.comparisons += 1
                    logger.debug(
                        f"Comparing indices {i} and {i+1}: "
                        f"{array[i]} < {array[i+1]}"
                    )

                    # Compare smaller with min
                    if array[i] < min_val:
                        min_val = array[i]
                        min_index = i
                        self.analysis_data["min_updates"] += 1
                        logger.info(
                            f"New minimum found: {min_val} at index {i}"
                        )
                    self.comparisons += 1

                    # Compare larger with max
                    if array[i + 1] > max_val:
                        max_val = array[i + 1]
                        max_index = i + 1
                        self.analysis_data["max_updates"] += 1
                        logger.info(
                            f"New maximum found: {max_val} at index {i+1}"
                        )
                    self.comparisons += 1
                else:
                    self.comparisons += 1
                    logger.debug(
                        f"Comparing indices {i} and {i+1}: "
                        f"{array[i+1]} < {array[i]}"
                    )

                    # Compare smaller with min
                    if array[i + 1] < min_val:
                        min_val = array[i + 1]
                        min_index = i + 1
                        self.analysis_data["min_updates"] += 1
                        logger.info(
                            f"New minimum found: {min_val} at index {i+1}"
                        )
                    self.comparisons += 1

                    # Compare larger with max
                    if array[i] > max_val:
                        max_val = array[i]
                        max_index = i
                        self.analysis_data["max_updates"] += 1
                        logger.info(
                            f"New maximum found: {max_val} at index {i}"
                        )
                    self.comparisons += 1

                i += 2
            else:
                # Handle last element if array length is odd
                self.comparisons += 1
                if array[i] < min_val:
                    min_val = array[i]
                    min_index = i
                    self.analysis_data["min_updates"] += 1
                    logger.info(f"New minimum found: {min_val} at index {i}")
                self.comparisons += 1
                if array[i] > max_val:
                    max_val = array[i]
                    max_index = i
                    self.analysis_data["max_updates"] += 1
                    logger.info(f"New maximum found: {max_val} at index {i}")
                i += 1

        self.analysis_data["min_value"] = min_val
        self.analysis_data["max_value"] = max_val
        self.analysis_data["min_index"] = min_index
        self.analysis_data["max_index"] = max_index

        logger.info(
            f"Search completed: min={min_val} (index {min_index}), "
            f"max={max_val} (index {max_index}), "
            f"comparisons={self.comparisons}"
        )

        return (min_val, max_val)

    def get_analysis(self) -> Dict[str, any]:
        """Get detailed analysis of the algorithm execution.

        Returns:
            Dictionary containing analysis data.
        """
        analysis = self.analysis_data.copy()
        analysis["total_comparisons"] = self.comparisons
        analysis["comparisons_per_element"] = (
            self.comparisons / max(1, self.analysis_data["array_length"])
        )
        analysis["efficiency_ratio"] = (
            self.comparisons / max(1, 2 * (self.analysis_data["array_length"] - 1))
        )

        return analysis

    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate detailed analysis report.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        if not self.analysis_data:
            return "No analysis data available. Run find_max_min() first."

        analysis = self.get_analysis()

        report_lines = [
            "=" * 80,
            "MAX-MIN FINDER ALGORITHM ANALYSIS REPORT",
            "=" * 80,
            "",
            "RESULTS",
            "-" * 80,
            f"Minimum value: {analysis['min_value']} (index {analysis['min_index']})",
            f"Maximum value: {analysis['max_value']} (index {analysis['max_index']})",
            f"Range: {analysis['max_value'] - analysis['min_value']}",
            "",
            "PERFORMANCE METRICS",
            "-" * 80,
            f"Array length: {analysis['array_length']}",
            f"Total comparisons: {analysis['total_comparisons']:,}",
            f"Comparisons per element: {analysis['comparisons_per_element']:.2f}",
            f"Efficiency ratio: {analysis['efficiency_ratio']:.2%}",
            "",
            "ALGORITHM STATISTICS",
            "-" * 80,
            f"Minimum value updates: {analysis['min_updates']}",
            f"Maximum value updates: {analysis['max_updates']}",
            f"Elements processed: {analysis['elements_processed']}",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(n) - Single pass through array",
            "Space Complexity: O(1) - Constant extra space",
            "Optimization: Processes elements in pairs when possible",
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
    import argparse

    parser = argparse.ArgumentParser(
        description="Find maximum and minimum values using single pass algorithm"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers to analyze",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-r",
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
        finder = MaxMinFinder(config_path=args.config)
        min_val, max_val = finder.find_max_min(args.numbers)

        print(f"\nArray: {args.numbers}")
        print(f"Minimum: {min_val}")
        print(f"Maximum: {max_val}")
        print(f"Range: {max_val - min_val}")
        print(f"Comparisons: {finder.comparisons}")

        if args.analysis:
            analysis = finder.get_analysis()
            print("\nDetailed Analysis:")
            print(f"  Array length: {analysis['array_length']}")
            print(f"  Comparisons per element: {analysis['comparisons_per_element']:.2f}")
            print(f"  Efficiency ratio: {analysis['efficiency_ratio']:.2%}")
            print(f"  Min updates: {analysis['min_updates']}")
            print(f"  Max updates: {analysis['max_updates']}")

        if args.report:
            report = finder.generate_report(output_path=args.report)
            print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
