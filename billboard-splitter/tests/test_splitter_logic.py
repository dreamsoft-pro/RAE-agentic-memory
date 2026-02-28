import pytest
import os
import sys
from unittest.mock import MagicMock

# Dodaj katalog główny do sys.path, aby importy działały
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from splitter import SplitPDF

class MockConfig:
    def __init__(self):
        self.settings = {
            "graphic_settings": {
                "margin_top": 2.5,
                "margin_bottom": 0.0,
                "margin_left": 2.5,
                "margin_right": 2.5,
                "reg_mark_width": 10.0,
                "reg_mark_height": 5.0,
                "slice_gap": 25.0,
                "sep_line_black_width": 0.5,
                "sep_line_white_width": 0.3
            },
            "billboard_settings": {},
            "scaling_settings": {
                "scale_non_uniform": False,
                "scale_den": 1.0,
                "scale_den_x": 1.0,
                "scale_den_y": 1.0
            }
        }
    def load_settings(self, path=None):
        return self.settings
    def save_settings(self, path=None):
        pass

@pytest.fixture
def splitter():
    mock_cfg = MockConfig()
    # Mockujemy logging, żeby nie śmiecił w testach
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("splitter.verify_license", lambda **kwargs: False)
        s = SplitPDF(mock_cfg)
        return s

def test_calculate_dimensions_no_scale(splitter):
    # Szerokość 504mm, wysokość 238mm (billboard1.pdf)
    splitter.width = 504.0 * splitter.mm
    splitter.height = 238.0 * splitter.mm
    
    # 2 wiersze, 3 kolumny, overlap 20mm, white_stripe 10mm
    splitter.calculate_dimensions(overlap=20.0, rows=2, cols=3, white_stripe=10.0, add_white_to_overlap=True)
    
    # Efektywny overlap = 20 + 10 = 30mm
    # S_x = (504 + (3-1)*30) / 3 = (504 + 60) / 3 = 564 / 3 = 188mm
    # S_y = (238 + (2-1)*30) / 2 = (238 + 30) / 2 = 268 / 2 = 134mm
    
    assert round(splitter.slice_width / splitter.mm, 2) == 188.0
    assert round(splitter.slice_height / splitter.mm, 2) == 134.0

def test_calculate_dimensions_with_scale(splitter):
    # Szerokość 504mm, wysokość 238mm
    splitter.width = 504.0 * splitter.mm
    splitter.height = 238.0 * splitter.mm
    
    # Skala 10x (sx=10, sy=10)
    # Przy skali 10x, fizyczny overlap 30mm odpowiada 3mm w przestrzeni dokumentu źródłowego
    splitter.calculate_dimensions(overlap=20.0, rows=2, cols=3, white_stripe=10.0, add_white_to_overlap=True, sx=10.0, sy=10.0)
    
    # Adjusted overlap = 30 / 10 = 3mm
    # S_x_mm = (504 + 2*3) / 3 = 510 / 3 = 170mm
    # S_y_mm = (238 + 1*3) / 2 = 241 / 2 = 120.5mm
    
    assert round(splitter.slice_width / splitter.mm, 2) == 170.0
    assert round(splitter.slice_height / splitter.mm, 2) == 120.5

def test_get_slice_info(splitter):
    splitter.width = 500 * splitter.mm
    splitter.height = 200 * splitter.mm
    splitter.calculate_dimensions(overlap=0, rows=2, cols=2, white_stripe=0)
    # slice_width = 250, slice_height = 100
    
    info_0_0 = splitter.get_slice_info(0, 0, 2, 2)
    assert info_0_0["name"] == "0A01"
    # r=0 to górny rząd w PDF (Y rośnie w górę). 
    # Wysokość strony 200mm, bryt ma 100mm. Dolna krawędź górnego brytu jest na 100mm.
    expected_y = 100.0 * splitter.mm
    assert info_0_0["offset"] == (0.0, round(expected_y, 3))
    
    info_1_1 = splitter.get_slice_info(1, 1, 2, 2)
    assert info_1_1["name"] == "0B02"
    expected_x = 250.0 * splitter.mm
    assert info_1_1["offset"] == (round(expected_x, 3), 0.0)

def test_separation_line_position_with_scale(splitter):
    # Testujemy nową logikę z przeskalowaną wysokością
    page_w = 1000.0
    page_h = 2000.0
    total_slices = 2
    gap = 50.0
    slice_h_scaled = 400.0 # Przeskalowany bryt
    
    splitter.margin_bottom = 100.0
    
    # Mockujemy canvas
    mock_canvas = MagicMock()
    
    # Wywołujemy metodę rysującą linie (z nowym argumentem slice_h_on_page)
    splitter._draw_separation_lines_for_page(
        mock_canvas, page_w, page_h, total_slices, 0, "vertical", 
        gap, enable_between=True, enable_start=False, enable_end=False,
        slice_h_on_page=slice_h_scaled
    )
    
    # Oczekiwana pozycja linii:
    # y = margin_bottom + 1 * slice_h_scaled + 1 * gap - gap/2
    # y = 100 + 400 + 50 - 25 = 525.0
    
    # Sprawdzamy czy draw_single_separation_line zostało wywołane z poprawnym Y
    # Musimy zmockować draw_single_separation_line wewnątrz splitter, albo sprawdzić wywołania canvas.line
    # Najprościej: sprawdźmy czy wywołało draw_single_separation_line (musimy ją najpierw zmockować)
    
    splitter.draw_single_separation_line = MagicMock()
    splitter._draw_separation_lines_for_page(
        mock_canvas, page_w, page_h, total_slices, 0, "vertical",
        gap, enable_between=True, enable_start=False, enable_end=False,
        slice_h_on_page=slice_h_scaled
    )

    splitter.draw_single_separation_line.assert_called_with(mock_canvas, 0.0, 525.0, page_w, horizontal=True, sx=None)
