import pytest
from unittest.mock import MagicMock

# Symulacja klasy aplikacji (tylko logika profili)
class AppLogic:
    def __init__(self, profiles_data, saved_recent_profiles):
        self.profiles_data = profiles_data
        self.config = MagicMock()
        self.config.settings = {"recent_profiles": saved_recent_profiles}
        self.profile_list = []
        
        # --- LOGIKA Z MAIN.PYW ---
        all_profiles = sorted(list(self.profiles_data.keys()))
        recent_saved = self.config.settings.get("recent_profiles", [])
        
        valid_recent = [p for p in recent_saved if p in self.profiles_data]
        remaining = [p for p in all_profiles if p not in valid_recent]
        
        self.profile_list = valid_recent + remaining
        # -------------------------

    def _update_recent_profiles(self, profile_name):
        # --- LOGIKA Z MAIN.PYW ---
        if profile_name in self.profile_list:
            self.profile_list.remove(profile_name)
        self.profile_list.insert(0, profile_name)
        
        self.config.settings["recent_profiles"] = self.profile_list[:20]
        self.config.save_settings("settings.json")
        # -------------------------

class TestRecentProfilesLogic:
    
    def test_initialization_order(self):
        """Sprawdza, czy lista profili jest inicjalizowana z uwzględnieniem historii."""
        data = {"A": {}, "B": {}, "C": {}, "D": {}}
        recent = ["A", "B"] # Historia
        
        app = AppLogic(data, recent)
        
        # Oczekiwane: [A, B, C, D] (A i B na początku, reszta alfabetycznie)
        assert app.profile_list == ["A", "B", "C", "D"]

    def test_initialization_order_mixed(self):
        """Sprawdza historię z mieszaną kolejnością."""
        data = {"A": {}, "B": {}, "C": {}, "D": {}}
        recent = ["C", "A"] # Historia
        
        app = AppLogic(data, recent)
        
        # Oczekiwane: [C, A, B, D]
        assert app.profile_list == ["C", "A", "B", "D"]

    def test_initialization_with_deleted_profiles(self):
        """Sprawdza, czy usuwa z historii profile, których już nie ma."""
        data = {"A": {}, "C": {}} # Brak B
        recent = ["A", "B"] 
        
        app = AppLogic(data, recent)
        
        # Oczekiwane: [A, C] (B usunięte)
        assert app.profile_list == ["A", "C"]

    def test_update_existing_profile(self):
        """Sprawdza przesunięcie na górę."""
        data = {"A": {}, "B": {}, "C": {}}
        recent = ["A", "B", "C"]
        app = AppLogic(data, recent)
        
        app._update_recent_profiles("C")
        
        assert app.profile_list == ["C", "A", "B"]
        assert app.config.settings["recent_profiles"] == ["C", "A", "B"]

    def test_update_new_profile(self):
        """Sprawdza dodanie nowego."""
        data = {"A": {}}
        recent = ["A"]
        app = AppLogic(data, recent)
        
        app._update_recent_profiles("NEW")
        
        assert app.profile_list == ["NEW", "A"]

    def test_limit_recent_profiles(self):
        """Sprawdza limit 20 w configu."""
        data = {str(i): {} for i in range(30)}
        recent = [str(i) for i in range(30)] # Za długa historia wejściowa
        app = AppLogic(data, recent)
        
        # Inicjalizacja nie przycina listy w pamięci (pokazuje wszystkie), 
        # ale update powinien przyciąć zapisywaną listę.
        assert len(app.profile_list) == 30 
        
        app._update_recent_profiles("NEW")
        
        # W configu tylko 20
        assert len(app.config.settings["recent_profiles"]) == 20
        assert app.config.settings["recent_profiles"][0] == "NEW"
