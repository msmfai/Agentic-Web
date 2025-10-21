"""
# Calculator Class Tests

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/test_calculator.py #domain/testing #domain/testing/integration #layer/test #category/unit-test #domain/ui

## Purpose
Unit tests for the Calculator class.
Tests the calculator interface, input parsing, and integration with operations.

## Related Documentation
- Tests: [[code/calculator.py|Calculator Class]]
- Concept: [[calculator-interface|Calculator Interface]]
- Concept: [[user-input-validation|User Input Validation]]
- Pattern: [[strategy-pattern|Strategy Pattern]]

## Dependencies
- [[code/calculator.py|Calculator Class]]
- [[code/operations.py|Operations Module]]
"""
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import math
from calculator import Calculator


class TestCalculatorBasic(unittest.TestCase):  # ^TestCalculatorBasic
    """
    Test basic calculator functionality.

    Related: [[code/calculator.py|Calculator Class]]
    """

    def setUp(self):  # ^TestCalculatorBasic-setUp
        """Set up test calculator instance."""
        self.calc = Calculator()

    def test_basic_addition(self):  # ^TestCalculatorBasic-test_basic_addition
        """Test basic addition through calculator."""
        result = self.calc.calculate(2, 3, '+')
        self.assertEqual(result, 5)

    def test_basic_subtraction(self):  # ^TestCalculatorBasic-test_basic_subtraction
        """Test basic subtraction through calculator."""
        result = self.calc.calculate(10, 3, '-')
        self.assertEqual(result, 7)

    def test_basic_multiplication(self):  # ^TestCalculatorBasic-test_basic_multiplication
        """Test basic multiplication through calculator."""
        result = self.calc.calculate(4, 5, '*')
        self.assertEqual(result, 20)

    def test_basic_division(self):  # ^TestCalculatorBasic-test_basic_division
        """Test basic division through calculator."""
        result = self.calc.calculate(15, 3, '/')
        self.assertEqual(result, 5)

    def test_power_operations(self):  # ^TestCalculatorBasic-test_power_operations
        """Test power operations through calculator."""
        result = self.calc.calculate(2, 8, '^')
        self.assertAlmostEqual(result, 256)

        result = self.calc.calculate(2, 8, '**')
        self.assertAlmostEqual(result, 256)

    def test_logarithm_with_base(self):  # ^TestCalculatorBasic-test_logarithm_with_base
        """Test logarithm with custom base through calculator."""
        result = self.calc.calculate(8, 2, 'log')
        self.assertAlmostEqual(result, 3)

    def test_invalid_operation(self):  # ^TestCalculatorBasic-test_invalid_operation
        """Test that invalid operation raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc.calculate(5, 3, '%')
        self.assertIn("Invalid operation", str(context.exception))

    def test_division_by_zero(self):  # ^TestCalculatorBasic-test_division_by_zero
        """Test that division by zero is handled properly."""
        with self.assertRaises(ValueError) as context:
            self.calc.calculate(10, 0, '/')
        self.assertIn("Cannot divide by zero", str(context.exception))


class TestCalculatorParsing(unittest.TestCase):  # ^TestCalculatorParsing
    """
    Test calculator input parsing functionality.

    Related: [[code/calculator.py|Calculator Class]]
    Related: [[user-input-validation|User Input Validation]]
    """

    def setUp(self):  # ^TestCalculatorParsing-setUp
        """Set up test calculator instance."""
        self.calc = Calculator()

    def test_parse_binary_operation(self):  # ^TestCalculatorParsing-test_parse_binary_operation
        """Test parsing of binary operations."""
        result = self.calc._parse_and_calculate("5 + 3")
        self.assertEqual(result, 8)

        result = self.calc._parse_and_calculate("10 - 4")
        self.assertEqual(result, 6)

        result = self.calc._parse_and_calculate("6 * 7")
        self.assertEqual(result, 42)

        result = self.calc._parse_and_calculate("20 / 4")
        self.assertEqual(result, 5)

    def test_parse_power_operation(self):  # ^TestCalculatorParsing-test_parse_power_operation
        """Test parsing of power operations."""
        result = self.calc._parse_and_calculate("2 ^ 10")
        self.assertAlmostEqual(result, 1024)

        result = self.calc._parse_and_calculate("3 ** 4")
        self.assertAlmostEqual(result, 81)

    def test_parse_logarithm(self):  # ^TestCalculatorParsing-test_parse_logarithm
        """Test parsing of logarithm with custom base."""
        result = self.calc._parse_and_calculate("16 log 2")
        self.assertAlmostEqual(result, 4)

    def test_parse_unary_operation(self):  # ^TestCalculatorParsing-test_parse_unary_operation
        """Test parsing of unary operations."""
        result = self.calc._parse_and_calculate("5 !")
        self.assertEqual(result, 120)

        result = self.calc._parse_and_calculate("16 sqrt")
        self.assertAlmostEqual(result, 4)

        result = self.calc._parse_and_calculate("27 cbrt")
        self.assertAlmostEqual(result, 3)

    def test_parse_trigonometric(self):  # ^TestCalculatorParsing-test_parse_trigonometric
        """Test parsing of trigonometric functions."""
        result = self.calc._parse_and_calculate("0 sin")
        self.assertAlmostEqual(result, 0)

        result = self.calc._parse_and_calculate("0 cos")
        self.assertAlmostEqual(result, 1)

        result = self.calc._parse_and_calculate("1 asin")
        self.assertAlmostEqual(result, math.pi / 2)

    def test_parse_exponential_logarithmic(self):  # ^TestCalculatorParsing-test_parse_exponential_logarithmic
        """Test parsing of exponential and logarithmic functions."""
        result = self.calc._parse_and_calculate("0 exp")
        self.assertAlmostEqual(result, 1)

        result = self.calc._parse_and_calculate("1 ln")
        self.assertAlmostEqual(result, 0)

        result = self.calc._parse_and_calculate("100 log10")
        self.assertAlmostEqual(result, 2)

    def test_parse_constants(self):  # ^TestCalculatorParsing-test_parse_constants
        """Test parsing of mathematical constants."""
        result = self.calc._parse_and_calculate("0 pi")
        self.assertAlmostEqual(result, math.pi)

        result = self.calc._parse_and_calculate("0 e")
        self.assertAlmostEqual(result, math.e)

    def test_parse_angle_conversion(self):  # ^TestCalculatorParsing-test_parse_angle_conversion
        """Test parsing of angle conversion functions."""
        result = self.calc._parse_and_calculate("90 rad")
        self.assertAlmostEqual(result, math.pi / 2)

        result = self.calc._parse_and_calculate(f"{math.pi} deg")
        self.assertAlmostEqual(result, 180)

    def test_parse_invalid_format(self):  # ^TestCalculatorParsing-test_parse_invalid_format
        """Test that invalid format raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc._parse_and_calculate("5 + 3 + 2")
        self.assertIn("Invalid format", str(context.exception))

        with self.assertRaises(ValueError):
            self.calc._parse_and_calculate("5 +")

        with self.assertRaises(ValueError):
            self.calc._parse_and_calculate("+ 5")

    def test_parse_invalid_numbers(self):  # ^TestCalculatorParsing-test_parse_invalid_numbers
        """Test that invalid numbers raise ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc._parse_and_calculate("abc + 5")
        self.assertIn("Invalid number", str(context.exception))

        with self.assertRaises(ValueError):
            self.calc._parse_and_calculate("5 + xyz")

    def test_parse_invalid_unary_operation(self):  # ^TestCalculatorParsing-test_parse_invalid_unary_operation
        """Test that invalid unary operation raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.calc._parse_and_calculate("5 unknown")
        self.assertIn("Invalid unary operation", str(context.exception))

    def test_parse_with_floats(self):  # ^TestCalculatorParsing-test_parse_with_floats
        """Test parsing with floating point numbers."""
        result = self.calc._parse_and_calculate("3.14 + 2.86")
        self.assertAlmostEqual(result, 6.0)

        result = self.calc._parse_and_calculate("10.5 * 2")
        self.assertAlmostEqual(result, 21.0)

    def test_parse_with_negative_numbers(self):  # ^TestCalculatorParsing-test_parse_with_negative_numbers
        """Test parsing with negative numbers."""
        result = self.calc._parse_and_calculate("-5 + 3")
        self.assertEqual(result, -2)

        result = self.calc._parse_and_calculate("10 + -5")
        self.assertEqual(result, 5)


