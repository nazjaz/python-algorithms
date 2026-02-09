"""Branch and bound algorithm for integer linear programming.

This module implements branch and bound algorithm for solving integer linear
programming problems using LP relaxation and tree search.
"""

import copy
import logging
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class NodeStatus(Enum):
    """Status of branch and bound node."""

    OPEN = "open"
    PRUNED = "pruned"
    SOLVED = "solved"
    INFEASIBLE = "infeasible"


@dataclass
class BBNode:
    """Branch and bound node."""

    lower_bounds: List[Optional[float]]
    upper_bounds: List[Optional[float]]
    lp_solution: Optional[Dict[int, float]] = None
    lp_objective: float = float("-inf")
    status: NodeStatus = NodeStatus.OPEN
    depth: int = 0


class BranchAndBound:
    """Branch and bound algorithm for integer linear programming."""

    def __init__(
        self,
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        maximize: bool = True,
        integer_vars: Optional[List[int]] = None,
    ) -> None:
        """Initialize branch and bound algorithm.

        Args:
            objective: Objective function coefficients.
            constraints: Constraint matrix.
            rhs: Right-hand side values.
            maximize: True to maximize, False to minimize.
            integer_vars: List of variable indices that must be integer.
                         If None, all variables are integer.
        """
        self.objective = objective
        self.constraints = constraints
        self.rhs = rhs
        self.maximize = maximize
        self.num_vars = len(objective)
        self.num_constraints = len(constraints)

        if integer_vars is None:
            self.integer_vars = list(range(self.num_vars))
        else:
            self.integer_vars = integer_vars

        self.best_solution: Optional[Dict[int, float]] = None
        self.best_objective = float("-inf") if maximize else float("inf")
        self.nodes_explored = 0
        self.has_feasible = False

    def _solve_lp_relaxation(
        self, lower_bounds: List[Optional[float]], upper_bounds: List[Optional[float]]
    ) -> Tuple[Optional[Dict[int, float]], float, bool]:
        """Solve LP relaxation with bounds.

        Args:
            lower_bounds: Lower bounds for each variable.
            upper_bounds: Upper bounds for each variable.

        Returns:
            Tuple (solution, objective_value, feasible).
        """
        try:
            adjusted_constraints = []
            adjusted_rhs = []

            for i in range(self.num_constraints):
                adjusted_constraints.append(self.constraints[i][:])
                adjusted_rhs.append(self.rhs[i])

            for j in range(self.num_vars):
                if lower_bounds[j] is not None:
                    constraint = [0.0] * self.num_vars
                    constraint[j] = -1.0
                    adjusted_constraints.append(constraint)
                    adjusted_rhs.append(-lower_bounds[j])

                if upper_bounds[j] is not None:
                    constraint = [0.0] * self.num_vars
                    constraint[j] = 1.0
                    adjusted_constraints.append(constraint)
                    adjusted_rhs.append(upper_bounds[j])

            solution, obj_value = self._simple_simplex(
                self.objective, adjusted_constraints, adjusted_rhs, self.maximize
            )

            if solution is None:
                return (None, 0.0, False)

            for j in range(self.num_vars):
                if lower_bounds[j] is not None and solution.get(j, 0.0) < lower_bounds[j] - 1e-6:
                    return (None, 0.0, False)
                if upper_bounds[j] is not None and solution.get(j, 0.0) > upper_bounds[j] + 1e-6:
                    return (None, 0.0, False)

            return (solution, obj_value, True)

        except Exception:
            return (None, 0.0, False)

    def _simple_simplex(
        self,
        objective: List[float],
        constraints: List[List[float]],
        rhs: List[float],
        maximize: bool,
    ) -> Tuple[Optional[Dict[int, float]], float]:
        """Simple simplex solver for LP relaxation.

        Args:
            objective: Objective coefficients.
            constraints: Constraint matrix.
            rhs: Right-hand side values.
            maximize: True to maximize.

        Returns:
            Tuple (solution, objective_value).
        """
        num_vars = len(objective)
        num_constraints = len(constraints)

        tableau: List[List[float]] = []
        for i in range(num_constraints):
            row = constraints[i][:] + [0.0] * num_constraints
            row[num_vars + i] = 1.0
            row.append(rhs[i])
            tableau.append(row)

        obj_row = []
        for j in range(num_vars):
            sign = -1.0 if maximize else 1.0
            obj_row.append(sign * objective[j])
        for j in range(num_constraints + 1):
            obj_row.append(0.0)
        tableau.append(obj_row)

        basic_vars = list(range(num_vars, num_vars + num_constraints))

        max_iterations = 1000
        for _ in range(max_iterations):
            if self._is_optimal_simple(tableau, maximize):
                break

            entering_col = self._find_entering_simple(tableau, maximize)
            if entering_col is None:
                break

            leaving_row = self._find_leaving_simple(tableau, entering_col)
            if leaving_row is None:
                return (None, float("inf") if maximize else float("-inf"))

            self._pivot_simple(tableau, leaving_row, entering_col)
            basic_vars[leaving_row] = entering_col

        rhs_col = len(tableau[0]) - 1
        solution: Dict[int, float] = {}

        for i in range(num_vars):
            solution[i] = 0.0

        for i, var_idx in enumerate(basic_vars):
            if var_idx < num_vars:
                solution[var_idx] = tableau[i][rhs_col]

        obj_value = (
            tableau[-1][rhs_col] if maximize else -tableau[-1][rhs_col]
        )

        return (solution, obj_value)

    def _is_optimal_simple(
        self, tableau: List[List[float]], maximize: bool
    ) -> bool:
        """Check if tableau is optimal.

        Args:
            tableau: Simplex tableau.
            maximize: True if maximizing.

        Returns:
            True if optimal.
        """
        last_row = tableau[-1]
        if maximize:
            return all(x >= -1e-9 for x in last_row[:-1])
        else:
            return all(x <= 1e-9 for x in last_row[:-1])

    def _find_entering_simple(
        self, tableau: List[List[float]], maximize: bool
    ) -> Optional[int]:
        """Find entering variable.

        Args:
            tableau: Simplex tableau.
            maximize: True if maximizing.

        Returns:
            Column index or None.
        """
        last_row = tableau[-1]
        if maximize:
            min_val = min(last_row[:-1])
            if min_val >= -1e-9:
                return None
            return last_row.index(min_val)
        else:
            max_val = max(last_row[:-1])
            if max_val <= 1e-9:
                return None
            return last_row.index(max_val)

    def _find_leaving_simple(
        self, tableau: List[List[float]], entering_col: int
    ) -> Optional[int]:
        """Find leaving variable.

        Args:
            tableau: Simplex tableau.
            entering_col: Entering column.

        Returns:
            Row index or None.
        """
        ratios: List[Tuple[float, int]] = []
        rhs_col = len(tableau[0]) - 1

        for i in range(len(tableau) - 1):
            if tableau[i][entering_col] > 1e-9:
                ratio = tableau[i][rhs_col] / tableau[i][entering_col]
                if ratio >= -1e-9:
                    ratios.append((ratio, i))

        if not ratios:
            return None

        ratios.sort(key=lambda x: x[0])
        return ratios[0][1]

    def _pivot_simple(
        self, tableau: List[List[float]], pivot_row: int, pivot_col: int
    ) -> None:
        """Perform pivot operation.

        Args:
            tableau: Simplex tableau.
            pivot_row: Pivot row.
            pivot_col: Pivot column.
        """
        pivot_val = tableau[pivot_row][pivot_col]

        for j in range(len(tableau[0])):
            tableau[pivot_row][j] /= pivot_val

        for i in range(len(tableau)):
            if i != pivot_row:
                factor = tableau[i][pivot_col]
                for j in range(len(tableau[0])):
                    tableau[i][j] -= factor * tableau[pivot_row][j]

    def _is_integer_solution(self, solution: Dict[int, float]) -> bool:
        """Check if solution is integer for integer variables.

        Args:
            solution: Solution dictionary.

        Returns:
            True if all integer variables are integer.
        """
        for var_idx in self.integer_vars:
            if var_idx in solution:
                value = solution[var_idx]
                if abs(value - round(value)) > 1e-6:
                    return False
        return True

    def _round_solution(self, solution: Dict[int, float]) -> Dict[int, float]:
        """Round solution to integers.

        Args:
            solution: Solution dictionary.

        Returns:
            Rounded solution.
        """
        rounded = {}
        for var_idx, value in solution.items():
            if var_idx in self.integer_vars:
                rounded[var_idx] = float(round(value))
            else:
                rounded[var_idx] = value
        return rounded

    def _find_branching_variable(
        self, solution: Dict[int, float]
    ) -> Optional[int]:
        """Find variable to branch on.

        Args:
            solution: Current LP solution.

        Returns:
            Variable index to branch on, or None.
        """
        for var_idx in self.integer_vars:
            if var_idx in solution:
                value = solution[var_idx]
                fractional = abs(value - round(value))
                if fractional > 1e-6:
                    return var_idx
        return None

    def _should_prune(self, lp_objective: float) -> bool:
        """Check if node should be pruned.

        Args:
            lp_objective: LP relaxation objective value.

        Returns:
            True if should prune.
        """
        if not self.has_feasible:
            return False

        if self.maximize:
            return lp_objective < self.best_objective - 1e-9
        else:
            return lp_objective > self.best_objective + 1e-9

    def _update_best_solution(
        self, solution: Dict[int, float], objective: float
    ) -> None:
        """Update best solution if better.

        Args:
            solution: Integer solution.
            objective: Objective value.
        """
        if self.maximize:
            if not self.has_feasible or objective > self.best_objective + 1e-9:
                self.best_objective = objective
                self.best_solution = solution.copy()
                self.has_feasible = True
        else:
            if not self.has_feasible or objective < self.best_objective - 1e-9:
                self.best_objective = objective
                self.best_solution = solution.copy()
                self.has_feasible = True

    def solve(self, max_nodes: int = 10000) -> Tuple[Optional[Dict[int, float]], float]:
        """Solve integer linear programming problem using branch and bound.

        Args:
            max_nodes: Maximum number of nodes to explore.

        Returns:
            Tuple (solution, objective_value).
        """
        initial_lower = [None] * self.num_vars
        initial_upper = [None] * self.num_vars

        root_node = BBNode(
            lower_bounds=initial_lower,
            upper_bounds=initial_upper,
        )

        solution, obj_value, feasible = self._solve_lp_relaxation(
            initial_lower, initial_upper
        )

        if not feasible:
            return (None, float("-inf") if self.maximize else float("inf"))

        root_node.lp_solution = solution
        root_node.lp_objective = obj_value

        if self._is_integer_solution(solution):
            rounded = self._round_solution(solution)
            rounded_obj = sum(
                self.objective[i] * rounded.get(i, 0.0) for i in range(self.num_vars)
            )
            self._update_best_solution(rounded, rounded_obj)
            if self.best_solution:
                return (self.best_solution.copy(), self.best_objective)
            return (rounded, rounded_obj)

        nodes: List[BBNode] = [root_node]

        while nodes and self.nodes_explored < max_nodes:
            node = nodes.pop(0)
            self.nodes_explored += 1

            if node.status == NodeStatus.PRUNED:
                continue

            if self._should_prune(node.lp_objective):
                node.status = NodeStatus.PRUNED
                continue

            if node.lp_solution is None:
                continue

            branch_var = self._find_branching_variable(node.lp_solution)
            if branch_var is None:
                rounded = self._round_solution(node.lp_solution)
                rounded_obj = sum(
                    self.objective[i] * rounded.get(i, 0.0)
                    for i in range(self.num_vars)
                )
                self._update_best_solution(rounded, rounded_obj)
                node.status = NodeStatus.SOLVED
                continue

            branch_value = node.lp_solution[branch_var]
            floor_val = int(branch_value)
            ceil_val = floor_val + 1

            lower_bounds1 = node.lower_bounds[:]
            upper_bounds1 = node.upper_bounds[:]
            if upper_bounds1[branch_var] is None:
                upper_bounds1[branch_var] = float(floor_val)
            else:
                upper_bounds1[branch_var] = min(
                    upper_bounds1[branch_var], float(floor_val)
                )

            solution1, obj1, feasible1 = self._solve_lp_relaxation(
                lower_bounds1, upper_bounds1
            )

            if feasible1 and solution1 is not None and not self._should_prune(obj1):
                node1 = BBNode(
                    lower_bounds=lower_bounds1,
                    upper_bounds=upper_bounds1,
                    lp_solution=solution1,
                    lp_objective=obj1,
                    depth=node.depth + 1,
                )
                if self._is_integer_solution(solution1):
                    rounded = self._round_solution(solution1)
                    rounded_obj = sum(
                        self.objective[i] * rounded.get(i, 0.0)
                        for i in range(self.num_vars)
                    )
                    self._update_best_solution(rounded, rounded_obj)
                    node1.status = NodeStatus.SOLVED
                else:
                    nodes.insert(0, node1)

            lower_bounds2 = node.lower_bounds[:]
            upper_bounds2 = node.upper_bounds[:]
            if lower_bounds2[branch_var] is None:
                lower_bounds2[branch_var] = float(ceil_val)
            else:
                lower_bounds2[branch_var] = max(
                    lower_bounds2[branch_var], float(ceil_val)
                )

            solution2, obj2, feasible2 = self._solve_lp_relaxation(
                lower_bounds2, upper_bounds2
            )

            if feasible2 and solution2 is not None and not self._should_prune(obj2):
                node2 = BBNode(
                    lower_bounds=lower_bounds2,
                    upper_bounds=upper_bounds2,
                    lp_solution=solution2,
                    lp_objective=obj2,
                    depth=node.depth + 1,
                )
                if self._is_integer_solution(solution2):
                    rounded = self._round_solution(solution2)
                    rounded_obj = sum(
                        self.objective[i] * rounded.get(i, 0.0)
                        for i in range(self.num_vars)
                    )
                    self._update_best_solution(rounded, rounded_obj)
                    node2.status = NodeStatus.SOLVED
                else:
                    nodes.insert(0, node2)

        if self.best_solution is None:
            return (None, float("-inf") if self.maximize else float("inf"))

        return (self.best_solution.copy(), self.best_objective)


