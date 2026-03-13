# lang_cs.py
"""
Soubor s překlady pro český jazyk.
"""

LANG = {
    "barcode_font_size_label": "Velikost písma popisu čárového kódu [pt]:",
    # ==========================
    #  Aplikace – Obecné
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Chyba",
    "no_file": "Žádný soubor",
    "language": "Jazyk",
    "language_switch": "Změna jazyka",
    "choose_language": "Vyberte jazyk:",
    "apply_language": "Použít",
    "language_changed": "Jazyk byl změněn. Některé změny budou viditelné až po restartu aplikace.",

    # ========================================
    #  Prvky uživatelského rozhraní (GUI)
    # ========================================

    # --- Hlavní karty ---
    "tab_home": " Domů ",
    "tab_settings": " Nastavení ",
    "tab_help": " Nápověda ",
    "tab_license": " Licence ",

    # --- Obecná tlačítka ---
    "button_browse": "Procházet...",
    "browse_folder": "Procházet složku...",
    "button_save": "Uložit",
    "button_delete": "Smazat",
    "button_close": "Zavřít",
    "save_all_settings": "Uložit veškeré nastavení",

    # --- Popisky polí (karta Domů) ---
    "label_rows": "Vertikální dělení (řádky):",
    "label_columns": "Horizontální dělení (sloupce):",
    "label_overlap": "Překrytí [mm]:",
    "label_white_stripe": "Bílý pruh [mm]:",
    "label_add_white_stripe": "Přidat bílý pruh k efektivnímu překrytí",
    "label_layout": "Rozložení výstupu:",
    "label_output_type": "Typ výstupu:",
    "label_enable_reg_marks": "Povolit registrační značky:",
    "label_enable_codes": "Povolit kódy:",
    "label_enable_sep_lines": "Povolit dělicí čáry (mezi panely)",
    "label_enable_start_line": "Povolit čáru začátku/horní okraj archu",
    "label_enable_end_line": "Povolit čáru konce/dolní okraj archu",
    "label_bryt_order": "Pořadí panelů:",
    "label_slice_rotation": "Rotace panelů:",
    "label_create_order_folder": "Vytvořit složku s číslem zakázky",

    # --- Sekce/skupiny (karta Domů) ---
    "section_input_file": " Vstupní soubor ",
    "section_scale_and_dimensions": " Měřítko a výstupní rozměry ",
    "label_original_size": "Původní velikost:",
    "label_scale_non_uniform": "Neproporcionální měřítko",
    "label_scale": "Měřítko: 1:",
    "label_scale_x": "Měřítko X: 1:",
    "label_scale_y": "Měřítko Y: 1:",
    "label_output_dimensions": "Výstupní rozměry souboru:",
    "label_width_cm": "Šířka [cm]:",
    "label_height_cm": "Výška [cm]:",
    "section_split_settings": " Nastavení řezu ",
    "section_profiles": " Profily nastavení ",
    "section_save_location": " Místo uložení ",
    "section_input_preview": " Náhled vstupního souboru ",
    "section_output_preview": " Náhled výstupu ",

    # --- Hodnoty voleb (combobox, radiobutton apod.) ---
    "layout_vertical": "Vertikální",
    "layout_horizontal": "Horizontální",
    "output_common_sheet": "Společný arch",
    "output_separate_files": "Samostatné soubory",
    "output_both": "Společný arch i samostatné soubory",
    "output_common": "Společný arch",
    "output_separate": "Samostatné soubory",
    "reg_mark_cross": "Kříž",
    "reg_mark_line": "Čára",
    "code_qr": "QR kód",
    "code_barcode": "Čárový kód",
    "bryt_order_1": "A1–An, B1–Bn, .. Standard, shora",
    "bryt_order_2": "A1–An, Bn–B1, .. Had po řádcích, shora",
    "bryt_order_3": "A1..B1, A2..B2, .. Po sloupcích, shora",
    "bryt_order_4": "A1–A2..B2–B1.. Had po sloupcích, shora",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Standard, zdola",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Had po řádcích, zdola",
    "logging_console": "konzole",
    "logging_file": "soubor",
    "logging_both": "oboje",

    # --- Sekce/skupiny (karta Nastavení) ---
    "section_processing_mode": " Režimy zpracování ",
    "processing_mode_ram": "RAM (v paměti)",
    "processing_mode_hdd": "Disk (na úložišti)",
    "graphic_settings": "Grafická nastavení",
    "code_settings": "Nastavení QR / čárového kódu",
    "logging_settings": "Nastavení logování",
    "barcode_text_position_label": "Pozice textu u kódu:",
    "barcode_text_bottom": "dole",
    "barcode_text_side": "na straně",
    "barcode_text_none": "žádný",

    # --- Popisky (Nastavení – Grafika) ---
    "extra_margin_label": "Okraj kolem panelů [mm]:",
    "margin_top_label": "Horní okraj [mm]:",
    "margin_bottom_label": "Dolní okraj [mm]:",
    "margin_left_label": "Levý okraj [mm]:",
    "margin_right_label": "Pravý okraj [mm]:",
    "reg_mark_width_label": "Registrační značka – šířka [mm]:",
    "reg_mark_height_label": "Registrační značka – výška [mm]:",
    "reg_mark_white_line_width_label": "Registrační značka – tloušťka bílé čáry [mm]:",
    "reg_mark_black_line_width_label": "Registrační značka – tloušťka černé čáry [mm]:",
    "sep_line_black_width_label": "Dělicí – tloušťka černé čáry [mm]:",
    "sep_line_white_width_label": "Dělicí – tloušťka bílé čáry [mm]:",
    "slice_gap_label": "Mezera mezi panely [mm]:",
    "label_draw_slice_border": "Kreslit rámeček kolem panelu (řezná linie)",

    # --- Popisky (Nastavení – Kódy) ---
    "scale_label": "Velikost [mm]:",
    "scale_x_label": "Šířka X [mm]:",
    "scale_y_label": "Výška Y [mm]:",
    "offset_x_label": "Posun X [mm]:",
    "offset_y_label": "Posun Y [mm]:",
    "rotation_label": "Rotace (°):",
    "anchor_label": "Roh:",

    # --- Popisky (Nastavení – Logy) ---
    "logging_mode_label": "Režim logování:",
    "log_file_label": "Soubor logu:",
    "logging_level_label": "Úroveň logování:",

    # --- Tlačítka / akce (karta Domů) ---
    "button_load": "Načíst",
    "button_save_settings": "Uložit aktuální nastavení",
    "button_generate_pdf": "Vygenerovat PDF",
    "button_refresh_preview": "Obnovit náhled",
    "button_refresh_layout": "Obnovit rozložení",

    # --- Licence (GUI) ---
    "hwid_frame_title": "Jedinečný identifikátor hardwaru (HWID)",
    "copy_hwid": "Kopírovat HWID",
    "license_frame_title": "Aktivace licence",
    "enter_license_key": "Zadejte licenční klíč:",
    "activate": "Aktivovat",
    "status_trial": "Zkušební režim",
    "license_active": "Licence je aktivní",

    # ================================================
    #  Zprávy pro uživatele (okna, stavový řádek)
    # ================================================

    # --- Profily ---
    "msg_no_profile_name": "Bez názvu",
    "msg_enter_profile_name": "Zadejte název profilu pro uložení.",
    "msg_profile_saved": "Profil uložen",
    "profile_saved_title": "Profil uložen",
    "msg_profile_saved_detail": "Profil „{0}“ byl uložen.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profil '{profile}' byl uložen a použit.",
    "msg_no_profile": "Žádný profil",
    "warning_no_profile": "Žádný profil",
    "msg_select_profile": "Vyberte v seznamu název profilu pro načtení.",
    "select_profile": "Vyberte v seznamu název profilu pro načtení.",
    "profile_loaded_title": "Profil načten",
    "profile_loaded": "Profil „{profile}“ byl načten.",
    "warning_no_profile_delete": "Žádný profil",
    "warning_no_profile_delete_message": "Vyberte v seznamu profil, který chcete smazat.",
    "profile_not_found": "Profil „{profile}“ nebyl nalezen.",
    "profile_not_exist": "Profil „{profile}“ neexistuje.",
    "confirm_delete_title": "Potvrďte smazání",
    "confirm_delete_profile": "Opravdu chcete smazat profil „{profile}“?",
    "profile_deleted_title": "Profil smazán",
    "profile_deleted": "Profil „{profile}“ byl smazán.",

    # --- Soubory / adresáře ---
    "msg_no_input_file": "Žádný vstupní soubor",
    "msg_unsupported_format": "Nepodporovaný formát",
    "select_file_title": "Vybrat vstupní soubor",
    "supported_files": "Podporované soubory",
    "all_files": "Všechny soubory",
    "select_dir_title": "Vybrat výstupní složku",
    "select_log_dir_title": "Vybrat složku pro logy",
    "error_output_dir_title": "Chyba výstupní složky",
    "error_output_dir": "Zadaná výstupní složka je neplatná nebo neexistuje:\n{directory}",
    "error_input_file_title": "Chyba vstupního souboru",
    "error_input_file": "Zadaný vstupní soubor je neplatný nebo neexistuje:\n{file}",
    "save_file_error_title": "Chyba ukládání souboru",
    "save_file_error": "Soubor se nepodařilo uložit: {error}",

    # --- Zpracování PDF / náhled ---
    "msg_pdf_processing_error": "Selhalo zpracování PDF souboru",
    "msg_thumbnail_error": "Chyba načítání miniatury",
    "msg_no_pdf_output": "Žádný PDF výstup",
    "no_pdf_pages": "PDF neobsahuje stránky",
    "unsupported_output": "Nepodporovaný typ výstupu pro náhled",
    "pdf_generated_title": "Generování dokončeno",
    "pdf_generated": "PDF soubor(y) byly úspěšně vygenerovány do složky:\n{directory}",
    "pdf_generation_error_title": "Chyba generování",
    "pdf_generation_error": "Při generování PDF došlo k chybám. Zkontrolujte logy.",
    "critical_pdf_error_title": "Kritická chyba generování PDF",
    "critical_pdf_error": "Došlo ke kritické chybě při generování PDF:\n{error}\nViz logy.",
    "settings_saved_title": "Nastavení uloženo",
    "settings_saved": "Nastavení bylo uloženo do souboru:\n{filepath}",
    "settings_save_error_title": "Chyba ukládání nastavení",
    "settings_save_error": "Nastavení se nepodařilo uložit: {error}",
    "conversion_error_title": "Chyba převodu",
    "conversion_error": "Chyba při převodu hodnot z rozhraní: {error}",
    "update_gui_error_title": "Chyba aktualizace rozhraní",
    "update_gui_error": "Došlo k chybě při aktualizaci rozhraní: {error}",

    # --- Licence ---
    "hwid_copied_to_clipboard": "HWID byl zkopírován do schránky",
    "computer_hwid": "HWID počítače",
    "public_key_load_error": "Chyba načtení veřejného klíče: {error}",
    "invalid_license_format": "Neplatný formát licenčního klíče: {error}",
    "activation_success": "Licence byla úspěšně aktivována.",
    "activation_error": "Chyba aktivace licence: {error}",
    "log_trial_mode_active": "Zkušební režim je aktivní",
    "log_trial_mode_inactive": "Zkušební režim není aktivní",

    # --- Inicializace ---
    "init_error_title": "Chyba inicializace",
    "init_error": "Chyba při inicializaci adresářů: {error}",
    "poppler_path_info": "Informace o cestě k Poppleru",
    "ttkthemes_not_installed": "Upozornění: knihovna ttkthemes není nainstalována. Použije se výchozí styl Tkinteru.",

    # =====================================
    #  Logy (zprávy loggeru)
    # =====================================

    # --- Obecné / Konfigurace ---
    "log_configured": "Logování nastaveno: úroveň={0}, režim={1}, soubor={2}",
    "log_no_handlers": "Upozornění: nejsou nastaveny žádné handlery logů (režim: {0}).",
    "log_critical_error": "Kritická chyba konfigurace logování: {0}",
    "log_basic_config": "Kvůli chybě bylo použito základní nastavení logování.",
    "log_dir_create_error": "Kritická chyba: nelze vytvořit složku logů {0}: {1}",

    # --- Logy – Inicializace / Adresáře (init_directories.py) ---
    "error_critical_init": "KRITICKÁ CHYBA během inicializace: {0}",
    "logger_init_error": "Chyba inicializace adresářů: {error}",
    "directory_created": "Vytvořena složka: {0}",
    "directory_creation_error": "Nelze vytvořit složku {0}: {1}",
    "sample_file_copied": "Ukázkový soubor zkopírován do {0}",
    "sample_file_copy_error": "Chyba kopírování ukázkového souboru: {0}",
    "log_created_output_dir": "Vytvořena výstupní složka: {0}",
    "log_cannot_create_output_dir": "Nelze vytvořit výstupní složku {0}: {1}",

    # --- Logy – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Chyba načtení grafických nastavení při inicializaci: {0}",
    "log_loading_pdf": "Načítám PDF soubor: {0}",
    "log_loading_bitmap": "Načítám rastrový soubor: {0}",
    "log_invalid_dpi": "Načteno neplatné DPI ({0}). Používám výchozí hodnotu {1} DPI.",
    "log_image_dimensions": "Rozměry obrázku: {0}×{1}px, režim: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Zpracování obrazu v původním barevném režimu: {0}",
    "log_unusual_color_mode": "Neobvyklý barevný režim: „{0}“. ReportLab/Pillow s ním nemusí pracovat správně.",
    "log_draw_image_error": "Chyba ReportLab drawImage pro režim {0}: {1}",
    "log_unsupported_format": "Nepodporovaný vstupní formát: {0}",
    "log_input_file_not_found": "Vstupní soubor nenalezen: {0}",
    "log_load_process_error": "Chyba načtení nebo zpracování souboru {0}: {1}",
    "log_input_file_not_exists": "Vstupní soubor neexistuje nebo je prázdná cesta: „{0}“",
    "log_cannot_load_or_empty_pdf": "Nelze načíst vstupní soubor, nebo je PDF prázdné/poškozené.",
    "log_pdf_dimensions_info": "  Rozměry PDF: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Neplatné rozměry stránky PDF: {0}×{1} pt.",

    #   Splitter – Výpočty rozměrů
    "log_extra_margin": "Dodatečný okraj nastaven na {0:.3f} pt",
    "log_invalid_rows_cols": "Neplatný počet řádků ({0}) nebo sloupců ({1}).",
    "error_invalid_rows_cols": "Řádky a sloupce musí být kladná celá čísla.",
    "log_invalid_overlap_white_stripe": "Neplatné hodnoty překrytí ({0}) nebo bílého pruhu ({1}). Musí být číselné.",
    "error_invalid_overlap_white_stripe": "Překrytí a bílý pruh musí být číselné hodnoty (mm).",
    "log_stripe_usage": "Nastaveno use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Základní překrytí (grafika): {0:.3f} mm, bílý pruh: {1:.3f} mm, efektivní překrytí: {2:.3f} mm",
    "log_computed_dimensions": "Vypočteno: PDF {0:.3f}×{1:.3f} mm. Panel: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Jádro: {6:.3f}×{7:.3f} pt. Efektivní překrytí: {8:.3f} mm",
    "log_invalid_dimensions": "Neplatné rozměry panelu ({0:.3f}×{1:.3f}) nebo jádra ({2:.3f}×{3:.3f}) pro per={4}, stripe={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Vypočtené rozměry panelu/jádra jsou neplatné nebo záporné.",

    #   Splitter – Generování informací a pořadí panelů
    "log_generating_slice_info": "Generuji informace o panelu: {0}",
    "log_no_slices_info_generated": "Nepodařilo se vygenerovat informace o panelech.",
    "log_applying_rotated_order": "Aplikuji pořadí pro rotaci o 180°: {0}",
    "log_applying_standard_order": "Aplikuji pořadí pro 0° (standard): {0}",
    "log_unknown_bryt_order": "Neznámé pořadí panelů: „{0}“. Použito výchozí.",
    "log_final_slices_order": "  Konečné pořadí panelů ({0}): [{1}]",

    #   Splitter – Tvorba překryvů (overlays) a slučování
    "log_invalid_dimensions_overlay": "Pokus o vytvoření overlay s neplatnými rozměry: {0}. Přeskakuji.",
    "log_empty_overlay": "Vytvořen prázdný nebo téměř prázdný overlay PDF. Slučování přeskočeno.",
    "log_overlay_error": "Chyba při vytváření overlay PDF: {0}",
    "log_merge_error": "Pokus o sloučení overlay bez stránek. Přeskakuji.",
    "log_merge_page_error": "Chyba slučování overlay PDF: {0}",
    "log_fallback_draw_rotating_elements": "Nepodařilo se získat řádky/sloupce pro _draw_rotating_elements, použito 1×1.",
    "log_overlay_created_for_slice": "Overlay pruhů/znaků vytvořen pro panel {0}",
    "log_overlay_creation_failed_for_slice": "Overlay pro {0} se nepodařilo vytvořit",
    "log_merging_rotated_overlay": "Sloučení OTOČENÉHO overlay pro {0} s T={1}",
    "log_merging_nonrotated_overlay": "Sloučení NEOTOČENÉHO overlay pro {0}",
    "log_merging_all_codes_overlay": "Sloučení overlay všech kódů (bez rotace)",
    "log_merging_separation_lines_overlay": "Sloučení overlay dělicích čar (bez rotace)",
    "log_merging_code_overlay_for_slice": "Overlay kódu pro {0} sloučen bez rotace.",
    "log_merging_separation_overlay_for_slice": "Overlay dělicích čar pro {0} sloučen bez rotace.",

    #   Splitter – Kreslení grafických prvků (pruhy, značky, čáry)
    "log_drawing_top_stripe": "[Canvas Draw] Kreslím horní pruh pro {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas Draw] Kreslím pravý pruh pro {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas Draw] Vyplňuji a orámuji roh pro {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Kreslím kříž se středem v ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Kreslím registrační čáry pro {0} v oblasti od ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Kreslím pravou vertikální čáru: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Kreslím horní horizontální čáru: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Kreslím dělicí čáru (bílá přes černou): ({0}) @ ({1:.3f}, {2:.3f}), délka={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Kreslím kříže pro {0} [{1},{2}] / [{3},{4}] v oblasti od ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Vypočtené středy: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Kreslím TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Kreslím TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Kreslím BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Kreslím BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Značka {0} vynechána podle pravidla pro pozici [{1},{2}]",
    "log_trial_common_sheet": "Aplikuji vodoznak TRIAL na společném archu",

    # Vodoznak
    "log_trial_watermark_added": "Byl přidán vodoznak TRIAL",
    "error_drawing_trial_text": "Chyba při kreslení vodoznaku: {error}",

    #   Splitter – Dělicí čáry (celá stránka)
    "log_drawing_separation_lines_for_page": "Kreslím dělicí čáry pro stránku (rozložení={0}, počet panelů={1}, index panelu={2})",
    "log_vertical_line_between_slices": "  Vertikální čára mezi panely {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Začátek vertikální čáry @ x={0:.1f}",
    "log_vertical_line_end": "  Konec vertikální čáry @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Horizontální čára mezi panely {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Začátek horizontální čáry @ y={0:.1f}",
    "log_horizontal_line_end": "  Konec horizontální čáry @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Samostatné_soubory) Začátek vert./horiz. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Samostatné_soubory) Konec vert./horiz. @ {0:.1f}",

    #   Splitter – Generování kódů / QR
    "log_generate_barcode_data": "Generuji data pro kód: {0}",
    "log_barcode_data_shortened": "Data kódu zkrácena na {0} znaků.",
    "log_barcode_data_error": "Chyba při generování dat kódu: {0}",
    "log_compose_barcode_payload": "Sestavuji payload kódu ({0}): {1}",
    "log_barcode_payload_shortened": "Payload zkrácen na {0} znaků pro formát {1}",
    "log_barcode_payload_error": "Chyba při sestavení payloadu: {0}",
    "log_unknown_anchor_fallback": "Neznámý kotevní roh „{0}“, použit levý spodní",
    "log_used_default_code_settings": "Použito nastavení „default“ pro kód {0}/{1}.",
    "log_no_layout_key_fallback": "Pro {1}/{2} neexistuje rozložení „{0}“. Použito první dostupné: „{3}“.",
    "log_code_settings_error": "Nebylo nalezeno / chyba načtení nastavení kódu ({0}/{1}/{2}): {3}. Použity výchozí hodnoty.",
    "log_drawing_barcode": "Kreslím {0} na ({1:.3f}, {2:.3f}) [základ ({3:.3f}, {4:.3f}) + posun ({5:.3f}, {6:.3f})], rotace: {7}°",
    "error_generate_qr_svg": "Selhalo generování SVG QR kódu.",
    "error_invalid_scale_for_qr": "Neplatná velikost QR: {0} mm",
    "error_invalid_qr_scale_factor": "Neplatný měřítkový faktor QR: {0}",
    "error_generate_barcode_svg": "Selhalo generování SVG čárového kódu.",
    "error_invalid_scale_for_barcode": "Neplatná velikost čárového kódu: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Neplatný měřítkový faktor čárového kódu: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: velikost v konfiguraci={1:.3f} mm, šířka SVG={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: velikost v konfiguraci=({1:.3f} mm, {2:.3f} mm), rozměr SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Chyba kreslení kódu „{0}“: {1}",
    "log_prepared_barcode_info": "Připraveny informace o kódu pro {0} ({1}, kotva={2}): základní absolutní pozice ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Chyba přípravy dat kódu pro {0}: {1}",
    "log_drawing_barcodes_count": "Kreslím {0} kódů/QR…",
    "log_missing_barcode_info_key": "Chybí klíč v informaci o kódu při kreslení: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Chyba kreslení kódu „{0}“ v _draw_all_barcodes: {1}",

    #   Splitter – Proces řezu (metody split_*)
    "log_start_splitting_process": "--- Spouštím proces řezu pro: {0} ---",
    "log_split_settings": "  Nastavení: {0}×{1} panelů, překrytí={2} mm, bílý pruh={3} mm (+překrytí: {4})",
    "log_output_dir_info": "  Výstup: {0} / {1} do „{2}“",
    "log_lines_marks_barcodes_info": "  Čáry: dělicí={0}, start={1}, konec={2} | Značky: {3} ({4}), Kódy: {5} ({6})",
    "log_bryt_order_info": "  Pořadí: {0}, rotace panelů: {1}°",
    "log_invalid_dimensions_in_slice_info": "Neplatné rozměry v slice_info pro {0}: {1}×{2}",
    "log_content_transform": "Transformace obsahu T_content pro {0}: {1}",
    "log_merged_content_for_slice": "Obsah spojen pro panel {0} do new_page",
    "log_slice_reader_created": "Kompletní panel (PdfReader) vytvořen pro {0}",
    "log_slice_reader_creation_error": "Chyba vytvoření kompletního panelu pro {0}: {1}",
    "log_used_get_transform": "Použit _get_transform (jen posun): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Start: SAMOSTATNÉ SOUBORY (rotace v create_slice_reader) ---",
    "log_creating_file_for_slice": "Vytvářím soubor pro panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Neplatná velikost stránky ({0}×{1}) pro {2}. Přeskakuji.",
    "log_blank_page_creation_error": "Chyba vytvoření stránky pro {0} (rozměr {1}×{2}): {3}. Přeskakuji.",
    "log_transform_for_slice": "Transformace T (jen posun) pro {0}: {1}",
    "log_merging_complete_slice": "Sloučení kompletního panelu {0} s transformací: {1}",
    "log_skipped_slice_merging": "Sloučení kompletního panelu pro {0} přeskočeno.",
    "log_file_saved": "Soubor uložen: {0}",
    "log_file_save_error": "Chyba ukládání souboru {0}: {1}",
    "log_finished_split_separate_files": "--- Dokončeno: SAMOSTATNÉ SOUBORY (uloženo {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Žádné panely ke zpracování ve split_horizontal.",
    "log_start_split_horizontal": "--- Start: SPOLEČNÝ ARCH – HORIZONTÁLNÍ (rotace v create_slice_reader) ---",
    "log_page_dimensions": "Rozměry stránky: {0:.1f}×{1:.1f} mm ({2} panelů)",
    "log_page_creation_error": "Chyba vytvoření výstupní stránky ({0}×{1}): {2}. Přerušuji.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformace T (jen posun) pro {0}: {1}",
    "log_merging_complete_bryt": "Sloučení kompletního panelu {0} s transformací: {1}",
    "log_skipped_merging_bryt": "Sloučení kompletního panelu pro {0} přeskočeno.",
    "log_file_result_saved": "Výsledný soubor uložen: {0}",
    "log_file_result_save_error": "Chyba ukládání výsledného souboru {0}: {1}",
    "log_finished_split_horizontal": "--- Dokončeno: SPOLEČNÝ ARCH – HORIZONTÁLNÍ ---",
    "log_no_slices_split_vertical": "Žádné panely ke zpracování ve split_vertical.",
    "log_start_split_vertical": "--- Start: SPOLEČNÝ ARCH – VERTIKÁLNÍ (rotace v create_slice_reader) ---",
    "log_finished_split_vertical": "--- Dokončeno: SPOLEČNÝ ARCH – VERTIKÁLNÍ ---",
    "log_unknown_layout": "Neznámé rozložení pro společný arch: „{0}“.",
    "log_unknown_output_type": "Neznámý typ výstupu: „{0}“.",
    "log_finished_splitting_success": "--- Proces řezu dokončen pro: {0} – ÚSPĚCH ---",
    "log_finished_splitting_errors": "--- Proces řezu dokončen pro: {0} – DOŠLO K CHYBÁM ---",
    "log_value_error_in_splitting": "Chyba vstupu nebo výpočtu: {0}",
    "log_finished_splitting_critical_error": "--- Proces řezu dokončen pro: {0} – KRITICKÁ CHYBA ---",
    "log_unexpected_error_in_splitting": "Neočekávaná chyba při řezu souboru {0}: {1}",

    #   Splitter – Testovací režim (__main__)
    "log_script_mode_test": "splitter.py spuštěn jako hlavní skript (testovací režim).",
    "log_loaded_config": "Konfigurace načtena.",
    "log_error_loading_config": "Selhalo načtení konfigurace: {0}",
    "log_created_example_pdf": "Vytvořen ukázkový PDF: {0}",
    "log_cannot_create_example_pdf": "Selhalo vytvoření ukázkového PDF: {0}",
    "log_start_test_split": "Spouštím testovací řez souboru: {0} do {1}",
    "log_test_split_success": "Testovací řez úspěšně dokončen.",
    "log_test_split_errors": "Testovací řez dokončen s chybami.",

    # --- Logy – QR/čárový kód (barcode_qr.py) ---
    "log_qr_empty_data": "Pokus o generování QR kódu pro prázdná data.",
    "log_qr_generated": "SVG QR kód vygenerován pro: {0}...",
    "log_qr_error": "Chyba generování QR pro data „{0}“: {1}",
    "log_barcode_empty_data": "Pokus o generování čárového kódu pro prázdná data.",
    "log_barcode_generated": "SVG čárový kód vygenerován pro: {0}...",
    "log_barcode_error": "Chyba generování čárového kódu pro „{0}“: {1}",
    "log_basic_handler_configured": "Základní handler nastaven pro logger v barcode_qr.py",
    "log_basic_handler_error": "Chyba nastavení základního handleru v barcode_qr: {0}",

    # --- Logy – Konfigurace/Profily (main_config_manager.py) ---
    "loading_profiles_from": "Načítám profily z",
    "profiles_file": "Soubor profilů",
    "does_not_contain_dict": "neobsahuje slovník. Vytvářím nový",
    "not_found_creating_new": "nenalezen. Vytvářím nový prázdný",
    "json_profiles_read_error": "Chyba čtení JSON souboru profilů",
    "file_will_be_overwritten": "Soubor bude při ukládání přepsán",
    "json_decode_error_in_profiles": "Chyba dekódování JSON v souboru profilů",
    "cannot_load_profiles_file": "Nelze načíst soubor profilů",
    "unexpected_profiles_read_error": "Neočekávaná chyba čtení profilů",
    "saving_profiles_to": "Ukládám profily do",
    "cannot_save_profiles_file": "Nelze uložit soubor profilů",
    "profiles_save_error": "Chyba ukládání profilů do souboru",
    "logger_profile_saved": "Profil uložen: {profile}",
    "logger_profile_not_found": "Profil pro načtení nenalezen: {profile}",
    "logger_profile_loaded": "Profil načten: {profile}",
    "logger_profile_delete_not_exist": "Pokus o smazání neexistujícího profilu: {profile}",
    "logger_profile_deleted": "Profil smazán: {profile}",
    "logger_start_save_settings": "Zahájeno ukládání nastavení z GUI.",
    "logger_invalid_value": "Neplatná hodnota pro „{key}“. Nastavena na 0.0.",
    "logger_end_save_settings": "Ukládání nastavení z GUI dokončeno.",
    "logger_conversion_error": "Chyba převodu hodnot z GUI: {error}",
    "conversion_failed": "Převod hodnot z GUI selhal",
    "logger_unexpected_save_error": "Neočekávaná chyba ukládání nastavení: {error}",
    "logger_settings_saved": "Nastavení uloženo do souboru: {file}",

    # --- Logy – Licencování (main_license.py) ---
    "public_key_load_error_log": "Chyba načtení veřejného klíče",
    "license_key_decode_error": "Chyba dekódování licenčního klíče",
    "license_activation_error": "Chyba aktivace licence",

    # --- Logy – Hlavní modul (main.py) ---
    "ui_created": "Uživatelské rozhraní bylo vytvořeno.",
    "error_tab_home": "Chyba při vytváření rozhraní „Domů“",
    "error_tab_settings": "Chyba při vytváření rozhraní „Nastavení“",
    "error_tab_help": "Chyba při vytváření rozhraní „Nápověda“",
    "error_creating_license_ui": "Chyba při vytváření rozhraní „Licence“",
    "error_loading_ui": "Obecná chyba načítání rozhraní: {error}",
    "error_creating_home_ui": "Chyba při vytváření rozhraní „Domů“",
    "error_creating_settings_ui": "Chyba při vytváření rozhraní „Nastavení“",
    "error_creating_help_ui": "Chyba při vytváření rozhraní „Nápověda“",
    "logger_update_gui": "Zahájeno aktualizování GUI z konfigurace.",
    "logger_end_update_gui": "Aktualizace GUI z konfigurace dokončena.",
    "logger_update_gui_error": "Neočekávaná chyba při aktualizaci GUI: {error}",
    "logger_invalid_output_dir": "Neplatná nebo neexistující výstupní složka: {directory}",
    "logger_invalid_input_file": "Neplatný nebo neexistující vstupní soubor: {file}",
    "logger_start_pdf": "Zahájen proces generování PDF.",
    "logger_pdf_save_error": "Generování PDF zrušeno: nepodařilo se uložit aktuální nastavení.",
    "logger_pdf_success": "Generování PDF úspěšně dokončeno.",
    "logger_pdf_exception": "Výjimka v hlavním procesu generování PDF.",
    "icon_set_error": "Chyba při nastavování ikony aplikace: {error}",
    "accent_button_style_error": "Chyba při nastavování stylu akcentního tlačítka: {error}",
    "logger_file_save_error": "Chyba ukládání souboru {file}: {error}",

    #   Logy – Náhled (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Chyba generování miniatury",
    "output_preview_update_called": "Volána aktualizace náhledu výstupu",
    "output_preview_canvas_missing": "Chybí plátno náhledu výstupu",
    "pdf_found_in_output_dir": "PDF nalezeno ve výstupní složce",
    "preparing_thumbnail": "Připravuji miniaturu",
    "thumbnail_generated_successfully": "Miniatura úspěšně vygenerována",
    "thumbnail_generation_error": "Chyba generování miniatury pro",
    "no_pdf_for_common_sheet": "Pro náhled společného archu není k dispozici PDF",
    "no_pdf_for_separate_files": "Pro náhled nejsou k dispozici vygenerované PDF",
    "cannot_load_thumbnail": "Nelze načíst miniaturu z",

    #   Logy – Vývojář / interní GUI (main.py)
    "missing_gui_var_created": "Vytvořena chybějící GUI proměnná pro klíč: {key}",
    "missing_gui_structure_created": "Vytvořena chybějící GUI struktura pro: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Vytvořena chybějící GUI proměnná pro: {code_type}/{output_type}/{layout}/{param}",

    # Další klíče pro main_ui_help.py
    "help_text": """
    Billboard Splitter – Uživatelská příručka\n\n
    Účel programu:\n
    Billboard Splitter slouží k automatickému rozdělení projektů billboardů na panely připravené k tisku.
    Program je připraven pracovat se soubory v měřítku 1:10.\n
    Hodnoty v sekcích: Překrytí, Bílý pruh a Nastavení se zadávají v měřítku 1:1.
    Program umožňuje skládat vyřezané panely do PDF dle zvoleného rozložení:\n
    • Společný arch: všechny panely v jednom dokumentu.\n
    • Samostatné soubory: každý panel se ukládá do samostatného PDF.\n\n
    Dále program umožňuje:\n
    • Volit rozložení – vertikální či horizontální (u vertikálního jsou dělicí čáry nahoře a dole,
      u horizontálního vlevo a vpravo).\n
    • Otočit panely o 180° (invertovat celý projekt).\n
    • Přidat registrační značky (křížky nebo čáry) pro přesné polohování při lepení.\n
    • Přidat QR kódy nebo čárové kódy – generované ze vstupních dat pro identifikaci jednotlivých panelů.\n
    • Ukládat konfigurace jako profily, které lze načítat, upravovat a mazat – snadný přepínatel mezi projekty.\n\n
    Základní postup:\n\n
    1. Výběr vstupního souboru:\n
    • Na kartě „Domů“ zvolte PDF, JPG nebo TIFF s návrhem billboardu.\n
    • Pokud nezadáte vlastní cestu, program použije výchozí ukázkový soubor.\n\n
    2. Nastavení řezu:\n
    • Uveďte počet řádků a sloupců, na které se projekt rozdělí.\n
    • Nastavte velikost překrytí.\n
    • Volitelně nastavte šířku bílého pruhu, který se přičte k efektivnímu překrytí.\n\n
    3. Volba rozložení výstupu:\n
    • Vertikální: panely budou skládané vertikálně na PDF stránce.\n
    • Horizontální: panely budou skládané horizontálně.\n\n
    4. Typ výstupu:\n
    • Společný arch – jeden PDF.\n
    • Samostatné soubory – jeden PDF na panel.\n
    • Na kartě „Domů“ můžete zapnout a nastavit registrační značky – kříž nebo čáru.\n
    • Volitelně zapněte QR nebo čárový kód – vygeneruje se z dat projektu.\n
    • Parametry kódu (měřítko, posun, rotace, poloha) doladíte na kartě „Nastavení“.\n\n
    5. Správa konfigurací:\n
    • Na kartě „Nastavení“ lze detailně upravit grafické parametry (okraje, tloušťky čar, mezery) a nastavení kódů.\n
    • Uložte aktuální konfiguraci jako profil pro pozdější načtení či úpravu.\n
    • Profily (soubor profiles.json) umožňují rychlé přepínání mezi různými sadami nastavení.\n\n
    6. Generování PDF:\n
    • Po nastavení všech parametrů klikněte na „Vygenerovat PDF“.\n
    • Výsledné soubory se uloží do složky „output“ (nebo jiné) a logy (s denní rotací) do složky „logs“ (nebo jiné).\n\n
    Pokud nastanou problémy:\n
    • Zkontrolujte logy ve složce „logs“. Každý den se vytváří soubor logu s datem v názvu.\n
    • Ověřte, že jsou definovány všechny požadované složky.\n
    • Technická podpora: tech@printworks.pl (pracovní dny, 8–16)\n
    """
}