class TestCalculatorInteractive(unittest.TestCase):  # ^TestCalculatorInteractive
    """
    Test calculator interactive mode.

    Related: [[code/calculator.py|Calculator Class]]
    Related: [[calculator-interface|Calculator Interface]]
    """

    def setUp(self):  # ^TestCalculatorInteractive-setUp
        """Set up test calculator instance."""
        self.calc = Calculator()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_quit(self, mock_print, mock_input):  # ^TestCalculatorInteractive-test_interactive_quit
        """Test that 'quit' command exits interactive mode."""
        mock_input.return_value = 'quit'
        self.calc.run_interactive()

        # Verify goodbye message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Goodbye' in str(call) for call in print_calls))

    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_calculation(self, mock_print, mock_input):  # ^TestCalculatorInteractive-test_interactive_calculation
        """Test interactive mode performs calculations."""
        mock_input.side_effect = ['5 + 3', 'quit']
        self.calc.run_interactive()

        # Verify result was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Result: 8' in str(call) for call in print_calls))

    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_error_handling(self, mock_print, mock_input):  # ^TestCalculatorInteractive-test_interactive_error_handling
        """Test interactive mode handles errors gracefully."""
        mock_input.side_effect = ['5 / 0', 'quit']
        self.calc.run_interactive()

        # Verify error message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Error' in str(call) for call in print_calls))

    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_keyboard_interrupt(self, mock_print, mock_input):  # ^TestCalculatorInteractive-test_interactive_keyboard_interrupt
        """Test that KeyboardInterrupt exits gracefully."""
        mock_input.side_effect = KeyboardInterrupt()
        self.calc.run_interactive()

        # Verify goodbye message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Goodbye' in str(call) for call in print_calls))

    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_multiple_calculations(self, mock_print, mock_input):  # ^TestCalculatorInteractive-test_interactive_multiple_calculations
        """Test interactive mode handles multiple calculations."""
        mock_input.side_effect = ['5 + 3', '10 - 2', '4 * 3', 'quit']
        self.calc.run_interactive()

        # Verify all results were printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        self.assertTrue(any('Result: 8' in str(call) for call in print_calls))
        self.assertTrue(any('Result: 8' in str(call) for call in print_calls))  # 10 - 2
        self.assertTrue(any('Result: 12' in str(call) for call in print_calls))


