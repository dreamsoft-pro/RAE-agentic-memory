# main.pyw  (UWAGA: .pyw!)
import sys, os
import tkinter as tk
from pathlib import Path
import logging

# --- ANTY-MIGANIE: schowaj jakiekolwiek okno konsoli, gdyby jednak powstało
if os.name == "nt":
    try:
        import ctypes
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd:
            ctypes.windll.user32.ShowWindow(whnd, 0)  # SW_HIDE
            ctypes.windll.kernel32.CloseHandle(whnd)
    except Exception:
        pass

# --- LOGI DO PLIKU W TRYBIE FROZEN (żadnych printów)
is_frozen = getattr(sys, "frozen", False)
base_dir = Path(os.path.dirname(sys.executable) if is_frozen else os.getcwd())
log_dir = base_dir / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(log_dir / "app.log", encoding="utf-8")]
)
log = logging.getLogger("app")
log.info("Start GUI (frozen=%s)", is_frozen)

# Jeśli aplikacja jest uruchamiana z bundla (pyinstaller) zmień bieżący katalog
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import json
import config  # Import konfiguracji
import threading
from queue import Queue, Empty

# Załaduj ustawienia PRZED inicjalizacją języka
try:
    log.info("Loading settings from settings.json...")
    config.load_settings("settings.json")
except Exception as e:
    # Użyj logging, a nie print. Na tym etapie LANG może nie być dostępne.
    logging.critical(f"CRITICAL ERROR during settings load: {e}", exc_info=True)
    # Próbuj wyświetlić MessageBox jako ostatnią deskę ratunku, ale może się nie udać
    try:
        root_tk = tk.Tk()
        root_tk.withdraw()  # Ukryj główne okno Tkinter
        messagebox.showerror("Critical Error", f"Failed to load settings: {e}")
        root_tk.destroy()
    except Exception:
        pass  # Ignoruj błędy przy próbie pokazania messageboxa
    sys.exit(1)

# Dopiero TERAZ importuj lang_manager i zainicjalizuj język
from lang_manager import init_language, LANG, set_language, translate
try:
    log.info("Initializing language...")
    init_language()  # Uaktualnij słownik językowy zgodnie z wczytanymi ustawieniami
except Exception as e:
    logging.critical(f"CRITICAL ERROR during language init: {e}", exc_info=True)
    # Tutaj też można spróbować pokazać messagebox
    sys.exit(1)

# Importy zależne od zainicjalizowanego języka lub reszta importów
from init_directories import initialize_directories
from splitter import SplitPDF
import license_manager

from main_utils import get_base_dir, _on_mousewheel
from main_config_manager import load_profiles_from_file, save_profiles_to_file
from main_ui_home import HomeTabUI
from main_ui_settings import SettingsTabUI
from main_ui_help import HelpTabUI
from main_license import LicenseTabUI
from billboard_splitter.services.rasterize import clear_raster_cache

# Definicje plików konfiguracyjnych
PROFILES_FILE = "profiles.json"
SETTINGS_FILE = "settings.json"

# Zainicjalizuj katalogi PO wczytaniu ustawień i języka
try:
    log.info("Initializing directories...")
    initialize_directories()  # Ta funkcja też powinna teraz używać loggera
    log.info("Directories initialized.")
except Exception as e:
    # Użycie klucza językowego jest już bezpieczne
    logging.critical(translate("error_critical_init").format(e), exc_info=True)
    # Próba wyświetlenia komunikatu
    try:
        root_tk = tk.Tk()
        root_tk.withdraw()
        messagebox.showerror(translate("error_critical_init_title", "Critical Initialization Error"),
                              translate("error_critical_init").format(e))
        root_tk.destroy()
    except Exception:
        pass
    sys.exit(1)

# Ustal tryb trial na podstawie weryfikacji licencji
trial_mode = license_manager.verify_license()

