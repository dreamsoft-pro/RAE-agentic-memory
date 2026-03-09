"""Unit tests for fixed-point quantization module."""

import math
import pytest
from rae_core.math.quantization import (
    quantize_vector,
    dequantize_vector,
    dot_product_fixed,
    cosine_similarity_fixed,
    SCALE_FACTOR
)

def test_quantize_empty():
    assert quantize_vector([]) == []

def test_quantize_basic():
    vec = [0.5, -0.25, 1.0]
    expected = [
        int(0.5 * SCALE_FACTOR),
        int(-0.25 * SCALE_FACTOR),
        int(1.0 * SCALE_FACTOR)
    ]
    assert quantize_vector(vec) == expected

def test_quantize_non_finite():
    with pytest.raises(ValueError, match="Non-finite value"):
        quantize_vector([1.0, float('inf')])
    with pytest.raises(ValueError, match="Non-finite value"):
        quantize_vector([float('nan'), 0.0])

def test_dequantize_empty():
    assert dequantize_vector([]) == []

def test_dequantize_basic():
    vec = [SCALE_FACTOR, SCALE_FACTOR // 2]
    expected = [1.0, 0.5]
    assert dequantize_vector(vec) == expected

def test_dot_product_fixed():
    vec_a = [SCALE_FACTOR, 0]
    vec_b = [SCALE_FACTOR, SCALE_FACTOR]
    # (1.0 * 1.0) + (0 * 1.0) = 1.0
    # In fixed point: SCALE^2
    expected = SCALE_FACTOR * SCALE_FACTOR
    assert dot_product_fixed(vec_a, vec_b) == expected

def test_dot_product_mismatch():
    with pytest.raises(ValueError, match="dimension mismatch"):
        dot_product_fixed([1], [1, 2])

def test_cosine_similarity_fixed():
    # Orthogonal
    assert cosine_similarity_fixed([SCALE_FACTOR, 0], [0, SCALE_FACTOR]) == 0.0
    
    # Identical
    vec = [SCALE_FACTOR, SCALE_FACTOR]
    assert abs(cosine_similarity_fixed(vec, vec) - 1.0) < 1e-9
    
    # Zero vector
    assert cosine_similarity_fixed([0, 0], [SCALE_FACTOR, SCALE_FACTOR]) == 0.0
    assert cosine_similarity_fixed([SCALE_FACTOR, SCALE_FACTOR], [0, 0]) == 0.0

def test_quantize_dequantize_roundtrip():
    original = [0.12345, -0.6789, 0.999]
    quantized = quantize_vector(original)
    recovered = dequantize_vector(quantized)
    
    for o, r in zip(original, recovered):
        # Error should be less than 1/SCALE_FACTOR
        assert abs(o - r) <= (1.0 / SCALE_FACTOR)