class TestCalculatorIntegration(unittest.TestCase):  # ^TestCalculatorIntegration
    """
    Integration tests combining calculator and operations.

    Related: [[code/calculator.py|Calculator Class]]
    Related: [[code/operations.py|Operations Module]]
    Related: [[strategy-pattern|Strategy Pattern]]
    """

    def setUp(self):  # ^TestCalculatorIntegration-setUp
        """Set up test calculator instance."""
        self.calc = Calculator()

    def test_complex_scientific_calculation(self):  # ^TestCalculatorIntegration-test_complex_scientific_calculation
        """Test complex scientific calculations through the calculator."""
        # sin(π/2) should equal 1
        result = self.calc._parse_and_calculate(f"{math.pi / 2} sin")
        self.assertAlmostEqual(result, 1)

        # log₂(1024) should equal 10
        result = self.calc._parse_and_calculate("1024 log 2")
        self.assertAlmostEqual(result, 10)

        # √(e^2) should equal e
        exp_result = self.calc._parse_and_calculate("2 exp")
        sqrt_of_exp = math.sqrt(exp_result)
        self.assertAlmostEqual(sqrt_of_exp, math.e)

    def test_factorial_then_sqrt(self):  # ^TestCalculatorIntegration-test_factorial_then_sqrt
        """Test that we can compute factorial then take square root."""
        # 5! = 120
        factorial_result = self.calc._parse_and_calculate("5 !")
        self.assertEqual(factorial_result, 120)

        # √120 ≈ 10.954
        sqrt_result = math.sqrt(factorial_result)
        self.assertAlmostEqual(sqrt_result, 10.954451150103322)

    def test_power_and_logarithm_inverse(self):  # ^TestCalculatorIntegration-test_power_and_logarithm_inverse
        """Test that power and logarithm are inverse operations."""
        # 2^8 = 256
        power_result = self.calc._parse_and_calculate("2 ^ 8")
        self.assertAlmostEqual(power_result, 256)

        # log₂(256) = 8
        log_result = self.calc.calculate(power_result, 2, 'log')
        self.assertAlmostEqual(log_result, 8)

    def test_angle_conversion_roundtrip(self):  # ^TestCalculatorIntegration-test_angle_conversion_roundtrip
        """Test that angle conversion is reversible."""
        # 45° to radians
        rad_result = self.calc._parse_and_calculate("45 rad")

        # Convert back to degrees
        deg_result = self.calc._parse_and_calculate(f"{rad_result} deg")
        self.assertAlmostEqual(deg_result, 45)


if __name__ == '__main__':
    unittest.main()
