"""Union-Find (Disjoint Set) Data Structure.

This module provides functionality to implement union-find (disjoint set)
data structure with path compression and union by rank optimizations.
The union-find data structure efficiently tracks disjoint sets and
supports union and find operations.
"""

import logging
import logging.handlers
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class UnionFind:
    """Union-Find (Disjoint Set) with path compression and union by rank.

    This implementation uses two optimizations:
    1. Path Compression: Flattens the tree during find operations
    2. Union by Rank: Always attaches smaller tree under larger tree
    """

    def __init__(
        self, num_elements: int, config_path: str = "config.yaml"
    ) -> None:
        """Initialize UnionFind with specified number of elements.

        Args:
            num_elements: Number of elements (0 to num_elements-1).
            config_path: Path to configuration YAML file.

        Raises:
            ValueError: If num_elements is negative.
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        if num_elements < 0:
            raise ValueError("Number of elements must be non-negative")

        self.num_elements = num_elements
        self.parent = list(range(num_elements))
        self.rank = [0] * num_elements
        self.components = num_elements

        self.config = self._load_config(config_path)
        self._setup_logging()

        logger.info(f"UnionFind initialized with {num_elements} elements")

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

    def _validate_element(self, x: int) -> None:
        """Validate element index.

        Args:
            x: Element index to validate.

        Raises:
            ValueError: If element index is invalid.
        """
        if x < 0 or x >= self.num_elements:
            raise ValueError(
                f"Element {x} is out of range [0, {self.num_elements - 1}]"
            )

    def find(self, x: int) -> int:
        """Find root of element with path compression.

        Path compression flattens the tree by making all nodes point
        directly to the root during the find operation.

        Args:
            x: Element to find root for.

        Returns:
            Root element of the set containing x.

        Raises:
            ValueError: If element index is invalid.
        """
        self._validate_element(x)

        if self.parent[x] != x:
            # Path compression: make parent point directly to root
            self.parent[x] = self.find(self.parent[x])
            logger.debug(f"  Path compressed: {x} -> {self.parent[x]}")

        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union two sets using union by rank.

        Union by rank attaches the smaller tree under the larger tree,
        keeping the tree height small.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if union was performed, False if already in same set.

        Raises:
            ValueError: If element indices are invalid.
        """
        self._validate_element(x)
        self._validate_element(y)

        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            logger.debug(f"  Elements {x} and {y} already in same set")
            return False

        # Union by rank: attach smaller tree under larger tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            logger.debug(
                f"  Union: {root_x} attached to {root_y} "
                f"(rank {self.rank[root_x]} < {self.rank[root_y]})"
            )
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            logger.debug(
                f"  Union: {root_y} attached to {root_x} "
                f"(rank {self.rank[root_y]} < {self.rank[root_x]})"
            )
        else:
            # Ranks equal, attach one to other and increment rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            logger.debug(
                f"  Union: {root_y} attached to {root_x} "
                f"(ranks equal, new rank: {self.rank[root_x]})"
            )

        self.components -= 1
        logger.info(f"Union({x}, {y}): components = {self.components}")
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if two elements are in the same set.

        Args:
            x: First element.
            y: Second element.

        Returns:
            True if elements are in same set, False otherwise.

        Raises:
            ValueError: If element indices are invalid.
        """
        self._validate_element(x)
        self._validate_element(y)

        result = self.find(x) == self.find(y)
        logger.debug(f"  Connected({x}, {y}): {result}")
        return result

    def get_component_count(self) -> int:
        """Get number of disjoint components.

        Returns:
            Number of disjoint sets.
        """
        return self.components

    def get_component(self, x: int) -> List[int]:
        """Get all elements in the same component as x.

        Args:
            x: Element to get component for.

        Returns:
            List of all elements in the same component.

        Raises:
            ValueError: If element index is invalid.
        """
        self._validate_element(x)

        root = self.find(x)
        component = [i for i in range(self.num_elements) if self.find(i) == root]
        logger.debug(f"  Component of {x}: {component}")
        return component

    def get_all_components(self) -> Dict[int, List[int]]:
        """Get all disjoint components.

        Returns:
            Dictionary mapping root to list of elements in that component.
        """
        components: Dict[int, List[int]] = {}

        for i in range(self.num_elements):
            root = self.find(i)
            if root not in components:
                components[root] = []
            components[root].append(i)

        logger.debug(f"  All components: {len(components)} sets")
        return components

    def get_largest_component(self) -> Optional[List[int]]:
        """Get the largest component.

        Returns:
            List of elements in largest component, or None if no elements.
        """
        all_components = self.get_all_components()
        if not all_components:
            return None

        largest = max(all_components.values(), key=len)
        logger.debug(f"  Largest component: size {len(largest)}")
        return largest

    def get_component_statistics(self) -> Dict[str, any]:
        """Get statistics about components.

        Returns:
            Dictionary containing component statistics:
                - count: Total number of components
                - sizes: List of component sizes
                - largest_size: Size of largest component
                - smallest_size: Size of smallest component
                - average_size: Average component size
        """
        all_components = self.get_all_components()
        if not all_components:
            return {
                "count": 0,
                "sizes": [],
                "largest_size": 0,
                "smallest_size": 0,
                "average_size": 0.0,
            }

        sizes = [len(comp) for comp in all_components.values()]
        return {
            "count": len(all_components),
            "sizes": sizes,
            "largest_size": max(sizes),
            "smallest_size": min(sizes),
            "average_size": sum(sizes) / len(sizes) if sizes else 0.0,
        }

    def union_all(self, pairs: List[Tuple[int, int]]) -> int:
        """Union multiple pairs of elements.

        Args:
            pairs: List of (x, y) tuples to union.

        Returns:
            Number of unions performed.
        """
        unions_performed = 0
        logger.info(f"Unioning {len(pairs)} pairs")

        for x, y in pairs:
            if self.union(x, y):
                unions_performed += 1

        logger.info(f"Performed {unions_performed} unions")
        return unions_performed

    def reset(self) -> None:
        """Reset union-find to initial state (all elements separate)."""
        self.parent = list(range(self.num_elements))
        self.rank = [0] * self.num_elements
        self.components = self.num_elements
        logger.info("UnionFind reset to initial state")

    def compare_performance(
        self, pairs: List[Tuple[int, int]], iterations: int = 1
    ) -> Dict[str, any]:
        """Compare performance of union-find operations.

        Args:
            pairs: List of (x, y) tuples to union.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        logger.info(
            f"Performance comparison: {len(pairs)} pairs, "
            f"iterations={iterations}"
        )

        results = {
            "num_elements": self.num_elements,
            "num_pairs": len(pairs),
            "iterations": iterations,
            "union_all": {},
            "find_operations": {},
            "connected_checks": {},
        }

        # Union all pairs
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                self.reset()
                unions = self.union_all(pairs)
            union_time = time.perf_counter() - start_time

            results["union_all"] = {
                "unions_performed": unions,
                "components": self.components,
                "time_seconds": union_time / iterations,
                "time_milliseconds": (union_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Union all failed: {e}")
            results["union_all"] = {"success": False, "error": str(e)}

        # Find operations
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                for x, y in pairs:
                    self.find(x)
                    self.find(y)
            find_time = time.perf_counter() - start_time

            results["find_operations"] = {
                "operations": len(pairs) * 2,
                "time_seconds": find_time / iterations,
                "time_milliseconds": (find_time / iterations) * 1000,
                "time_per_operation_microseconds": (
                    (find_time / iterations) / (len(pairs) * 2) * 1000000
                ),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Find operations failed: {e}")
            results["find_operations"] = {"success": False, "error": str(e)}

        # Connected checks
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                for x, y in pairs:
                    self.connected(x, y)
            connected_time = time.perf_counter() - start_time

            results["connected_checks"] = {
                "checks": len(pairs),
                "time_seconds": connected_time / iterations,
                "time_milliseconds": (connected_time / iterations) * 1000,
                "time_per_check_microseconds": (
                    (connected_time / iterations) / len(pairs) * 1000000
                ),
                "success": True,
            }
        except Exception as e:
            logger.error(f"Connected checks failed: {e}")
            results["connected_checks"] = {
                "success": False,
                "error": str(e),
            }

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for union-find operations.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "UNION-FIND DATA STRUCTURE PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of elements: {performance_data['num_elements']}",
            f"Number of pairs: {performance_data['num_pairs']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # Union all
        report_lines.append("\nunion_all():")
        union_data = performance_data["union_all"]
        if union_data.get("success", False):
            report_lines.append(
                f"  Unions performed: {union_data['unions_performed']}"
            )
            report_lines.append(
                f"  Components: {union_data['components']}"
            )
            report_lines.append(
                f"  Time: {union_data['time_milliseconds']:.4f} ms "
                f"({union_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {union_data.get('error', 'Unknown')}")

        # Find operations
        report_lines.append("\nfind() operations:")
        find_data = performance_data["find_operations"]
        if find_data.get("success", False):
            report_lines.append(
                f"  Operations: {find_data['operations']}"
            )
            report_lines.append(
                f"  Time: {find_data['time_milliseconds']:.4f} ms "
                f"({find_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per operation: "
                f"{find_data['time_per_operation_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {find_data.get('error', 'Unknown')}")

        # Connected checks
        report_lines.append("\nconnected() checks:")
        connected_data = performance_data["connected_checks"]
        if connected_data.get("success", False):
            report_lines.append(f"  Checks: {connected_data['checks']}")
            report_lines.append(
                f"  Time: {connected_data['time_milliseconds']:.4f} ms "
                f"({connected_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Time per check: "
                f"{connected_data['time_per_check_microseconds']:.2f} μs"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {connected_data.get('error', 'Unknown')}"
            )

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Union-Find with optimizations:",
            "  Time Complexity:",
            "    - Find: O(α(n)) amortized (inverse Ackermann function)",
            "    - Union: O(α(n)) amortized",
            "    - Connected: O(α(n)) amortized",
            "  Space Complexity: O(n) for parent and rank arrays",
            "  Optimizations:",
            "    - Path Compression: Flattens tree during find",
            "    - Union by Rank: Keeps tree height small",
            "",
            "Note: α(n) is the inverse Ackermann function, which grows",
            "extremely slowly and is effectively constant for practical n.",
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
        description="Union-Find (Disjoint Set) data structure with "
        "path compression and union by rank optimizations"
    )
    parser.add_argument(
        "-n",
        "--num-elements",
        type=int,
        required=True,
        help="Number of elements",
    )
    parser.add_argument(
        "-p",
        "--pairs",
        nargs="+",
        type=str,
        help="Pairs as 'x-y' (e.g., '0-1 1-2')",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-o",
        "--operation",
        choices=["union", "find", "connected", "components", "stats", "compare"],
        default="union",
        help="Operation to perform (default: union)",
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
        uf = UnionFind(args.num_elements, config_path=args.config)

        # Parse pairs
        pairs: List[Tuple[int, int]] = []
        if args.pairs:
            for pair_str in args.pairs:
                try:
                    if "-" in pair_str:
                        x, y = map(int, pair_str.split("-"))
                        pairs.append((x, y))
                    else:
                        raise ValueError(
                            f"Invalid pair format: {pair_str}. "
                            f"Use 'x-y' format"
                        )
                except ValueError as e:
                    logger.error(f"Error parsing pair '{pair_str}': {e}")
                    raise

        logger.info(
            f"Input: {args.num_elements} elements, "
            f"{len(pairs)} pairs"
        )

        if args.operation == "union":
            if pairs:
                unions = uf.union_all(pairs)
                print(f"Unions performed: {unions}")
                print(f"Components: {uf.get_component_count()}")
            else:
                print("No pairs provided for union operation")

        elif args.operation == "find":
            if pairs:
                for x, y in pairs:
                    root_x = uf.find(x)
                    root_y = uf.find(y)
                    print(f"find({x}) = {root_x}, find({y}) = {root_y}")
            else:
                print("No pairs provided for find operation")

        elif args.operation == "connected":
            if pairs:
                for x, y in pairs:
                    result = uf.connected(x, y)
                    print(f"connected({x}, {y}) = {result}")
            else:
                print("No pairs provided for connected operation")

        elif args.operation == "components":
            all_components = uf.get_all_components()
            print(f"Number of components: {len(all_components)}")
            for root, component in all_components.items():
                print(f"  Component {root}: {component}")

        elif args.operation == "stats":
            stats = uf.get_component_statistics()
            print("Component Statistics:")
            print(f"  Count: {stats['count']}")
            print(f"  Largest size: {stats['largest_size']}")
            print(f"  Smallest size: {stats['smallest_size']}")
            print(f"  Average size: {stats['average_size']:.2f}")
            print(f"  Sizes: {stats['sizes']}")

        elif args.operation == "compare":
            if pairs:
                performance = uf.compare_performance(pairs, args.iterations)

                print(f"\nUnion-Find Performance:")
                print(f"Elements: {performance['num_elements']}")
                print(f"Pairs: {performance['num_pairs']}")
                print("-" * 60)

                methods = [
                    ("union_all", "union_all()"),
                    ("find_operations", "find() operations"),
                    ("connected_checks", "connected() checks"),
                ]

                for method_key, method_name in methods:
                    data = performance[method_key]
                    if data.get("success", False):
                        if method_key == "union_all":
                            print(
                                f"{method_name:20s}: "
                                f"unions={data['unions_performed']}, "
                                f"components={data['components']}  "
                                f"({data['time_milliseconds']:8.4f} ms)"
                            )
                        elif method_key == "find_operations":
                            print(
                                f"{method_name:20s}: "
                                f"ops={data['operations']}  "
                                f"({data['time_milliseconds']:8.4f} ms, "
                                f"{data['time_per_operation_microseconds']:.2f} μs/op)"
                            )
                        else:
                            print(
                                f"{method_name:20s}: "
                                f"checks={data['checks']}  "
                                f"({data['time_milliseconds']:8.4f} ms, "
                                f"{data['time_per_check_microseconds']:.2f} μs/check)"
                            )
                    else:
                        print(
                            f"{method_name:20s}: Failed - "
                            f"{data.get('error', 'Unknown')}"
                        )

                if args.report:
                    report = uf.generate_report(
                        performance, output_path=args.report
                    )
                    print(f"\nReport saved to {args.report}")
            else:
                print("No pairs provided for comparison operation")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
