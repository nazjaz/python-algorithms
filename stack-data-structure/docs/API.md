# API Documentation

## Stack Class

The main class for stack data structure implementation.

### Methods

#### `__init__()`

Initialize empty stack.

**Example:**
```python
stack = Stack()
```

#### `push(item: Any) -> None`

Push item onto stack.

**Parameters:**
- `item` (Any): Item to push onto stack.

**Time Complexity:** O(1)

**Example:**
```python
stack = Stack()
stack.push(10)
stack.push(20)
```

#### `pop() -> Any`

Pop item from stack.

**Returns:**
- `Any`: Item from top of stack.

**Raises:**
- `IndexError`: If stack is empty.

**Time Complexity:** O(1)

**Example:**
```python
stack = Stack()
stack.push(10)
stack.push(20)
item = stack.pop()  # Returns 20
```

#### `peek() -> Any`

Peek at top item without removing it.

**Returns:**
- `Any`: Item at top of stack.

**Raises:**
- `IndexError`: If stack is empty.

**Time Complexity:** O(1)

**Example:**
```python
stack = Stack()
stack.push(10)
stack.push(20)
item = stack.peek()  # Returns 20, stack unchanged
```

#### `is_empty() -> bool`

Check if stack is empty.

**Returns:**
- `bool`: True if stack is empty, False otherwise.

**Time Complexity:** O(1)

**Example:**
```python
stack = Stack()
if stack.is_empty():
    print("Stack is empty")
```

#### `size() -> int`

Get size of stack.

**Returns:**
- `int`: Number of items in stack.

**Time Complexity:** O(1)

**Example:**
```python
stack = Stack()
stack.push(10)
stack.push(20)
print(stack.size())  # 2
```

## ExpressionEvaluator Class

The main class for evaluating expressions using stack data structure.

### Methods

#### `__init__(config_path: str = "config.yaml")`

Initialize the ExpressionEvaluator with configuration.

**Parameters:**
- `config_path` (str): Path to configuration YAML file. Defaults to "config.yaml".

**Raises:**
- `FileNotFoundError`: If config file doesn't exist.
- `yaml.YAMLError`: If config file is invalid YAML.

#### `evaluate_postfix(expression: str) -> float`

Evaluate postfix (Reverse Polish Notation) expression.

**Parameters:**
- `expression` (str): Postfix expression string (space-separated tokens).

**Returns:**
- `float`: Result of expression evaluation.

**Raises:**
- `ValueError`: If expression is invalid.

**Time Complexity:** O(n) where n is number of tokens
**Space Complexity:** O(n) for stack storage

**Example:**
```python
evaluator = ExpressionEvaluator()
result = evaluator.evaluate_postfix("3 4 + 2 *")
print(result)  # 14.0
```

#### `evaluate_infix(expression: str) -> float`

Evaluate infix expression by converting to postfix first.

**Parameters:**
- `expression` (str): Infix expression string.

**Returns:**
- `float`: Result of expression evaluation.

**Raises:**
- `ValueError`: If expression is invalid.

**Time Complexity:** O(n) where n is number of tokens
**Space Complexity:** O(n) for stack storage

**Example:**
```python
evaluator = ExpressionEvaluator()
result = evaluator.evaluate_infix("(3 + 4) * 2")
print(result)  # 14.0
```

#### `infix_to_postfix(expression: str) -> str`

Convert infix expression to postfix notation.

**Parameters:**
- `expression` (str): Infix expression string.

**Returns:**
- `str`: Postfix expression string.

**Raises:**
- `ValueError`: If expression is invalid.

**Time Complexity:** O(n) where n is length of expression
**Space Complexity:** O(n) for stack storage

**Example:**
```python
evaluator = ExpressionEvaluator()
postfix = evaluator.infix_to_postfix("(3 + 4) * 2")
print(postfix)  # "3 4 + 2 *"
```

#### `generate_report(expression: str, expression_type: str, result: float, output_path: Optional[str] = None) -> str`

Generate evaluation report.

**Parameters:**
- `expression` (str): Expression that was evaluated.
- `expression_type` (str): Type of expression (postfix/infix).
- `result` (float): Evaluation result.
- `output_path` (Optional[str]): Optional path to save report file.

**Returns:**
- `str`: Report content as string.

**Example:**
```python
evaluator = ExpressionEvaluator()
result = evaluator.evaluate_infix("3 + 4")
report = evaluator.generate_report("3 + 4", "infix", result, output_path="report.txt")
```

### Example Usage

```python
from src.main import Stack, ExpressionEvaluator

# Stack operations
stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)
print(stack.peek())  # 30
print(stack.pop())   # 30
print(stack.size())  # 2

# Expression evaluation
evaluator = ExpressionEvaluator()

# Postfix evaluation
result = evaluator.evaluate_postfix("3 4 + 2 *")
print(result)  # 14.0

# Infix evaluation
result = evaluator.evaluate_infix("(3 + 4) * 2")
print(result)  # 14.0

# Infix to postfix conversion
postfix = evaluator.infix_to_postfix("3 + 4 * 2")
print(postfix)  # "3 4 2 * +"
```

### Stack Data Structure

**Characteristics:**
- LIFO (Last In, First Out) data structure
- Implemented using Python list
- All operations are O(1) time complexity
- O(n) space complexity for n items

**Operations:**
- `push(item)`: Add item to top - O(1)
- `pop()`: Remove and return top item - O(1)
- `peek()`: View top item without removal - O(1)
- `is_empty()`: Check if empty - O(1)
- `size()`: Get number of items - O(1)

### Expression Evaluation

**Postfix Evaluation Algorithm:**
1. Read tokens from left to right
2. If operand, push onto stack
3. If operator, pop two operands, apply operator, push result
4. Final result is on stack

**Infix to Postfix Conversion Algorithm:**
1. Use stack to handle operator precedence
2. Process tokens and operators according to precedence
3. Handle parentheses correctly
4. Output postfix expression

**Supported Operators:**
- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `^`: Exponentiation

**Operator Precedence:**
1. `^` (highest - precedence 3)
2. `*`, `/` (precedence 2)
3. `+`, `-` (lowest - precedence 1)

### Error Handling

**Stack Errors:**
- `IndexError`: Attempted to pop or peek from empty stack

**Expression Errors:**
- `ValueError`: Invalid expression syntax
- `ValueError`: Division by zero
- `ValueError`: Mismatched parentheses
- `ValueError`: Insufficient operands for operator

### Performance Notes

- Stack operations are all O(1) time complexity
- Expression evaluation is O(n) where n is number of tokens
- Postfix evaluation is simpler and faster than infix
- Stack provides efficient LIFO access pattern
- All operations are optimized for performance

### Edge Cases

- Empty stack: All operations check for empty stack
- Single operand: Handled correctly in expressions
- Negative numbers: Supported in expressions
- Decimal numbers: Supported in expressions
- Parentheses: Handled with proper precedence
- Division by zero: Detected and raises error
