"""Bellman-Ford Algorithm for Shortest Paths.

This module provides functionality to find shortest paths from a source
vertex using Bellman-Ford algorithm with negative edge detection and
cycle finding. The algorithm works with weighted directed graphs and can
detect negative cycles.
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


class BellmanFord:
    """Bellman-Ford algorithm for shortest paths with negative cycle detection."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BellmanFord with configuration.

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

    def find_shortest_paths(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        source: int,
    ) -> Tuple[List[float], List[Optional[int]], bool]:
        """Find shortest paths from source using Bellman-Ford algorithm.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.
            source: Source vertex.

        Returns:
            Tuple containing:
                - Distance array (shortest distances from source)
                - Parent array (for path reconstruction)
                - Boolean indicating if negative cycle exists

        Raises:
            ValueError: If inputs are invalid.

        Time Complexity: O(V*E) where V=vertices, E=edges
        Space Complexity: O(V)
        """
        if num_vertices < 0:
            raise ValueError("Number of vertices must be non-negative")

        if source < 0 or source >= num_vertices:
            raise ValueError(
                f"Source vertex {source} out of range [0, {num_vertices - 1}]"
            )

        if num_vertices == 0:
            logger.info("Empty graph: returning empty arrays")
            return [], [], False

        logger.info(
            f"Bellman-Ford: {num_vertices} vertices, {len(edges)} edges, "
            f"source={source}"
        )

        # Initialize distances
        dist = [float("inf")] * num_vertices
        dist[source] = 0.0
        parent: List[Optional[int]] = [None] * num_vertices

        logger.debug(f"  Initialized distances: source={source}, dist={dist}")

        # Relax edges V-1 times
        for i in range(num_vertices - 1):
            logger.debug(f"  Relaxation iteration {i + 1}")
            updated = False
            for u, v, w in edges:
                if dist[u] != float("inf") and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    updated = True
                    logger.debug(
                        f"    Relaxed edge ({u}, {v}): dist[{v}] = {dist[v]}"
                    )
            if not updated:
                logger.debug("    No updates in this iteration, early termination")
                break

        # Check for negative cycles
        has_negative_cycle = False
        logger.debug("  Checking for negative cycles")
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                has_negative_cycle = True
                logger.warning(
                    f"    Negative cycle detected: edge ({u}, {v}) "
                    f"can still be relaxed"
                )
                break

        if has_negative_cycle:
            logger.warning("Graph contains negative cycle reachable from source")
        else:
            logger.info("Shortest paths calculated successfully")

        return dist, parent, has_negative_cycle

    def find_negative_cycle(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        source: int,
    ) -> Optional[List[int]]:
        """Find negative cycle in graph.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.
            source: Source vertex.

        Returns:
            List of vertices in negative cycle, or None if no cycle exists.
        """
        dist, parent, has_negative_cycle = self.find_shortest_paths(
            num_vertices, edges, source
        )

        if not has_negative_cycle:
            return None

        logger.info("Finding negative cycle")

        # Find an edge that can still be relaxed
        cycle_start = None
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                cycle_start = v
                logger.debug(f"  Cycle detected starting at vertex {v}")
                break

        if cycle_start is None:
            return None

        # Trace back to find cycle
        # Use slow and fast pointer technique (Floyd's cycle detection)
        visited = set()
        current = cycle_start
        path: List[int] = []

        # Trace back through parent pointers
        for _ in range(num_vertices):
            if current is None:
                break
            if current in visited:
                # Found cycle, extract it
                cycle_start_idx = path.index(current)
                cycle = path[cycle_start_idx:] + [current]
                logger.info(f"  Negative cycle found: {cycle}")
                return cycle
            visited.add(current)
            path.append(current)
            current = parent[current]

        # Alternative: find cycle by following edges
        # Start from cycle_start and follow parent pointers
        cycle_vertices: List[int] = []
        current = cycle_start
        seen = set()

        for _ in range(num_vertices):
            if current is None:
                break
            if current in seen:
                # Extract cycle
                start_idx = cycle_vertices.index(current)
                cycle = cycle_vertices[start_idx:] + [current]
                logger.info(f"  Negative cycle found: {cycle}")
                return cycle
            seen.add(current)
            cycle_vertices.append(current)
            current = parent[current]

        return None

    def reconstruct_path(
        self, parent: List[Optional[int]], start: int, end: int
    ) -> Optional[List[int]]:
        """Reconstruct shortest path from start to end.

        Args:
            parent: Parent array from find_shortest_paths().
            start: Start vertex.
            end: End vertex.

        Returns:
            List of vertices in path, or None if no path exists.
        """
        if parent[end] is None and start != end:
            return None

        path: List[int] = []
        current = end

        while current is not None:
            path.append(current)
            if current == start:
                break
            current = parent[current]

        if path[-1] != start:
            return None

        path.reverse()
        logger.debug(f"Reconstructed path from {start} to {end}: {path}")
        return path

    def get_shortest_distance(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        source: int,
        target: int,
    ) -> Optional[float]:
        """Get shortest distance from source to target.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.
            source: Source vertex.
            target: Target vertex.

        Returns:
            Shortest distance, or None if no path exists or negative cycle.
        """
        dist, _, has_negative_cycle = self.find_shortest_paths(
            num_vertices, edges, source
        )

        if has_negative_cycle:
            return None

        if dist[target] == float("inf"):
            return None

        return dist[target]

    def get_all_distances(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        source: int,
    ) -> Tuple[List[float], bool]:
        """Get all shortest distances from source.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.
            source: Source vertex.

        Returns:
            Tuple containing distance array and negative cycle flag.
        """
        dist, _, has_negative_cycle = self.find_shortest_paths(
            num_vertices, edges, source
        )
        return dist, has_negative_cycle

    def compare_performance(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        source: int,
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare performance of Bellman-Ford algorithm.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.
            source: Source vertex.
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing performance data.
        """
        logger.info(
            f"Performance comparison: {num_vertices} vertices, "
            f"{len(edges)} edges, source={source}, iterations={iterations}"
        )

        results = {
            "num_vertices": num_vertices,
            "num_edges": len(edges),
            "source": source,
            "iterations": iterations,
            "bellman_ford": {},
        }

        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                dist, parent, has_negative_cycle = self.find_shortest_paths(
                    num_vertices, edges, source
                )
            bf_time = time.perf_counter() - start_time

            results["bellman_ford"] = {
                "time_seconds": bf_time / iterations,
                "time_milliseconds": (bf_time / iterations) * 1000,
                "has_negative_cycle": has_negative_cycle,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Bellman-Ford failed: {e}")
            results["bellman_ford"] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for Bellman-Ford algorithm.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "BELLMAN-FORD ALGORITHM PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of vertices: {performance_data['num_vertices']}",
            f"Number of edges: {performance_data['num_edges']}",
            f"Source vertex: {performance_data['source']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # Bellman-Ford results
        report_lines.append("\nBELLMAN-FORD ALGORITHM:")
        bf_data = performance_data["bellman_ford"]
        if bf_data.get("success", False):
            report_lines.append(
                f"  Time: {bf_data['time_milliseconds']:.4f} ms "
                f"({bf_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Negative cycle detected: {bf_data['has_negative_cycle']}"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {bf_data.get('error', 'Unknown')}")

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Bellman-Ford Algorithm:",
            "  Time Complexity: O(V*E) where V=vertices, E=edges",
            "  Space Complexity: O(V) for distance and parent arrays",
            "  Works with: Weighted directed graphs",
            "  Handles: Negative edge weights and negative cycles",
            "",
            "Key Features:",
            "  - Finds shortest paths from single source",
            "  - Can detect negative cycles",
            "  - Works with negative edge weights",
            "  - Supports path reconstruction",
            "  - More flexible than Dijkstra's algorithm",
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
        description="Bellman-Ford algorithm for shortest paths with "
        "negative edge detection and cycle finding"
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
        "-s",
        "--source",
        type=int,
        default=0,
        help="Source vertex (default: 0)",
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
        type=int,
        help="Query shortest distance to target vertex",
    )
    parser.add_argument(
        "-a",
        "--all-distances",
        action="store_true",
        help="Display all distances from source",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=int,
        help="Reconstruct path to target vertex",
    )
    parser.add_argument(
        "-cy",
        "--cycle",
        action="store_true",
        help="Find negative cycle",
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
        bf = BellmanFord(config_path=args.config)

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
            f"Input: {args.num_vertices} vertices, {len(edges)} edges, "
            f"source={args.source}"
        )

        # Find shortest paths
        dist, parent, has_negative_cycle = bf.find_shortest_paths(
            args.num_vertices, edges, args.source
        )

        if has_negative_cycle:
            print("WARNING: Graph contains negative cycle reachable from source!")
            print("Shortest paths may not be well-defined.")

        if args.query is not None:
            distance = bf.get_shortest_distance(
                args.num_vertices, edges, args.source, args.query
            )
            if distance is None:
                if has_negative_cycle:
                    print(f"No valid distance (negative cycle detected)")
                else:
                    print(f"No path from {args.source} to {args.query}")
            else:
                print(f"Shortest distance from {args.source} to {args.query}: {distance}")

        if args.path is not None:
            path = bf.reconstruct_path(parent, args.source, args.path)
            if path is None:
                print(f"No path from {args.source} to {args.path}")
            else:
                print(
                    f"Shortest path from {args.source} to {args.path}: "
                    f"{' -> '.join(map(str, path))}"
                )

        if args.all_distances:
            print(f"\nAll distances from source {args.source}:")
            for i, d in enumerate(dist):
                if d == float("inf"):
                    print(f"  {i}: INF")
                else:
                    print(f"  {i}: {d:.2f}")

        if args.cycle:
            cycle = bf.find_negative_cycle(
                args.num_vertices, edges, args.source
            )
            if cycle is None:
                print("No negative cycle found")
            else:
                print(f"Negative cycle found: {' -> '.join(map(str, cycle))}")

        if args.report:
            performance = bf.compare_performance(
                args.num_vertices, edges, args.source, args.iterations
            )
            report = bf.generate_report(performance, output_path=args.report)
            print(f"\nReport saved to {args.report}")

        if not any(
            [args.query is not None, args.path is not None, args.all_distances, args.cycle, args.report]
        ):
            print(f"Bellman-Ford algorithm executed successfully")
            print(f"Vertices: {args.num_vertices}, Edges: {len(edges)}, Source: {args.source}")
            if has_negative_cycle:
                print("WARNING: Negative cycle detected")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
