import pytest
import sys
import os
from unittest.mock import MagicMock

# Dodaj katalog główny do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from splitter import SplitPDF

class MockConfig:
    def __init__(self):
        self.settings = {
            "graphic_settings": {},
            "billboard_settings": {},
            "scaling_settings": {
                "scale_non_uniform": False,
                "scale_den": 10.0, # Skala 10x
            }
        }

@pytest.fixture
def splitter():
    mock_cfg = MockConfig()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("splitter.verify_license", lambda **kwargs: False)
        s = SplitPDF(mock_cfg)
        return s

def test_billboard_6x3_scale_1_10(splitter):
    # KROK 1: Symulacja pliku wejściowego 1:10 (60cm x 30cm)
    # Wymiary w punktach (1 mm = 2.83465 pt)
    input_w_mm = 600.0
    input_h_mm = 300.0
    splitter.width = input_w_mm * splitter.mm
    splitter.height = input_h_mm * splitter.mm

    # KROK 2: Parametry podziału
    # 6x3m docelowo, 2 rzędy, 5 kolumn
    rows = 2
    cols = 5
    overlap_mm = 20.0
    white_stripe_mm = 10.0
    
    # Skala 10x
    scale_factor = 10.0

    # KROK 3: Obliczenia
    # calculate_dimensions przyjmuje overlap w skali DOCELOWEJ (mm na wydruku)
    # i parametry sx, sy (mnożniki skali)
    splitter.calculate_dimensions(
        overlap=overlap_mm, 
        rows=rows, 
        cols=cols, 
        white_stripe=white_stripe_mm, 
        add_white_to_overlap=True,
        sx=scale_factor,
        sy=scale_factor
    )

    # KROK 4: Weryfikacja
    # Oczekiwana efektywna zakładka na łączeniach = 20 + 10 = 30mm
    effective_overlap = overlap_mm + white_stripe_mm
    
    # Oczekiwana szerokość brytu (z zakładkami)
    # Total target width = 6000mm
    # Total overlaps added width = (cols - 1) * effective_overlap = 4 * 30 = 120mm
    # Total material width = 6120mm
    # Slice width = 6120 / 5 = 1224mm
    expected_slice_width_mm = 1224.0

    # Oczekiwana wysokość brytu (z zakładkami)
    # Total target height = 3000mm
    # Total overlaps added height = (rows - 1) * effective_overlap = 1 * 30 = 30mm
    # Total material height = 3030mm
    # Slice height = 3030 / 2 = 1515mm
    expected_slice_height_mm = 1515.0

    # slice_width/height w splitterze to wymiary WSPÓŁRZĘDNYCH PLIKU ŹRÓDŁOWEGO (przed skalowaniem).
    # Aby uzyskać wymiar na wydruku, musimy pomnożyć przez scale_factor.
    actual_w_mm = (splitter.slice_width / splitter.mm) * scale_factor
    actual_h_mm = (splitter.slice_height / splitter.mm) * scale_factor

    print(f"\n--- WYNIKI TESTU 6x3m (Wejście 60x30cm, Skala 10x) ---")
    print(f"Wejście: {input_w_mm}x{input_h_mm} mm")
    print(f"Skala: {scale_factor}x")
    print(f"Oczekiwany bryt: {expected_slice_width_mm} x {expected_slice_height_mm} mm")
    print(f"Obliczony bryt (na wyjściu): {actual_w_mm:.2f} x {actual_h_mm:.2f} mm")

    # Asercja z tolerancją na błędy zmiennoprzecinkowe (0.01mm)
    assert abs(actual_w_mm - expected_slice_width_mm) < 0.01
    assert abs(actual_h_mm - expected_slice_height_mm) < 0.01
