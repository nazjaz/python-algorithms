"""Depth-First Search (DFS) Algorithm - Recursive and Iterative.

This module provides implementations of depth-first search algorithm on a
graph using both recursive and iterative approaches. It includes graph
representation, traversal visualization, and performance comparison.
"""

import argparse
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


class DFS:
    """Depth-First Search implementation with recursive and iterative methods."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize DFS with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.traversal_path: List[Any] = []
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

    def dfs_recursive(
        self, graph: Graph, start: Any, track_path: bool = True
    ) -> List[Any]:
        """Perform DFS using recursive approach.

        Args:
            graph: Graph to traverse.
            start: Starting vertex.
            track_path: If True, track traversal path.

        Returns:
            List of vertices in DFS order.

        Raises:
            ValueError: If start vertex not in graph.
        """
        logger.info(f"Starting DFS recursive from vertex: {start}")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")

        if track_path:
            self.traversal_path = []
            self.visited = set()

        def _dfs_recursive_helper(vertex: Any) -> None:
            """Recursive helper function."""
            if vertex in self.visited:
                return

            self.visited.add(vertex)
            if track_path:
                self.traversal_path.append(vertex)

            logger.debug(f"Visiting vertex: {vertex}")

            # Visit all neighbors
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in self.visited:
                    _dfs_recursive_helper(neighbor)

        _dfs_recursive_helper(start)
        logger.info(f"DFS recursive complete. Visited {len(self.visited)} vertices")
        return self.traversal_path.copy() if track_path else list(self.visited)

    def dfs_iterative(
        self, graph: Graph, start: Any, track_path: bool = True
    ) -> List[Any]:
        """Perform DFS using iterative approach with stack.

        Args:
            graph: Graph to traverse.
            start: Starting vertex.
            track_path: If True, track traversal path.

        Returns:
            List of vertices in DFS order.

        Raises:
            ValueError: If start vertex not in graph.
        """
        logger.info(f"Starting DFS iterative from vertex: {start}")

        if start not in graph.adjacency_list:
            raise ValueError(f"Start vertex {start} not in graph")

        if track_path:
            self.traversal_path = []
        self.visited = set()

        # Use stack for iterative DFS
        stack = [start]

        while stack:
            vertex = stack.pop()

            if vertex not in self.visited:
                self.visited.add(vertex)
                if track_path:
                    self.traversal_path.append(vertex)

                logger.debug(f"Visiting vertex: {vertex}")

                # Add neighbors to stack (reverse order for same traversal as recursive)
                neighbors = graph.get_neighbors(vertex)
                for neighbor in reversed(neighbors):
                    if neighbor not in self.visited:
                        stack.append(neighbor)

        logger.info(f"DFS iterative complete. Visited {len(self.visited)} vertices")
        return self.traversal_path.copy() if track_path else list(self.visited)

    def dfs_all_components(self, graph: Graph, method: str = "recursive") -> List[List[Any]]:
        """Perform DFS on all connected components.

        Args:
            graph: Graph to traverse.
            method: Method to use ('recursive' or 'iterative').

        Returns:
            List of traversal paths for each component.
        """
        logger.info(f"Finding all connected components using {method} DFS")

        all_components = []
        visited_all = set()

        for vertex in graph.get_vertices():
            if vertex not in visited_all:
                if method == "recursive":
                    component = self.dfs_recursive(graph, vertex, track_path=True)
                else:
                    component = self.dfs_iterative(graph, vertex, track_path=True)

                all_components.append(component)
                visited_all.update(component)

        logger.info(f"Found {len(all_components)} connected components")
        return all_components

    def find_path(
        self, graph: Graph, start: Any, target: Any, method: str = "recursive"
    ) -> Optional[List[Any]]:
        """Find path from start to target using DFS.

        Args:
            graph: Graph to search.
            start: Starting vertex.
            target: Target vertex.
            method: Method to use ('recursive' or 'iterative').

        Returns:
            Path from start to target, or None if no path exists.
        """
        logger.info(f"Finding path from {start} to {target} using {method} DFS")

        if method == "recursive":
            path = []
            visited = set()

            def _dfs_path_helper(vertex: Any, current_path: List[Any]) -> bool:
                """Recursive helper for path finding."""
                if vertex == target:
                    path.extend(current_path + [vertex])
                    return True

                if vertex in visited:
                    return False

                visited.add(vertex)
                current_path.append(vertex)

                for neighbor in graph.get_neighbors(vertex):
                    if neighbor not in visited:
                        if _dfs_path_helper(neighbor, current_path):
                            return True

                current_path.pop()
                return False

            _dfs_path_helper(start, [])
            return path if path else None

        else:
            # Iterative approach
            stack = [(start, [start])]
            visited = set()

            while stack:
                vertex, path = stack.pop()

                if vertex == target:
                    return path

                if vertex not in visited:
                    visited.add(vertex)

                    for neighbor in graph.get_neighbors(vertex):
                        if neighbor not in visited:
                            stack.append((neighbor, path + [neighbor]))

            return None

    def compare_methods(
        self, graph: Graph, start: Any
    ) -> Dict[str, Dict[str, Any]]:
        """Compare recursive and iterative DFS methods.

        Args:
            graph: Graph to traverse.
            start: Starting vertex.

        Returns:
            Dictionary with comparison results.
        """
        logger.info(f"Comparing DFS methods starting from {start}")

        import time

        # Test recursive method
        start_time = time.perf_counter()
        recursive_path = self.dfs_recursive(graph, start, track_path=True)
        recursive_time = time.perf_counter() - start_time

        # Test iterative method
        start_time = time.perf_counter()
        iterative_path = self.dfs_iterative(graph, start, track_path=True)
        iterative_time = time.perf_counter() - start_time

        results = {
            "recursive": {
                "path": recursive_path,
                "execution_time": recursive_time,
                "vertices_visited": len(recursive_path),
                "method": "Recursive DFS",
            },
            "iterative": {
                "path": iterative_path,
                "execution_time": iterative_time,
                "vertices_visited": len(iterative_path),
                "method": "Iterative DFS (Stack-based)",
            },
            "paths_match": recursive_path == iterative_path,
        }

        logger.info(
            f"Comparison complete: recursive={recursive_time:.10f}s, "
            f"iterative={iterative_time:.10f}s"
        )

        return results

    def generate_report(
        self,
        graph: Graph,
        start: Any,
        comparison_results: Dict[str, Dict[str, Any]],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate detailed DFS analysis report.

        Args:
            graph: Graph that was traversed.
            start: Starting vertex.
            comparison_results: Results from compare_methods.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "DEPTH-FIRST SEARCH (DFS) ANALYSIS REPORT",
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
            "TRAVERSAL RESULTS",
            "-" * 80,
        ]

        for method_name in ["recursive", "iterative"]:
            result = comparison_results[method_name]
            report_lines.append(f"\n{method_name.upper().replace('_', ' ')}:")
            report_lines.append(f"  Method: {result['method']}")
            report_lines.append(f"  Execution Time: {result['execution_time']:.10f} seconds")
            report_lines.append(f"  Vertices Visited: {result['vertices_visited']}")
            report_lines.append(f"  Traversal Path: {result['path']}")

        report_lines.extend([
            "",
            f"Paths Match: {comparison_results['paths_match']}",
            "",
            "ALGORITHM DETAILS",
            "-" * 80,
            "RECURSIVE DFS:",
            "  - Uses function call stack for backtracking",
            "  - Natural recursive implementation",
            "  - May cause stack overflow for deep graphs",
            "  - Time: O(V + E) where V=vertices, E=edges",
            "  - Space: O(V) for recursion stack",
            "",
            "ITERATIVE DFS:",
            "  - Uses explicit stack data structure",
            "  - More control over traversal",
            "  - Avoids stack overflow issues",
            "  - Time: O(V + E) where V=vertices, E=edges",
            "  - Space: O(V) for stack",
            "",
            "ALGORITHM STEPS",
            "-" * 80,
            "1. Mark current vertex as visited",
            "2. Process/visit current vertex",
            "3. For each unvisited neighbor:",
            "   - Recursively/iteratively visit neighbor",
            "4. Backtrack when no more unvisited neighbors",
            "",
            "PROPERTIES",
            "-" * 80,
            "- Explores as far as possible along each branch",
            "- Backtracks when reaches dead end",
            "- Visits all vertices in connected component",
            "- Can be used for path finding",
            "- Useful for cycle detection",
            "- Foundation for many graph algorithms",
            "",
            "APPLICATIONS",
            "-" * 80,
            "1. Path finding between vertices",
            "2. Cycle detection in graphs",
            "3. Topological sorting",
            "4. Connected components",
            "5. Maze solving",
            "6. Tree/graph traversal",
            "7. Puzzle solving (e.g., Sudoku)",
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
        description="Depth-first search algorithm with recursive and iterative approaches"
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
        choices=["recursive", "iterative", "both"],
        default="both",
        help="DFS method to use (default: both)",
    )
    parser.add_argument(
        "-s",
        "--start",
        help="Starting vertex for DFS",
    )
    parser.add_argument(
        "-t",
        "--target",
        help="Target vertex for path finding",
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
        dfs = DFS(config_path=args.config)

        if args.demo:
            # Run demonstration
            print("\n=== Depth-First Search Demonstration ===\n")

            # Example 1: Simple graph
            print("Example 1: Simple Graph")
            graph1 = Graph(directed=False)
            graph1.add_edge(0, 1)
            graph1.add_edge(0, 2)
            graph1.add_edge(1, 3)
            graph1.add_edge(2, 4)

            if args.visualize:
                print("\n" + graph1.visualize())

            if args.method in ["recursive", "both"]:
                path = dfs.dfs_recursive(graph1, 0)
                print(f"\nRecursive DFS from 0: {path}")

            if args.method in ["iterative", "both"]:
                path = dfs.dfs_iterative(graph1, 0)
                print(f"Iterative DFS from 0: {path}")

            if args.method == "both":
                comparison = dfs.compare_methods(graph1, 0)
                print(f"\nRecursive time: {comparison['recursive']['execution_time']:.10f}s")
                print(f"Iterative time: {comparison['iterative']['execution_time']:.10f}s")
                print(f"Paths match: {comparison['paths_match']}")

            # Example 2: More complex graph
            print("\n\nExample 2: Complex Graph")
            graph2 = Graph(directed=False)
            graph2.add_edge("A", "B")
            graph2.add_edge("A", "C")
            graph2.add_edge("B", "D")
            graph2.add_edge("B", "E")
            graph2.add_edge("C", "F")
            graph2.add_edge("D", "G")

            if args.visualize:
                print("\n" + graph2.visualize())

            if args.method in ["recursive", "both"]:
                path = dfs.dfs_recursive(graph2, "A")
                print(f"\nRecursive DFS from A: {path}")

            if args.method in ["iterative", "both"]:
                path = dfs.dfs_iterative(graph2, "A")
                print(f"Iterative DFS from A: {path}")

            # Example 3: Path finding
            if args.target:
                print(f"\n\nExample 3: Path Finding (A -> {args.target})")
                path = dfs.find_path(graph2, "A", args.target, method=args.method)
                if path:
                    print(f"Path: {' -> '.join(str(v) for v in path)}")
                else:
                    print("No path found")

            # Example 4: Connected components
            if args.components:
                print("\n\nExample 4: Connected Components")
                graph3 = Graph(directed=False)
                graph3.add_edge(1, 2)
                graph3.add_edge(2, 3)
                graph3.add_edge(4, 5)
                graph3.add_vertex(6)

                components = dfs.dfs_all_components(graph3, method=args.method)
                print(f"Found {len(components)} components:")
                for i, component in enumerate(components, 1):
                    print(f"  Component {i}: {component}")

            if args.report and args.method == "both":
                comparison = dfs.compare_methods(graph1, 0)
                report = dfs.generate_report(
                    graph1, 0, comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

        else:
            print("Use --demo for demonstration")
            print("DFS operations available:")
            print("  - dfs_recursive(graph, start)")
            print("  - dfs_iterative(graph, start)")
            print("  - find_path(graph, start, target)")
            print("  - dfs_all_components(graph)")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
