"""Simplex algorithm for linear programming with pivot operations.

This module implements the simplex algorithm for solving linear programming
problems using tableau management and pivot operations.
"""

import logging
import sys
from enum import Enum
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class SolutionStatus(Enum):
    """Status of linear programming solution."""

    OPTIMAL = "optimal"
    UNBOUNDED = "unbounded"
    INFEASIBLE = "infeasible"
    UNKNOWN = "unknown"


class SimplexAlgorithm:
    """Simplex algorithm for linear programming."""

    def __init__(
        self,
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        maximize: bool = True,
    ) -> None:
        """Initialize simplex algorithm.

        Args:
            objective: Objective function coefficients (c).
            constraints: Constraint matrix (A).
            rhs: Right-hand side values (b).
            maximize: True to maximize, False to minimize.
        """
        self.objective = objective
        self.constraints = constraints
        self.rhs = rhs
        self.maximize = maximize
        self.tableau: List[List[float]] = []
        self.basic_vars: List[int] = []
        self.non_basic_vars: List[int] = []
        self.num_vars = len(objective)
        self.num_constraints = len(constraints)

    def _create_tableau(self) -> None:
        """Create initial simplex tableau."""
        num_cols = self.num_vars + self.num_constraints + 1
        num_rows = self.num_constraints + 1

        self.tableau = [[0.0] * num_cols for _ in range(num_rows)]

        for i in range(self.num_constraints):
            for j in range(self.num_vars):
                self.tableau[i][j] = self.constraints[i][j]

            for j in range(self.num_constraints):
                if i == j:
                    self.tableau[i][self.num_vars + j] = 1.0

            self.tableau[i][num_cols - 1] = self.rhs[i]

        for j in range(self.num_vars):
            sign = -1.0 if self.maximize else 1.0
            self.tableau[num_rows - 1][j] = sign * self.objective[j]

        self.basic_vars = list(
            range(self.num_vars, self.num_vars + self.num_constraints)
        )
        self.non_basic_vars = list(range(self.num_vars))

    def _find_entering_variable(self) -> Optional[int]:
        """Find entering variable (pivot column).

        Returns:
            Column index of entering variable, or None if optimal.
        """
        last_row = self.tableau[-1]
        if self.maximize:
            min_val = min(last_row[:-1])
            if min_val >= -1e-9:
                return None
            return last_row.index(min_val)
        else:
            max_val = max(last_row[:-1])
            if max_val <= 1e-9:
                return None
            return last_row.index(max_val)

    def _find_leaving_variable(self, entering_col: int) -> Optional[int]:
        """Find leaving variable (pivot row).

        Args:
            entering_col: Column index of entering variable.

        Returns:
            Row index of leaving variable, or None if unbounded.
        """
        ratios: List[Tuple[float, int]] = []
        rhs_col = len(self.tableau[0]) - 1

        for i in range(len(self.tableau) - 1):
            if self.tableau[i][entering_col] > 1e-9:
                ratio = self.tableau[i][rhs_col] / self.tableau[i][entering_col]
                if ratio >= -1e-9:
                    ratios.append((ratio, i))

        if not ratios:
            return None

        ratios.sort(key=lambda x: x[0])
        return ratios[0][1]

    def _pivot(self, pivot_row: int, pivot_col: int) -> None:
        """Perform pivot operation.

        Args:
            pivot_row: Row index of pivot element.
            pivot_col: Column index of pivot element.
        """
        pivot_val = self.tableau[pivot_row][pivot_col]

        if abs(pivot_val) < 1e-9:
            raise ValueError("Pivot element is zero")

        for j in range(len(self.tableau[0])):
            self.tableau[pivot_row][j] /= pivot_val

        for i in range(len(self.tableau)):
            if i != pivot_row:
                factor = self.tableau[i][pivot_col]
                for j in range(len(self.tableau[0])):
                    self.tableau[i][j] -= factor * self.tableau[pivot_row][j]

        entering_var = pivot_col
        leaving_var = self.basic_vars[pivot_row]

        self.basic_vars[pivot_row] = entering_var

        if leaving_var in self.non_basic_vars:
            idx = self.non_basic_vars.index(leaving_var)
            self.non_basic_vars[idx] = entering_var
        else:
            self.non_basic_vars.append(entering_var)

    def _is_optimal(self) -> bool:
        """Check if current solution is optimal.

        Returns:
            True if optimal, False otherwise.
        """
        last_row = self.tableau[-1]
        if self.maximize:
            return all(x >= -1e-9 for x in last_row[:-1])
        else:
            return all(x <= 1e-9 for x in last_row[:-1])

    def solve(self, max_iterations: int = 1000) -> Tuple[SolutionStatus, Dict[str, float], float]:
        """Solve linear programming problem using simplex algorithm.

        Args:
            max_iterations: Maximum number of iterations.

        Returns:
            Tuple (status, solution_dict, objective_value).
        """
        self._create_tableau()

        for iteration in range(max_iterations):
            if self._is_optimal():
                return self._extract_solution()

            entering_col = self._find_entering_variable()
            if entering_col is None:
                return self._extract_solution()

            leaving_row = self._find_leaving_variable(entering_col)
            if leaving_row is None:
                return (SolutionStatus.UNBOUNDED, {}, float("inf"))

            self._pivot(leaving_row, entering_col)

        return (SolutionStatus.UNKNOWN, {}, 0.0)

    def _extract_solution(self) -> Tuple[SolutionStatus, Dict[str, float], float]:
        """Extract solution from tableau.

        Returns:
            Tuple (status, solution_dict, objective_value).
        """
        solution: Dict[str, float] = {}
        rhs_col = len(self.tableau[0]) - 1

        for i in range(self.num_vars):
            solution[f"x{i + 1}"] = 0.0

        for i, var_idx in enumerate(self.basic_vars):
            if var_idx < self.num_vars:
                solution[f"x{var_idx + 1}"] = self.tableau[i][rhs_col]

        objective_value = self.tableau[-1][rhs_col] if self.maximize else -self.tableau[-1][rhs_col]

        return (SolutionStatus.OPTIMAL, solution, objective_value)

    def get_tableau(self) -> List[List[float]]:
        """Get current tableau.

        Returns:
            Current tableau matrix.
        """
        return [row[:] for row in self.tableau]

    def get_basic_variables(self) -> List[int]:
        """Get list of basic variables.

        Returns:
            List of basic variable indices.
        """
        return self.basic_vars[:]

    def get_non_basic_variables(self) -> List[int]:
        """Get list of non-basic variables.

        Returns:
            List of non-basic variable indices.
        """
        return self.non_basic_vars[:]


