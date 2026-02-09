"""Prim's Algorithm for Minimum Spanning Tree.

This module provides functionality to find minimum spanning tree (MST)
in weighted graphs using Prim's algorithm with different data structure
choices: list-based and binary heap implementations.
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


class MinHeap:
    """Min-heap implementation for priority queue in Prim's algorithm."""

    def __init__(self) -> None:
        """Initialize MinHeap."""
        self.heap: List[Tuple[float, int]] = []

    def _parent(self, index: int) -> int:
        """Get parent index."""
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get left child index."""
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get right child index."""
        return 2 * index + 2

    def _swap(self, i: int, j: int) -> None:
        """Swap elements at indices i and j."""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index: int) -> None:
        """Heapify up from given index."""
        while index > 0:
            parent = self._parent(index)
            if self.heap[parent][0] <= self.heap[index][0]:
                break
            self._swap(parent, index)
            index = parent

    def _heapify_down(self, index: int) -> None:
        """Heapify down from given index."""
        while True:
            smallest = index
            left = self._left_child(index)
            right = self._right_child(index)

            if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right

            if smallest == index:
                break

            self._swap(index, smallest)
            index = smallest

    def insert(self, weight: float, vertex: int) -> None:
        """Insert element into heap."""
        self.heap.append((weight, vertex))
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self) -> Optional[Tuple[float, int]]:
        """Extract and return minimum element."""
        if not self.heap:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        min_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return min_item

    def is_empty(self) -> bool:
        """Check if heap is empty."""
        return len(self.heap) == 0

    def decrease_key(self, vertex: int, new_weight: float) -> None:
        """Decrease key for given vertex."""
        for i, (weight, v) in enumerate(self.heap):
            if v == vertex:
                if new_weight < weight:
                    self.heap[i] = (new_weight, vertex)
                    self._heapify_up(i)
                break


