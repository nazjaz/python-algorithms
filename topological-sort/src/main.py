"""Topological Sort Algorithm - Kahn's and DFS-based implementations.

This module provides functionality to perform topological sorting on
directed acyclic graphs (DAGs) with cycle detection. It includes both
Kahn's algorithm (BFS-based) and DFS-based approaches.
"""

import logging
import logging.handlers
import time
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class TopologicalSort:
    """Implements topological sort with cycle detection for DAGs."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize TopologicalSort with configuration.

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

    def _build_graph(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> Tuple[Dict[int, List[int]], List[int]]:
        """Build adjacency list representation of graph.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Tuple containing:
                - Adjacency list dictionary (vertex -> list of neighbors)
                - List of all vertices

        Raises:
            ValueError: If edges are invalid.
        """
        if not edges:
            if num_vertices is None:
                raise ValueError(
                    "Either edges or num_vertices must be provided"
                )
            return {}, list(range(num_vertices))

        all_vertices = set()
        for source, dest in edges:
            if source < 0 or dest < 0:
                raise ValueError("Vertex indices must be non-negative")
            all_vertices.add(source)
            all_vertices.add(dest)

        if num_vertices is not None:
            if num_vertices < len(all_vertices):
                raise ValueError(
                    f"num_vertices ({num_vertices}) is less than "
                    f"vertices in edges ({len(all_vertices)})"
                )
            vertices = list(range(num_vertices))
        else:
            vertices = sorted(all_vertices)

        adjacency_list: Dict[int, List[int]] = {v: [] for v in vertices}

        for source, dest in edges:
            if dest not in adjacency_list[source]:
                adjacency_list[source].append(dest)

        logger.debug(
            f"Built graph: {len(vertices)} vertices, "
            f"{len(edges)} edges"
        )

        return adjacency_list, vertices

    def _calculate_in_degrees(
        self, adjacency_list: Dict[int, List[int]], vertices: List[int]
    ) -> Dict[int, int]:
        """Calculate in-degree for each vertex.

        Args:
            adjacency_list: Adjacency list representation of graph.
            vertices: List of all vertices.

        Returns:
            Dictionary mapping vertex to its in-degree.
        """
        in_degrees = {v: 0 for v in vertices}

        for source in adjacency_list:
            for dest in adjacency_list[source]:
                if dest in in_degrees:
                    in_degrees[dest] += 1

        return in_degrees

    def sort_kahn(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> Tuple[Optional[List[int]], bool]:
        """Perform topological sort using Kahn's algorithm (BFS-based).

        Kahn's algorithm works by repeatedly removing vertices with
        in-degree 0. If all vertices are processed, the graph is a DAG.
        If not, a cycle exists.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Tuple containing:
                - Topological order (list of vertices) if DAG, None if cycle
                - Boolean indicating if cycle was detected

        Raises:
            ValueError: If inputs are invalid.
        """
        adjacency_list, vertices = self._build_graph(edges, num_vertices)

        if not vertices:
            logger.info("Empty graph: returning empty topological order")
            return [], False

        logger.info(
            f"Kahn's algorithm: {len(vertices)} vertices, "
            f"{len(edges)} edges"
        )

        in_degrees = self._calculate_in_degrees(adjacency_list, vertices)

        # Initialize queue with vertices having in-degree 0
        queue = deque([v for v in vertices if in_degrees[v] == 0])
        topological_order = []
        processed_count = 0

        while queue:
            current = queue.popleft()
            topological_order.append(current)
            processed_count += 1

            logger.debug(
                f"  Processing vertex {current} "
                f"(in-degree was 0)"
            )

            # Reduce in-degree of neighbors
            for neighbor in adjacency_list[current]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)
                    logger.debug(
                        f"    Vertex {neighbor} now has in-degree 0"
                    )

        # If not all vertices processed, cycle exists
        has_cycle = processed_count != len(vertices)

        if has_cycle:
            logger.warning(
                f"Cycle detected: only {processed_count}/{len(vertices)} "
                f"vertices processed"
            )
            return None, True

        logger.info(
            f"Topological order found: {topological_order} "
            f"({processed_count} vertices)"
        )

        return topological_order, False

    def _dfs_visit(
        self,
        vertex: int,
        adjacency_list: Dict[int, List[int]],
        visited: Set[int],
        rec_stack: Set[int],
        result: List[int],
    ) -> bool:
        """DFS helper to visit vertex and detect cycles.

        Args:
            vertex: Current vertex to visit.
            adjacency_list: Adjacency list representation of graph.
            visited: Set of visited vertices.
            rec_stack: Set of vertices in current recursion stack.
            result: List to store topological order (built in reverse).

        Returns:
            True if cycle detected, False otherwise.
        """
        visited.add(vertex)
        rec_stack.add(vertex)

        logger.debug(f"  Visiting vertex {vertex}")

        for neighbor in adjacency_list.get(vertex, []):
            if neighbor not in visited:
                if self._dfs_visit(
                    neighbor, adjacency_list, visited, rec_stack, result
                ):
                    return True
            elif neighbor in rec_stack:
                logger.debug(
                    f"    Cycle detected: back edge from {vertex} "
                    f"to {neighbor}"
                )
                return True

        rec_stack.remove(vertex)
        result.append(vertex)

        logger.debug(f"  Finished vertex {vertex}, added to result")

        return False

    def sort_dfs(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> Tuple[Optional[List[int]], bool]:
        """Perform topological sort using DFS-based algorithm.

        DFS-based algorithm uses depth-first search with recursion stack
        to detect cycles. Topological order is built by adding vertices
        after all their descendants are processed.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Tuple containing:
                - Topological order (list of vertices) if DAG, None if cycle
                - Boolean indicating if cycle was detected

        Raises:
            ValueError: If inputs are invalid.
        """
        adjacency_list, vertices = self._build_graph(edges, num_vertices)

        if not vertices:
            logger.info("Empty graph: returning empty topological order")
            return [], False

        logger.info(
            f"DFS algorithm: {len(vertices)} vertices, "
            f"{len(edges)} edges"
        )

        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        result: List[int] = []

        for vertex in vertices:
            if vertex not in visited:
                if self._dfs_visit(
                    vertex, adjacency_list, visited, rec_stack, result
                ):
                    logger.warning("Cycle detected during DFS traversal")
                    return None, True

        # Reverse result to get topological order
        result.reverse()
        topological_order = result

        logger.info(
            f"Topological order found: {topological_order} "
            f"({len(topological_order)} vertices)"
        )

        return topological_order, False

    def detect_cycle(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> Tuple[bool, Optional[List[int]]]:
        """Detect cycles in directed graph.

        Uses DFS-based approach to detect cycles. If cycle found,
        attempts to return cycle path.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Tuple containing:
                - Boolean indicating if cycle exists
                - Cycle path if cycle found, None otherwise
        """
        adjacency_list, vertices = self._build_graph(edges, num_vertices)

        if not vertices:
            return False, None

        logger.info(f"Cycle detection: {len(vertices)} vertices")

        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        parent: Dict[int, int] = {}

        def dfs_cycle(vertex: int) -> Optional[List[int]]:
            """DFS helper to detect cycle and return cycle path."""
            visited.add(vertex)
            rec_stack.add(vertex)

            for neighbor in adjacency_list.get(vertex, []):
                if neighbor not in visited:
                    parent[neighbor] = vertex
                    cycle = dfs_cycle(neighbor)
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # Cycle found, reconstruct path
                    cycle_path = [neighbor]
                    current = vertex
                    while current != neighbor:
                        cycle_path.append(current)
                        current = parent.get(current, neighbor)
                    cycle_path.reverse()
                    logger.debug(f"Cycle path: {cycle_path}")
                    return cycle_path

            rec_stack.remove(vertex)
            return None

        for vertex in vertices:
            if vertex not in visited:
                cycle_path = dfs_cycle(vertex)
                if cycle_path:
                    logger.warning(f"Cycle detected: {cycle_path}")
                    return True, cycle_path

        logger.info("No cycle detected")
        return False, None

    def compare_approaches(
        self,
        edges: List[Tuple[int, int]],
        num_vertices: Optional[int] = None,
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare Kahn's and DFS-based topological sort approaches.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing comparison data for both approaches.
        """
        logger.info(
            f"Comparing approaches: {len(edges)} edges, "
            f"iterations={iterations}"
        )

        adjacency_list, vertices = self._build_graph(edges, num_vertices)

        results = {
            "num_vertices": len(vertices),
            "num_edges": len(edges),
            "iterations": iterations,
            "kahn": {},
            "dfs": {},
            "cycle_detection": {},
        }

        # Cycle detection
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                has_cycle, cycle_path = self.detect_cycle(edges, num_vertices)
            cycle_time = time.perf_counter() - start_time

            results["cycle_detection"] = {
                "has_cycle": has_cycle,
                "cycle_path": cycle_path,
                "time_seconds": cycle_time / iterations,
                "time_milliseconds": (cycle_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Cycle detection failed: {e}")
            results["cycle_detection"] = {"success": False, "error": str(e)}

        # Kahn's algorithm
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                order_kahn, cycle_kahn = self.sort_kahn(edges, num_vertices)
            kahn_time = time.perf_counter() - start_time

            results["kahn"] = {
                "order": order_kahn,
                "has_cycle": cycle_kahn,
                "time_seconds": kahn_time / iterations,
                "time_milliseconds": (kahn_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Kahn's algorithm failed: {e}")
            results["kahn"] = {"success": False, "error": str(e)}

        # DFS algorithm
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                order_dfs, cycle_dfs = self.sort_dfs(edges, num_vertices)
            dfs_time = time.perf_counter() - start_time

            results["dfs"] = {
                "order": order_dfs,
                "has_cycle": cycle_dfs,
                "time_seconds": dfs_time / iterations,
                "time_milliseconds": (dfs_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"DFS algorithm failed: {e}")
            results["dfs"] = {"success": False, "error": str(e)}

        # Verify results match
        if (
            results["kahn"].get("success", False)
            and results["dfs"].get("success", False)
        ):
            if (
                results["kahn"]["has_cycle"] == results["dfs"]["has_cycle"]
                and not results["kahn"]["has_cycle"]
            ):
                order_kahn = results["kahn"]["order"]
                order_dfs = results["dfs"]["order"]
                if order_kahn == order_dfs:
                    logger.info("Both approaches produced identical orders")
                else:
                    logger.warning(
                        "Orders differ but both are valid topological orders"
                    )

        # Determine fastest
        successful_results = [
            (name, data)
            for name, data in [
                ("kahn", results["kahn"]),
                ("dfs", results["dfs"]),
            ]
            if data.get("success", False) and not data.get("has_cycle", False)
        ]

        if successful_results:
            fastest = min(
                successful_results, key=lambda x: x[1]["time_seconds"]
            )
            results["fastest"] = fastest[0]
            results["fastest_time"] = fastest[1]["time_seconds"]

        return results

    def generate_report(
        self,
        comparison_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate comparison report for topological sort solutions.

        Args:
            comparison_data: Comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "TOPOLOGICAL SORT ALGORITHM COMPARISON REPORT",
            "=" * 80,
            "",
            f"Number of vertices: {comparison_data['num_vertices']}",
            f"Number of edges: {comparison_data['num_edges']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "CYCLE DETECTION",
            "-" * 80,
        ]

        cycle_data = comparison_data["cycle_detection"]
        if cycle_data.get("success", False):
            has_cycle = cycle_data["has_cycle"]
            report_lines.append(f"Cycle detected: {has_cycle}")
            if has_cycle and cycle_data.get("cycle_path"):
                report_lines.append(
                    f"Cycle path: {cycle_data['cycle_path']}"
                )
            report_lines.append(
                f"Time: {cycle_data['time_milliseconds']:.4f} ms "
                f"({cycle_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"Status: Failed")
            report_lines.append(
                f"Error: {cycle_data.get('error', 'Unknown')}"
            )

        report_lines.extend([
            "",
            "RESULTS",
            "-" * 80,
        ])

        # Kahn's algorithm results
        report_lines.append("\nKAHN'S ALGORITHM (BFS-based):")
        kahn_data = comparison_data["kahn"]
        if kahn_data.get("success", False):
            if kahn_data.get("has_cycle", False):
                report_lines.append("  Status: Cycle detected")
            else:
                order = kahn_data.get("order")
                if order:
                    report_lines.append(f"  Topological order: {order}")
                else:
                    report_lines.append("  Topological order: None")
            report_lines.append(
                f"  Time: {kahn_data['time_milliseconds']:.4f} ms "
                f"({kahn_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {kahn_data.get('error', 'Unknown')}")

        # DFS algorithm results
        report_lines.append("\nDFS-BASED ALGORITHM:")
        dfs_data = comparison_data["dfs"]
        if dfs_data.get("success", False):
            if dfs_data.get("has_cycle", False):
                report_lines.append("  Status: Cycle detected")
            else:
                order = dfs_data.get("order")
                if order:
                    report_lines.append(f"  Topological order: {order}")
                else:
                    report_lines.append("  Topological order: None")
            report_lines.append(
                f"  Time: {dfs_data['time_milliseconds']:.4f} ms "
                f"({dfs_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {dfs_data.get('error', 'Unknown')}")

        if "fastest" in comparison_data:
            report_lines.extend([
                "",
                "PERFORMANCE SUMMARY",
                "-" * 80,
                f"Fastest method: {comparison_data['fastest']}",
                f"Fastest time: {comparison_data['fastest_time']*1000:.4f} ms",
            ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Kahn's Algorithm:",
            "  Time Complexity: O(V + E) where V=vertices, E=edges",
            "  Space Complexity: O(V) for queue and in-degree storage",
            "  Approach: BFS-based, processes vertices with in-degree 0",
            "",
            "DFS-based Algorithm:",
            "  Time Complexity: O(V + E) where V=vertices, E=edges",
            "  Space Complexity: O(V) for recursion stack and visited set",
            "  Approach: DFS-based, processes vertices in depth-first order",
            "",
            "Cycle Detection:",
            "  Time Complexity: O(V + E) where V=vertices, E=edges",
            "  Space Complexity: O(V) for recursion stack and visited set",
            "  Approach: DFS with recursion stack to detect back edges",
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
        description="Perform topological sort on directed acyclic graphs "
        "with cycle detection"
    )
    parser.add_argument(
        "-e",
        "--edges",
        nargs="+",
        type=str,
        help="Edges as 'source-dest' pairs (e.g., '0-1 1-2')",
    )
    parser.add_argument(
        "-n",
        "--num-vertices",
        type=int,
        help="Number of vertices (if not specified, inferred from edges)",
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
        choices=["kahn", "dfs", "compare", "cycle"],
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
        solver = TopologicalSort(config_path=args.config)

        # Parse edges
        edges: List[Tuple[int, int]] = []
        if args.edges:
            for edge_str in args.edges:
                try:
                    if "-" in edge_str:
                        source, dest = map(int, edge_str.split("-"))
                        edges.append((source, dest))
                    else:
                        raise ValueError(
                            f"Invalid edge format: {edge_str}. "
                            f"Use 'source-dest' format"
                        )
                except ValueError as e:
                    logger.error(f"Error parsing edge '{edge_str}': {e}")
                    raise

        logger.info(
            f"Input: {len(edges)} edges, "
            f"num_vertices={args.num_vertices}"
        )

        if args.method == "compare":
            comparison = solver.compare_approaches(
                edges, args.num_vertices, args.iterations
            )

            print(f"\nTopological Sort Comparison:")
            print(f"Vertices: {comparison['num_vertices']}")
            print(f"Edges: {comparison['num_edges']}")
            print("-" * 60)

            # Cycle detection
            cycle_data = comparison["cycle_detection"]
            if cycle_data.get("success", False):
                has_cycle = cycle_data["has_cycle"]
                print(f"Cycle detected: {has_cycle}")
                if has_cycle and cycle_data.get("cycle_path"):
                    print(f"Cycle path: {cycle_data['cycle_path']}")
            else:
                print(
                    f"Cycle detection: Failed - "
                    f"{cycle_data.get('error', 'Unknown')}"
                )

            # Kahn's algorithm
            kahn_data = comparison["kahn"]
            if kahn_data.get("success", False):
                if kahn_data.get("has_cycle", False):
                    print("Kahn's:        Cycle detected")
                else:
                    order = kahn_data.get("order")
                    status = (
                        f"Order={order}"
                        if order
                        else "No order (cycle)"
                    )
                    print(
                        f"Kahn's:        {status:30s} "
                        f"({kahn_data['time_milliseconds']:8.4f} ms)"
                    )
            else:
                print(
                    f"Kahn's:        Failed - "
                    f"{kahn_data.get('error', 'Unknown')}"
                )

            # DFS algorithm
            dfs_data = comparison["dfs"]
            if dfs_data.get("success", False):
                if dfs_data.get("has_cycle", False):
                    print("DFS:           Cycle detected")
                else:
                    order = dfs_data.get("order")
                    status = (
                        f"Order={order}"
                        if order
                        else "No order (cycle)"
                    )
                    print(
                        f"DFS:           {status:30s} "
                        f"({dfs_data['time_milliseconds']:8.4f} ms)"
                    )
            else:
                print(
                    f"DFS:           Failed - "
                    f"{dfs_data.get('error', 'Unknown')}"
                )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = solver.generate_report(
                    comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.method == "kahn":
            order, has_cycle = solver.sort_kahn(edges, args.num_vertices)
            if has_cycle:
                print("Cycle detected: Cannot perform topological sort")
            else:
                print(f"Topological order (Kahn's): {order}")

        elif args.method == "dfs":
            order, has_cycle = solver.sort_dfs(edges, args.num_vertices)
            if has_cycle:
                print("Cycle detected: Cannot perform topological sort")
            else:
                print(f"Topological order (DFS): {order}")

        elif args.method == "cycle":
            has_cycle, cycle_path = solver.detect_cycle(
                edges, args.num_vertices
            )
            if has_cycle:
                print(f"Cycle detected: {cycle_path}")
            else:
                print("No cycle detected: Graph is a DAG")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