def main() -> None:
    """Main function to run the simplex algorithm CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Simplex algorithm for linear programming"
    )
    parser.add_argument(
        "--objective",
        type=str,
        required=True,
        help="Objective function coefficients (format: c1,c2,...)",
    )
    parser.add_argument(
        "--constraints",
        type=str,
        required=True,
        help="Constraints matrix (format: 'a11,a12,...;a21,a22,...')",
    )
    parser.add_argument(
        "--rhs",
        type=str,
        required=True,
        help="Right-hand side values (format: b1,b2,...)",
    )
    parser.add_argument(
        "--minimize",
        action="store_true",
        help="Minimize objective (default: maximize)",
    )
    parser.add_argument(
        "--tableau",
        action="store_true",
        help="Show final tableau",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1000,
        help="Maximum iterations (default: 1000)",
    )

    args = parser.parse_args()

    try:
        objective = [float(x.strip()) for x in args.objective.split(",")]

        constraint_strings = args.constraints.split(";")
        constraints: List[List[float]] = []
        for cs in constraint_strings:
            constraints.append([float(x.strip()) for x in cs.split(",")])

        rhs = [float(x.strip()) for x in args.rhs.split(",")]

        if len(constraints) != len(rhs):
            raise ValueError("Number of constraints must match number of RHS values")

        for constraint in constraints:
            if len(constraint) != len(objective):
                raise ValueError(
                    "Each constraint must have same number of coefficients as objective"
                )

        print(f"Objective: {objective}")
        print(f"Constraints: {constraints}")
        print(f"RHS: {rhs}")
        print(f"Mode: {'Minimize' if args.minimize else 'Maximize'}")
        print()

        simplex = SimplexAlgorithm(
            objective, constraints, rhs, maximize=not args.minimize
        )
        status, solution, obj_value = simplex.solve(max_iterations=args.iterations)

        print(f"Solution Status: {status.value}")
        print(f"Objective Value: {obj_value:.4f}")
        print(f"Solution:")
        for var, value in sorted(solution.items()):
            print(f"  {var} = {value:.4f}")

        if args.tableau:
            print(f"\nFinal Tableau:")
            tableau = simplex.get_tableau()
            for i, row in enumerate(tableau):
                print(f"  Row {i}: {[f'{x:.4f}' for x in row]}")

        print(f"\nBasic Variables: {simplex.get_basic_variables()}")
        print(f"Non-Basic Variables: {simplex.get_non_basic_variables()}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
