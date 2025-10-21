"""
# Unit Conversion Plugin Tests

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/test_units.py #domain/unit-conversion #domain/testing #domain/testing/unit #layer/test #category/unit-test

## Purpose
Unit tests for the unit conversion plugin operations including length, weight,
and temperature conversions.

## Related Documentation
- Pattern: [[../obsidian/testing-strategy|Testing Strategy]]
- Implementation: [[plugins/units.py|Unit Conversion Plugin]]
- Concept: [[../obsidian/dimensional-analysis|Dimensional Analysis]]

## Test Coverage
Tests all conversion functions: length (meters/feet, km/miles, inches/cm),
weight (kg/lbs, grams/oz), temperature (celsius/fahrenheit/kelvin)
"""
import unittest
from plugins import units


class TestLengthConversions(unittest.TestCase):  # ^TestLengthConversions
    """
    Tests for length conversion functions.

    Related: [[../obsidian/testing-strategy|Testing Strategy]]
    """

    def test_meters_to_feet(self):  # ^TestLengthConversions-test_meters_to_feet
        """Test meters to feet conversion."""
        result = units.meters_to_feet(1)
        self.assertAlmostEqual(result, 3.28084, places=5)

    def test_feet_to_meters(self):  # ^TestLengthConversions-test_feet_to_meters
        """Test feet to meters conversion."""
        result = units.feet_to_meters(3.28084)
        self.assertAlmostEqual(result, 1.0, places=5)

    def test_meters_feet_roundtrip(self):  # ^TestLengthConversions-test_meters_feet_roundtrip
        """Test meters→feet→meters roundtrip."""
        original = 10.0
        result = units.feet_to_meters(units.meters_to_feet(original))
        self.assertAlmostEqual(result, original, places=5)

    def test_km_to_miles(self):  # ^TestLengthConversions-test_km_to_miles
        """Test kilometers to miles conversion."""
        result = units.km_to_miles(5)
        self.assertAlmostEqual(result, 3.106855, places=5)

    def test_miles_to_km(self):  # ^TestLengthConversions-test_miles_to_km
        """Test miles to kilometers conversion."""
        result = units.miles_to_km(10)
        self.assertAlmostEqual(result, 16.0934, places=4)

    def test_km_miles_roundtrip(self):  # ^TestLengthConversions-test_km_miles_roundtrip
        """Test km→miles→km roundtrip."""
        original = 100.0
        result = units.miles_to_km(units.km_to_miles(original))
        self.assertAlmostEqual(result, original, places=3)

    def test_inches_to_cm(self):  # ^TestLengthConversions-test_inches_to_cm
        """Test inches to centimeters conversion."""
        result = units.inches_to_cm(1)
        self.assertEqual(result, 2.54)  # Exact by definition

    def test_cm_to_inches(self):  # ^TestLengthConversions-test_cm_to_inches
        """Test centimeters to inches conversion."""
        result = units.cm_to_inches(2.54)
        self.assertAlmostEqual(result, 1.0, places=5)

    def test_inches_cm_roundtrip(self):  # ^TestLengthConversions-test_inches_cm_roundtrip
        """Test inches→cm→inches roundtrip."""
        original = 12.0
        result = units.cm_to_inches(units.inches_to_cm(original))
        self.assertAlmostEqual(result, original, places=4)

    def test_negative_length(self):  # ^TestLengthConversions-test_negative_length
        """Test that negative lengths raise ValueError."""
        with self.assertRaises(ValueError):
            units.meters_to_feet(-5)
        with self.assertRaises(ValueError):
            units.km_to_miles(-10)
        with self.assertRaises(ValueError):
            units.inches_to_cm(-1)

    def test_zero_length(self):  # ^TestLengthConversions-test_zero_length
        """Test that zero length is valid."""
        self.assertEqual(units.meters_to_feet(0), 0)
        self.assertEqual(units.km_to_miles(0), 0)
        self.assertEqual(units.inches_to_cm(0), 0)


