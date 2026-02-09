"""Dijkstra's Algorithm - Shortest Path in Weighted Graphs.

This module provides implementation of Dijkstra's algorithm for finding
shortest paths in weighted graphs. The algorithm uses a priority queue
(min-heap) for efficient vertex selection, ensuring optimal performance
for finding shortest paths from a source vertex to all other vertices.
"""

import argparse
import heapq
import logging
import logging.handlers
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class WeightedGraph:
    """Graph data structure with weighted edges using adjacency list."""

    def __init__(self, directed: bool = False) -> None:
        """Initialize weighted graph.

        Args:
            directed: If True, graph is directed; if False, undirected.
        """
        self.adjacency_list: Dict[Any, List[Tuple[Any, float]]] = defaultdict(list)
        self.directed = directed
        logger.debug(f"Initialized {'directed' if directed else 'undirected'} weighted graph")

    def add_edge(self, u: Any, v: Any, weight: float) -> None:
        """Add weighted edge to graph.

        Args:
            u: First vertex.
            v: Second vertex.
            weight: Edge weight (must be non-negative for Dijkstra's algorithm).
        """
        if weight < 0:
            logger.warning(f"Negative weight detected: {weight}. Dijkstra's algorithm requires non-negative weights.")
        
        logger.debug(f"Adding edge: {u} -> {v} (weight: {weight})")
        self.adjacency_list[u].append((v, weight))

        if not self.directed:
            self.adjacency_list[v].append((u, weight))

    def add_vertex(self, vertex: Any) -> None:
        """Add vertex to graph.

        Args:
            vertex: Vertex to add.
        """
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            logger.debug(f"Added vertex: {vertex}")

    def get_vertices(self) -> List[Any]:
        """Get all vertices in graph.

        Returns:
            List of all vertices.
        """
        return list(self.adjacency_list.keys())

    def get_neighbors(self, vertex: Any) -> List[Tuple[Any, float]]:
        """Get neighbors of a vertex with their edge weights.

        Args:
            vertex: Vertex to get neighbors for.

        Returns:
            List of tuples (neighbor, weight).
        """
        return self.adjacency_list.get(vertex, [])

    def visualize(self) -> str:
        """Generate visual representation of graph.

        Returns:
            String representation of graph structure.
        """
        lines = []
        lines.append("Weighted Graph Structure:")
        lines.append("=" * 50)

        for vertex in sorted(self.adjacency_list.keys()):
            neighbors = self.adjacency_list[vertex]
            if neighbors:
                neighbor_str = ", ".join(f"{n}(w:{w})" for n, w in neighbors)
                lines.append(f"{vertex} -> [{neighbor_str}]")
            else:
                lines.append(f"{vertex} -> []")

        lines.append("=" * 50)
        lines.append(f"Vertices: {len(self.adjacency_list)}")
        lines.append(f"Type: {'Directed' if self.directed else 'Undirected'}")

        return "\n".join(lines)


