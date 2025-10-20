"""
# Calculator Class

**Tags**: #type/code-file #domain/ui #layer/interface #layer/application #pattern/strategy #pattern/strategy/delegation

## Purpose
Provides user interface for calculator operations.
Handles input validation and delegates computation to operations.

## Related Documentation
- Concept: [[calculator-interface|Calculator Interface]]
- Concept: [[user-input-validation|User Input Validation]]
- Pattern: [[single-responsibility|Single Responsibility Principle]]

## Dependencies
- [[operations.py|Operations Module]]
"""
from typing import Optional
import operations


class Calculator:  # ^Calculator
    """
    A simple calculator that performs basic arithmetic operations.

    Implements: [[calculator-interface|Calculator Interface]]
    """

    def calculate(self, a: float, b: float, operation: str) -> float:  # ^Calculator-calculate
        """
        Perform a calculation using the specified operation.

        Args:
            a: First operand
            b: Second operand
            operation: Operation symbol (+, -, *, /)

        Returns:
            Result of the calculation

        Raises:
            ValueError: If operation is invalid or calculation fails

        Related: [[operations.py|Operations Module]]
        Related: [[user-input-validation|User Input Validation]]
        """
        if operation not in operations.OPERATIONS:
            raise ValueError(f"Invalid operation: {operation}")

        operation_func = operations.OPERATIONS[operation]
        return operation_func(a, b)

    def run_interactive(self) -> None:  # ^Calculator-run_interactive
        """
        Run the calculator in interactive mode.

        Continuously prompts user for calculations until they exit.
        Implements: [[calculator-interface|Calculator Interface]]
        """
        print("Scientific Calculator - Interactive Mode")
        print("\nBasic operations: +, -, *, /")
        print("Power: ^ or ** (e.g., 2 ^ 3)")
        print("Factorial: ! (e.g., 5 !)")
        print("\nTrigonometric (radians): sin, cos, tan, asin, acos, atan")
        print("Exponential/Log: exp, ln, log10, sqrt, cbrt")
        print("Logarithm with base: log (e.g., 8 log 2)")
        print("Constants: pi, e (e.g., pi)")
        print("Angle conversion: rad (deg→rad), deg (rad→deg)")
        print("\nType 'quit' to exit\n")

        while True:
            try:
                user_input = input("Enter calculation (e.g., 5 + 3): ").strip()

                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break

                # Parse input
                result = self._parse_and_calculate(user_input)
                if result is not None:
                    print(f"Result: {result}\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")

    def _parse_and_calculate(self, expression: str) -> Optional[float]:  # ^Calculator-_parse_and_calculate
        """
        Parse a string expression and calculate the result.

        Related: [[user-input-validation|User Input Validation]]
        """
        parts = expression.split()

        # Check for unary operation (e.g., "5 !")
        if len(parts) == 2:
            try:
                n = float(parts[0])
                operation = parts[1]
            except ValueError:
                raise ValueError("Invalid number provided")

            if operation in operations.UNARY_OPERATIONS:
                operation_func = operations.UNARY_OPERATIONS[operation]
                return operation_func(n)
            else:
                raise ValueError(f"Invalid unary operation: {operation}")

        # Check for binary operation (e.g., "5 + 3")
        if len(parts) != 3:
            raise ValueError("Invalid format. Use: number operation number (or: number unary_operation)")

        try:
            a = float(parts[0])
            operation = parts[1]
            b = float(parts[2])
        except ValueError:
            raise ValueError("Invalid numbers provided")

        return self.calculate(a, b, operation)
