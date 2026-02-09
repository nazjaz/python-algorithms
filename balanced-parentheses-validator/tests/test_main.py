"""Unit tests for balanced parentheses validator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BalancedParenthesesValidator


class TestBalancedParenthesesValidator:
    """Test cases for BalancedParenthesesValidator class."""

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
    def validator(self, config_file):
        """Create BalancedParenthesesValidator instance."""
        return BalancedParenthesesValidator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        validator = BalancedParenthesesValidator(config_path=str(config_path))
        assert validator.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            BalancedParenthesesValidator(config_path="nonexistent.yaml")

    def test_is_balanced_simple_parentheses(self, validator):
        """Test balanced simple parentheses."""
        assert validator.is_balanced("()") is True

    def test_is_balanced_nested_parentheses(self, validator):
        """Test balanced nested parentheses."""
        assert validator.is_balanced("(())") is True
        assert validator.is_balanced("((()))") is True

    def test_is_balanced_multiple_types(self, validator):
        """Test balanced multiple bracket types."""
        assert validator.is_balanced("()[]{}") is True
        assert validator.is_balanced("([{}])") is True

    def test_is_balanced_angle_brackets(self, validator):
        """Test balanced angle brackets."""
        assert validator.is_balanced("<>") is True
        assert validator.is_balanced("<<>>") is True

    def test_is_balanced_mixed_types(self, validator):
        """Test balanced mixed bracket types."""
        assert validator.is_balanced("([{<>}])") is True
        assert validator.is_balanced("{[()]}") is True

    def test_is_balanced_empty_string(self, validator):
        """Test empty string is balanced."""
        assert validator.is_balanced("") is True

    def test_is_balanced_no_brackets(self, validator):
        """Test string with no brackets is balanced."""
        assert validator.is_balanced("hello world") is True

    def test_is_balanced_complex_expression(self, validator):
        """Test balanced complex expression."""
        expr = "function() { return [1, 2, 3]; }"
        assert validator.is_balanced(expr) is True

    def test_is_not_balanced_unmatched_opening(self, validator):
        """Test unbalanced expression with unmatched opening bracket."""
        assert validator.is_balanced("(((") is False
        assert validator.is_balanced("([{") is False

    def test_is_not_balanced_unmatched_closing(self, validator):
        """Test unbalanced expression with unmatched closing bracket."""
        assert validator.is_balanced(")))") is False
        assert validator.is_balanced("}])") is False

    def test_is_not_balanced_mismatched_types(self, validator):
        """Test unbalanced expression with mismatched bracket types."""
        assert validator.is_balanced("([)]") is False
        assert validator.is_balanced("{(})") is False

    def test_is_not_balanced_wrong_order(self, validator):
        """Test unbalanced expression with wrong bracket order."""
        assert validator.is_balanced(")(") is False
        assert validator.is_balanced("][") is False

    def test_is_not_balanced_partial_match(self, validator):
        """Test unbalanced expression with partial matches."""
        assert validator.is_balanced("()(") is False
        assert validator.is_balanced("([]") is False

    def test_is_opening_bracket(self, validator):
        """Test opening bracket detection."""
        assert validator._is_opening_bracket("(") is True
        assert validator._is_opening_bracket("[") is True
        assert validator._is_opening_bracket("{") is True
        assert validator._is_opening_bracket("<") is True
        assert validator._is_opening_bracket(")") is False
        assert validator._is_opening_bracket("a") is False

    def test_is_closing_bracket(self, validator):
        """Test closing bracket detection."""
        assert validator._is_closing_bracket(")") is True
        assert validator._is_closing_bracket("]") is True
        assert validator._is_closing_bracket("}") is True
        assert validator._is_closing_bracket(">") is True
        assert validator._is_closing_bracket("(") is False
        assert validator._is_closing_bracket("a") is False

    def test_matches(self, validator):
        """Test bracket matching."""
        assert validator._matches("(", ")") is True
        assert validator._matches("[", "]") is True
        assert validator._matches("{", "}") is True
        assert validator._matches("<", ">") is True
        assert validator._matches("(", "]") is False
        assert validator._matches("[", ")") is False

    def test_get_unmatched_brackets_balanced(self, validator):
        """Test getting unmatched brackets from balanced expression."""
        assert validator.get_unmatched_brackets("()[]{}") == []

    def test_get_unmatched_brackets_unbalanced(self, validator):
        """Test getting unmatched brackets from unbalanced expression."""
        unmatched = validator.get_unmatched_brackets("(((")
        assert "(" in unmatched
        assert len(unmatched) == 3

    def test_get_unmatched_brackets_mismatched(self, validator):
        """Test getting unmatched brackets from mismatched expression."""
        unmatched = validator.get_unmatched_brackets("([)]")
        assert len(unmatched) > 0

    def test_validate_with_details_balanced(self, validator):
        """Test detailed validation for balanced expression."""
        result = validator.validate_with_details("()[]{}")
        assert result["is_balanced"] is True
        assert result["unmatched_brackets"] == []
        assert "bracket_count" in result

    def test_validate_with_details_unbalanced(self, validator):
        """Test detailed validation for unbalanced expression."""
        result = validator.validate_with_details("(((")
        assert result["is_balanced"] is False
        assert len(result["unmatched_brackets"]) > 0
        assert result["bracket_count"]["("] == 3

    def test_validate_with_details_bracket_counts(self, validator):
        """Test bracket counting in detailed validation."""
        result = validator.validate_with_details("()[]{}")
        counts = result["bracket_count"]
        assert counts["("] == 1
        assert counts[")"] == 1
        assert counts["["] == 1
        assert counts["]"] == 1
        assert counts["{"] == 1
        assert counts["}"] == 1

    def test_generate_report(self, validator, temp_dir):
        """Test report generation."""
        result = validator.validate_with_details("()[]{}")
        report_path = temp_dir / "report.txt"
        report = validator.generate_report(
            "()[]{}", result, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "BALANCED PARENTHESES VALIDATION REPORT" in report
        assert "STACK OPERATIONS USED" in report
        assert "()[]{}" in report

    def test_generate_report_unbalanced(self, validator):
        """Test report generation for unbalanced expression."""
        result = validator.validate_with_details("(((")
        report = validator.generate_report("(((", result)

        assert "NOT BALANCED" in report
        assert "(((" in report

    def test_stack_behavior_lifo(self, validator):
        """Test that stack follows LIFO behavior."""
        # This test verifies the stack implementation indirectly
        # by checking that nested brackets are handled correctly
        assert validator.is_balanced("([{()}])") is True
        assert validator.is_balanced("([{()}])") is True

    def test_multiple_nested_levels(self, validator):
        """Test validation with multiple nested levels."""
        assert validator.is_balanced("((([{}])))") is True
        assert validator.is_balanced("([{<>}])") is True

    def test_real_world_examples(self, validator):
        """Test validation with real-world code-like examples."""
        assert validator.is_balanced("function() { return [1, 2]; }") is True
        assert validator.is_balanced("if (x > 0) { return true; }") is True
        assert validator.is_balanced("array[0] = { key: 'value' }") is True

    def test_edge_cases(self, validator):
        """Test edge cases."""
        assert validator.is_balanced("a") is True
        assert validator.is_balanced("a(b)c") is True
        assert validator.is_balanced("a(b)c(d)e") is True
        assert validator.is_balanced("a(b") is False
        assert validator.is_balanced("a)b") is False
