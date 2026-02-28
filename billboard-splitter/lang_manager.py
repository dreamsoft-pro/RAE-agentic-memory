# lang_manager.py
from lang_meta import LANG_META, DEFAULT_LANG_META
import config
import logging

logger = logging.getLogger('BillboardSplitter')

LANG = None  # pozostaje jak jest

def get_language():
    lang_code = config.settings.get("language", "pl")
    LANG_DICT = None
    try:
        if lang_code == "en":
            from lang_en import LANG as LANG_DICT
        elif lang_code == "zn":
            from lang_zn import LANG as LANG_DICT
        elif lang_code == "da":
            from lang_da import LANG as LANG_DICT
        elif lang_code == "de":
            from lang_de import LANG as LANG_DICT
        elif lang_code == "es":
            from lang_es import LANG as LANG_DICT
        elif lang_code == "fr":
            from lang_fr import LANG as LANG_DICT
        elif lang_code == "it":
            from lang_it import LANG as LANG_DICT
        elif lang_code == "nb":
            from lang_nb import LANG as LANG_DICT
        elif lang_code == "nl":
            from lang_nl import LANG as LANG_DICT
        elif lang_code == "pt":
            from lang_pt import LANG as LANG_DICT
        elif lang_code == "ru":
            from lang_ru import LANG as LANG_DICT
        elif lang_code == "sv":
            from lang_sv import LANG as LANG_DICT
        elif lang_code == "tr":
            from lang_tr import LANG as LANG_DICT
        elif lang_code == "uk":
            from lang_uk import LANG as LANG_DICT
        elif lang_code == "hu":
            from lang_hu import LANG as LANG_DICT
        elif lang_code == "el":
            from lang_el import LANG as LANG_DICT
        elif lang_code == "bg":
            from lang_bg import LANG as LANG_DICT
        elif lang_code == "ro":
            from lang_ro import LANG as LANG_DICT
        elif lang_code == "sr":
            from lang_sr import LANG as LANG_DICT
        elif lang_code == "hr":
            from lang_hr import LANG as LANG_DICT
        elif lang_code == "fi":
            from lang_fi import LANG as LANG_DICT
        elif lang_code == "sk":
            from lang_sk import LANG as LANG_DICT
        elif lang_code == "cs":
            from lang_cs import LANG as LANG_DICT
        elif lang_code == "th":
            from lang_th import LANG as LANG_DICT
        elif lang_code == "fil":
            from lang_fil import LANG as LANG_DICT
        elif lang_code == "km":
            from lang_km import LANG as LANG_DICT
        elif lang_code == "id":
            from lang_id import LANG as LANG_DICT
        elif lang_code == "ms":
            from lang_ms import LANG as LANG_DICT
        elif lang_code == "vi":
            from lang_vi import LANG as LANG_DICT
        elif lang_code == "ja":
            from lang_ja import LANG as LANG_DICT
        elif lang_code == "ko":
            from lang_ko import LANG as LANG_DICT
        elif lang_code == "hi":
            from lang_hi import LANG as LANG_DICT
        elif lang_code == "ur":
            from lang_ur import LANG as LANG_DICT
        elif lang_code == "ar":
            from lang_ar import LANG as LANG_DICT
        # Dodaj inne języki tutaj w razie potrzeby
        else: # Domyślnie lub jeśli lang_code == "pl"
            lang_code = "pl" # Upewnij się, że kod jest "pl" dla logowania
            from lang_pl import LANG as LANG_DICT

    except (ImportError, AttributeError, SyntaxError) as e:
        # Błąd importu - użyj domyślnego języka (polskiego)
        logger.error(f"Nie udało się załadować pliku językowego dla '{lang_code}': {e}. Używam języka polskiego.")
        try:
            from lang_pl import LANG as LANG_DICT
        except (ImportError, AttributeError, SyntaxError) as fallback_e:
             logger.critical(f"Nie udało się załadować nawet domyślnego pliku polskiego lang_pl.py: {fallback_e}")
             # W ostateczności zwróć pusty słownik, aby uniknąć dalszych błędów
             return {}

    if LANG_DICT is None: # Jeśli warunki if/elif nie złapały, a nie było błędu
         logger.warning(f"Nie znaleziono obsługi dla kodu języka '{lang_code}'. Używam języka polskiego.")
         try:
             from lang_pl import LANG as LANG_DICT
         except Exception: # Obsłuż jak wyżej
             return {} # Zwróć pusty słownik w razie problemu z plikiem PL

    return LANG_DICT

def init_language():
    global LANG
    LANG = get_language()

def set_language(lang_code):
    config.settings["language"] = lang_code
    init_language()
    return LANG

def translate(key, default=None):
    """
    Funkcja pomocnicza do tłumaczenia tekstów.
    Zwraca wartość dla podanego klucza z aktualnego słownika językowego.
    Jeśli klucz nie istnieje, zwraca wartość domyślną lub sam klucz.
    """
    if LANG and key in LANG:
        return LANG[key]
    return default if default is not None else key

# Funkcja do aktualizacji interfejsu po zmianie języka
def update_ui_language(app):
    """
    Aktualizuje interfejs użytkownika po zmianie języka.
    Odświeża wszystkie elementy UI, które zawierają przetłumaczone teksty.
    """
    # Aktualizacja tytułu aplikacji
    app.root.title(translate("app_title"))
    
    # Aktualizacja wszystkich zakładek
    app.notebook.tab(0, text=translate("tab_home"))
    app.notebook.tab(1, text=translate("tab_settings"))
    app.notebook.tab(2, text=translate("tab_license"))
    app.notebook.tab(3, text=translate("tab_help"))

    # Aktualizacja zarejestrowanych widgetów w głównej aplikacji
    if hasattr(app, 'translatable_widgets'):
        for widget, key in app.translatable_widgets:
            if widget.winfo_exists():
                widget.configure(text=translate(key))

    # Aktualizacja widgetów w poszczególnych zakładkach
    if hasattr(app, 'home_tab_instance'):
        app.home_tab_instance.update_combobox_values()
    
    if hasattr(app, 'settings_tab_instance'):
        app.settings_tab_instance.update_combobox_values()
    
    # Ta funkcja jest teraz zbędna, bo wszystko jest odświeżane powyżej
    # app.update_gui_from_config()

def get_language_code() -> str:
    return config.settings.get("language", "pl")

def get_lang_meta(lang_code: str | None = None) -> dict:
    code = lang_code or get_language_code()
    return LANG_META.get(code, DEFAULT_LANG_META)

def is_rtl(lang_code: str | None = None) -> bool:
    return get_lang_meta(lang_code).get("direction") == "rtl"

def text_align(lang_code: str | None = None) -> str:
    return get_lang_meta(lang_code).get("align", "left")

def text_justify(lang_code: str | None = None) -> str:
    return get_lang_meta(lang_code).get("justify", "left")

# Inicjalizujemy LANG, aby był dostępny przy imporcie
init_language()
