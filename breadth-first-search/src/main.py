"""Breadth-First Search (BFS) Algorithm - Shortest Path in Unweighted Graphs.

This module provides implementation of breadth-first search algorithm for
finding shortest paths in unweighted graphs. BFS explores all vertices at
the current depth level before moving to the next level, making it ideal
for finding shortest paths in unweighted graphs.
"""

import argparse
import logging
import logging.handlers
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Graph:
    """Graph data structure using adjacency list representation."""

    def __init__(self, directed: bool = False) -> None:
        """Initialize graph.

        Args:
            directed: If True, graph is directed; if False, undirected.
        """
        self.adjacency_list: Dict[Any, List[Any]] = defaultdict(list)
        self.directed = directed
        logger.debug(f"Initialized {'directed' if directed else 'undirected'} graph")

    def add_edge(self, u: Any, v: Any) -> None:
        """Add edge to graph.

        Args:
            u: First vertex.
            v: Second vertex.
        """
        logger.debug(f"Adding edge: {u} -> {v}")
        self.adjacency_list[u].append(v)

        if not self.directed:
            self.adjacency_list[v].append(u)

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

    def get_neighbors(self, vertex: Any) -> List[Any]:
        """Get neighbors of a vertex.

        Args:
            vertex: Vertex to get neighbors for.

        Returns:
            List of neighboring vertices.
        """
        return self.adjacency_list.get(vertex, [])

    def visualize(self) -> str:
        """Generate visual representation of graph.

        Returns:
            String representation of graph structure.
        """
        lines = []
        lines.append("Graph Structure:")
        lines.append("=" * 50)

        for vertex in sorted(self.adjacency_list.keys()):
            neighbors = self.adjacency_list[vertex]
            if neighbors:
                neighbor_str = ", ".join(str(n) for n in neighbors)
                lines.append(f"{vertex} -> [{neighbor_str}]")
            else:
                lines.append(f"{vertex} -> []")

        lines.append("=" * 50)
        lines.append(f"Vertices: {len(self.adjacency_list)}")
        lines.append(f"Type: {'Directed' if self.directed else 'Undirected'}")

        return "\n".join(lines)


