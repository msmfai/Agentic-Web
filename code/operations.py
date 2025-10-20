"""
# Operations Module

**Tags**: #type/code-file #domain/mathematics #layer/core #pattern/strategy

## Purpose
Implements arithmetic operations using the Strategy Pattern.
Each operation is a self-contained function that can be called independently.

## Related Documentation
- Concept: [[arithmetic-operations|Arithmetic Operations]]
- Pattern: [[strategy-pattern|Strategy Pattern]]
- Pattern: [[single-responsibility|Single Responsibility Principle]]

## Used By
- [[calculator.py|Calculator Class]]
"""
def add(a: float, b: float) -> float:  # ^add
    """
    Add two numbers together.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return a + b


def subtract(a: float, b: float) -> float:  # ^subtract
    """
    Subtract b from a.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return a - b


def multiply(a: float, b: float) -> float:  # ^multiply
    """
    Multiply two numbers.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return a * b


def divide(a: float, b: float) -> float:  # ^divide
    """
    Divide a by b.

    Raises ValueError if b is zero.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def factorial(n: float) -> float:  # ^factorial
    """
    Calculate the factorial of n.

    Raises ValueError if n is negative or not an integer.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n != int(n):
        raise ValueError("Factorial is only defined for integers")

    n = int(n)
    result = 1
    for i in range(2, n + 1):
        result *= i
    return float(result)


# Operation registry mapping operation names to functions
# This demonstrates the Strategy Pattern
OPERATIONS = {  # ^OPERATIONS
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

# Unary operations (single operand)
UNARY_OPERATIONS = {  # ^UNARY_OPERATIONS
    '!': factorial,
}