class BillboardSplitterApp:
    def __init__(self, root):
        self.work_queue = Queue()
        # Ustawienie trybu trial na podstawie weryfikacji licencji
        self.trial_mode = trial_mode

 
        self.root = root
        self.root.title(translate("app_title"))
        self.root.minsize(1200, 1000)
        self.generated_output_files = []
        self.generated_output_pdf = None # <-- DODANA LINIJKA

        # Utwórz obiekt SplitPDF przekazując konfigurację
        log.info("Creating SplitPDF instance (which will call setup_logging)...")
        try:
            self.splitter = SplitPDF(config)
            self.splitter.trial_mode = self.trial_mode
 
            self.logger = self.splitter.logger  # Pobierz skonfigurowany logger
            self.logger.info("Full logger configuration complete (in App __init__).")
        except Exception as e:
            logging.critical(f"CRITICAL ERROR creating SplitPDF instance: {e}", exc_info=True)
            try:
                messagebox.showerror(translate("error", "Error"), f"Failed to initialize core component: {e}")
            except Exception:
                pass
            self.root.quit()
            return



        # Pamięć ostatnio wygenerowanych ścieżek – użyje jej HomeTabUI do podglądu
        self._last_result_paths = {
            "mode": None,                  # 'output_common_sheet' | 'output_separate_files' | 'output_both'
            "layout": None,                # 'layout_vertical' | 'layout_horizontal'
            "common_sheet_path": None,     # str lub None
            "separate_files": [],          # list[str]
            "separate_first_path": None,   # str lub None
            "preview_preferred": None      # str lub None
        }




        # Upewnij się, że comboboxy przechowują klucze zamiast tłumaczeń
        conversion_map = {
            "layout": ["layout_vertical", "layout_horizontal"],
       
             "output_type": ["output_common_sheet", "output_separate_files", "output_both"],
            "registration_mark_type": ["reg_mark_cross", "reg_mark_line"],
            "barcode_type": ["code_qr", "code_barcode"],
            "bryt_order": ["bryt_order_1", "bryt_order_2", "bryt_order_3", "bryt_order_4", "bryt_order_5", "bryt_order_6"],
            "logging_mode": ["logging_console", "logging_file", "logging_both"]
        }
        conversion_done = False
        for cfg_key, valid_keys in conversion_map.items():
 
            val = config.settings.get(cfg_key)
            if isinstance(val, str) and val not in valid_keys:
                new_key = self.find_key_for_value(val, valid_keys) if val else valid_keys[0]
                if new_key != val:
                    self.logger.debug(f"Konwersja {cfg_key}: {val} -> {new_key}")
  
                    config.settings[cfg_key] = new_key
                    conversion_done = True

        # Wczytaj profile i zamień ewentualne tłumaczenia na klucze
        self.profiles_data = load_profiles_from_file()
        profiles_converted = False
        for prof_name, prof_settings in self.profiles_data.items():
          
           for cfg_key, valid_keys in conversion_map.items():
                if cfg_key in prof_settings and isinstance(prof_settings[cfg_key], str) and prof_settings[cfg_key] not in valid_keys:
                    new_key = self.find_key_for_value(prof_settings[cfg_key], valid_keys) if prof_settings[cfg_key] else valid_keys[0]
                    if new_key != prof_settings[cfg_key]:
                 
                        self.logger.debug(f"Konwersja profilu '{prof_name}' - {cfg_key}: {prof_settings[cfg_key]} -> {new_key}")
                        prof_settings[cfg_key] = new_key
                        profiles_converted = True
        if profiles_converted:
            save_profiles_to_file(self.profiles_data)
        if conversion_done:
    
             config.save_settings("settings.json")

        # --- Inicjalizacja listy profili z uwzględnieniem historii (Recent Profiles) ---
        all_profiles = sorted(list(self.profiles_data.keys()))
        recent_saved = config.settings.get("recent_profiles", [])
        
        # Filtrujemy zapisane w historii, usuwając te, które już nie istnieją
        valid_recent = [p for p in recent_saved if p in self.profiles_data]
        
        # Dodajemy pozostałe profile (których nie ma w historii), alfabetycznie
        remaining = [p for p in all_profiles if p not in valid_recent]
        
        self.profile_list = valid_recent + remaining
        # -----------------------------------------------------------------------------


        # --- Definicja zmiennych Tkinter (przechowujących klucze) ---
        billboard_settings = config.settings.get("billboard_settings", {})
        self.file_path = tk.StringVar(value=config.settings.get("file_path", ""))
        self.rows = tk.StringVar(value=str(billboard_settings.get("rows", 2)))
        self.cols = tk.StringVar(value=str(billboard_settings.get("cols", 5)))
        self.overlap = tk.StringVar(value=str(billboard_settings.get("overlap", 20.0)))
        self.white_stripe = tk.StringVar(value=str(billboard_settings.get("white_stripe", 10.0)))
        self.add_white_to_overlap = tk.BooleanVar(value=billboard_settings.get("add_white_to_overlap", True))
        self.create_order_folder = tk.BooleanVar(value=config.settings.get("create_order_folder", False)) 
        self.draw_slice_border = tk.BooleanVar(value=billboard_settings.get("draw_slice_border", False))

        # --- Scaling Settings ---
        scaling_settings = config.settings.get("scaling_settings", {})
        self.scale_non_uniform = tk.BooleanVar(value=scaling_settings.get("scale_non_uniform", False))
        self.scale_den = tk.DoubleVar(value=scaling_settings.get("scale_den", 10.0))
        self.scale_den_x = tk.DoubleVar(value=scaling_settings.get("scale_den_x", 10.0))
        self.scale_den_y = tk.DoubleVar(value=scaling_settings.get("scale_den_y", 10.0))
        self.out_width_cm = tk.DoubleVar(value=scaling_settings.get("out_width_cm", 0.0))
        self.out_height_cm = tk.DoubleVar(value=scaling_settings.get("out_height_cm", 0.0))
        self.input_file_size_info_scaling = tk.StringVar(value="") 

        # --- POCZĄTEK ZMIAN HDD/RAM---
        self.processing_mode = tk.StringVar(value=config.settings.get("processing_mode", "hdd"))
        # --- KONIEC ZMIAN ---

        layout_key = billboard_settings.get("layout", "layout_vertical")
        self.layout = tk.StringVar(value=layout_key)

        output_type_key = billboard_settings.get("output_type", "output_common_sheet")
        self.output_type = tk.StringVar(value=output_type_key)

        self.enable_reg_marks = tk.BooleanVar(value=billboard_settings.get("enable_reg_marks", True))

        reg_mark_key = billboard_settings.get("registration_mark_type", "reg_mark_cross")
        self.reg_mark = tk.StringVar(value=reg_mark_key)

        self.enable_barcode = tk.BooleanVar(value=billboard_settings.get("enable_barcode", True))

        barcode_type_key = billboard_settings.get("barcode_type", "code_qr")
        self.barcode_type = tk.StringVar(value=barcode_type_key)

        barcode_text_position_value = config.settings.get("barcode_text_position", "side")
        self.barcode_text_position = tk.StringVar(value=barcode_text_position_value)

        self.enable_separation_lines = tk.BooleanVar(value=billboard_settings.get("enable_separation_lines", True))
        self.add_line_at_start = tk.BooleanVar(value=billboard_settings.get("add_line_at_start", False))
   
        self.add_line_at_end = tk.BooleanVar(value=billboard_settings.get("add_line_at_end", False))

        bryt_order_key = billboard_settings.get("bryt_order", "bryt_order_1")
        self.bryt_order = tk.StringVar(value=bryt_order_key)

        self.slice_rotation = tk.StringVar(value=str(billboard_settings.get("slice_rotation", 0)))
        self.profile_name_var = tk.StringVar()
        self.output_dir = tk.StringVar(value=config.settings.get("output_dir", ""))
        self.barcode_text_position = tk.StringVar(value=config.settings.get("barcode_text_position", "side"))

        self.graphic_vars = {}
        gf_keys = ["margin_top", "margin_bottom", "margin_left", "margin_right",
     
                   "reg_mark_width", "reg_mark_height",
                   "reg_mark_white_line_width", "reg_mark_black_line_width",
                   "sep_line_black_width", "sep_line_white_width", "slice_gap", "barcode_font_size"]
        for key in gf_keys:
            self.graphic_vars[key] = tk.StringVar()

        self.sep_line_length = tk.StringVar(value=str(billboard_settings.get("sep_line_length", 0.0)))

        self.code_gui_vars = {}
        code_type_keys = ["code_qr", "code_barcode"]
        output_type_keys_internal = ["common_sheet", "separate_files"]
        layout_keys_internal = ["horizontal", "vertical"]
        qr_param_keys = ["scale", "offset_x", "offset_y", "rotation", "anchor"]
        barcode_param_keys = ["scale_x", "scale_y", "offset_x", "offset_y", "rotation", "anchor"]
        for c_key in code_type_keys:
            self.code_gui_vars[c_key] = {}
            for o_key in output_type_keys_internal:
       
                self.code_gui_vars[c_key][o_key] = {}
                for l_key in layout_keys_internal:
                    self.code_gui_vars[c_key][o_key][l_key] = {}
                    current_param_keys = qr_param_keys if c_key == "code_qr" else barcode_param_keys
                    
                    for p_key in current_param_keys:
                        self.code_gui_vars[c_key][o_key][l_key][p_key] = tk.StringVar()

        logging_mode_key = config.settings.get("logging_mode", "logging_console")
        self.logging_mode = tk.StringVar(value=logging_mode_key)
        self.log_file_path = tk.StringVar(value=config.settings.get("log_file_path", ""))
        self.logging_level = tk.StringVar(value=config.settings.get("logging_level", "INFO"))

        # --- Rasterization Settings ---
        raster_settings = config.settings.get("rasterization", {})
        self.rasterization_enabled = tk.BooleanVar(value=raster_settings.get("enabled", False))
        self.rasterization_dpi = tk.IntVar(value=raster_settings.get("dpi", 300))
        self.rasterization_compression = tk.StringVar(value=raster_settings.get("compression", "LZW"))

        self.product_mode = tk.StringVar(value=config.settings.get("product_mode", "billboard"))

        # --- Poster Settings ---
        poster_settings = config.settings.get("poster_settings", {})
        self.poster_repetitions = tk.IntVar(value=poster_settings.get("repetitions", 1))
        self.poster_margin_external = tk.StringVar(value=str(poster_settings.get("margin_external", 2.0)))
        self.poster_separation_lines = tk.BooleanVar(value=poster_settings.get("separation_lines", False))
        self.poster_input_rotation = tk.IntVar(value=poster_settings.get("input_rotation", 0))
        self.poster_vertical_cut_marks = tk.BooleanVar(value=poster_settings.get("vertical_cut_marks", False))
        self.poster_gap = tk.StringVar(value=str(poster_settings.get("poster_gap", 2.0)))
        self.poster_enable_barcode = tk.BooleanVar(value=poster_settings.get("enable_barcode", True))
        self.poster_add_line_at_start = tk.BooleanVar(value=poster_settings.get("add_line_at_start", False))
        self.poster_add_line_at_end = tk.BooleanVar(value=poster_settings.get("add_line_at_end", False))

        # --- POS Settings ---
        pos_settings = config.settings.get("pos_settings", {})
        self.pos_enable_barcode = tk.BooleanVar(value=pos_settings.get("enable_barcode", True))
        self.poster_enable_barcode = tk.BooleanVar(value=poster_settings.get("enable_barcode", True))
        self.poster_add_line_at_start = tk.BooleanVar(value=poster_settings.get("add_line_at_start", False))
        self.poster_add_line_at_end = tk.BooleanVar(value=poster_settings.get("add_line_at_end", False))

        # --- Manufacturer Spec Settings ---
        spec_settings = config.settings.get("manufacturer_spec", {})
        self.manufacturer_spec_enabled = tk.BooleanVar(value=spec_settings.get("enabled", False))
        self.manufacturer_spec_name = tk.StringVar(value=spec_settings.get("name", "default"))

        self.input_file_size_info = tk.StringVar(value="")

        self.profile_list = sorted(list(self.profiles_data.keys()))
        # Ensure profile_combo is defined to avoid attribute errors
  
        self.profile_combo = None

        # Tworzenie głównego GUI
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)

        # Konfiguracja siatki (grid) w głównym kontenerze, aby widgety mogły się rozciągać
        main_container.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)

        # 1. Tworzymy widget Notebook (zakładki) i umieszczamy go w siatce, aby wypełnił całe okno
 
        self.notebook = ttk.Notebook(main_container)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.translatable_widgets = []

        # 2. Tworzymy ramkę dla przycisków
        top_buttons_frame = ttk.Frame(main_container)
        
        # --- POCZĄTEK POPRAWKI ---
        # Przycisk "Zapisz wszystkie ustawienia" ze stylem zwiększającym wysokość
        save_all_btn_top = ttk.Button(top_buttons_frame, text=translate("save_all_settings"), command=self.save_settings, style="Pad.TButton")
        save_all_btn_top.pack(side="left", padx=(0, 5))
        self.translatable_widgets.append((save_all_btn_top, "save_all_settings"))

        # Dodany przycisk "Odśwież podgląd"
        refresh_btn_top = ttk.Button(top_buttons_frame, text=translate("button_refresh_preview"), command=self.refresh_previews, style="Pad.TButton")
        refresh_btn_top.pack(side="left", padx=(0, 5))
        self.translatable_widgets.append((refresh_btn_top, "button_refresh_preview"))
        
        # Przycisk "Generuj PDF" ze specjalnym, zielonym stylem
        generate_btn_top = ttk.Button(top_buttons_frame, text=translate("button_generate_pdf"), command=self.generate_pdf, style="Success.TButton")
        generate_btn_top.pack(side="left")
        self.translatable_widgets.append((generate_btn_top, "button_generate_pdf"))

        # 3. Umieszczamy ramkę z przyciskami w TEJ SAMEJ komórce siatki co Notebook,
        #    ale wyrównujemy ją do prawego górnego rogu ("ne" - north-east).
        #    Zmieniono pady na 5, aby lepiej dopasować w pionie.
        top_buttons_frame.grid(row=0, column=0, sticky="ne", padx=10, pady=5)
        # --- KONIEC POPRAWKI ---

        self.tab_home = ttk.Frame(self.notebook, padding="5")
        self.tab_settings = ttk.Frame(self.notebook, padding="5")
        self.tab_license = ttk.Frame(self.notebook, padding="5")
        self.tab_help = ttk.Frame(self.notebook, padding="5")

        self.notebook.add(self.tab_home, text=translate("tab_home"))
        self.notebook.add(self.tab_settings, text=translate("tab_settings"))
        self.notebook.add(self.tab_license, text=translate("tab_license"))
        self.notebook.add(self.tab_help, text=translate("tab_help"))

    
        try:
            self.license_tab_instance = LicenseTabUI(self.tab_license, self)
        except Exception as e:
            self.logger.error(translate("error_creating_license_ui"), exc_info=True)
            ttk.Label(self.tab_license,
                      text=translate("error_loading_ui").format(error=e), foreground="red").pack()
        try:
            self.home_tab_instance = HomeTabUI(self.tab_home, self)
        except Exception as e:
            self.logger.error(translate("error_tab_home"), exc_info=True)
            ttk.Label(self.tab_home,
                      text=translate("error_loading_ui").format(error=e), foreground="red").pack()
        try:
            self.settings_tab_instance = SettingsTabUI(self.tab_settings, self)
        except Exception as e:
      
            self.logger.error(translate("error_tab_settings"), exc_info=True)
            ttk.Label(self.tab_settings,
                      text=translate("error_loading_ui").format(error=e), foreground="red").pack()
        try:
            self.help_tab_instance = HelpTabUI(self.tab_help, self)
        except Exception as e:
            self.logger.error(translate("error_tab_help"), exc_info=True)
           
            ttk.Label(self.tab_help,
                      text=translate("error_loading_ui").format(error=e), foreground="red").pack()

        self.update_gui_from_config()
        self.logger.info(translate("ui_created"))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handles application cleanup before closing."""
        self.logger.info("Application closing. Cleaning up...")
        clear_raster_cache()
        self.root.destroy()

    # -------------------- METODY POMOCNICZE GUI --------------------

    def refresh_previews(self):
        """Odświeża podgląd pliku wejściowego i wyjściowego."""
        if hasattr(self, 'home_tab_instance'):
            self.logger.debug("Ręczne odświeżanie podglądów.")
            self.home_tab_instance.update_preview()
            self.home_tab_instance.update_output_preview()

    def find_key_for_value(self, value_to_find, possible_keys):
        """
        Znajduje klucz językowy w LANG, którego przetłumaczona wartość
        odpowiada podanej wartości (value_to_find).
        Przeszukuje tylko w ramach podanej listy możliwych kluczy.
        """
        global LANG  # Potrzebujemy dostępu do globalnego słownika językowego
        for key in possible_keys:
            if key in LANG and LANG[key] == value_to_find:
                return key
        # Jeśli nie znaleziono dokładnego dopasowania, zwróć pierwszy możliwy klucz jako domyślny
        self.logger.warning(f"Nie znaleziono klucza dla wartości '{value_to_find}'. Używam domyślnego '{possible_keys[0]}'.")
        return possible_keys[0]

    def browse_file(self):
        # --- POCZĄTEK ZMIANY ---
        # Sprawdź, czy w konfiguracji zapisana jest ścieżka do ostatnio używanego pliku
        last_file_path = config.settings.get("file_path")

        # Jeśli ścieżka istnieje i prowadzi do istniejącego pliku,
        # użyj katalogu tego pliku jako lokalizacji początkowej.
       
        if last_file_path and os.path.isfile(last_file_path):
            initial_dir = os.path.dirname(last_file_path)
        else:
            # W przeciwnym razie (np. pierwsze uruchomienie), użyj domyślnego katalogu wejściowego
            initial_dir = config.settings.get("default_input_dir", get_base_dir())
        # --- KONIEC ZMIANY ---

        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
   
            title=translate("select_file_title"),
            filetypes=[(translate("supported_files"), "*.pdf *.jpg *.jpeg *.tiff *.tif"), (translate("all_files"), "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            config.settings["file_path"] = file_path
            
            # --- KLUCZOWA ZMIANA ---
            # Wyczyść listę starych plików wyjściowych, aby podgląd się zaktualizował poprawnie
            self.generated_output_files = []
            self.generated_output_pdf = None
            # --- KONIEC ZMIANY ---

            # Po wybraniu nowego pliku, odśwież oba podglądy.
            if hasattr(self, 'home_tab_instance'):
                self.home_tab_instance.update_preview()
                self.home_tab_instance.update_output_preview()

    def browse_output_dir(self):
        initial_dir = config.settings.get("output_dir", get_base_dir())
        output_dir = filedialog.askdirectory(
            initialdir=initial_dir,
            title=translate("select_dir_title")
        )
        if output_dir:
            self.output_dir.set(output_dir)
            config.settings["output_dir"] = output_dir

    def browse_log_folder(self):
        initial_dir = os.path.dirname(config.settings.get("log_file_path", get_base_dir()))
        log_folder = filedialog.askdirectory(
            initialdir=initial_dir,
            title=translate("select_log_dir_title")
        )
        if log_folder:
            log_file = os.path.join(log_folder, "app.log")
            self.log_file_path.set(log_file)
            config.settings["log_file_path"] = log_file

    def save_settings(self):
        """Zapisuje aktualne ustawienia, stosuje je w silniku i odświeża GUI."""
        self.logger.debug(translate("logger_start_save_settings"))
        # Najpierw pobieramy wartości z GUI do globalnego słownika config.settings
        if self.save_settings_local():
            try:
                # Zapisujemy ustawienia do pliku
                config.save_settings(SETTINGS_FILE)
                self.logger.info(translate("logger_settings_saved").format(file=SETTINGS_FILE))
                messagebox.showinfo(
                    translate("settings_saved_title"),
                    translate("settings_saved").format(filepath=SETTINGS_FILE)
                )

                # --- KLUCZOWA ZMIANA: NATYCHMIASTOWE ZASTOSOWANIE USTAWIEŃ ---
                # 1. Przekaż zaktualizowany moduł config do instancji splittera
                self.splitter.config = config
                # 2. Wywołaj metodę w splitterze, która przeładuje ustawienia graficzne
                self.splitter.update_graphic_settings()
                # 3. Odśwież cały interfejs użytkownika, aby odzwierciedlić zmiany
                self.update_gui_from_config()
                # 4. Odśwież podglądy, które mogły ulec zmianie
                if hasattr(self, 'home_tab_instance'):
                    self.home_tab_instance.update_preview()
                    self.home_tab_instance.update_output_preview()
                # --- KONIEC KLUCZOWEJ ZMIANY ---

            except Exception as e:
                self.logger.error(translate("logger_unexpected_save_error").format(error=e), exc_info=True)
                messagebox.showerror(
                    translate("settings_save_error_title"),
                    translate("settings_save_error").format(error=e)
                )
        else:
            # Błąd konwersji wartości z GUI został już zalogowany w save_settings_local
            self.logger.error(translate("logger_conversion_error").format(error="conversion_failed"))


    # -------------------- LOGIKA PROFILI I USTAWIEŃ --------------------

    def _update_recent_profiles(self, profile_name):
        """Przesuwa profil na początek listy i zapisuje historię."""
        if profile_name in self.profile_list:
            self.profile_list.remove(profile_name)
        self.profile_list.insert(0, profile_name)
        
        # Opcjonalnie: Limit historii w pliku konfiguracyjnym (np. 20), 
        # ale w GUI wyświetlamy 10.
        
        config.settings["recent_profiles"] = self.profile_list[:20]
        config.save_settings(SETTINGS_FILE)

    def save_profile(self):
        profile_name = self.profile_name_var.get().strip()
        if not profile_name:
            messagebox.showwarning(translate("warning_no_name"), translate("profile_enter_name"))
            return

        if not self.save_settings_local():
            return

        # Utwórz kopię ustawień, usuwając ścieżkę pliku wejściowego
        profile_settings = config.settings.copy()
        profile_settings.pop("file_path", None)
        self.profiles_data[profile_name] = profile_settings
        save_profiles_to_file(self.profiles_data)

        # Aktualizacja listy ostatnich profili
        self._update_recent_profiles(profile_name)

        if self.profile_combo is not None:
            self.profile_combo['values'] = self.profile_list
        else:
            self.logger.warning("profile_combo is None; cannot update its values.")

        if hasattr(self, 'settings_tab_instance') and hasattr(self.settings_tab_instance, 'recent_profiles_container'):
            self.settings_tab_instance._create_recent_profile_buttons_simple(self.settings_tab_instance.recent_profiles_container)

        if hasattr(self, 'home_tab_instance') and hasattr(self.home_tab_instance, 'recent_profiles_container'):
            self.home_tab_instance._create_recent_profile_buttons_simple(self.home_tab_instance.recent_profiles_container)

        # Zastosuj zapisane ustawienia natychmiast
        self._apply_profile_settings(profile_name)

        messagebox.showinfo(translate("profile_saved_title"), translate("profile_saved_and_applied").format(profile=profile_name))
        self.logger.info(translate("logger_profile_saved").format(profile=profile_name))

    def _apply_profile_settings(self, profile_name):
        """Applies the settings from a given profile name without showing a message box."""
        if profile_name not in self.profiles_data:
            self.logger.warning(f"Attempted to apply non-existent profile: {profile_name}")
            return

        profile_settings = self.profiles_data[profile_name].copy()
        self.logger.info(f"[profiles] Loading profile '{profile_name}' with keys: {list(profile_settings.keys())}")

        # Zapewnij kompatybilność wsteczną dla profili bez product_mode lub rasteryzacji
        if "product_mode" not in profile_settings:
            profile_settings["product_mode"] = "billboard"
            self.logger.info(f"[profiles] Profile '{profile_name}' has no 'product_mode'. Defaulting to 'billboard'.")

        if "rasterization" not in profile_settings:
            profile_settings["rasterization"] = config.default_settings.get("rasterization", {}).copy()
            self.logger.info(f"[profiles] Profile '{profile_name}' has no 'rasterization' settings. Applying defaults.")

        if "scaling_settings" not in profile_settings:
            profile_settings["scaling_settings"] = config.default_settings.get("scaling_settings", {}).copy()
            self.logger.info(f"[profiles] Profile '{profile_name}' has no 'scaling_settings'. Applying defaults.")

        current_file_path = config.settings.get("file_path", "")
        config.settings.clear()
        # Załaduj domyślne ustawienia, a następnie nadpisz je ustawieniami z profilu
        config.settings.update(config.default_settings.copy())
        config.settings.update(profile_settings)
        config.settings["file_path"] = current_file_path

        try:
            initialize_directories()
        except Exception as e:
            messagebox.showerror(translate("init_error_title"), translate("init_error").format(error=e))
            self.logger.error(translate("logger_init_error").format(error=e), exc_info=True)
            return

        self.update_gui_from_config()
        self.logger.info(translate("logger_profile_loaded").format(profile=profile_name))

    def load_profile(self):
        profile_name = self.profile_name_var.get().strip()
        if not profile_name:
            messagebox.showwarning(translate("warning_no_profile"), translate("select_profile"))
            return
        if profile_name not in self.profiles_data:
            messagebox.showerror(translate("error"), translate("profile_not_found").format(profile=profile_name))
            self.logger.warning(translate("logger_profile_not_found").format(profile=profile_name))
            return

        self._apply_profile_settings(profile_name)
        # Przesuń na górę listy ostatnio używanych
        self._update_recent_profiles(profile_name)
        
        # Odśwież widok przycisków
        if hasattr(self, 'settings_tab_instance') and hasattr(self.settings_tab_instance, 'recent_profiles_container'):
            self.settings_tab_instance._create_recent_profile_buttons_simple(self.settings_tab_instance.recent_profiles_container)
        if hasattr(self, 'home_tab_instance') and hasattr(self.home_tab_instance, 'recent_profiles_container'):
            self.home_tab_instance._create_recent_profile_buttons_simple(self.home_tab_instance.recent_profiles_container)

        messagebox.showinfo(translate("profile_loaded_title"), translate("profile_loaded").format(profile=profile_name))

    def delete_profile(self):
        profile_name = self.profile_name_var.get().strip()
        if not profile_name:
            messagebox.showwarning(translate("warning_no_profile"), translate("select_profile"))
            return
        if profile_name not in self.profiles_data:
            messagebox.showerror(translate("error"), translate("profile_not_found").format(profile=profile_name))
            self.logger.warning(translate("logger_profile_not_found").format(profile=profile_name))
            return

        if messagebox.askyesno(translate("confirm_delete_title"), translate("confirm_delete_profile").format(profile=profile_name)):
            del self.profiles_data[profile_name]
            save_profiles_to_file(self.profiles_data)

            if profile_name in self.profile_list:
                self.profile_list.remove(profile_name)
                
                # Aktualizuj też w configu
                recent = config.settings.get("recent_profiles", [])
                if profile_name in recent:
                    recent.remove(profile_name)
                    config.settings["recent_profiles"] = recent
                    config.save_settings(SETTINGS_FILE)

                if self.profile_combo is not None:
                    self.profile_combo['values'] = self.profile_list
            self.profile_name_var.set("")

            if hasattr(self, 'settings_tab_instance') and hasattr(self.settings_tab_instance, 'recent_profiles_container'):
                self.settings_tab_instance._create_recent_profile_buttons_simple(self.settings_tab_instance.recent_profiles_container)

            if hasattr(self, 'home_tab_instance') and hasattr(self.home_tab_instance, 'recent_profiles_container'):
                self.home_tab_instance._create_recent_profile_buttons_simple(self.home_tab_instance.recent_profiles_container)

            messagebox.showinfo(translate("profile_deleted_title"), translate("profile_deleted").format(profile=profile_name))
            self.logger.info(translate("logger_profile_deleted").format(profile=profile_name))

    def save_settings_local(self) -> bool:
        """Pobiera wartości z GUI i aktualizuje globalny słownik config.settings."""
        self.logger.debug(translate("logger_start_save_settings"))
        try:
            # --- Ustawienia globalne i współdzielone ---
            config.settings["file_path"] = self.file_path.get()
            config.settings["output_dir"] = self.output_dir.get()
            config.settings["create_order_folder"] = self.create_order_folder.get()
            config.settings["barcode_text_position"] = self.barcode_text_position.get()
            config.settings["product_mode"] = self.product_mode.get()
            config.settings["processing_mode"] = self.processing_mode.get()

            # --- Ustawienia Billboard ---
            billboard_settings = config.settings.setdefault("billboard_settings", {})
            billboard_settings["rows"] = int(self.rows.get())
            billboard_settings["cols"] = int(self.cols.get())
            billboard_settings["overlap"] = float(self.overlap.get())
            billboard_settings["white_stripe"] = float(self.white_stripe.get())
            billboard_settings["add_white_to_overlap"] = self.add_white_to_overlap.get()
            billboard_settings["layout"] = self.layout.get()
            billboard_settings["output_type"] = self.output_type.get()
            billboard_settings["registration_mark_type"] = self.reg_mark.get()
            billboard_settings["barcode_type"] = self.barcode_type.get()
            billboard_settings["bryt_order"] = self.bryt_order.get()
            billboard_settings["enable_reg_marks"] = self.enable_reg_marks.get()
            billboard_settings["enable_barcode"] = self.enable_barcode.get()
            billboard_settings["enable_separation_lines"] = self.enable_separation_lines.get()
            billboard_settings["add_line_at_start"] = self.add_line_at_start.get()
            billboard_settings["add_line_at_end"] = self.add_line_at_end.get()
            billboard_settings["slice_rotation"] = int(self.slice_rotation.get())
            billboard_settings["draw_slice_border"] = self.draw_slice_border.get()
            billboard_settings["sep_line_length"] = float(self.sep_line_length.get())

            # --- Scaling Settings ---
            scaling_settings = config.settings.setdefault("scaling_settings", {})
            scaling_settings["scale_non_uniform"] = self.scale_non_uniform.get()
            scaling_settings["scale_den"] = self.scale_den.get()
            scaling_settings["scale_den_x"] = self.scale_den_x.get()
            scaling_settings["scale_den_y"] = self.scale_den_y.get()
            scaling_settings["out_width_cm"] = self.out_width_cm.get()
            scaling_settings["out_height_cm"] = self.out_height_cm.get()

            # --- Poster Settings ---
            poster_settings = config.settings.setdefault("poster_settings", {})
            try:
                poster_settings["repetitions"] = int(self.poster_repetitions.get())
                if not (1 <= poster_settings["repetitions"] <= 10):
                    poster_settings["repetitions"] = 1
                    self.logger.warning("Invalid poster repetitions value, falling back to 1.")
            except ValueError:
                poster_settings["repetitions"] = 1
                self.logger.warning("Invalid poster repetitions value, falling back to 1.")
            try:
                poster_settings["margin_external"] = float(self.poster_margin_external.get())
            except ValueError:
                poster_settings["margin_external"] = 2.0
                self.logger.warning("Invalid poster external margin value, falling back to 2.0.")
            poster_settings["separation_lines"] = self.poster_separation_lines.get()
            try:
                poster_settings["input_rotation"] = int(self.poster_input_rotation.get())
            except ValueError:
                poster_settings["input_rotation"] = 0
                self.logger.warning("Invalid poster input rotation value, falling back to 0.")
            poster_settings["vertical_cut_marks"] = self.poster_vertical_cut_marks.get()
            poster_settings["enable_barcode"] = self.poster_enable_barcode.get()
            poster_settings["add_line_at_start"] = self.poster_add_line_at_start.get()
            poster_settings["add_line_at_end"] = self.poster_add_line_at_end.get()
            try:
                poster_settings["poster_gap"] = float(self.poster_gap.get())
            except ValueError:
                poster_settings["poster_gap"] = 2.0
                self.logger.warning("Invalid poster gap value, falling back to 2.0.")

            # --- POS Settings ---
            pos_settings = config.settings.setdefault("pos_settings", {})
            pos_settings["enable_barcode"] = self.pos_enable_barcode.get()

            # --- Manufacturer Spec ---
            spec_settings = config.settings.setdefault("manufacturer_spec", {})
            spec_settings["enabled"] = self.manufacturer_spec_enabled.get()
            spec_settings["name"] = self.manufacturer_spec_name.get()

            # --- Rasterization Settings ---
            raster_settings = config.settings.setdefault("rasterization", {})
            raster_settings["enabled"] = self.rasterization_enabled.get()
            raster_settings["dpi"] = self.rasterization_dpi.get()
            raster_settings["compression"] = self.rasterization_compression.get()

            # --- Zakładka Ustawienia (Graphic and Code Settings) ---
            graphic_settings = config.settings.setdefault("graphic_settings", {})
            for key, var in self.graphic_vars.items():
                try:
                    graphic_settings[key] = float(var.get())
                except ValueError:
                    graphic_settings[key] = 0.0
                    self.logger.warning(translate("logger_invalid_value").format(key=key))

            config.settings["logging_mode"] = self.logging_mode.get()
            config.settings["log_file_path"] = self.log_file_path.get()
            config.settings["logging_level"] = self.logging_level.get()

            code_settings_target = graphic_settings.setdefault("code_settings", {})
            for code_type, output_types in self.code_gui_vars.items():
                code_settings_target.setdefault(code_type, {})
                for output_type_key, layouts in output_types.items():
                    code_settings_target[code_type].setdefault(output_type_key, {})
                    for layout_key, params in layouts.items():
                        code_settings_target[code_type][output_type_key].setdefault(layout_key, {})
                        for param_key, var in params.items():
                            value_str = var.get()
                            target_dict = code_settings_target[code_type][output_type_key][layout_key]
                            if param_key == "anchor":
                                target_dict[param_key] = value_str
                            else:
                                try:
                                    target_dict[param_key] = float(value_str)
                                except ValueError:
                                    target_dict[param_key] = 0.0
                                    self.logger.warning(translate("logger_invalid_value").format(key=param_key))

            self.logger.debug(translate("logger_end_save_settings"))
            return True

        except ValueError as e:
            messagebox.showerror(translate("conversion_error_title"), translate("conversion_error").format(error=e))
            self.logger.error(translate("logger_conversion_error").format(error=e))
            return False
        except Exception as e:
            messagebox.showerror(translate("settings_save_error_title"), translate("settings_save_error").format(error=e))
            self.logger.error(translate("logger_unexpected_save_error").format(error=e), exc_info=True)
            return False



    def update_gui_from_config(self):
        """Aktualizuje wartości w GUI na podstawie globalnego config.settings."""
        self.logger.debug(translate("logger_update_gui"))
        try:
            # --- Ustawienia globalne i współdzielone ---
            self.file_path.set(config.settings.get("file_path", ""))
            self.output_dir.set(config.settings.get("output_dir", ""))
            self.create_order_folder.set(config.settings.get("create_order_folder", False))
            self.barcode_text_position.set(config.settings.get("barcode_text_position", "side"))
            self.product_mode.set(config.settings.get("product_mode", "billboard"))
            self.processing_mode.set(config.settings.get("processing_mode", "hdd"))

            # --- Ustawienia Billboard (z fallbackiem dla starych profili) ---
            billboard_settings = config.settings.get("billboard_settings", {})
            
            def get_bb_val(key, legacy_key, default):
                return billboard_settings.get(key, config.settings.get(legacy_key, default))

            self.rows.set(str(get_bb_val("rows", "split_rows", 2)))
            self.cols.set(str(get_bb_val("cols", "split_cols", 5)))
            self.overlap.set(str(get_bb_val("overlap", "overlap", 20.0)))
            self.white_stripe.set(str(get_bb_val("white_stripe", "white_stripe", 10.0)))
            self.add_white_to_overlap.set(get_bb_val("add_white_to_overlap", "add_white_to_overlap", True))
            self.draw_slice_border.set(get_bb_val("draw_slice_border", "draw_slice_border", False))
            self.layout.set(get_bb_val("layout", "layout", "layout_vertical"))
            self.output_type.set(get_bb_val("output_type", "output_type", "output_common_sheet"))
            self.reg_mark.set(get_bb_val("registration_mark_type", "registration_mark_type", "reg_mark_cross"))
            self.barcode_type.set(get_bb_val("barcode_type", "barcode_type", "code_qr"))
            self.bryt_order.set(get_bb_val("bryt_order", "bryt_order", "bryt_order_1"))
            self.enable_reg_marks.set(get_bb_val("enable_reg_marks", "enable_reg_marks", True))
            self.enable_barcode.set(get_bb_val("enable_barcode", "enable_barcode", True))
            self.enable_separation_lines.set(get_bb_val("enable_separation_lines", "enable_separation_lines", True))
            self.add_line_at_start.set(get_bb_val("add_line_at_start", "add_line_at_start", False))
            self.add_line_at_end.set(get_bb_val("add_line_at_end", "add_line_at_end", False))
            self.slice_rotation.set(str(get_bb_val("slice_rotation", "slice_rotation", 0)))
            self.sep_line_length.set(str(get_bb_val("sep_line_length", "sep_line_length", 0.0)))

            # --- Scaling Settings ---
            scaling_settings = config.settings.get("scaling_settings", {})
            self.scale_non_uniform.set(scaling_settings.get("scale_non_uniform", False))
            self.scale_den.set(scaling_settings.get("scale_den", 10.0))
            self.scale_den_x.set(scaling_settings.get("scale_den_x", 10.0))
            self.scale_den_y.set(scaling_settings.get("scale_den_y", 10.0))
            self.out_width_cm.set(scaling_settings.get("out_width_cm", 0.0))
            self.out_height_cm.set(scaling_settings.get("out_height_cm", 0.0))

            # --- Poster Settings ---
            poster_settings = config.settings.get("poster_settings", {})
            self.poster_repetitions.set(poster_settings.get("repetitions", 1))
            self.poster_margin_external.set(str(poster_settings.get("margin_external", 2.0)))
            self.poster_separation_lines.set(poster_settings.get("separation_lines", False))
            self.poster_input_rotation.set(poster_settings.get("input_rotation", 0))
            self.poster_vertical_cut_marks.set(poster_settings.get("vertical_cut_marks", False))
            self.poster_enable_barcode.set(poster_settings.get("enable_barcode", True))
            self.poster_add_line_at_start.set(poster_settings.get("add_line_at_start", False))
            self.poster_add_line_at_end.set(poster_settings.get("add_line_at_end", False))

            # --- POS Settings ---
            pos_settings = config.settings.get("pos_settings", {})
            self.pos_enable_barcode.set(pos_settings.get("enable_barcode", True))
            self.poster_gap.set(str(poster_settings.get("poster_gap", 2.0)))

            # --- Zakładka Ustawienia ---
            graphic_settings = config.settings.get("graphic_settings", {})
            for key, var in self.graphic_vars.items():
                var.set(str(graphic_settings.get(key, "")))

            logging_mode_key = config.settings.get("logging_mode", "logging_console")
            self.logging_mode.set(logging_mode_key)
            self.log_file_path.set(config.settings.get("log_file_path", ""))
            self.logging_level.set(config.settings.get("logging_level", "INFO"))

            # --- Rasterization Settings ---
            raster_settings = config.settings.get("rasterization", {})
            self.rasterization_enabled.set(raster_settings.get("enabled", False))
            self.rasterization_dpi.set(raster_settings.get("dpi", 300))
            self.rasterization_compression.set(raster_settings.get("compression", "LZW"))

            code_settings_root = graphic_settings.get("code_settings", {})
            code_params_defaults = {"scale": 10.0, "scale_x": 50.0, "scale_y": 10.0,
                                    "offset_x": 0.0, "offset_y": 0.0, "rotation": 0.0, "anchor": "bottom-left"}

            for code_type, output_types in self.code_gui_vars.items():
                type_settings = code_settings_root.get(code_type, {})
                for output_type_key, layouts in output_types.items():
                    output_settings = type_settings.get(output_type_key, {})
                    for layout_key, params in layouts.items():
                        layout_settings = output_settings.get(layout_key, {})
                        for param_key, var in params.items():
                            default_val = code_params_defaults.get(param_key, "")
                            current_val = layout_settings.get(param_key, default_val)
                            var.set(str(current_val))

            self.logger.debug(translate("logger_end_update_gui"))
        except Exception as e:
            messagebox.showerror(translate("update_gui_error_title"), translate("update_gui_error").format(error=e))
            self.logger.error(translate("logger_update_gui_error").format(error=e), exc_info=True)
        # Zaktualizuj tłumaczenia w comboboxach na zakładce Głównej
        if hasattr(self, 'home_tab_instance'):
            try:
                self.home_tab_instance.update_combobox_values()
            except Exception as e:
                self.logger.error(f"Błąd aktualizacji comboboxów: {e}", exc_info=True)



    def generate_pdf(self):
        """Uruchamia proces generowania PDF w osobnym wątku, aby nie blokować GUI."""
        self.logger.info(translate("logger_start_pdf"))
        if not self.save_settings_local():
            self.logger.warning(translate("logger_pdf_save_error"))
            return

        # Walidacja ścieżek przed uruchomieniem wątku
        output_directory = self.output_dir.get()
        input_file = self.file_path.get()

        if self.create_order_folder.get():
            if input_file and os.path.exists(input_file):
                order_folder_name = os.path.splitext(os.path.basename(input_file))[0]
                output_directory = os.path.join(output_directory, order_folder_name)
                try:
                    os.makedirs(output_directory, exist_ok=True)
                    self.logger.info(f"Utworzono lub potwierdzono istnienie folderu zamówienia: {output_directory}")
                except OSError as e:
                    messagebox.showerror(translate("error"), f"Nie można utworzyć folderu zamówienia: {output_directory}\nBłąd: {e}")
                    return
            else:
                messagebox.showwarning(translate("error"), "Aby utworzyć folder zamówienia, najpierw wybierz poprawny plik wejściowy.")
                return
        
        if not output_directory or not os.path.isdir(output_directory):
            messagebox.showerror(translate("error_output_dir_title"), translate("error_output_dir").format(directory=output_directory))
            self.logger.warning(translate("logger_invalid_output_dir").format(directory=output_directory))
            return

        if not input_file or not os.path.isfile(input_file):
            messagebox.showerror(translate("error_input_file_title"), translate("error_input_file").format(file=input_file))
            self.logger.warning(translate("logger_invalid_input_file").format(file=input_file))
            return
            
        # Natychmiastowe uruchomienie paska postępu
        home_ui = self.home_tab_instance
        home_ui.start_progress(home_ui.output_preview_canvas, home_ui.output_preview_progress)

        def worker():
            """Funkcja, która zostanie wykonana w osobnym wątku."""
            try:
                # Zbierz wszystkie argumenty do jednego słownika kwargs
                kwargs = {
                    "input_pdf_path": config.settings.get("file_path"),
                    "output_dir": output_directory,
                }

                # Dodaj kluczowe sekcje ustawień do kwargs, aby silnik miał do nich bezpośredni dostęp
                kwargs["scaling_settings"] = config.settings.get("scaling_settings", {})
                kwargs["graphic_settings"] = config.settings.get("graphic_settings", {})

                # Dodaj ustawienia globalne/współdzielone
                shared_keys = ["enable_barcode", "barcode_type", "add_line_at_start", "add_line_at_end"]
                for key in shared_keys:
                    kwargs[key] = config.settings.get(key)

                # Dodaj ustawienia specyficzne dla produktu
                product_mode = config.settings.get("product_mode")
                if product_mode == 'billboard':
                    kwargs.update(config.settings.get("billboard_settings", {}))
                elif product_mode == 'poster':
                    kwargs.update(config.settings.get("poster_settings", {}))
                elif product_mode == 'pos':
                    kwargs.update(config.settings.get("pos_settings", {}))

                # Długotrwała operacja cięcia plików
                result = self.splitter.split(**kwargs)
                
                # Umieść wynik w kolejce, aby główny wątek mógł go odczytać
                self.work_queue.put(result)
            except Exception as e:
                # W razie błędu w wątku, również przekaż go do kolejki
                self.work_queue.put(e)

        # Uruchomienie wątku
        threading.Thread(target=worker, daemon=True).start()
        # Rozpoczęcie cyklicznego sprawdzania kolejki
        self.process_queue()

    def process_queue(self):
        """
        Sprawdza kolejkę z wynikiem pracy wątku.
        Obsługuje wyjątki oraz sukces (True). Po sukcesie pobiera ścieżki
        z instancji splittera, buduje słownik _last_result_paths i wywołuje podgląd.
        """
        try:
            item = self.work_queue.get_nowait()

            # --- JEST ELEMENT W KOLEJCE ---
            home_ui = getattr(self, "home_tab_instance", None)
            if home_ui:
                home_ui.stop_progress(home_ui.output_preview_canvas, home_ui.output_preview_progress)

            if isinstance(item, Exception):
                self.logger.error(f"Błąd wątku generowania PDF: {item}", exc_info=True)
                messagebox.showerror(translate("error"), str(item))
                # Nie kontynuujemy pętli po błędzie, czekamy na następną akcję użytkownika
                return

            if item is True:
                # Sukces - pobierz dane z instancji splittera i ustawień
                generated_files = self.splitter.generated_output_files
                mode = self.output_type.get()
                layout = self.layout.get()
                product_mode = self.product_mode.get()

                common_sheet_path = None
                separate_files_paths = []
                poster_path = None

                for f in generated_files:
                    if "_poster.pdf" in os.path.basename(f):
                        poster_path = f
                    elif "_separated.pdf" in os.path.basename(f):
                        common_sheet_path = f
                    else:
                        separate_files_paths.append(f)
                
                separate_files_paths.sort()

                # Ustal preferowany plik do podglądu
                preferred = None
                if product_mode == 'poster' and poster_path:
                    preferred = poster_path
                elif mode in ("output_common_sheet", "output_both") and common_sheet_path:
                    preferred = common_sheet_path
                elif separate_files_paths:
                    preferred = separate_files_paths[0]

                # Zbuduj słownik wyników
                self._last_result_paths = {
                    "mode": mode,
                    "layout": layout,
                    "product_mode": product_mode,
                    "poster_path": poster_path,
                    "common_sheet_path": common_sheet_path,
                    "separate_files": separate_files_paths,
                    "separate_first_path": separate_files_paths[0] if separate_files_paths else None,
                    "preview_preferred": preferred,
                }

                self.logger.info("Generowanie PDF zakończone sukcesem.")
                
                # Wywołaj aktualizację podglądu z nowymi danymi
                if home_ui:
                    home_ui.update_output_preview(self._last_result_paths, manage_progress=False)
            
            # Po przetworzeniu elementu, nie restartuj pętli. Czekaj na kolejną akcję.
            return

        except Empty:
            # Kolejka pusta, kontynuuj sprawdzanie
            self.root.after(100, self.process_queue)



if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    try:
        from ttkthemes import ThemedTk
        root = ThemedTk(theme="adapta")
    except ImportError:
        root = tk.Tk()
        logging.getLogger('BillboardSplitter').warning(translate("ttkthemes_not_installed"))

    from main_utils import get_base_dir
    base_dir = get_base_dir()
    icon_path = os.path.join(base_dir, "icons", "billboard_icon.ico")
    try:
        root.iconbitmap(icon_path)
    except Exception as e:
        logging.getLogger('BillboardSplitter').error(translate("icon_set_error").format(error=e))

    style = ttk.Style(root)
    try:
        # Istniejący styl dla przycisku akcentującego
        style.configure("Accent.TButton", font=('Segoe UI', 10, 'bold'), foreground="black", background="#0078D7")
        style.map("Accent.TButton",
                  background=[('active', '#005A9E'), ('pressed', '#004C87')])
        
        # --- POCZĄTEK POPRAWEK ---
        # 1. Definicja stylu dla zielonego przycisku.
        #    Zwiększono dopełnienie pionowe do 5 (padding=(10, 5)), aby przycisk był wyższy.
        style.configure("Success.TButton", font=('Segoe UI', 10, 'bold'), foreground="#218838", padding=(10, 5))
        
        # 2. Definicja stylu dla zwykłego przycisku "Zapisz", aby miał taką samą wysokość.
        style.configure("Pad.TButton", padding=(10, 5))

        # 3. Zwiększenie wysokości zakładek, aby pasowały do przycisków.
        style.configure('TNotebook.Tab', padding=(10, 10))
        # --- KONIEC POPRAWEK ---

    except tk.TclError as e:
        logging.getLogger('BillboardSplitter').error(translate("accent_button_style_error").format(error=e))

    app = BillboardSplitterApp(root)
    root.mainloop()