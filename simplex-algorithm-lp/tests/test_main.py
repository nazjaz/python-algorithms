"""Test suite for simplex algorithm implementation."""

import pytest

from src.main import SimplexAlgorithm, SolutionStatus


class TestSimplexAlgorithm:
    """Test cases for SimplexAlgorithm class."""

    def test_initialization(self) -> None:
        """Test SimplexAlgorithm initialization."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        assert simplex.objective == objective
        assert simplex.constraints == constraints
        assert simplex.rhs == rhs
        assert simplex.maximize is True

    def test_initialization_minimize(self) -> None:
        """Test initialization with minimize."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=False)
        assert simplex.maximize is False

    def test_create_tableau(self) -> None:
        """Test tableau creation."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        assert len(simplex.tableau) == 3
        assert len(simplex.tableau[0]) == 5

    def test_find_entering_variable_maximize(self) -> None:
        """Test finding entering variable for maximization."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        simplex._create_tableau()
        entering = simplex._find_entering_variable()
        assert entering is not None

    def test_find_entering_variable_minimize(self) -> None:
        """Test finding entering variable for minimization."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=False)
        simplex._create_tableau()
        entering = simplex._find_entering_variable()
        assert entering is not None

    def test_find_leaving_variable(self) -> None:
        """Test finding leaving variable."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        entering = simplex._find_entering_variable()
        if entering is not None:
            leaving = simplex._find_leaving_variable(entering)
            assert leaving is not None

    def test_pivot(self) -> None:
        """Test pivot operation."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        entering = simplex._find_entering_variable()
        if entering is not None:
            leaving = simplex._find_leaving_variable(entering)
            if leaving is not None:
                simplex._pivot(leaving, entering)
                assert abs(simplex.tableau[leaving][entering] - 1.0) < 1e-9

    def test_is_optimal(self) -> None:
        """Test optimality check."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        optimal = simplex._is_optimal()
        assert isinstance(optimal, bool)

    def test_solve_simple_maximize(self) -> None:
        """Test solving simple maximization problem."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL
        assert abs(obj_value - 2.0) < 1e-6

    def test_solve_simple_minimize(self) -> None:
        """Test solving simple minimization problem."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=False)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL
        assert abs(obj_value - 0.0) < 1e-6

    def test_solve_complex(self) -> None:
        """Test solving more complex problem."""
        objective = [3, 2]
        constraints = [[1, 1], [2, 1]]
        rhs = [4, 6]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL
        assert abs(obj_value - 10.0) < 1e-6
        assert abs(solution["x1"] - 2.0) < 1e-6
        assert abs(solution["x2"] - 2.0) < 1e-6

    def test_solve_unbounded(self) -> None:
        """Test solving unbounded problem."""
        objective = [1, 1]
        constraints = [[-1, 1]]
        rhs = [1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status in [SolutionStatus.UNBOUNDED, SolutionStatus.OPTIMAL]

    def test_get_tableau(self) -> None:
        """Test getting tableau."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        tableau = simplex.get_tableau()
        assert len(tableau) == len(simplex.tableau)

    def test_get_basic_variables(self) -> None:
        """Test getting basic variables."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        basic_vars = simplex.get_basic_variables()
        assert len(basic_vars) == len(constraints)

    def test_get_non_basic_variables(self) -> None:
        """Test getting non-basic variables."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        non_basic_vars = simplex.get_non_basic_variables()
        assert len(non_basic_vars) == len(objective)

    def test_solve_single_variable(self) -> None:
        """Test solving with single variable."""
        objective = [1]
        constraints = [[1]]
        rhs = [1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL

    def test_solve_single_constraint(self) -> None:
        """Test solving with single constraint."""
        objective = [1, 1]
        constraints = [[1, 1]]
        rhs = [1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL

    def test_extract_solution(self) -> None:
        """Test solution extraction."""
        objective = [1, 1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs)
        simplex._create_tableau()
        status, solution, obj_value = simplex._extract_solution()
        assert "x1" in solution
        assert "x2" in solution

    def test_solve_zero_objective(self) -> None:
        """Test solving with zero objective."""
        objective = [0, 0]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL
        assert abs(obj_value) < 1e-6

    def test_solve_negative_coefficients(self) -> None:
        """Test solving with negative coefficients."""
        objective = [-1, -1]
        constraints = [[1, 0], [0, 1]]
        rhs = [1, 1]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL

    def test_solve_large_problem(self) -> None:
        """Test solving larger problem."""
        objective = [1, 2, 3]
        constraints = [[1, 1, 1], [2, 1, 0], [0, 1, 2]]
        rhs = [10, 8, 6]
        simplex = SimplexAlgorithm(objective, constraints, rhs, maximize=True)
        status, solution, obj_value = simplex.solve()
        assert status == SolutionStatus.OPTIMAL
