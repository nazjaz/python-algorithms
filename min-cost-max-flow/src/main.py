"""Min-Cost Max-Flow Algorithm using Successive Shortest Paths and Cycle Canceling.

This module provides functionality to implement min-cost max-flow algorithms using
two different approaches: successive shortest paths and cycle canceling. These
algorithms find the maximum flow with minimum cost in a flow network.
"""

import logging
import logging.handlers
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Edge:
    """Edge in flow network."""

    def __init__(
        self, to: int, capacity: float, cost: float, reverse: Optional["Edge"] = None
    ) -> None:
        """Initialize edge.

        Args:
            to: Destination vertex.
            capacity: Edge capacity.
            cost: Edge cost per unit flow.
            reverse: Reverse edge.
        """
        self.to = to
        self.capacity = capacity
        self.cost = cost
        self.flow = 0.0
        self.reverse = reverse

    def __repr__(self) -> str:
        """String representation."""
        return f"Edge(to={self.to}, cap={self.capacity}, cost={self.cost}, flow={self.flow})"


class FlowNetwork:
    """Flow network for min-cost max-flow algorithms."""

    def __init__(self, num_vertices: int) -> None:
        """Initialize flow network.

        Args:
            num_vertices: Number of vertices in network.
        """
        self.num_vertices = num_vertices
        self.graph: List[List[Edge]] = [[] for _ in range(num_vertices)]
        self.potential: List[float] = [0.0] * num_vertices

    def add_edge(self, from_vertex: int, to_vertex: int, capacity: float, cost: float) -> None:
        """Add edge to network.

        Args:
            from_vertex: Source vertex.
            to_vertex: Destination vertex.
            capacity: Edge capacity.
            cost: Edge cost per unit flow.
        """
        forward = Edge(to_vertex, capacity, cost)
        backward = Edge(from_vertex, 0, -cost, forward)
        forward.reverse = backward

        self.graph[from_vertex].append(forward)
        self.graph[to_vertex].append(backward)

    def get_residual_capacity(self, edge: Edge) -> float:
        """Get residual capacity of edge.

        Args:
            edge: Edge to check.

        Returns:
            Residual capacity.
        """
        return edge.capacity - edge.flow

    def is_residual(self, edge: Edge) -> bool:
        """Check if edge has residual capacity.

        Args:
            edge: Edge to check.

        Returns:
            True if has residual capacity, False otherwise.
        """
        return self.get_residual_capacity(edge) > 0


