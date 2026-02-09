"""Unit tests for stack data structure module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Stack, ExpressionEvaluator


class TestStack:
    """Test cases for Stack class."""

    def test_stack_initialization(self):
        """Test stack initialization."""
        stack = Stack()
        assert stack.is_empty() is True
        assert stack.size() == 0

    def test_push(self):
        """Test push operation."""
        stack = Stack()
        stack.push(1)
        assert stack.is_empty() is False
        assert stack.size() == 1

    def test_pop(self):
        """Test pop operation."""
        stack = Stack()
        stack.push(10)
        stack.push(20)
        assert stack.pop() == 20
        assert stack.pop() == 10
        assert stack.is_empty() is True

    def test_pop_empty_stack(self):
        """Test pop from empty stack raises error."""
        stack = Stack()
        with pytest.raises(IndexError, match="Stack is empty"):
            stack.pop()

    def test_peek(self):
        """Test peek operation."""
        stack = Stack()
        stack.push(10)
        stack.push(20)
        assert stack.peek() == 20
        assert stack.size() == 2  # Size unchanged

    def test_peek_empty_stack(self):
        """Test peek on empty stack raises error."""
        stack = Stack()
        with pytest.raises(IndexError, match="Stack is empty"):
            stack.peek()

    def test_is_empty(self):
        """Test is_empty method."""
        stack = Stack()
        assert stack.is_empty() is True
        stack.push(1)
        assert stack.is_empty() is False

    def test_size(self):
        """Test size method."""
        stack = Stack()
        assert stack.size() == 0
        stack.push(1)
        assert stack.size() == 1
        stack.push(2)
        assert stack.size() == 2
        stack.pop()
        assert stack.size() == 1

    def test_lifo_behavior(self):
        """Test Last In First Out behavior."""
        stack = Stack()
        items = [1, 2, 3, 4, 5]
        for item in items:
            stack.push(item)

        popped = []
        while not stack.is_empty():
            popped.append(stack.pop())

        assert popped == list(reversed(items))


class TestExpressionEvaluator:
    """Test cases for ExpressionEvaluator class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def evaluator(self, config_file):
        """Create ExpressionEvaluator instance."""
        return ExpressionEvaluator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        evaluator = ExpressionEvaluator(config_path=str(config_path))
        assert evaluator.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            ExpressionEvaluator(config_path="nonexistent.yaml")

    def test_evaluate_postfix_simple(self, evaluator):
        """Test postfix evaluation with simple expression."""
        result = evaluator.evaluate_postfix("3 4 +")
        assert result == 7.0

    def test_evaluate_postfix_complex(self, evaluator):
        """Test postfix evaluation with complex expression."""
        result = evaluator.evaluate_postfix("3 4 + 2 *")
        assert result == 14.0

    def test_evaluate_postfix_division(self, evaluator):
        """Test postfix evaluation with division."""
        result = evaluator.evaluate_postfix("10 2 /")
        assert result == 5.0

    def test_evaluate_postfix_exponentiation(self, evaluator):
        """Test postfix evaluation with exponentiation."""
        result = evaluator.evaluate_postfix("2 3 ^")
        assert result == 8.0

    def test_evaluate_postfix_decimal(self, evaluator):
        """Test postfix evaluation with decimal numbers."""
        result = evaluator.evaluate_postfix("3.5 2.5 +")
        assert abs(result - 6.0) < 0.001

    def test_evaluate_postfix_negative(self, evaluator):
        """Test postfix evaluation with negative numbers."""
        result = evaluator.evaluate_postfix("-5 3 +")
        assert result == -2.0

    def test_evaluate_postfix_insufficient_operands(self, evaluator):
        """Test postfix evaluation with insufficient operands."""
        with pytest.raises(ValueError, match="Insufficient operands"):
            evaluator.evaluate_postfix("3 +")

    def test_evaluate_postfix_invalid_token(self, evaluator):
        """Test postfix evaluation with invalid token."""
        with pytest.raises(ValueError, match="Invalid token"):
            evaluator.evaluate_postfix("3 x +")

    def test_infix_to_postfix_simple(self, evaluator):
        """Test infix to postfix conversion with simple expression."""
        result = evaluator.infix_to_postfix("3 + 4")
        assert result == "3 4 +"

    def test_infix_to_postfix_complex(self, evaluator):
        """Test infix to postfix conversion with complex expression."""
        result = evaluator.infix_to_postfix("(3 + 4) * 2")
        assert result == "3 4 + 2 *"

    def test_infix_to_postfix_precedence(self, evaluator):
        """Test infix to postfix conversion with operator precedence."""
        result = evaluator.infix_to_postfix("3 + 4 * 2")
        assert result == "3 4 2 * +"

    def test_infix_to_postfix_parentheses(self, evaluator):
        """Test infix to postfix conversion with parentheses."""
        result = evaluator.infix_to_postfix("(3 + 4) * (2 + 1)")
        assert "3 4 +" in result
        assert "2 1 +" in result

    def test_infix_to_postfix_mismatched_parentheses(self, evaluator):
        """Test infix to postfix conversion with mismatched parentheses."""
        with pytest.raises(ValueError, match="Mismatched parentheses"):
            evaluator.infix_to_postfix("(3 + 4")

    def test_evaluate_infix_simple(self, evaluator):
        """Test infix evaluation with simple expression."""
        result = evaluator.evaluate_infix("3 + 4")
        assert result == 7.0

    def test_evaluate_infix_complex(self, evaluator):
        """Test infix evaluation with complex expression."""
        result = evaluator.evaluate_infix("(3 + 4) * 2")
        assert result == 14.0

    def test_evaluate_infix_precedence(self, evaluator):
        """Test infix evaluation with operator precedence."""
        result = evaluator.evaluate_infix("3 + 4 * 2")
        assert result == 11.0

    def test_evaluate_infix_division_by_zero(self, evaluator):
        """Test infix evaluation with division by zero."""
        with pytest.raises(ValueError, match="Division by zero"):
            evaluator.evaluate_infix("10 / 0")

    def test_generate_report(self, evaluator, temp_dir):
        """Test report generation."""
        result = evaluator.evaluate_infix("3 + 4")
        report_path = temp_dir / "report.txt"
        report = evaluator.generate_report(
            "3 + 4", "infix", result, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "EXPRESSION EVALUATION REPORT" in report
        assert "STACK OPERATIONS" in report

    def test_is_operator(self, evaluator):
        """Test operator detection."""
        assert evaluator._is_operator("+") is True
        assert evaluator._is_operator("-") is True
        assert evaluator._is_operator("*") is True
        assert evaluator._is_operator("/") is True
        assert evaluator._is_operator("^") is True
        assert evaluator._is_operator("3") is False

    def test_get_precedence(self, evaluator):
        """Test operator precedence."""
        assert evaluator._get_precedence("+") == 1
        assert evaluator._get_precedence("*") == 2
        assert evaluator._get_precedence("^") == 3

    def test_apply_operator(self, evaluator):
        """Test operator application."""
        assert evaluator._apply_operator("+", 2, 3) == 5.0
        assert evaluator._apply_operator("-", 2, 3) == 1.0
        assert evaluator._apply_operator("*", 2, 3) == 6.0
        assert evaluator._apply_operator("/", 2, 3) == 1.5
        assert evaluator._apply_operator("^", 2, 3) == 9.0
