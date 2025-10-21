"""
# Linear Algebra Plugin

**File Tags**: #type/code-file
**Inheritable Tags**: #location/code-file/code/plugins/linear_algebra.py #domain/linear-algebra #domain/mathematics #layer/plugin-implementation #pattern/plugin-architecture #pattern/strategy/function-registry

## Purpose
Provides linear algebra operations including vector operations (dot product,
cross product, magnitude, normalization) and matrix operations (multiplication,
transpose, determinant).

## Related Documentation
- Pattern: [[../../obsidian/plugin-architecture|Plugin Architecture]]
- Concept: [[../../obsidian/mathematical-structures|Mathematical Structures]]

## Plugin Interface
Exports PLUGIN_OPERATIONS dictionary for dynamic loading by the plugin system.

## Used By
- [[../plugin_system.py|Plugin System]]
"""
import math
from typing import List, Tuple


def dot_product(v1: List[float], v2: List[float]) -> float:  # ^dot_product
    """
    Calculate dot product of two vectors.

    Formula: v1 · v2 = Σ(v1ᵢ * v2ᵢ)

    Args:
        v1: First vector
        v2: Second vector

    Returns:
        Dot product (scalar value)

    Raises:
        ValueError: If vectors have different dimensions

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must have the same dimension")
    if not v1:
        raise ValueError("Vectors cannot be empty")

    return sum(a * b for a, b in zip(v1, v2))


def cross_product(v1: List[float], v2: List[float]) -> List[float]:  # ^cross_product
    """
    Calculate cross product of two 3D vectors.

    Formula: v1 × v2 = [v1y*v2z - v1z*v2y, v1z*v2x - v1x*v2z, v1x*v2y - v1y*v2x]

    Args:
        v1: First 3D vector [x, y, z]
        v2: Second 3D vector [x, y, z]

    Returns:
        Cross product vector (orthogonal to both inputs)

    Raises:
        ValueError: If vectors are not 3-dimensional

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    if len(v1) != 3 or len(v2) != 3:
        raise ValueError("Cross product requires 3D vectors")

    return [
        v1[1] * v2[2] - v1[2] * v2[1],  # x component
        v1[2] * v2[0] - v1[0] * v2[2],  # y component
        v1[0] * v2[1] - v1[1] * v2[0],  # z component
    ]


def magnitude(v: List[float]) -> float:  # ^magnitude
    """
    Calculate magnitude (Euclidean norm) of a vector.

    Formula: ||v|| = √(Σvᵢ²)

    Args:
        v: Input vector

    Returns:
        Magnitude (length) of the vector

    Raises:
        ValueError: If vector is empty

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    if not v:
        raise ValueError("Vector cannot be empty")

    return math.sqrt(sum(x * x for x in v))


def normalize(v: List[float]) -> List[float]:  # ^normalize
    """
    Normalize a vector to unit length.

    Formula: v̂ = v / ||v||

    Args:
        v: Input vector

    Returns:
        Unit vector in same direction

    Raises:
        ValueError: If vector is zero (cannot normalize)

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    mag = magnitude(v)
    if mag == 0:
        raise ValueError("Cannot normalize zero vector")

    return [x / mag for x in v]


def matrix_multiply(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:  # ^matrix_multiply
    """
    Multiply two matrices.

    Formula: (AB)ᵢⱼ = Σₖ(aᵢₖ * bₖⱼ)

    Args:
        m1: First matrix (m × n)
        m2: Second matrix (n × p)

    Returns:
        Product matrix (m × p)

    Raises:
        ValueError: If matrix dimensions incompatible

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    if not m1 or not m1[0]:
        raise ValueError("First matrix cannot be empty")
    if not m2 or not m2[0]:
        raise ValueError("Second matrix cannot be empty")

    # Validate dimensions
    m1_rows = len(m1)
    m1_cols = len(m1[0])
    m2_rows = len(m2)
    m2_cols = len(m2[0])

    if m1_cols != m2_rows:
        raise ValueError(f"Cannot multiply {m1_rows}×{m1_cols} by {m2_rows}×{m2_cols} matrices")

    # Validate rectangular matrices
    if not all(len(row) == m1_cols for row in m1):
        raise ValueError("First matrix must be rectangular")
    if not all(len(row) == m2_cols for row in m2):
        raise ValueError("Second matrix must be rectangular")

    # Perform multiplication
    result = []
    for i in range(m1_rows):
        row = []
        for j in range(m2_cols):
            value = sum(m1[i][k] * m2[k][j] for k in range(m1_cols))
            row.append(value)
        result.append(row)

    return result


def transpose(m: List[List[float]]) -> List[List[float]]:  # ^transpose
    """
    Transpose a matrix (flip rows and columns).

    Formula: (Aᵀ)ᵢⱼ = Aⱼᵢ

    Args:
        m: Input matrix (m × n)

    Returns:
        Transposed matrix (n × m)

    Raises:
        ValueError: If matrix is empty or not rectangular

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    if not m or not m[0]:
        raise ValueError("Matrix cannot be empty")

    rows = len(m)
    cols = len(m[0])

    # Validate rectangular matrix
    if not all(len(row) == cols for row in m):
        raise ValueError("Matrix must be rectangular")

    # Transpose
    result = []
    for j in range(cols):
        row = [m[i][j] for i in range(rows)]
        result.append(row)

    return result


def determinant(m: List[List[float]]) -> float:  # ^determinant
    """
    Calculate determinant of a 2×2 or 3×3 matrix.

    Formula (2×2): det(A) = a₁₁a₂₂ - a₁₂a₂₁
    Formula (3×3): Uses rule of Sarrus

    Args:
        m: Square matrix (2×2 or 3×3)

    Returns:
        Determinant value

    Raises:
        ValueError: If matrix is not 2×2 or 3×3, or not square

    Related: [[../../obsidian/mathematical-structures|Mathematical Structures]]
    """
    if not m or not m[0]:
        raise ValueError("Matrix cannot be empty")

    rows = len(m)
    cols = len(m[0])

    if rows != cols:
        raise ValueError("Determinant requires square matrix")

    if rows not in (2, 3):
        raise ValueError("Determinant only implemented for 2×2 and 3×3 matrices")

    # Validate rectangular matrix
    if not all(len(row) == cols for row in m):
        raise ValueError("Matrix must be rectangular")

    if rows == 2:
        # 2×2 determinant
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    else:
        # 3×3 determinant (rule of Sarrus)
        return (
            m[0][0] * m[1][1] * m[2][2] +
            m[0][1] * m[1][2] * m[2][0] +
            m[0][2] * m[1][0] * m[2][1] -
            m[0][2] * m[1][1] * m[2][0] -
            m[0][1] * m[1][0] * m[2][2] -
            m[0][0] * m[1][2] * m[2][1]
        )


# Plugin Operations Registry
# Exported for dynamic loading by the plugin system
PLUGIN_OPERATIONS = {  # ^PLUGIN_OPERATIONS
    'dot_product': dot_product,
    'cross_product': cross_product,
    'magnitude': magnitude,
    'normalize': normalize,
    'matrix_multiply': matrix_multiply,
    'transpose': transpose,
    'determinant': determinant,
}