class MinCostMaxFlow:
    """Min-cost max-flow algorithm implementation."""

    def __init__(self, network: FlowNetwork, config_path: str = "config.yaml") -> None:
        """Initialize min-cost max-flow solver.

        Args:
            network: Flow network.
            config_path: Path to configuration file.
        """
        self.network = network
        self._setup_logging()
        self._load_config(config_path)

    def _setup_logging(self) -> None:
        """Configure logging for min-cost max-flow operations."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        handler = logging.handlers.RotatingFileHandler(
            log_dir / "min_cost_max_flow.log",
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

    def _bellman_ford(
        self, source: int, distances: List[float], parent: List[Optional[int]]
    ) -> bool:
        """Bellman-Ford algorithm for finding shortest paths.

        Args:
            source: Source vertex.
            distances: Distance array to fill.
            parent: Parent array to fill.

        Returns:
            True if negative cycle found, False otherwise.
        """
        n = self.network.num_vertices
        distances[:] = [float("inf")] * n
        parent[:] = [None] * n
        distances[source] = 0.0

        for _ in range(n - 1):
            updated = False
            for u in range(n):
                if distances[u] == float("inf"):
                    continue

                for edge in self.network.graph[u]:
                    if not self.network.is_residual(edge):
                        continue

                    v = edge.to
                    new_dist = distances[u] + edge.cost
                    if new_dist < distances[v]:
                        distances[v] = new_dist
                        parent[v] = u
                        updated = True

            if not updated:
                break

        for u in range(n):
            if distances[u] == float("inf"):
                continue

            for edge in self.network.graph[u]:
                if not self.network.is_residual(edge):
                    continue

                v = edge.to
                if distances[u] + edge.cost < distances[v]:
                    return True

        return False

    def _dijkstra(
        self, source: int, distances: List[float], parent: List[Optional[int]]
    ) -> bool:
        """Dijkstra's algorithm with potentials for finding shortest paths.

        Args:
            source: Source vertex.
            distances: Distance array to fill.
            parent: Parent array to fill.

        Returns:
            True if path found, False otherwise.
        """
        from heapq import heappush, heappop

        n = self.network.num_vertices
        distances[:] = [float("inf")] * n
        parent[:] = [None] * n
        distances[source] = 0.0

        pq: List[Tuple[float, int]] = []
        heappush(pq, (0.0, source))

        while pq:
            dist_u, u = heappop(pq)

            if dist_u > distances[u]:
                continue

            for edge in self.network.graph[u]:
                if not self.network.is_residual(edge):
                    continue

                v = edge.to
                reduced_cost = edge.cost + self.network.potential[u] - self.network.potential[v]
                new_dist = distances[u] + reduced_cost

                if new_dist < distances[v]:
                    distances[v] = new_dist
                    parent[v] = u
                    heappush(pq, (new_dist, v))

        return distances[source] != float("inf")

    def _find_path(
        self, source: int, sink: int, parent: List[Optional[int]]
    ) -> Tuple[float, List[int]]:
        """Find path from source to sink.

        Args:
            source: Source vertex.
            sink: Sink vertex.
            parent: Parent array.

        Returns:
            Tuple of (flow, path).
        """
        if parent[sink] is None:
            return 0.0, []

        path: List[int] = []
        current = sink
        min_flow = float("inf")

        while current is not None:
            path.append(current)
            if parent[current] is not None:
                for edge in self.network.graph[parent[current]]:
                    if edge.to == current and self.network.is_residual(edge):
                        min_flow = min(min_flow, self.network.get_residual_capacity(edge))
                        break
            current = parent[current]

        path.reverse()
        return min_flow, path

    def _augment_path(self, path: List[int], flow: float) -> None:
        """Augment flow along path.

        Args:
            path: Path vertices.
            flow: Flow amount.
        """
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]

            for edge in self.network.graph[u]:
                if edge.to == v:
                    edge.flow += flow
                    if edge.reverse:
                        edge.reverse.flow -= flow
                    break

    def successive_shortest_paths(self, source: int, sink: int) -> Tuple[float, float]:
        """Solve min-cost max-flow using successive shortest paths.

        Args:
            source: Source vertex.
            sink: Sink vertex.

        Returns:
            Tuple of (max_flow, min_cost).
        """
        max_flow = 0.0
        min_cost = 0.0

        distances: List[float] = [0.0] * self.network.num_vertices
        parent: List[Optional[int]] = [None] * self.network.num_vertices

        while True:
            if not self._dijkstra(source, distances, parent):
                break

            for i in range(self.network.num_vertices):
                if distances[i] != float("inf"):
                    self.network.potential[i] += distances[i]

            flow, path = self._find_path(source, sink, parent)
            if flow == 0.0:
                break

            path_cost = 0.0
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                for edge in self.network.graph[u]:
                    if edge.to == v:
                        path_cost += edge.cost
                        break

            self._augment_path(path, flow)
            max_flow += flow
            min_cost += path_cost * flow

        logger.info(f"Successive shortest paths: flow={max_flow}, cost={min_cost}")
        return max_flow, min_cost

    def _find_negative_cycle(
        self, distances: List[float], parent: List[Optional[int]]
    ) -> Optional[List[int]]:
        """Find negative cycle in residual graph.

        Args:
            distances: Distance array.
            parent: Parent array.

        Returns:
            Cycle vertices or None.
        """
        n = self.network.num_vertices
        cycle_start = None

        for u in range(n):
            if distances[u] == float("inf"):
                continue

            for edge in self.network.graph[u]:
                if not self.network.is_residual(edge):
                    continue

                v = edge.to
                if distances[u] + edge.cost < distances[v]:
                    cycle_start = v
                    break

            if cycle_start is not None:
                break

        if cycle_start is None:
            return None

        visited: List[bool] = [False] * n
        cycle: List[int] = []
        current = cycle_start

        while not visited[current]:
            visited[current] = True
            cycle.append(current)
            if parent[current] is not None:
                current = parent[current]
            else:
                return None

            if current == cycle_start:
                cycle.append(cycle_start)
                idx = cycle.index(cycle_start)
                return cycle[idx:]

        return None

    def cycle_canceling(self, source: int, sink: int) -> Tuple[float, float]:
        """Solve min-cost max-flow using cycle canceling.

        Args:
            source: Source vertex.
            sink: Sink vertex.

        Returns:
            Tuple of (max_flow, min_cost).
        """
        max_flow = 0.0

        distances: List[float] = [0.0] * self.network.num_vertices
        parent: List[Optional[int]] = [None] * self.network.num_vertices

        while True:
            if not self._bellman_ford(source, distances, parent):
                break

            flow, path = self._find_path(source, sink, parent)
            if flow == 0.0:
                break

            self._augment_path(path, flow)
            max_flow += flow

        while True:
            if self._bellman_ford(source, distances, parent):
                cycle = self._find_negative_cycle(distances, parent)
                if cycle is None:
                    break

                min_flow = float("inf")
                for i in range(len(cycle) - 1):
                    u = cycle[i]
                    v = cycle[i + 1]
                    for edge in self.network.graph[u]:
                        if edge.to == v and self.network.is_residual(edge):
                            min_flow = min(min_flow, self.network.get_residual_capacity(edge))
                            break

                if min_flow > 0:
                    self._augment_path(cycle, min_flow)
            else:
                break

        total_cost = 0.0
        for u in range(self.network.num_vertices):
            for edge in self.network.graph[u]:
                if edge.flow > 0 and edge.capacity > 0:
                    total_cost += edge.cost * edge.flow

        logger.info(f"Cycle canceling: flow={max_flow}, cost={total_cost}")
        return max_flow, total_cost

    def get_flow(self) -> Dict[Tuple[int, int], float]:
        """Get flow on each edge.

        Returns:
            Dictionary mapping (from, to) to flow.
        """
        flow_dict: Dict[Tuple[int, int], float] = {}
        for u in range(self.network.num_vertices):
            for edge in self.network.graph[u]:
                if edge.capacity > 0 and edge.flow > 0:
                    flow_dict[(u, edge.to)] = edge.flow
        return flow_dict


def main() -> None:
    """Main function to demonstrate min-cost max-flow algorithms."""
    print("Min-Cost Max-Flow Algorithms Demo")
    print("=" * 50)

    network = FlowNetwork(4)
    network.add_edge(0, 1, 10, 1)
    network.add_edge(0, 2, 5, 2)
    network.add_edge(1, 2, 15, 1)
    network.add_edge(1, 3, 10, 3)
    network.add_edge(2, 3, 10, 1)

    print("\n=== Successive Shortest Paths ===")
    solver1 = MinCostMaxFlow(network)
    flow1, cost1 = solver1.successive_shortest_paths(0, 3)
    print(f"Max Flow: {flow1}")
    print(f"Min Cost: {cost1}")

    print("\n=== Cycle Canceling ===")
    network2 = FlowNetwork(4)
    network2.add_edge(0, 1, 10, 1)
    network2.add_edge(0, 2, 5, 2)
    network2.add_edge(1, 2, 15, 1)
    network2.add_edge(1, 3, 10, 3)
    network2.add_edge(2, 3, 10, 1)

    solver2 = MinCostMaxFlow(network2)
    flow2, cost2 = solver2.cycle_canceling(0, 3)
    print(f"Max Flow: {flow2}")
    print(f"Min Cost: {cost2}")


if __name__ == "__main__":
    main()
