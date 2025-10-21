"""
# Linear Algebra Plugin Tests

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/test_linear_algebra.py #domain/linear-algebra #domain/testing/unit #layer/test

## Purpose
Unit tests for the linear algebra plugin operations including vector operations
(dot product, cross product, magnitude, normalize) and matrix operations
(multiply, transpose, determinant).

## Related Documentation
- Pattern: [[obsidian/testing-strategy.md|Testing Strategy]]
- Implementation: [[code/plugins/linear_algebra.py|Linear Algebra Plugin]]

## Test Coverage
Tests all linear algebra functions: dot_product, cross_product, magnitude,
normalize, matrix_multiply, transpose, determinant
"""
import unittest
import math
from plugins import linear_algebra


class TestDotProduct(unittest.TestCase):  # ^TestDotProduct
    """
    Tests for the dot product function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_dot_product_basic(self):  # ^TestDotProduct-test_dot_product_basic
        """Test basic dot product calculation."""
        result = linear_algebra.dot_product([1, 2, 3], [4, 5, 6])
        # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
        self.assertEqual(result, 32)

    def test_dot_product_orthogonal(self):  # ^TestDotProduct-test_dot_product_orthogonal
        """Test dot product of orthogonal vectors (should be 0)."""
        result = linear_algebra.dot_product([1, 0], [0, 1])
        self.assertEqual(result, 0)

    def test_dot_product_same_vector(self):  # ^TestDotProduct-test_dot_product_same_vector
        """Test dot product of vector with itself."""
        v = [3, 4]
        result = linear_algebra.dot_product(v, v)
        # Should equal magnitude squared: 3² + 4² = 25
        self.assertEqual(result, 25)

    def test_dot_product_different_dimensions(self):  # ^TestDotProduct-test_dot_product_different_dimensions
        """Test dot product raises error on different dimensions."""
        with self.assertRaises(ValueError):
            linear_algebra.dot_product([1, 2], [1, 2, 3])

    def test_dot_product_empty(self):  # ^TestDotProduct-test_dot_product_empty
        """Test dot product raises error on empty vectors."""
        with self.assertRaises(ValueError):
            linear_algebra.dot_product([], [])


class TestCrossProduct(unittest.TestCase):  # ^TestCrossProduct
    """
    Tests for the cross product function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_cross_product_basic(self):  # ^TestCrossProduct-test_cross_product_basic
        """Test basic cross product calculation."""
        result = linear_algebra.cross_product([1, 0, 0], [0, 1, 0])
        # i × j = k
        self.assertEqual(result, [0, 0, 1])

    def test_cross_product_orthogonality(self):  # ^TestCrossProduct-test_cross_product_orthogonality
        """Test that cross product is orthogonal to both inputs."""
        v1 = [1, 2, 3]
        v2 = [4, 5, 6]
        result = linear_algebra.cross_product(v1, v2)
        # Result should be orthogonal (dot product = 0)
        self.assertEqual(linear_algebra.dot_product(result, v1), 0)
        self.assertEqual(linear_algebra.dot_product(result, v2), 0)

    def test_cross_product_parallel(self):  # ^TestCrossProduct-test_cross_product_parallel
        """Test cross product of parallel vectors (should be zero)."""
        result = linear_algebra.cross_product([2, 4, 6], [1, 2, 3])
        self.assertEqual(result, [0, 0, 0])

    def test_cross_product_anticommutative(self):  # ^TestCrossProduct-test_cross_product_anticommutative
        """Test that v1 × v2 = -(v2 × v1)."""
        v1 = [1, 2, 3]
        v2 = [4, 5, 6]
        result1 = linear_algebra.cross_product(v1, v2)
        result2 = linear_algebra.cross_product(v2, v1)
        # Should be negatives of each other
        self.assertEqual(result1, [-x for x in result2])

    def test_cross_product_wrong_dimension(self):  # ^TestCrossProduct-test_cross_product_wrong_dimension
        """Test cross product raises error on non-3D vectors."""
        with self.assertRaises(ValueError):
            linear_algebra.cross_product([1, 2], [3, 4])


