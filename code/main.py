"""
# Main Entry Point

**Tags**: #type/code-file #domain/ui #layer/entry-point

## Purpose
Application entry point for the calculator.
Initializes and launches the calculator interface.

## Related Documentation
- Concept: [[calculator-interface|Calculator Interface]]

## Dependencies
- [[calculator.py|Calculator Class]]
"""
from calculator import Calculator


def main():  # ^main
    """
    Main entry point for the calculator application.

    Creates a calculator instance and runs it in interactive mode.
    Related: [[calculator.py|Calculator Class]]
    """
    calc = Calculator()
    calc.run_interactive()


if __name__ == "__main__":
    main()
