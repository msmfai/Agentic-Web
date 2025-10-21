---
tags:
  - type/concept
  - domain/unit-conversion
  - category/theory
---

# Dimensional Analysis

**Concept**: Systematic approach to unit conversion and dimensional consistency

## Overview

Dimensional analysis is a method for converting between different units of measurement while maintaining physical consistency. It ensures that calculations involving physical quantities respect dimensional homogeneity (all terms must have compatible dimensions).

## Core Principles

### Dimensional Homogeneity

**Principle**: Only quantities with the same dimensions can be added, subtracted, or equated.

**Valid operations**:
- 5 meters + 3 meters = 8 meters ✓
- 10 kilograms - 2 kilograms = 8 kilograms ✓

**Invalid operations**:
- 5 meters + 3 kilograms = ??? ✗ (incompatible dimensions)
- 10 seconds × 2 meters = 20 meter-seconds (valid, but new dimension)

### Conversion Factors

**Definition**: Ratios equal to 1 that change units without changing value

**Examples**:
- 1 meter / 3.28084 feet = 1 (by definition)
- 1 kilogram / 2.20462 pounds = 1
- (°F - 32) × 5/9 = °C (affine transformation)

**Usage**: Multiply by conversion factors to transform units while preserving value

## Unit Systems

### Metric System (SI)

**Base units**:

- Length: meter (m)
- Mass: kilogram (kg)
- Time: second (s)
- Temperature: Kelvin (K)

**Properties**:
- Decimal-based (powers of 10)
- Internally consistent
- Used in science globally

**Prefixes**:
- kilo- (k) = 10³ = 1,000
- centi- (c) = 10⁻² = 0.01
- milli- (m) = 10⁻³ = 0.001

### Imperial System

**Base units**:

- Length: inch, foot, yard, mile
- Mass: ounce, pound, ton
- Temperature: Fahrenheit (°F)

**Properties**:
- Non-decimal relationships (12 inches = 1 foot, 3 feet = 1 yard)
- Historical origin
- Used primarily in United States

### Temperature Scales

**Three common scales**:

#### Celsius (°C)
- Freezing point of water: 0°C
- Boiling point of water: 100°C
- Absolute zero: -273.15°C
- Used in science and most countries

#### Fahrenheit (°F)
- Freezing point of water: 32°F
- Boiling point of water: 212°F
- Absolute zero: -459.67°F
- Used in United States

#### Kelvin (K)
- Absolute zero: 0 K
- Freezing point of water: 273.15 K
- Boiling point of water: 373.15 K
- SI base unit, no negative values

## Conversion Categories

### Length Conversions

**Metric ↔ Imperial**:

- 1 meter = 3.28084 feet
- 1 kilometer = 0.621371 miles
- 1 inch = 2.54 centimeters (exact)

**Implementation**: [[code/plugins/units.py|Unit Conversion Plugin]]

**Pattern**: Simple multiplication by constant factor

```
feet = meters × 3.28084
meters = feet × 0.3048
```

### Weight/Mass Conversions

**Metric ↔ Imperial**:

- 1 kilogram = 2.20462 pounds
- 1 gram = 0.035274 ounces

**Important distinction**:

- **Mass**: Intrinsic property (kilograms, grams)
- **Weight**: Force due to gravity (technically newtons)
- In common usage, "weight" refers to mass