class TestWeightConversions(unittest.TestCase):  # ^TestWeightConversions
    """
    Tests for weight conversion functions.

    Related: [[../obsidian/testing-strategy|Testing Strategy]]
    """

    def test_kg_to_lbs(self):  # ^TestWeightConversions-test_kg_to_lbs
        """Test kilograms to pounds conversion."""
        result = units.kg_to_lbs(1)
        self.assertAlmostEqual(result, 2.20462, places=5)

    def test_lbs_to_kg(self):  # ^TestWeightConversions-test_lbs_to_kg
        """Test pounds to kilograms conversion."""
        result = units.lbs_to_kg(2.20462)
        self.assertAlmostEqual(result, 1.0, places=5)

    def test_kg_lbs_roundtrip(self):  # ^TestWeightConversions-test_kg_lbs_roundtrip
        """Test kg→lbs→kg roundtrip."""
        original = 50.0
        result = units.lbs_to_kg(units.kg_to_lbs(original))
        self.assertAlmostEqual(result, original, places=3)

    def test_grams_to_oz(self):  # ^TestWeightConversions-test_grams_to_oz
        """Test grams to ounces conversion."""
        result = units.grams_to_oz(100)
        self.assertAlmostEqual(result, 3.5274, places=4)

    def test_oz_to_grams(self):  # ^TestWeightConversions-test_oz_to_grams
        """Test ounces to grams conversion."""
        result = units.oz_to_grams(1)
        self.assertAlmostEqual(result, 28.3495, places=4)

    def test_grams_oz_roundtrip(self):  # ^TestWeightConversions-test_grams_oz_roundtrip
        """Test grams→oz→grams roundtrip."""
        original = 500.0
        result = units.oz_to_grams(units.grams_to_oz(original))
        self.assertAlmostEqual(result, original, places=3)

    def test_negative_weight(self):  # ^TestWeightConversions-test_negative_weight
        """Test that negative weights raise ValueError."""
        with self.assertRaises(ValueError):
            units.kg_to_lbs(-5)
        with self.assertRaises(ValueError):
            units.grams_to_oz(-10)

    def test_zero_weight(self):  # ^TestWeightConversions-test_zero_weight
        """Test that zero weight is valid."""
        self.assertEqual(units.kg_to_lbs(0), 0)
        self.assertEqual(units.grams_to_oz(0), 0)


class TestTemperatureConversions(unittest.TestCase):  # ^TestTemperatureConversions
    """
    Tests for temperature conversion functions.

    Related: [[../obsidian/testing-strategy|Testing Strategy]]
    """

    def test_celsius_to_fahrenheit_freezing(self):  # ^TestTemperatureConversions-test_celsius_to_fahrenheit_freezing
        """Test water freezing point: 0°C = 32°F."""
        result = units.celsius_to_fahrenheit(0)
        self.assertEqual(result, 32)

    def test_celsius_to_fahrenheit_boiling(self):  # ^TestTemperatureConversions-test_celsius_to_fahrenheit_boiling
        """Test water boiling point: 100°C = 212°F."""
        result = units.celsius_to_fahrenheit(100)
        self.assertEqual(result, 212)

    def test_fahrenheit_to_celsius_freezing(self):  # ^TestTemperatureConversions-test_fahrenheit_to_celsius_freezing
        """Test water freezing point: 32°F = 0°C."""
        result = units.fahrenheit_to_celsius(32)
        self.assertEqual(result, 0)

    def test_fahrenheit_to_celsius_boiling(self):  # ^TestTemperatureConversions-test_fahrenheit_to_celsius_boiling
        """Test water boiling point: 212°F = 100°C."""
        result = units.fahrenheit_to_celsius(212)
        self.assertEqual(result, 100)

    def test_celsius_fahrenheit_roundtrip(self):  # ^TestTemperatureConversions-test_celsius_fahrenheit_roundtrip
        """Test celsius→fahrenheit→celsius roundtrip."""
        original = 25.0
        result = units.fahrenheit_to_celsius(units.celsius_to_fahrenheit(original))
        self.assertAlmostEqual(result, original, places=10)

    def test_celsius_to_kelvin_freezing(self):  # ^TestTemperatureConversions-test_celsius_to_kelvin_freezing
        """Test water freezing point: 0°C = 273.15 K."""
        result = units.celsius_to_kelvin(0)
        self.assertEqual(result, 273.15)

    def test_celsius_to_kelvin_absolute_zero(self):  # ^TestTemperatureConversions-test_celsius_to_kelvin_absolute_zero
        """Test absolute zero: -273.15°C = 0 K."""
        result = units.celsius_to_kelvin(-273.15)
        self.assertEqual(result, 0)

    def test_kelvin_to_celsius_freezing(self):  # ^TestTemperatureConversions-test_kelvin_to_celsius_freezing
        """Test water freezing point: 273.15 K = 0°C."""
        result = units.kelvin_to_celsius(273.15)
        self.assertEqual(result, 0)

    def test_kelvin_to_celsius_absolute_zero(self):  # ^TestTemperatureConversions-test_kelvin_to_celsius_absolute_zero
        """Test absolute zero: 0 K = -273.15°C."""
        result = units.kelvin_to_celsius(0)
        self.assertEqual(result, -273.15)

    def test_celsius_kelvin_roundtrip(self):  # ^TestTemperatureConversions-test_celsius_kelvin_roundtrip
        """Test celsius→kelvin→celsius roundtrip."""
        original = 100.0
        result = units.kelvin_to_celsius(units.celsius_to_kelvin(original))
        self.assertEqual(result, original)

    def test_celsius_below_absolute_zero(self):  # ^TestTemperatureConversions-test_celsius_below_absolute_zero
        """Test that temperatures below absolute zero raise ValueError."""
        with self.assertRaises(ValueError):
            units.celsius_to_fahrenheit(-300)
        with self.assertRaises(ValueError):
            units.celsius_to_kelvin(-300)

    def test_fahrenheit_below_absolute_zero(self):  # ^TestTemperatureConversions-test_fahrenheit_below_absolute_zero
        """Test that Fahrenheit below absolute zero raises ValueError."""
        with self.assertRaises(ValueError):
            units.fahrenheit_to_celsius(-500)

    def test_kelvin_below_absolute_zero(self):  # ^TestTemperatureConversions-test_kelvin_below_absolute_zero
        """Test that negative Kelvin raises ValueError."""
        with self.assertRaises(ValueError):
            units.kelvin_to_celsius(-1)

    def test_celsius_fahrenheit_specific_values(self):  # ^TestTemperatureConversions-test_celsius_fahrenheit_specific_values
        """Test specific temperature values."""
        # Body temperature: 37°C ≈ 98.6°F
        self.assertAlmostEqual(units.celsius_to_fahrenheit(37), 98.6, places=1)
        # Room temperature: 20°C = 68°F
        self.assertAlmostEqual(units.celsius_to_fahrenheit(20), 68, places=1)


