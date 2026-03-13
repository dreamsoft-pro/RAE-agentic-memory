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
                "sep_line_black_width": 1.0, # Włączamy czarną linię
                "sep_line_white_width": 0.0,
                "sep_line_length": 0.0 # Domyślnie 0
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
        # Mockujemy logger, żeby nie sypał błędami
        s.logger = MagicMock()
        return s

def test_draw_full_length_line(splitter):
    """Testuje rysowanie linii na całą szerokość (gdy sep_line_length = 0)."""
    # Ustawiamy długość na 0 (domyślnie)
    splitter.sep_line_length = 0.0
    
    mock_canvas = MagicMock()
    page_width = 1000.0
    y_pos = 500.0
    
    splitter.draw_single_separation_line(mock_canvas, 0, y_pos, page_width, horizontal=True)
    
    # Oczekujemy linii od (0, 500) do (1000, 500)
    # Metoda draw_single_separation_line wywołuje c.line(x1, y1, x2, y2)
    # Sprawdzamy wywołania. Może być ich więcej (dla białej i czarnej linii), sprawdzamy czy choć jedno pasuje.
    
    found = False
    for call in mock_canvas.line.call_args_list:
        args, _ = call
        if args == (0, y_pos, page_width, y_pos):
            found = True
            break
            
    assert found, "Nie znaleziono wywołania rysowania pełnej linii poziomej."

def test_draw_shortened_centered_line(splitter):
    """Testuje rysowanie skróconej, wyśrodkowanej linii."""
    # Ustawiamy długość linii na 200 jednostek
    splitter.sep_line_length = 200.0
    
    mock_canvas = MagicMock()
    page_width = 1000.0
    y_pos = 500.0
    
    splitter.draw_single_separation_line(mock_canvas, 0, y_pos, page_width, horizontal=True)
    
    # Oczekiwany offset: (1000 - 200) / 2 = 400
    # Linia powinna być od x=400 do x=400+200=600
    expected_x1 = 400.0
    expected_x2 = 600.0
    
    found = False
    for call in mock_canvas.line.call_args_list:
        args, _ = call
        # args to (x1, y1, x2, y2)
        if args == (expected_x1, y_pos, expected_x2, y_pos):
            found = True
            break
            
    assert found, f"Nie znaleziono wywołania linii od {expected_x1} do {expected_x2}."

def test_draw_vertical_shortened_line(splitter):
    """Testuje rysowanie skróconej linii PIONOWEJ."""
    splitter.sep_line_length = 200.0
    
    mock_canvas = MagicMock()
    x_pos = 100.0
    page_height = 1000.0
    
    splitter.draw_single_separation_line(mock_canvas, x_pos, 0, page_height, horizontal=False)
    
    # Oczekiwany offset pionowy: (1000 - 200) / 2 = 400
    # Linia od y=400 do y=600
    expected_y1 = 400.0
    expected_y2 = 600.0
    
    found = False
    for call in mock_canvas.line.call_args_list:
        args, _ = call
        if args == (x_pos, expected_y1, x_pos, expected_y2):
            found = True
            break
    
    assert found, f"Nie znaleziono wywołania pionowej linii od {expected_y1} do {expected_y2}."
