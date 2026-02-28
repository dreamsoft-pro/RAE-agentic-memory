import pytest
from unittest.mock import MagicMock

# Symulacja klasy aplikacji z logiką update_gui_from_config
class AppProfileLogic:
    def __init__(self, settings):
        self.settings = settings
        # Mockujemy zmienne Tkinter (StringVar)
        self.rows = MagicMock()
        self.rows.set = MagicMock()
        self.cols = MagicMock()
        self.cols.set = MagicMock()
        self.layout = MagicMock()
        self.layout.set = MagicMock()

    def update_gui_from_config(self):
        # --- LOGIKA Z MAIN.PYW ---
        config_settings = self.settings
        
        billboard_settings = config_settings.get("billboard_settings", {})
        
        def get_bb_val(key, legacy_key, default):
            return billboard_settings.get(key, config_settings.get(legacy_key, default))

        self.rows.set(str(get_bb_val("rows", "split_rows", 2)))
        self.cols.set(str(get_bb_val("cols", "split_cols", 5)))
        self.layout.set(get_bb_val("layout", "layout", "layout_vertical"))
        # -------------------------

class TestProfileLoading:
    
    def test_load_legacy_profile(self):
        """Testuje ładowanie starego profilu (płaska struktura)."""
        legacy_settings = {
            "split_rows": 4,
            "split_cols": 8,
            "layout": "layout_horizontal"
            # Brak billboard_settings
        }
        
        app = AppProfileLogic(legacy_settings)
        app.update_gui_from_config()
        
        # Sprawdzamy czy pobrało z legacy keys
        app.rows.set.assert_called_with("4")
        app.cols.set.assert_called_with("8")
        app.layout.set.assert_called_with("layout_horizontal")

    def test_load_new_profile(self):
        """Testuje ładowanie nowego profilu (zagnieżdżona struktura)."""
        new_settings = {
            "billboard_settings": {
                "rows": 3,
                "cols": 6,
                "layout": "layout_vertical"
            },
            # Legacy keys mogą istnieć jako śmieci lub defaulty, ale powinny być ignorowane
            "split_rows": 99,
            "split_cols": 99
        }
        
        app = AppProfileLogic(new_settings)
        app.update_gui_from_config()
        
        # Sprawdzamy czy priorytet ma billboard_settings
        app.rows.set.assert_called_with("3")
        app.cols.set.assert_called_with("6")
        app.layout.set.assert_called_with("layout_vertical")

    def test_load_mixed_profile(self):
        """Testuje profil mieszany (część w nowym, część brak)."""
        mixed_settings = {
            "billboard_settings": {
                "rows": 5
                # Brak cols
            },
            "split_cols": 7 # Legacy fallback
        }
        
        app = AppProfileLogic(mixed_settings)
        app.update_gui_from_config()
        
        app.rows.set.assert_called_with("5") # Z nowego
        app.cols.set.assert_called_with("7") # Z legacy fallback
