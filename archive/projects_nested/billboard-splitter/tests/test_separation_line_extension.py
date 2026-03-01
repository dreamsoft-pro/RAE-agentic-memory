import pytest
import os
import sys
from unittest.mock import MagicMock

# Dodaj katalog główny do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from splitter import SplitPDF

class MockConfig:
    def __init__(self):
        self.settings = {
            "graphic_settings": {
                "sep_line_black_width": 1.0,
                "sep_line_white_width": 0.0,
                "sep_line_length": 0.0
            },
            "billboard_settings": {},
            "scaling_settings": {}
        }

@pytest.fixture
def splitter():
    mock_cfg = MockConfig()
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("splitter.verify_license", lambda **kwargs: False)
        s = SplitPDF(mock_cfg)
        s.logger = MagicMock()
        return s

def test_draw_extended_line(splitter):
    """Testuje rysowanie linii DŁUŻSZEJ niż krawędź (wydłużanie dla kamer)."""
    # Ustawiamy długość na 1200 (więcej niż krawędź 1000)
    splitter.sep_line_length = 1200.0
    
    mock_canvas = MagicMock()
    page_width = 1000.0 # Krawędź cięcia
    y_pos = 500.0
    
    splitter.draw_single_separation_line(mock_canvas, 0, y_pos, page_width, horizontal=True)
    
    # Oczekiwany offset: (1000 - 1200) / 2 = -100
    # Linia powinna być od x=-100 do x=-100+1200=1100
    expected_x1 = -100.0
    expected_x2 = 1100.0
    
    found = False
    for call in mock_canvas.line.call_args_list:
        args, _ = call
        if args == (expected_x1, y_pos, expected_x2, y_pos):
            found = True
            break
            
    assert found, f"Nie znaleziono wywołania linii od {expected_x1} do {expected_x2}."

def test_draw_normal_shortened_line(splitter):
    """Upewniamy się, że skracanie nadal działa."""
    splitter.sep_line_length = 800.0
    mock_canvas = MagicMock()
    page_width = 1000.0
    y_pos = 500.0
    
    splitter.draw_single_separation_line(mock_canvas, 0, y_pos, page_width, horizontal=True)
    
    # Offset: (1000 - 800) / 2 = 100. Linia 100 do 900.
    expected_x1 = 100.0
    expected_x2 = 900.0
    
    found = False
    for call in mock_canvas.line.call_args_list:
        args, _ = call
        if args == (expected_x1, y_pos, expected_x2, y_pos):
            found = True
            break
            
    assert found
