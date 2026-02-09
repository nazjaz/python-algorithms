"""Floyd-Warshall Algorithm for All-Pairs Shortest Paths.

This module provides functionality to find shortest paths between all pairs
of vertices using Floyd-Warshall algorithm with path reconstruction
capabilities. The algorithm works with weighted directed graphs and can
handle negative edge weights (but not negative cycles).
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


class FloydWarshall:
    """Floyd-Warshall algorithm for all-pairs shortest paths."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize FloydWarshall with configuration.

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

    def _build_adjacency_matrix(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> List[List[float]]:
        """Build adjacency matrix from edge list.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            Adjacency matrix (distance matrix).
        """
        # Initialize with infinity (no path) and 0 on diagonal
        dist = [[float("inf")] * num_vertices for _ in range(num_vertices)]
        for i in range(num_vertices):
            dist[i][i] = 0.0

        # Add edges
        for source, dest, weight in edges:
            if 0 <= source < num_vertices and 0 <= dest < num_vertices:
                dist[source][dest] = weight
                logger.debug(
                    f"  Edge: {source} -> {dest} with weight {weight}"
                )

        return dist

    def find_shortest_paths(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> Tuple[List[List[float]], List[List[Optional[int]]], bool]:
        """Find shortest paths between all pairs using Floyd-Warshall.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            Tuple containing:
                - Distance matrix (shortest distances)
                - Next matrix (for path reconstruction)
                - Boolean indicating if negative cycle exists

        Raises:
            ValueError: If inputs are invalid.

        Time Complexity: O(V³) where V is number of vertices
        Space Complexity: O(V²)
        """
        if num_vertices < 0:
            raise ValueError("Number of vertices must be non-negative")

        if num_vertices == 0:
            logger.info("Empty graph: returning empty matrices")
            return [], [], False

        logger.info(
            f"Floyd-Warshall: {num_vertices} vertices, {len(edges)} edges"
        )

        # Build initial distance matrix
        dist = self._build_adjacency_matrix(num_vertices, edges)

        # Initialize next matrix for path reconstruction
        next_matrix: List[List[Optional[int]]] = [
            [None] * num_vertices for _ in range(num_vertices)
        ]
        for i in range(num_vertices):
            for j in range(num_vertices):
                if i != j and dist[i][j] != float("inf"):
                    next_matrix[i][j] = j

        logger.debug("  Initialized distance and next matrices")

        # Floyd-Warshall algorithm
        for k in range(num_vertices):
            logger.debug(f"  Intermediate vertex k={k}")
            for i in range(num_vertices):
                for j in range(num_vertices):
                    # If going through k is shorter, update distance
                    if dist[i][k] != float("inf") and dist[k][j] != float("inf"):
                        new_dist = dist[i][k] + dist[k][j]
                        if new_dist < dist[i][j]:
                            dist[i][j] = new_dist
                            next_matrix[i][j] = next_matrix[i][k]
                            logger.debug(
                                f"    Updated dist[{i}][{j}] = {new_dist} "
                                f"(via k={k})"
                            )

        # Check for negative cycles
        has_negative_cycle = False
        for i in range(num_vertices):
            if dist[i][i] < 0:
                has_negative_cycle = True
                logger.warning(f"Negative cycle detected at vertex {i}")
                break

        if has_negative_cycle:
            logger.warning("Graph contains negative cycle")
        else:
            logger.info("Shortest paths calculated successfully")

        return dist, next_matrix, has_negative_cycle

    def reconstruct_path(
        self,
        next_matrix: List[List[Optional[int]]],
        start: int,
        end: int,
    ) -> Optional[List[int]]:
        """Reconstruct shortest path from start to end.

        Args:
            next_matrix: Next matrix from find_shortest_paths().
            start: Start vertex.
            end: End vertex.

        Returns:
            List of vertices in path, or None if no path exists.
        """
        if next_matrix[start][end] is None:
            return None

        path: List[int] = [start]
        current = start

        while current != end:
            current = next_matrix[current][end]
            if current is None:
                return None
            path.append(current)

        logger.debug(f"Reconstructed path from {start} to {end}: {path}")
        return path

    def get_shortest_distance(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start: int,
        end: int,
    ) -> Optional[float]:
        """Get shortest distance between two vertices.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.
            start: Start vertex.
            end: End vertex.

        Returns:
            Shortest distance, or None if no path exists or negative cycle.
        """
        dist, _, has_negative_cycle = self.find_shortest_paths(
            num_vertices, edges
        )

        if has_negative_cycle:
            return None

        if dist[start][end] == float("inf"):
            return None

        return dist[start][end]

    def get_all_distances(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> Tuple[List[List[float]], bool]:
        """Get all-pairs shortest distances.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            Tuple containing distance matrix and negative cycle flag.
        """
        dist, _, has_negative_cycle = self.find_shortest_paths(
            num_vertices, edges
        )
        return dist, has_negative_cycle

    def compare_performance(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare performance of Floyd-Warshall algorithm.

        Args:
            num_vertices: Number of vertices.
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
            "floyd_warshall": {},
        }

        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                dist, next_matrix, has_negative_cycle = self.find_shortest_paths(
                    num_vertices, edges
                )
            fw_time = time.perf_counter() - start_time

            results["floyd_warshall"] = {
                "time_seconds": fw_time / iterations,
                "time_milliseconds": (fw_time / iterations) * 1000,
                "has_negative_cycle": has_negative_cycle,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Floyd-Warshall failed: {e}")
            results["floyd_warshall"] = {"success": False, "error": str(e)}

        return results

    def generate_report(
        self,
        performance_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate performance report for Floyd-Warshall algorithm.

        Args:
            performance_data: Performance data from compare_performance().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "FLOYD-WARSHALL ALGORITHM PERFORMANCE REPORT",
            "=" * 80,
            "",
            f"Number of vertices: {performance_data['num_vertices']}",
            f"Number of edges: {performance_data['num_edges']}",
            f"Iterations: {performance_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # Floyd-Warshall results
        report_lines.append("\nFLOYD-WARSHALL ALGORITHM:")
        fw_data = performance_data["floyd_warshall"]
        if fw_data.get("success", False):
            report_lines.append(
                f"  Time: {fw_data['time_milliseconds']:.4f} ms "
                f"({fw_data['time_seconds']:.6f} seconds)"
            )
            report_lines.append(
                f"  Negative cycle detected: {fw_data['has_negative_cycle']}"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {fw_data.get('error', 'Unknown')}")

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Floyd-Warshall Algorithm:",
            "  Time Complexity: O(V³) where V=number of vertices",
            "  Space Complexity: O(V²) for distance and next matrices",
            "  Works with: Weighted directed graphs",
            "  Handles: Negative edge weights (but not negative cycles)",
            "",
            "Key Features:",
            "  - Finds shortest paths between all pairs of vertices",
            "  - Can detect negative cycles",
            "  - Supports path reconstruction",
            "  - Works with negative edge weights",
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
        description="Floyd-Warshall algorithm for all-pairs shortest paths "
        "with path reconstruction"
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
        "-q",
        "--query",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        help="Query shortest path from START to END",
    )
    parser.add_argument(
        "-a",
        "--all-pairs",
        action="store_true",
        help="Display all-pairs shortest distances",
    )
    parser.add_argument(
        "-p",
        "--path",
        nargs=2,
        type=int,
        metavar=("START", "END"),
        help="Reconstruct path from START to END",
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
        fw = FloydWarshall(config_path=args.config)

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

        # Find shortest paths
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(
            args.num_vertices, edges
        )

        if has_negative_cycle:
            print("WARNING: Graph contains negative cycle!")
            print("Shortest paths may not be well-defined.")

        if args.query:
            start, end = args.query
            distance = fw.get_shortest_distance(
                args.num_vertices, edges, start, end
            )
            if distance is None:
                if has_negative_cycle:
                    print(f"No valid distance (negative cycle detected)")
                else:
                    print(f"No path from {start} to {end}")
            else:
                print(f"Shortest distance from {start} to {end}: {distance}")

        if args.path:
            start, end = args.path
            path = fw.reconstruct_path(next_matrix, start, end)
            if path is None:
                print(f"No path from {start} to {end}")
            else:
                print(f"Shortest path from {start} to {end}: {' -> '.join(map(str, path))}")

        if args.all_pairs:
            print("\nAll-pairs shortest distances:")
            print("    ", end="")
            for j in range(args.num_vertices):
                print(f"{j:8d}", end="")
            print()
            for i in range(args.num_vertices):
                print(f"{i:4d}", end="")
                for j in range(args.num_vertices):
                    if dist[i][j] == float("inf"):
                        print("     INF", end="")
                    else:
                        print(f"{dist[i][j]:8.2f}", end="")
                print()

        if args.report:
            performance = fw.compare_performance(
                args.num_vertices, edges, args.iterations
            )
            report = fw.generate_report(performance, output_path=args.report)
            print(f"\nReport saved to {args.report}")

        if not any([args.query, args.path, args.all_pairs, args.report]):
            print(f"Floyd-Warshall algorithm executed successfully")
            print(f"Vertices: {args.num_vertices}, Edges: {len(edges)}")
            if has_negative_cycle:
                print("WARNING: Negative cycle detected")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
