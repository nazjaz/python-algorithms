"""Stack Data Structure - Implementation and expression evaluation.

This module provides a stack data structure implementation with push, pop, peek
operations and demonstrates its use in expression evaluation (postfix/infix).
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Any, List, Optional

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Stack:
    """Stack data structure implementation using list."""

    def __init__(self) -> None:
        """Initialize empty stack."""
        self._items: List[Any] = []
        logger.debug("Stack initialized")

    def push(self, item: Any) -> None:
        """Push item onto stack.

        Args:
            item: Item to push onto stack.
        """
        self._items.append(item)
        logger.debug(f"Pushed {item} onto stack. Stack: {self._items}")

    def pop(self) -> Any:
        """Pop item from stack.

        Returns:
            Item from top of stack.

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            logger.error("Attempted to pop from empty stack")
            raise IndexError("Stack is empty")

        item = self._items.pop()
        logger.debug(f"Popped {item} from stack. Stack: {self._items}")
        return item

    def peek(self) -> Any:
        """Peek at top item without removing it.

        Returns:
            Item at top of stack.

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            logger.error("Attempted to peek at empty stack")
            raise IndexError("Stack is empty")

        item = self._items[-1]
        logger.debug(f"Peeked at {item}. Stack: {self._items}")
        return item

    def is_empty(self) -> bool:
        """Check if stack is empty.

        Returns:
            True if stack is empty, False otherwise.
        """
        return len(self._items) == 0

    def size(self) -> int:
        """Get size of stack.

        Returns:
            Number of items in stack.
        """
        return len(self._items)

    def __str__(self) -> str:
        """String representation of stack.

        Returns:
            String representation showing stack contents.
        """
        return f"Stack({self._items})"

    def __repr__(self) -> str:
        """Representation of stack.

        Returns:
            Representation string.
        """
        return f"Stack({self._items!r})"


class ExpressionEvaluator:
    """Expression evaluator using stack data structure."""

    def __init__(self, config_path: str = "config.yaml") -> None:
        """Initialize ExpressionEvaluator with configuration.

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

    def _is_operator(self, char: str) -> bool:
        """Check if character is an operator.

        Args:
            char: Character to check.

        Returns:
            True if operator, False otherwise.
        """
        return char in ["+", "-", "*", "/", "^"]

    def _get_precedence(self, operator: str) -> int:
        """Get operator precedence.

        Args:
            operator: Operator character.

        Returns:
            Precedence value (higher = higher precedence).
        """
        precedences = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3,
        }
        return precedences.get(operator, 0)

    def _apply_operator(self, op: str, b: float, a: float) -> float:
        """Apply operator to two operands.

        Args:
            op: Operator character.
            b: Second operand (right side).
            a: First operand (left side).

        Returns:
            Result of operation.

        Raises:
            ValueError: If operator is invalid or division by zero.
        """
        logger.debug(f"Applying {op} to {a} and {b}")

        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise ValueError("Division by zero")
            result = a / b
        elif op == "^":
            result = a ** b
        else:
            raise ValueError(f"Invalid operator: {op}")

        logger.debug(f"Result: {result}")
        return result

    def evaluate_postfix(self, expression: str) -> float:
        """Evaluate postfix (Reverse Polish Notation) expression.

        Args:
            expression: Postfix expression string (space-separated tokens).

        Returns:
            Result of expression evaluation.

        Raises:
            ValueError: If expression is invalid.
        """
        logger.info(f"Evaluating postfix expression: {expression}")

        stack = Stack()
        tokens = expression.split()

        for token in tokens:
            logger.debug(f"Processing token: {token}")

            if token.replace(".", "").replace("-", "").isdigit() or (
                token.startswith("-") and token[1:].replace(".", "").isdigit()
            ):
                # Operand
                value = float(token)
                stack.push(value)
                logger.debug(f"Pushed operand {value}")

            elif self._is_operator(token):
                # Operator
                if stack.size() < 2:
                    raise ValueError(
                        f"Insufficient operands for operator {token}"
                    )

                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(token, b, a)
                stack.push(result)
                logger.debug(f"Applied {token}, pushed result {result}")

            else:
                raise ValueError(f"Invalid token: {token}")

        if stack.size() != 1:
            raise ValueError("Invalid expression: too many operands")

        result = stack.pop()
        logger.info(f"Postfix evaluation result: {result}")
        return result

    def infix_to_postfix(self, expression: str) -> str:
        """Convert infix expression to postfix notation.

        Args:
            expression: Infix expression string.

        Returns:
            Postfix expression string.

        Raises:
            ValueError: If expression is invalid.
        """
        logger.info(f"Converting infix to postfix: {expression}")

        output: List[str] = []
        operator_stack = Stack()

        i = 0
        while i < len(expression):
            char = expression[i]

            if char == " ":
                i += 1
                continue

            if char.isdigit() or char == ".":
                # Read number (including decimals)
                num = ""
                while i < len(expression) and (
                    expression[i].isdigit() or expression[i] == "."
                ):
                    num += expression[i]
                    i += 1
                output.append(num)
                i -= 1  # Adjust for loop increment
                logger.debug(f"Read number: {num}")

            elif char == "(":
                operator_stack.push(char)
                logger.debug(f"Pushed opening parenthesis")

            elif char == ")":
                while not operator_stack.is_empty() and operator_stack.peek() != "(":
                    output.append(operator_stack.pop())
                if operator_stack.is_empty():
                    raise ValueError("Mismatched parentheses")
                operator_stack.pop()  # Remove opening parenthesis
                logger.debug(f"Processed closing parenthesis")

            elif self._is_operator(char):
                while (
                    not operator_stack.is_empty()
                    and operator_stack.peek() != "("
                    and self._get_precedence(operator_stack.peek())
                    >= self._get_precedence(char)
                ):
                    output.append(operator_stack.pop())
                operator_stack.push(char)
                logger.debug(f"Pushed operator: {char}")

            else:
                raise ValueError(f"Invalid character: {char}")

            i += 1

        # Pop remaining operators
        while not operator_stack.is_empty():
            if operator_stack.peek() == "(":
                raise ValueError("Mismatched parentheses")
            output.append(operator_stack.pop())

        postfix = " ".join(output)
        logger.info(f"Postfix expression: {postfix}")
        return postfix

    def evaluate_infix(self, expression: str) -> float:
        """Evaluate infix expression by converting to postfix first.

        Args:
            expression: Infix expression string.

        Returns:
            Result of expression evaluation.

        Raises:
            ValueError: If expression is invalid.
        """
        logger.info(f"Evaluating infix expression: {expression}")

        postfix = self.infix_to_postfix(expression)
        result = self.evaluate_postfix(postfix)

        logger.info(f"Infix evaluation result: {result}")
        return result

    def generate_report(
        self, expression: str, expression_type: str, result: float,
        output_path: Optional[str] = None
    ) -> str:
        """Generate evaluation report.

        Args:
            expression: Expression that was evaluated.
            expression_type: Type of expression (postfix/infix).
            result: Evaluation result.
            output_path: Optional path to save report file.

        Returns:
            Report content as string.
        """
        report_lines = [
            "=" * 80,
            "EXPRESSION EVALUATION REPORT",
            "=" * 80,
            "",
            f"Expression type: {expression_type.upper()}",
            f"Expression: {expression}",
            f"Result: {result}",
            "",
            "STACK OPERATIONS",
            "-" * 80,
            "The evaluation used stack data structure with:",
            "  - push(): Add operand/result to stack",
            "  - pop(): Remove operand from stack for operation",
            "  - peek(): Check top of stack (used in conversion)",
            "",
            "ALGORITHM COMPLEXITY",
            "-" * 80,
            "Time Complexity: O(n) where n is number of tokens",
            "Space Complexity: O(n) for stack storage",
            "",
            "STACK DATA STRUCTURE",
            "-" * 80,
            "Stack operations used:",
            "  - push(item): O(1) - add item to top",
            "  - pop(): O(1) - remove item from top",
            "  - peek(): O(1) - view top item without removal",
            "  - is_empty(): O(1) - check if stack is empty",
            "  - size(): O(1) - get number of items",
        ]

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
        description="Stack data structure with expression evaluation"
    )
    parser.add_argument(
        "expression",
        type=str,
        nargs="?",
        default=None,
        help="Expression to evaluate",
    )
    parser.add_argument(
        "-c",
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["postfix", "infix", "auto"],
        default="auto",
        help="Expression type (default: auto-detect)",
    )
    parser.add_argument(
        "-r",
        "--report",
        help="Output path for evaluation report",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run stack operations demonstration",
    )

    args = parser.parse_args()

    try:
        if args.demo or args.expression is None:
            # Demonstrate stack operations
            print("\n=== Stack Operations Demonstration ===\n")

            stack = Stack()
            print(f"Initial stack: {stack}")
            print(f"Is empty: {stack.is_empty()}")
            print(f"Size: {stack.size()}")

            print("\n--- Pushing items ---")
            for item in [10, 20, 30, 40, 50]:
                stack.push(item)
                print(f"After pushing {item}: {stack}")

            print("\n--- Peeking ---")
            print(f"Top item (peek): {stack.peek()}")
            print(f"Stack after peek: {stack}")

            print("\n--- Popping items ---")
            while not stack.is_empty():
                item = stack.pop()
                print(f"Popped {item}, remaining: {stack}")

            print("\n--- Stack is now empty ---")
            print(f"Is empty: {stack.is_empty()}")
            print(f"Size: {stack.size()}")

        else:
            evaluator = ExpressionEvaluator(config_path=args.config)

            expression = args.expression
            expr_type = args.type

            # Auto-detect expression type
            if expr_type == "auto":
                if " " in expression and any(
                    c in expression for c in ["+", "-", "*", "/"]
                ):
                    expr_type = "postfix"
                else:
                    expr_type = "infix"

            if expr_type == "postfix":
                result = evaluator.evaluate_postfix(expression)
                print(f"\nPostfix Expression: {expression}")
                print(f"Result: {result}")
            else:
                result = evaluator.evaluate_infix(expression)
                print(f"\nInfix Expression: {expression}")
                postfix = evaluator.infix_to_postfix(expression)
                print(f"Postfix Conversion: {postfix}")
                print(f"Result: {result}")

            if args.report:
                report = evaluator.generate_report(
                    expression, expr_type, result, output_path=args.report
                )
                print(f"\nReport saved to {args.report}")

    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
