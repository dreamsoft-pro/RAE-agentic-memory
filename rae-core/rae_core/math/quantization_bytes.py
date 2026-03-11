"""Service for converting between float and fixed-point integer vectors (Deterministyczna Wersja)."""

import math
import struct
from typing import Final, Sequence

# Stała skalowania (Precision configuration for Q16.16 equivalent)
Q16_SCALE: Final[float] = 65536.0

def quantize_vector_bytes(vector: Sequence[float]) -> bytes:
    """Konwersja wektora float na spakowany ciąg bajtów int32 (Big Endian)."""
    if not vector:
        return b""

    packed_data = bytearray(len(vector) * 4)
    offset = 0
    fmt = ">i"
    pack = struct.pack_into
    
    for val in vector:
        if not math.isfinite(val):
            raise ValueError(f"Non-finite value in vector: {val}")
        
        # Mnożenie przez skalę i rzutowanie na int (obcięcie do stałoprzecinkowej)
        int_val = int(val * Q16_SCALE)
        
        # Zapobieganie przepełnieniu int32
        if int_val > 2147483647: int_val = 2147483647
        if int_val < -2147483648: int_val = -2147483648
            
        pack(fmt, packed_data, offset, int_val)
        offset += 4
        
    return bytes(packed_data)

def dequantize_vector_bytes(data: bytes) -> list[float]:
    """Konwersja spakowanych bajtów int32 z powrotem na listę float."""
    if not data:
        return []
        
    count = len(data) // 4
    fmt = f">{count}i"
    
    ints = struct.unpack(fmt, data)
    
    # Dzielenie przez skalę, aby przywrócić float
    return [float(x) / Q16_SCALE for x in ints]

def dot_product_bytes(vec_a_bytes: bytes, vec_b_bytes: bytes) -> float:
    """Obliczenie iloczynu skalarnego bezpośrednio na bajtach (int32)."""
    len_a = len(vec_a_bytes)
    len_b = len(vec_b_bytes)
    
    if len_a != len_b:
        raise ValueError(f"Vector dimension mismatch: {len_a} vs {len_b} bytes")
        
    count = len_a // 4
    fmt = f">{count}i"
    
    ints_a = struct.unpack(fmt, vec_a_bytes)
    ints_b = struct.unpack(fmt, vec_b_bytes)
    
    total = 0
    for a, b in zip(ints_a, ints_b):
        total += a * b
        
    # Ponieważ mnożymy dwie liczby przeskalowane, wynik jest przeskalowany do kwadratu
    return float(total) / (Q16_SCALE * Q16_SCALE)

def cosine_similarity_bytes(vec_a_bytes: bytes, vec_b_bytes: bytes) -> float:
    """Obliczenie podobieństwa kosinusowego na bajtach int32."""
    dot = dot_product_bytes(vec_a_bytes, vec_b_bytes)
    
    norm_a_sq = dot_product_bytes(vec_a_bytes, vec_a_bytes)
    norm_b_sq = dot_product_bytes(vec_b_bytes, vec_b_bytes)
    
    if norm_a_sq == 0 or norm_b_sq == 0:
        return 0.0
        
    return dot / (math.sqrt(norm_a_sq) * math.sqrt(norm_b_sq))
