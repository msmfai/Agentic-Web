"""
# Statistics Plugin Tests

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/test_statistics.py #domain/statistics #domain/testing #domain/testing/unit #layer/test #category/unit-test

## Purpose
Unit tests for the statistics plugin operations.

## Related Documentation
- Pattern: [[obsidian/testing-strategy.md|Testing Strategy]]
- Implementation: [[code/plugins/statistics.py|Statistics Plugin]]

## Test Coverage
Tests all statistical functions: mean, median, mode, variance, stddev, range
"""
import unittest
from plugins import statistics


class TestMean(unittest.TestCase):  # ^TestMean
    """
    Tests for the mean (average) function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_mean_basic(self):  # ^TestMean-test_mean_basic
        """Test mean of simple list."""
        result = statistics.mean([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)

    def test_mean_floats(self):  # ^TestMean-test_mean_floats
        """Test mean with floating point numbers."""
        result = statistics.mean([1.5, 2.5, 3.5])
        self.assertAlmostEqual(result, 2.5)

    def test_mean_single_value(self):  # ^TestMean-test_mean_single_value
        """Test mean of single value."""
        result = statistics.mean([42])
        self.assertEqual(result, 42.0)

    def test_mean_empty_list(self):  # ^TestMean-test_mean_empty_list
        """Test mean raises error on empty list."""
        with self.assertRaises(ValueError):
            statistics.mean([])


class TestMedian(unittest.TestCase):  # ^TestMedian
    """
    Tests for the median function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_median_odd_count(self):  # ^TestMedian-test_median_odd_count
        """Test median with odd number of elements."""
        result = statistics.median([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)

    def test_median_even_count(self):  # ^TestMedian-test_median_even_count
        """Test median with even number of elements."""
        result = statistics.median([1, 2, 3, 4])
        self.assertEqual(result, 2.5)

    def test_median_unsorted(self):  # ^TestMedian-test_median_unsorted
        """Test median with unsorted data."""
        result = statistics.median([5, 1, 3, 2, 4])
        self.assertEqual(result, 3.0)

    def test_median_empty_list(self):  # ^TestMedian-test_median_empty_list
        """Test median raises error on empty list."""
        with self.assertRaises(ValueError):
            statistics.median([])


class TestMode(unittest.TestCase):  # ^TestMode
    """
    Tests for the mode function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_mode_single_mode(self):  # ^TestMode-test_mode_single_mode
        """Test mode with clear most frequent value."""
        result = statistics.mode([1, 2, 2, 3, 4])
        self.assertEqual(result, 2)

    def test_mode_all_same(self):  # ^TestMode-test_mode_all_same
        """Test mode when all values are the same."""
        result = statistics.mode([5, 5, 5, 5])
        self.assertEqual(result, 5)

    def test_mode_no_unique_mode(self):  # ^TestMode-test_mode_no_unique_mode
        """Test mode raises error when no unique mode exists."""
        with self.assertRaises(ValueError):
            statistics.mode([1, 2, 3, 4])

    def test_mode_empty_list(self):  # ^TestMode-test_mode_empty_list
        """Test mode raises error on empty list."""
        with self.assertRaises(ValueError):
            statistics.mode([])


class TestVariance(unittest.TestCase):  # ^TestVariance
    """
    Tests for the variance function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_variance_sample(self):  # ^TestVariance-test_variance_sample
        """Test sample variance calculation."""
        result = statistics.variance([2, 4, 4, 4, 5, 5, 7, 9], sample=True)
        self.assertAlmostEqual(result, 4.571, places=3)

    def test_variance_population(self):  # ^TestVariance-test_variance_population
        """Test population variance calculation."""
        result = statistics.variance([2, 4, 4, 4, 5, 5, 7, 9], sample=False)
        self.assertAlmostEqual(result, 4.0, places=3)

    def test_variance_empty_list(self):  # ^TestVariance-test_variance_empty_list
        """Test variance raises error on empty list."""
        with self.assertRaises(ValueError):
            statistics.variance([])

    def test_variance_single_value_sample(self):  # ^TestVariance-test_variance_single_value_sample
        """Test sample variance raises error with single value."""
        with self.assertRaises(ValueError):
            statistics.variance([5], sample=True)


class TestStdDev(unittest.TestCase):  # ^TestStdDev
    """
    Tests for the standard deviation function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_stddev_sample(self):  # ^TestStdDev-test_stddev_sample
        """Test sample standard deviation."""
        result = statistics.stddev([2, 4, 4, 4, 5, 5, 7, 9], sample=True)
        self.assertAlmostEqual(result, 2.138, places=3)

    def test_stddev_population(self):  # ^TestStdDev-test_stddev_population
        """Test population standard deviation."""
        result = statistics.stddev([2, 4, 4, 4, 5, 5, 7, 9], sample=False)
        self.assertAlmostEqual(result, 2.0, places=3)


class TestRange(unittest.TestCase):  # ^TestRange
    """
    Tests for the range function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_range_basic(self):  # ^TestRange-test_range_basic
        """Test range calculation."""
        result = statistics.range_stat([1, 2, 3, 4, 5])
        self.assertEqual(result, 4)

    def test_range_negative(self):  # ^TestRange-test_range_negative
        """Test range with negative numbers."""
        result = statistics.range_stat([-5, -2, 0, 3, 10])
        self.assertEqual(result, 15)

    def test_range_empty_list(self):  # ^TestRange-test_range_empty_list
        """Test range raises error on empty list."""
        with self.assertRaises(ValueError):
            statistics.range_stat([])


if __name__ == '__main__':
    unittest.main()