class BFS:
    """Breadth-First Search implementation for shortest path finding."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize BFS with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.visited: Set[Any] = set()
        self.distance: Dict[Any, int] = {}
        self.parent: Dict[Any, Optional[Any]] = {}

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

    def bfs_traversal(self, graph: Graph, start: Any) -> List[Any]:
        """Perform BFS traversal starting from given vertex.

        Args:
            graph: Graph to traverse.
            start: Starting vertex.

        Returns:
            List of vertices in BFS order.

        Raises:
            ValueError: If start vertex not in graph.
        """
        logger.info(f"Starting BFS traversal from vertex: {start}")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")

        self.visited = set()
        traversal_order = []
        queue = deque([start])
        self.visited.add(start)

        while queue:
            vertex = queue.popleft()
            traversal_order.append(vertex)

            logger.debug(f"Visiting vertex: {vertex}")

            # Add all unvisited neighbors to queue
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append(neighbor)

        logger.info(f"BFS traversal complete. Visited {len(traversal_order)} vertices")
        return traversal_order

    def shortest_path(
        self, graph: Graph, start: Any, target: Any
    ) -> Tuple[Optional[List[Any]], int]:
        """Find shortest path from start to target using BFS.

        BFS guarantees shortest path in unweighted graphs because it explores
        vertices level by level, ensuring the first path found is the shortest.

        Args:
            graph: Graph to search.
            start: Starting vertex.
            target: Target vertex.

        Returns:
            Tuple of (path, distance):
                - path: List of vertices from start to target, or None if no path
                - distance: Number of edges in shortest path, or -1 if no path

        Raises:
            ValueError: If start or target vertex not in graph.
        """
        logger.info(f"Finding shortest path from {start} to {target}")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")
        if target not in graph.adjacency_list:
            raise ValueError(f"Target vertex {target} not in graph")

        if start == target:
            return [start], 0

        # Initialize BFS data structures
        self.visited = set()
        self.distance = {start: 0}
        self.parent = {start: None}
        queue = deque([start])
        self.visited.add(start)

        while queue:
            vertex = queue.popleft()

            # Check if we reached target
            if vertex == target:
                # Reconstruct path
                path = []
                current = target
                while current is not None:
                    path.append(current)
                    current = self.parent.get(current)
                path.reverse()
                distance = self.distance[target]

                logger.info(
                    f"Shortest path found: {path} (distance: {distance})"
                )
                return path, distance

            # Explore neighbors
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.distance[neighbor] = self.distance[vertex] + 1
                    self.parent[neighbor] = vertex
                    queue.append(neighbor)

                    logger.debug(
                        f"Discovered {neighbor} from {vertex} "
                        f"(distance: {self.distance[neighbor]})"
                    )

        # No path found
        logger.warning(f"No path found from {start} to {target}")
        return None, -1

    def shortest_distances(self, graph: Graph, start: Any) -> Dict[Any, int]:
        """Find shortest distances from start to all reachable vertices.

        Args:
            graph: Graph to search.
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

        self.visited = set()
        self.distance = {start: 0}
        queue = deque([start])
        self.visited.add(start)

        while queue:
            vertex = queue.popleft()

            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    self.distance[neighbor] = self.distance[vertex] + 1
                    queue.append(neighbor)

        logger.info(
            f"Found distances to {len(self.distance)} vertices from {start}"
        )
        return self.distance.copy()

    def bfs_all_components(self, graph: Graph) -> List[List[Any]]:
        """Perform BFS on all connected components.

        Args:
            graph: Graph to traverse.

        Returns:
            List of traversal orders for each component.
        """
        logger.info("Finding all connected components using BFS")

        all_components = []
        visited_all = set()

        for vertex in graph.get_vertices():
            if vertex not in visited_all:
                component = self.bfs_traversal(graph, vertex)
                all_components.append(component)
                visited_all.update(component)

        logger.info(f"Found {len(all_components)} connected components")
        return all_components

    def level_order_traversal(self, graph: Graph, start: Any) -> List[List[Any]]:
        """Get vertices grouped by level (distance from start).

        Args:
            graph: Graph to traverse.
            start: Starting vertex.

        Returns:
            List of lists, where each inner list contains vertices at that level.

        Raises:
            ValueError: If start vertex not in graph.
        """
        logger.info(f"Performing level-order traversal from {start}")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")

        levels = []
        self.visited = set()
        queue = deque([(start, 0)])
        self.visited.add(start)

        current_level = 0
        current_level_vertices = []

        while queue:
            vertex, level = queue.popleft()

            # New level started
            if level > current_level:
                levels.append(current_level_vertices)
                current_level_vertices = []
                current_level = level

            current_level_vertices.append(vertex)

            # Add neighbors to next level
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in self.visited:
                    self.visited.add(neighbor)
                    queue.append((neighbor, level + 1))

        # Add last level
        if current_level_vertices:
            levels.append(current_level_vertices)

        logger.info(f"Found {len(levels)} levels from {start}")
        return levels

    def generate_report(
        self,
        graph: Graph,
        start: Any,
        target: Optional[Any] = None,
        output_path: Optional[str] = None,
    ) -> str:
        """Generate detailed BFS analysis report.

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
            "BREADTH-FIRST SEARCH (BFS) ANALYSIS REPORT",
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

        # BFS Traversal
        traversal = self.bfs_traversal(graph, start)
        report_lines.extend([
            "BFS TRAVERSAL",
            "-" * 80,
            f"Traversal Order: {traversal}",
            f"Vertices Visited: {len(traversal)}",
            "",
        ])

        # Level Order
        levels = self.level_order_traversal(graph, start)
        report_lines.extend([
            "LEVEL-ORDER TRAVERSAL",
            "-" * 80,
        ])
        for i, level_vertices in enumerate(levels):
            report_lines.append(f"Level {i}: {level_vertices}")
        report_lines.append("")

        # Shortest Distances
        distances = self.shortest_distances(graph, start)
        report_lines.extend([
            "SHORTEST DISTANCES",
            "-" * 80,
        ])
        for vertex in sorted(distances.keys()):
            report_lines.append(f"  {start} -> {vertex}: {distances[vertex]} edges")
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
                report_lines.append(f"Distance: {distance} edges")
            else:
                report_lines.append(f"No path found from {start} to {target}")
            report_lines.append("")

        report_lines.extend([
            "ALGORITHM DETAILS",
            "-" * 80,
            "BFS ALGORITHM:",
            "  - Explores graph level by level (breadth-first)",
            "  - Uses queue data structure (FIFO)",
            "  - Guarantees shortest path in unweighted graphs",
            "  - Time: O(V + E) where V=vertices, E=edges",
            "  - Space: O(V) for queue and visited set",
            "",
            "ALGORITHM STEPS",
            "-" * 80,
            "1. Initialize queue with start vertex",
            "2. Mark start as visited",
            "3. While queue is not empty:",
            "   a. Dequeue vertex",
            "   b. Process/visit vertex",
            "   c. Enqueue all unvisited neighbors",
            "   d. Mark neighbors as visited",
            "4. Continue until queue is empty",
            "",
            "SHORTEST PATH FINDING",
            "-" * 80,
            "1. Use BFS to explore graph level by level",
            "2. Track parent of each vertex",
            "3. When target is found, backtrack using parents",
            "4. First path found is guaranteed to be shortest",
            "",
            "PROPERTIES",
            "-" * 80,
            "- Explores all vertices at current level before next level",
            "- Guarantees shortest path in unweighted graphs",
            "- Visits all vertices in connected component",
            "- Level-order traversal (distance from start)",
            "- Uses queue (FIFO) instead of stack (LIFO)",
            "",
            "APPLICATIONS",
            "-" * 80,
            "1. Shortest path in unweighted graphs",
            "2. Level-order tree traversal",
            "3. Social network analysis (degrees of separation)",
            "4. Web crawling",
            "5. GPS navigation (unweighted roads)",
            "6. Puzzle solving (minimum moves)",
            "7. Connected component detection",
            "8. Cycle detection in undirected graphs",
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
        description="Breadth-first search algorithm for shortest path in unweighted graphs"
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
        help="Starting vertex for BFS",
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
        "--levels",
        action="store_true",
        help="Show level-order traversal",
    )
    parser.add_argument(
        "--components",
        action="store_true",
        help="Find all connected components",
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
        bfs = BFS(config_path=args.config)

        if args.demo:
            # Run demonstration
            print("\n=== Breadth-First Search Demonstration ===\n")

            # Example 1: Simple graph
            print("Example 1: Simple Graph")
            graph1 = Graph(directed=False)
            graph1.add_edge(0, 1)
            graph1.add_edge(0, 2)
            graph1.add_edge(1, 3)
            graph1.add_edge(2, 4)
            graph1.add_edge(3, 5)

            if args.visualize:
                print("\n" + graph1.visualize())

            traversal = bfs.bfs_traversal(graph1, 0)
            print(f"\nBFS Traversal from 0: {traversal}")

            if args.levels:
                levels = bfs.level_order_traversal(graph1, 0)
                print("\nLevel-order traversal:")
                for i, level in enumerate(levels):
                    print(f"  Level {i}: {level}")

            if args.distances:
                distances = bfs.shortest_distances(graph1, 0)
                print("\nShortest distances from 0:")
                for vertex in sorted(distances.keys()):
                    print(f"  0 -> {vertex}: {distances[vertex]} edges")

            if args.target:
                try:
                    target_vertex = int(args.target)
                    if target_vertex in graph1.get_vertices():
                        path, distance = bfs.shortest_path(graph1, 0, target_vertex)
                        if path:
                            print(f"\nShortest path from 0 to {args.target}: {path}")
                            print(f"Distance: {distance} edges")
                        else:
                            print(f"\nNo path found from 0 to {args.target}")
                    else:
                        print(f"\nTarget vertex {args.target} not in graph1")
                except ValueError:
                    print(f"\nInvalid target vertex: {args.target}")

            # Example 2: More complex graph
            print("\n\nExample 2: Complex Graph")
            graph2 = Graph(directed=False)
            graph2.add_edge("A", "B")
            graph2.add_edge("A", "C")
            graph2.add_edge("B", "D")
            graph2.add_edge("B", "E")
            graph2.add_edge("C", "F")
            graph2.add_edge("D", "G")
            graph2.add_edge("E", "H")

            if args.visualize:
                print("\n" + graph2.visualize())

            traversal = bfs.bfs_traversal(graph2, "A")
            print(f"\nBFS Traversal from A: {traversal}")

            if args.target:
                try:
                    # Try as string first (for graph2)
                    if args.target in graph2.get_vertices():
                        path, distance = bfs.shortest_path(graph2, "A", args.target)
                        if path:
                            print(f"\nShortest path from A to {args.target}: {' -> '.join(path)}")
                            print(f"Distance: {distance} edges")
                        else:
                            print(f"\nNo path found from A to {args.target}")
                    else:
                        print(f"\nTarget vertex {args.target} not in graph2")
                except Exception as e:
                    logger.debug(f"Error finding path in graph2: {e}")

            # Example 3: Shortest path demonstration
            print("\n\nExample 3: Shortest Path Demonstration")
            graph3 = Graph(directed=False)
            graph3.add_edge(1, 2)
            graph3.add_edge(1, 3)
            graph3.add_edge(2, 4)
            graph3.add_edge(2, 5)
            graph3.add_edge(3, 6)
            graph3.add_edge(4, 7)
            graph3.add_edge(5, 7)

            path, distance = bfs.shortest_path(graph3, 1, 7)
            if path:
                print(f"Shortest path from 1 to 7: {' -> '.join(str(v) for v in path)}")
                print(f"Distance: {distance} edges")
                print("Note: BFS guarantees this is the shortest path!")

            # Example 4: Connected components
            if args.components:
                print("\n\nExample 4: Connected Components")
                graph4 = Graph(directed=False)
                graph4.add_edge(1, 2)
                graph4.add_edge(2, 3)
                graph4.add_edge(4, 5)
                graph4.add_vertex(6)

                components = bfs.bfs_all_components(graph4)
                print(f"Found {len(components)} connected components:")
                for i, component in enumerate(components, 1):
                    print(f"  Component {i}: {component}")

            if args.report:
                report = bfs.generate_report(
                    graph1, 0, target=args.target, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        else:
            print("Use --demo for demonstration")
            print("BFS operations available:")
            print("  - bfs_traversal(graph, start)")
            print("  - shortest_path(graph, start, target)")
            print("  - shortest_distances(graph, start)")
            print("  - level_order_traversal(graph, start)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
