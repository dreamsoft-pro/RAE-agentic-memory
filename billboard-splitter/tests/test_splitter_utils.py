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
            "graphic_settings": {"code_settings": {}},
            "billboard_settings": {},
            "scaling_settings": {}
        }

@pytest.fixture
def splitter():
    mock_cfg = MockConfig()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("splitter.verify_license", lambda **kwargs: False)
        s = SplitPDF(mock_cfg)
        return s

def test_generate_barcode_data_simple(splitter):
    """Testuje generowanie danych kodu dla prostej nazwy pliku."""
    path = "/path/to/moj_plik.pdf"
    slice_name = "0A01"
    result = splitter.generate_barcode_data(path, slice_name)
    assert result == "moj_plik"

def test_generate_barcode_data_pattern(splitter):
    """Testuje generowanie danych kodu dla nazwy pasującej do wzorca (cyfry_cyfry_...)."""
    path = "12345_001_nazwa_zlecenia.pdf"
    slice_name = "0A01"
    result = splitter.generate_barcode_data(path, slice_name)
    assert result == "12345_001_0A01"

def test_generate_barcode_data_pattern_no_slice(splitter):
    """Testuje wzorzec bez nazwy brytu."""
    path = "999_55_job.pdf"
    result = splitter.generate_barcode_data(path, None)
    assert result == "999_55"

def test_anchor_to_offset(splitter):
    bg_w = 100.0
    bg_h = 50.0
    assert splitter._anchor_to_offset("bottom-left", bg_w, bg_h) == (0.0, 0.0)
    assert splitter._anchor_to_offset("top-right", bg_w, bg_h) == (-100.0, -50.0)
    assert splitter._anchor_to_offset("center", bg_w, bg_h) == (-50.0, -25.0)
    assert splitter._anchor_to_offset("center-bottom", bg_w, bg_h) == (-50.0, 0.0)
    assert splitter._anchor_to_offset("invalid-anchor", bg_w, bg_h) == (0.0, 0.0)

def test_get_code_settings_defaults(splitter):
    """Sprawdza czy pobiera domyślne ustawienia, gdy brak specyficznych."""
    splitter.config.settings["graphic_settings"]["code_settings"] = {
        "code_qr": {
            "common_sheet": {
                "default": {"scale": 55.0}
            }
        }
    }
    settings = splitter.get_code_settings("common_sheet", "horizontal", "code_qr")
    assert settings["scale"] == 55.0

def test_get_code_settings_specific(splitter):
    """Sprawdza czy pobiera specyficzne ustawienia."""
    splitter.config.settings["graphic_settings"]["code_settings"] = {
        "code_qr": {
            "common_sheet": {
                "horizontal": {"scale": 99.0},
                "default": {"scale": 11.0}
            }
        }
    }
    settings = splitter.get_code_settings("common_sheet", "horizontal", "code_qr")
    assert settings["scale"] == 99.0

# --- NOWE TESTY DLA SORTOWANIA ---

def test_get_ordered_slices_order_1(splitter):
    """Test sortowania standardowego (od góry, wierszami)."""
    # 2 rzędy, 2 kolumny
    # Oczekiwane: (0,0), (0,1), (1,0), (1,1)
    # gdzie (row, col)
    
    # Uwaga: get_slice_info generuje 'name' np. 0A01 (r=0, c=0), 0A02 (r=0, c=1)
    
    slices = splitter.get_ordered_slices(2, 2, "bryt_order_1")
    
    # Sprawdzamy kolejność po indeksach row/col
    assert slices[0]["row"] == 0 and slices[0]["col"] == 0
    assert slices[1]["row"] == 0 and slices[1]["col"] == 1
    assert slices[2]["row"] == 1 and slices[2]["col"] == 0
    assert slices[3]["row"] == 1 and slices[3]["col"] == 1

def test_get_ordered_slices_order_2(splitter):
    """Test sortowania serpentyną po rzędach (od góry)."""
    # 2 rzędy, 2 kolumny
    # Rząd 0 (parzysty): 0,0 -> 0,1 (rosnąco)
    # Rząd 1 (nieparzysty): 1,1 -> 1,0 (malejąco)
    
    slices = splitter.get_ordered_slices(2, 2, "bryt_order_2")
    
    assert slices[0]["row"] == 0 and slices[0]["col"] == 0
    assert slices[1]["row"] == 0 and slices[1]["col"] == 1
    assert slices[2]["row"] == 1 and slices[2]["col"] == 1 # Odwrócone
    assert slices[3]["row"] == 1 and slices[3]["col"] == 0

def test_get_ordered_slices_order_3(splitter):
    """Test sortowania po kolumnach."""
    # 2 rzędy, 2 kolumny
    # Kolumna 0: 0,0 -> 1,0
    # Kolumna 1: 0,1 -> 1,1
    
    slices = splitter.get_ordered_slices(2, 2, "bryt_order_3")
    
    assert slices[0]["row"] == 0 and slices[0]["col"] == 0
    assert slices[1]["row"] == 1 and slices[1]["col"] == 0
    assert slices[2]["row"] == 0 and slices[2]["col"] == 1
    assert slices[3]["row"] == 1 and slices[3]["col"] == 1