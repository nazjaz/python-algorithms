"""Blossom Algorithm for Finding Maximum Matching in General Graphs.

This module provides functionality to implement the blossom algorithm (Edmonds'
algorithm) that finds maximum matching in general graphs. The algorithm handles
odd cycles (blossoms) by contracting them and then expanding after finding
augmenting paths.
"""

import logging
import logging.handlers
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BlossomAlgorithm:
    """Blossom algorithm for maximum matching in general graphs."""

    def __init__(self, num_vertices: int, config_path: str = "config.yaml") -> None:
        """Initialize blossom algorithm.

        Args:
            num_vertices: Number of vertices in graph.
            config_path: Path to configuration file.
        """
        self.num_vertices = num_vertices
        self.graph: List[List[int]] = [[] for _ in range(num_vertices)]
        self.matching: List[Optional[int]] = [None] * num_vertices
        self.parent: List[Optional[int]] = [None] * num_vertices
        self.base: List[int] = list(range(num_vertices))
        self.in_queue: List[bool] = [False] * num_vertices
        self.in_blossom: List[int] = list(range(num_vertices))
        self._setup_logging()
        self._load_config(config_path)
        logger.info(f"Initialized blossom algorithm for {num_vertices} vertices")

    def _setup_logging(self) -> None:
        """Configure logging for blossom algorithm operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "blossom_algorithm.log",
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

    def add_edge(self, u: int, v: int) -> None:
        """Add undirected edge to graph.

        Args:
            u: First vertex.
            v: Second vertex.

        Raises:
            ValueError: If vertices are invalid.
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise ValueError(f"Invalid vertices: {u}, {v}")

        if u == v:
            return

        if v not in self.graph[u]:
            self.graph[u].append(v)
        if u not in self.graph[v]:
            self.graph[v].append(u)

        logger.info(f"Added edge ({u}, {v})")

    def _lca(self, u: int, v: int) -> int:
        """Find lowest common ancestor in alternating tree.

        Args:
            u: First vertex.
            v: Second vertex.

        Returns:
            Lowest common ancestor.
        """
        used: Set[int] = set()
        while True:
            u = self.base[u]
            used.add(u)
            if self.matching[u] is None:
                break
            u = self.parent[self.matching[u]]

        while True:
            v = self.base[v]
            if v in used:
                return v
            v = self.parent[self.matching[v]]

    def _mark_path(self, v: int, b: int, children: List[int]) -> None:
        """Mark path in blossom.

        Args:
            v: Current vertex.
            b: Base vertex.
            children: Children list.
        """
        while self.base[v] != b:
            u = self.matching[v]
            children.append(u)
            self.in_blossom[self.base[u]] = True
            self.in_blossom[self.base[v]] = True
            v = self.parent[u]
            if self.base[v] != b:
                children.append(v)

    def _contract_blossom(self, u: int, v: int) -> None:
        """Contract blossom (odd cycle).

        Args:
            u: First vertex in cycle.
            v: Second vertex in cycle.
        """
        b = self._lca(u, v)
        blossom: List[int] = []
        self._mark_path(u, b, blossom)
        self._mark_path(v, b, blossom)

        for i in range(self.num_vertices):
            if self.in_blossom[self.base[i]]:
                self.base[i] = b
                if not self.in_queue[i]:
                    self.in_queue[i] = True

    def _find_augmenting_path(self, root: int) -> bool:
        """Find augmenting path from root.

        Args:
            root: Root vertex.

        Returns:
            True if augmenting path found, False otherwise.
        """
        for i in range(self.num_vertices):
            self.parent[i] = None
            self.in_queue[i] = False
            self.base[i] = i
            self.in_blossom[i] = False

        queue: deque = deque()
        queue.append(root)
        self.in_queue[root] = True
        self.parent[root] = None

        while queue:
            u = queue.popleft()

            for v in self.graph[u]:
                if self.base[u] == self.base[v] or self.matching[u] == v:
                    continue

                if v == root or (
                    self.matching[v] is not None and self.parent[self.matching[v]] is not None
                ):
                    blossom_base = self._lca(u, v)
                    self._contract_blossom(u, v)
                elif self.parent[v] is None:
                    self.parent[v] = u
                    if self.matching[v] is None:
                        return True
                    matched_v = self.matching[v]
                    self.in_queue[matched_v] = True
                    queue.append(matched_v)

        return False

    def _augment_path(self, v: int) -> None:
        """Augment matching along path.

        Args:
            v: End vertex of augmenting path.
        """
        while v is not None:
            u = self.parent[v]
            w = self.matching[u]
            self.matching[v] = u
            self.matching[u] = v
            v = w

    def find_maximum_matching(self) -> Dict[int, int]:
        """Find maximum matching in graph.

        Returns:
            Dictionary mapping vertex to its matched vertex.
        """
        for i in range(self.num_vertices):
            if self.matching[i] is None:
                if self._find_augmenting_path(i):
                    self._augment_path(i)

        matching_dict: Dict[int, int] = {}
        for i in range(self.num_vertices):
            if self.matching[i] is not None and i < self.matching[i]:
                matching_dict[i] = self.matching[i]

        matching_size = len(matching_dict)
        logger.info(f"Found maximum matching of size {matching_size}")
        return matching_dict

    def get_matching_size(self) -> int:
        """Get size of current matching.

        Returns:
            Number of edges in matching.
        """
        count = 0
        for i in range(self.num_vertices):
            if self.matching[i] is not None and i < self.matching[i]:
                count += 1
        return count

    def is_matched(self, vertex: int) -> bool:
        """Check if vertex is matched.

        Args:
            vertex: Vertex to check.

        Returns:
            True if matched, False otherwise.

        Raises:
            ValueError: If vertex is invalid.
        """
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Invalid vertex: {vertex}")

        return self.matching[vertex] is not None

    def get_matched_vertex(self, vertex: int) -> Optional[int]:
        """Get vertex matched to given vertex.

        Args:
            vertex: Vertex to check.

        Returns:
            Matched vertex or None.

        Raises:
            ValueError: If vertex is invalid.
        """
        if vertex < 0 or vertex >= self.num_vertices:
            raise ValueError(f"Invalid vertex: {vertex}")

        return self.matching[vertex]


def main() -> None:
    """Main function to demonstrate blossom algorithm."""
    print("Blossom Algorithm for Maximum Matching Demo")
    print("=" * 50)

    blossom = BlossomAlgorithm(6)

    print("\nAdding edges:")
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (1, 3)]
    for u, v in edges:
        blossom.add_edge(u, v)
        print(f"Edge ({u}, {v})")

    print("\nFinding maximum matching:")
    matching = blossom.find_maximum_matching()

    print(f"\nMatching size: {blossom.get_matching_size()}")
    print("Matching edges:")
    for u, v in matching.items():
        print(f"  ({u}, {v})")

    print("\nVertex matching status:")
    for i in range(6):
        matched = blossom.is_matched(i)
        match_vertex = blossom.get_matched_vertex(i)
        print(f"  Vertex {i}: {'matched' if matched else 'unmatched'}", end="")
        if match_vertex is not None:
            print(f" to {match_vertex}")
        else:
            print()


if __name__ == "__main__":
    main()
