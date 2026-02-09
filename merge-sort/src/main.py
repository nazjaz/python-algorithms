"""Merge Sort Algorithm - Divide and Conquer Implementation with Visualization.

This module provides a merge sort implementation with detailed visualization
of the divide and conquer process. It shows how the algorithm recursively
divides the array and merges sorted subarrays.
"""

import argparse
import logging
import logging.handlers
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class MergeSortVisualizer:
    """Merge sort implementation with divide and conquer visualization."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize visualizer with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.visualization_steps: List[Dict[str, Any]] = []
        self.step_counter = 0

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

    def _add_visualization_step(
        self,
        action: str,
        array: List[Any],
        left: Optional[int] = None,
        right: Optional[int] = None,
        mid: Optional[int] = None,
        left_array: Optional[List[Any]] = None,
        right_array: Optional[List[Any]] = None,
        merged_array: Optional[List[Any]] = None,
        depth: int = 0,
    ) -> None:
        """Add a step to visualization history.

        Args:
            action: Action description (divide, merge, etc.).
            array: Current array state.
            left: Left index (for divide operations).
            right: Right index (for divide operations).
            mid: Middle index (for divide operations).
            left_array: Left subarray (for merge operations).
            right_array: Right subarray (for merge operations).
            merged_array: Merged result (for merge operations).
            depth: Recursion depth.
        """
        self.step_counter += 1
        step = {
            "step": self.step_counter,
            "action": action,
            "array": array.copy(),
            "depth": depth,
        }

        if left is not None:
            step["left"] = left
        if right is not None:
            step["right"] = right
        if mid is not None:
            step["mid"] = mid
        if left_array is not None:
            step["left_array"] = left_array.copy()
        if right_array is not None:
            step["right_array"] = right_array.copy()
        if merged_array is not None:
            step["merged_array"] = merged_array.copy()

        self.visualization_steps.append(step)
        logger.debug(f"Visualization step {self.step_counter}: {action}")

    def _merge(
        self,
        array: List[Any],
        left: int,
        mid: int,
        right: int,
        depth: int = 0,
    ) -> None:
        """Merge two sorted subarrays.

        Merges array[left:mid+1] and array[mid+1:right+1] into sorted order.

        Args:
            array: Array to merge.
            left: Left index of subarray.
            mid: Middle index (end of left subarray).
            right: Right index (end of right subarray).
            depth: Recursion depth for visualization.
        """
        # Create temporary arrays for left and right subarrays
        left_array = array[left : mid + 1]
        right_array = array[mid + 1 : right + 1]

        logger.debug(
            f"Merging: left={left}, mid={mid}, right={right}, "
            f"left_array={left_array}, right_array={right_array}"
        )

        self._add_visualization_step(
            action="merge_start",
            array=array.copy(),
            left=left,
            right=right,
            mid=mid,
            left_array=left_array,
            right_array=right_array,
            depth=depth,
        )

        # Merge the temporary arrays back into array[left:right+1]
        i = 0  # Index for left_array
        j = 0  # Index for right_array
        k = left  # Index for merged array

        while i < len(left_array) and j < len(right_array):
            if left_array[i] <= right_array[j]:
                array[k] = left_array[i]
                i += 1
            else:
                array[k] = right_array[j]
                j += 1
            k += 1

        # Copy remaining elements from left_array
        while i < len(left_array):
            array[k] = left_array[i]
            i += 1
            k += 1

        # Copy remaining elements from right_array
        while j < len(right_array):
            array[k] = right_array[j]
            j += 1
            k += 1

        self._add_visualization_step(
            action="merge_complete",
            array=array.copy(),
            left=left,
            right=right,
            mid=mid,
            merged_array=array[left : right + 1],
            depth=depth,
        )

        logger.debug(f"Merged result: {array[left:right+1]}")

    def _merge_sort_recursive(
        self,
        array: List[Any],
        left: int,
        right: int,
        depth: int = 0,
    ) -> None:
        """Recursively sort array using merge sort (divide and conquer).

        Args:
            array: Array to sort.
            left: Left index of subarray to sort.
            right: Right index of subarray to sort.
            depth: Recursion depth for visualization.
        """
        if left < right:
            # Find middle point to divide array
            mid = left + (right - left) // 2

            logger.debug(
                f"Dividing: left={left}, mid={mid}, right={right}, "
                f"depth={depth}"
            )

            self._add_visualization_step(
                action="divide",
                array=array.copy(),
                left=left,
                right=right,
                mid=mid,
                depth=depth,
            )

            # Sort first and second halves
            self._merge_sort_recursive(array, left, mid, depth + 1)
            self._merge_sort_recursive(array, mid + 1, right, depth + 1)

            # Merge the sorted halves
            self._merge(array, left, mid, right, depth)

    def sort(self, array: List[Any], visualize: bool = True) -> List[Any]:
        """Sort array using merge sort algorithm.

        Args:
            array: Array to sort.
            visualize: If True, record visualization steps.

        Returns:
            Sorted array.

        Example:
            >>> sorter = MergeSortVisualizer()
            >>> result = sorter.sort([64, 34, 25, 12, 22, 11, 90])
            >>> result
            [11, 12, 22, 25, 34, 64, 90]
        """
        logger.info(f"Sorting array: {array}")

        if visualize:
            self.visualization_steps = []
            self.step_counter = 0

        # Create a copy to avoid modifying original
        sorted_array = array.copy()

        if len(sorted_array) <= 1:
            logger.info("Array is already sorted (length <= 1)")
            return sorted_array

        self._add_visualization_step(
            action="start",
            array=sorted_array.copy(),
            depth=0,
        )

        self._merge_sort_recursive(sorted_array, 0, len(sorted_array) - 1, 0)

        self._add_visualization_step(
            action="complete",
            array=sorted_array.copy(),
            depth=0,
        )

        logger.info(f"Sorted array: {sorted_array}")
        return sorted_array

    def get_visualization_steps(self) -> List[Dict[str, Any]]:
        """Get list of visualization steps.

        Returns:
            List of visualization step dictionaries.
        """
        return self.visualization_steps.copy()

    def print_visualization(self, detailed: bool = False) -> None:
        """Print visualization of merge sort process.

        Args:
            detailed: If True, print detailed information for each step.
        """
        if not self.visualization_steps:
            print("No visualization data available.")
            return

        print("\n" + "=" * 80)
        print("MERGE SORT VISUALIZATION - DIVIDE AND CONQUER PROCESS")
        print("=" * 80 + "\n")

        for step in self.visualization_steps:
            action = step["action"]
            depth = step.get("depth", 0)
            indent = "  " * depth

            if action == "start":
                print(f"{indent}Step {step['step']}: START")
                print(f"{indent}  Original array: {step['array']}\n")

            elif action == "divide":
                left = step.get("left", 0)
                right = step.get("right", 0)
                mid = step.get("mid", 0)
                subarray = step["array"][left : right + 1]
                print(
                    f"{indent}Step {step['step']}: DIVIDE (depth {depth})"
                )
                print(f"{indent}  Subarray[{left}:{right+1}]: {subarray}")
                print(f"{indent}  Split at index {mid}")
                print(
                    f"{indent}  Left: {step['array'][left:mid+1]}, "
                    f"Right: {step['array'][mid+1:right+1]}\n"
                )

            elif action == "merge_start":
                left = step.get("left", 0)
                right = step.get("right", 0)
                left_array = step.get("left_array", [])
                right_array = step.get("right_array", [])
                print(
                    f"{indent}Step {step['step']}: MERGE START (depth {depth})"
                )
                print(f"{indent}  Merging subarrays:")
                print(f"{indent}    Left:  {left_array}")
                print(f"{indent}    Right: {right_array}")

            elif action == "merge_complete":
                merged = step.get("merged_array", [])
                print(f"{indent}Step {step['step']}: MERGE COMPLETE")
                print(f"{indent}  Merged result: {merged}\n")

            elif action == "complete":
                print(f"{indent}Step {step['step']}: COMPLETE")
                print(f"{indent}  Final sorted array: {step['array']}\n")

            if detailed and action in ["merge_start", "merge_complete"]:
                print(f"{indent}  Full array state: {step['array']}")

        print("=" * 80)

    def generate_visualization_report(
        self, output_path: Optional[str] = None
    ) -> str:
        """Generate detailed visualization report.

        Args:
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        if not self.visualization_steps:
            return "No visualization data available."

        report_lines = [
            "=" * 80,
            "MERGE SORT VISUALIZATION REPORT",
            "=" * 80,
            "",
            "ALGORITHM: Merge Sort (Divide and Conquer)",
            "",
            "PROCESS OVERVIEW",
            "-" * 80,
            "Merge sort uses a divide and conquer strategy:",
            "1. DIVIDE: Split the array into two halves",
            "2. CONQUER: Recursively sort both halves",
            "3. COMBINE: Merge the sorted halves",
            "",
            "VISUALIZATION STEPS",
            "-" * 80,
            "",
        ]

        for step in self.visualization_steps:
            action = step["action"]
            depth = step.get("depth", 0)
            indent = "  " * depth

            report_lines.append(f"Step {step['step']}: {action.upper()}")

            if action == "start":
                report_lines.append(f"{indent}Original array: {step['array']}")

            elif action == "divide":
                left = step.get("left", 0)
                right = step.get("right", 0)
                mid = step.get("mid", 0)
                subarray = step["array"][left : right + 1]
                report_lines.append(
                    f"{indent}Subarray[{left}:{right+1}]: {subarray}"
                )
                report_lines.append(f"{indent}Split at index {mid}")
                report_lines.append(
                    f"{indent}Left: {step['array'][left:mid+1]}, "
                    f"Right: {step['array'][mid+1:right+1]}"
                )

            elif action == "merge_start":
                left_array = step.get("left_array", [])
                right_array = step.get("right_array", [])
                report_lines.append(f"{indent}Merging:")
                report_lines.append(f"{indent}  Left:  {left_array}")
                report_lines.append(f"{indent}  Right: {right_array}")

            elif action == "merge_complete":
                merged = step.get("merged_array", [])
                report_lines.append(f"{indent}Merged: {merged}")

            elif action == "complete":
                report_lines.append(f"{indent}Final sorted: {step['array']}")

            report_lines.append("")

        report_lines.extend([
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(n log n) in all cases",
            "  - Divide: O(log n) levels of recursion",
            "  - Merge: O(n) work at each level",
            "Space Complexity: O(n) for temporary arrays",
            "",
            "DIVIDE AND CONQUER ANALYSIS",
            "-" * 80,
            "Divide Phase:",
            "  - Array is divided into halves at each level",
            "  - Total levels: log₂(n)",
            "  - Each level processes all n elements",
            "",
            "Conquer Phase:",
            "  - Base case: arrays of size 1 are already sorted",
            "  - Recursively sort left and right halves",
            "",
            "Combine Phase:",
            "  - Merge two sorted subarrays",
            "  - Compare elements and place in order",
            "  - O(n) time per merge operation",
            "",
            "PROPERTIES",
            "-" * 80,
            "- Stable: Maintains relative order of equal elements",
            "- Not in-place: Requires O(n) extra space",
            "- Guaranteed O(n log n) performance",
            "- Well-suited for linked lists and external sorting",
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
        description="Merge sort algorithm with divide and conquer visualization"
    )
    parser.add_argument(
        "numbers",
        type=int,
        nargs="*",
        help="Numbers to sort (space-separated)",
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
        help="Show visualization of sorting process",
    )
    parser.add_argument(
        "-d",
        "--detailed",
        action="store_true",
        help="Show detailed visualization information",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for visualization report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example arrays",
    )

    args = parser.parse_args()

    try:
        visualizer = MergeSortVisualizer(config_path=args.config)

        if args.demo or not args.numbers:
            # Run demonstration
            print("\n=== Merge Sort Demonstration ===\n")

            examples = [
                [64, 34, 25, 12, 22, 11, 90],
                [5, 2, 8, 1, 9],
                [3, 1, 4, 1, 5, 9, 2, 6],
                [10],
                [5, 4, 3, 2, 1],
            ]

            for example in examples:
                print(f"Original array: {example}")
                sorted_result = visualizer.sort(example, visualize=True)
                print(f"Sorted array:  {sorted_result}")

                if args.visualize or args.detailed:
                    visualizer.print_visualization(detailed=args.detailed)

                if args.report:
                    report_path = f"report_{example}.txt"
                    visualizer.generate_visualization_report(
                        output_path=report_path
                    )
                    print(f"Report saved to {report_path}")

                print()

        else:
            # Sort provided numbers
            numbers = args.numbers
            print(f"\nOriginal array: {numbers}")

            sorted_result = visualizer.sort(numbers, visualize=True)
            print(f"Sorted array:  {sorted_result}")

            if args.visualize or args.detailed:
                visualizer.print_visualization(detailed=args.detailed)

            if args.report:
                visualizer.generate_visualization_report(
                    output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