class TestMagnitude(unittest.TestCase):  # ^TestMagnitude
    """
    Tests for the magnitude function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_magnitude_3_4(self):  # ^TestMagnitude-test_magnitude_3_4
        """Test magnitude of 3-4-5 right triangle."""
        result = linear_algebra.magnitude([3, 4])
        self.assertEqual(result, 5.0)

    def test_magnitude_unit_vector(self):  # ^TestMagnitude-test_magnitude_unit_vector
        """Test magnitude of unit vector."""
        result = linear_algebra.magnitude([1, 0, 0])
        self.assertEqual(result, 1.0)

    def test_magnitude_3d(self):  # ^TestMagnitude-test_magnitude_3d
        """Test magnitude in 3D."""
        result = linear_algebra.magnitude([1, 2, 2])
        self.assertEqual(result, 3.0)

    def test_magnitude_empty(self):  # ^TestMagnitude-test_magnitude_empty
        """Test magnitude raises error on empty vector."""
        with self.assertRaises(ValueError):
            linear_algebra.magnitude([])


class TestNormalize(unittest.TestCase):  # ^TestNormalize
    """
    Tests for the normalize function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_normalize_basic(self):  # ^TestNormalize-test_normalize_basic
        """Test normalization produces unit vector."""
        result = linear_algebra.normalize([3, 4])
        self.assertAlmostEqual(result[0], 0.6)
        self.assertAlmostEqual(result[1], 0.8)
        # Check magnitude is 1
        self.assertAlmostEqual(linear_algebra.magnitude(result), 1.0)

    def test_normalize_already_unit(self):  # ^TestNormalize-test_normalize_already_unit
        """Test normalizing a unit vector returns unit vector."""
        result = linear_algebra.normalize([1, 0, 0])
        self.assertEqual(result, [1.0, 0.0, 0.0])

    def test_normalize_preserves_direction(self):  # ^TestNormalize-test_normalize_preserves_direction
        """Test that normalization preserves direction."""
        v = [5, 12]  # magnitude 13
        result = linear_algebra.normalize(v)
        # Should be in same direction (proportional)
        self.assertAlmostEqual(result[0] / result[1], v[0] / v[1])

    def test_normalize_zero_vector(self):  # ^TestNormalize-test_normalize_zero_vector
        """Test normalize raises error on zero vector."""
        with self.assertRaises(ValueError):
            linear_algebra.normalize([0, 0, 0])


class TestMatrixMultiply(unittest.TestCase):  # ^TestMatrixMultiply
    """
    Tests for the matrix multiplication function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_matrix_multiply_basic(self):  # ^TestMatrixMultiply-test_matrix_multiply_basic
        """Test basic 2×2 matrix multiplication."""
        m1 = [[1, 2], [3, 4]]
        m2 = [[5, 6], [7, 8]]
        result = linear_algebra.matrix_multiply(m1, m2)
        # [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]]
        # [[19, 22], [43, 50]]
        self.assertEqual(result, [[19, 22], [43, 50]])

    def test_matrix_multiply_identity(self):  # ^TestMatrixMultiply-test_matrix_multiply_identity
        """Test multiplication by identity matrix."""
        m = [[1, 2], [3, 4]]
        identity = [[1, 0], [0, 1]]
        result = linear_algebra.matrix_multiply(m, identity)
        self.assertEqual(result, m)

    def test_matrix_multiply_non_square(self):  # ^TestMatrixMultiply-test_matrix_multiply_non_square
        """Test multiplication of non-square matrices."""
        m1 = [[1, 2, 3],]  # 1×3
        m2 = [[4], [5], [6]]  # 3×1
        result = linear_algebra.matrix_multiply(m1, m2)
        # Result: [1*4 + 2*5 + 3*6] = [32]
        self.assertEqual(result, [[32],])

    def test_matrix_multiply_incompatible_dimensions(self):  # ^TestMatrixMultiply-test_matrix_multiply_incompatible_dimensions
        """Test matrix multiply raises error on incompatible dimensions."""
        m1 = [[1, 2],]  # 1x2 matrix
        m2 = [[3, 4, 5],]  # 1x3 matrix
        with self.assertRaises(ValueError):
            linear_algebra.matrix_multiply(m1, m2)

    def test_matrix_multiply_empty(self):  # ^TestMatrixMultiply-test_matrix_multiply_empty
        """Test matrix multiply raises error on empty matrix."""
        with self.assertRaises(ValueError):
            linear_algebra.matrix_multiply([], [1])

    def test_matrix_multiply_non_rectangular(self):  # ^TestMatrixMultiply-test_matrix_multiply_non_rectangular
        """Test matrix multiply raises error on non-rectangular matrix."""
        m1 = [[1, 2], [3]]  # Invalid - not rectangular
        m2 = [[4], [5]]
        with self.assertRaises(ValueError):
            linear_algebra.matrix_multiply(m1, m2)


class TestTranspose(unittest.TestCase):  # ^TestTranspose
    """
    Tests for the transpose function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_transpose_square(self):  # ^TestTranspose-test_transpose_square
        """Test transpose of square matrix."""
        m = [[1, 2], [3, 4]]
        result = linear_algebra.transpose(m)
        self.assertEqual(result, [[1, 3], [2, 4]])

    def test_transpose_non_square(self):  # ^TestTranspose-test_transpose_non_square
        """Test transpose of non-square matrix."""
        m = [[1, 2, 3], [4, 5, 6]]  # 2×3
        result = linear_algebra.transpose(m)
        # Should become 3×2
        self.assertEqual(result, [[1, 4], [2, 5], [3, 6]])

    def test_transpose_row_vector(self):  # ^TestTranspose-test_transpose_row_vector
        """Test transpose of row vector to column vector."""
        m = [[1, 2, 3],]  # 1×3
        result = linear_algebra.transpose(m)
        self.assertEqual(result, [[1], [2], [3]])  # 3×1

    def test_transpose_symmetric(self):  # ^TestTranspose-test_transpose_symmetric
        """Test transpose of symmetric matrix (should equal itself)."""
        m = [[1, 2, 3], [2, 4, 5], [3, 5, 6]]
        result = linear_algebra.transpose(m)
        self.assertEqual(result, m)

    def test_transpose_double(self):  # ^TestTranspose-test_transpose_double
        """Test that double transpose returns original."""
        m = [[1, 2], [3, 4], [5, 6]]
        result = linear_algebra.transpose(linear_algebra.transpose(m))
        self.assertEqual(result, m)

    def test_transpose_empty(self):  # ^TestTranspose-test_transpose_empty
        """Test transpose raises error on empty matrix."""
        with self.assertRaises(ValueError):
            linear_algebra.transpose([])

    def test_transpose_non_rectangular(self):  # ^TestTranspose-test_transpose_non_rectangular
        """Test transpose raises error on non-rectangular matrix."""
        m = [[1, 2], [3]]  # Invalid
        with self.assertRaises(ValueError):
            linear_algebra.transpose(m)