class TestConversionInverses(unittest.TestCase):  # ^TestConversionInverses
    """
    Tests that conversion functions are proper inverses.

    Related: [[../obsidian/testing-strategy|Testing Strategy]]
    """

    def test_all_length_roundtrips(self):  # ^TestConversionInverses-test_all_length_roundtrips
        """Test all length conversions are proper inverses."""
        test_value = 42.0

        # Meters ↔ Feet
        result = units.feet_to_meters(units.meters_to_feet(test_value))
        self.assertAlmostEqual(result, test_value, places=5)

        # Km ↔ Miles
        result = units.miles_to_km(units.km_to_miles(test_value))
        self.assertAlmostEqual(result, test_value, places=3)

        # Inches ↔ Cm
        result = units.cm_to_inches(units.inches_to_cm(test_value))
        self.assertAlmostEqual(result, test_value, places=4)

    def test_all_weight_roundtrips(self):  # ^TestConversionInverses-test_all_weight_roundtrips
        """Test all weight conversions are proper inverses."""
        test_value = 42.0

        # Kg ↔ Lbs
        result = units.lbs_to_kg(units.kg_to_lbs(test_value))
        self.assertAlmostEqual(result, test_value, places=3)

        # Grams ↔ Oz
        result = units.oz_to_grams(units.grams_to_oz(test_value))
        self.assertAlmostEqual(result, test_value, places=4)

    def test_all_temperature_roundtrips(self):  # ^TestConversionInverses-test_all_temperature_roundtrips
        """Test all temperature conversions are proper inverses."""
        test_value = 42.0

        # Celsius ↔ Fahrenheit
        result = units.fahrenheit_to_celsius(units.celsius_to_fahrenheit(test_value))
        self.assertAlmostEqual(result, test_value, places=10)

        # Celsius ↔ Kelvin
        result = units.kelvin_to_celsius(units.celsius_to_kelvin(test_value))
        self.assertEqual(result, test_value)


if __name__ == '__main__':
    unittest.main()
