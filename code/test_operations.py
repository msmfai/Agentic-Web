"""
# Operations Module Tests

**Tags**: #type/code-file #domain/testing #domain/testing/unit #layer/test #category/unit-test #domain/mathematics

## Purpose
Unit tests for the operations module.
Tests all arithmetic and scientific operations including edge cases and error handling.

## Related Documentation
- Tests: [[operations.py|Operations Module]]
- Concept: [[arithmetic-operations|Arithmetic Operations]]
- Pattern: [[user-input-validation|User Input Validation]]

## Dependencies
- [[operations.py|Operations Module]]
"""
import unittest
import math
import operations


class TestBasicArithmetic(unittest.TestCase):  # ^TestBasicArithmetic
    """
    Test basic arithmetic operations.

    Related: [[operations.py|Operations Module]]
    Related: [[arithmetic-operations|Arithmetic Operations]]
    """

    def test_add(self):  # ^TestBasicArithmetic-test_add
        """Test addition operation."""
        self.assertEqual(operations.add(2, 3), 5)
        self.assertEqual(operations.add(-1, 1), 0)
        self.assertEqual(operations.add(0, 0), 0)
        self.assertAlmostEqual(operations.add(0.1, 0.2), 0.3)

    def test_subtract(self):  # ^TestBasicArithmetic-test_subtract
        """Test subtraction operation."""
        self.assertEqual(operations.subtract(5, 3), 2)
        self.assertEqual(operations.subtract(3, 5), -2)
        self.assertEqual(operations.subtract(0, 0), 0)
        self.assertAlmostEqual(operations.subtract(0.3, 0.1), 0.2)

    def test_multiply(self):  # ^TestBasicArithmetic-test_multiply
        """Test multiplication operation."""
        self.assertEqual(operations.multiply(2, 3), 6)
        self.assertEqual(operations.multiply(-2, 3), -6)
        self.assertEqual(operations.multiply(0, 100), 0)
        self.assertAlmostEqual(operations.multiply(0.1, 0.2), 0.02)

    def test_divide(self):  # ^TestBasicArithmetic-test_divide
        """Test division operation."""
        self.assertEqual(operations.divide(6, 3), 2)
        self.assertEqual(operations.divide(-6, 3), -2)
        self.assertAlmostEqual(operations.divide(1, 3), 0.3333333333333333)

    def test_divide_by_zero(self):  # ^TestBasicArithmetic-test_divide_by_zero
        """Test that division by zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            operations.divide(5, 0)
        self.assertIn("Cannot divide by zero", str(context.exception))


class TestFactorial(unittest.TestCase):  # ^TestFactorial
    """
    Test factorial operation.

    Related: [[operations.py|Operations Module]]
    """

    def test_factorial_positive(self):  # ^TestFactorial-test_factorial_positive
        """Test factorial with positive integers."""
        self.assertEqual(operations.factorial(0), 1)
        self.assertEqual(operations.factorial(1), 1)
        self.assertEqual(operations.factorial(5), 120)
        self.assertEqual(operations.factorial(10), 3628800)

    def test_factorial_negative(self):  # ^TestFactorial-test_factorial_negative
        """Test that factorial of negative number raises ValueError."""
        with self.assertRaises(ValueError) as context:
            operations.factorial(-1)
        self.assertIn("not defined for negative", str(context.exception))

    def test_factorial_non_integer(self):  # ^TestFactorial-test_factorial_non_integer
        """Test that factorial of non-integer raises ValueError."""
        with self.assertRaises(ValueError) as context:
            operations.factorial(3.5)
        self.assertIn("only defined for integers", str(context.exception))


class TestTrigonometric(unittest.TestCase):  # ^TestTrigonometric
    """
    Test trigonometric functions.

    Related: [[operations.py|Operations Module]]
    """

    def test_sin(self):  # ^TestTrigonometric-test_sin
        """Test sine function."""
        self.assertAlmostEqual(operations.sin(0), 0)
        self.assertAlmostEqual(operations.sin(math.pi / 2), 1)
        self.assertAlmostEqual(operations.sin(math.pi), 0, places=10)
        self.assertAlmostEqual(operations.sin(3 * math.pi / 2), -1)

    def test_cos(self):  # ^TestTrigonometric-test_cos
        """Test cosine function."""
        self.assertAlmostEqual(operations.cos(0), 1)
        self.assertAlmostEqual(operations.cos(math.pi / 2), 0, places=10)
        self.assertAlmostEqual(operations.cos(math.pi), -1)
        self.assertAlmostEqual(operations.cos(2 * math.pi), 1)

    def test_tan(self):  # ^TestTrigonometric-test_tan
        """Test tangent function."""
        self.assertAlmostEqual(operations.tan(0), 0)
        self.assertAlmostEqual(operations.tan(math.pi / 4), 1)
        self.assertAlmostEqual(operations.tan(math.pi), 0, places=10)

    def test_asin(self):  # ^TestTrigonometric-test_asin
        """Test arcsine function."""
        self.assertAlmostEqual(operations.asin(0), 0)
        self.assertAlmostEqual(operations.asin(1), math.pi / 2)
        self.assertAlmostEqual(operations.asin(-1), -math.pi / 2)
        self.assertAlmostEqual(operations.asin(0.5), math.pi / 6)

    def test_asin_domain_error(self):  # ^TestTrigonometric-test_asin_domain_error
        """Test that asin raises ValueError for out-of-range inputs."""
        with self.assertRaises(ValueError) as context:
            operations.asin(1.5)
        self.assertIn("asin domain error", str(context.exception))

        with self.assertRaises(ValueError):
            operations.asin(-1.5)

    def test_acos(self):  # ^TestTrigonometric-test_acos
        """Test arccosine function."""
        self.assertAlmostEqual(operations.acos(1), 0)
        self.assertAlmostEqual(operations.acos(0), math.pi / 2)
        self.assertAlmostEqual(operations.acos(-1), math.pi)
        self.assertAlmostEqual(operations.acos(0.5), math.pi / 3)

    def test_acos_domain_error(self):  # ^TestTrigonometric-test_acos_domain_error
        """Test that acos raises ValueError for out-of-range inputs."""
        with self.assertRaises(ValueError) as context:
            operations.acos(1.5)
        self.assertIn("acos domain error", str(context.exception))

        with self.assertRaises(ValueError):
            operations.acos(-1.5)

    def test_atan(self):  # ^TestTrigonometric-test_atan
        """Test arctangent function."""
        self.assertAlmostEqual(operations.atan(0), 0)
        self.assertAlmostEqual(operations.atan(1), math.pi / 4)
        self.assertAlmostEqual(operations.atan(-1), -math.pi / 4)


class TestExponentialLogarithmic(unittest.TestCase):  # ^TestExponentialLogarithmic
    """
    Test exponential and logarithmic functions.

    Related: [[operations.py|Operations Module]]
    """

    def test_exp(self):  # ^TestExponentialLogarithmic-test_exp
        """Test exponential function."""
        self.assertAlmostEqual(operations.exp(0), 1)
        self.assertAlmostEqual(operations.exp(1), math.e)
        self.assertAlmostEqual(operations.exp(2), math.e ** 2)
        self.assertAlmostEqual(operations.exp(-1), 1 / math.e)

    def test_ln(self):  # ^TestExponentialLogarithmic-test_ln
        """Test natural logarithm."""
        self.assertAlmostEqual(operations.ln(1), 0)
        self.assertAlmostEqual(operations.ln(math.e), 1)
        self.assertAlmostEqual(operations.ln(math.e ** 2), 2)
        self.assertAlmostEqual(operations.ln(10), math.log(10))

    def test_ln_domain_error(self):  # ^TestExponentialLogarithmic-test_ln_domain_error
        """Test that ln raises ValueError for non-positive inputs."""
        with self.assertRaises(ValueError) as context:
            operations.ln(0)
        self.assertIn("ln domain error", str(context.exception))

        with self.assertRaises(ValueError):
            operations.ln(-5)

    def test_log10(self):  # ^TestExponentialLogarithmic-test_log10
        """Test base-10 logarithm."""
        self.assertAlmostEqual(operations.log10(1), 0)
        self.assertAlmostEqual(operations.log10(10), 1)
        self.assertAlmostEqual(operations.log10(100), 2)
        self.assertAlmostEqual(operations.log10(1000), 3)

    def test_log10_domain_error(self):  # ^TestExponentialLogarithmic-test_log10_domain_error
        """Test that log10 raises ValueError for non-positive inputs."""
        with self.assertRaises(ValueError) as context:
            operations.log10(0)
        self.assertIn("log10 domain error", str(context.exception))

        with self.assertRaises(ValueError):
            operations.log10(-10)

    def test_log_custom_base(self):  # ^TestExponentialLogarithmic-test_log_custom_base
        """Test logarithm with custom base."""
        self.assertAlmostEqual(operations.log(8, 2), 3)
        self.assertAlmostEqual(operations.log(27, 3), 3)
        self.assertAlmostEqual(operations.log(1, 10), 0)
        self.assertAlmostEqual(operations.log(100, 10), 2)

    def test_log_domain_errors(self):  # ^TestExponentialLogarithmic-test_log_domain_errors
        """Test that log raises ValueError for invalid inputs."""
        # Non-positive x
        with self.assertRaises(ValueError) as context:
            operations.log(0, 2)
        self.assertIn("x must be positive", str(context.exception))

        with self.assertRaises(ValueError):
            operations.log(-5, 2)

        # Non-positive base
        with self.assertRaises(ValueError) as context:
            operations.log(10, 0)
        self.assertIn("base must be positive", str(context.exception))

        with self.assertRaises(ValueError):
            operations.log(10, -2)

        # Base equal to 1
        with self.assertRaises(ValueError) as context:
            operations.log(10, 1)
        self.assertIn("not equal to 1", str(context.exception))


class TestPowerOperations(unittest.TestCase):  # ^TestPowerOperations
    """
    Test power and root operations.

    Related: [[operations.py|Operations Module]]
    """

    def test_power(self):  # ^TestPowerOperations-test_power
        """Test power operation."""
        self.assertAlmostEqual(operations.power(2, 3), 8)
        self.assertAlmostEqual(operations.power(5, 2), 25)
        self.assertAlmostEqual(operations.power(2, -1), 0.5)
        self.assertAlmostEqual(operations.power(10, 0), 1)
        self.assertAlmostEqual(operations.power(4, 0.5), 2)

    def test_sqrt(self):  # ^TestPowerOperations-test_sqrt
        """Test square root."""
        self.assertAlmostEqual(operations.sqrt(0), 0)
        self.assertAlmostEqual(operations.sqrt(1), 1)
        self.assertAlmostEqual(operations.sqrt(4), 2)
        self.assertAlmostEqual(operations.sqrt(9), 3)
        self.assertAlmostEqual(operations.sqrt(2), math.sqrt(2))

    def test_sqrt_domain_error(self):  # ^TestPowerOperations-test_sqrt_domain_error
        """Test that sqrt raises ValueError for negative inputs."""
        with self.assertRaises(ValueError) as context:
            operations.sqrt(-1)
        self.assertIn("sqrt domain error", str(context.exception))

    def test_cbrt(self):  # ^TestPowerOperations-test_cbrt
        """Test cube root."""
        self.assertAlmostEqual(operations.cbrt(0), 0)
        self.assertAlmostEqual(operations.cbrt(1), 1)
        self.assertAlmostEqual(operations.cbrt(8), 2)
        self.assertAlmostEqual(operations.cbrt(27), 3)
        self.assertAlmostEqual(operations.cbrt(-8), -2)  # Handles negative numbers


class TestAngleConversion(unittest.TestCase):  # ^TestAngleConversion
    """
    Test angle conversion functions.

    Related: [[operations.py|Operations Module]]
    """

    def test_deg_to_rad(self):  # ^TestAngleConversion-test_deg_to_rad
        """Test degrees to radians conversion."""
        self.assertAlmostEqual(operations.deg_to_rad(0), 0)
        self.assertAlmostEqual(operations.deg_to_rad(90), math.pi / 2)
        self.assertAlmostEqual(operations.deg_to_rad(180), math.pi)
        self.assertAlmostEqual(operations.deg_to_rad(360), 2 * math.pi)
        self.assertAlmostEqual(operations.deg_to_rad(-90), -math.pi / 2)

    def test_rad_to_deg(self):  # ^TestAngleConversion-test_rad_to_deg
        """Test radians to degrees conversion."""
        self.assertAlmostEqual(operations.rad_to_deg(0), 0)
        self.assertAlmostEqual(operations.rad_to_deg(math.pi / 2), 90)
        self.assertAlmostEqual(operations.rad_to_deg(math.pi), 180)
        self.assertAlmostEqual(operations.rad_to_deg(2 * math.pi), 360)
        self.assertAlmostEqual(operations.rad_to_deg(-math.pi / 2), -90)


class TestConstants(unittest.TestCase):  # ^TestConstants
    """
    Test mathematical constants.

    Related: [[operations.py|Operations Module]]
    """

    def test_pi_const(self):  # ^TestConstants-test_pi_const
        """Test pi constant."""
        self.assertAlmostEqual(operations.pi_const(), math.pi)
        self.assertAlmostEqual(operations.pi_const(0), math.pi)
        self.assertAlmostEqual(operations.pi_const(999), math.pi)  # Ignores argument

    def test_e_const(self):  # ^TestConstants-test_e_const
        """Test e constant."""
        self.assertAlmostEqual(operations.e_const(), math.e)
        self.assertAlmostEqual(operations.e_const(0), math.e)
        self.assertAlmostEqual(operations.e_const(999), math.e)  # Ignores argument


class TestOperationRegistries(unittest.TestCase):  # ^TestOperationRegistries
    """
    Test operation registry dictionaries.

    Related: [[operations.py|Operations Module]]
    Related: [[strategy-pattern|Strategy Pattern]]
    """

    def test_operations_registry(self):  # ^TestOperationRegistries-test_operations_registry
        """Test that OPERATIONS dictionary contains expected binary operations."""
        expected_ops = ['+', '-', '*', '/', '^', '**', 'log']
        for op in expected_ops:
            self.assertIn(op, operations.OPERATIONS)
            self.assertTrue(callable(operations.OPERATIONS[op]))

    def test_unary_operations_registry(self):  # ^TestOperationRegistries-test_unary_operations_registry
        """Test that UNARY_OPERATIONS dictionary contains expected unary operations."""
        expected_ops = [
            '!', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
            'exp', 'ln', 'log10', 'sqrt', 'cbrt', 'pi', 'e', 'deg', 'rad'
        ]
        for op in expected_ops:
            self.assertIn(op, operations.UNARY_OPERATIONS)
            self.assertTrue(callable(operations.UNARY_OPERATIONS[op]))

    def test_operations_functionality(self):  # ^TestOperationRegistries-test_operations_functionality
        """Test that operations can be called through the registry."""
        self.assertEqual(operations.OPERATIONS['+'](2, 3), 5)
        self.assertEqual(operations.OPERATIONS['-'](5, 3), 2)
        self.assertEqual(operations.OPERATIONS['*'](2, 4), 8)
        self.assertEqual(operations.OPERATIONS['/'](10, 2), 5)
        self.assertAlmostEqual(operations.OPERATIONS['^'](2, 3), 8)
        self.assertAlmostEqual(operations.OPERATIONS['**'](2, 3), 8)

    def test_unary_operations_functionality(self):  # ^TestOperationRegistries-test_unary_operations_functionality
        """Test that unary operations can be called through the registry."""
        self.assertEqual(operations.UNARY_OPERATIONS['!'](5), 120)
        self.assertAlmostEqual(operations.UNARY_OPERATIONS['sqrt'](16), 4)
        self.assertAlmostEqual(operations.UNARY_OPERATIONS['cbrt'](27), 3)
        self.assertAlmostEqual(operations.UNARY_OPERATIONS['pi'](), math.pi)
        self.assertAlmostEqual(operations.UNARY_OPERATIONS['e'](), math.e)


if __name__ == '__main__':
    unittest.main()
