"""
# Statistics Plugin

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/plugins/statistics.py #domain/statistics #domain/mathematics #layer/plugin-implementation #pattern/plugin-architecture #pattern/strategy/function-registry

## Purpose
Provides statistical operations for data analysis including measures of central tendency and dispersion.

## Related Documentation
- Pattern: [[obsidian/plugin-architecture.md|Plugin Architecture]]
- Concept: [[obsidian/mathematical-structures.md|Mathematical Structures]]

## Plugin Interface
Exports PLUGIN_OPERATIONS dictionary for dynamic loading by the plugin system.

## Used By
- [[../plugin_system.py|Plugin System]]
"""
from typing import List
import math


def mean(values: List[float]) -> float:  # ^mean
    """
    Calculate the arithmetic mean (average) of a list of numbers.

    Args:
        values: List of numbers

    Returns:
        The mean value

    Raises:
        ValueError: If the list is empty

    Related: [[obsidian/mathematical-structures.md|Mathematical Structures]]
    """
    if not values:
        raise ValueError("Cannot calculate mean of empty list")

    return sum(values) / len(values)


def median(values: List[float]) -> float:  # ^median
    """
    Calculate the median (middle value) of a list of numbers.

    Args:
        values: List of numbers

    Returns:
        The median value

    Raises:
        ValueError: If the list is empty

    Related: [[obsidian/mathematical-structures.md|Mathematical Structures]]
    """
    if not values:
        raise ValueError("Cannot calculate median of empty list")

    sorted_values = sorted(values)
    n = len(sorted_values)

    if n % 2 == 0:
        # Even number of elements: average the two middle values
        return (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
    else:
        # Odd number of elements: return the middle value
        return sorted_values[n // 2]


def mode(values: List[float]) -> float:  # ^mode
    """
    Calculate the mode (most frequent value) of a list of numbers.

    Args:
        values: List of numbers

    Returns:
        The mode value

    Raises:
        ValueError: If the list is empty or has no unique mode

    Related: [[obsidian/mathematical-structures.md|Mathematical Structures]]
    """
    if not values:
        raise ValueError("Cannot calculate mode of empty list")

    frequency = {}
    for value in values:
        frequency[value] = frequency.get(value, 0) + 1

    max_freq = max(frequency.values())
    modes = [val for val, freq in frequency.items() if freq == max_freq]

    if len(modes) > 1 and len(modes) == len(frequency):
        raise ValueError("No unique mode: all values appear equally")

    return modes[0]


def variance(values: List[float], sample: bool = True) -> float:  # ^variance
    """
    Calculate the variance of a list of numbers.

    Args:
        values: List of numbers
        sample: If True, calculate sample variance (n-1). If False, population variance (n)

    Returns:
        The variance

    Raises:
        ValueError: If the list is empty or has only one element (for sample variance)

    Related: [[obsidian/mathematical-structures.md|Mathematical Structures]]
    """
    if not values:
        raise ValueError("Cannot calculate variance of empty list")

    if sample and len(values) < 2:
        raise ValueError("Sample variance requires at least 2 values")

    avg = mean(values)
    squared_diffs = [(x - avg) ** 2 for x in values]

    divisor = len(values) - 1 if sample else len(values)
    return sum(squared_diffs) / divisor


def stddev(values: List[float], sample: bool = True) -> float:  # ^stddev
    """
    Calculate the standard deviation of a list of numbers.

    Args:
        values: List of numbers
        sample: If True, calculate sample std dev (n-1). If False, population std dev (n)

    Returns:
        The standard deviation

    Raises:
        ValueError: If the list is empty or has only one element (for sample std dev)

    Related: [[obsidian/mathematical-structures.md|Mathematical Structures]]
    """
    return math.sqrt(variance(values, sample))


def range_stat(values: List[float]) -> float:  # ^range_stat
    """
    Calculate the range (difference between max and min) of a list of numbers.

    Args:
        values: List of numbers

    Returns:
        The range

    Raises:
        ValueError: If the list is empty

    Related: [[obsidian/mathematical-structures.md|Mathematical Structures]]
    """
    if not values:
        raise ValueError("Cannot calculate range of empty list")

    return max(values) - min(values)


# Plugin Operations Registry
# Exported for dynamic loading by the plugin system
PLUGIN_OPERATIONS = {  # ^PLUGIN_OPERATIONS
    'mean': mean,
    'median': median,
    'mode': mode,
    'variance': variance,
    'stddev': stddev,
    'range': range_stat,
}
