---
tags:
  - type/pattern
  - domain/testing
  - category/best-practices
---

# Testing Strategy

## Overview

This document describes the testing approach for the calculator application. The test suite ensures correctness, reliability, and maintainability through comprehensive unit and integration tests.

## Test Organization

### Test Files

- **[[code/test_operations.py|test_operations.py]]** - Tests for the operations module
- **[[code/test_calculator.py|test_calculator.py]]** - Tests for the Calculator class

### Test Structure

Tests are organized using Python's `unittest` framework with the following hierarchy:

```
TestClass (one per logical grouping)
  ├── setUp() - Initialize test fixtures
  └── test_methods() - Individual test cases
```

## Testing Levels

### Unit Tests

**Purpose**: Test individual functions and methods in isolation.

**Coverage**:
- All arithmetic operations ([[code/operations.py#^add|add]], [[code/operations.py#^subtract|subtract]], [[code/operations.py#^multiply|multiply]], [[code/operations.py#^divide|divide]])
- Scientific functions (trigonometric, logarithmic, exponential)
- Power operations and roots
- Angle conversions
- Mathematical constants
- Input validation and error handling

**Example**:
```python
def test_divide_by_zero(self):
    """Test that division by zero raises ValueError."""
    with self.assertRaises(ValueError) as context:
        operations.divide(5, 0)
    self.assertIn("Cannot divide by zero", str(context.exception))
```

### Integration Tests

**Purpose**: Test interactions between Calculator and Operations modules.

**Coverage**:
- Calculator's `calculate()` method with various operations
- Input parsing (`_parse_and_calculate()`)
- Interactive mode flow
- Error propagation through layers

**Example**:
```python
def test_complex_scientific_calculation(self):
    """Test complex scientific calculations through the calculator."""
    result = self.calc._parse_and_calculate(f"{math.pi / 2} sin")
    self.assertAlmostEqual(result, 1)
```

### Interactive Mode Tests

**Purpose**: Test user interface behavior and input handling.

**Coverage**:
- User input processing
- Error handling in interactive mode
- Graceful exit (quit command, KeyboardInterrupt)
- Multiple sequential calculations

**Approach**: Uses mocking (`@patch`) to simulate user input and verify output.

## Test Categories by Domain

### Mathematical Correctness

Tests verify mathematical accuracy:
- **Exact values**: Integer arithmetic, factorials
- **Floating-point**: Trigonometric functions, logarithms (using `assertAlmostEqual`)
- **Edge cases**: Zero, negative numbers, boundary values
- **Identities**: Inverse operations (e.g., power/log, sin/asin)

### Error Handling

Tests verify proper validation:
- **Domain errors**: sqrt of negative, log of non-positive, asin/acos out of range
- **Division by zero**: Explicit ValueError with message
- **Type errors**: Non-integer for factorial
- **Invalid operations**: Unknown operation symbols

### Strategy Pattern

Tests verify registry functionality ([[strategy-pattern|Strategy Pattern]]):
- **Operation registries**: All operations registered correctly
- **Callable verification**: Registry entries are functions
- **Invocation through registry**: Operations work when called via dictionary

## Running Tests

### Run All Tests

```bash
cd code
python -m unittest discover -s . -p "test_*.py"
```

### Run Specific Test File

```bash
cd code
python -m unittest test_operations
python -m unittest test_calculator
```

### Run Specific Test Class

```bash
cd code
python -m unittest test_operations.TestBasicArithmetic
python -m unittest test_calculator.TestCalculatorParsing
```

### Run Specific Test Method

```bash
cd code
python -m unittest test_operations.TestBasicArithmetic.test_divide_by_zero
```

### Verbose Output

```bash
cd code
python -m unittest discover -v
```

## Test Naming Conventions

### Test Classes

- `Test{Component}{Category}` - e.g., `TestBasicArithmetic`, `TestCalculatorParsing`
- One test class per logical grouping of functionality

### Test Methods

- `test_{functionality}` - Descriptive name of what is being tested
- `test_{functionality}_error` - For error/exception tests
- Examples: `test_divide_by_zero`, `test_parse_invalid_format`

### Docstrings

Every test method includes a docstring explaining:
- What functionality is being tested
- Expected behavior

## Coverage Goals

### Current Coverage

- **Operations Module**: ~100% function coverage
  - All arithmetic operations
  - All scientific functions
  - All error conditions
  - Operation registries

- **Calculator Class**: ~95% method coverage
  - `calculate()` method
  - `_parse_and_calculate()` method
  - `run_interactive()` method (via mocking)

### What's Tested

✅ All basic arithmetic operations
✅ All scientific functions
✅ Input validation and domain errors
✅ Parser for binary operations
✅ Parser for unary operations
✅ Constants (pi, e)
✅ Angle conversions
✅ Operation registries
✅ Interactive mode flow
✅ Error handling at all layers

### What's Not Tested

⚠️ Main entry point (`main.py`) - Tested manually
⚠️ Exact terminal output formatting - Visual verification only

## Test Maintenance

### When to Update Tests

1. **Adding new operations**: Add tests to `test_operations.py`
   - Test normal cases
   - Test edge cases
   - Test error conditions
   - Add to registry tests

2. **Modifying calculator interface**: Update `test_calculator.py`
   - Update parsing tests if input format changes
   - Update interactive tests if UI changes

3. **Changing error messages**: Update error message assertions in tests

### Best Practices

- **Test first**: Write tests before implementing features (TDD)
- **One concept per test**: Each test method tests one specific behavior
- **Descriptive names**: Test names should describe what they verify
- **Avoid test interdependence**: Tests should run independently
- **Use appropriate assertions**: `assertEqual` for exact, `assertAlmostEqual` for floats
- **Test error messages**: Verify not just that exceptions occur, but their messages

## Related Documentation

- Implementation: [[code/operations.py|Operations Module]]
- Implementation: [[code/calculator.py|Calculator Class]]
- Pattern: [[strategy-pattern|Strategy Pattern]]
- Validation: [[user-input-validation|User Input Validation]]
- Concepts: [[arithmetic-operations|Arithmetic Operations]]
