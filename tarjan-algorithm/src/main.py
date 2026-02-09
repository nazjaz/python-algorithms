"""Tarjan's Algorithm for Finding Strongly Connected Components and Articulation Points.

This module provides functionality to implement Tarjan's algorithm that finds
strongly connected components (SCCs) and articulation points in directed and
undirected graphs. Tarjan's algorithm achieves O(V + E) time complexity using
depth-first search with low-link values.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import List, Set

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Graph:
    """Graph representation for Tarjan's algorithm."""

    def __init__(self, num_vertices: int, directed: bool = True) -> None:
        """Initialize graph.

        Args:
            num_vertices: Number of vertices.
            directed: True for directed graph, False for undirected.
        """
        self.num_vertices = num_vertices
        self.directed = directed
        self.adjacency_list: List[List[int]] = [[] for _ in range(num_vertices)]

    def add_edge(self, u: int, v: int) -> None:
        """Add edge to graph.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Raises:
            ValueError: If vertices are invalid.
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise ValueError(f"Invalid vertices: {u}, {v}")

        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)

        if not self.directed and u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)

        logger.info(f"Added edge ({u}, {v})")


class TarjanAlgorithm:
    """Tarjan's algorithm for SCCs and articulation points."""

    def __init__(self, graph: Graph, config_path: str = "config.yaml") -> None:
        """Initialize Tarjan's algorithm.

        Args:
            graph: Graph to analyze.
            config_path: Path to configuration file.
        """
        self.graph = graph
        self.disc: List[int] = [-1] * graph.num_vertices
        self.low: List[int] = [-1] * graph.num_vertices
        self.stack: List[int] = []
        self.in_stack: List[bool] = [False] * graph.num_vertices
        self.time = 0
        self.sccs: List[List[int]] = []
        self.articulation_points: Set[int] = set()
        self.parent: List[int] = [-1] * graph.num_vertices
        self.children: List[int] = [0] * graph.num_vertices
        self._setup_logging()
        self._load_config(config_path)
        logger.info(f"Initialized Tarjan's algorithm for {graph.num_vertices} vertices")

    def _setup_logging(self) -> None:
        """Configure logging for Tarjan's algorithm operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "tarjan_algorithm.log",
            maxBytes=10485760,
            backupCount=5,
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def _load_config(self, config_path: str) -> None:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.
        """
        try:
            config_file = Path(config_path)
            if config_file.exists():
                with open(config_file, "r") as f:
                    config = yaml.safe_load(f)
                    if config and "logging" in config:
                        log_level = config["logging"].get("level", "INFO")
                        logger.setLevel(getattr(logging, log_level))
        except Exception as e:
            logger.warning(f"Could not load config: {e}")

    def _scc_dfs(self, u: int) -> None:
        """DFS for finding strongly connected components.

        Args:
            u: Current vertex.
        """
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        self.stack.append(u)
        self.in_stack[u] = True

        for v in self.graph.adjacency_list[u]:
            if self.disc[v] == -1:
                self._scc_dfs(v)
                self.low[u] = min(self.low[u], self.low[v])
            elif self.in_stack[v]:
                self.low[u] = min(self.low[u], self.disc[v])

        if self.low[u] == self.disc[u]:
            scc: List[int] = []
            while True:
                v = self.stack.pop()
                self.in_stack[v] = False
                scc.append(v)
                if v == u:
                    break
            self.sccs.append(scc)

    def find_strongly_connected_components(self) -> List[List[int]]:
        """Find strongly connected components in directed graph.

        Returns:
            List of strongly connected components.

        Raises:
            ValueError: If graph is undirected.
        """
        if not self.graph.directed:
            raise ValueError("Strongly connected components require directed graph")

        self.disc = [-1] * self.graph.num_vertices
        self.low = [-1] * self.graph.num_vertices
        self.stack = []
        self.in_stack = [False] * self.graph.num_vertices
        self.time = 0
        self.sccs = []

        for i in range(self.graph.num_vertices):
            if self.disc[i] == -1:
                self._scc_dfs(i)

        logger.info(f"Found {len(self.sccs)} strongly connected components")
        return self.sccs

    def _articulation_dfs(self, u: int) -> None:
        """DFS for finding articulation points.

        Args:
            u: Current vertex.
        """
        self.disc[u] = self.time
        self.low[u] = self.time
        self.time += 1
        children_count = 0

        for v in self.graph.adjacency_list[u]:
            if self.disc[v] == -1:
                self.parent[v] = u
                children_count += 1
                self._articulation_dfs(v)

                self.low[u] = min(self.low[u], self.low[v])

                if self.parent[u] == -1 and children_count > 1:
                    self.articulation_points.add(u)
                if self.parent[u] != -1 and self.low[v] >= self.disc[u]:
                    self.articulation_points.add(u)
            elif v != self.parent[u]:
                self.low[u] = min(self.low[u], self.disc[v])

    def find_articulation_points(self) -> Set[int]:
        """Find articulation points in undirected graph.

        Returns:
            Set of articulation point vertices.

        Raises:
            ValueError: If graph is directed.
        """
        if self.graph.directed:
            raise ValueError("Articulation points require undirected graph")

        self.disc = [-1] * self.graph.num_vertices
        self.low = [-1] * self.graph.num_vertices
        self.parent = [-1] * self.graph.num_vertices
        self.children = [0] * self.graph.num_vertices
        self.time = 0
        self.articulation_points = set()

        for i in range(self.graph.num_vertices):
            if self.disc[i] == -1:
                self._articulation_dfs(i)

        logger.info(f"Found {len(self.articulation_points)} articulation points")
        return self.articulation_points

    def get_scc_count(self) -> int:
        """Get number of strongly connected components.

        Returns:
            Number of SCCs.
        """
        return len(self.sccs)

    def get_articulation_point_count(self) -> int:
        """Get number of articulation points.

        Returns:
            Number of articulation points.
        """
        return len(self.articulation_points)


def main() -> None:
    """Main function to demonstrate Tarjan's algorithm."""
    print("Tarjan's Algorithm Demo")
    print("=" * 50)

    print("\n=== Strongly Connected Components ===")
    graph1 = Graph(5, directed=True)
    graph1.add_edge(0, 1)
    graph1.add_edge(1, 2)
    graph1.add_edge(2, 0)
    graph1.add_edge(1, 3)
    graph1.add_edge(3, 4)

    tarjan1 = TarjanAlgorithm(graph1)
    sccs = tarjan1.find_strongly_connected_components()
    print(f"Number of SCCs: {tarjan1.get_scc_count()}")
    for i, scc in enumerate(sccs):
        print(f"SCC {i}: {scc}")

    print("\n=== Articulation Points ===")
    graph2 = Graph(5, directed=False)
    graph2.add_edge(0, 1)
    graph2.add_edge(1, 2)
    graph2.add_edge(2, 0)
    graph2.add_edge(1, 3)
    graph2.add_edge(3, 4)

    tarjan2 = TarjanAlgorithm(graph2)
    articulation_points = tarjan2.find_articulation_points()
    print(f"Number of articulation points: {tarjan2.get_articulation_point_count()}")
    print(f"Articulation points: {sorted(articulation_points)}")


if __name__ == "__main__":
    main()