**Implementation**: [[code/plugins/units.py#^kg_to_lbs|kg_to_lbs Function]]

**Pattern**: Simple multiplication by constant factor

```
pounds = kilograms × 2.20462
kilograms = pounds × 0.453592
```

### Temperature Conversions

**Special case**: Temperature is an **affine** space, not a vector space

**Celsius ↔ Fahrenheit** (affine transformation):

```
°F = °C × 9/5 + 32
°C = (°F - 32) × 5/9
```

**Celsius ↔ Kelvin** (simple translation):

```
K = °C + 273.15
°C = K - 273.15
```

**Why affine?** Zero points are arbitrary (except Kelvin). The zero of Celsius (freezing water) is not the same as zero Fahrenheit.

**Absolute zero**:

- 0 K (by definition)
- -273.15°C
- -459.67°F

**Implementation**: [[code/plugins/units.py#^celsius_to_fahrenheit|Temperature Conversions]]

## Mathematical Properties

### Multiplicative Conversions

**Pattern**: `target_unit = source_value × conversion_factor`

**Properties**:

- Commutative: Order doesn't matter
- Associative: Can group conversions
- Identity: Multiplying by 1 preserves value
- Inverse: Forward and backward conversions are reciprocals

**Example (chaining)**:

```
inches → cm → meters
5 inches × 2.54 cm/inch × 0.01 m/cm = 0.127 meters
```

### Affine Conversions

**Pattern**: `target = source × scale + offset`

**Properties**:

- NOT linear (due to offset)
- Cannot chain like multiplicative conversions
- Requires special handling
- Only appears in temperature conversions

**Example (why you can't chain)**:

```
0°C → 32°F → Kelvin
Wrong: 32°F = 273.15 K (should be 273.15 K)
Correct: 0°C → 273.15 K (then convert to F if needed)
```

## Validation and Edge Cases

### Physical Constraints

**Length/Mass**: Cannot be negative

```python
if meters < 0:
    raise ValueError("Length cannot be negative")
```

**Temperature**: Cannot be below absolute zero

```python
if celsius < -273.15:
    raise ValueError("Temperature below absolute zero")
```

### Precision Considerations

**Conversion factors**:

- Use sufficient precision (e.g., 3.28084, not 3.28)
- Exact conversions: 1 inch = 2.54 cm (by definition)
- Approximate conversions: Most metric ↔ imperial

**Rounding**:

- Perform conversions first, then round
- Don't round intermediate values in chains
- Consider significant figures in scientific contexts

### Numerical Stability

**Avoid**:

- Very large or very small conversion factors
- Deep chains of conversions (accumulates error)

**Prefer**:

- Direct conversions when available
- Conversions through standard units (SI)

## Related Patterns

### Function Registry Pattern

All conversion functions follow same signature:

```python
def unit_a_to_unit_b(value: float) -> float:
    validate(value)
    return value * CONVERSION_FACTOR
```

**Benefits**:

- Uniform interface
- Easy to add new conversions
- Plugin-compatible
- Testable

**Implementation**: [[code/plugins/units.py|Unit Conversion Plugin]]

### Bidirectional Conversions

Every conversion has an inverse:

- `meters_to_feet` ↔ `feet_to_meters`
- `kg_to_lbs` ↔ `lbs_to_kg`
- `celsius_to_fahrenheit` ↔ `fahrenheit_to_celsius`

**Relationship**: `factor_inverse = 1 / factor_forward`

**Validation**: `convert_back(convert_forward(x)) ≈ x`

## Common Conversion Factors

### Length

| From       | To          | Factor   |
|------------|-------------|----------|
| meters     | feet        | 3.28084  |
| km         | miles       | 0.621371 |
| inches     | cm          | 2.54     |

### Weight

| From       | To          | Factor   |
|------------|-------------|----------|
| kg         | lbs         | 2.20462  |
| grams      | oz          | 0.035274 |

### Temperature

| From       | To          | Formula           |
|------------|-------------|-------------------|
| Celsius    | Fahrenheit  | C × 9/5 + 32      |
| Celsius    | Kelvin      | C + 273.15        |
| Fahrenheit | Celsius     | (F - 32) × 5/9    |

## Implementation Strategy

### Input Validation

1. Check for negative values (length, mass)
2. Check for below absolute zero (temperature)
3. Raise `ValueError` with descriptive message

### Computation

1. Apply conversion formula
2. Use precise conversion factors
3. Return result directly (no rounding)

### Testing

**Test cases**:

- Known values (0°C = 32°F, 1 inch = 2.54 cm)
- Round-trip conversions (A→B→A)
- Edge cases (absolute zero, zero values)
- Invalid inputs (negative lengths, sub-zero temps)

**Implementation**: [[code/test_units.py|Unit Conversion Tests]]

## Related Documentation

**Implementations**:

- [[code/plugins/units.py|Unit Conversion Plugin]]
- [[code/test_units.py|Unit Conversion Tests]] (to be created)

**Patterns**:

- [[plugin-architecture.md|Plugin Architecture]]
- [[mathematical-structures.md|Mathematical Structures]]

**Related Domains**:

- [[code/plugins/finance.py|Finance Plugin]] - Also deals with conversions (currency, time value)
