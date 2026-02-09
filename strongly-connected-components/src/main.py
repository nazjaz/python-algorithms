"""Strongly Connected Components - Kosaraju's Algorithm.

This module provides functionality to find strongly connected components
(SCCs) in a directed graph using Kosaraju's algorithm. A strongly connected
component is a maximal set of vertices such that every vertex in the set
is reachable from every other vertex in the set.
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


class StronglyConnectedComponents:
    """Finds strongly connected components using Kosaraju's algorithm."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize StronglyConnectedComponents with configuration.

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

    def _transpose_graph(
        self, adjacency_list: Dict[int, List[int]], vertices: List[int]
    ) -> Dict[int, List[int]]:
        """Build transpose (reversed) graph.

        Args:
            adjacency_list: Original adjacency list.
            vertices: List of all vertices.

        Returns:
            Transpose adjacency list with all edges reversed.
        """
        transpose: Dict[int, List[int]] = {v: [] for v in vertices}

        for source in adjacency_list:
            for dest in adjacency_list[source]:
                if dest in transpose:
                    transpose[dest].append(source)

        logger.debug("Built transpose graph")
        return transpose

    def _dfs_fill_order(
        self,
        vertex: int,
        adjacency_list: Dict[int, List[int]],
        visited: Set[int],
        stack: List[int],
    ) -> None:
        """DFS helper to fill stack with vertices in order of finishing times.

        Performs DFS and pushes vertices to stack after all descendants
        are processed. This ensures vertices with later finishing times
        are at the top of the stack.

        Args:
            vertex: Current vertex to visit.
            adjacency_list: Adjacency list representation of graph.
            visited: Set of visited vertices.
            stack: Stack to store vertices in finishing time order.
        """
        visited.add(vertex)
        logger.debug(f"  Visiting vertex {vertex} (first pass)")

        for neighbor in adjacency_list.get(vertex, []):
            if neighbor not in visited:
                self._dfs_fill_order(neighbor, adjacency_list, visited, stack)

        stack.append(vertex)
        logger.debug(f"  Finished vertex {vertex}, added to stack")

    def _dfs_collect_scc(
        self,
        vertex: int,
        transpose: Dict[int, List[int]],
        visited: Set[int],
        scc: List[int],
    ) -> None:
        """DFS helper to collect vertices in current SCC.

        Performs DFS on transpose graph starting from given vertex,
        collecting all reachable vertices into the current SCC.

        Args:
            vertex: Current vertex to visit.
            transpose: Transpose adjacency list.
            visited: Set of visited vertices.
            scc: List to collect vertices in current SCC.
        """
        visited.add(vertex)
        scc.append(vertex)
        logger.debug(f"  Visiting vertex {vertex} (second pass), SCC size: {len(scc)}")

        for neighbor in transpose.get(vertex, []):
            if neighbor not in visited:
                self._dfs_collect_scc(neighbor, transpose, visited, scc)

    def find_sccs(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> List[List[int]]:
        """Find strongly connected components using Kosaraju's algorithm.

        Kosaraju's algorithm works in two passes:
        1. First DFS pass: Fill stack with vertices in order of finishing times
        2. Second DFS pass: Process vertices from stack on transpose graph
           to find SCCs

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            List of SCCs, where each SCC is a list of vertex indices.

        Raises:
            ValueError: If inputs are invalid.
        """
        adjacency_list, vertices = self._build_graph(edges, num_vertices)

        if not vertices:
            logger.info("Empty graph: returning empty SCC list")
            return []

        logger.info(
            f"Finding SCCs: {len(vertices)} vertices, "
            f"{len(edges)} edges"
        )

        # Step 1: First DFS pass - fill stack with vertices in finishing order
        visited: Set[int] = set()
        stack: List[int] = []

        for vertex in vertices:
            if vertex not in visited:
                self._dfs_fill_order(vertex, adjacency_list, visited, stack)

        logger.debug(f"Stack filled with {len(stack)} vertices")

        # Step 2: Build transpose graph
        transpose = self._transpose_graph(adjacency_list, vertices)

        # Step 3: Second DFS pass - process vertices from stack on transpose
        visited.clear()
        sccs: List[List[int]] = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                scc = []
                self._dfs_collect_scc(vertex, transpose, visited, scc)
                sccs.append(scc)
                logger.debug(f"Found SCC: {scc}")

        logger.info(f"Found {len(sccs)} strongly connected components")
        return sccs

    def get_scc_count(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> int:
        """Get count of strongly connected components.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Number of strongly connected components.
        """
        sccs = self.find_sccs(edges, num_vertices)
        return len(sccs)

    def get_largest_scc(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> Optional[List[int]]:
        """Get the largest strongly connected component.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Largest SCC as list of vertices, or None if graph is empty.
        """
        sccs = self.find_sccs(edges, num_vertices)
        if not sccs:
            return None
        return max(sccs, key=len)

    def get_scc_statistics(
        self, edges: List[Tuple[int, int]], num_vertices: Optional[int] = None
    ) -> Dict[str, any]:
        """Get statistics about strongly connected components.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.

        Returns:
            Dictionary containing SCC statistics:
                - count: Total number of SCCs
                - sizes: List of SCC sizes
                - largest_size: Size of largest SCC
                - smallest_size: Size of smallest SCC
                - average_size: Average SCC size
        """
        sccs = self.find_sccs(edges, num_vertices)
        if not sccs:
            return {
                "count": 0,
                "sizes": [],
                "largest_size": 0,
                "smallest_size": 0,
                "average_size": 0.0,
            }

        sizes = [len(scc) for scc in sccs]
        return {
            "count": len(sccs),
            "sizes": sizes,
            "largest_size": max(sizes),
            "smallest_size": min(sizes),
            "average_size": sum(sizes) / len(sizes) if sizes else 0.0,
        }

    def compare_performance(
        self,
        edges: List[Tuple[int, int]],
        num_vertices: Optional[int] = None,
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare performance of SCC finding operations.

        Args:
            edges: List of (source, destination) tuples representing edges.
            num_vertices: Number of vertices. If None, inferred from edges.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        adjacency_list, vertices = self._build_graph(edges, num_vertices)

        logger.info(
            f"Performance comparison: {len(vertices)} vertices, "
            f"{len(edges)} edges, iterations={iterations}"
        )

        results = {
            "num_vertices": len(vertices),
            "num_edges": len(edges),
            "iterations": iterations,
            "find_sccs": {},
            "get_scc_count": {},
            "get_largest_scc": {},
            "get_scc_statistics": {},
        }

        # find_sccs
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                sccs = self.find_sccs(edges, num_vertices)
            find_time = time.perf_counter() - start_time

            results["find_sccs"] = {
                "scc_count": len(sccs),
                "time_seconds": find_time / iterations,
                "time_milliseconds": (find_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"find_sccs failed: {e}")
            results["find_sccs"] = {"success": False, "error": str(e)}

        # get_scc_count
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                count = self.get_scc_count(edges, num_vertices)
            count_time = time.perf_counter() - start_time

            results["get_scc_count"] = {
                "count": count,
                "time_seconds": count_time / iterations,
                "time_milliseconds": (count_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"get_scc_count failed: {e}")
            results["get_scc_count"] = {"success": False, "error": str(e)}

        # get_largest_scc
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                largest = self.get_largest_scc(edges, num_vertices)
            largest_time = time.perf_counter() - start_time

            results["get_largest_scc"] = {
                "largest_size": len(largest) if largest else 0,
                "time_seconds": largest_time / iterations,
                "time_milliseconds": (largest_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"get_largest_scc failed: {e}")
            results["get_largest_scc"] = {"success": False, "error": str(e)}

        # get_scc_statistics
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                stats = self.get_scc_statistics(edges, num_vertices)
            stats_time = time.perf_counter() - start_time

            results["get_scc_statistics"] = {
                "statistics": stats,
                "time_seconds": stats_time / iterations,
                "time_milliseconds": (stats_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"get_scc_statistics failed: {e}")
            results["get_scc_statistics"] = {
                "success": False,
                "error": str(e),
            }

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for SCC operations.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "STRONGLY CONNECTED COMPONENTS PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of vertices: {performance_data['num_vertices']}",
            f"Number of edges: {performance_data['num_edges']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # find_sccs
        report_lines.append("\nfind_sccs():")
        find_data = performance_data["find_sccs"]
        if find_data.get("success", False):
            report_lines.append(f"  SCC count: {find_data['scc_count']}")
            report_lines.append(
                f"  Time: {find_data['time_milliseconds']:.4f} ms "
                f"({find_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {find_data.get('error', 'Unknown')}")

        # get_scc_count
        report_lines.append("\nget_scc_count():")
        count_data = performance_data["get_scc_count"]
        if count_data.get("success", False):
            report_lines.append(f"  Count: {count_data['count']}")
            report_lines.append(
                f"  Time: {count_data['time_milliseconds']:.4f} ms "
                f"({count_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {count_data.get('error', 'Unknown')}")

        # get_largest_scc
        report_lines.append("\nget_largest_scc():")
        largest_data = performance_data["get_largest_scc"]
        if largest_data.get("success", False):
            report_lines.append(f"  Largest SCC size: {largest_data['largest_size']}")
            report_lines.append(
                f"  Time: {largest_data['time_milliseconds']:.4f} ms "
                f"({largest_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {largest_data.get('error', 'Unknown')}"
            )

        # get_scc_statistics
        report_lines.append("\nget_scc_statistics():")
        stats_data = performance_data["get_scc_statistics"]
        if stats_data.get("success", False):
            stats = stats_data["statistics"]
            report_lines.append(f"  SCC count: {stats['count']}")
            report_lines.append(f"  Largest size: {stats['largest_size']}")
            report_lines.append(f"  Smallest size: {stats['smallest_size']}")
            report_lines.append(f"  Average size: {stats['average_size']:.2f}")
            report_lines.append(
                f"  Time: {stats_data['time_milliseconds']:.4f} ms "
                f"({stats_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(
                f"  Error: {stats_data.get('error', 'Unknown')}"
            )

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Kosaraju's Algorithm:",
            "  Time Complexity: O(V + E) where V=vertices, E=edges",
            "  Space Complexity: O(V + E) for adjacency lists and stack",
            "  Approach: Two-pass DFS",
            "    - First pass: Fill stack with vertices in finishing order",
            "    - Second pass: Process transpose graph to find SCCs",
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
        description="Find strongly connected components in directed graph "
        "using Kosaraju's algorithm"
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
        choices=["find", "count", "largest", "stats", "compare"],
        default="find",
        help="Operation method (default: find)",
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
        scc_finder = StronglyConnectedComponents(config_path=args.config)

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
            performance = scc_finder.compare_performance(
                edges, args.num_vertices, args.iterations
            )

            print(f"\nStrongly Connected Components Performance:")
            print(f"Vertices: {performance['num_vertices']}")
            print(f"Edges: {performance['num_edges']}")
            print("-" * 60)

            methods = [
                ("find_sccs", "find_sccs()"),
                ("get_scc_count", "get_scc_count()"),
                ("get_largest_scc", "get_largest_scc()"),
                ("get_scc_statistics", "get_scc_statistics()"),
            ]

            for method_key, method_name in methods:
                data = performance[method_key]
                if data.get("success", False):
                    if method_key == "get_scc_statistics":
                        stats = data["statistics"]
                        print(
                            f"{method_name:20s}: "
                            f"count={stats['count']}, "
                            f"largest={stats['largest_size']}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                    elif method_key == "get_scc_count":
                        print(
                            f"{method_name:20s}: "
                            f"count={data['count']}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                    elif method_key == "get_largest_scc":
                        print(
                            f"{method_name:20s}: "
                            f"size={data['largest_size']}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                    else:
                        print(
                            f"{method_name:20s}: "
                            f"count={data['scc_count']}  "
                            f"({data['time_milliseconds']:8.4f} ms)"
                        )
                else:
                    print(
                        f"{method_name:20s}: Failed - "
                        f"{data.get('error', 'Unknown')}"
                    )

            if args.report:
                report = scc_finder.generate_report(
                    performance, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        elif args.method == "find":
            sccs = scc_finder.find_sccs(edges, args.num_vertices)
            print(f"Strongly Connected Components ({len(sccs)} total):")
            for i, scc in enumerate(sccs):
                print(f"  SCC {i + 1}: {scc}")

        elif args.method == "count":
            count = scc_finder.get_scc_count(edges, args.num_vertices)
            print(f"Number of strongly connected components: {count}")

        elif args.method == "largest":
            largest = scc_finder.get_largest_scc(edges, args.num_vertices)
            if largest:
                print(f"Largest SCC: {largest} (size: {len(largest)})")
            else:
                print("No SCCs found (empty graph)")

        elif args.method == "stats":
            stats = scc_finder.get_scc_statistics(edges, args.num_vertices)
            print("SCC Statistics:")
            print(f"  Count: {stats['count']}")
            print(f"  Largest size: {stats['largest_size']}")
            print(f"  Smallest size: {stats['smallest_size']}")
            print(f"  Average size: {stats['average_size']:.2f}")
            print(f"  Sizes: {stats['sizes']}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
