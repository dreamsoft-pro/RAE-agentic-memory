"""Unit tests for byte-level quantization module."""

import math
import struct
import pytest
from rae_core.math.quantization_bytes import (
    quantize_vector_bytes,
    dequantize_vector_bytes,
    dot_product_bytes,
    cosine_similarity_bytes,
    SCALE_FACTOR
)

def test_quantize_bytes_empty():
    assert quantize_vector_bytes([]) == b""

def test_quantize_bytes_basic():
    vec = [1.0, -1.0, 0.5]
    res = quantize_vector_bytes(vec)
    assert len(res) == 12
    # Check big-endian int32
    assert struct.unpack(">3i", res) == (SCALE_FACTOR, -SCALE_FACTOR, SCALE_FACTOR // 2)

def test_quantize_bytes_clamping():
    # 2^31 / SCALE_FACTOR is approx 32768
    huge = 1000000.0
    res = quantize_vector_bytes([huge, -huge])
    assert struct.unpack(">2i", res) == (2147483647, -2147483648)

def test_quantize_bytes_non_finite():
    with pytest.raises(ValueError, match="Non-finite value"):
        quantize_vector_bytes([float('nan')])

def test_dequantize_bytes_empty():
    assert dequantize_vector_bytes(b"") == []

def test_dequantize_bytes_basic():
    data = struct.pack(">2i", SCALE_FACTOR, SCALE_FACTOR // 4)
    assert dequantize_vector_bytes(data) == [1.0, 0.25]

def test_dot_product_bytes():
    v1 = quantize_vector_bytes([1.0, 2.0])
    v2 = quantize_vector_bytes([0.5, 3.0])
    # 1.0*0.5 + 2.0*3.0 = 0.5 + 6.0 = 6.5
    expected = int(6.5 * SCALE_FACTOR * SCALE_FACTOR)
    assert dot_product_bytes(v1, v2) == expected

def test_dot_product_bytes_mismatch():
    v1 = quantize_vector_bytes([1.0])
    v2 = quantize_vector_bytes([1.0, 2.0])
    with pytest.raises(ValueError, match="dimension mismatch"):
        dot_product_bytes(v1, v2)

def test_cosine_similarity_bytes():
    v1 = quantize_vector_bytes([1.0, 0.0])
    v2 = quantize_vector_bytes([1.0, 1.0])
    # cos(45 deg) = 1/sqrt(2) approx 0.7071
    res = cosine_similarity_bytes(v1, v2)
    assert abs(res - 1.0/math.sqrt(2)) < 1e-5

def test_cosine_similarity_bytes_zero():
    v1 = quantize_vector_bytes([0.0, 0.0])
    v2 = quantize_vector_bytes([1.0, 1.0])
    assert cosine_similarity_bytes(v1, v2) == 0.0
