# lang_hu.py
"""
Fordítási fájl magyar nyelvhez.
"""

LANG = {
    "barcode_font_size_label": "Vonalkód leírás betűmérete [pt]:",
    # ==========================
    #  Alkalmazás – Általános
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Hiba",
    "no_file": "Nincs fájl",
    "language": "Nyelv",
    "language_switch": "Nyelvváltás",
    "choose_language": "Válasszon nyelvet:",
    "apply_language": "Alkalmaz",
    "language_changed": "A nyelv megváltozott. Néhány módosítás csak az alkalmazás újraindítása után látható.",

    # ========================================
    #  Grafikus felület (GUI)
    # ========================================

    # --- Fő fülek ---
    "tab_home": " Kezdőlap ",
    "tab_settings": " Beállítások ",
    "tab_help": " Súgó ",
    "tab_license": " Licenc ",

    # --- Általános gombok ---
    "button_browse": "Tallózás...",
    "browse_folder": "Mappa tallózása...",
    "button_save": "Mentés",
    "button_delete": "Törlés",
    "button_close": "Bezárás",
    "save_all_settings": "Összes beállítás mentése",

    # --- Mezőcímkék (Kezdőlap) ---
    "label_rows": "Függőleges osztás (sorok):",
    "label_columns": "Vízszintes osztás (oszlopok):",
    "label_overlap": "Átfedés [mm]:",
    "label_white_stripe": "Fehér sáv [mm]:",
    "label_add_white_stripe": "Fehér sáv hozzáadása a tényleges átfedéshez",
    "label_layout": "Kimeneti elrendezés:",
    "label_output_type": "Kimenet típusa:",
    "label_enable_reg_marks": "Illesztőjelek engedélyezése:",
    "label_enable_codes": "Kódok engedélyezése:",
    "label_enable_sep_lines": "Elválasztóvonalak engedélyezése (panelek között)",
    "label_enable_start_line": "Kezdő/felső lapszél vonal engedélyezése",
    "label_enable_end_line": "Záró/alsó lapszél vonal engedélyezése",
    "label_bryt_order": "Panelek sorrendje:",
    "label_slice_rotation": "Panelek forgatása:",
    "label_create_order_folder": "Rendelésszám szerinti mappa létrehozása",

    # --- Szakaszok (Kezdőlap) ---
    "section_input_file": " Bemeneti fájl ",
    "section_scale_and_dimensions": " Méretarány és kimeneti méretek ",
    "label_original_size": "Eredeti méret:",
    "label_scale_non_uniform": "Aránytalan méretezés",
    "label_scale": "Méretarány: 1:",
    "label_scale_x": "Méretarány X: 1:",
    "label_scale_y": "Méretarány Y: 1:",
    "label_output_dimensions": "Kimeneti fájl méretei:",
    "label_width_cm": "Szélesség [cm]:",
    "label_height_cm": "Magasság [cm]:",
    "section_split_settings": " Vágási beállítások ",
    "section_profiles": " Beállítási profilok ",
    "section_save_location": " Mentés helye ",
    "section_input_preview": " Bemenet előnézete ",
    "section_output_preview": " Kimenet előnézete ",

    # --- Opcióértékek ---
    "layout_vertical": "Függőleges",
    "layout_horizontal": "Vízszintes",
    "output_common_sheet": "Közös ív",
    "output_separate_files": "Külön fájlok",
    "output_both": "Közös ív és külön fájlok",
    "output_common": "Közös ív",
    "output_separate": "Külön fájlok",
    "reg_mark_cross": "Kereszt",
    "reg_mark_line": "Vonal",
    "code_qr": "QR-kód",
    "code_barcode": "Vonalkód",
    "bryt_order_1": "A1–An, B1–Bn, .. Standard, felülről",
    "bryt_order_2": "A1–An, Bn–B1, .. Kígyózó soronként, felülről",
    "bryt_order_3": "A1..B1, A2..B2, .. Oszloponként, felülről",
    "bryt_order_4": "A1–A2..B2–B1.. Kígyózó oszloponként, felülről",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Standard, alulról",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Kígyózó soronként, alulról",
    "logging_console": "konzol",
    "logging_file": "fájl",
    "logging_both": "mindkettő",

    # --- Szakaszok (Beállítások) ---
    "section_processing_mode": " Feldolgozási módok ",
    "processing_mode_ram": "RAM (memóriában)",
    "processing_mode_hdd": "Lemez (tárhely)",
    "graphic_settings": "Grafikai beállítások",
    "code_settings": "QR/vonalkód beállítások",
    "logging_settings": "Naplózás beállításai",
    "barcode_text_position_label": "Szöveg pozíciója a kód mellett:",
    "barcode_text_bottom": "alul",
    "barcode_text_side": "oldalt",
    "barcode_text_none": "nincs",

    # --- Címkék (Beállítások – Grafika) ---
    "extra_margin_label": "Margó a panelek körül [mm]:",
    "margin_top_label": "Felső margó [mm]:",
    "margin_bottom_label": "Alsó margó [mm]:",
    "margin_left_label": "Bal margó [mm]:",
    "margin_right_label": "Jobb margó [mm]:",
    "reg_mark_width_label": "Illesztőjel – szélesség [mm]:",
    "reg_mark_height_label": "Illesztőjel – magasság [mm]:",
    "reg_mark_white_line_width_label": "Illesztőjel – fehér vonal vastagsága [mm]:",
    "reg_mark_black_line_width_label": "Illesztőjel – fekete vonal vastagsága [mm]:",
    "sep_line_black_width_label": "Elválasztó – fekete vonal vastagsága [mm]:",
    "sep_line_white_width_label": "Elválasztó – fehér vonal vastagsága [mm]:",
    "slice_gap_label": "Hézag a panelek között [mm]:",
    "label_draw_slice_border": "Szegély rajzolása a panel köré (vágóvonal)",

    # --- Címkék (Beállítások – Kódok) ---
    "scale_label": "Méret [mm]:",
    "scale_x_label": "X szélesség [mm]:",
    "scale_y_label": "Y magasság [mm]:",
    "offset_x_label": "X eltolás [mm]:",
    "offset_y_label": "Y eltolás [mm]:",
    "rotation_label": "Forgatás (°):",
    "anchor_label": "Sarok:",

    # --- Címkék (Beállítások – Logok) ---
    "logging_mode_label": "Naplózási mód:",
    "log_file_label": "Naplófájl:",
    "logging_level_label": "Naplózási szint:",

    # --- Gombok / műveletek (Kezdőlap) ---
    "button_load": "Betöltés",
    "button_save_settings": "Aktuális beállítások mentése",
    "button_generate_pdf": "PDF generálása",
    "button_refresh_preview": "Előnézet frissítése",
    "button_refresh_layout": "Elrendezés frissítése",

    # --- Licenc (GUI) ---
    "hwid_frame_title": "Egyedi hardverazonosító (HWID)",
    "copy_hwid": "HWID másolása",
    "license_frame_title": "Licenc aktiválása",
    "enter_license_key": "Adja meg a licenckulcsot:",
    "activate": "Aktiválás",
    "status_trial": "Próbaverzió",
    "license_active": "A licenc aktív",

    # ================================================
    #  Üzenetek a felhasználónak (párbeszédek, státusz)
    # ================================================

    # --- Profilok ---
    "msg_no_profile_name": "Nincs név",
    "msg_enter_profile_name": "Adjon meg profilnevet a mentéshez.",
    "msg_profile_saved": "Profil mentve",
    "profile_saved_title": "Profil mentve",
    "msg_profile_saved_detail": "A(z) „{0}” profil elmentve.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "A(z) '{profile}' profil mentve és alkalmazva.",
    "msg_no_profile": "Nincs profil",
    "warning_no_profile": "Nincs profil",
    "msg_select_profile": "Válasszon ki egy profilt a listából betöltéshez.",
    "select_profile": "Válasszon ki egy profilt a listából betöltéshez.",
    "profile_loaded_title": "Profil betöltve",
    "profile_loaded": "A(z) „{profile}” profil betöltve.",
    "warning_no_profile_delete": "Nincs profil",
    "warning_no_profile_delete_message": "Válasszon ki egy profilt a törléshez.",
    "profile_not_found": "A(z) „{profile}” profil nem található.",
    "profile_not_exist": "A(z) „{profile}” profil nem létezik.",
    "confirm_delete_title": "Törlés megerősítése",
    "confirm_delete_profile": "Biztosan törli a(z) „{profile}” profilt?",
    "profile_deleted_title": "Profil törölve",
    "profile_deleted": "A(z) „{profile}” profil törölve.",

    # --- Fájlok / könyvtárak ---
    "msg_no_input_file": "Nincs bemeneti fájl",
    "msg_unsupported_format": "Nem támogatott formátum",
    "select_file_title": "Bemeneti fájl kiválasztása",
    "supported_files": "Támogatott fájlok",
    "all_files": "Összes fájl",
    "select_dir_title": "Kimeneti mappa kiválasztása",
    "select_log_dir_title": "Naplómappa kiválasztása",
    "error_output_dir_title": "Kimeneti mappa hiba",
    "error_output_dir": "A megadott kimeneti mappa érvénytelen vagy nem létezik:\n{directory}",
    "error_input_file_title": "Bemeneti fájl hiba",
    "error_input_file": "A megadott bemeneti fájl érvénytelen vagy nem létezik:\n{file}",
    "save_file_error_title": "Fájlmentési hiba",
    "save_file_error": "A fájl nem menthető: {error}",

    # --- PDF feldolgozás / előnézet ---
    "msg_pdf_processing_error": "A PDF fájl feldolgozása sikertelen",
    "msg_thumbnail_error": "Hiba a bélyegkép betöltésekor",
    "msg_no_pdf_output": "Nincs PDF kimenet",
    "no_pdf_pages": "A PDF nem tartalmaz oldalakat",
    "unsupported_output": "Az előnézethez nem támogatott kimenettípus",
    "pdf_generated_title": "Generálás befejeződött",
    "pdf_generated": "A PDF fájl(ok) sikeresen létrehozva itt:\n{directory}",
    "pdf_generation_error_title": "Generálási hiba",
    "pdf_generation_error": "Hibák történtek a PDF generálása közben. Ellenőrizze a naplókat.",
    "critical_pdf_error_title": "Kritikus hiba a PDF generálásában",
    "critical_pdf_error": "Kritikus hiba történt a PDF generálásakor:\n{error}\nLásd a naplókat.",
    "settings_saved_title": "Beállítások mentve",
    "settings_saved": "A beállítások elmentve a fájlba:\n{filepath}",
    "settings_save_error_title": "Beállításmentési hiba",
    "settings_save_error": "A beállítások nem menthetők: {error}",
    "conversion_error_title": "Konverziós hiba",
    "conversion_error": "Hiba a felület értékeinek konvertálásakor: {error}",
    "update_gui_error_title": "Felületfrissítési hiba",
    "update_gui_error": "Hiba történt a felület frissítése közben: {error}",

    # --- Licenc ---
    "hwid_copied_to_clipboard": "A HWID a vágólapra másolva",
    "computer_hwid": "Számítógép HWID",
    "public_key_load_error": "Nyilvános kulcs betöltési hiba: {error}",
    "invalid_license_format": "Érvénytelen licenckulcs formátum: {error}",
    "activation_success": "A licenc sikeresen aktiválva.",
    "activation_error": "Licencaktiválási hiba: {error}",
    "log_trial_mode_active": "A próbaverzió aktív",
    "log_trial_mode_inactive": "A próbaverzió nem aktív",

    # --- Inicializálás ---
    "init_error_title": "Inicializálási hiba",
    "init_error": "Hiba a könyvtárak inicializálásakor: {error}",
    "poppler_path_info": "Poppler elérési út információ",
    "ttkthemes_not_installed": "Megjegyzés: a ttkthemes könyvtár nincs telepítve. Az alapértelmezett Tkinter stílus lesz használva.",

    # =====================================
    #  Logok (naplóüzenetek)
    # =====================================

    # --- Általános / Konfiguráció ---
    "log_configured": "Naplózás konfigurálva: szint={0}, mód={1}, fájl={2}",
    "log_no_handlers": "Figyelmeztetés: nincs beállított naplókezelő (mód: {0}).",
    "log_critical_error": "Kritikus hiba a naplózás konfigurálásában: {0}",
    "log_basic_config": "Hiba miatt alap naplózási konfiguráció lett használva.",
    "log_dir_create_error": "Kritikus hiba: nem hozható létre naplómappa {0}: {1}",

    # --- Logok – Inicializálás / Könyvtárak (init_directories.py) ---
    "error_critical_init": "KRITIKUS HIBA az inicializálás során: {0}",
    "logger_init_error": "Hiba a könyvtárak inicializálásakor: {error}",
    "directory_created": "Könyvtár létrehozva: {0}",
    "directory_creation_error": "A(z) {0} könyvtár nem hozható létre: {1}",
    "sample_file_copied": "Minta fájl bemásolva ide: {0}",
    "sample_file_copy_error": "Hiba a minta fájl másolásakor: {0}",
    "log_created_output_dir": "Kimeneti mappa létrehozva: {0}",
    "log_cannot_create_output_dir": "A kimeneti mappa nem hozható létre {0}: {1}",

    # --- Logok – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Grafikai beállítások betöltése sikertelen az inicializáláskor: {0}",
    "log_loading_pdf": "PDF fájl betöltése: {0}",
    "log_loading_bitmap": "Raszteres fájl betöltése: {0}",
    "log_invalid_dpi": "Érvénytelen DPI olvasva ({0}). Alapérték használata: {1} DPI.",
    "log_image_dimensions": "Képméret: {0}×{1}px, mód: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Kép feldolgozása eredeti színmódban: {0}",
    "log_unusual_color_mode": "Szokatlan színmód: „{0}”. A ReportLab/Pillow hibásan működhet.",
    "log_draw_image_error": "ReportLab drawImage hiba a(z) {0} módban: {1}",
    "log_unsupported_format": "Nem támogatott bemeneti formátum: {0}",
    "log_input_file_not_found": "A bemeneti fájl nem található: {0}",
    "log_load_process_error": "Hiba a(z) {0} fájl betöltése vagy feldolgozása közben: {1}",
    "log_input_file_not_exists": "A bemeneti fájl nem létezik vagy az útvonal üres: „{0}”",
    "log_cannot_load_or_empty_pdf": "A bemeneti fájl nem tölthető be, vagy a PDF üres/sérült.",
    "log_pdf_dimensions_info": "  PDF méretek: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Érvénytelen PDF oldalméret: {0}×{1} pt.",

    #   Splitter – Méretszámítások
    "log_extra_margin": "Extra margó beállítva: {0:.3f} pt",
    "log_invalid_rows_cols": "Érvénytelen sor ({0}) vagy oszlop ({1}) szám.",
    "error_invalid_rows_cols": "A sorok és oszlopok száma pozitív egész legyen.",
    "log_invalid_overlap_white_stripe": "Érvénytelen átfedés ({0}) vagy fehér sáv ({1}) érték. Számnak kell lennie.",
    "error_invalid_overlap_white_stripe": "Az átfedés és a fehér sáv értékeinek számnak kell lenniük (mm).",
    "log_stripe_usage": "Beállítva: use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Alap átfedés (grafika): {0:.3f} mm, fehér sáv: {1:.3f} mm, tényleges átfedés: {2:.3f} mm",
    "log_computed_dimensions": "Számítva: PDF {0:.3f}×{1:.3f} mm. Panel: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Mag: {6:.3f}×{7:.3f} pt. Tényl. átfedés: {8:.3f} mm",
    "log_invalid_dimensions": "Érvénytelen panel ({0:.3f}×{1:.3f}) vagy mag ({2:.3f}×{3:.3f}) méret per={4}, sáv={5}, r={6}, c={7}, W={8} mm, H={9} mm esetén",
    "error_invalid_slice_dimensions": "A számított panel/mag méretek érvénytelenek vagy negatívak.",

    #   Splitter – Információ és sorrend
    "log_generating_slice_info": "Panelinformáció generálása: {0}",
    "log_no_slices_info_generated": "Nem sikerült panelinformációt generálni.",
    "log_applying_rotated_order": "180°-os forgatás szerinti sorrend alkalmazása: {0}",
    "log_applying_standard_order": "0° (standard) sorrend alkalmazása: {0}",
    "log_unknown_bryt_order": "Ismeretlen panel sorrend: „{0}”. Alapértelmezett használata.",
    "log_final_slices_order": "  Végső panelsorrend ({0}): [{1}]",

    #   Splitter – Átfedések (overlay) és összefésülés
    "log_invalid_dimensions_overlay": "Érvénytelen méretű overlay készítési kísérlet: {0}. Kihagyva.",
    "log_empty_overlay": "Üres vagy csaknem üres overlay PDF készült. Összefésülés kihagyva.",
    "log_overlay_error": "Hiba az overlay PDF létrehozásakor: {0}",
    "log_merge_error": "Overlay összevonása oldalak nélkül – kihagyva.",
    "log_merge_page_error": "Hiba az overlay PDF összevonásakor: {0}",
    "log_fallback_draw_rotating_elements": "Nem sikerült a sor/oszlop értékeket lekérni _draw_rotating_elements-hez, 1×1 használata.",
    "log_overlay_created_for_slice": "Overlay (sávok/jelek) létrehozva ehhez: {0}",
    "log_overlay_creation_failed_for_slice": "Overlay létrehozása sikertelen ehhez: {0}",
    "log_merging_rotated_overlay": "FORGATOTT overlay összevonása ehhez: {0}, T={1}",
    "log_merging_nonrotated_overlay": "NEM FORGATOTT overlay összevonása ehhez: {0}",
    "log_merging_all_codes_overlay": "Összevonás: összes kód overlay (forgatás nélkül)",
    "log_merging_separation_lines_overlay": "Összevonás: elválasztóvonal overlay (forgatás nélkül)",
    "log_merging_code_overlay_for_slice": "A {0} panel kód overlay-e összevonva forgatás nélkül.",
    "log_merging_separation_overlay_for_slice": "A {0} panel elválasztó overlay-e összevonva forgatás nélkül.",

    #   Splitter – Rajzolás (sávok, jelek, vonalak)
    "log_drawing_top_stripe": "[Canvas] Felső sáv rajzolása {0} számára: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Jobb sáv rajzolása {0} számára: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Sarok kitöltése és körberajzolása {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Kereszt rajzolása középponttal itt: ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Illesztővonalak rajzolása {0} számára a ({1:.3f},{2:.3f}) tartományban",
    "log_drawing_right_vertical_line": "  Jobb függőleges vonal rajzolása: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Felső vízszintes vonal rajzolása: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Elválasztóvonal rajzolása (fehér fekete felett): ({0}) @ ({1:.3f}, {2:.3f}), hossz={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Keresztek rajzolása {0} számára [{1},{2}] / [{3},{4}] a ({5:.1f},{6:.1f}) tartományban",
    "log_coord_calculation": "  Számított középpontok: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    TL rajzolása @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    TR rajzolása @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    BL rajzolása @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    BR rajzolása @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    {0} jel kihagyva a pozíciószabály szerint: [{1},{2}]",
    "log_trial_common_sheet": "TRIAL vízjel alkalmazása a közös íven",

    # Vízjel
    "log_trial_watermark_added": "TRIAL vízjel hozzáadva",
    "error_drawing_trial_text": "Hiba a vízjel szöveg rajzolásakor: {error}",

    #   Splitter – Elválasztóvonalak (teljes oldal)
    "log_drawing_separation_lines_for_page": "Elválasztóvonalak rajzolása oldalra (elrendezés={0}, panelek={1}, panel index={2})",
    "log_vertical_line_between_slices": "  Függőleges vonal {0}-{1} panelek között @ x={2:.1f}",
    "log_vertical_line_start": "  Függőleges vonal kezdete @ x={0:.1f}",
    "log_vertical_line_end": "  Függőleges vonal vége @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Vízszintes vonal {0}-{1} panelek között @ y={2:.1f}",
    "log_horizontal_line_start": "  Vízszintes vonal kezdete @ y={0:.1f}",
    "log_horizontal_line_end": "  Vízszintes vonal vége @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Külön_fájlok) Kezdés függ./vízsz. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Külön_fájlok) Vég függ./vízsz. @ {0:.1f}",

    #   Splitter – Kódok / QR generálása
    "log_generate_barcode_data": "Kód adatok generálása: {0}",
    "log_barcode_data_shortened": "A kód adatai {0} karakterre rövidítve.",
    "log_barcode_data_error": "Hiba a kód adatainak generálásakor: {0}",
    "log_compose_barcode_payload": "Kód payload összeállítása ({0}): {1}",
    "log_barcode_payload_shortened": "Payload {0} karakterre rövidítve a(z) {1} formátumhoz",
    "log_barcode_payload_error": "Hiba a payload összeállításakor: {0}",
    "log_unknown_anchor_fallback": "Ismeretlen horgony-sarok „{0}”, bal alsó használata",
    "log_used_default_code_settings": "Alapértelmezett kódbeállítások használata: {0}/{1}.",
    "log_no_layout_key_fallback": "Nincs „{0}” elrendezés {1}/{2} számára. Az első elérhető használata: „{3}”.",
    "log_code_settings_error": "Hiányzó/hibás kódbeállítások ({0}/{1}/{2}): {3}. Alapértékek használata.",
    "log_drawing_barcode": "{0} rajzolása itt: ({1:.3f}, {2:.3f}) [alap ({3:.3f}, {4:.3f}) + eltolás ({5:.3f}, {6:.3f})], forgatás: {7}°",
    "error_generate_qr_svg": "QR SVG generálása sikertelen.",
    "error_invalid_scale_for_qr": "Érvénytelen QR méret: {0} mm",
    "error_invalid_qr_scale_factor": "Érvénytelen QR skálázási tényező: {0}",
    "error_generate_barcode_svg": "Vonalkód SVG generálása sikertelen.",
    "error_invalid_scale_for_barcode": "Érvénytelen vonalkód méret: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Érvénytelen vonalkód skálázási tényező: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: beállított méret={1:.3f} mm, SVG szélesség={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: beállított méret=({1:.3f} mm, {2:.3f} mm), SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Hiba a(z) „{0}” kód rajzolásakor: {1}",
    "log_prepared_barcode_info": "Kódinformáció előkészítve ehhez: {0} ({1}, sarok={2}): alap abszolút pozíció ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Hiba a kódadatok előkészítésekor ehhez: {0}: {1}",
    "log_drawing_barcodes_count": "{0} kód/QR rajzolása...",
    "log_missing_barcode_info_key": "Hiányzó kulcs a kódinformációkban rajzoláskor: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Hiba a „{0}” kód rajzolásakor a _draw_all_barcodes metódusban: {1}",

    #   Splitter – Vágási folyamat (split_* metódusok)
    "log_start_splitting_process": "--- Vágási folyamat indítása ehhez: {0} ---",
    "log_split_settings": "  Beállítások: {0}×{1} panel, átfedés={2} mm, fehér sáv={3} mm (+átfedés: {4})",
    "log_output_dir_info": "  Kimenet: {0} / {1} itt: „{2}”",
    "log_lines_marks_barcodes_info": "  Vonalak: elválasztó={0}, kezdő={1}, záró={2} | Jelek: {3} ({4}), Kódok: {5} ({6})",
    "log_bryt_order_info": "  Sorrend: {0}, panelek forgatása: {1}°",
    "log_invalid_dimensions_in_slice_info": "Érvénytelen méretek a slice_info-ban ehhez: {0}: {1}×{2}",
    "log_content_transform": "Tartalom transzformáció T_content ehhez: {0}: {1}",
    "log_merged_content_for_slice": "Tartalom összevonva a(z) {0} panelhez a new_page oldalon",
    "log_slice_reader_created": "Teljes panel (PdfReader) létrehozva: {0}",
    "log_slice_reader_creation_error": "Hiba a teljes panel létrehozásakor ehhez: {0}: {1}",
    "log_used_get_transform": "_get_transform használata (csak eltolás): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Start: KÜLÖN FÁjlOK (forgatás a create_slice_reader-ben) ---",
    "log_creating_file_for_slice": "Fájl létrehozása ehhez a panelhez: {0}: {1}",
    "log_invalid_page_size_for_slice": "Érvénytelen oldalméret ({0}×{1}) ehhez: {2}. Kihagyva.",
    "log_blank_page_creation_error": "Üres oldal létrehozási hiba {0} számára (méret {1}×{2}): {3}. Kihagyva.",
    "log_transform_for_slice": "T transzformáció (csak eltolás) ehhez: {0}: {1}",
    "log_merging_complete_slice": "Teljes panel összevonása {0} transzformációval: {1}",
    "log_skipped_slice_merging": "A teljes panel összevonása kihagyva ehhez: {0}.",
    "log_file_saved": "Fájl mentve: {0}",
    "log_file_save_error": "Hiba a(z) {0} fájl mentésekor: {1}",
    "log_finished_split_separate_files": "--- Kész: KÜLÖN FÁjlOK (mentve {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Nincs feldolgozandó panel a split_horizontal-ban.",
    "log_start_split_horizontal": "--- Start: KÖZÖS ÍV – VÍZSZINTES (forgatás a create_slice_reader-ben) ---",
    "log_page_dimensions": "Oldalméret: {0:.1f}×{1:.1f} mm ({2} panel)",
    "log_page_creation_error": "Hiba a kimeneti oldal létrehozásakor ({0}×{1}): {2}. Megszakítva.",
    "log_slice_at_position": "{0} panel [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "T transzformáció (csak eltolás) ehhez: {0}: {1}",
    "log_merging_complete_bryt": "Teljes panel összevonása {0} transzformációval: {1}",
    "log_skipped_merging_bryt": "A teljes panel összevonása kihagyva ehhez: {0}.",
    "log_file_result_saved": "Eredményfájl mentve: {0}",
    "log_file_result_save_error": "Hiba az eredményfájl mentésekor {0}: {1}",
    "log_finished_split_horizontal": "--- Kész: KÖZÖS ÍV – VÍZSZINTES ---",
    "log_no_slices_split_vertical": "Nincs feldolgozandó panel a split_vertical-ban.",
    "log_start_split_vertical": "--- Start: KÖZÖS ÍV – FÜGGŐLEGES (forgatás a create_slice_reader-ben) ---",
    "log_finished_split_vertical": "--- Kész: KÖZÖS ÍV – FÜGGŐLEGES ---",
    "log_unknown_layout": "Ismeretlen elrendezés a közös ívhez: „{0}”.",
    "log_unknown_output_type": "Ismeretlen kimenettípus: „{0}”.",
    "log_finished_splitting_success": "--- Vágási folyamat befejezve: {0} — SIKER ---",
    "log_finished_splitting_errors": "--- Vágási folyamat befejezve: {0} — HIBÁK VOLTAK ---",
    "log_value_error_in_splitting": "Bemeneti vagy számítási hiba: {0}",
    "log_finished_splitting_critical_error": "--- Vágási folyamat befejezve: {0} — KRITIKUS HIBA ---",
    "log_unexpected_error_in_splitting": "Váratlan hiba a(z) {0} fájl vágása közben: {1}",

    #   Splitter – Teszt mód (__main__)
    "log_script_mode_test": "A splitter.py fő szkriptként fut (teszt mód).",
    "log_loaded_config": "Konfiguráció betöltve.",
    "log_error_loading_config": "Konfiguráció betöltése sikertelen: {0}",
    "log_created_example_pdf": "Példa PDF létrehozva: {0}",
    "log_cannot_create_example_pdf": "Példa PDF létrehozása sikertelen: {0}",
    "log_start_test_split": "Tesztvágás indítása a fájlra: {0} → {1}",
    "log_test_split_success": "Tesztvágás sikeresen befejezve.",
    "log_test_split_errors": "Tesztvágás hibákkal zárult.",

    # --- Logok – QR/vonalkód (barcode_qr.py) ---
    "log_qr_empty_data": "QR kód generálási kísérlet üres adatokkal.",
    "log_qr_generated": "QR SVG generálva ehhez: {0}...",
    "log_qr_error": "Hiba a QR generálásakor a(z) „{0}” adatokra: {1}",
    "log_barcode_empty_data": "Vonalkód generálási kísérlet üres adatokkal.",
    "log_barcode_generated": "Vonalkód SVG generálva ehhez: {0}...",
    "log_barcode_error": "Hiba a vonalkód generálásakor „{0}” számára: {1}",
    "log_basic_handler_configured": "Alap naplókezelő beállítva a barcode_qr.py-ben",
    "log_basic_handler_error": "Hiba az alap naplókezelő beállításakor a barcode_qr-ben: {0}",

    # --- Logok – Konfiguráció/Profilok (main_config_manager.py) ---
    "loading_profiles_from": "Profilok betöltése innen:",
    "profiles_file": "Profilfájl",
    "does_not_contain_dict": "nem tartalmaz szótárat. Új létrehozása",
    "not_found_creating_new": "nem található. Üres létrehozása",
    "json_profiles_read_error": "Hiba a profilok JSON olvasásakor",
    "file_will_be_overwritten": "A fájl mentéskor felülíródik",
    "json_decode_error_in_profiles": "JSON dekódolási hiba a profilfájlban",
    "cannot_load_profiles_file": "A profilfájl nem tölthető be",
    "unexpected_profiles_read_error": "Váratlan hiba a profilok olvasásakor",
    "saving_profiles_to": "Profilok mentése ide:",
    "cannot_save_profiles_file": "A profilfájl nem menthető",
    "profiles_save_error": "Hiba a profilok fájlba mentésekor",
    "logger_profile_saved": "Profil mentve: {profile}",
    "logger_profile_not_found": "A betöltendő profil nem található: {profile}",
    "logger_profile_loaded": "Profil betöltve: {profile}",
    "logger_profile_delete_not_exist": "Nem létező profil törlésének kísérlete: {profile}",
    "logger_profile_deleted": "Profil törölve: {profile}",
    "logger_start_save_settings": "GUI beállítások mentésének indítása.",
    "logger_invalid_value": "Érvénytelen érték a(z) „{key}” kulcshoz. 0.0 beállítva.",
    "logger_end_save_settings": "GUI beállítások mentése befejezve.",
    "logger_conversion_error": "Hiba a GUI értékek konvertálásakor: {error}",
    "conversion_failed": "GUI értékek konvertálása sikertelen",
    "logger_unexpected_save_error": "Váratlan hiba a beállítások mentésekor: {error}",
    "logger_settings_saved": "Beállítások mentve ebbe a fájlba: {file}",

    # --- Logok – Licencelés (main_license.py) ---
    "public_key_load_error_log": "Nyilvános kulcs betöltési hiba",
    "license_key_decode_error": "Licenckulcs dekódolási hiba",
    "license_activation_error": "Licencaktiválási hiba",

    # --- Logok – Fő modul (main.py) ---
    "ui_created": "A felhasználói felület létrehozva.",
    "error_tab_home": "Hiba a „Kezdőlap” felület létrehozásakor",
    "error_tab_settings": "Hiba a „Beállítások” felület létrehozásakor",
    "error_tab_help": "Hiba a „Súgó” felület létrehozásakor",
    "error_creating_license_ui": "Hiba a „Licenc” felület létrehozásakor",
    "error_loading_ui": "Általános hiba a felület betöltésekor: {error}",
    "error_creating_home_ui": "Hiba a „Kezdőlap” felület létrehozásakor",
    "error_creating_settings_ui": "Hiba a „Beállítások” felület létrehozásakor",
    "error_creating_help_ui": "Hiba a „Súgó” felület létrehozásakor",
    "logger_update_gui": "GUI frissítés indítva konfigurációból.",
    "logger_end_update_gui": "GUI frissítés konfigurációból befejezve.",
    "logger_update_gui_error": "Váratlan hiba a GUI frissítésekor: {error}",
    "logger_invalid_output_dir": "Érvénytelen vagy nem létező kimeneti mappa: {directory}",
    "logger_invalid_input_file": "Érvénytelen vagy nem létező bemeneti fájl: {file}",
    "logger_start_pdf": "PDF generálási folyamat indítva.",
    "logger_pdf_save_error": "PDF generálás megszakítva: az aktuális beállítások mentése sikertelen.",
    "logger_pdf_success": "PDF generálás sikeresen befejezve.",
    "logger_pdf_exception": "Kivétel a fő PDF generálási folyamatban.",
    "icon_set_error": "Hiba az alkalmazás ikon beállításakor: {error}",
    "accent_button_style_error": "Hiba a kiemelt gomb stílusának beállításakor: {error}",
    "logger_file_save_error": "Hiba a(z) {file} fájl mentésekor: {error}",

    #   Logok – Előnézet (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Hiba a bélyegkép generálásakor",
    "output_preview_update_called": "Kimeneti előnézet frissítése meghívva",
    "output_preview_canvas_missing": "Hiányzik a kimeneti előnézet vászna (canvas)",
    "pdf_found_in_output_dir": "PDF található a kimeneti mappában",
    "preparing_thumbnail": "Bélyegkép előkészítése",
    "thumbnail_generated_successfully": "Bélyegkép sikeresen létrehozva",
    "thumbnail_generation_error": "Hiba a bélyegkép létrehozásakor ehhez:",
    "no_pdf_for_common_sheet": "Nincs PDF a közös ív előnézetéhez",
    "no_pdf_for_separate_files": "Nincsenek generált PDF-ek az előnézethez",
    "cannot_load_thumbnail": "A bélyegkép nem tölthető be innen:",

    #   Logok – Fejlesztői belső (main.py)
    "missing_gui_var_created": "Hiányzó GUI változó létrehozva a kulcshoz: {key}",
    "missing_gui_structure_created": "Hiányzó GUI struktúra létrehozva ehhez: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Hiányzó GUI változó létrehozva ehhez: {code_type}/{output_type}/{layout}/{param}",

    # Kiegészítő szöveg a main_ui_help.py-hez
    "help_text": """
    Billboard Splitter – Felhasználói útmutató\n\n
    A program célja:\n
    A Billboard Splitter automatikusan olyan panelekké osztja a billboard-projekteket,
    amelyek nyomtatásra készek. A program 1:10 léptékű fájlokkal dolgozik.\n
    Az Átfedés, Fehér sáv és Beállítások szekciók értékeit 1:1 léptékben kell megadni.
    A program a kiválasztott elrendezés szerint PDF-be tudja rendezni a darabolt paneleket:\n
    • Közös ív: minden panel egy dokumentumban.\n
    • Külön fájlok: minden panel külön PDF-ben.\n\n
    További lehetőségek:\n
    • Elrendezés választása – függőleges vagy vízszintes (függőlegesnél a felső/alsó,
      vízszintesnél a bal/jobb oldalon vannak az elválasztóvonalak).\n
    • Panelek 180°-os elforgatása (a teljes projekt inverziója).\n
    • Illesztőjelek (kereszt vagy vonal) hozzáadása a pontos illesztéshez.\n
    • QR-kódok vagy vonalkódok hozzáadása – a bemeneti adatokból generálva a panelek azonosításához.\n
    • Beállítások mentése profilként, amelyeket betölthet, módosíthat és törölhet – gyors váltás projektek között.\n\n
    Alap lépések:\n\n
    1. Bemeneti fájl kiválasztása:\n
    • A „Kezdőlap” fülön válasszon PDF, JPG vagy TIFF fájlt a billboard tervvel.\n
    • Ha nem ad meg saját elérési utat, egy alapértelmezett mintafájl használatos.\n\n
    2. Vágási beállítások:\n
    • Adja meg a sorok és oszlopok számát, amelyre a projekt osztandó.\n
    • Állítsa be az átfedés méretét.\n
    • Opcionálisan adja meg a fehér sáv szélességét, amely hozzáadódik a tényleges átfedéshez.\n\n
    3. Kimeneti elrendezés:\n
    • Függőleges: a panelek függőlegesen helyezkednek el a PDF oldalon.\n
    • Vízszintes: a panelek vízszintesen helyezkednek el.\n\n
    4. Kimenet típusa:\n
    • Közös ív – egy PDF.\n
    • Külön fájlok – panelenként egy PDF.\n
    • A „Kezdőlap” fülön bekapcsolhatja és állíthatja az illesztőjeleket – kereszt vagy vonal.\n
    • Opcionálisan engedélyezze a QR/vonalkódot – a projekt adataiból generálódik.\n
    • A kód paraméterei (skála, eltolás, forgatás, pozíció) a „Beállítások” fülön állíthatók.\n\n
    5. Konfigurációk kezelése:\n
    • A „Beállítások” fülön finoman hangolhatók a grafikai paraméterek (margók, vonalvastagságok, hézagok) és a kódok.\n
    • Mentse az aktuális konfigurációt profilként a későbbi betöltéshez/módosításhoz.\n
    • A profilok (profiles.json) gyors váltást tesznek lehetővé a különböző beállításkészletek között.\n\n
    6. PDF generálása:\n
    • Ha kész, kattintson a „PDF generálása” gombra.\n
    • Az eredmények az „output” mappába kerülnek (vagy a megadottba), a naplók (napi rotációval) a „logs” mappába.\n\n
    Ha probléma merül fel:\n
    • Ellenőrizze a „logs” mappában található naplófájlokat. Minden nap új napló készül dátummal a nevében.\n
    • Győződjön meg róla, hogy minden szükséges könyvtár definiálva van.\n
    • Támogatás: tech@printworks.pl (munkanapokon, 8–16)\n
    """
}