class Dijkstra:
    """Dijkstra's algorithm implementation with priority queue optimization."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize Dijkstra with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.distance: Dict[Any, float] = {}
        self.parent: Dict[Any, Optional[Any]] = {}
        self.visited: Set[Any] = set()

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

    def shortest_path(
        self, graph: WeightedGraph, start: Any, target: Any
    ) -> Tuple[Optional[List[Any]], float]:
        """Find shortest path from start to target using Dijkstra's algorithm.

        Args:
            graph: Weighted graph to search.
            start: Starting vertex.
            target: Target vertex.

        Returns:
            Tuple of (path, distance):
                - path: List of vertices from start to target, or None if no path
                - distance: Shortest distance, or float('inf') if no path

        Raises:
            ValueError: If start or target vertex not in graph.
        """
        logger.info(f"Finding shortest path from {start} to {target} using Dijkstra's algorithm")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")
        if target not in graph.adjacency_list:
            raise ValueError(f"Target vertex {target} not in graph")

        if start == target:
            return [start], 0.0

        # Initialize distances and parent tracking
        self.distance = {start: 0.0}
        self.parent = {start: None}
        self.visited = set()

        # Priority queue: (distance, vertex)
        # Using heap for efficient minimum extraction
        priority_queue = [(0.0, start)]

        while priority_queue:
            current_dist, current_vertex = heapq.heappop(priority_queue)

            # Skip if already processed with shorter distance
            if current_vertex in self.visited:
                continue

            # Mark as visited
            self.visited.add(current_vertex)

            # Check if we reached target
            if current_vertex == target:
                # Reconstruct path
                path = []
                current = target
                while current is not None:
                    path.append(current)
                    current = self.parent.get(current)
                path.reverse()

                logger.info(
                    f"Shortest path found: {path} (distance: {self.distance[target]})"
                )
                return path, self.distance[target]

            # Explore neighbors
            for neighbor, edge_weight in graph.get_neighbors(current_vertex):
                if neighbor in self.visited:
                    continue

                # Calculate new distance
                new_distance = current_dist + edge_weight

                # Update if shorter path found
                if neighbor not in self.distance or new_distance < self.distance[neighbor]:
                    self.distance[neighbor] = new_distance
                    self.parent[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (new_distance, neighbor))

                    logger.debug(
                        f"Updated distance to {neighbor}: {new_distance} "
                        f"(via {current_vertex})"
                    )

        # No path found
        logger.warning(f"No path found from {start} to {target}")
        return None, float('inf')

    def shortest_distances(self, graph: WeightedGraph, start: Any) -> Dict[Any, float]:
        """Find shortest distances from start to all reachable vertices.

        Args:
            graph: Weighted graph to search.
            start: Starting vertex.

        Returns:
            Dictionary mapping each vertex to its shortest distance from start.
            Unreachable vertices are not included.

        Raises:
            ValueError: If start vertex not in graph.
        """
        logger.info(f"Finding shortest distances from {start} to all vertices")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")

        # Initialize distances
        self.distance = {start: 0.0}
        self.parent = {start: None}
        self.visited = set()

        # Priority queue: (distance, vertex)
        priority_queue = [(0.0, start)]

        while priority_queue:
            current_dist, current_vertex = heapq.heappop(priority_queue)

            # Skip if already processed
            if current_vertex in self.visited:
                continue

            # Mark as visited
            self.visited.add(current_vertex)

            # Explore neighbors
            for neighbor, edge_weight in graph.get_neighbors(current_vertex):
                if neighbor in self.visited:
                    continue

                # Calculate new distance
                new_distance = current_dist + edge_weight

                # Update if shorter path found
                if neighbor not in self.distance or new_distance < self.distance[neighbor]:
                    self.distance[neighbor] = new_distance
                    self.parent[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        logger.info(
            f"Found distances to {len(self.distance)} vertices from {start}"
        )
        return self.distance.copy()

    def shortest_paths_from_source(
        self, graph: WeightedGraph, start: Any
    ) -> Dict[Any, Tuple[Optional[List[Any]], float]]:
        """Find shortest paths from start to all reachable vertices.

        Args:
            graph: Weighted graph to search.
            start: Starting vertex.

        Returns:
            Dictionary mapping each vertex to (path, distance) tuple.
            Unreachable vertices are not included.

        Raises:
            ValueError: If start vertex not in graph.
        """
        logger.info(f"Finding shortest paths from {start} to all vertices")

        # First, compute all shortest distances
        self.shortest_distances(graph, start)

        # Reconstruct paths for all vertices
        paths = {}
        for vertex in self.distance.keys():
            if vertex == start:
                paths[vertex] = ([start], 0.0)
            else:
                # Reconstruct path
                path = []
                current = vertex
                while current is not None:
                    path.append(current)
                    current = self.parent.get(current)
                path.reverse()
                paths[vertex] = (path, self.distance[vertex])

        logger.info(f"Computed paths to {len(paths)} vertices from {start}")
        return paths

    def generate_report(
        self,
        graph: WeightedGraph,
        start: Any,
        target: Optional[Any] = None,
        output_path: Optional[str] = None,
    ) -> str:
        """Generate detailed Dijkstra's algorithm analysis report.

        Args:
            graph: Graph that was traversed.
            start: Starting vertex.
            target: Optional target vertex for path analysis.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "DIJKSTRA'S ALGORITHM ANALYSIS REPORT",
            "=" * 80,
            "",
            "GRAPH INFORMATION",
            "-" * 80,
            graph.visualize(),
            "",
            "STARTING VERTEX",
            "-" * 80,
            f"Start: {start}",
            "",
        ]

        # Shortest Distances
        distances = self.shortest_distances(graph, start)
        report_lines.extend([
            "SHORTEST DISTANCES",
            "-" * 80,
        ])
        for vertex in sorted(distances.keys()):
            report_lines.append(f"  {start} -> {vertex}: {distances[vertex]}")
        report_lines.append("")

        # Shortest Path (if target provided)
        if target:
            path, distance = self.shortest_path(graph, start, target)
            report_lines.extend([
                "SHORTEST PATH",
                "-" * 80,
            ])
            if path:
                report_lines.append(f"Path: {' -> '.join(str(v) for v in path)}")
                report_lines.append(f"Distance: {distance}")
            else:
                report_lines.append(f"No path found from {start} to {target}")
            report_lines.append("")

        report_lines.extend([
            "ALGORITHM DETAILS",
            "-" * 80,
            "DIJKSTRA'S ALGORITHM:",
            "  - Greedy algorithm for shortest paths in weighted graphs",
            "  - Uses priority queue (min-heap) for efficient vertex selection",
            "  - Guarantees shortest path when all edge weights are non-negative",
            "  - Time: O((V + E) log V) with binary heap",
            "  - Space: O(V) for distance and parent tracking",
            "",
            "ALGORITHM STEPS",
            "-" * 80,
            "1. Initialize distance to start as 0, all others as infinity",
            "2. Add start vertex to priority queue",
            "3. While queue is not empty:",
            "   a. Extract vertex with minimum distance (u)",
            "   b. Mark u as visited",
            "   c. For each unvisited neighbor v of u:",
            "      - Calculate new distance = distance[u] + weight(u, v)",
            "      - If new distance < distance[v]:",
            "        * Update distance[v] = new distance",
            "        * Set parent[v] = u",
            "        * Add (distance[v], v) to priority queue",
            "4. Reconstruct path using parent pointers",
            "",
            "PRIORITY QUEUE OPTIMIZATION",
            "-" * 80,
            "- Uses Python's heapq (min-heap) for O(log n) operations",
            "- Always processes vertex with minimum distance first",
            "- Ensures optimal greedy selection",
            "- More efficient than checking all vertices each iteration",
            "",
            "PROPERTIES",
            "-" * 80,
            "- Works only with non-negative edge weights",
            "- Finds shortest path from single source to all vertices",
            "- Greedy algorithm (makes locally optimal choice)",
            "- Optimal for single-source shortest path problem",
            "- Can be extended for all-pairs shortest paths",
            "",
            "APPLICATIONS",
            "-" * 80,
            "1. GPS navigation and route planning",
            "2. Network routing protocols",
            "3. Social network analysis",
            "4. Game pathfinding",
            "5. Resource allocation",
            "6. Transportation planning",
            "7. Internet routing",
            "8. Map applications",
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
        description="Dijkstra's algorithm for shortest path in weighted graphs"
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-s",
        "--start",
        help="Starting vertex for Dijkstra's algorithm",
    )
    parser.add_argument(
        "-t",
        "--target",
        help="Target vertex for shortest path finding",
    )
    parser.add_argument(
        "--distances",
        action="store_true",
        help="Show shortest distances to all vertices",
    )
    parser.add_argument(
        "--paths",
        action="store_true",
        help="Show shortest paths to all vertices",
    )
    parser.add_argument(
        "-v",
        "--visualize",
        action="store_true",
        help="Show graph visualization",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for analysis report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example graphs",
    )

    args = parser.parse_args()

    try:
        dijkstra = Dijkstra(config_path=args.config)

        if args.demo:
            # Run demonstration
            print("\n=== Dijkstra's Algorithm Demonstration ===\n")

            # Example 1: Simple weighted graph
            print("Example 1: Simple Weighted Graph")
            graph1 = WeightedGraph(directed=False)
            graph1.add_edge(0, 1, 4.0)
            graph1.add_edge(0, 2, 1.0)
            graph1.add_edge(1, 3, 1.0)
            graph1.add_edge(2, 3, 5.0)
            graph1.add_edge(2, 4, 2.0)
            graph1.add_edge(3, 4, 3.0)

            if args.visualize:
                print("\n" + graph1.visualize())

            if args.distances:
                distances = dijkstra.shortest_distances(graph1, 0)
                print("\nShortest distances from 0:")
                for vertex in sorted(distances.keys()):
                    print(f"  0 -> {vertex}: {distances[vertex]}")

            if args.target:
                try:
                    target_vertex = int(args.target)
                    if target_vertex in graph1.get_vertices():
                        path, distance = dijkstra.shortest_path(graph1, 0, target_vertex)
                        if path:
                            print(f"\nShortest path from 0 to {args.target}: {path}")
                            print(f"Distance: {distance}")
                        else:
                            print(f"\nNo path found from 0 to {args.target}")
                    else:
                        print(f"\nTarget vertex {args.target} not in graph1")
                except ValueError:
                    print(f"\nInvalid target vertex: {args.target}")

            if args.paths:
                paths = dijkstra.shortest_paths_from_source(graph1, 0)
                print("\nShortest paths from 0:")
                for vertex in sorted(paths.keys()):
                    path, dist = paths[vertex]
                    print(f"  0 -> {vertex}: {path} (distance: {dist})")

            # Example 2: More complex graph
            print("\n\nExample 2: Complex Weighted Graph")
            graph2 = WeightedGraph(directed=False)
            graph2.add_edge("A", "B", 2.0)
            graph2.add_edge("A", "C", 4.0)
            graph2.add_edge("B", "C", 1.0)
            graph2.add_edge("B", "D", 7.0)
            graph2.add_edge("C", "D", 3.0)
            graph2.add_edge("C", "E", 5.0)
            graph2.add_edge("D", "E", 2.0)
            graph2.add_edge("D", "F", 1.0)
            graph2.add_edge("E", "F", 3.0)

            if args.visualize:
                print("\n" + graph2.visualize())

            if args.target:
                try:
                    if args.target in graph2.get_vertices():
                        path, distance = dijkstra.shortest_path(graph2, "A", args.target)
                        if path:
                            print(f"\nShortest path from A to {args.target}: {' -> '.join(path)}")
                            print(f"Distance: {distance}")
                        else:
                            print(f"\nNo path found from A to {args.target}")
                    else:
                        print(f"\nTarget vertex {args.target} not in graph2")
                except Exception as e:
                    logger.debug(f"Error finding path in graph2: {e}")

            # Example 3: Shortest path demonstration
            print("\n\nExample 3: Shortest Path Demonstration")
            graph3 = WeightedGraph(directed=False)
            graph3.add_edge(1, 2, 1.0)
            graph3.add_edge(1, 3, 4.0)
            graph3.add_edge(2, 3, 2.0)
            graph3.add_edge(2, 4, 5.0)
            graph3.add_edge(3, 4, 1.0)
            graph3.add_edge(4, 5, 3.0)

            path, distance = dijkstra.shortest_path(graph3, 1, 5)
            if path:
                print(f"Shortest path from 1 to 5: {' -> '.join(str(v) for v in path)}")
                print(f"Distance: {distance}")
                print("Note: Dijkstra's algorithm guarantees shortest path with non-negative weights!")

            if args.report:
                report = dijkstra.generate_report(
                    graph1, 0, target=args.target, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        else:
            print("Use --demo for demonstration")
            print("Dijkstra operations available:")
            print("  - shortest_path(graph, start, target)")
            print("  - shortest_distances(graph, start)")
            print("  - shortest_paths_from_source(graph, start)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
