"""Hungarian Algorithm for Solving Assignment Problem.

This module provides functionality to solve the assignment problem in bipartite
graphs using the Hungarian algorithm (Kuhn-Munkres algorithm). The assignment
problem finds the minimum cost assignment of workers to jobs given a cost matrix.
"""

import logging
import logging.handlers
import sys
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class HungarianAlgorithm:
    """Hungarian algorithm for solving assignment problem."""

    def __init__(self, cost_matrix: List[List[int]], config_path: str = "config.yaml") -> None:
        """Initialize Hungarian algorithm with cost matrix.

        Args:
            cost_matrix: Square cost matrix (n x n) where cost_matrix[i][j]
                        is cost of assigning worker i to job j.
            config_path: Path to configuration YAML file.
        """
        if not cost_matrix:
            raise ValueError("Cost matrix cannot be empty")
        if not all(len(row) == len(cost_matrix) for row in cost_matrix):
            raise ValueError("Cost matrix must be square")

        self.original_matrix = [row[:] for row in cost_matrix]
        self.n = len(cost_matrix)
        self._setup_logging()
        self.config = self._load_config(config_path)
        logger.info(f"Hungarian algorithm initialized with {self.n}x{self.n} matrix")

    def _setup_logging(self) -> None:
        """Configure logging for the application."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / "hungarian_algorithm.log"
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10485760, backupCount=5
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file.

        Args:
            config_path: Path to configuration file.

        Returns:
            Configuration dictionary.
        """
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded from {config_path}")
                return config or {}
        except FileNotFoundError:
            logger.warning(f"Configuration file not found: {config_path}")
            return {}

    def solve(self) -> Tuple[int, List[Tuple[int, int]]]:
        """Solve assignment problem using Hungarian algorithm.

        Returns:
            Tuple of (minimum_cost, assignments) where assignments is list of
            (worker, job) pairs.
        """
        logger.info("Solving assignment problem using Hungarian algorithm")

        matrix = [row[:] for row in self.original_matrix]

        matrix = self._reduce_rows(matrix)
        matrix = self._reduce_columns(matrix)

        while True:
            marked_rows, marked_cols = self._cover_zeros(matrix)
            if len(marked_rows) + len(marked_cols) == self.n:
                break
            matrix = self._adjust_matrix(matrix, marked_rows, marked_cols)

        assignments = self._find_optimal_assignment(matrix)
        total_cost = self._calculate_total_cost(assignments)

        logger.info(f"Optimal assignment found with cost: {total_cost}")
        return total_cost, assignments

    def _reduce_rows(self, matrix: List[List[int]]) -> List[List[int]]:
        """Reduce rows by subtracting minimum from each row.

        Args:
            matrix: Cost matrix.

        Returns:
            Reduced matrix.
        """
        reduced = [row[:] for row in matrix]
        for i in range(self.n):
            min_val = min(reduced[i])
            if min_val > 0:
                for j in range(self.n):
                    reduced[i][j] -= min_val
        logger.debug("Rows reduced")
        return reduced

    def _reduce_columns(self, matrix: List[List[int]]) -> List[List[int]]:
        """Reduce columns by subtracting minimum from each column.

        Args:
            matrix: Cost matrix.

        Returns:
            Reduced matrix.
        """
        reduced = [row[:] for row in matrix]
        for j in range(self.n):
            min_val = min(reduced[i][j] for i in range(self.n))
            if min_val > 0:
                for i in range(self.n):
                    reduced[i][j] -= min_val
        logger.debug("Columns reduced")
        return reduced

    def _cover_zeros(
        self, matrix: List[List[int]]
    ) -> Tuple[List[int], List[int]]:
        """Cover zeros with minimum number of lines.

        Args:
            matrix: Cost matrix.

        Returns:
            Tuple of (marked_rows, marked_cols).
        """
        marked_rows = []
        marked_cols = []
        zeros = self._find_zeros(matrix)

        while zeros:
            row_counts = [0] * self.n
            col_counts = [0] * self.n

            for i, j in zeros:
                row_counts[i] += 1
                col_counts[j] += 1

            max_row = max(range(self.n), key=lambda i: row_counts[i])
            max_col = max(range(self.n), key=lambda j: col_counts[j])

            if row_counts[max_row] >= col_counts[max_col]:
                marked_rows.append(max_row)
                zeros = [(i, j) for i, j in zeros if i != max_row]
            else:
                marked_cols.append(max_col)
                zeros = [(i, j) for i, j in zeros if j != max_col]

        logger.debug(f"Covered zeros: {len(marked_rows)} rows, {len(marked_cols)} cols")
        return marked_rows, marked_cols

    def _find_zeros(self, matrix: List[List[int]]) -> List[Tuple[int, int]]:
        """Find all zero positions in matrix.

        Args:
            matrix: Cost matrix.

        Returns:
            List of (row, col) positions with zeros.
        """
        zeros = []
        for i in range(self.n):
            for j in range(self.n):
                if matrix[i][j] == 0:
                    zeros.append((i, j))
        return zeros

    def _adjust_matrix(
        self,
        matrix: List[List[int]],
        marked_rows: List[int],
        marked_cols: List[int],
    ) -> List[List[int]]:
        """Adjust matrix by adding/subtracting minimum uncovered value.

        Args:
            matrix: Cost matrix.
            marked_rows: Rows covered by lines.
            marked_cols: Columns covered by lines.

        Returns:
            Adjusted matrix.
        """
        adjusted = [row[:] for row in matrix]
        uncovered = []

        for i in range(self.n):
            for j in range(self.n):
                if i not in marked_rows and j not in marked_cols:
                    uncovered.append(adjusted[i][j])

        if not uncovered:
            return adjusted

        min_uncovered = min(uncovered)

        for i in range(self.n):
            for j in range(self.n):
                if i not in marked_rows and j not in marked_cols:
                    adjusted[i][j] -= min_uncovered
                elif i in marked_rows and j in marked_cols:
                    adjusted[i][j] += min_uncovered

        logger.debug("Matrix adjusted")
        return adjusted

    def _find_optimal_assignment(
        self, matrix: List[List[int]]
    ) -> List[Tuple[int, int]]:
        """Find optimal assignment from reduced matrix.

        Args:
            matrix: Reduced cost matrix.

        Returns:
            List of (worker, job) assignments.
        """
        zeros = self._find_zeros(matrix)
        assignments = []

        def find_matching() -> List[Tuple[int, int]]:
            matching = []
            used_rows = set()
            used_cols = set()

            for i, j in zeros:
                if i not in used_rows and j not in used_cols:
                    matching.append((i, j))
                    used_rows.add(i)
                    used_cols.add(j)

            if len(matching) == self.n:
                return matching

            for i in range(self.n):
                if i not in used_rows:
                    for j in range(self.n):
                        if j not in used_cols and matrix[i][j] == 0:
                            matching.append((i, j))
                            used_rows.add(i)
                            used_cols.add(j)
                            break

            if len(matching) < self.n:
                matching = self._find_complete_assignment(matrix, matching)

            return matching

        assignments = find_matching()
        return sorted(assignments)

    def _find_complete_assignment(
        self,
        matrix: List[List[int]],
        partial: List[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        """Find complete assignment using DFS.

        Args:
            matrix: Reduced cost matrix.
            partial: Partial assignments.

        Returns:
            Complete assignment list.
        """
        zeros = self._find_zeros(matrix)
        used_rows = {i for i, _ in partial}
        used_cols = {j for _, j in partial}

        def dfs(assignment: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
            if len(assignment) == self.n:
                return assignment

            assigned_rows = {i for i, _ in assignment}
            assigned_cols = {j for _, j in assignment}

            for i in range(self.n):
                if i not in assigned_rows:
                    for j in range(self.n):
                        if (
                            j not in assigned_cols
                            and (i, j) in zeros
                        ):
                            result = dfs(assignment + [(i, j)])
                            if result:
                                return result
            return None

        result = dfs(partial)
        return result if result else partial

    def _calculate_total_cost(
        self, assignments: List[Tuple[int, int]]
    ) -> int:
        """Calculate total cost of assignment.

        Args:
            assignments: List of (worker, job) pairs.

        Returns:
            Total cost.
        """
        total = 0
        for i, j in assignments:
            total += self.original_matrix[i][j]
        return total

    def get_assignment_cost(self, worker: int, job: int) -> int:
        """Get cost of specific assignment.

        Args:
            worker: Worker index.
            job: Job index.

        Returns:
            Assignment cost.
        """
        if worker < 0 or worker >= self.n:
            raise ValueError(f"Invalid worker index: {worker}")
        if job < 0 or job >= self.n:
            raise ValueError(f"Invalid job index: {job}")
        return self.original_matrix[worker][job]

    def solve_maximization(self) -> Tuple[int, List[Tuple[int, int]]]:
        """Solve maximization version of assignment problem.

        Converts maximization to minimization by negating costs.

        Returns:
            Tuple of (maximum_value, assignments).
        """
        logger.info("Solving maximization assignment problem")

        max_val = max(max(row) for row in self.original_matrix)
        transformed = [
            [max_val - cost for cost in row] for row in self.original_matrix
        ]

        temp_algorithm = HungarianAlgorithm(transformed)
        min_cost, assignments = temp_algorithm.solve()
        max_value = len(assignments) * max_val - min_cost

        logger.info(f"Maximum assignment value: {max_value}")
        return max_value, assignments

    def is_valid_assignment(self, assignments: List[Tuple[int, int]]) -> bool:
        """Check if assignment is valid (one-to-one mapping).

        Args:
            assignments: List of (worker, job) pairs.

        Returns:
            True if valid, False otherwise.
        """
        if len(assignments) != self.n:
            return False

        workers = {i for i, _ in assignments}
        jobs = {j for _, j in assignments}

        return len(workers) == self.n and len(jobs) == self.n


class BipartiteGraph:
    """Bipartite graph representation for assignment problems."""

    def __init__(self, left_size: int, right_size: int) -> None:
        """Initialize bipartite graph.

        Args:
            left_size: Number of vertices in left partition.
            right_size: Number of vertices in right partition.
        """
        if left_size < 1 or right_size < 1:
            raise ValueError("Graph size must be at least 1")
        self.left_size = left_size
        self.right_size = right_size
        self.edges: Dict[Tuple[int, int], int] = {}
        logger.info(
            f"Bipartite graph initialized: "
            f"{left_size} left, {right_size} right vertices"
        )

    def add_edge(self, left: int, right: int, weight: int) -> None:
        """Add weighted edge to graph.

        Args:
            left: Vertex in left partition.
            right: Vertex in right partition.
            weight: Edge weight (cost).
        """
        if left < 0 or left >= self.left_size:
            raise ValueError(f"Invalid left vertex: {left}")
        if right < 0 or right >= self.right_size:
            raise ValueError(f"Invalid right vertex: {right}")

        self.edges[(left, right)] = weight
        logger.debug(f"Added edge ({left}, {right}) with weight {weight}")

    def to_cost_matrix(self) -> List[List[int]]:
        """Convert bipartite graph to cost matrix.

        Returns:
            Cost matrix for Hungarian algorithm.
        """
        size = max(self.left_size, self.right_size)
        matrix = [[sys.maxsize] * size for _ in range(size)]

        for (left, right), weight in self.edges.items():
            matrix[left][right] = weight

        for i in range(size):
            for j in range(size):
                if matrix[i][j] == sys.maxsize:
                    matrix[i][j] = 0

        return matrix

    def solve_assignment(self) -> Tuple[int, List[Tuple[int, int]]]:
        """Solve assignment problem using Hungarian algorithm.

        Returns:
            Tuple of (minimum_cost, assignments).
        """
        matrix = self.to_cost_matrix()
        algorithm = HungarianAlgorithm(matrix)
        return algorithm.solve()


def main() -> None:
    """Main function to demonstrate Hungarian algorithm."""
    cost_matrix = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]

    logger.info("Solving assignment problem:")
    for i, row in enumerate(cost_matrix):
        logger.info(f"Worker {i}: {row}")

    algorithm = HungarianAlgorithm(cost_matrix)
    min_cost, assignments = algorithm.solve()

    logger.info(f"Minimum cost: {min_cost}")
    logger.info("Optimal assignments:")
    for worker, job in assignments:
        cost = algorithm.get_assignment_cost(worker, job)
        logger.info(f"  Worker {worker} -> Job {job} (cost: {cost})")

    logger.info("\nSolving maximization problem:")
    max_value, max_assignments = algorithm.solve_maximization()
    logger.info(f"Maximum value: {max_value}")

    logger.info("\nUsing bipartite graph representation:")
    graph = BipartiteGraph(4, 4)
    for i in range(4):
        for j in range(4):
            graph.add_edge(i, j, cost_matrix[i][j])

    graph_cost, graph_assignments = graph.solve_assignment()
    logger.info(f"Graph-based solution cost: {graph_cost}")


if __name__ == "__main__":
    main()
