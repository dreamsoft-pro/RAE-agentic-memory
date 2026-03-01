# lang_pl.py
"""
Plik zawierający tłumaczenia dla języka polskiego.
"""

LANG = {
    # ==========================
    #  Aplikacja Ogólne
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Błąd", # Ogólny tytuł błędu
    "no_file": "Brak pliku", # Ogólny tekst 'brak pliku'
    "language": "Język", # Etykieta w menu lub ustawieniach
    "language_switch": "Przełącznik języka", # Tytuł okna/sekcji
    "choose_language": "Wybierz język:", # Etykieta
    "apply_language": "Zastosuj", # Przycisk
    "language_changed": "Język został zmieniony. Niektóre zmiany będą widoczne po ponownym uruchomieniu aplikacji.", # Komunikat po zmianie

    # ========================================
    #  Interfejs Użytkownika (GUI) Elementy
    # ========================================

    # --- Zakładki Główne ---
    "tab_home": " Główna ",
    "tab_settings": " Ustawienia ",
    "tab_help": " Pomoc ",
    "tab_license": " Licencja ",

    # --- Przyciski Ogólne ---
    "button_browse": "Przeglądaj...",
    "browse_folder": "Przeglądaj folder...", # Często używane przy wyborze katalogu
    "button_save": "Zapisz",
    "button_delete": "Usuń",
    "button_close": "Zamknij",
    "save_all_settings": "Zapisz wszystkie ustawienia", # Przycisk w zakładce Ustawienia

    # --- Etykiety Pól (Główna Zakładka) ---
    "label_rows": "Podział pionowy (rzędy):",
    "label_columns": "Podział poziomy (kolumny):",
    "label_overlap": "Zakładka [mm]:",
    "label_white_stripe": "Biały pasek [mm]:",
    "label_add_white_stripe": "Dodaj biały pasek do efektywnej zakładki", # Checkbox
    "label_layout": "Układ wyjścia:",
    "label_output_type": "Typ wyjścia:",
    "label_enable_reg_marks": "Włącz znaczniki pasowania:", # Checkbox
    "label_enable_codes": "Włącz kody:", # Checkbox
    "label_enable_sep_lines": "Włącz linie separujące (między brytami)", # Checkbox
    "label_enable_start_line": "Włącz linię na początku/górze arkusza", # Checkbox
    "label_enable_end_line": "Włącz linię na końcu/dole arkusza", # Checkbox
    "label_bryt_order": "Kolejność brytów:",
    "label_slice_rotation": "Obrót brytów:",
    "label_create_order_folder": "Utwórz folder z numerem zamówienia",

    # --- Sekcje/Ramki (Główna Zakładka) ---
    "section_input_file": " Plik wejściowy ",
    "section_scale_and_dimensions": " Skala i wymiary wyjściowe ",
    "label_original_size": "Rozmiar oryginału:",
    "label_scale_non_uniform": "Skaluj nieproporcjonalnie",
    "label_scale": "Skala: 1:",
    "label_scale_x": "Skala X: 1:",
    "label_scale_y": "Skala Y: 1:",
    "label_output_dimensions": "Wymiar pliku wyjściowego:",
    "label_width_cm": "Szerokość [cm]:",
    "label_height_cm": "Wysokość [cm]:",
    "section_split_settings": " Ustawienia podziału ",
    "section_profiles": " Profile ustawień ",
    "section_save_location": " Lokalizacja zapisu ",
    "section_input_preview": " Podgląd pliku wejściowego ",
    "section_output_preview": " Podgląd pliku wyjściowego ",

    # --- Wartości Opcji (Combobox, Radiobutton itp.) ---
    "layout_vertical": "Pionowo",
    "layout_horizontal": "Poziomo",
    "output_common_sheet": "Wspólny arkusz",
    "output_separate_files": "Osobne pliki",
    "output_both": "Wspólny arkusz i osobne pliki",
    "output_common": "Wspólny arkusz", # Używane też jako etykieta ramki w ustawieniach kodów
    "output_separate": "Osobne pliki",  # Używane też jako etykieta ramki w ustawieniach kodów
    "reg_mark_cross": "Krzyżyk",
    "reg_mark_line": "Linia",
    "code_qr": "QR Code",
    "code_barcode": "Kod kreskowy",
    "bryt_order_1": "A1-An, B1-Bn, .. Standardowo, od góry",
    "bryt_order_2": "A1-An, Bn-B1, .. Serpentyna po rzędach, od góry",
    "bryt_order_3": "A1..B1, A2..B2, .. Po kolumnach, od góry",
    "bryt_order_4": "A1-A2..B2-B1.. Serpentyna po kolumnach, od góry",
    "bryt_order_5": "N1-Nn, (N-1)1-(N-1)n, .. Standardowo, od dołu",
    "bryt_order_6": "N1-Nn, (N-1)n-(N-1)1, .. Serpentyna po rzędach, od dołu",
    "logging_console": "console", # Tryb logowania: tylko konsola
    "logging_file": "file",       # Tryb logowania: tylko plik
    "logging_both": "both",       # Tryb logowania: konsola i plik

    # --- Sekcje/Ramki (Zakładka Ustawienia) ---
    "section_processing_mode": " Operacje cięcia ", 
    "processing_mode_ram": "RAM (w pamięci)",      
    "processing_mode_hdd": "HDD (na dysku)",        
    "graphic_settings": "Ustawienia graficzne",
    "code_settings": "Ustawienia kodów QR / Kreskowych",
    "logging_settings": "Ustawienia logowania",
    "barcode_text_position_label": "Położenie opisu kodu kreskowego:",
    "barcode_text_bottom": "pod spodem",
    "barcode_text_side": "obok",
    "barcode_text_none": "brak",

    # --- Etykiety Pól (Zakładka Ustawienia - Graficzne) ---
    "extra_margin_label": "Margines wokół brytów [mm]:",
    "margin_top_label": "Margines górny [mm]:",
    "margin_bottom_label": "Margines dolny [mm]:",
    "margin_left_label": "Margines lewy [mm]:",
    "margin_right_label": "Margines prawy [mm]:",
    "reg_mark_width_label": "Znacznik pasowania - Szerokość [mm]:",
    "reg_mark_height_label": "Znacznik pasowania - Wysokość [mm]:",
    "reg_mark_white_line_width_label": "Znacznik pasowania - Grubość linii białej [mm]:",
    "reg_mark_black_line_width_label": "Znacznik pasowania - Grubość linii czarnej [mm]:",
    "sep_line_black_width_label": "Linia separująca - Grubość linii czarnej [mm]:",
    "sep_line_white_width_label": "Linia separująca - Grubość linii białej [mm]:",
    "label_sep_line_length": "Długość linii separacyjnej [mm] (0=cała):",
    "slice_gap_label": "Odstęp między brytami/posterami [mm]:",
    "label_draw_slice_border": "Narysuj obramowanie wokół brytu (linia cięcia)",
    'barcode_font_size_label': "Rozmiar czcionki opisu kodu kreskowego [pt]:",

    # --- Etykiety Pól (Zakładka Ustawienia - Kody) ---
    "scale_label": "Rozmiar [mm]:",      # Dla QR Code
    "scale_x_label": "Szer. X [mm]:",    # Dla Kodu Kreskowego
    "scale_y_label": "Wys. Y [mm]:",     # Dla Kodu Kreskowego
    "offset_x_label": "Odsunięcie X [mm]:",
    "offset_y_label": "Odsunięcie Y [mm]:",
    "rotation_label": "Rotacja (°):",
    "anchor_label": "Narożnik:",

    # --- Etykiety Pól (Zakładka Ustawienia - Logowanie) ---
    "logging_mode_label": "Tryb logowania:",
    "log_file_label": "Plik logów:",
    "settings_log_filename_label": "Nazwa pliku z logami:",
    "settings_log_level_label": "Poziom logowania:",
    "settings_log_to_file_label": "Zapisuj logi do pliku",
    
    "rasterization_title": "Rasteryzacja wejścia",
    "rasterization_enable": "Włącz rasteryzację",
    "rasterization_dpi": "Rozdzielczość (DPI)",
    "rasterization_compression": "Kompresja",
    "rasterization_compression_none": "Brak",
    "rasterization_compression_lzw": "LZW (bezstratna)",

    "actual_size": "Rzeczywisty rozmiar",
    "size_read_error": "Błąd odczytu rozmiaru",
    "preview_error": "Błąd podglądu",

    "section_product_mode": "Tryb produktu",
    "product_mode_billboard": "Billboard",
    "product_mode_poster": "Poster",
    "product_mode_pos": "POS",
    "section_poster_settings": "Ustawienia posteru",
    "poster_repetitions": "Liczba powtórzeń",
    "poster_external_margin": "Margines zewnętrzny",
    "poster_separation_lines": "Linie separacyjne",
    "poster_input_rotation": "Obrót wejścia",
    "poster_vertical_cut_marks": "Pionowe znaczniki cięcia",
    "poster_gap": "Odstęp między posterami",

    "section_manufacturer_spec": "Specyfikacja producenta",
    "spec_enable": "Użyj specyfikacji producenta",
    "spec_name": "Nazwa specyfikacji",

    "help_title": "Pomoc i informacje",
    "help_content": "To jest treść pomocy...",
    "info_title": "Informacje o aplikacji",

    # --- Przyciski / Akcje (Główna Zakładka) ---
    "button_load": "Wczytaj", # Przycisk profilu
    "button_save_settings": "Zapisz bieżące ustawienia", # Przycisk profilu
    "button_generate_pdf": "Generuj PDF", # Główny przycisk akcji
    "button_refresh_preview": "Odśwież podgląd", # Przycisk podglądu wejścia
    "button_refresh_layout": "Odśwież układ", # (?) Może odświeżenie podglądu wyjścia?

    # --- Licencja (GUI) ---
    "hwid_frame_title": "Unikalny identyfikator sprzętowy (HWID)",
    "copy_hwid": "Kopiuj HWID", # Przycisk
    "license_frame_title": "Aktywacja licencji",
    "enter_license_key": "Wprowadź klucz licencyjny:", # Etykieta
    "activate": "Aktywuj", # Przycisk
    "status_trial": "Tryb próbny", # Status licencji
    "license_active": "Licencja aktywna", # Status licencji

    # ================================================
    #  Komunikaty dla Użytkownika (Okna, Status Bar)
    # ================================================

    # --- Profile ---
    "msg_no_profile_name": "Brak Nazwy", # Tytuł błędu
    "msg_enter_profile_name": "Podaj nazwę profilu do zapisania.", # Treść błędu/ostrzeżenia
    "msg_profile_saved": "Zapisano Profil", # Tytuł sukcesu
    "profile_saved_title": "Zapisano Profil", # Tytuł w loggerze/oknie? (z main.py)
    "msg_profile_saved_detail": "Profil '{0}' został zapisany.", # Treść sukcesu
    "profile_saved": "Profil '{profile}' został zapisany.",
    "profile_saved_and_applied": "Profil '{profile}' został zapisany i zastosowany.", # Treść sukcesu (z main.py)
    "msg_no_profile": "Brak Profilu", # Tytuł błędu
    "warning_no_profile": "Brak Profilu", # Tytuł błędu (z main.py)
    "msg_select_profile": "Wybierz nazwę profilu z listy do wczytania.", # Treść błędu/ostrzeżenia
    "select_profile": "Wybierz nazwę profilu z listy do wczytania.", # Treść błędu/ostrzeżenia (z main.py)
    "profile_loaded_title": "Wczytano Profil", # Tytuł info (z main.py)
    "profile_loaded": "Profil '{profile}' został wczytany.", # Treść info (z main.py)
    "warning_no_profile_delete": "Brak Profilu", # Tytuł błędu przy usuwaniu (z main.py)
    "warning_no_profile_delete_message": "Wybierz profil z listy do usunięcia.", # Treść błędu przy usuwaniu (z main.py)
    "profile_not_found": "Profil '{profile}' nie został znaleziony.", # Komunikat błędu (z main.py)
    "profile_not_exist": "Profil '{profile}' nie istnieje.", # Komunikat błędu przy usuwaniu (z main.py)
    "confirm_delete_title": "Potwierdź Usunięcie", # Tytuł okna potwierdzenia (z main.py)
    "confirm_delete_profile": "Czy na pewno chcesz usunąć profil '{profile}'?", # Treść potwierdzenia (z main.py)
    "profile_deleted_title": "Usunięto Profil", # Tytuł sukcesu (z main.py)
    "profile_deleted": "Profil '{profile}' został usunięty.", # Treść sukcesu (z main.py)

    # --- Pliki / Katalogi ---
    "msg_no_input_file": "Brak pliku wejściowego", # Tytuł błędu
    "msg_unsupported_format": "Format nieobsługiwany", # Tytuł błędu
    "select_file_title": "Wybierz plik wejściowy", # Tytuł okna dialogowego
    "supported_files": "Obsługiwane pliki", # Filtr plików
    "all_files": "Wszystkie pliki", # Filtr plików
    "select_dir_title": "Wybierz katalog wyjściowy", # Tytuł okna dialogowego
    "select_log_dir_title": "Wybierz katalog na pliki logów", # Tytuł okna dialogowego
    "error_output_dir_title": "Błąd Katalogu Wyjściowego", # Tytuł błędu (z main.py)
    "error_output_dir": "Podany katalog wyjściowy jest nieprawidłowy lub nie istnieje:\n{directory}", # Treść błędu (z main.py)
    "error_input_file_title": "Błąd Pliku Wejściowego", # Tytuł błędu (z main.py)
    "error_input_file": "Podany plik wejściowy jest nieprawidłowy lub nie istnieje:\n{file}", # Treść błędu (z main.py)
    "save_file_error_title": "Błąd Zapisu Pliku", # Tytuł błędu (z main.py)
    "save_file_error": "Nie udało się zapisać pliku: {error}", # Treść błędu (z main.py)

    # --- Przetwarzanie PDF / Podgląd ---
    "msg_pdf_processing_error": "Nie udało się przetworzyć pliku PDF", # Tytuł błędu
    "msg_thumbnail_error": "Błąd wczytywania miniatury", # Tytuł błędu
    "msg_no_pdf_output": "Brak wyjścia PDF", # Tytuł informacji/ostrzeżenia (dla podglądu)
    "no_pdf_pages": "Brak stron w pliku PDF", # Komunikat na podglądzie (z main.py)
    "unsupported_output": "Nieobsługiwany typ wyjścia dla podglądu", # Komunikat na podglądzie (z main.py)
    "pdf_generated_title": "Generowanie Zakończone", # Tytuł sukcesu (z main.py)
    "pdf_generated": "Plik(i) PDF zostały wygenerowane pomyślnie w katalogu:\n{directory}", # Treść sukcesu (z main.py)
    "pdf_generation_error_title": "Błąd Generowania", # Tytuł błędu (z main.py)
    "pdf_generation_error": "Podczas generowania PDF wystąpiły błędy. Sprawdź logi po więcej informacji.", # Treść błędu (z main.py)
    "critical_pdf_error_title": "Krytyczny Błąd Generowania PDF", # Tytuł błędu (z main.py)
    "critical_pdf_error": "Wystąpił krytyczny błąd podczas generowania PDF:\n{error}\nSprawdź logi.", # Treść błędu (z main.py)

    # --- Ustawienia ---
    "settings_saved_title": "Zapisano Ustawienia", # Tytuł info (z main.py)
    "settings_saved": "Ustawienia zostały zapisane do pliku:\n{filepath}", # Treść info (z main.py)
    "settings_save_error_title": "Błąd Zapisu Ustawień", # Tytuł błędu (z main.py)
    "settings_save_error": "Nie udało się zapisać ustawień: {error}", # Treść błędu (z main.py)
    "conversion_error_title": "Błąd Konwersji", # Tytuł błędu (z main.py)
    "conversion_error": "Błąd podczas konwersji wartości z GUI: {error}", # Treść błędu (z main.py)
    "update_gui_error_title": "Błąd Aktualizacji GUI", # Tytuł błędu (z main.py)
    "update_gui_error": "Wystąpił błąd podczas aktualizacji interfejsu: {error}", # Treść błędu (z main.py)

    # --- Licencja ---
    "hwid_copied_to_clipboard": "HWID został skopiowany do schowka", # Komunikat info
    "computer_hwid": "HWID komputera", # Etykieta (?)
    "public_key_load_error": "Błąd ładowania klucza publicznego: {error}", # Komunikat błędu
    "invalid_license_format": "Nieprawidłowy format klucza licencyjnego: {error}", # Komunikat błędu
    "activation_success": "Licencja została pomyślnie aktywowana.", # Komunikat sukcesu
    "activation_error": "Błąd aktywacji licencji: {error}", # Komunikat błędu
    "log_trial_mode_active": "Tryb trial jest aktywny",
    "log_trial_mode_inactive": "Tryb trial jest nieaktywny",

    # --- Inicjalizacja ---
    "init_error_title": "Błąd inicjalizacji", # Tytuł błędu (z main.py)
    "init_error": "Błąd inicjalizacji katalogów: {error}", # Treść błędu (z main.py)
    "poppler_path_info": "Informacja o ścieżce Poppler", # Tytuł okna (z main.py - get_poppler_path)
    "ttkthemes_not_installed": "Ostrzeżenie: Biblioteka ttkthemes nie jest zainstalowana. Używam domyślnego stylu Tkinter.", # Komunikat ostrzeżenia (z main.py)

    # =====================================
    #  Logi (Komunikaty Rejestratora)
    # =====================================

    # --- Logowanie Ogólne / Konfiguracja ---
    "log_configured": "Logowanie skonfigurowane: poziom={0}, tryb={1}, plik={2}",
    "log_no_handlers": "Ostrzeżenie: Brak skonfigurowanych handlerów logowania (tryb: {0}).",
    "log_critical_error": "Krytyczny błąd konfiguracji logowania: {0}",
    "log_basic_config": "Użyto podstawowej konfiguracji logowania z powodu błędu.",
    "log_dir_create_error": "Krytyczny błąd: Nie można utworzyć katalogu logów {0}: {1}", # Może być też w sekcji Init

    # --- Logi - Inicjalizacja / Katalogi (`init_directories.py`) ---
    "error_critical_init": "BŁĄD KRYTYCZNY podczas inicjalizacji: {0}", # Ogólny błąd init
    "logger_init_error": "Błąd inicjalizacji katalogów: {error}", # Log z main.py
    "directory_created": "Utworzono katalog: {0}",
    "directory_creation_error": "Nie udało się utworzyć katalogu {0}: {1}",
    "sample_file_copied": "Skopiowano przykładowy plik do {0}",
    "sample_file_copy_error": "Błąd przy kopiowaniu przykładowego pliku: {0}",
    "log_created_output_dir": "Utworzono katalog wyjściowy: {0}", # Z metod split_*
    "log_cannot_create_output_dir": "Nie można utworzyć katalogu wyjściowego {0}: {1}", # Z metod split_*

    # --- Logi - Splitter (`splitter.py`) ---
    #   Splitter - Inicjalizacja i Wczytywanie
    "log_graphic_settings_error": "Nie udało się załadować ustawień graficznych przy inicjalizacji: {0}",
    "log_loading_pdf": "Wczytywanie pliku PDF: {0}",
    "log_loading_bitmap": "Wczytywanie pliku bitmapowego: {0}",
    "log_invalid_dpi": "Odczytano nieprawidłowe DPI ({0}). Używam domyślnego {1} DPI.",
    "log_image_dimensions": "Wymiary obrazu: {0}x{1}px, Tryb: {2}, DPI: {3:.1f} -> {4:.3f}x{5:.3f}pt",
    "log_image_processing_color": "Przetwarzanie obrazu z oryginalnym trybem koloru: {0}",
    "log_unusual_color_mode": "Niestandardowy tryb koloru obrazu: '{0}'. ReportLab/Pillow mogą go nie obsłużyć poprawnie.",
    "log_draw_image_error": "Błąd podczas ReportLab drawImage dla trybu {0}: {1}",
    "log_unsupported_format": "Nieobsługiwany format pliku wejściowego: {0}",
    "log_input_file_not_found": "Plik wejściowy nie znaleziony: {0}",
    "log_load_process_error": "Błąd podczas wczytywania lub przetwarzania pliku {0}: {1}",
    "log_input_file_not_exists": "Plik wejściowy nie istnieje lub ścieżka jest pusta: '{0}'", # Z metody split()
    "log_cannot_load_or_empty_pdf": "Nie udało się wczytać pliku wejściowego lub plik PDF jest pusty/uszkodzony.", # Z metody split()
    "log_pdf_dimensions_info": "  Wymiary PDF: {0:.1f}mm x {1:.1f}mm", # Z metody split()
    "log_invalid_pdf_dimensions": "Nieprawidłowe wymiary strony PDF: {0}x{1} pt.", # Z metody split()

    #   Splitter - Obliczenia Wymiarów
    "log_extra_margin": "Dodatkowy margines ustawiony na {0:.3f} pt",
    "log_invalid_rows_cols": "Nieprawidłowa liczba rzędów ({0}) lub kolumn ({1}).",
    "error_invalid_rows_cols": "Liczba rzędów i kolumn musi być dodatnią liczbą całkowitą.", # Błąd dla użytkownika
    "log_invalid_overlap_white_stripe": "Nieprawidłowe wartości zakładki ({0}) lub białego paska ({1}). Muszą być liczbami.",
    "error_invalid_overlap_white_stripe": "Zakładka i biały pasek muszą być wartościami liczbowymi (mm).", # Błąd dla użytkownika
    "log_stripe_usage": "Ustawiono use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Podstawowy overlap (grafika): {0:.3f} mm, Biały pasek: {1:.3f} mm, Efektywny overlap: {2:.3f} mm",
    "log_computed_dimensions": "Obliczone wymiary: PDF: {0:.3f}mm x {1:.3f}mm. Bryt: {2:.3f}pt ({3:.3f}mm) x {4:.3f}pt ({5:.3f}mm). Rdzeń: {6:.3f}pt x {7:.3f}pt. Efektywna zakładka: {8:.3f}mm",
    "log_invalid_dimensions": "Obliczone wymiary brytu ({0:.3f}x{1:.3f}) lub rdzenia ({2:.3f}x{3:.3f}) są nieprawidłowe dla zakładki={4}, paska={5}, r={6}, k={7}, W={8}mm, H={9}mm", # Poprawiony log błędu wymiarów
    "error_invalid_slice_dimensions": "Obliczone wymiary brytu/rdzenia są nieprawidłowe lub ujemne.", # Błąd dla użytkownika

    #   Splitter - Generowanie Informacji o Brytach i Kolejność
    "log_generating_slice_info": "Generowanie informacji o brycie: {0}",
    "log_no_slices_info_generated": "Nie udało się wygenerować informacji o brytach.",
    "log_applying_rotated_order": "Stosowanie kolejności dla obrotu 180 stopni: {0}", # Logika sortowania
    "log_applying_standard_order": "Stosowanie kolejności dla obrotu 0 stopni (standardowo): {0}", # Logika sortowania
    "log_unknown_bryt_order": "Nieznana kolejność brytów: '{0}'. Używam domyślnej.", # Z metody split()
    "log_final_slices_order": "  Finalna kolejność brytów ({0}): [{1}]", # Z metody split()

    #   Splitter - Tworzenie Overlayów i Scalanie
    "log_invalid_dimensions_overlay": "Próba utworzenia overlay'a z nieprawidłowymi wymiarami: {0}. Pomijanie.",
    "log_empty_overlay": "Utworzono pusty lub prawie pusty overlay PDF. Pomijanie scalania.",
    "log_overlay_error": "Błąd tworzenia overlay'a PDF: {0}",
    "log_merge_error": "Próba scalenia overlay'a bez stron. Pomijanie.",
    "log_merge_page_error": "Błąd podczas scalania overlay'a PDF: {0}",
    "log_fallback_draw_rotating_elements": "Nie można było uzyskać rows/cols dla _draw_rotating_elements, użyto 1x1.",
    "log_overlay_created_for_slice": "Utworzono overlay pasków/znaczników dla brytu {0}",
    "log_overlay_creation_failed_for_slice": "Nie udało się utworzyć overlay'a pasków/znaczników dla {0}",
    "log_merging_rotated_overlay": "Scalanie OBRÓCONEGO overlay'a pasków/znaczników dla {0} z T={1}",
    "log_merging_nonrotated_overlay": "Scalanie NIEobróconego overlay'a pasków/znaczników dla {0}",
    "log_merging_all_codes_overlay": "Scalanie overlay'a wszystkich kodów (bez rotacji)",
    "log_merging_separation_lines_overlay": "Scalanie overlay'a linii separacyjnych (bez rotacji)",
    "log_merging_code_overlay_for_slice": "Overlay kodu dla {0} scalany bez rotacji.", # Dla osobnych plików
    "log_merging_separation_overlay_for_slice": "Overlay linii separacyjnych dla {0} scalany bez rotacji.", # Dla osobnych plików

    #   Splitter - Rysowanie Elementów Graficznych (Paski, Znaczniki, Linie)
    "log_drawing_top_stripe": "[Canvas Draw] Rysowanie paska górnego dla {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas Draw] Rysowanie paska prawego dla {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas Draw] Wypełnianie i obrys rogu dla {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Rysowanie krzyżyka wyśrodkowanego w ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Rysowanie linii rej. dla {0} w obszarze od ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Rysowanie linii pionowej prawej: x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  Rysowanie linii poziomej górnej: y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "Rysowanie linii separacji (biała na czarnej): ({0}) @ ({1:.3f}, {2:.3f}), dł={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Rysowanie krzyżyków dla {0} [{1},{2}] / [{3},{4}] w obszarze od ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Obliczone środki: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Rysowanie TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Rysowanie TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Rysowanie BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Rysowanie BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Pominięto {0} zgodnie z regułą dla pozycji [{1},{2}]",
    "log_trial_common_sheet": "Nakładanie napisu TRIAL na wspólny arkusz",

    # Znak wodny
    "log_trial_watermark_added": "Watermark TRIAL został dodany",
    "error_drawing_trial_text": "Błąd podczas rysowania watermarku: {error}",

    #   Splitter - Rysowanie Linii Separujących (Cała Strona)
    "log_drawing_separation_lines_for_page": "Rysowanie linii separacyjnych dla strony (layout={0}, total_slices={1}, slice_index={2})",
    "log_vertical_line_between_slices": "  Linia pionowa między brytami {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Linia pionowa start @ x={0:.1f}",
    "log_vertical_line_end": "  Linia pionowa end @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Linia pozioma między brytami {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Linia pozioma start @ y={0:.1f}",
    "log_horizontal_line_end": "  Linia pozioma end @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Separate_files) Linia pionowa/pozioma start @ {0:.1f}",
    "log_sep_line_end_separate": "  (Separate_files) Linia pionowa/pozioma end @ {0:.1f}",

    #   Splitter - Generowanie Kodów Kreskowych / QR
    "log_generate_barcode_data": "Generowanie danych kodu kreskowego: {0}",
    "log_barcode_data_shortened": "Dane kodu kreskowego skrócone do {0} znaków.",
    "log_barcode_data_error": "Błąd generowania danych kodu kreskowego: {0}",
    "log_compose_barcode_payload": "Komponowanie payload'u kodu kreskowego ({0}): {1}",
    "log_barcode_payload_shortened": "Payload skrócony do {0} znaków dla formatu {1}",
    "log_barcode_payload_error": "Błąd podczas komponowania payload'u: {0}",
    "log_unknown_anchor_fallback": "Nieznany anchor '{0}', używam bottom-left",
    "log_used_default_code_settings": "Użyto ustawień 'default' dla kodu {0}/{1}.",
    "log_no_layout_key_fallback": "Brak layoutu '{0}' dla {1}/{2}. Użyto pierwszego dostępnego: '{3}'.",
    "log_code_settings_error": "Nie znaleziono lub błąd podczas pobierania ustawień kodu ({0}/{1}/{2}): {3}. Używam domyślnych.",
    "log_drawing_barcode": "Rysowanie {0} w ({1:.3f}, {2:.3f}) [bazowe ({3:.3f}, {4:.3f}) + offset ({5:.3f}, {6:.3f})], rotacja: {7}°",
    "error_generate_qr_svg": "Nie udało się wygenerować QR kodu SVG.", # Błąd dla użytkownika
    "error_invalid_scale_for_qr": "Nieprawidłowa skala dla QR: {0}mm", # Błąd dla użytkownika
    "error_invalid_qr_scale_factor": "Nieprawidłowy współczynnik skali dla QR: {0}", # Błąd dla użytkownika
    "error_generate_barcode_svg": "Nie udało się wygenerować kodu kreskowego SVG.", # Błąd dla użytkownika
    "error_invalid_scale_for_barcode": "Nieprawidłowa skala dla Kodu kreskowego: {0}x{1}mm", # Błąd dla użytkownika
    "error_invalid_barcode_scale_factor": "Nieprawidłowy współczynnik skali dla Kodu kreskowego: ({0:.4f}, {1:.4f})", # Błąd dla użytkownika
    "log_barcode_scale_qr": "  {0}: skala config={1:.3f}mm, szer. SVG={2:.3f}pt, sf={3:.4f}",
    "log_barcode_scale_code128": "  {0}: skala config=({1:.3f}mm, {2:.3f}mm), wym. SVG=({3:.3f}pt, {4:.3f}pt), sf=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Błąd podczas rysowania kodu '{0}': {1}",
    "log_prepared_barcode_info": "Przygotowano info kodu dla {0} ({1}, anchor={2}): pozycja bazowa abs ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Błąd przygotowania danych kodu dla {0}: {1}",
    "log_drawing_barcodes_count": "Rysowanie {0} kodów kreskowych/QR...",
    "log_missing_barcode_info_key": "Brakujący klucz w info kodu kreskowego podczas rysowania: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Błąd podczas rysowania kodu '{0}' w _draw_all_barcodes: {1}",

    #   Splitter - Proces Dzielenia (split_* metody)
    "log_start_splitting_process": "--- Rozpoczynanie procesu podziału dla: {0} ---",
    "log_split_settings": "  Ustawienia: {0}x{1} brytów, Zakładka={2}mm, Biały pasek={3}mm (+zakł: {4})",
    "log_output_dir_info": "  Wyjście: {0} / {1} do '{2}'",
    "log_lines_marks_barcodes_info": "  Linie: Separujące={0}, Start={1}, End={2} | Znaczniki: {3} ({4}), Kody: {5} ({6})",
    "log_bryt_order_info": "  Kolejność: {0}, Obrót brytów: {1}°",
    "log_invalid_dimensions_in_slice_info": "Nieprawidłowe wymiary w slice_info dla {0}: {1}x{2}", # Przy tworzeniu reader'a
    "log_content_transform": "Transformacja treści T_content dla {0}: {1}", # Przy tworzeniu reader'a
    "log_merged_content_for_slice": "Scalono treść dla brytu {0} na new_page", # Przy tworzeniu reader'a
    "log_slice_reader_created": "Utworzono kompletny wycinek (PdfReader) dla brytu {0}", # Przy tworzeniu reader'a
    "log_slice_reader_creation_error": "Błąd tworzenia kompletnego wycinka dla brytu {0}: {1}", # Przy tworzeniu reader'a
    "log_used_get_transform": "Użyto _get_transform (tylko translacja): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Rozpoczynanie: OSOBNE PLIKI (Obrót obsługiwany w create_slice_reader) ---",
    "log_creating_file_for_slice": "Tworzenie pliku dla brytu {0}: {1}",
    "log_invalid_page_size_for_slice": "Nieprawidłowe wymiary strony ({0}x{1}) dla {2}. Pomijanie.", # Dla osobnych plików
    "log_blank_page_creation_error": "Błąd tworzenia strony dla {0} (wymiary {1}x{2}): {3}. Pomijanie.", # Dla osobnych plików
    "log_transform_for_slice": "Transformacja T (tylko translacja) dla {0}: {1}", # Dla osobnych plików
    "log_merging_complete_slice": "Scalanie kompletnego brytu {0} z transformacją: {1}", # Dla osobnych plików
    "log_skipped_slice_merging": "Pominięto scalanie kompletnego brytu dla {0}.", # Dla osobnych plików
    "log_file_saved": "Zapisano plik: {0}", # Dla osobnych plików
    "log_file_save_error": "Błąd zapisu pliku {0}: {1}", # Dla osobnych plików i końcowego
    "log_finished_split_separate_files": "--- Zakończono: OSOBNE PLIKI (Zapisano {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Brak brytów do przetworzenia w split_horizontal.",
    "log_start_split_horizontal": "--- Rozpoczynanie: WSPÓLNY ARKUSZ - POZIOMO (Obrót obsługiwany w create_slice_reader) ---",
    "log_page_dimensions": "Wymiary arkusza: {0:.1f}mm x {1:.1f}mm ({2} brytów)", # Dla wspólnego arkusza H/V
    "log_page_creation_error": "Błąd tworzenia strony wynikowej ({0}x{1}): {2}. Przerywanie.", # Dla wspólnego arkusza H/V
    "log_slice_at_position": "Bryt {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})", # Dla wspólnego arkusza H/V
    "log_transform_t_only": "Transformacja T (tylko translacja) dla {0}: {1}", # Dla wspólnego arkusza H/V
    "log_merging_complete_bryt": "Scalanie kompletnego brytu {0} z transformacją: {1}", # Dla wspólnego arkusza H/V
    "log_skipped_merging_bryt": "Pominięto scalanie kompletnego brytu dla {0}.", # Dla wspólnego arkusza H/V
    "log_file_result_saved": "Zapisano plik wynikowy: {0}", # Dla wspólnego arkusza H/V
    "log_file_result_save_error": "Błąd zapisu pliku wynikowego {0}: {1}", # Dla wspólnego arkusza H/V
    "log_finished_split_horizontal": "--- Zakończono: WSPÓLNY ARKUSZ - POZIOMO ---",
    "log_no_slices_split_vertical": "Brak brytów do przetworzenia w split_vertical.",
    "log_start_split_vertical": "--- Rozpoczynanie: WSPÓLNY ARKUSZ - PIONOWO (Obrót obsługiwany w create_slice_reader) ---",
    "log_finished_split_vertical": "--- Zakończono: WSPÓLNY ARKUSZ - PIONOWO ---",
    "log_unknown_layout": "Nieznany layout dla wspólnego arkusza: '{0}'.", # Błąd w logice split()
    "log_unknown_output_type": "Nieznany typ wyjścia: '{0}'.", # Błąd w logice split()
    "log_finished_splitting_success": "--- Zakończono proces podziału dla: {0} - SUKCES ---", # Podsumowanie split()
    "log_finished_splitting_errors": "--- Zakończono proces podziału dla: {0} - WYSTĄPIŁY BŁĘDY ---", # Podsumowanie split()
    "log_value_error_in_splitting": "Błąd danych wejściowych lub obliczeń: {0}", # Błąd w split()
    "log_finished_splitting_critical_error": "--- Zakończono proces podziału dla: {0} - BŁĄD KRYTYCZNY ---", # Podsumowanie split()
    "log_unexpected_error_in_splitting": "Nieoczekiwany błąd podczas podziału pliku {0}: {1}", # Błąd w split()

    #   Splitter - Tryb Testowy (__main__)
    "log_script_mode_test": "Uruchomiono splitter.py jako skrypt główny (tryb testowy).",
    "log_loaded_config": "Załadowano konfigurację.", # W trybie testowym
    "log_error_loading_config": "Nie udało się załadować konfiguracji: {0}", # W trybie testowym
    "log_created_example_pdf": "Utworzono przykładowy plik PDF: {0}", # W trybie testowym
    "log_cannot_create_example_pdf": "Nie udało się utworzyć przykładowego PDF: {0}", # W trybie testowym
    "log_start_test_split": "Rozpoczynanie testowego podziału pliku: {0} do {1}", # W trybie testowym
    "log_test_split_success": "Testowy podział zakończony sukcesem.", # W trybie testowym
    "log_test_split_errors": "Testowy podział zakończył się błędami.", # W trybie testowym

    # --- Logi - Kody QR/Kreskowe (`barcode_qr.py`) ---
    "log_qr_empty_data": "Próba wygenerowania QR kodu dla pustych danych.",
    "log_qr_generated": "Wygenerowano QR kod SVG dla: {0}...",
    "log_qr_error": "Błąd generowania QR kodu dla danych '{0}': {1}",
    "log_barcode_empty_data": "Próba wygenerowania kodu kreskowego dla pustych danych.",
    "log_barcode_generated": "Wygenerowano kod kreskowy SVG dla: {0}...",
    "log_barcode_error": "Błąd generowania kodu kreskowego dla danych '{0}': {1}",
    "log_basic_handler_configured": "Skonfigurowano podstawowy handler dla loggera w barcode_qr.py", # Jeśli używa własnego fallback loggera
    "log_basic_handler_error": "Nie udało się skonfigurować podstawowego loggera w barcode_qr: {0}", # Jeśli używa własnego fallback loggera

    # --- Logi - Zarządzanie Konfiguracją/Profilami (`main_config_manager.py`) ---
    "loading_profiles_from": "Wczytywanie profili z",
    "profiles_file": "Plik profili",
    "does_not_contain_dict": "nie zawiera słownika. Tworzenie nowego",
    "not_found_creating_new": "nie znaleziony. Tworzenie nowego pustego",
    "json_profiles_read_error": "Błąd odczytu pliku JSON z profilami",
    "file_will_be_overwritten": "Plik zostanie nadpisany przy zapisie",
    "json_decode_error_in_profiles": "Błąd dekodowania JSON w pliku profili",
    "cannot_load_profiles_file": "Nie można wczytać pliku z profilami",
    "unexpected_profiles_read_error": "Nieoczekiwany błąd odczytu profili",
    "saving_profiles_to": "Zapisywanie profili do",
    "cannot_save_profiles_file": "Nie można zapisać pliku z profilami",
    "profiles_save_error": "Błąd zapisu profili do pliku",
    "logger_profile_saved": "Zapisano profil: {profile}", # Log z main.py
    "logger_profile_not_found": "Nie znaleziono profilu do wczytania: {profile}", # Log z main.py
    "logger_profile_loaded": "Wczytano profil: {profile}", # Log z main.py
    "logger_profile_delete_not_exist": "Próba usunięcia nieistniejącego profilu: {profile}", # Log z main.py
    "logger_profile_deleted": "Usunięto profil: {profile}", # Log z main.py
    "logger_start_save_settings": "Rozpoczęto zapisywanie ustawień z GUI.", # Log z main.py
    "logger_invalid_value": "Nieprawidłowa wartość dla '{key}'. Ustawiono 0.0.", # Log z main.py (konwersja)
    "logger_end_save_settings": "Zakończono zapisywanie ustawień z GUI.", # Log z main.py
    "logger_conversion_error": "Błąd konwersji wartości z GUI: {error}", # Log z main.py 
    "conversion_failed": "Konwersja wartości z GUI nie powiodła się",
    "logger_unexpected_save_error": "Nieoczekiwany błąd zapisu ustawień: {error}", # Log z main.py
    "logger_settings_saved": "Zapisano ustawienia do pliku: {file}", # Log z main.py

    # --- Logi - Licencjonowanie (`main_license.py`) ---
    "public_key_load_error_log": "Błąd ładowania klucza publicznego",
    "license_key_decode_error": "Błąd dekodowania klucza licencyjnego",
    "license_activation_error": "Błąd aktywacji licencji",

    # --- Logi - Główny Moduł (`main.py`) ---
    "ui_created": "Interfejs użytkownika został utworzony.",
    "error_tab_home": "Błąd tworzenia UI zakładki 'Główna'",
    "error_tab_settings": "Błąd tworzenia UI zakładki 'Ustawienia'",
    "error_tab_help": "Błąd tworzenia UI zakładki 'Pomoc'",
    "error_creating_license_ui": "Błąd tworzenia UI zakładki 'Licencja'",
    "error_loading_ui": "Błąd ładowania interfejsu: {error}", # Ogólny błąd ładowania UI
    "error_creating_home_ui": "Błąd tworzenia UI zakładki 'Główna'", # Powtórzenie?
    "error_creating_settings_ui": "Błąd tworzenia UI zakładki 'Ustawienia'", # Powtórzenie?
    "error_creating_help_ui": "Błąd tworzenia UI zakładki 'Pomoc'", # Powtórzenie?
    "logger_update_gui": "Rozpoczęto aktualizację GUI z konfiguracji.",
    "logger_end_update_gui": "Zakończono aktualizację GUI z konfiguracji.",
    "logger_update_gui_error": "Nieoczekiwany błąd podczas aktualizacji GUI: {error}",
    "logger_invalid_output_dir": "Nieprawidłowy lub nieistniejący katalog wyjściowy: {directory}",
    "logger_invalid_input_file": "Nieprawidłowy lub nieistniejący plik wejściowy: {file}",
    "logger_start_pdf": "Rozpoczęto proces generowania PDF.",
    "logger_pdf_save_error": "Generowanie PDF przerwane - nie udało się zapisać bieżących ustawień.",
    "logger_pdf_success": "Generowanie PDF zakończone sukcesem.",
    "logger_pdf_exception": "Wyjątek podczas głównego procesu generowania PDF.",
    "icon_set_error": "Nie udało się ustawić ikony aplikacji: {error}",
    "accent_button_style_error": "Nie udało się ustawić stylu dla przycisku akcentu: {error}",
    "logger_file_save_error": "Błąd zapisu pliku {file}: {error}", # Ogólny log błędu zapisu

    #   Logi - Podgląd (`main.py` - update_preview, update_output_preview)
    "thumbnail_error_log": "Błąd generowania miniatury",
    "output_preview_update_called": "Wywołano aktualizację podglądu wyjściowego",
    "output_preview_canvas_missing": "Brak canvasu podglądu wyjściowego",
    "pdf_found_in_output_dir": "Znaleziono PDF w katalogu wyjściowym",
    "preparing_thumbnail": "Przygotowywanie miniatury",
    "thumbnail_generated_successfully": "Miniatura wygenerowana pomyślnie",
    "thumbnail_generation_error": "Błąd generowania miniatury dla",
    "no_pdf_for_common_sheet": "Brak pliku PDF dla wspólnego arkusza do podglądu",
    "no_pdf_for_separate_files": "Brak wygenerowanych osobnych plików PDF do podglądu",
    "cannot_load_thumbnail": "Nie można załadować miniatury z",

    #   Logi - Developerskie / GUI Internals (`main.py`)
    "missing_gui_var_created": "Utworzono brakującą zmienną GUI dla klucza: {key}",
    "missing_gui_structure_created": "Utworzono brakującą strukturę GUI dla: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Utworzono brakującą zmienną GUI dla: {code_type}/{output_type}/{layout}/{param}",



    # Dodatkowe klucze dla main_ui_help.py
    "help_text": """
    Billboard Splitter – Instrukcja Użytkowania\n\n
    Cel programu:\n
    Billboard Splitter służy do automatycznego cięcia projektów billboardów na bryty gotowe do druku. 
    Program został przygotowany do pracy na plikach przygotowanych w skali 1:10.\n 
    Wartości w sekcji: Zakładki, Biały pasek, Ustawienia wpisujemy w skali 1:1
    Program umożliwia układanie wyciętych brytów na arkuszach PDF w zależności od wybranego układu:\n
    • Wspólny arkusz: Wszystkie bryty umieszczone są na jednym dokumencie.\n
    • Osobne pliki: Każdy bryt zapisany jest w osobnym pliku PDF.\n\n
    Dodatkowo program pozwala na:\n
    • Wybór układu – pionowy lub poziomy (odpowiednio: w układzie pionowym linie separacyjne pojawiają się u góry i dołu, 
      a w poziomym z lewej i prawej strony).\n
    • Obrót brytów o 180° (odwrócenie całego projektu).\n
    • Dodanie znaczników pasowania (np. krzyżyków lub linii) ułatwiających precyzyjne pozycjonowanie podczas klejenia.\n
    • Dodanie kodów QR lub kodów kreskowych – generowanych na podstawie danych wejściowych, które pomagają 
      identyfikować poszczególne bryty.\n
    • Zapisywanie ustawień jako profile, które można wczytywać, modyfikować i usuwać, co umożliwia szybkie 
      przełączanie się między różnymi konfiguracjami projektów.\n\n
    Główne kroki korzystania z programu:\n\n
    1. Wybór pliku wejściowego:\n
    • W zakładce 'Główna' wybierz plik PDF, JPG lub TIFF zawierający projekt billboardu.\n
    • Jeśli nie ustawisz własnej ścieżki, domyślnie program ustawi plik przykładowy.\n\n
    2. Ustawienia cięcia:\n
    • Określ liczbę rzędów i kolumn, na które projekt ma zostać podzielony.\n
    • Ustaw rozmiar zakładki (overlap).\n
    • Opcjonalnie możesz określić szerokość białego paska, który zostanie dodany do efektywnej zakładki.\n\n
    3. Wybór układu wyjścia:\n
    • Pionowo: Wszystkie bryty zostaną ułożone na arkuszu PDF pionowo.\n
    • Poziomo: Wszystkie bryty zostaną ułożone na arkuszu PDF poziomo.\n\n
    4. Wybór typu wyjścia:\n
    • Wspólny arkusz: Wszystkie bryty zostaną ułożone na jednym wspólnym arkuszu PDF.\n
    • Osobne pliki: Każdy bryt zostanie zapisany w osobnym pliku PDF.\n
    • W zakładce 'Główna' możesz włączyć i skonfigurować znaczniki pasowania – wybierając między krzyżykiem a linią.\n
    • Opcjonalnie włącz kod QR lub kod kreskowy, który będzie generowany na podstawie danych projektu.\n
    • Parametry kodów (skalowanie, offset, rotacja, pozycja) można szczegółowo dostosować w zakładce 'Ustawienia'.\n\n
    5. Zarządzanie ustawieniami:\n
    • W zakładce 'Ustawienia' możesz precyzyjnie zmodyfikować parametry graficzne (marginesy, grubości linii, odstępy) oraz 
      ustawienia kodów.\n
    • Zapisz bieżące ustawienia jako profil, aby później móc je łatwo wczytać lub modyfikować.\n
    • Profile ustawień (zapisywane w pliku profiles.json) pozwalają szybko przełączać się między różnymi\n
      konfiguracjami projektów.\n\n
    6. Generowanie PDF:\n
    • Po skonfigurowaniu wszystkich parametrów kliknij 'Generuj PDF'.\n
    • Pliki wynikowe zostaną zapisane w katalogu 'output' lub innym wskazanym, a logi (z dzienną rotacją) w katalogu 'logs' 
      lub innym wskazanym.\n\n
    W razie problemów:\n
    • Sprawdź logi znajdujące się w folderze 'logs'. Każdy dzień generuje osobny plik logu z datą w nazwie.\n
    • Upewnij się, że wszystkie wymagane foldery są ustawione.\n
    • Pomoc techniczna: tech@printworks.pl (dni robocze, godziny 8-16)\n
    """
}
