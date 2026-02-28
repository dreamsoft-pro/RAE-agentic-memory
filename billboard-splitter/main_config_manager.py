# main_config_manager.py
import os
import json
import logging
import config
from tkinter import messagebox
from main_utils import get_base_dir
from lang_manager import translate
import config

# Stałe definiujące nazwy plików konfiguracyjnych
PROFILES_FILE = "profiles.json"
SETTINGS_FILE = "settings.json"

# Inicjalizacja loggera dla tego modułu
logger = logging.getLogger('BillboardSplitter')

def load_profiles_from_file():
    """Wczytuje profile użytkownika z pliku JSON."""
    base_dir = get_base_dir()
    full_path = os.path.join(base_dir, PROFILES_FILE)
    logger.info(f"{translate('loading_profiles_from')}: {full_path}")
    try:
        # Próba otwarcia i odczytania pliku profili
        with open(full_path, "r", encoding="utf-8") as f:
            profiles = json.load(f)
        # Sprawdzenie, czy wczytane dane są słownikiem
        if not isinstance(profiles, dict):
            logger.warning(f"{translate('profiles_file')} {PROFILES_FILE} {translate('does_not_contain_dict')}.")
            return {} # Zwróć pusty słownik, jeśli format jest nieprawidłowy
        return profiles # Zwróć wczytane profile
    except FileNotFoundError:
        # Informacja, jeśli plik profili nie istnieje (normalne przy pierwszym uruchomieniu)
        logger.info(f"{translate('profiles_file')} {PROFILES_FILE} {translate('not_found_creating_new')}.")
        return {} # Zwróć pusty słownik, zostanie utworzony przy zapisie
    except json.JSONDecodeError as e:
        # Obsługa błędu, jeśli plik JSON jest uszkodzony
        messagebox.showerror(translate("error"), f"{translate('json_profiles_read_error')}:\n{e}\n\n{translate('file_will_be_overwritten')}")
        logger.error(f"{translate('json_decode_error_in_profiles')}: {e}")
        return {} # Zwróć pusty słownik, aby zapobiec dalszym błędom
    except Exception as e:
        # Obsługa innych nieoczekiwanych błędów odczytu
        messagebox.showerror(translate("error"), f"{translate('cannot_load_profiles_file')}:\n{e}")
        logger.error(f"{translate('unexpected_profiles_read_error')}: {e}", exc_info=True)
        return {} # Zwróć pusty słownik w razie błędu

def save_profiles_to_file(profiles_data: dict):
    """Zapisuje profile użytkownika do pliku JSON."""
    base_dir = get_base_dir()
    full_path = os.path.join(base_dir, PROFILES_FILE)
    logger.info(f"{translate('saving_profiles_to')}: {full_path}")
    try:
        # Próba zapisu danych profili do pliku JSON
        with open(full_path, "w", encoding="utf-8") as f:
            # Zapis z wcięciami dla czytelności, bez konwersji ASCII, posortowane klucze
            json.dump(profiles_data, f, indent=4, ensure_ascii=False, sort_keys=True)
    except Exception as e:
        # Obsługa błędów zapisu
        messagebox.showerror(translate("error"), f"{translate('cannot_save_profiles_file')}:\n{e}")
        logger.error(f"{translate('profiles_save_error')}: {e}", exc_info=True)

def load_settings_from_file():
    """Wczytuje główne ustawienia aplikacji z pliku JSON."""
    base_dir = get_base_dir()
    full_path = os.path.join(base_dir, SETTINGS_FILE)
    # Uwaga: Upewnij się, że klucz 'loading_settings_from' istnieje w pliku językowym
    logger.info(f"{translate('loading_settings_from', default='Wczytywanie ustawień z')}: {full_path}") # Dodano 'default' dla bezpieczeństwa
    try:
        # Próba otwarcia i odczytania pliku ustawień
        with open(full_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
        # Sprawdzenie, czy wczytane dane są słownikiem
        if not isinstance(settings, dict):
             # Uwaga: Upewnij się, że klucz 'settings_file' istnieje w pliku językowym
            logger.warning(f"{translate('settings_file', default='Plik ustawień')} {SETTINGS_FILE} {translate('does_not_contain_dict')}.")
            return {} # Zwróć pusty słownik, jeśli format jest nieprawidłowy
        return settings # Zwróć wczytane ustawienia
    except FileNotFoundError:
        # Informacja, jeśli plik ustawień nie istnieje
        logger.info(f"{translate('settings_file', default='Plik ustawień')} {SETTINGS_FILE} {translate('not_found_creating_new')}.")
        return {} # Zwróć pusty słownik, zostanie utworzony przy zapisie
    except json.JSONDecodeError as e:
        # Obsługa błędu, jeśli plik JSON jest uszkodzony
        # Uwaga: Upewnij się, że klucze 'json_settings_read_error', 'json_decode_error_in_settings' istnieją w pliku językowym
        messagebox.showerror(translate("error"), f"{translate('json_settings_read_error', default='Błąd odczytu pliku JSON z ustawieniami')}:\n{e}\n\n{translate('file_will_be_overwritten')}")
        logger.error(f"{translate('json_decode_error_in_settings', default='Błąd dekodowania JSON w pliku ustawień')}: {e}")
        return {} # Zwróć pusty słownik
    except Exception as e:
        # Obsługa innych nieoczekiwanych błędów odczytu
        # Uwaga: Upewnij się, że klucze 'cannot_load_settings_file', 'unexpected_settings_read_error' istnieją w pliku językowym
        messagebox.showerror(translate("error"), f"{translate('cannot_load_settings_file', default='Nie można wczytać pliku ustawień')}:\n{e}")
        logger.error(f"{translate('unexpected_settings_read_error', default='Nieoczekiwany błąd odczytu ustawień')}: {e}", exc_info=True)
        return {} # Zwróć pusty słownik

def save_settings_to_file(settings_data: dict):
    """Zapisuje główne ustawienia aplikacji do pliku JSON."""
    base_dir = get_base_dir()
    full_path = os.path.join(base_dir, SETTINGS_FILE)
    # Uwaga: Upewnij się, że klucz 'saving_settings_to' istnieje w pliku językowym
    logger.info(f"{translate('saving_settings_to', default='Zapisywanie ustawień do')}: {full_path}") # Dodano 'default' dla bezpieczeństwa
    try:
        # Próba zapisu danych ustawień do pliku JSON
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=4, ensure_ascii=False, sort_keys=True)
    except Exception as e:
        # Obsługa błędów zapisu
        # Uwaga: Upewnij się, że klucze 'cannot_save_settings_file', 'settings_save_error' istnieją w pliku językowym
        messagebox.showerror(translate("error"), f"{translate('cannot_save_settings_file', default='Nie można zapisać pliku ustawień')}:\n{e}")
        logger.error(f"{translate('settings_save_error', default='Błąd zapisu ustawień do pliku')}: {e}", exc_info=True)