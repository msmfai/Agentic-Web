"""
# Calculator Class

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/calculator.py #domain/ui #domain/plugin-system #layer/interface #layer/application #pattern/strategy #pattern/strategy/delegation

## Purpose
Provides user interface for calculator operations.
Handles input validation and delegates computation to operations.
Integrates with plugin system to support extensible operations.

## Related Documentation
- Concept: [[calculator-interface|Calculator Interface]]
- Concept: [[user-input-validation|User Input Validation]]
- Pattern: [[single-responsibility|Single Responsibility Principle]]
- Pattern: [[obsidian/plugin-architecture.md|Plugin Architecture]]

## Dependencies
- [[code/operations.py|Operations Module]]
- [[code/plugin_system.py|Plugin System]]
"""
from typing import Optional, Dict, Callable
import operations
from plugin_system import PluginSystem


class Calculator:  # ^Calculator
    """
    A simple calculator that performs basic arithmetic operations.
    Supports extensibility through the plugin system.

    Implements: [[calculator-interface|Calculator Interface]]
    Integrates: [[code/plugin_system.py|Plugin System]]
    """

    def __init__(self):  # ^Calculator-__init__
        """Initialize calculator with plugin system."""
        self.plugin_system = PluginSystem()
        self.plugin_system.auto_discover_plugins()

    def _get_all_operations(self) -> Dict[str, Callable]:  # ^Calculator-_get_all_operations
        """
        Get all available operations (built-in + plugin operations).

        Related: [[code/plugin_system.py|Plugin System]]
        Related: [[code/operations.py|Operations Module]]
        """
        all_ops = operations.OPERATIONS.copy()
        plugin_ops = self.plugin_system.get_all_operations()
        all_ops.update(plugin_ops)
        return all_ops

    def _get_all_unary_operations(self) -> Dict[str, Callable]:  # ^Calculator-_get_all_unary_operations
        """
        Get all available unary operations (built-in + plugin unary operations).

        Related: [[code/plugin_system.py|Plugin System]]
        Related: [[code/operations.py|Operations Module]]
        """
        return operations.UNARY_OPERATIONS.copy()

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

        Related: [[code/operations.py|Operations Module]]
        Related: [[user-input-validation|User Input Validation]]
        Related: [[code/plugin_system.py|Plugin System]]
        """
        all_operations = self._get_all_operations()

        if operation not in all_operations:
            raise ValueError(f"Invalid operation: {operation}")

        operation_func = all_operations[operation]
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
        print("\nPlugin commands:")
        print("  !plugins - List loaded plugins")
        print("  !reload <plugin> - Reload a plugin")
        print("  !enable <plugin> - Enable a plugin")
        print("  !disable <plugin> - Disable a plugin")
        print("\nType 'quit' to exit\n")

        while True:
            try:
                user_input = input("Enter calculation (e.g., 5 + 3): ").strip()

                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break

                # Check for plugin commands
                if user_input.startswith('!'):
                    self._handle_plugin_command(user_input)
                    continue

                # Parse input
                result = self._parse_and_calculate(user_input)
                if result is not None:
                    print(f"Result: {result}\n")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}\n")

    def _handle_plugin_command(self, command: str) -> None:  # ^Calculator-_handle_plugin_command
        """
        Handle plugin management commands.

        Commands:
        - !plugins: List all loaded plugins
        - !reload <plugin>: Reload a specific plugin
        - !enable <plugin>: Enable a plugin
        - !disable <plugin>: Disable a plugin

        Related: [[code/plugin_system.py|Plugin System]]
        """
        parts = command.split()
        cmd = parts[0].lower()

        if cmd == '!plugins':
            if not self.plugin_system.plugins:
                print("No plugins loaded.\n")
            else:
                print("Loaded plugins:")
                for name, metadata in self.plugin_system.plugins.items():
                    status = "enabled" if metadata.enabled else "disabled"
                    ops = list(metadata.operations.keys())
                    print(f"  - {name} [{status}]: {', '.join(ops)}")
                print()

        elif cmd == '!reload':
            if len(parts) < 2:
                print("Usage: !reload <plugin_name>\n")
                return
            plugin_name = parts[1]
            if self.plugin_system.reload_plugin(plugin_name):
                print(f"Plugin '{plugin_name}' reloaded successfully.\n")
            else:
                print(f"Failed to reload plugin '{plugin_name}'.\n")

        elif cmd == '!enable':
            if len(parts) < 2:
                print("Usage: !enable <plugin_name>\n")
                return
            plugin_name = parts[1]
            if plugin_name in self.plugin_system.plugins:
                self.plugin_system.plugins[plugin_name].enabled = True
                print(f"Plugin '{plugin_name}' enabled.\n")
            else:
                print(f"Plugin '{plugin_name}' not found.\n")

        elif cmd == '!disable':
            if len(parts) < 2:
                print("Usage: !disable <plugin_name>\n")
                return
            plugin_name = parts[1]
            if plugin_name in self.plugin_system.plugins:
                self.plugin_system.plugins[plugin_name].enabled = False
                print(f"Plugin '{plugin_name}' disabled.\n")
            else:
                print(f"Plugin '{plugin_name}' not found.\n")

        else:
            print(f"Unknown command: {cmd}\n")
            print("Available commands: !plugins, !reload, !enable, !disable\n")

    def _parse_and_calculate(self, expression: str) -> Optional[float]:  # ^Calculator-_parse_and_calculate
        """
        Parse a string expression and calculate the result.

        Related: [[user-input-validation|User Input Validation]]
        """
        parts = expression.split()
        all_unary = self._get_all_unary_operations()

        # Check for unary operation (e.g., "5 !")
        if len(parts) == 2:
            try:
                n = float(parts[0])
                operation = parts[1]
            except ValueError:
                raise ValueError("Invalid number provided")

            if operation in all_unary:
                operation_func = all_unary[operation]
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
