"""Kruskal's Algorithm for Minimum Spanning Tree.

This module provides functionality to find minimum spanning tree (MST)
in weighted graphs using Kruskal's algorithm. The algorithm uses
union-find data structure for efficient cycle detection.
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


class UnionFind:
    """Union-Find data structure for cycle detection in Kruskal's algorithm.

    Simplified implementation with path compression for efficient
    cycle detection during MST construction.
    """

    def __init__(self, num_vertices: int) -> None:
        """Initialize UnionFind.

        Args:
            num_vertices: Number of vertices.
        """
        self.parent = list(range(num_vertices))
        self.rank = [0] * num_vertices

    def find(self, x: int) -> int:
        """Find root with path compression.

        Args:
            x: Vertex to find root for.

        Returns:
            Root vertex.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union two sets using union by rank.

        Args:
            x: First vertex.
            y: Second vertex.

        Returns:
            True if union was performed, False if already in same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


class KruskalMST:
    """Kruskal's algorithm for finding minimum spanning tree."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize KruskalMST with configuration.

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

    def _validate_edge(
        self, edge: Tuple[int, int, float], num_vertices: int
    ) -> None:
        """Validate edge.

        Args:
            edge: Edge tuple (source, destination, weight).
            num_vertices: Number of vertices in graph.

        Raises:
            ValueError: If edge is invalid.
        """
        source, dest, weight = edge
        if source < 0 or source >= num_vertices:
            raise ValueError(
                f"Source vertex {source} out of range [0, {num_vertices - 1}]"
            )
        if dest < 0 or dest >= num_vertices:
            raise ValueError(
                f"Destination vertex {dest} out of range [0, {num_vertices - 1}]"
            )
        if source == dest:
            raise ValueError("Self-loops are not allowed in MST")
        if not isinstance(weight, (int, float)):
            raise ValueError(f"Weight must be numeric, got {type(weight)}")

    def find_mst(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> Tuple[List[Tuple[int, int, float]], float]:
        """Find minimum spanning tree using Kruskal's algorithm.

        Algorithm steps:
        1. Sort all edges by weight in ascending order
        2. Initialize union-find data structure
        3. Iterate through edges in sorted order
        4. Add edge to MST if it doesn't create a cycle
        5. Stop when we have V-1 edges (for V vertices)

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            Tuple containing:
                - List of edges in MST
                - Total weight of MST

        Raises:
            ValueError: If inputs are invalid or graph is disconnected.
        """
        if num_vertices < 0:
            raise ValueError("Number of vertices must be non-negative")

        if num_vertices == 0:
            logger.info("Empty graph: returning empty MST")
            return [], 0.0

        if num_vertices == 1:
            logger.info("Single vertex: returning empty MST")
            return [], 0.0

        logger.info(
            f"Finding MST: {num_vertices} vertices, {len(edges)} edges"
        )

        # Validate all edges
        for edge in edges:
            self._validate_edge(edge, num_vertices)

        # Sort edges by weight
        sorted_edges = sorted(edges, key=lambda e: e[2])
        logger.debug(f"Sorted {len(sorted_edges)} edges by weight")

        # Initialize union-find
        uf = UnionFind(num_vertices)
        mst_edges: List[Tuple[int, int, float]] = []
        total_weight = 0.0

        # Kruskal's algorithm
        for source, dest, weight in sorted_edges:
            if len(mst_edges) >= num_vertices - 1:
                break

            if uf.union(source, dest):
                mst_edges.append((source, dest, weight))
                total_weight += weight
                logger.debug(
                    f"  Added edge ({source}, {dest}, {weight}) to MST"
                )

        # Check if MST is complete
        if len(mst_edges) < num_vertices - 1:
            raise ValueError(
                f"Graph is disconnected: MST has {len(mst_edges)} edges, "
                f"expected {num_vertices - 1}"
            )

        logger.info(
            f"MST found: {len(mst_edges)} edges, total weight = {total_weight}"
        )

        return mst_edges, total_weight

    def get_mst_edges(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> List[Tuple[int, int, float]]:
        """Get edges in minimum spanning tree.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            List of edges in MST.
        """
        mst_edges, _ = self.find_mst(num_vertices, edges)
        return mst_edges

    def get_mst_weight(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> float:
        """Get total weight of minimum spanning tree.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            Total weight of MST.
        """
        _, total_weight = self.find_mst(num_vertices, edges)
        return total_weight

    def compare_performance(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare performance of MST operations.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        logger.info(
            f"Performance comparison: {num_vertices} vertices, "
            f"{len(edges)} edges, iterations={iterations}"
        )

        results = {
            "num_vertices": num_vertices,
            "num_edges": len(edges),
            "iterations": iterations,
            "find_mst": {},
            "get_mst_edges": {},
            "get_mst_weight": {},
        }

        # find_mst
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                mst_edges, total_weight = self.find_mst(num_vertices, edges)
            mst_time = time.perf_counter() - start_time

            results["find_mst"] = {
                "mst_edges": len(mst_edges),
                "total_weight": total_weight,
                "time_seconds": mst_time / iterations,
                "time_milliseconds": (mst_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"find_mst failed: {e}")
            results["find_mst"] = {"success": False, "error": str(e)}

        # get_mst_edges
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                mst_edges = self.get_mst_edges(num_vertices, edges)
            edges_time = time.perf_counter() - start_time

            results["get_mst_edges"] = {
                "mst_edges": len(mst_edges),
                "time_seconds": edges_time / iterations,
                "time_milliseconds": (edges_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"get_mst_edges failed: {e}")
            results["get_mst_edges"] = {"success": False, "error": str(e)}

        # get_mst_weight
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                weight = self.get_mst_weight(num_vertices, edges)
            weight_time = time.perf_counter() - start_time

            results["get_mst_weight"] = {
                "total_weight": weight,
                "time_seconds": weight_time / iterations,
                "time_milliseconds": (weight_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"get_mst_weight failed: {e}")
            results["get_mst_weight"] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for MST operations.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "KRUSKAL'S ALGORITHM PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of vertices: {performance_data['num_vertices']}",
            f"Number of edges: {performance_data['num_edges']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # find_mst
        report_lines.append("\nfind_mst():")
        mst_data = performance_data["find_mst"]
        if mst_data.get("success", False):
            report_lines.append(f"  MST edges: {mst_data['mst_edges']}")
            report_lines.append(f"  Total weight: {mst_data['total_weight']:.2f}")
            report_lines.append(
                f"  Time: {mst_data['time_milliseconds']:.4f} ms "
                f"({mst_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {mst_data.get('error', 'Unknown')}")

        # get_mst_edges
        report_lines.append("\nget_mst_edges():")
        edges_data = performance_data["get_mst_edges"]
        if edges_data.get("success", False):
            report_lines.append(f"  MST edges: {edges_data['mst_edges']}")
            report_lines.append(
                f"  Time: {edges_data['time_milliseconds']:.4f} ms "
                f"({edges_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {edges_data.get('error', 'Unknown')}")

        # get_mst_weight
        report_lines.append("\nget_mst_weight():")
        weight_data = performance_data["get_mst_weight"]
        if weight_data.get("success", False):
            report_lines.append(f"  Total weight: {weight_data['total_weight']:.2f}")
            report_lines.append(
                f"  Time: {weight_data['time_milliseconds']:.4f} ms "
                f"({weight_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {weight_data.get('error', 'Unknown')}"
            )

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Kruskal's Algorithm:",
            "  Time Complexity: O(E log E) where E=edges",
            "    - Sorting edges: O(E log E)",
            "    - Union-Find operations: O(E α(V)) where α is inverse Ackermann",
            "  Space Complexity: O(V) for union-find, O(E) for edges",
            "  Approach:",
            "    1. Sort all edges by weight",
            "    2. Use union-find to detect cycles",
            "    3. Add edges greedily if no cycle",
            "    4. Stop when V-1 edges added",
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
        description="Find minimum spanning tree using Kruskal's algorithm"
    )
    parser.add_argument(
        "-n",
        "--num-vertices",
        type=int,
        required=True,
        help="Number of vertices",
    )
    parser.add_argument(
        "-e",
        "--edges",
        nargs="+",
        type=str,
        help="Edges as 'source-dest-weight' (e.g., '0-1-5 1-2-3')",
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
        choices=["mst", "edges", "weight", "compare"],
        default="mst",
        help="Operation to perform (default: mst)",
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
        kruskal = KruskalMST(config_path=args.config)

        # Parse edges
        edges: List[Tuple[int, int, float]] = []
        if args.edges:
            for edge_str in args.edges:
                try:
                    parts = edge_str.split("-")
                    if len(parts) == 3:
                        source = int(parts[0])
                        dest = int(parts[1])
                        weight = float(parts[2])
                        edges.append((source, dest, weight))
                    else:
                        raise ValueError(
                            f"Invalid edge format: {edge_str}. "
                            f"Use 'source-dest-weight' format"
                        )
                except ValueError as e:
                    logger.error(f"Error parsing edge '{edge_str}': {e}")
                    raise

        logger.info(
            f"Input: {args.num_vertices} vertices, {len(edges)} edges"
        )

        if args.operation == "mst":
            mst_edges, total_weight = kruskal.find_mst(
                args.num_vertices, edges
            )
            print(f"Minimum Spanning Tree:")
            print(f"  Edges: {mst_edges}")
            print(f"  Total weight: {total_weight:.2f}")

        elif args.operation == "edges":
            mst_edges = kruskal.get_mst_edges(args.num_vertices, edges)
            print(f"MST Edges: {mst_edges}")

        elif args.operation == "weight":
            total_weight = kruskal.get_mst_weight(args.num_vertices, edges)
            print(f"MST Total Weight: {total_weight:.2f}")

        elif args.operation == "compare":
            performance = kruskal.compare_performance(
                args.num_vertices, edges, args.iterations
            )

            print(f"\nKruskal's Algorithm Performance:")
            print(f"Vertices: {performance['num_vertices']}")
            print(f"Edges: {performance['num_edges']}")
            print("-" * 60)

            methods = [
                ("find_mst", "find_mst()"),
                ("get_mst_edges", "get_mst_edges()"),
                ("get_mst_weight", "get_mst_weight()"),
            ]

            for method_key, method_name in methods:
                data = performance[method_key]
                if data.get("success", False):
                    if method_key == "find_mst":
                        print(
                            f"{method_name:20s}: "
                            f"edges={data['mst_edges']}, "
                            f"weight={data['total_weight']:.2f}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                    elif method_key == "get_mst_edges":
                        print(
                            f"{method_name:20s}: "
                            f"edges={data['mst_edges']}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                    else:
                        print(
                            f"{method_name:20s}: "
                            f"weight={data['total_weight']:.2f}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                else:
                    print(
                        f"{method_name:20s}: Failed - "
                        f"{data.get('error', 'Unknown')}"
                    )

            if args.report:
                report = kruskal.generate_report(
                    performance, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