class TestDeterminant(unittest.TestCase):  # ^TestDeterminant
    """
    Tests for the determinant function.

    Related: [[obsidian/testing-strategy.md|Testing Strategy]]
    """

    def test_determinant_2x2(self):  # ^TestDeterminant-test_determinant_2x2
        """Test determinant of 2×2 matrix."""
        m = [[1, 2], [3, 4]]
        result = linear_algebra.determinant(m)
        # 1*4 - 2*3 = -2
        self.assertEqual(result, -2)

    def test_determinant_2x2_identity(self):  # ^TestDeterminant-test_determinant_2x2_identity
        """Test determinant of 2×2 identity (should be 1)."""
        m = [[1, 0], [0, 1]]
        result = linear_algebra.determinant(m)
        self.assertEqual(result, 1)

    def test_determinant_3x3(self):  # ^TestDeterminant-test_determinant_3x3
        """Test determinant of 3×3 matrix."""
        m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        result = linear_algebra.determinant(m)
        # This is a singular matrix, det should be 0
        self.assertEqual(result, 0)

    def test_determinant_3x3_identity(self):  # ^TestDeterminant-test_determinant_3x3_identity
        """Test determinant of 3×3 identity (should be 1)."""
        m = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        result = linear_algebra.determinant(m)
        self.assertEqual(result, 1)

    def test_determinant_3x3_nonzero(self):  # ^TestDeterminant-test_determinant_3x3_nonzero
        """Test determinant of 3×3 matrix with known value."""
        m = [[2, 3, 1], [1, 2, 3], [3, 1, 2]]
        result = linear_algebra.determinant(m)
        # Calculate: 2*2*2 + 3*3*3 + 1*1*1 - 1*2*3 - 3*1*2 - 2*3*1
        # = 8 + 27 + 1 - 6 - 6 - 6 = 18
        self.assertEqual(result, 18)

    def test_determinant_non_square(self):  # ^TestDeterminant-test_determinant_non_square
        """Test determinant raises error on non-square matrix."""
        m = [[1, 2, 3], [4, 5, 6]]
        with self.assertRaises(ValueError):
            linear_algebra.determinant(m)

    def test_determinant_4x4(self):  # ^TestDeterminant-test_determinant_4x4
        """Test determinant raises error on 4×4 matrix (not implemented)."""
        m = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        with self.assertRaises(ValueError):
            linear_algebra.determinant(m)

    def test_determinant_empty(self):  # ^TestDeterminant-test_determinant_empty
        """Test determinant raises error on empty matrix."""
        with self.assertRaises(ValueError):
            linear_algebra.determinant([])


if __name__ == '__main__':
    unittest.main()
