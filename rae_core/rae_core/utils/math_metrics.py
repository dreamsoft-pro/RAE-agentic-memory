# /app/src/rae_core/rae_core/utils/math_metrics.py
import math
from collections import Counter

def calculate_ttr(text: str) -> float:
    words = text.split()
    unique_words = set(words)
    return len(unique_words) / len(words) if words else 0