"""
# Operations Module

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/operations.py #domain/mathematics #layer/core #layer/domain #pattern/strategy #pattern/strategy/function-registry #category/mixed-concerns

## Purpose
Implements arithmetic and scientific operations using the Strategy Pattern.
Each operation is a self-contained function that can be called independently.

## Related Documentation
- Concept: [[arithmetic-operations|Arithmetic Operations]]
- Pattern: [[strategy-pattern|Strategy Pattern]]
- Pattern: [[single-responsibility|Single Responsibility Principle]]

## Used By
- [[code/calculator.py|Calculator Class]]
"""
import math


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


# Scientific functions - Trigonometric
def sin(x: float) -> float:  # ^sin
    """
    Calculate sine of x (x in radians).

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.sin(x)


def cos(x: float) -> float:  # ^cos
    """
    Calculate cosine of x (x in radians).

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.cos(x)


def tan(x: float) -> float:  # ^tan
    """
    Calculate tangent of x (x in radians).

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.tan(x)


def asin(x: float) -> float:  # ^asin
    """
    Calculate arcsine of x, returns result in radians.

    Raises ValueError if x is not in range [-1, 1].
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if x < -1 or x > 1:
        raise ValueError("asin domain error: x must be in range [-1, 1]")
    return math.asin(x)


def acos(x: float) -> float:  # ^acos
    """
    Calculate arccosine of x, returns result in radians.

    Raises ValueError if x is not in range [-1, 1].
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if x < -1 or x > 1:
        raise ValueError("acos domain error: x must be in range [-1, 1]")
    return math.acos(x)


def atan(x: float) -> float:  # ^atan
    """
    Calculate arctangent of x, returns result in radians.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.atan(x)


# Scientific functions - Exponential and Logarithmic
def exp(x: float) -> float:  # ^exp
    """
    Calculate e raised to the power of x.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.exp(x)


def ln(x: float) -> float:  # ^ln
    """
    Calculate natural logarithm (base e) of x.

    Raises ValueError if x <= 0.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if x <= 0:
        raise ValueError("ln domain error: x must be positive")
    return math.log(x)


def log10(x: float) -> float:  # ^log10
    """
    Calculate base-10 logarithm of x.

    Raises ValueError if x <= 0.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if x <= 0:
        raise ValueError("log10 domain error: x must be positive")
    return math.log10(x)


def log(x: float, base: float) -> float:  # ^log
    """
    Calculate logarithm of x with custom base.

    Raises ValueError if x <= 0 or base <= 0 or base == 1.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if x <= 0:
        raise ValueError("log domain error: x must be positive")
    if base <= 0 or base == 1:
        raise ValueError("log domain error: base must be positive and not equal to 1")
    return math.log(x, base)


# Scientific functions - Power operations
def power(a: float, b: float) -> float:  # ^power
    """
    Calculate a raised to the power of b.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.pow(a, b)


def sqrt(x: float) -> float:  # ^sqrt
    """
    Calculate square root of x.

    Raises ValueError if x < 0.
    Related: [[arithmetic-operations|Arithmetic Operations]]
    Related: [[user-input-validation|User Input Validation]]
    """
    if x < 0:
        raise ValueError("sqrt domain error: x must be non-negative")
    return math.sqrt(x)


def cbrt(x: float) -> float:  # ^cbrt
    """
    Calculate cube root of x.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.copysign(abs(x) ** (1/3), x)


# Angle conversion
def deg_to_rad(degrees: float) -> float:  # ^deg_to_rad
    """
    Convert degrees to radians.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.radians(degrees)


def rad_to_deg(radians: float) -> float:  # ^rad_to_deg
    """
    Convert radians to degrees.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.degrees(radians)


# Constants (implemented as unary operations)
def pi_const(_: float = 0) -> float:  # ^pi_const
    """
    Return the value of pi.

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.pi


def e_const(_: float = 0) -> float:  # ^e_const
    """
    Return the value of e (Euler's number).

    Related: [[arithmetic-operations|Arithmetic Operations]]
    """
    return math.e


# Update UNARY_OPERATIONS to include scientific functions
UNARY_OPERATIONS['sin'] = sin
UNARY_OPERATIONS['cos'] = cos
UNARY_OPERATIONS['tan'] = tan
UNARY_OPERATIONS['asin'] = asin
UNARY_OPERATIONS['acos'] = acos
UNARY_OPERATIONS['atan'] = atan
UNARY_OPERATIONS['exp'] = exp
UNARY_OPERATIONS['ln'] = ln
UNARY_OPERATIONS['log10'] = log10
UNARY_OPERATIONS['sqrt'] = sqrt
UNARY_OPERATIONS['cbrt'] = cbrt
UNARY_OPERATIONS['pi'] = pi_const
UNARY_OPERATIONS['e'] = e_const
UNARY_OPERATIONS['deg'] = rad_to_deg  # convert radians to degrees
UNARY_OPERATIONS['rad'] = deg_to_rad  # convert degrees to radians

# Update OPERATIONS to include binary scientific functions
OPERATIONS['^'] = power
OPERATIONS['**'] = power
OPERATIONS['log'] = log