class PrimMST:
    """Prim's algorithm for finding minimum spanning tree."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize PrimMST with configuration.

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

    def _build_adjacency_list(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
    ) -> Dict[int, List[Tuple[int, float]]]:
        """Build adjacency list representation of graph.

        Args:
            num_vertices: Number of vertices.
            edges: List of edges as (source, destination, weight) tuples.

        Returns:
            Adjacency list dictionary.
        """
        adjacency_list: Dict[int, List[Tuple[int, float]]] = {
            i: [] for i in range(num_vertices)
        }

        for source, dest, weight in edges:
            adjacency_list[source].append((dest, weight))
            adjacency_list[dest].append((source, weight))

        return adjacency_list

    def _validate_edge(
        self, edge: Tuple[int, int, float], num_vertices: int
    ) -> None:
        """Validate edge.

        Args:
            edge: Edge tuple (source, destination, weight).
            num_vertices: Number of vertices in graph.

        Raises:
            ValueError: If edge is invalid.
        """
        source, dest, weight = edge
        if source < 0 or source >= num_vertices:
            raise ValueError(
                f"Source vertex {source} out of range [0, {num_vertices - 1}]"
            )
        if dest < 0 or dest >= num_vertices:
            raise ValueError(
                f"Destination vertex {dest} out of range [0, {num_vertices - 1}]"
            )
        if source == dest:
            raise ValueError("Self-loops are not allowed in MST")
        if not isinstance(weight, (int, float)):
            raise ValueError(f"Weight must be numeric, got {type(weight)}")

    def find_mst_list(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
    ) -> Tuple[List[Tuple[int, int, float]], float]:
        """Find MST using Prim's algorithm with list-based approach.

        Uses simple list to find minimum edge, resulting in O(V²) time
        complexity. Suitable for dense graphs.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).

        Returns:
            Tuple containing:
                - List of edges in MST
                - Total weight of MST

        Raises:
            ValueError: If inputs are invalid or graph is disconnected.
        """
        if num_vertices < 0:
            raise ValueError("Number of vertices must be non-negative")

        if num_vertices == 0:
            logger.info("Empty graph: returning empty MST")
            return [], 0.0

        if num_vertices == 1:
            logger.info("Single vertex: returning empty MST")
            return [], 0.0

        if start_vertex < 0 or start_vertex >= num_vertices:
            raise ValueError(f"Start vertex {start_vertex} out of range")

        logger.info(
            f"Prim's algorithm (list-based): {num_vertices} vertices, "
            f"{len(edges)} edges, start={start_vertex}"
        )

        # Validate all edges
        for edge in edges:
            self._validate_edge(edge, num_vertices)

        # Build adjacency list
        adjacency_list = self._build_adjacency_list(num_vertices, edges)

        # Initialize
        in_mst = [False] * num_vertices
        key = [float("inf")] * num_vertices
        parent = [-1] * num_vertices

        key[start_vertex] = 0.0
        mst_edges: List[Tuple[int, int, float]] = []
        total_weight = 0.0

        # Prim's algorithm with list-based approach
        for _ in range(num_vertices):
            # Find vertex with minimum key not in MST
            u = -1
            min_key = float("inf")
            for v in range(num_vertices):
                if not in_mst[v] and key[v] < min_key:
                    min_key = key[v]
                    u = v

            if u == -1:
                raise ValueError("Graph is disconnected")

            in_mst[u] = True

            # Add edge to MST (except for start vertex)
            if parent[u] != -1:
                edge_weight = key[u]
                mst_edges.append((parent[u], u, edge_weight))
                total_weight += edge_weight
                logger.debug(
                    f"  Added edge ({parent[u]}, {u}, {edge_weight}) to MST"
                )

            # Update keys of adjacent vertices
            for neighbor, weight in adjacency_list[u]:
                if not in_mst[neighbor] and weight < key[neighbor]:
                    key[neighbor] = weight
                    parent[neighbor] = u
                    logger.debug(
                        f"    Updated key[{neighbor}] = {weight}, "
                        f"parent = {u}"
                    )

        logger.info(
            f"MST found: {len(mst_edges)} edges, total weight = {total_weight}"
        )

        return mst_edges, total_weight

    def find_mst_heap(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
    ) -> Tuple[List[Tuple[int, int, float]], float]:
        """Find MST using Prim's algorithm with binary heap approach.

        Uses binary min-heap for priority queue, resulting in O(E log V)
        time complexity. Suitable for sparse graphs.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).

        Returns:
            Tuple containing:
                - List of edges in MST
                - Total weight of MST

        Raises:
            ValueError: If inputs are invalid or graph is disconnected.
        """
        if num_vertices < 0:
            raise ValueError("Number of vertices must be non-negative")

        if num_vertices == 0:
            logger.info("Empty graph: returning empty MST")
            return [], 0.0

        if num_vertices == 1:
            logger.info("Single vertex: returning empty MST")
            return [], 0.0

        if start_vertex < 0 or start_vertex >= num_vertices:
            raise ValueError(f"Start vertex {start_vertex} out of range")

        logger.info(
            f"Prim's algorithm (heap-based): {num_vertices} vertices, "
            f"{len(edges)} edges, start={start_vertex}"
        )

        # Validate all edges
        for edge in edges:
            self._validate_edge(edge, num_vertices)

        # Build adjacency list
        adjacency_list = self._build_adjacency_list(num_vertices, edges)

        # Initialize
        in_mst = [False] * num_vertices
        key = [float("inf")] * num_vertices
        parent = [-1] * num_vertices

        key[start_vertex] = 0.0

        # Initialize heap with all vertices
        heap = MinHeap()
        for v in range(num_vertices):
            heap.insert(key[v], v)

        mst_edges: List[Tuple[int, int, float]] = []
        total_weight = 0.0
        vertices_processed = 0

        # Prim's algorithm with heap-based approach
        while not heap.is_empty() and vertices_processed < num_vertices:
            # Extract vertex with minimum key
            min_item = heap.extract_min()
            if min_item is None:
                break

            weight_u, u = min_item

            if in_mst[u]:
                continue

            in_mst[u] = True
            vertices_processed += 1

            # Add edge to MST (except for start vertex)
            if parent[u] != -1:
                edge_weight = key[u]
                mst_edges.append((parent[u], u, edge_weight))
                total_weight += edge_weight
                logger.debug(
                    f"  Added edge ({parent[u]}, {u}, {edge_weight}) to MST"
                )

            # Update keys of adjacent vertices
            for neighbor, weight in adjacency_list[u]:
                if not in_mst[neighbor] and weight < key[neighbor]:
                    key[neighbor] = weight
                    parent[neighbor] = u
                    heap.insert(weight, neighbor)
                    logger.debug(
                        f"    Updated key[{neighbor}] = {weight}, "
                        f"parent = {u}"
                    )

        if vertices_processed < num_vertices:
            raise ValueError("Graph is disconnected")

        logger.info(
            f"MST found: {len(mst_edges)} edges, total weight = {total_weight}"
        )

        return mst_edges, total_weight

    def get_mst_edges_list(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
    ) -> List[Tuple[int, int, float]]:
        """Get MST edges using list-based approach.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).

        Returns:
            List of edges in MST.
        """
        mst_edges, _ = self.find_mst_list(num_vertices, edges, start_vertex)
        return mst_edges

    def get_mst_edges_heap(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
    ) -> List[Tuple[int, int, float]]:
        """Get MST edges using heap-based approach.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).

        Returns:
            List of edges in MST.
        """
        mst_edges, _ = self.find_mst_heap(num_vertices, edges, start_vertex)
        return mst_edges

    def get_mst_weight_list(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
    ) -> float:
        """Get MST weight using list-based approach.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).

        Returns:
            Total weight of MST.
        """
        _, total_weight = self.find_mst_list(num_vertices, edges, start_vertex)
        return total_weight

    def get_mst_weight_heap(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
    ) -> float:
        """Get MST weight using heap-based approach.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).

        Returns:
            Total weight of MST.
        """
        _, total_weight = self.find_mst_heap(num_vertices, edges, start_vertex)
        return total_weight

    def compare_approaches(
        self,
        num_vertices: int,
        edges: List[Tuple[int, int, float]],
        start_vertex: int = 0,
        iterations: int = 1,
    ) -> Dict[str, any]:
        """Compare list-based and heap-based approaches.

        Args:
            num_vertices: Number of vertices in graph.
            edges: List of edges as (source, destination, weight) tuples.
            start_vertex: Starting vertex (default: 0).
            iterations: Number of iterations for timing (default: 1).

        Returns:
            Dictionary containing comparison data.
        """
        logger.info(
            f"Comparing approaches: {num_vertices} vertices, "
            f"{len(edges)} edges, iterations={iterations}"
        )

        results = {
            "num_vertices": num_vertices,
            "num_edges": len(edges),
            "start_vertex": start_vertex,
            "iterations": iterations,
            "list_based": {},
            "heap_based": {},
        }

        # List-based approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                mst_edges, total_weight = self.find_mst_list(
                    num_vertices, edges, start_vertex
                )
            list_time = time.perf_counter() - start_time

            results["list_based"] = {
                "mst_edges": len(mst_edges),
                "total_weight": total_weight,
                "time_seconds": list_time / iterations,
                "time_milliseconds": (list_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"List-based approach failed: {e}")
            results["list_based"] = {"success": False, "error": str(e)}

        # Heap-based approach
        try:
            start_time = time.perf_counter()
            for _ in range(iterations):
                mst_edges, total_weight = self.find_mst_heap(
                    num_vertices, edges, start_vertex
                )
            heap_time = time.perf_counter() - start_time

            results["heap_based"] = {
                "mst_edges": len(mst_edges),
                "total_weight": total_weight,
                "time_seconds": heap_time / iterations,
                "time_milliseconds": (heap_time / iterations) * 1000,
                "success": True,
            }
        except Exception as e:
            logger.error(f"Heap-based approach failed: {e}")
            results["heap_based"] = {"success": False, "error": str(e)}

        # Verify results match
        if (
            results["list_based"].get("success", False)
            and results["heap_based"].get("success", False)
        ):
            list_weight = results["list_based"]["total_weight"]
            heap_weight = results["heap_based"]["total_weight"]
            if abs(list_weight - heap_weight) < 0.001:
                logger.info("Both approaches produced identical MST weights")
            else:
                logger.warning("MST weights differ between approaches!")

            # Determine fastest
            list_time = results["list_based"]["time_seconds"]
            heap_time = results["heap_based"]["time_seconds"]
            if list_time < heap_time:
                results["fastest"] = "list_based"
                results["fastest_time"] = list_time
            else:
                results["fastest"] = "heap_based"
                results["fastest_time"] = heap_time

        return results

    def generate_report(
        self,
        comparison_data: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate comparison report for Prim's algorithm approaches.

        Args:
            comparison_data: Comparison data from compare_approaches().
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "PRIM'S ALGORITHM COMPARISON REPORT",
            "=" * 80,
            "",
            f"Number of vertices: {comparison_data['num_vertices']}",
            f"Number of edges: {comparison_data['num_edges']}",
            f"Start vertex: {comparison_data['start_vertex']}",
            f"Iterations: {comparison_data['iterations']}",
            "",
            "RESULTS",
            "-" * 80,
        ]

        # List-based results
        report_lines.append("\nLIST-BASED APPROACH:")
        list_data = comparison_data["list_based"]
        if list_data.get("success", False):
            report_lines.append(f"  MST edges: {list_data['mst_edges']}")
            report_lines.append(f"  Total weight: {list_data['total_weight']:.2f}")
            report_lines.append(
                f"  Time: {list_data['time_milliseconds']:.4f} ms "
                f"({list_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {list_data.get('error', 'Unknown')}")

        # Heap-based results
        report_lines.append("\nHEAP-BASED APPROACH:")
        heap_data = comparison_data["heap_based"]
        if heap_data.get("success", False):
            report_lines.append(f"  MST edges: {heap_data['mst_edges']}")
            report_lines.append(f"  Total weight: {heap_data['total_weight']:.2f}")
            report_lines.append(
                f"  Time: {heap_data['time_milliseconds']:.4f} ms "
                f"({heap_data['time_seconds']:.6f} seconds)"
            )
        else:
            report_lines.append(f"  Status: Failed")
            report_lines.append(f"  Error: {heap_data.get('error', 'Unknown')}")

        if "fastest" in comparison_data:
            report_lines.extend([
                "",
                "PERFORMANCE SUMMARY",
                "-" * 80,
                f"Fastest approach: {comparison_data['fastest']}",
                f"Fastest time: {comparison_data['fastest_time']*1000:.4f} ms",
            ])

        report_lines.extend([
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "List-based Approach:",
            "  Time Complexity: O(V²) where V=vertices",
            "  Space Complexity: O(V + E) for adjacency list",
            "  Best for: Dense graphs (E ≈ V²)",
            "",
            "Heap-based Approach:",
            "  Time Complexity: O(E log V) where E=edges, V=vertices",
            "  Space Complexity: O(V + E) for adjacency list and heap",
            "  Best for: Sparse graphs (E << V²)",
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
        description="Find minimum spanning tree using Prim's algorithm "
        "with different data structure choices"
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
        "--start-vertex",
        type=int,
        default=0,
        help="Starting vertex (default: 0)",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-o",
        "--operation",
        choices=["list", "heap", "compare"],
        default="compare",
        help="Operation to perform (default: compare)",
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
        prim = PrimMST(config_path=args.config)

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
            f"Input: {args.num_vertices} vertices, "
            f"{len(edges)} edges, start={args.start_vertex}"
        )

        if args.operation == "list":
            mst_edges, total_weight = prim.find_mst_list(
                args.num_vertices, edges, args.start_vertex
            )
            print(f"Minimum Spanning Tree (List-based):")
            print(f"  Edges: {mst_edges}")
            print(f"  Total weight: {total_weight:.2f}")

        elif args.operation == "heap":
            mst_edges, total_weight = prim.find_mst_heap(
                args.num_vertices, edges, args.start_vertex
            )
            print(f"Minimum Spanning Tree (Heap-based):")
            print(f"  Edges: {mst_edges}")
            print(f"  Total weight: {total_weight:.2f}")

        elif args.operation == "compare":
            comparison = prim.compare_approaches(
                args.num_vertices, edges, args.start_vertex, args.iterations
            )

            print(f"\nPrim's Algorithm Comparison:")
            print(f"Vertices: {comparison['num_vertices']}")
            print(f"Edges: {comparison['num_edges']}")
            print(f"Start vertex: {comparison['start_vertex']}")
            print("-" * 60)

            # List-based
            list_data = comparison["list_based"]
            if list_data.get("success", False):
                print(
                    f"List-based:      "
                    f"edges={list_data['mst_edges']}, "
                    f"weight={list_data['total_weight']:.2f}  "
                    f"({list_data['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"List-based:      Failed - "
                    f"{list_data.get('error', 'Unknown')}"
                )

            # Heap-based
            heap_data = comparison["heap_based"]
            if heap_data.get("success", False):
                print(
                    f"Heap-based:      "
                    f"edges={heap_data['mst_edges']}, "
                    f"weight={heap_data['total_weight']:.2f}  "
                    f"({heap_data['time_milliseconds']:8.4f} ms)"
                )
            else:
                print(
                    f"Heap-based:      Failed - "
                    f"{heap_data.get('error', 'Unknown')}"
                )

            if "fastest" in comparison:
                print(f"\nFastest: {comparison['fastest']}")

            if args.report:
                report = prim.generate_report(
                    comparison, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
