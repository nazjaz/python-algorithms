"""Test suite for branch and bound algorithm implementation."""

import pytest

from src.main import BranchAndBound, BBNode, NodeStatus


class TestBranchAndBound:
    """Test cases for BranchAndBound class."""

    def test_initialization(self) -> None:
        """Test BranchAndBound initialization."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs)
        assert bb.objective == objective
        assert bb.constraints == constraints
        assert bb.rhs == rhs
        assert bb.maximize is True

    def test_initialization_minimize(self) -> None:
        """Test initialization with minimize."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs, maximize=False)
        assert bb.maximize is False

    def test_initialization_integer_vars(self) -> None:
        """Test initialization with specific integer variables."""
        objective = [1, 1, 1]
        constraints = [[1, 0, 0], [0, 1, 0]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs, integer_vars=[0, 1])
        assert bb.integer_vars == [0, 1]

    def test_solve_lp_relaxation(self) -> None:
        """Test LP relaxation solving."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1.5, 1.5]
        bb = BranchAndBound(objective, constraints, rhs)
        solution, obj_value, feasible = bb._solve_lp_relaxation([None, None], [None, None])
        assert feasible is True
        assert solution is not None
        assert obj_value > 0

    def test_solve_lp_relaxation_with_bounds(self) -> None:
        """Test LP relaxation with bounds."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1.5, 1.5]
        bb = BranchAndBound(objective, constraints, rhs)
        solution, obj_value, feasible = bb._solve_lp_relaxation([None, None], [1.0, None])
        assert feasible is True
        assert solution is not None
        assert solution[0] <= 1.0 + 1e-6

    def test_is_integer_solution(self) -> None:
        """Test integer solution check."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs)
        solution1 = {0: 1.0, 1: 1.0}
        solution2 = {0: 1.5, 1: 1.0}
        assert bb._is_integer_solution(solution1) is True
        assert bb._is_integer_solution(solution2) is False

    def test_round_solution(self) -> None:
        """Test solution rounding."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs)
        solution = {0: 1.5, 1: 2.3}
        rounded = bb._round_solution(solution)
        assert rounded[0] == 2.0
        assert rounded[1] == 2.0

    def test_find_branching_variable(self) -> None:
        """Test finding branching variable."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs)
        solution1 = {0: 1.0, 1: 1.0}
        solution2 = {0: 1.5, 1: 1.0}
        assert bb._find_branching_variable(solution1) is None
        assert bb._find_branching_variable(solution2) == 0

    def test_should_prune(self) -> None:
        """Test pruning check."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        bb.best_objective = 5.0
        bb.has_feasible = True
        assert bb._should_prune(3.0) is True
        assert bb._should_prune(6.0) is False

    def test_update_best_solution(self) -> None:
        """Test updating best solution."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution = {0: 1.0, 1: 1.0}
        bb._update_best_solution(solution, 2.0)
        assert bb.best_solution == solution
        assert bb.best_objective == 2.0
        assert bb.has_feasible is True

    def test_solve_simple_integer(self) -> None:
        """Test solving simple integer problem."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1.0, 1.0]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution, obj_value = bb.solve()
        assert solution is not None
        assert abs(obj_value - 2.0) < 1e-6

    def test_solve_with_branching(self) -> None:
        """Test solving problem requiring branching."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1.5, 1.5]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution, obj_value = bb.solve()
        assert solution is not None
        assert abs(obj_value - 2.0) < 1e-6
        assert solution[0] == 1.0
        assert solution[1] == 1.0

    def test_solve_minimize(self) -> None:
        """Test solving minimization problem."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1.5, 1.5]
        bb = BranchAndBound(objective, constraints, rhs, maximize=False)
        solution, obj_value = bb.solve()
        assert solution is not None
        assert obj_value >= 0

    def test_solve_complex(self) -> None:
        """Test solving more complex problem."""
        objective = [3, 2]
        constraints = [[1, 1], [2, 1]]
        rhs = [4.5, 6.5]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution, obj_value = bb.solve()
        assert solution is not None
        assert obj_value > 0

    def test_solve_infeasible(self) -> None:
        """Test solving infeasible problem."""
        objective = [1, 1]
        constraints = [[1, 1], [-1, -1]]
        rhs = [1, -2]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution, obj_value = bb.solve()
        assert solution is None or obj_value == float("-inf")

    def test_solve_empty(self) -> None:
        """Test solving with empty constraints."""
        objective = [1]
        constraints: List[List[float]] = []
        rhs: List[float] = []
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution, obj_value = bb.solve()
        assert solution is None

    def test_solve_single_variable(self) -> None:
        """Test solving with single variable."""
        objective = [1]
        constraints = [[1]]
        rhs = [1.5]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        solution, obj_value = bb.solve()
        assert solution is not None
        assert solution[0] == 1.0

    def test_nodes_explored(self) -> None:
        """Test nodes explored counter."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1.5, 1.5]
        bb = BranchAndBound(objective, constraints, rhs, maximize=True)
        bb.solve()
        assert bb.nodes_explored > 0

    def test_partial_integer_vars(self) -> None:
        """Test with partial integer variables."""
        objective = [1, 1, 1]
        constraints = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        rhs = [1.5, 1.5, 1.5]
        bb = BranchAndBound(objective, constraints, rhs, integer_vars=[0, 1], maximize=True)
        solution, obj_value = bb.solve()
        assert solution is not None
        assert solution[0] == 1.0 or solution[0] == 2.0
        assert solution[1] == 1.0 or solution[1] == 2.0
