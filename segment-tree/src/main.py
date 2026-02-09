"""Segment Tree Data Structure.

This module provides functionality to implement segment tree data structure
for efficient range queries and point/range updates with lazy propagation.
Segment trees allow O(log n) range queries and updates.
"""

import logging
import logging.handlers
import math
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class SegmentTree:
    """Segment tree for range queries and updates with lazy propagation."""

    def __init__(
        self,
        arr: List[float],
        operation: str = "sum",
        config_path: str = "config.yaml",
    ) -> None:
        """Initialize SegmentTree with array and operation.

        Args:
            arr: Input array.
            operation: Operation type - 'sum', 'min', or 'max'.
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
            ValueError: If operation is invalid or array is empty.
        """
        if not arr:
            raise ValueError("Array cannot be empty")

        if operation not in ["sum", "min", "max"]:
            raise ValueError(f"Invalid operation: {operation}. Choose from: sum, min, max")

        self.arr = arr
        self.n = len(arr)
        self.operation = operation
        self.config = self._load_config(config_path)
        self._setup_logging()

        # Select operation functions
        self._init_operation_functions()

        # Build segment tree
        self._build_tree()

        logger.info(
            f"Segment tree initialized: size={self.n}, operation={operation}"
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

    def _init_operation_functions(self) -> None:
        """Initialize operation functions based on operation type."""
        if self.operation == "sum":
            self._combine = lambda a, b: a + b
            self._neutral = 0.0
            self._apply_lazy = lambda val, lazy, size: val + lazy * size
            self._combine_lazy = lambda a, b: a + b
        elif self.operation == "min":
            self._combine = lambda a, b: min(a, b)
            self._neutral = float("inf")
            self._apply_lazy = lambda val, lazy, size: val + lazy
            self._combine_lazy = lambda a, b: a + b
        elif self.operation == "max":
            self._combine = lambda a, b: max(a, b)
            self._neutral = float("-inf")
            self._apply_lazy = lambda val, lazy, size: val + lazy
            self._combine_lazy = lambda a, b: a + b

    def _build_tree(self) -> None:
        """Build segment tree from array."""
        # Calculate tree size (next power of 2)
        tree_size = 2 * (2 ** math.ceil(math.log2(self.n))) - 1
        self.tree = [self._neutral] * tree_size
        self.lazy = [0.0] * tree_size

        logger.debug(f"Building segment tree: array_size={self.n}, tree_size={tree_size}")

        def _build(node: int, start: int, end: int) -> None:
            """Recursive helper to build tree."""
            if start == end:
                self.tree[node] = self.arr[start]
                logger.debug(f"  Leaf node {node}: value={self.arr[start]}")
            else:
                mid = (start + end) // 2
                left_child = 2 * node + 1
                right_child = 2 * node + 2

                _build(left_child, start, mid)
                _build(right_child, mid + 1, end)

                self.tree[node] = self._combine(
                    self.tree[left_child], self.tree[right_child]
                )
                logger.debug(
                    f"  Internal node {node}: value={self.tree[node]} "
                    f"(from {start} to {end})"
                )

        _build(0, 0, self.n - 1)

    def _push_lazy(self, node: int, start: int, end: int) -> None:
        """Push lazy value to children.

        Args:
            node: Current node index.
            start: Start of segment.
            end: End of segment.
        """
        if self.lazy[node] != 0.0:
            # Apply lazy value to current node
            segment_size = end - start + 1
            self.tree[node] = self._apply_lazy(
                self.tree[node], self.lazy[node], segment_size
            )

            # Push to children if not leaf
            if start != end:
                left_child = 2 * node + 1
                right_child = 2 * node + 2
                self.lazy[left_child] = self._combine_lazy(
                    self.lazy[left_child], self.lazy[node]
                )
                self.lazy[right_child] = self._combine_lazy(
                    self.lazy[right_child], self.lazy[node]
                )

            # Reset lazy value
            self.lazy[node] = 0.0

    def query(self, left: int, right: int) -> float:
        """Query range [left, right].

        Args:
            left: Left index (0-indexed, inclusive).
            right: Right index (0-indexed, inclusive).

        Returns:
            Result of operation over range.

        Raises:
            ValueError: If indices are invalid.
        """
        if left < 0 or right >= self.n or left > right:
            raise ValueError(
                f"Invalid range: [{left}, {right}]. "
                f"Must be within [0, {self.n - 1}]"
            )

        logger.info(f"Query range [{left}, {right}]")

        def _query(node: int, start: int, end: int, qleft: int, qright: int) -> float:
            """Recursive helper for query."""
            # Push lazy value
            self._push_lazy(node, start, end)

            # No overlap
            if qright < start or qleft > end:
                return self._neutral

            # Complete overlap
            if qleft <= start and end <= qright:
                return self.tree[node]

            # Partial overlap
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            left_result = _query(left_child, start, mid, qleft, qright)
            right_result = _query(right_child, mid + 1, end, qleft, qright)

            result = self._combine(left_result, right_result)
            logger.debug(
                f"  Query [{qleft}, {qright}] in [{start}, {end}]: {result}"
            )
            return result

        result = _query(0, 0, self.n - 1, left, right)
        logger.info(f"Query result: {result}")
        return result

    def update_point(self, index: int, value: float) -> None:
        """Update single point at index.

        Args:
            index: Index to update (0-indexed).
            value: New value.

        Raises:
            ValueError: If index is invalid.
        """
        if index < 0 or index >= self.n:
            raise ValueError(f"Invalid index: {index}. Must be in [0, {self.n - 1}]")

        logger.info(f"Point update: index={index}, value={value}")

        def _update(node: int, start: int, end: int, idx: int, val: float) -> None:
            """Recursive helper for point update."""
            # Push lazy value
            self._push_lazy(node, start, end)

            # Leaf node
            if start == end:
                self.tree[node] = val
                logger.debug(f"  Updated leaf node {node}: {val}")
            else:
                mid = (start + end) // 2
                left_child = 2 * node + 1
                right_child = 2 * node + 2

                if idx <= mid:
                    _update(left_child, start, mid, idx, val)
                else:
                    _update(right_child, mid + 1, end, idx, val)

                # Push lazy before combining
                self._push_lazy(left_child, start, mid)
                self._push_lazy(right_child, mid + 1, end)

                self.tree[node] = self._combine(
                    self.tree[left_child], self.tree[right_child]
                )
                logger.debug(f"  Updated node {node}: {self.tree[node]}")

        _update(0, 0, self.n - 1, index, value)
        self.arr[index] = value

    def update_range(
        self, left: int, right: int, value: float
    ) -> None:
        """Update range [left, right] with lazy propagation.

        Args:
            left: Left index (0-indexed, inclusive).
            right: Right index (0-indexed, inclusive).
            value: Value to add/update.

        Raises:
            ValueError: If indices are invalid.
        """
        if left < 0 or right >= self.n or left > right:
            raise ValueError(
                f"Invalid range: [{left}, {right}]. "
                f"Must be within [0, {self.n - 1}]"
            )

        logger.info(f"Range update: [{left}, {right}], value={value}")

        def _update_range(
            node: int, start: int, end: int, uleft: int, uright: int, val: float
        ) -> None:
            """Recursive helper for range update."""
            # Push lazy value
            self._push_lazy(node, start, end)

            # No overlap
            if uright < start or uleft > end:
                return

            # Complete overlap
            if uleft <= start and end <= uright:
                # Apply lazy value
                segment_size = end - start + 1
                self.tree[node] = self._apply_lazy(
                    self.tree[node], val, segment_size
                )

                # Mark children as lazy
                if start != end:
                    left_child = 2 * node + 1
                    right_child = 2 * node + 2
                    self.lazy[left_child] = self._combine_lazy(
                        self.lazy[left_child], val
                    )
                    self.lazy[right_child] = self._combine_lazy(
                        self.lazy[right_child], val
                    )

                logger.debug(
                    f"  Updated range [{uleft}, {uright}] in [{start}, {end}]"
                )
                return

            # Partial overlap
            mid = (start + end) // 2
            left_child = 2 * node + 1
            right_child = 2 * node + 2

            _update_range(left_child, start, mid, uleft, uright, val)
            _update_range(right_child, mid + 1, end, uleft, uright, val)

            # Push lazy before combining
            self._push_lazy(left_child, start, mid)
            self._push_lazy(right_child, mid + 1, end)

            self.tree[node] = self._combine(
                self.tree[left_child], self.tree[right_child]
            )

        _update_range(0, 0, self.n - 1, left, right, value)

        # Update array (for sum operation, add value; for min/max, set value)
        if self.operation == "sum":
            for i in range(left, right + 1):
                self.arr[i] += value
        else:
            for i in range(left, right + 1):
                self.arr[i] += value

    def get_array(self) -> List[float]:
        """Get current array values.

        Returns:
            Copy of current array.
        """
        return self.arr.copy()

    def compare_operations(
        self, queries: List[tuple], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of different operations.

        Args:
            queries: List of query tuples (type, *args).
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        logger.info(
            f"Performance comparison: {len(queries)} queries, "
            f"iterations={iterations}"
        )

        results = {
            "array_size": self.n,
            "operation": self.operation,
            "num_queries": len(queries),
            "iterations": iterations,
            "query": {},
            "update_point": {},
            "update_range": {},
        }

        # Query operations
        try:
            query_ops = [q for q in queries if q[0] == "query"]
            if query_ops:
                start_time = time.perf_counter()
                for _ in range(iterations):
                    for op_type, left, right in query_ops:
                        self.query(left, right)
                query_time = time.perf_counter() - start_time

                results["query"] = {
                    "operations": len(query_ops) * iterations,
                    "time_seconds": query_time / iterations,
                    "time_milliseconds": (query_time / iterations) * 1000,
                    "time_per_query_microseconds": (
                        (query_time / iterations) / len(query_ops) * 1000000
                    ),
                    "success": True,
                }
        except Exception as e:
            logger.error(f"Query operations failed: {e}")
            results["query"] = {"success": False, "error": str(e)}

        # Point update operations
        try:
            point_ops = [q for q in queries if q[0] == "update_point"]
            if point_ops:
                start_time = time.perf_counter()
                for _ in range(iterations):
                    for op_type, index, value in point_ops:
                        self.update_point(index, value)
                point_time = time.perf_counter() - start_time

                results["update_point"] = {
                    "operations": len(point_ops) * iterations,
                    "time_seconds": point_time / iterations,
                    "time_milliseconds": (point_time / iterations) * 1000,
                    "time_per_update_microseconds": (
                        (point_time / iterations) / len(point_ops) * 1000000
                    ),
                    "success": True,
                }
        except Exception as e:
            logger.error(f"Point update operations failed: {e}")
            results["update_point"] = {"success": False, "error": str(e)}

        # Range update operations
        try:
            range_ops = [q for q in queries if q[0] == "update_range"]
            if range_ops:
                start_time = time.perf_counter()
                for _ in range(iterations):
                    for op_type, left, right, value in range_ops:
                        self.update_range(left, right, value)
                range_time = time.perf_counter() - start_time

                results["update_range"] = {
                    "operations": len(range_ops) * iterations,
                    "time_seconds": range_time / iterations,
                    "time_milliseconds": (range_time / iterations) * 1000,
                    "time_per_update_microseconds": (
                        (range_time / iterations) / len(range_ops) * 1000000
                    ),
                    "success": True,
                }
        except Exception as e:
            logger.error(f"Range update operations failed: {e}")
            results["update_range"] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for segment tree operations.

        Args:
            performance_data: Performance data from compare_operations().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "SEGMENT TREE PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Array size: {performance_data['array_size']}",
            f"Operation: {performance_data['operation']}",
            f"Number of queries: {performance_data['num_queries']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # Query
        report_lines.append("\nquery():")
        query_data = performance_data["query"]
        if query_data.get("success", False):
            report_lines.append(f"  Operations: {query_data['operations']}")
            report_lines.append(
                f"  Time: {query_data['time_milliseconds']:.4f} ms "
                f"({query_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per query: "
                f"{query_data['time_per_query_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {query_data.get('error', 'Unknown')}")

        # Point update
        report_lines.append("\nupdate_point():")
        point_data = performance_data["update_point"]
        if point_data.get("success", False):
            report_lines.append(f"  Operations: {point_data['operations']}")
            report_lines.append(
                f"  Time: {point_data['time_milliseconds']:.4f} ms "
                f"({point_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per update: "
                f"{point_data['time_per_update_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {point_data.get('error', 'Unknown')}")

        # Range update
        report_lines.append("\nupdate_range():")
        range_data = performance_data["update_range"]
        if range_data.get("success", False):
            report_lines.append(f"  Operations: {range_data['operations']}")
            report_lines.append(
                f"  Time: {range_data['time_milliseconds']:.4f} ms "
                f"({range_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per update: "
                f"{range_data['time_per_update_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {range_data.get('error', 'Unknown')}")

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Segment Tree Operations:",
            "  Build: O(n) where n=array size",
            "  Query: O(log n) for range query",
            "  Point Update: O(log n) for single element update",
            "  Range Update: O(log n) with lazy propagation",
            "  Space Complexity: O(n) for tree and lazy arrays",
            "",
            "Lazy Propagation:",
            "  - Defers updates until needed",
            "  - Reduces update complexity from O(n log n) to O(log n)",
            "  - Essential for efficient range updates",
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
        description="Segment tree data structure for range queries and "
        "point/range updates with lazy propagation"
    )
    parser.add_argument(
        "numbers",
        nargs="+",
        type=float,
        help="Numbers in the array",
    )
    parser.add_argument(
        "-o",
        "--operation",
        choices=["sum", "min", "max"],
        default="sum",
        help="Operation type (default: sum)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-q",
        "--query",
        nargs=2,
        type=int,
        metavar=("LEFT", "RIGHT"),
        help="Query range [left, right]",
    )
    parser.add_argument(
        "-u",
        "--update-point",
        nargs=2,
        type=float,
        metavar=("INDEX", "VALUE"),
        help="Update point at index with value",
    )
    parser.add_argument(
        "-r",
        "--update-range",
        nargs=3,
        type=float,
        metavar=("LEFT", "RIGHT", "VALUE"),
        help="Update range [left, right] with value",
    )
    parser.add_argument(
        "-a",
        "--array",
        action="store_true",
        help="Display current array",
    )

    args = parser.parse_args()

    try:
        st = SegmentTree(
            args.numbers, operation=args.operation, config_path=args.config
        )

        logger.info(f"Input: {len(args.numbers)} numbers, operation={args.operation}")

        if args.query:
            left, right = args.query
            result = st.query(left, right)
            print(f"Query [{left}, {right}]: {result}")

        if args.update_point:
            index, value = args.update_point
            st.update_point(int(index), value)
            print(f"Updated index {int(index)} to {value}")

        if args.update_range:
            left, right, value = args.update_range
            st.update_range(int(left), int(right), value)
            print(f"Updated range [{int(left)}, {int(right)}] with {value}")

        if args.array:
            print(f"Current array: {st.get_array()}")

        if not any([args.query, args.update_point, args.update_range, args.array]):
            print(f"Segment tree created with {len(args.numbers)} elements")
            print(f"Operation: {args.operation}")
            print(f"Array: {st.get_array()}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
