# lang_sk.py
"""
Súbor s prekladmi pre slovenský jazyk.
"""

LANG = {
    "barcode_font_size_label": "Veľkosť písma popisu čiarového kódu [pt]:",
    # ==========================
    #  Aplikácia – Všeobecné
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Chyba",
    "no_file": "Žiadny súbor",
    "language": "Jazyk",
    "language_switch": "Zmena jazyka",
    "choose_language": "Vyberte jazyk:",
    "apply_language": "Použiť",
    "language_changed": "Jazyk bol zmenený. Niektoré zmeny budú viditeľné až po reštarte aplikácie.",

    # ========================================
    #  Prvky používateľského rozhrania (GUI)
    # ========================================

    # --- Hlavné karty ---
    "tab_home": " Domov ",
    "tab_settings": " Nastavenia ",
    "tab_help": " Pomoc ",
    "tab_license": " Licencia ",

    # --- Všeobecné tlačidlá ---
    "button_browse": "Prehľadávať...",
    "browse_folder": "Prehľadávať priečinok...",
    "button_save": "Uložiť",
    "button_delete": "Zmazať",
    "button_close": "Zavrieť",
    "save_all_settings": "Uložiť všetky nastavenia",

    # --- Popisky polí (karta Domov) ---
    "label_rows": "Vertikálne delenie (riadky):",
    "label_columns": "Horizontálne delenie (stĺpce):",
    "label_overlap": "Presah [mm]:",
    "label_white_stripe": "Biely pruh [mm]:",
    "label_add_white_stripe": "Pridať biely pruh k efektívnemu presahu",
    "label_layout": "Rozloženie výstupu:",
    "label_output_type": "Typ výstupu:",
    "label_enable_reg_marks": "Povoliť registračné značky:",
    "label_enable_codes": "Povoliť kódy:",
    "label_enable_sep_lines": "Povoliť deliace čiary (medzi panelmi)",
    "label_enable_start_line": "Povoliť čiaru začiatku/horný okraj hárku",
    "label_enable_end_line": "Povoliť čiaru konca/dolný okraj hárku",
    "label_bryt_order": "Poradie panelov:",
    "label_slice_rotation": "Otočenie panelov:",
    "label_create_order_folder": "Vytvoriť priečinok s číslom objednávky",

    # --- Sekcie/skupiny (karta Domov) ---
    "section_input_file": " Vstupný súbor ",
    "section_scale_and_dimensions": " Mierka a výstupné rozmery ",
    "label_original_size": "Pôvodná veľkosť:",
    "label_scale_non_uniform": "Neproporcionálne meniť mierku",
    "label_scale": "Mierka: 1:",
    "label_scale_x": "Mierka X: 1:",
    "label_scale_y": "Mierka Y: 1:",
    "label_output_dimensions": "Výstupné rozmery súboru:",
    "label_width_cm": "Šírka [cm]:",
    "label_height_cm": "Výška [cm]:",
    "section_split_settings": " Nastavenia rezu ",
    "section_profiles": " Profily nastavení ",
    "section_save_location": " Miesto uloženia ",
    "section_input_preview": " Náhľad vstupného súboru ",
    "section_output_preview": " Náhľad výstupu ",

    # --- Hodnoty volieb (combobox, radiobutton a pod.) ---
    "layout_vertical": "Vertikálne",
    "layout_horizontal": "Horizontálne",
    "output_common_sheet": "Spoločný hárok",
    "output_separate_files": "Samostatné súbory",
    "output_both": "Spoločný hárok aj samostatné súbory",
    "output_common": "Spoločný hárok",
    "output_separate": "Samostatné súbory",
    "reg_mark_cross": "Kríž",
    "reg_mark_line": "Čiara",
    "code_qr": "QR kód",
    "code_barcode": "Čiarový kód",
    "bryt_order_1": "A1–An, B1–Bn, .. Štandard, zhora",
    "bryt_order_2": "A1–An, Bn–B1, .. Hadovito po riadkoch, zhora",
    "bryt_order_3": "A1..B1, A2..B2, .. Po stĺpcoch, zhora",
    "bryt_order_4": "A1–A2..B2–B1.. Hadovito po stĺpcoch, zhora",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Štandard, zdola",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Hadovito po riadkoch, zdola",
    "logging_console": "konzola",
    "logging_file": "súbor",
    "logging_both": "oboje",

    # --- Sekcie/skupiny (karta Nastavenia) ---
    "section_processing_mode": " Režimy spracovania ",
    "processing_mode_ram": "RAM (v pamäti)",
    "processing_mode_hdd": "Disk (na úložisku)",
    "graphic_settings": "Grafické nastavenia",
    "code_settings": "Nastavenia QR / čiarového kódu",
    "logging_settings": "Nastavenia logovania",
    "barcode_text_position_label": "Pozícia textu pri kóde:",
    "barcode_text_bottom": "dole",
    "barcode_text_side": "zboku",
    "barcode_text_none": "žiadny",

    # --- Popisky (Nastavenia – Grafika) ---
    "extra_margin_label": "Okraj okolo panelov [mm]:",
    "margin_top_label": "Horný okraj [mm]:",
    "margin_bottom_label": "Dolný okraj [mm]:",
    "margin_left_label": "Ľavý okraj [mm]:",
    "margin_right_label": "Pravý okraj [mm]:",
    "reg_mark_width_label": "Registračná značka – šírka [mm]:",
    "reg_mark_height_label": "Registračná značka – výška [mm]:",
    "reg_mark_white_line_width_label": "Registračná značka – hrúbka bielej čiary [mm]:",
    "reg_mark_black_line_width_label": "Registračná značka – hrúbka čiernej čiary [mm]:",
    "sep_line_black_width_label": "Deliaca – hrúbka čiernej čiary [mm]:",
    "sep_line_white_width_label": "Deliaca – hrúbka bielej čiary [mm]:",
    "slice_gap_label": "Medzera medzi panelmi [mm]:",
    "label_draw_slice_border": "Kresliť rám okolo panelu (rezná čiara)",

    # --- Popisky (Nastavenia – Kódy) ---
    "scale_label": "Veľkosť [mm]:",
    "scale_x_label": "Šírka X [mm]:",
    "scale_y_label": "Výška Y [mm]:",
    "offset_x_label": "Posun X [mm]:",
    "offset_y_label": "Posun Y [mm]:",
    "rotation_label": "Otočenie (°):",
    "anchor_label": "Roh:",

    # --- Popisky (Nastavenia – Logy) ---
    "logging_mode_label": "Režim logovania:",
    "log_file_label": "Súbor logu:",
    "logging_level_label": "Úroveň logovania:",

    # --- Tlačidlá / akcie (karta Domov) ---
    "button_load": "Načítať",
    "button_save_settings": "Uložiť aktuálne nastavenia",
    "button_generate_pdf": "Vygenerovať PDF",
    "button_refresh_preview": "Obnoviť náhľad",
    "button_refresh_layout": "Obnoviť rozloženie",

    # --- Licencia (GUI) ---
    "hwid_frame_title": "Jedinečný identifikátor hardvéru (HWID)",
    "copy_hwid": "Kopírovať HWID",
    "license_frame_title": "Aktivácia licencie",
    "enter_license_key": "Zadajte licenčný kľúč:",
    "activate": "Aktivovať",
    "status_trial": "Skúšobný režim",
    "license_active": "Licencia je aktívna",

    # ================================================
    #  Správy pre používateľa (okná, stavový riadok)
    # ================================================

    # --- Profily ---
    "msg_no_profile_name": "Bez názvu",
    "msg_enter_profile_name": "Zadajte názov profilu na uloženie.",
    "msg_profile_saved": "Profil uložený",
    "profile_saved_title": "Profil uložený",
    "msg_profile_saved_detail": "Profil „{0}“ bol uložený.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profil '{profile}' bol uložený a aplikovaný.",
    "msg_no_profile": "Žiadny profil",
    "warning_no_profile": "Žiadny profil",
    "msg_select_profile": "Vyberte v zozname názov profilu na načítanie.",
    "select_profile": "Vyberte v zozname názov profilu na načítanie.",
    "profile_loaded_title": "Profil načítaný",
    "profile_loaded": "Profil „{profile}“ bol načítaný.",
    "warning_no_profile_delete": "Žiadny profil",
    "warning_no_profile_delete_message": "Vyberte v zozname profil, ktorý chcete zmazať.",
    "profile_not_found": "Profil „{profile}“ sa nenašiel.",
    "profile_not_exist": "Profil „{profile}“ neexistuje.",
    "confirm_delete_title": "Potvrďte zmazanie",
    "confirm_delete_profile": "Naozaj chcete zmazať profil „{profile}“?",
    "profile_deleted_title": "Profil zmazaný",
    "profile_deleted": "Profil „{profile}“ bol zmazaný.",

    # --- Súbory / priečinky ---
    "msg_no_input_file": "Žiadny vstupný súbor",
    "msg_unsupported_format": "Nepodporovaný formát",
    "select_file_title": "Vybrať vstupný súbor",
    "supported_files": "Podporované súbory",
    "all_files": "Všetky súbory",
    "select_dir_title": "Vybrať výstupný priečinok",
    "select_log_dir_title": "Vybrať priečinok pre logy",
    "error_output_dir_title": "Chyba výstupného priečinka",
    "error_output_dir": "Zadaný výstupný priečinok je neplatný alebo neexistuje:\n{directory}",
    "error_input_file_title": "Chyba vstupného súboru",
    "error_input_file": "Zadaný vstupný súbor je neplatný alebo neexistuje:\n{file}",
    "save_file_error_title": "Chyba ukladania súboru",
    "save_file_error": "Súbor sa nepodarilo uložiť: {error}",

    # --- Spracovanie PDF / náhľad ---
    "msg_pdf_processing_error": "Zlyhalo spracovanie PDF súboru",
    "msg_thumbnail_error": "Chyba načítania miniatúry",
    "msg_no_pdf_output": "Žiadny PDF výstup",
    "no_pdf_pages": "PDF neobsahuje stránky",
    "unsupported_output": "Nepodporovaný typ výstupu pre náhľad",
    "pdf_generated_title": "Generovanie dokončené",
    "pdf_generated": "PDF súbor(y) boli úspešne vygenerované do priečinka:\n{directory}",
    "pdf_generation_error_title": "Chyba generovania",
    "pdf_generation_error": "Počas generovania PDF došlo k chybám. Skontrolujte logy.",
    "critical_pdf_error_title": "Kritická chyba generovania PDF",
    "critical_pdf_error": "Vyskytla sa kritická chyba pri generovaní PDF:\n{error}\nPozrite logy.",
    "settings_saved_title": "Nastavenia uložené",
    "settings_saved": "Nastavenia boli uložené do súboru:\n{filepath}",
    "settings_save_error_title": "Chyba ukladania nastavení",
    "settings_save_error": "Nastavenia sa nepodarilo uložiť: {error}",
    "conversion_error_title": "Chyba konverzie",
    "conversion_error": "Chyba pri konverzii hodnôt z rozhrania: {error}",
    "update_gui_error_title": "Chyba aktualizácie rozhrania",
    "update_gui_error": "Pri aktualizácii rozhrania došlo k chybe: {error}",

    # --- Licencia ---
    "hwid_copied_to_clipboard": "HWID bol skopírovaný do schránky",
    "computer_hwid": "HWID počítača",
    "public_key_load_error": "Chyba načítania verejného kľúča: {error}",
    "invalid_license_format": "Neplatný formát licenčného kľúča: {error}",
    "activation_success": "Licencia bola úspešne aktivovaná.",
    "activation_error": "Chyba aktivácie licencie: {error}",
    "log_trial_mode_active": "Skúšobný režim je aktívny",
    "log_trial_mode_inactive": "Skúšobný režim nie je aktívny",

    # --- Inicializácia ---
    "init_error_title": "Chyba inicializácie",
    "init_error": "Chyba pri inicializácii priečinkov: {error}",
    "poppler_path_info": "Informácia o ceste Poppler",
    "ttkthemes_not_installed": "Upozornenie: knižnica ttkthemes nie je nainštalovaná. Použije sa predvolený štýl Tkinter.",

    # =====================================
    #  Logy (správy loggera)
    # =====================================

    # --- Všeobecné / Konfigurácia ---
    "log_configured": "Logovanie nastavené: úroveň={0}, režim={1}, súbor={2}",
    "log_no_handlers": "Upozornenie: nie sú nastavené žiadne handlery logov (režim: {0}).",
    "log_critical_error": "Kritická chyba konfigurácie logovania: {0}",
    "log_basic_config": "Pre chybu bola použitá základná konfigurácia logovania.",
    "log_dir_create_error": "Kritická chyba: nemožno vytvoriť priečinok logov {0}: {1}",

    # --- Logy – Inicializácia / Priečinky (init_directories.py) ---
    "error_critical_init": "KRITICKÁ CHYBA počas inicializácie: {0}",
    "logger_init_error": "Chyba inicializácie priečinkov: {error}",
    "directory_created": "Priečinok vytvorený: {0}",
    "directory_creation_error": "Nepodarilo sa vytvoriť priečinok {0}: {1}",
    "sample_file_copied": "Vzorový súbor skopírovaný do {0}",
    "sample_file_copy_error": "Chyba kopírovania vzorového súboru: {0}",
    "log_created_output_dir": "Vytvorený výstupný priečinok: {0}",
    "log_cannot_create_output_dir": "Nedá sa vytvoriť výstupný priečinok {0}: {1}",

    # --- Logy – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Zlyhalo načítanie grafických nastavení počas inicializácie: {0}",
    "log_loading_pdf": "Načítavam PDF súbor: {0}",
    "log_loading_bitmap": "Načítavam rastrový súbor: {0}",
    "log_invalid_dpi": "Načítané neplatné DPI ({0}). Používam predvolené {1} DPI.",
    "log_image_dimensions": "Rozmery obrázka: {0}×{1}px, režim: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Spracovanie obrazu s pôvodným farebným režimom: {0}",
    "log_unusual_color_mode": "Neobvyklý farebný režim: „{0}“. ReportLab/Pillow s ním nemusia pracovať správne.",
    "log_draw_image_error": "Chyba ReportLab drawImage pre režim {0}: {1}",
    "log_unsupported_format": "Nepodporovaný vstupný formát: {0}",
    "log_input_file_not_found": "Vstupný súbor sa nenašiel: {0}",
    "log_load_process_error": "Chyba načítania alebo spracovania súboru {0}: {1}",
    "log_input_file_not_exists": "Vstupný súbor neexistuje alebo je prázdna cesta: „{0}“",
    "log_cannot_load_or_empty_pdf": "Nepodarilo sa načítať vstupný súbor, alebo je PDF prázdne/poškodené.",
    "log_pdf_dimensions_info": "  Rozmery PDF: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Neplatné rozmery stránky PDF: {0}×{1} pt.",

    #   Splitter – Výpočty rozmerov
    "log_extra_margin": "Dodatočný okraj nastavený na {0:.3f} pt",
    "log_invalid_rows_cols": "Neplatný počet riadkov ({0}) alebo stĺpcov ({1}).",
    "error_invalid_rows_cols": "Riadky a stĺpce musia byť kladné celé čísla.",
    "log_invalid_overlap_white_stripe": "Neplatné hodnoty presahu ({0}) alebo bieleho pruhu ({1}). Musia byť číselné.",
    "error_invalid_overlap_white_stripe": "Presah a biely pruh musia byť číselné hodnoty (mm).",
    "log_stripe_usage": "Nastavené use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Základný presah (grafika): {0:.3f} mm, biely pruh: {1:.3f} mm, efektívny presah: {2:.3f} mm",
    "log_computed_dimensions": "Vypočítané: PDF {0:.3f}×{1:.3f} mm. Panel: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Jadro: {6:.3f}×{7:.3f} pt. Efekt. presah: {8:.3f} mm",
    "log_invalid_dimensions": "Neplatné rozmery panelu ({0:.3f}×{1:.3f}) alebo jadra ({2:.3f}×{3:.3f}) pri presah={4}, pruh={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Vypočítané rozmery panelu/jadra sú neplatné alebo záporné.",

    #   Splitter – Generovanie informácií a poradia panelov
    "log_generating_slice_info": "Generujem informácie o paneli: {0}",
    "log_no_slices_info_generated": "Nepodarilo sa vygenerovať informácie o paneloch.",
    "log_applying_rotated_order": "Aplikujem poradie pre otočenie o 180°: {0}",
    "log_applying_standard_order": "Aplikujem poradie pre 0° (štandard): {0}",
    "log_unknown_bryt_order": "Neznáme poradie panelov: „{0}“. Použije sa predvolené.",
    "log_final_slices_order": "  Konečné poradie panelov ({0}): [{1}]",

    #   Splitter – Tvorba overlay a spájanie
    "log_invalid_dimensions_overlay": "Pokus o vytvorenie overlay s neplatnými rozmermi: {0}. Preskakujem.",
    "log_empty_overlay": "Vytvorený prázdny alebo takmer prázdny overlay PDF. Spájanie preskočené.",
    "log_overlay_error": "Chyba vytvárania overlay PDF: {0}",
    "log_merge_error": "Pokus o zlúčenie overlay bez strán. Preskakujem.",
    "log_merge_page_error": "Chyba zlúčenia overlay PDF: {0}",
    "log_fallback_draw_rotating_elements": "Nepodarilo sa získať riadky/stĺpce pre _draw_rotating_elements, použité 1×1.",
    "log_overlay_created_for_slice": "Overlay pruhov/znakov vytvorený pre panel {0}",
    "log_overlay_creation_failed_for_slice": "Nepodarilo sa vytvoriť overlay pre {0}",
    "log_merging_rotated_overlay": "Spájam OTOČENÝ overlay pre {0} s T={1}",
    "log_merging_nonrotated_overlay": "Spájam NEOTOČENÝ overlay pre {0}",
    "log_merging_all_codes_overlay": "Spájam overlay všetkých kódov (bez otočenia)",
    "log_merging_separation_lines_overlay": "Spájam overlay deliacich čiar (bez otočenia)",
    "log_merging_code_overlay_for_slice": "Overlay kódu pre {0} zlúčený bez otočenia.",
    "log_merging_separation_overlay_for_slice": "Overlay deliacich čiar pre {0} zlúčený bez otočenia.",

    #   Splitter – Kreslenie grafických prvkov (pruhy, značky, čiary)
    "log_drawing_top_stripe": "[Canvas Draw] Kreslím horný pruh pre {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas Draw] Kreslím pravý pruh pre {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas Draw] Vyplňujem a orámujem roh pre {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Kreslím kríž so stredom v ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Kreslím registračné čiary pre {0} v oblasti od ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Kreslím pravú vertikálnu čiaru: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Kreslím hornú horizontálnu čiaru: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Kreslím deliacu čiaru (biela cez čiernu): ({0}) @ ({1:.3f}, {2:.3f}), dĺžka={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Kreslím kríže pre {0} [{1},{2}] / [{3},{4}] v oblasti od ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Vypočítané strety: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Kreslím TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Kreslím TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Kreslím BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Kreslím BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Značka {0} vynechaná podľa pravidla pre pozíciu [{1},{2}]",
    "log_trial_common_sheet": "Aplikujem vodoznak TRIAL na spoločnom hárku",

    # Vodoznak
    "log_trial_watermark_added": "Pridaný vodoznak TRIAL",
    "error_drawing_trial_text": "Chyba pri kreslení vodoznaku: {error}",

    #   Splitter – Deliace čiary (celá stránka)
    "log_drawing_separation_lines_for_page": "Kreslím deliace čiary pre stránku (rozloženie={0}, počet panelov={1}, index panelu={2})",
    "log_vertical_line_between_slices": "  Vertikálna čiara medzi panelmi {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Začiatok vertikálnej čiary @ x={0:.1f}",
    "log_vertical_line_end": "  Koniec vertikálnej čiary @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Horizontálna čiara medzi panelmi {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Začiatok horizontálnej čiary @ y={0:.1f}",
    "log_horizontal_line_end": "  Koniec horizontálnej čiary @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Samostatné_súbory) Začiatok vert./horiz. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Samostatné_súbory) Koniec vert./horiz. @ {0:.1f}",

    #   Splitter – Generovanie kódov / QR
    "log_generate_barcode_data": "Generujem dáta pre kód: {0}",
    "log_barcode_data_shortened": "Dáta kódu skrátené na {0} znakov.",
    "log_barcode_data_error": "Chyba generovania dát kódu: {0}",
    "log_compose_barcode_payload": "Skladám payload kódu ({0}): {1}",
    "log_barcode_payload_shortened": "Payload skrátený na {0} znakov pre formát {1}",
    "log_barcode_payload_error": "Chyba skladania payloadu: {0}",
    "log_unknown_anchor_fallback": "Neznámy kotviaci roh „{0}“, použitý ľavý dolný",
    "log_used_default_code_settings": "Použité nastavenia „default“ pre kód {0}/{1}.",
    "log_no_layout_key_fallback": "Pre {1}/{2} neexistuje rozloženie „{0}“. Použité prvé dostupné: „{3}“.",
    "log_code_settings_error": "Nenájdené/Chyba získania nastavení kódu ({0}/{1}/{2}): {3}. Použité predvolené hodnoty.",
    "log_drawing_barcode": "Kreslím {0} na ({1:.3f}, {2:.3f}) [základ ({3:.3f}, {4:.3f}) + posun ({5:.3f}, {6:.3f})], otočenie: {7}°",
    "error_generate_qr_svg": "Zlyhalo generovanie SVG QR kódu.",
    "error_invalid_scale_for_qr": "Neplatná veľkosť QR: {0} mm",
    "error_invalid_qr_scale_factor": "Neplatný mierkový faktor QR: {0}",
    "error_generate_barcode_svg": "Zlyhalo generovanie SVG čiarového kódu.",
    "error_invalid_scale_for_barcode": "Neplatná veľkosť čiarového kódu: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Neplatný mierkový faktor čiarového kódu: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: veľkosť v konfigurácii={1:.3f} mm, šírka SVG={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: veľkosť v konfigurácii=({1:.3f} mm, {2:.3f} mm), rozmer SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Chyba kreslenia kódu „{0}“: {1}",
    "log_prepared_barcode_info": "Pripravené informácie o kóde pre {0} ({1}, kotva={2}): základná absolútna pozícia ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Chyba prípravy dát kódu pre {0}: {1}",
    "log_drawing_barcodes_count": "Kreslím {0} kódov/QR…",
    "log_missing_barcode_info_key": "Chýba kľúč v informácii o kóde pri kreslení: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Chyba kreslenia kódu „{0}“ v _draw_all_barcodes: {1}",

    #   Splitter – Proces rezu (metódy split_*)
    "log_start_splitting_process": "--- Spúšťam proces rezu pre: {0} ---",
    "log_split_settings": "  Nastavenia: {0}×{1} panelov, presah={2} mm, biely pruh={3} mm (+presah: {4})",
    "log_output_dir_info": "  Výstup: {0} / {1} do „{2}“",
    "log_lines_marks_barcodes_info": "  Čiary: deliace={0}, začiatok={1}, koniec={2} | Značky: {3} ({4}), Kódy: {5} ({6})",
    "log_bryt_order_info": "  Poradie: {0}, otočenie panelov: {1}°",
    "log_invalid_dimensions_in_slice_info": "Neplatné rozmery v slice_info pre {0}: {1}×{2}",
    "log_content_transform": "Transformácia obsahu T_content pre {0}: {1}",
    "log_merged_content_for_slice": "Obsah zlúčený pre panel {0} do new_page",
    "log_slice_reader_created": "Kompletný panel (PdfReader) vytvorený pre {0}",
    "log_slice_reader_creation_error": "Chyba vytvorenia kompletného panelu pre {0}: {1}",
    "log_used_get_transform": "Použitý _get_transform (iba posun): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Štart: SAMOSTATNÉ SÚBORY (otočenie v create_slice_reader) ---",
    "log_creating_file_for_slice": "Vytváram súbor pre panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Neplatná veľkosť stránky ({0}×{1}) pre {2}. Preskakujem.",
    "log_blank_page_creation_error": "Chyba vytvárania stránky pre {0} (rozmer {1}×{2}): {3}. Preskakujem.",
    "log_transform_for_slice": "Transformácia T (iba posun) pre {0}: {1}",
    "log_merging_complete_slice": "Zlúčenie kompletného panelu {0} s transformáciou: {1}",
    "log_skipped_slice_merging": "Zlúčenie kompletného panelu pre {0} preskočené.",
    "log_file_saved": "Súbor uložený: {0}",
    "log_file_save_error": "Chyba ukladania súboru {0}: {1}",
    "log_finished_split_separate_files": "--- Dokončené: SAMOSTATNÉ SÚBORY (uložené {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Žiadne panely na spracovanie v split_horizontal.",
    "log_start_split_horizontal": "--- Štart: SPOLOČNÝ HÁROK – HORIZONTÁLNE (otočenie v create_slice_reader) ---",
    "log_page_dimensions": "Rozmery stránky: {0:.1f}×{1:.1f} mm ({2} panelov)",
    "log_page_creation_error": "Chyba vytvárania výstupnej stránky ({0}×{1}): {2}. Prerušujem.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformácia T (iba posun) pre {0}: {1}",
    "log_merging_complete_bryt": "Zlúčenie kompletného panelu {0} s transformáciou: {1}",
    "log_skipped_merging_bryt": "Zlúčenie kompletného panelu pre {0} preskočené.",
    "log_file_result_saved": "Výsledný súbor uložený: {0}",
    "log_file_result_save_error": "Chyba ukladania výsledného súboru {0}: {1}",
    "log_finished_split_horizontal": "--- Dokončené: SPOLOČNÝ HÁROK – HORIZONTÁLNE ---",
    "log_no_slices_split_vertical": "Žiadne panely na spracovanie v split_vertical.",
    "log_start_split_vertical": "--- Štart: SPOLOČNÝ HÁROK – VERTIKÁLNE (otočenie v create_slice_reader) ---",
    "log_finished_split_vertical": "--- Dokončené: SPOLOČNÝ HÁROK – VERTIKÁLNE ---",
    "log_unknown_layout": "Neznáme rozloženie pre spoločný hárok: „{0}“.",
    "log_unknown_output_type": "Neznámy typ výstupu: „{0}“.",
    "log_finished_splitting_success": "--- Proces rezu dokončený pre: {0} – ÚSPECH ---",
    "log_finished_splitting_errors": "--- Proces rezu dokončený pre: {0} – VYSKYTLI SA CHYBY ---",
    "log_value_error_in_splitting": "Chyba vstupu alebo výpočtu: {0}",
    "log_finished_splitting_critical_error": "--- Proces rezu dokončený pre: {0} – KRITICKÁ CHYBA ---",
    "log_unexpected_error_in_splitting": "Neočakávaná chyba pri reze súboru {0}: {1}",

    #   Splitter – Testovací režim (__main__)
    "log_script_mode_test": "splitter.py spustený ako hlavný skript (testovací režim).",
    "log_loaded_config": "Konfigurácia načítaná.",
    "log_error_loading_config": "Zlyhalo načítanie konfigurácie: {0}",
    "log_created_example_pdf": "Vytvorený ukážkový PDF: {0}",
    "log_cannot_create_example_pdf": "Zlyhalo vytvorenie ukážkového PDF: {0}",
    "log_start_test_split": "Spúšťam testovací rez súboru: {0} do {1}",
    "log_test_split_success": "Testovací rez úspešne dokončený.",
    "log_test_split_errors": "Testovací rez dokončený s chybami.",

    # --- Logy – QR/čiarový kód (barcode_qr.py) ---
    "log_qr_empty_data": "Pokus o generovanie QR kódu pre prázdne dáta.",
    "log_qr_generated": "SVG QR kód vygenerovaný pre: {0}...",
    "log_qr_error": "Chyba generovania QR pre dáta „{0}“: {1}",
    "log_barcode_empty_data": "Pokus o generovanie čiarového kódu pre prázdne dáta.",
    "log_barcode_generated": "SVG čiarový kód vygenerovaný pre: {0}...",
    "log_barcode_error": "Chyba generovania čiarového kódu pre „{0}“: {1}",
    "log_basic_handler_configured": "Základný handler nastavený pre logger v barcode_qr.py",
    "log_basic_handler_error": "Chyba nastavenia základného handlera v barcode_qr: {0}",

    # --- Logy – Konfigurácia/Profily (main_config_manager.py) ---
    "loading_profiles_from": "Načítavam profily z",
    "profiles_file": "Súbor profilov",
    "does_not_contain_dict": "neobsahuje slovník. Vytvára sa nový",
    "not_found_creating_new": "nenašiel sa. Vytvára sa nový prázdny",
    "json_profiles_read_error": "Chyba čítania JSON súboru profilov",
    "file_will_be_overwritten": "Súbor bude pri ukladaní prepísaný",
    "json_decode_error_in_profiles": "Chyba dekódovania JSON v súbore profilov",
    "cannot_load_profiles_file": "Nedá sa načítať súbor profilov",
    "unexpected_profiles_read_error": "Neočakávaná chyba čítania profilov",
    "saving_profiles_to": "Ukladám profily do",
    "cannot_save_profiles_file": "Nedá sa uložiť súbor profilov",
    "profiles_save_error": "Chyba ukladania profilov do súboru",
    "logger_profile_saved": "Profil uložený: {profile}",
    "logger_profile_not_found": "Profil na načítanie sa nenašiel: {profile}",
    "logger_profile_loaded": "Profil načítaný: {profile}",
    "logger_profile_delete_not_exist": "Pokus o zmazanie neexistujúceho profilu: {profile}",
    "logger_profile_deleted": "Profil zmazaný: {profile}",
    "logger_start_save_settings": "Spustené ukladanie nastavení z GUI.",
    "logger_invalid_value": "Neplatná hodnota pre „{key}“. Nastavené na 0.0.",
    "logger_end_save_settings": "Ukladanie nastavení z GUI dokončené.",
    "logger_conversion_error": "Chyba konverzie hodnôt z GUI: {error}",
    "conversion_failed": "Konverzia hodnôt z GUI zlyhala",
    "logger_unexpected_save_error": "Neočakávaná chyba ukladania nastavení: {error}",
    "logger_settings_saved": "Nastavenia uložené do súboru: {file}",

    # --- Logy – Licencovanie (main_license.py) ---
    "public_key_load_error_log": "Chyba načítania verejného kľúča",
    "license_key_decode_error": "Chyba dekódovania licenčného kľúča",
    "license_activation_error": "Chyba aktivácie licencie",

    # --- Logy – Hlavný modul (main.py) ---
    "ui_created": "Používateľské rozhranie bolo vytvorené.",
    "error_tab_home": "Chyba vytvárania rozhrania „Domov“",
    "error_tab_settings": "Chyba vytvárania rozhrania „Nastavenia“",
    "error_tab_help": "Chyba vytvárania rozhrania „Pomoc“",
    "error_creating_license_ui": "Chyba vytvárania rozhrania „Licencia“",
    "error_loading_ui": "Všeobecná chyba načítania rozhrania: {error}",
    "error_creating_home_ui": "Chyba vytvárania rozhrania „Domov“",
    "error_creating_settings_ui": "Chyba vytvárania rozhrania „Nastavenia“",
    "error_creating_help_ui": "Chyba vytvárania rozhrania „Pomoc“",
    "logger_update_gui": "Spustená aktualizácia GUI z konfigurácie.",
    "logger_end_update_gui": "Aktualizácia GUI z konfigurácie dokončená.",
    "logger_update_gui_error": "Neočakávaná chyba aktualizácie GUI: {error}",
    "logger_invalid_output_dir": "Neplatný alebo neexistujúci výstupný priečinok: {directory}",
    "logger_invalid_input_file": "Neplatný alebo neexistujúci vstupný súbor: {file}",
    "logger_start_pdf": "Spustený proces generovania PDF.",
    "logger_pdf_save_error": "Generovanie PDF prerušené: zlyhalo uloženie aktuálnych nastavení.",
    "logger_pdf_success": "Generovanie PDF úspešne dokončené.",
    "logger_pdf_exception": "Výnimka v hlavnom procese generovania PDF.",
    "icon_set_error": "Zlyhanie nastavenia ikony aplikácie: {error}",
    "accent_button_style_error": "Zlyhanie nastavenia štýlu akcentného tlačidla: {error}",
    "logger_file_save_error": "Chyba ukladania súboru {file}: {error}",

    #   Logy – Náhľad (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Chyba generovania miniatúry",
    "output_preview_update_called": "Volaná aktualizácia náhľadu výstupu",
    "output_preview_canvas_missing": "Chýba plátno náhľadu výstupu",
    "pdf_found_in_output_dir": "PDF nájdené vo výstupnom priečinku",
    "preparing_thumbnail": "Pripravujem miniatúru",
    "thumbnail_generated_successfully": "Miniatúra úspešne vygenerovaná",
    "thumbnail_generation_error": "Chyba generovania miniatúry pre",
    "no_pdf_for_common_sheet": "Pre náhľad spoločného hárku nie je k dispozícii PDF",
    "no_pdf_for_separate_files": "Pre náhľad nie sú k dispozícii vygenerované PDF",
    "cannot_load_thumbnail": "Nedá sa načítať miniatúra z",

    #   Logy – Vývojár / interné GUI (main.py)
    "missing_gui_var_created": "Vytvorená chýbajúca GUI premenná pre kľúč: {key}",
    "missing_gui_structure_created": "Vytvorená chýbajúca GUI štruktúra pre: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Vytvorená chýbajúca GUI premenná pre: {code_type}/{output_type}/{layout}/{param}",

    # Ďalšie kľúče pre main_ui_help.py
    "help_text": """
    Billboard Splitter – Používateľská príručka\n\n
    Účel programu:\n
    Billboard Splitter slúži na automatické rozdelenie projektov billboardov na panely pripravené na tlač.
    Program je pripravený pracovať so súbormi v mierke 1:10.\n
    Hodnoty v sekciách: Presah, Biely pruh a Nastavenia sa zadávajú v mierke 1:1.
    Program umožňuje ukladať rozrezané panely do PDF podľa zvoleného rozloženia:\n
    • Spoločný hárok: všetky panely v jednom dokumente.\n
    • Samostatné súbory: každý panel sa uloží do samostatného PDF.\n\n
    Ďalej program umožňuje:\n
    • Zvoliť rozloženie – vertikálne alebo horizontálne (pri vertikálnom sú deliace čiary hore a dole,
      pri horizontálnom vľavo a vpravo).\n
    • Otočiť panely o 180° (inverzia celého projektu).\n
    • Pridať registračné značky (kríže alebo čiary) na presné polohovanie pri lepení.\n
    • Pridať QR kódy alebo čiarové kódy – generované zo vstupných dát na identifikáciu jednotlivých panelov.\n
    • Uložiť konfigurácie ako profily, ktoré možno načítať, upravovať a mazať – uľahčujú prepínanie medzi projektmi.\n\n
    Základný postup:\n\n
    1. Výber vstupného súboru:\n
    • Na karte „Domov“ vyberte PDF, JPG alebo TIFF s návrhom billboardu.\n
    • Ak nezadáte vlastnú cestu, použije sa predvolený ukážkový súbor.\n\n
    2. Nastavenia rezu:\n
    • Zadajte počet riadkov a stĺpcov, na ktoré sa projekt rozdelí.\n
    • Nastavte veľkosť presahu.\n
    • Voliteľne nastavte šírku bieleho pruhu, ktorý sa pripočíta k efektívnemu presahu.\n\n
    3. Výber rozloženia výstupu:\n
    • Vertikálne: panely budú rozložené vertikálne na PDF stránke.\n
    • Horizontálne: panely budú rozložené horizontálne.\n\n
    4. Typ výstupu:\n
    • Spoločný hárok – jeden PDF.\n
    • Samostatné súbory – jeden PDF na panel.\n
    • Na karte „Domov“ môžete povoliť a nastaviť registračné značky – kríž alebo čiaru.\n
    • Voliteľne povoľte QR alebo čiarový kód – vygeneruje sa z dát projektu.\n
    • Parametre kódu (mierka, posun, otočenie, poloha) doladíte na karte „Nastavenia“.\n\n
    5. Správa konfigurácií:\n
    • Na karte „Nastavenia“ detailne upravíte grafické parametre (okraje, hrúbky čiar, medzery) a nastavenia kódov.\n
    • Uložte aktuálnu konfiguráciu ako profil na neskoršie načítanie alebo úpravu.\n
    • Profily (súbor profiles.json) umožňujú rýchle prepínanie medzi sadami nastavení.\n\n
    6. Generovanie PDF:\n
    • Po nastavení všetkých parametrov kliknite na „Vygenerovať PDF“.\n
    • Výsledné súbory sa uložia do priečinka „output“ (alebo iného) a logy (s dennou rotáciou) do priečinka „logs“ (alebo iného).\n\n
    Ak sa vyskytnú problémy:\n
    • Skontrolujte logy v priečinku „logs“. Každý deň sa vytvára súbor logu s dátumom v názve.\n
    • Overte, že sú definované všetky požadované priečinky.\n
    • Technická podpora: tech@printworks.pl (pracovné dni, 8–16)\n
    """
}
