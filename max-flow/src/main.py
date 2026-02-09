"""Maximum Flow Algorithm Using Ford-Fulkerson Method.

This module provides functionality to compute maximum flow in a flow network
using Ford-Fulkerson method with Edmonds-Karp and Dinic's optimizations.
Ford-Fulkerson finds the maximum flow from source to sink in a directed graph
with edge capacities.
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


class FlowNetwork:
    """Flow network representation for maximum flow algorithms."""

    def __init__(self, num_vertices: int) -> None:
        """Initialize flow network.

        Args:
            num_vertices: Number of vertices in the graph.
        """
        if num_vertices < 2:
            raise ValueError("Network must have at least 2 vertices")
        self.num_vertices = num_vertices
        self.graph: List[Dict[int, int]] = [
            {} for _ in range(num_vertices)
        ]
        self.residual: List[Dict[int, int]] = [
            {} for _ in range(num_vertices)
        ]
        logger.info(f"Flow network initialized with {num_vertices} vertices")

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        """Add edge with capacity to network.

        Args:
            u: Source vertex.
            v: Destination vertex.
            capacity: Edge capacity.
        """
        if u < 0 or u >= self.num_vertices:
            raise ValueError(f"Invalid source vertex: {u}")
        if v < 0 or v >= self.num_vertices:
            raise ValueError(f"Invalid destination vertex: {v}")
        if capacity < 0:
            raise ValueError("Capacity must be non-negative")

        self.graph[u][v] = capacity
        if v not in self.residual[u]:
            self.residual[u][v] = 0
        if u not in self.residual[v]:
            self.residual[v][u] = 0
        self.residual[u][v] = capacity
        logger.debug(f"Added edge ({u}, {v}) with capacity {capacity}")

    def get_capacity(self, u: int, v: int) -> int:
        """Get capacity of edge.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Returns:
            Edge capacity, 0 if edge doesn't exist.
        """
        return self.graph[u].get(v, 0)

    def get_residual_capacity(self, u: int, v: int) -> int:
        """Get residual capacity of edge.

        Args:
            u: Source vertex.
            v: Destination vertex.

        Returns:
            Residual capacity, 0 if edge doesn't exist.
        """
        return self.residual[u].get(v, 0)

    def update_residual(self, u: int, v: int, flow: int) -> None:
        """Update residual capacities after sending flow.

        Args:
            u: Source vertex.
            v: Destination vertex.
            flow: Flow amount to send.
        """
        self.residual[u][v] = self.residual[u].get(v, 0) - flow
        self.residual[v][u] = self.residual[v].get(u, 0) + flow

        if self.residual[u][v] == 0:
            self.residual[u].pop(v, None)
        if self.residual[v][u] == 0:
            self.residual[v].pop(u, None)


class MaxFlowSolver:
    """Maximum flow solver with multiple algorithms."""

    def __init__(self, network: FlowNetwork) -> None:
        """Initialize max flow solver.

        Args:
            network: Flow network to solve.
        """
        self.network = network
        logger.info("Max flow solver initialized")

    def ford_fulkerson(
        self, source: int, sink: int
    ) -> Tuple[int, Dict[Tuple[int, int], int]]:
        """Compute maximum flow using Ford-Fulkerson algorithm.

        Uses DFS to find augmenting paths. Time complexity: O(E * max_flow)
        where E is number of edges.

        Args:
            source: Source vertex.
            sink: Sink vertex.

        Returns:
            Tuple of (max_flow, flow_dict) where flow_dict maps (u, v) to flow.
        """
        if source < 0 or source >= self.network.num_vertices:
            raise ValueError(f"Invalid source vertex: {source}")
        if sink < 0 or sink >= self.network.num_vertices:
            raise ValueError(f"Invalid sink vertex: {sink}")
        if source == sink:
            raise ValueError("Source and sink must be different")

        logger.info(
            f"Computing max flow using Ford-Fulkerson: "
            f"source={source}, sink={sink}"
        )

        self._reset_residual()
        max_flow = 0
        parent = [-1] * self.network.num_vertices

        while self._dfs_path(source, sink, parent):
            path_flow = float("inf")
            v = sink

            while v != source:
                u = parent[v]
                path_flow = min(
                    path_flow,
                    self.network.get_residual_capacity(u, v),
                )
                v = u

            max_flow += path_flow
            v = sink

            while v != source:
                u = parent[v]
                self.network.update_residual(u, v, path_flow)
                v = u

            parent = [-1] * self.network.num_vertices

        flow_dict = self._compute_flow_dict(source, sink)
        logger.info(f"Ford-Fulkerson max flow: {max_flow}")
        return max_flow, flow_dict

    def edmonds_karp(
        self, source: int, sink: int
    ) -> Tuple[int, Dict[Tuple[int, int], int]]:
        """Compute maximum flow using Edmonds-Karp algorithm.

        Uses BFS to find shortest augmenting paths. Time complexity: O(V * E^2)
        where V is vertices and E is edges.

        Args:
            source: Source vertex.
            sink: Sink vertex.

        Returns:
            Tuple of (max_flow, flow_dict) where flow_dict maps (u, v) to flow.
        """
        if source < 0 or source >= self.network.num_vertices:
            raise ValueError(f"Invalid source vertex: {source}")
        if sink < 0 or sink >= self.network.num_vertices:
            raise ValueError(f"Invalid sink vertex: {sink}")
        if source == sink:
            raise ValueError("Source and sink must be different")

        logger.info(
            f"Computing max flow using Edmonds-Karp: "
            f"source={source}, sink={sink}"
        )

        self._reset_residual()
        max_flow = 0
        parent = [-1] * self.network.num_vertices

        while self._bfs_path(source, sink, parent):
            path_flow = float("inf")
            v = sink

            while v != source:
                u = parent[v]
                path_flow = min(
                    path_flow,
                    self.network.get_residual_capacity(u, v),
                )
                v = u

            max_flow += path_flow
            v = sink

            while v != source:
                u = parent[v]
                self.network.update_residual(u, v, path_flow)
                v = u

            parent = [-1] * self.network.num_vertices

        flow_dict = self._compute_flow_dict(source, sink)
        logger.info(f"Edmonds-Karp max flow: {max_flow}")
        return max_flow, flow_dict

    def dinic(
        self, source: int, sink: int
    ) -> Tuple[int, Dict[Tuple[int, int], int]]:
        """Compute maximum flow using Dinic's algorithm.

        Uses layered network and blocking flow. Time complexity: O(V^2 * E)
        where V is vertices and E is edges.

        Args:
            source: Source vertex.
            sink: Sink vertex.

        Returns:
            Tuple of (max_flow, flow_dict) where flow_dict maps (u, v) to flow.
        """
        if source < 0 or source >= self.network.num_vertices:
            raise ValueError(f"Invalid source vertex: {source}")
        if sink < 0 or sink >= self.network.num_vertices:
            raise ValueError(f"Invalid sink vertex: {sink}")
        if source == sink:
            raise ValueError("Source and sink must be different")

        logger.info(
            f"Computing max flow using Dinic's: source={source}, sink={sink}"
        )

        self._reset_residual()
        max_flow = 0
        level = [-1] * self.network.num_vertices

        while self._build_layered_network(source, sink, level):
            while True:
                flow = self._send_blocking_flow(
                    source, sink, level, float("inf")
                )
                if flow == 0:
                    break
                max_flow += flow

            level = [-1] * self.network.num_vertices

        flow_dict = self._compute_flow_dict(source, sink)
        logger.info(f"Dinic's max flow: {max_flow}")
        return max_flow, flow_dict

    def _reset_residual(self) -> None:
        """Reset residual graph to original capacities."""
        for u in range(self.network.num_vertices):
            self.network.residual[u].clear()
            for v, capacity in self.network.graph[u].items():
                self.network.residual[u][v] = capacity
                if u not in self.network.residual[v]:
                    self.network.residual[v][u] = 0

    def _dfs_path(
        self, source: int, sink: int, parent: List[int]
    ) -> bool:
        """Find augmenting path using DFS.

        Args:
            source: Source vertex.
            sink: Sink vertex.
            parent: Parent array to store path.

        Returns:
            True if path found, False otherwise.
        """
        visited = [False] * self.network.num_vertices
        stack = [source]
        visited[source] = True

        while stack:
            u = stack.pop()

            for v in list(self.network.residual[u].keys()):
                if (
                    not visited[v]
                    and self.network.get_residual_capacity(u, v) > 0
                ):
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
                    stack.append(v)

        return False

    def _bfs_path(
        self, source: int, sink: int, parent: List[int]
    ) -> bool:
        """Find augmenting path using BFS.

        Args:
            source: Source vertex.
            sink: Sink vertex.
            parent: Parent array to store path.

        Returns:
            True if path found, False otherwise.
        """
        visited = [False] * self.network.num_vertices
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()

            for v in list(self.network.residual[u].keys()):
                if (
                    not visited[v]
                    and self.network.get_residual_capacity(u, v) > 0
                ):
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)

        return False

    def _build_layered_network(
        self, source: int, sink: int, level: List[int]
    ) -> bool:
        """Build layered network using BFS.

        Args:
            source: Source vertex.
            sink: Sink vertex.
            level: Level array to store distances.

        Returns:
            True if sink is reachable, False otherwise.
        """
        for i in range(self.network.num_vertices):
            level[i] = -1

        queue = deque([source])
        level[source] = 0

        while queue:
            u = queue.popleft()

            for v in list(self.network.residual[u].keys()):
                if (
                    level[v] == -1
                    and self.network.get_residual_capacity(u, v) > 0
                ):
                    level[v] = level[u] + 1
                    queue.append(v)

        return level[sink] != -1

    def _send_blocking_flow(
        self, u: int, sink: int, level: List[int], flow: int
    ) -> int:
        """Send blocking flow using DFS in layered network.

        Args:
            u: Current vertex.
            sink: Sink vertex.
            level: Level array.
            flow: Current flow.

        Returns:
            Flow sent.
        """
        if u == sink:
            return flow

        for v in list(self.network.residual[u].keys()):
            if (
                level[v] == level[u] + 1
                and self.network.get_residual_capacity(u, v) > 0
            ):
                current_flow = min(
                    flow, self.network.get_residual_capacity(u, v)
                )
                temp_flow = self._send_blocking_flow(
                    v, sink, level, current_flow
                )

                if temp_flow > 0:
                    self.network.update_residual(u, v, temp_flow)
                    return temp_flow

        return 0

    def _compute_flow_dict(
        self, source: int, sink: int
    ) -> Dict[Tuple[int, int], int]:
        """Compute flow dictionary from residual graph.

        Args:
            source: Source vertex.
            sink: Sink vertex.

        Returns:
            Dictionary mapping (u, v) to flow value.
        """
        flow_dict: Dict[Tuple[int, int], int] = {}

        for u in range(self.network.num_vertices):
            for v in self.network.graph[u]:
                original_capacity = self.network.graph[u][v]
                residual_capacity = self.network.get_residual_capacity(u, v)
                flow = original_capacity - residual_capacity
                if flow > 0:
                    flow_dict[(u, v)] = flow

        return flow_dict

    def get_min_cut(
        self, source: int, sink: int, algorithm: str = "edmonds_karp"
    ) -> Tuple[List[int], List[int]]:
        """Find minimum cut (source side and sink side).

        Args:
            source: Source vertex.
            sink: Sink vertex.
            algorithm: Algorithm to use ("ford_fulkerson", "edmonds_karp", "dinic").

        Returns:
            Tuple of (source_side, sink_side) vertex lists.
        """
        if algorithm == "ford_fulkerson":
            self.ford_fulkerson(source, sink)
        elif algorithm == "edmonds_karp":
            self.edmonds_karp(source, sink)
        elif algorithm == "dinic":
            self.dinic(source, sink)
        else:
            raise ValueError(
                f"Unknown algorithm: {algorithm}. "
                "Use 'ford_fulkerson', 'edmonds_karp', or 'dinic'"
            )

        visited = [False] * self.network.num_vertices
        queue = deque([source])
        visited[source] = True

        while queue:
            u = queue.popleft()
            for v in list(self.network.residual[u].keys()):
                if (
                    not visited[v]
                    and self.network.get_residual_capacity(u, v) > 0
                ):
                    visited[v] = True
                    queue.append(v)

        source_side = [i for i in range(self.network.num_vertices) if visited[i]]
        sink_side = [
            i for i in range(self.network.num_vertices) if not visited[i]
        ]

        return source_side, sink_side


def main() -> None:
    """Main function to demonstrate maximum flow algorithms."""
    network = FlowNetwork(6)

    network.add_edge(0, 1, 16)
    network.add_edge(0, 2, 13)
    network.add_edge(1, 2, 10)
    network.add_edge(1, 3, 12)
    network.add_edge(2, 1, 4)
    network.add_edge(2, 4, 14)
    network.add_edge(3, 2, 9)
    network.add_edge(3, 5, 20)
    network.add_edge(4, 3, 7)
    network.add_edge(4, 5, 4)

    solver = MaxFlowSolver(network)
    source = 0
    sink = 5

    logger.info("Computing maximum flow using different algorithms:")

    max_flow_ff, flow_dict_ff = solver.ford_fulkerson(source, sink)
    logger.info(f"Ford-Fulkerson: {max_flow_ff}")

    max_flow_ek, flow_dict_ek = solver.edmonds_karp(source, sink)
    logger.info(f"Edmonds-Karp: {max_flow_ek}")

    max_flow_dinic, flow_dict_dinic = solver.dinic(source, sink)
    logger.info(f"Dinic's: {max_flow_dinic}")

    source_side, sink_side = solver.get_min_cut(source, sink)
    logger.info(f"Min cut - Source side: {source_side}, Sink side: {sink_side}")


if __name__ == "__main__":
    main()
