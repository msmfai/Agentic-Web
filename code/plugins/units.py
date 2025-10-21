"""
# Unit Conversion Plugin

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/plugins/units.py #domain/unit-conversion #layer/plugin-implementation #pattern/plugin-architecture #pattern/strategy/function-registry

## Purpose
Provides unit conversion operations for length, weight, and temperature.
Supports conversions between metric and imperial systems.

## Related Documentation
- Pattern: [[obsidian/plugin-architecture.md|Plugin Architecture]]
- Concept: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]

## Plugin Interface
Exports PLUGIN_OPERATIONS dictionary for dynamic loading by the plugin system.

## Used By
- [[../plugin_system.py|Plugin System]]
"""


# Length Conversions

def meters_to_feet(meters: float) -> float:  # ^meters_to_feet
    """
    Convert meters to feet.

    Conversion: 1 meter = 3.28084 feet

    Args:
        meters: Length in meters

    Returns:
        Length in feet

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if meters < 0:
        raise ValueError("Length cannot be negative")
    return meters * 3.28084


def feet_to_meters(feet: float) -> float:  # ^feet_to_meters
    """
    Convert feet to meters.

    Conversion: 1 foot = 0.3048 meters

    Args:
        feet: Length in feet

    Returns:
        Length in meters

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if feet < 0:
        raise ValueError("Length cannot be negative")
    return feet * 0.3048


def km_to_miles(km: float) -> float:  # ^km_to_miles
    """
    Convert kilometers to miles.

    Conversion: 1 kilometer = 0.621371 miles

    Args:
        km: Distance in kilometers

    Returns:
        Distance in miles

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if km < 0:
        raise ValueError("Distance cannot be negative")
    return km * 0.621371


def miles_to_km(miles: float) -> float:  # ^miles_to_km
    """
    Convert miles to kilometers.

    Conversion: 1 mile = 1.60934 kilometers

    Args:
        miles: Distance in miles

    Returns:
        Distance in kilometers

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if miles < 0:
        raise ValueError("Distance cannot be negative")
    return miles * 1.60934


def inches_to_cm(inches: float) -> float:  # ^inches_to_cm
    """
    Convert inches to centimeters.

    Conversion: 1 inch = 2.54 centimeters

    Args:
        inches: Length in inches

    Returns:
        Length in centimeters

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if inches < 0:
        raise ValueError("Length cannot be negative")
    return inches * 2.54


def cm_to_inches(cm: float) -> float:  # ^cm_to_inches
    """
    Convert centimeters to inches.

    Conversion: 1 centimeter = 0.393701 inches

    Args:
        cm: Length in centimeters

    Returns:
        Length in inches

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if cm < 0:
        raise ValueError("Length cannot be negative")
    return cm * 0.393701


# Weight Conversions

def kg_to_lbs(kg: float) -> float:  # ^kg_to_lbs
    """
    Convert kilograms to pounds.

    Conversion: 1 kilogram = 2.20462 pounds

    Args:
        kg: Weight in kilograms

    Returns:
        Weight in pounds

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if kg < 0:
        raise ValueError("Weight cannot be negative")
    return kg * 2.20462


def lbs_to_kg(lbs: float) -> float:  # ^lbs_to_kg
    """
    Convert pounds to kilograms.

    Conversion: 1 pound = 0.453592 kilograms

    Args:
        lbs: Weight in pounds

    Returns:
        Weight in kilograms

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if lbs < 0:
        raise ValueError("Weight cannot be negative")
    return lbs * 0.453592


def grams_to_oz(grams: float) -> float:  # ^grams_to_oz
    """
    Convert grams to ounces.

    Conversion: 1 gram = 0.035274 ounces

    Args:
        grams: Weight in grams

    Returns:
        Weight in ounces

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if grams < 0:
        raise ValueError("Weight cannot be negative")
    return grams * 0.035274


def oz_to_grams(oz: float) -> float:  # ^oz_to_grams
    """
    Convert ounces to grams.

    Conversion: 1 ounce = 28.3495 grams

    Args:
        oz: Weight in ounces

    Returns:
        Weight in grams

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if oz < 0:
        raise ValueError("Weight cannot be negative")
    return oz * 28.3495


# Temperature Conversions

def celsius_to_fahrenheit(celsius: float) -> float:  # ^celsius_to_fahrenheit
    """
    Convert Celsius to Fahrenheit.

    Formula: F = C × 9/5 + 32

    Args:
        celsius: Temperature in Celsius

    Returns:
        Temperature in Fahrenheit

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if celsius < -273.15:
        raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
    return celsius * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:  # ^fahrenheit_to_celsius
    """
    Convert Fahrenheit to Celsius.

    Formula: C = (F - 32) × 5/9

    Args:
        fahrenheit: Temperature in Fahrenheit

    Returns:
        Temperature in Celsius

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if fahrenheit < -459.67:
        raise ValueError("Temperature cannot be below absolute zero (-459.67°F)")
    return (fahrenheit - 32) * 5/9


def celsius_to_kelvin(celsius: float) -> float:  # ^celsius_to_kelvin
    """
    Convert Celsius to Kelvin.

    Formula: K = C + 273.15

    Args:
        celsius: Temperature in Celsius

    Returns:
        Temperature in Kelvin

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if celsius < -273.15:
        raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:  # ^kelvin_to_celsius
    """
    Convert Kelvin to Celsius.

    Formula: C = K - 273.15

    Args:
        kelvin: Temperature in Kelvin

    Returns:
        Temperature in Celsius

    Related: [[obsidian/dimensional-analysis.md|Dimensional Analysis]]
    """
    if kelvin < 0:
        raise ValueError("Temperature cannot be below absolute zero (0 K)")
    return kelvin - 273.15


# Plugin Operations Registry
# Exported for dynamic loading by the plugin system
PLUGIN_OPERATIONS = {  # ^PLUGIN_OPERATIONS
    # Length
    'meters_to_feet': meters_to_feet,
    'feet_to_meters': feet_to_meters,
    'km_to_miles': km_to_miles,
    'miles_to_km': miles_to_km,
    'inches_to_cm': inches_to_cm,
    'cm_to_inches': cm_to_inches,
    # Weight
    'kg_to_lbs': kg_to_lbs,
    'lbs_to_kg': lbs_to_kg,
    'grams_to_oz': grams_to_oz,
    'oz_to_grams': oz_to_grams,
    # Temperature
    'celsius_to_fahrenheit': celsius_to_fahrenheit,
    'fahrenheit_to_celsius': fahrenheit_to_celsius,
    'celsius_to_kelvin': celsius_to_kelvin,
    'kelvin_to_celsius': kelvin_to_celsius,
}
