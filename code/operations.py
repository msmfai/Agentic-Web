"""---
tags: [type/code-file, domain/FIXME, layer/FIXME]
---

---
tags: [type/code-file, domain/mathematics, layer/core, pattern/strategy]
---

# Operations Module

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
def add(a: float, b: float) -> float:
    """
    Add two numbers together.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """
    Subtract b from a.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return a - b


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return a * b


def divide(a: float, b: float) -> float:
    """
    Divide a by b.

    Raises ValueError if b is zero.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# Operation registry mapping operation names to functions
# This demonstrates the Strategy Pattern
OPERATIONS = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}