def main() -> None:
    """Main function to run the branch and bound CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Branch and bound algorithm for integer linear programming"
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
        "--integer-vars",
        type=str,
        help="Integer variable indices (format: 0,1,2,...). Default: all variables",
    )
    parser.add_argument(
        "--max-nodes",
        type=int,
        default=10000,
        help="Maximum nodes to explore (default: 10000)",
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

        integer_vars = None
        if args.integer_vars:
            integer_vars = [int(x.strip()) for x in args.integer_vars.split(",")]

        print(f"Objective: {objective}")
        print(f"Constraints: {constraints}")
        print(f"RHS: {rhs}")
        print(f"Mode: {'Minimize' if args.minimize else 'Maximize'}")
        if integer_vars:
            print(f"Integer Variables: {integer_vars}")
        else:
            print(f"Integer Variables: All")
        print()

        bb = BranchAndBound(
            objective, constraints, rhs, maximize=not args.minimize, integer_vars=integer_vars
        )
        solution, obj_value = bb.solve(max_nodes=args.max_nodes)

        if solution is not None:
            print(f"Solution Found:")
            print(f"  Objective Value: {obj_value:.4f}")
            print(f"  Solution:")
            for var_idx in sorted(solution.keys()):
                print(f"    x{var_idx + 1} = {solution[var_idx]:.0f}")
            print(f"  Nodes Explored: {bb.nodes_explored}")
        else:
            print("No feasible integer solution found")
            print(f"Nodes Explored: {bb.nodes_explored}")

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
