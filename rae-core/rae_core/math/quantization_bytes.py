"""Service for converting vectors to bytes (Float32 A/B Test)."""

import math
import struct
from typing import Final, Sequence

def quantize_vector_bytes(vector: Sequence[float]) -> bytes:
    """Konwersja wektora float na spakowany ciąg bajtów float32 (Big Endian).
    
    Format: >f (32-bit big-endian float).
    Wyłączenie kwantyzacji dla testu A/B (powrót do Float32).
    """
    if not vector:
        return b""

    # Alokacja bufora: 4 bajty na każdą liczbę
    packed_data = bytearray(len(vector) * 4)
    
    offset = 0
    fmt = ">f"  # Big-endian float32
    pack = struct.pack_into
    
    for val in vector:
        if not math.isfinite(val):
            raise ValueError(f"Non-finite value in vector: {val}")
            
        pack(fmt, packed_data, offset, float(val))
        offset += 4
        
    return bytes(packed_data)


def dequantize_vector_bytes(data: bytes) -> list[float]:
    """Konwersja spakowanych bajtów float32 z powrotem na listę float.
    """
    if not data:
        return []
        
    count = len(data) // 4
    fmt = f">{count}f"
    
    floats = struct.unpack(fmt, data)
    
    return list(floats)


def dot_product_bytes(vec_a_bytes: bytes, vec_b_bytes: bytes) -> float:
    """Obliczenie iloczynu skalarnego bezpośrednio na bajtach (float32).
    """
    len_a = len(vec_a_bytes)
    len_b = len(vec_b_bytes)
    
    if len_a != len_b:
        raise ValueError(f"Vector dimension mismatch: {len_a} vs {len_b} bytes")
        
    count = len_a // 4
    fmt = f">{count}f"
    
    floats_a = struct.unpack(fmt, vec_a_bytes)
    floats_b = struct.unpack(fmt, vec_b_bytes)
    
    total = 0.0
    for a, b in zip(floats_a, floats_b):
        total += a * b
        
    return total


def cosine_similarity_bytes(vec_a_bytes: bytes, vec_b_bytes: bytes) -> float:
    """Obliczenie podobieństwa kosinusowego na bajtach float32.
    """
    dot = dot_product_bytes(vec_a_bytes, vec_b_bytes)
    
    norm_a_sq = dot_product_bytes(vec_a_bytes, vec_a_bytes)
    norm_b_sq = dot_product_bytes(vec_b_bytes, vec_b_bytes)
    
    if norm_a_sq == 0 or norm_b_sq == 0:
        return 0.0
        
    return dot / (math.sqrt(norm_a_sq) * math.sqrt(norm_b_sq))
