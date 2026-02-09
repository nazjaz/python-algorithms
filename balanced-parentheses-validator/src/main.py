"""Balanced Parentheses Validator - Stack-based validation.

This module provides a balanced parentheses validator that uses a stack data
structure to check if parentheses, brackets, and braces are properly balanced
in a given string. Supports multiple bracket types: (), [], {}, <>.
"""

import argparse
import logging
import logging.handlers
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class BalancedParenthesesValidator:
    """Validator for balanced parentheses using stack data structure."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize validator with configuration.

        Args:
            config_path: Path to configuration YAML file.

        Raises:
            FileNotFoundError: If config file doesn't exist.
            yaml.YAMLError: If config file is invalid YAML.
        """
        self.config = self._load_config(config_path)
        self._setup_logging()
        self._initialize_bracket_mappings()

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

    def _initialize_bracket_mappings(self) -> None:
        """Initialize bracket type mappings for validation."""
        # Opening brackets map to their corresponding closing brackets
        self.opening_brackets: Set[str] = {"(", "[", "{", "<"}
        self.closing_brackets: Set[str] = {")", "]", "}", ">"}
        self.bracket_pairs: Dict[str, str] = {
            "(": ")",
            "[": "]",
            "{": "}",
            "<": ">",
        }
        logger.debug("Bracket mappings initialized")

    def _is_opening_bracket(self, char: str) -> bool:
        """Check if character is an opening bracket.

        Args:
            char: Character to check.

        Returns:
            True if opening bracket, False otherwise.
        """
        return char in self.opening_brackets

    def _is_closing_bracket(self, char: str) -> bool:
        """Check if character is a closing bracket.

        Args:
            char: Character to check.

        Returns:
            True if closing bracket, False otherwise.
        """
        return char in self.closing_brackets

    def _matches(self, opening: str, closing: str) -> bool:
        """Check if opening and closing brackets match.

        Args:
            opening: Opening bracket character.
            closing: Closing bracket character.

        Returns:
            True if brackets match, False otherwise.
        """
        return self.bracket_pairs.get(opening) == closing

    def is_balanced(self, expression: str) -> bool:
        """Check if parentheses in expression are balanced using stack.

        Uses a stack data structure to track opening brackets. When a closing
        bracket is encountered, it checks if it matches the most recent opening
        bracket on the stack.

        Args:
            expression: String expression to validate.

        Returns:
            True if parentheses are balanced, False otherwise.

        Example:
            >>> validator = BalancedParenthesesValidator()
            >>> validator.is_balanced("()[]{}")
            True
            >>> validator.is_balanced("([)]")
            False
        """
        logger.info(f"Validating expression: {expression}")

        stack: List[str] = []

        for char in expression:
            logger.debug(f"Processing character: {char}")

            if self._is_opening_bracket(char):
                # Push opening bracket onto stack
                stack.append(char)
                logger.debug(f"Pushed {char} onto stack. Stack: {stack}")

            elif self._is_closing_bracket(char):
                # Check if stack is empty or brackets don't match
                if not stack:
                    logger.warning(
                        f"Unmatched closing bracket {char} at position "
                        f"{expression.index(char)}"
                    )
                    return False

                # Pop opening bracket from stack
                opening = stack.pop()
                logger.debug(
                    f"Popped {opening} from stack. Stack: {stack}"
                )

                # Check if brackets match
                if not self._matches(opening, char):
                    logger.warning(
                        f"Mismatched brackets: {opening} and {char}"
                    )
                    return False

        # Expression is balanced only if stack is empty
        is_balanced = len(stack) == 0

        if not is_balanced:
            logger.warning(
                f"Unmatched opening brackets remaining: {stack}"
            )

        logger.info(
            f"Expression validation result: {is_balanced}"
        )
        return is_balanced

    def get_unmatched_brackets(self, expression: str) -> List[str]:
        """Get list of unmatched brackets in expression.

        Args:
            expression: String expression to analyze.

        Returns:
            List of unmatched bracket characters. Empty list if balanced.
        """
        logger.info(f"Finding unmatched brackets in: {expression}")

        stack: List[str] = []
        unmatched: List[str] = []

        for char in expression:
            if self._is_opening_bracket(char):
                stack.append(char)
            elif self._is_closing_bracket(char):
                if not stack:
                    unmatched.append(char)
                else:
                    opening = stack.pop()
                    if not self._matches(opening, char):
                        unmatched.append(opening)
                        unmatched.append(char)

        # Add remaining opening brackets to unmatched list
        unmatched.extend(stack)

        logger.info(f"Unmatched brackets: {unmatched}")
        return unmatched

    def validate_with_details(
        self, expression: str
    ) -> Dict[str, any]:
        """Validate expression and return detailed results.

        Args:
            expression: String expression to validate.

        Returns:
            Dictionary containing:
                - is_balanced: Boolean indicating if expression is balanced
                - unmatched_brackets: List of unmatched brackets
                - bracket_count: Dictionary with counts of each bracket type
        """
        logger.info(f"Validating expression with details: {expression}")

        is_balanced_result = self.is_balanced(expression)
        unmatched = self.get_unmatched_brackets(expression)

        # Count brackets
        bracket_count: Dict[str, int] = {
            "(": expression.count("("),
            ")": expression.count(")"),
            "[": expression.count("["),
            "]": expression.count("]"),
            "{": expression.count("{"),
            "}": expression.count("}"),
            "<": expression.count("<"),
            ">": expression.count(">"),
        }

        result = {
            "is_balanced": is_balanced_result,
            "unmatched_brackets": unmatched,
            "bracket_count": bracket_count,
        }

        logger.info(f"Validation details: {result}")
        return result

    def generate_report(
        self,
        expression: str,
        result: Dict[str, any],
        output_path: Optional[str] = None,
    ) -> str:
        """Generate validation report.

        Args:
            expression: Expression that was validated.
            result: Validation result dictionary from validate_with_details.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "BALANCED PARENTHESES VALIDATION REPORT",
            "=" * 80,
            "",
            f"Expression: {expression}",
            f"Status: {'BALANCED' if result['is_balanced'] else 'NOT BALANCED'}",
            "",
            "BRACKET COUNTS",
            "-" * 80,
        ]

        bracket_count = result["bracket_count"]
        for bracket, count in bracket_count.items():
            report_lines.append(f"  {bracket}: {count}")

        report_lines.extend([
            "",
            "UNMATCHED BRACKETS",
            "-" * 80,
        ])

        if result["unmatched_brackets"]:
            report_lines.append(
                f"  {', '.join(result['unmatched_brackets'])}"
            )
        else:
            report_lines.append("  None (all brackets are matched)")

        report_lines.extend([
            "",
            "ALGORITHM DETAILS",
            "-" * 80,
            "Algorithm: Stack-based validation",
            "Time Complexity: O(n) where n is length of expression",
            "Space Complexity: O(n) for stack storage in worst case",
            "",
            "STACK OPERATIONS USED",
            "-" * 80,
            "  - push(): Add opening bracket to stack",
            "  - pop(): Remove opening bracket when closing bracket found",
            "  - is_empty(): Check if stack is empty",
            "",
            "HOW IT WORKS",
            "-" * 80,
            "1. Iterate through each character in expression",
            "2. If opening bracket: push onto stack",
            "3. If closing bracket: pop from stack and verify match",
            "4. Expression is balanced if stack is empty at end",
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
    parser = argparse.ArgumentParser(
        description="Validate balanced parentheses using stack data structure"
    )
    parser.add_argument(
        "expression",
        type=str,
        nargs="?",
        default=None,
        help="Expression to validate for balanced parentheses",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-d",
        "--details",
        action="store_true",
        help="Show detailed validation results",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for validation report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demonstration with example expressions",
    )

    args = parser.parse_args()

    try:
        validator = BalancedParenthesesValidator(config_path=args.config)

        if args.demo or args.expression is None:
            # Run demonstration
            print("\n=== Balanced Parentheses Validator Demonstration ===\n")

            examples = [
                "()",
                "()[]{}",
                "([{}])",
                "([)]",
                "((()))",
                "{[()]}",
                "<>",
                "([{<>}])",
                "(((",
                ")))",
                "([)]",
                "function() { return [1, 2, 3]; }",
            ]

            for example in examples:
                result = validator.is_balanced(example)
                status = "BALANCED" if result else "NOT BALANCED"
                print(f"Expression: {example}")
                print(f"Status: {status}")
                print()

        else:
            expression = args.expression

            if args.details:
                result = validator.validate_with_details(expression)
                print(f"\nExpression: {expression}")
                print(f"Balanced: {result['is_balanced']}")
                print(f"\nBracket Counts:")
                for bracket, count in result["bracket_count"].items():
                    print(f"  {bracket}: {count}")
                print(f"\nUnmatched Brackets: {result['unmatched_brackets']}")
            else:
                result_bool = validator.is_balanced(expression)
                status = "BALANCED" if result_bool else "NOT BALANCED"
                print(f"\nExpression: {expression}")
                print(f"Status: {status}")

            if args.report:
                if args.details:
                    result_dict = validator.validate_with_details(expression)
                else:
                    result_dict = validator.validate_with_details(expression)
                report = validator.generate_report(
                    expression, result_dict, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
