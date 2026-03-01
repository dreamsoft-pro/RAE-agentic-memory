# lang_ro.py
"""
Fișier de traduceri pentru limba română.
"""

LANG = {
    "barcode_font_size_label": "Dimensiunea fontului pentru descrierea codului de bare [pt]:",
    # ==========================
    #  Aplicație – General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Eroare",
    "no_file": "Niciun fișier",
    "language": "Limbă",
    "language_switch": "Schimbare limbă",
    "choose_language": "Alegeți limba:",
    "apply_language": "Aplică",
    "language_changed": "Limba a fost schimbată. Unele modificări vor fi vizibile după repornirea aplicației.",

    # ========================================
    #  Interfață grafică (GUI)
    # ========================================

    # --- File principale ---
    "tab_home": " Acasă ",
    "tab_settings": " Setări ",
    "tab_help": " Ajutor ",
    "tab_license": " Licență ",

    # --- Butoane generale ---
    "button_browse": "Răsfoiește...",
    "browse_folder": "Răsfoiește folderul...",
    "button_save": "Salvează",
    "button_delete": "Șterge",
    "button_close": "Închide",
    "save_all_settings": "Salvează toate setările",

    # --- Etichete câmpuri (Acasă) ---
    "label_rows": "Împărțire verticală (rânduri):",
    "label_columns": "Împărțire orizontală (coloane):",
    "label_overlap": "Suprapunere [mm]:",
    "label_white_stripe": "Bandă albă [mm]:",
    "label_add_white_stripe": "Adaugă banda albă la suprapunerea efectivă",
    "label_layout": "Aranjament ieșire:",
    "label_output_type": "Tip ieșire:",
    "label_enable_reg_marks": "Activează marcaje de înregistrare:",
    "label_enable_codes": "Activează coduri:",
    "label_enable_sep_lines": "Activează linii de separare (între panouri)",
    "label_enable_start_line": "Activează linia de început/marginea superioară a colii",
    "label_enable_end_line": "Activează linia de sfârșit/marginea inferioară a colii",
    "label_bryt_order": "Ordinea panourilor:",
    "label_slice_rotation": "Rotirea panourilor:",
    "label_create_order_folder": "Creează folder cu numărul comenzii",

    # --- Secțiuni (Acasă) ---
    "section_input_file": " Fișier de intrare ",
    "section_scale_and_dimensions": " Scară și dimensiuni de ieșire ",
    "label_original_size": "Dimensiune originală:",
    "label_scale_non_uniform": "Scalare neuniformă",
    "label_scale": "Scară: 1:",
    "label_scale_x": "Scară X: 1:",
    "label_scale_y": "Scară Y: 1:",
    "label_output_dimensions": "Dimensiunile fișierului de ieșire:",
    "label_width_cm": "Lățime [cm]:",
    "label_height_cm": "Înălțime [cm]:",
    "section_split_settings": " Setări tăiere ",
    "section_profiles": " Profiluri de setări ",
    "section_save_location": " Locație salvare ",
    "section_input_preview": " Previzualizare intrare ",
    "section_output_preview": " Previzualizare ieșire ",

    # --- Valori opțiuni ---
    "layout_vertical": "Vertical",
    "layout_horizontal": "Orizontal",
    "output_common_sheet": "Coală comună",
    "output_separate_files": "Fișiere separate",
    "output_both": "Coală comună și fișiere separate",
    "output_common": "Coală comună",
    "output_separate": "Fișiere separate",
    "reg_mark_cross": "Cruce",
    "reg_mark_line": "Linie",
    "code_qr": "Cod QR",
    "code_barcode": "Cod de bare",
    "bryt_order_1": "A1–An, B1–Bn, .. Standard, de sus",
    "bryt_order_2": "A1–An, Bn–B1, .. În șarpe pe rânduri, de sus",
    "bryt_order_3": "A1..B1, A2..B2, .. Pe coloane, de sus",
    "bryt_order_4": "A1–A2..B2–B1.. În șarpe pe coloane, de sus",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Standard, de jos",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. În șarpe pe rânduri, de jos",
    "logging_console": "consolă",
    "logging_file": "fișier",
    "logging_both": "ambele",

    # --- Secțiuni (Setări) ---
    "section_processing_mode": " Moduri de procesare ",
    "processing_mode_ram": "RAM (în memorie)",
    "processing_mode_hdd": "Disc (stocare)",
    "graphic_settings": "Setări grafice",
    "code_settings": "Setări QR / cod de bare",
    "logging_settings": "Setări jurnalizare",
    "barcode_text_position_label": "Poziția textului lângă cod:",
    "barcode_text_bottom": "jos",
    "barcode_text_side": "lateral",
    "barcode_text_none": "fără",

    # --- Etichete (Setări – Grafică) ---
    "extra_margin_label": "Margine în jurul panourilor [mm]:",
    "margin_top_label": "Margine sus [mm]:",
    "margin_bottom_label": "Margine jos [mm]:",
    "margin_left_label": "Margine stânga [mm]:",
    "margin_right_label": "Margine dreapta [mm]:",
    "reg_mark_width_label": "Marcaj – lățime [mm]:",
    "reg_mark_height_label": "Marcaj – înălțime [mm]:",
    "reg_mark_white_line_width_label": "Marcaj – grosimea liniei albe [mm]:",
    "reg_mark_black_line_width_label": "Marcaj – grosimea liniei negre [mm]:",
    "sep_line_black_width_label": "Separare – grosimea liniei negre [mm]:",
    "sep_line_white_width_label": "Separare – grosimea liniei albe [mm]:",
    "slice_gap_label": "Spațiu între panouri [mm]:",
    "label_draw_slice_border": "Desenează chenar în jurul panoului (linie de tăiere)",

    # --- Etichete (Setări – Coduri) ---
    "scale_label": "Dimensiune [mm]:",
    "scale_x_label": "Lățime X [mm]:",
    "scale_y_label": "Înălțime Y [mm]:",
    "offset_x_label": "Deplasare X [mm]:",
    "offset_y_label": "Deplasare Y [mm]:",
    "rotation_label": "Rotire (°):",
    "anchor_label": "Colț:",

    # --- Etichete (Setări – Loguri) ---
    "logging_mode_label": "Mod jurnalizare:",
    "log_file_label": "Fișier jurnal:",
    "logging_level_label": "Nivel jurnalizare:",

    # --- Butoane / acțiuni (Acasă) ---
    "button_load": "Încarcă",
    "button_save_settings": "Salvează setările curente",
    "button_generate_pdf": "Generează PDF",
    "button_refresh_preview": "Reîmprospătează previzualizarea",
    "button_refresh_layout": "Reîmprospătează aranjamentul",

    # --- Licență (GUI) ---
    "hwid_frame_title": "Identificator unic hardware (HWID)",
    "copy_hwid": "Copiază HWID",
    "license_frame_title": "Activare licență",
    "enter_license_key": "Introduceți cheia de licență:",
    "activate": "Activează",
    "status_trial": "Mod trial",
    "license_active": "Licența este activă",

    # ================================================
    #  Mesaje pentru utilizator (ferestre, bară de stare)
    # ================================================

    # --- Profiluri ---
    "msg_no_profile_name": "Fără nume",
    "msg_enter_profile_name": "Introduceți numele profilului pentru salvare.",
    "msg_profile_saved": "Profil salvat",
    "profile_saved_title": "Profil salvat",
    "msg_profile_saved_detail": "Profilul „{0}” a fost salvat.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profilul '{profile}' a fost salvat și aplicat.",
    "msg_no_profile": "Niciun profil",
    "warning_no_profile": "Niciun profil",
    "msg_select_profile": "Selectați din listă numele profilului pentru încărcare.",
    "select_profile": "Selectați din listă numele profilului pentru încărcare.",
    "profile_loaded_title": "Profil încărcat",
    "profile_loaded": "Profilul „{profile}” a fost încărcat.",
    "warning_no_profile_delete": "Niciun profil",
    "warning_no_profile_delete_message": "Selectați un profil din listă pentru ștergere.",
    "profile_not_found": "Profilul „{profile}” nu a fost găsit.",
    "profile_not_exist": "Profilul „{profile}” nu există.",
    "confirm_delete_title": "Confirmați ștergerea",
    "confirm_delete_profile": "Sigur doriți să ștergeți profilul „{profile}”?",
    "profile_deleted_title": "Profil șters",
    "profile_deleted": "Profilul „{profile}” a fost șters.",

    # --- Fișiere / directoare ---
    "msg_no_input_file": "Niciun fișier de intrare",
    "msg_unsupported_format": "Format neacceptat",
    "select_file_title": "Selectați fișierul de intrare",
    "supported_files": "Fișiere acceptate",
    "all_files": "Toate fișierele",
    "select_dir_title": "Selectați folderul de ieșire",
    "select_log_dir_title": "Selectați folderul pentru jurnale",
    "error_output_dir_title": "Eroare folder ieșire",
    "error_output_dir": "Folderul de ieșire specificat este invalid sau nu există:\n{directory}",
    "error_input_file_title": "Eroare fișier de intrare",
    "error_input_file": "Fișierul de intrare specificat este invalid sau nu există:\n{file}",
    "save_file_error_title": "Eroare salvare fișier",
    "save_file_error": "Fișierul nu a putut fi salvat: {error}",

    # --- Procesare PDF / previzualizare ---
    "msg_pdf_processing_error": "Procesarea fișierului PDF a eșuat",
    "msg_thumbnail_error": "Eroare la încărcarea miniaturii",
    "msg_no_pdf_output": "Nicio ieșire PDF",
    "no_pdf_pages": "PDF-ul nu conține pagini",
    "unsupported_output": "Tip de ieșire neacceptat pentru previzualizare",
    "pdf_generated_title": "Generarea s-a încheiat",
    "pdf_generated": "Fișier(ele) PDF au fost generate cu succes în folderul:\n{directory}",
    "pdf_generation_error_title": "Eroare la generare",
    "pdf_generation_error": "Au apărut erori în timpul generării PDF. Verificați jurnalele.",
    "critical_pdf_error_title": "Eroare critică la generarea PDF",
    "critical_pdf_error": "A apărut o eroare critică la generarea PDF:\n{error}\nConsultați jurnalele.",
    "settings_saved_title": "Setări salvate",
    "settings_saved": "Setările au fost salvate în fișierul:\n{filepath}",
    "settings_save_error_title": "Eroare salvare setări",
    "settings_save_error": "Setările nu au putut fi salvate: {error}",
    "conversion_error_title": "Eroare conversie",
    "conversion_error": "Eroare la conversia valorilor din interfață: {error}",
    "update_gui_error_title": "Eroare actualizare interfață",
    "update_gui_error": "A apărut o eroare la actualizarea interfeței: {error}",

    # --- Licență ---
    "hwid_copied_to_clipboard": "HWID copiat în clipboard",
    "computer_hwid": "HWID-ul calculatorului",
    "public_key_load_error": "Eroare la încărcarea cheii publice: {error}",
    "invalid_license_format": "Format de cheie de licență invalid: {error}",
    "activation_success": "Licența a fost activată cu succes.",
    "activation_error": "Eroare la activarea licenței: {error}",
    "log_trial_mode_active": "Modul trial este activ",
    "log_trial_mode_inactive": "Modul trial nu este activ",

    # --- Inițializare ---
    "init_error_title": "Eroare de inițializare",
    "init_error": "Eroare la inițializarea directoarelor: {error}",
    "poppler_path_info": "Informații despre calea Poppler",
    "ttkthemes_not_installed": "Atenție: biblioteca ttkthemes nu este instalată. Se va folosi stilul implicit Tkinter.",

    # =====================================
    #  Loguri (mesaje ale logger-ului)
    # =====================================

    # --- General / Configurare ---
    "log_configured": "Jurnalizare configurată: nivel={0}, mod={1}, fișier={2}",
    "log_no_handlers": "Avertisment: niciun handler de jurnal nu este configurat (mod: {0}).",
    "log_critical_error": "Eroare critică de configurare a jurnalizării: {0}",
    "log_basic_config": "Din cauza erorii s-a folosit configurația de bază a jurnalizării.",
    "log_dir_create_error": "Eroare critică: nu se poate crea folderul de jurnale {0}: {1}",

    # --- Loguri – Inițializare / Directoare (init_directories.py) ---
    "error_critical_init": "EROARE CRITICĂ în timpul inițializării: {0}",
    "logger_init_error": "Eroare la inițializarea directoarelor: {error}",
    "directory_created": "Director creat: {0}",
    "directory_creation_error": "Nu s-a putut crea directorul {0}: {1}",
    "sample_file_copied": "Fișier exemplu copiat în {0}",
    "sample_file_copy_error": "Eroare la copierea fișierului exemplu: {0}",
    "log_created_output_dir": "Folder de ieșire creat: {0}",
    "log_cannot_create_output_dir": "Nu se poate crea folderul de ieșire {0}: {1}",

    # --- Loguri – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Eșec la încărcarea setărilor grafice în timpul inițializării: {0}",
    "log_loading_pdf": "Se încarcă fișierul PDF: {0}",
    "log_loading_bitmap": "Se încarcă fișierul bitmap: {0}",
    "log_invalid_dpi": "DPI citit invalid ({0}). Se folosește valoarea implicită {1} DPI.",
    "log_image_dimensions": "Dimensiuni imagine: {0}×{1}px, mod: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Se procesează imaginea în modul de culoare original: {0}",
    "log_unusual_color_mode": "Mod de culoare neobișnuit: „{0}”. ReportLab/Pillow pot funcționa incorect.",
    "log_draw_image_error": "Eroare ReportLab drawImage pentru modul {0}: {1}",
    "log_unsupported_format": "Format de intrare neacceptat: {0}",
    "log_input_file_not_found": "Fișierul de intrare nu a fost găsit: {0}",
    "log_load_process_error": "Eroare la încărcarea sau procesarea fișierului {0}: {1}",
    "log_input_file_not_exists": "Fișierul de intrare nu există sau calea este goală: „{0}”",
    "log_cannot_load_or_empty_pdf": "Nu se poate încărca fișierul de intrare sau PDF-ul este gol/deteriorat.",
    "log_pdf_dimensions_info": "  Dimensiuni PDF: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Dimensiuni nevalide ale paginii PDF: {0}×{1} pt.",

    #   Splitter – Calcul dimensiuni
    "log_extra_margin": "Margine suplimentară setată la {0:.3f} pt",
    "log_invalid_rows_cols": "Număr invalid de rânduri ({0}) sau coloane ({1}).",
    "error_invalid_rows_cols": "Rândurile și coloanele trebuie să fie numere întregi pozitive.",
    "log_invalid_overlap_white_stripe": "Valori invalide pentru suprapunere ({0}) sau banda albă ({1}). Trebuie să fie numerice.",
    "error_invalid_overlap_white_stripe": "Suprapunerea și banda albă trebuie să fie valori numerice (mm).",
    "log_stripe_usage": "Setat use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Suprapunere de bază (grafică): {0:.3f} mm, bandă albă: {1:.3f} mm, suprapunere efectivă: {2:.3f} mm",
    "log_computed_dimensions": "Calculat: PDF {0:.3f}×{1:.3f} mm. Panou: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Nucleu: {6:.3f}×{7:.3f} pt. Suprap. efectivă: {8:.3f} mm",
    "log_invalid_dimensions": "Dimensiuni invalide ale panoului ({0:.3f}×{1:.3f}) sau nucleului ({2:.3f}×{3:.3f}) pentru per={4}, bandă={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Dimensiunile calculate ale panoului/nucleului sunt invalide sau negative.",

    #   Splitter – Generare info și ordine
    "log_generating_slice_info": "Se generează informații pentru panou: {0}",
    "log_no_slices_info_generated": "Nu s-au putut genera informațiile despre panouri.",
    "log_applying_rotated_order": "Se aplică ordinea pentru rotație 180°: {0}",
    "log_applying_standard_order": "Se aplică ordinea pentru 0° (standard): {0}",
    "log_unknown_bryt_order": "Ordine necunoscută a panourilor: „{0}”. Se folosește cea implicită.",
    "log_final_slices_order": "  Ordinea finală a panourilor ({0}): [{1}]",

    #   Splitter – Suprapuneri (overlay) și îmbinare
    "log_invalid_dimensions_overlay": "Încercare de creare overlay cu dimensiuni invalide: {0}. Se omite.",
    "log_empty_overlay": "A fost creat un overlay PDF gol sau aproape gol. Îmbinarea este omisă.",
    "log_overlay_error": "Eroare la crearea overlay-ului PDF: {0}",
    "log_merge_error": "Încercare de îmbinare a overlay-ului fără pagini. Se omite.",
    "log_merge_page_error": "Eroare la îmbinarea overlay-ului PDF: {0}",
    "log_fallback_draw_rotating_elements": "Nu s-au putut obține rânduri/coloane pentru _draw_rotating_elements, s-a folosit 1×1.",
    "log_overlay_created_for_slice": "Overlay pentru benzi/marcaje creat pentru panoul {0}",
    "log_overlay_creation_failed_for_slice": "Eșec la crearea overlay-ului pentru {0}",
    "log_merging_rotated_overlay": "Se îmbină overlay ROTIT pentru {0} cu T={1}",
    "log_merging_nonrotated_overlay": "Se îmbină overlay NEROTIT pentru {0}",
    "log_merging_all_codes_overlay": "Se îmbină overlay-ul tuturor codurilor (fără rotație)",
    "log_merging_separation_lines_overlay": "Se îmbină overlay-ul liniilor de separare (fără rotație)",
    "log_merging_code_overlay_for_slice": "Overlay-ul codului pentru {0} îmbinat fără rotație.",
    "log_merging_separation_overlay_for_slice": "Overlay-ul liniilor de separare pentru {0} îmbinat fără rotație.",

    #   Splitter – Desen (benzi, marcaje, linii)
    "log_drawing_top_stripe": "[Canvas] Desenez banda superioară pentru {0}: x={1:.3f}, y={2:.3f}, l={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Desenez banda dreaptă pentru {0}: x={1:.3f}, y={2:.3f}, l={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Umplu și conturez colțul pentru {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Desenez cruce cu centrul în ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Desenez linii de înregistrare pentru {0} în zona de la ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Desenez linia verticală dreapta: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Desenez linia orizontală sus: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Desenez linie de separare (alb peste negru): ({0}) @ ({1:.3f}, {2:.3f}), lungime={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Desenez cruci pentru {0} [{1},{2}] / [{3},{4}] în zona de la ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Centre calculate: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Desenez TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Desenez TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Desenez BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Desenez BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Marcajul {0} omis conform regulii pentru poziția [{1},{2}]",
    "log_trial_common_sheet": "Aplic filigranul TRIAL pe coala comună",

    # Filigran
    "log_trial_watermark_added": "Filigran TRIAL adăugat",
    "error_drawing_trial_text": "Eroare la desenarea filigranului: {error}",

    #   Splitter – Linii de separare (pagină întreagă)
    "log_drawing_separation_lines_for_page": "Desenez linii de separare pentru pagină (aranjament={0}, nr. panouri={1}, index panou={2})",
    "log_vertical_line_between_slices": "  Linie verticală între panourile {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Început linie verticală @ x={0:.1f}",
    "log_vertical_line_end": "  Sfârșit linie verticală @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Linie orizontală între panourile {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Început linie orizontală @ y={0:.1f}",
    "log_horizontal_line_end": "  Sfârșit linie orizontală @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Fișiere_separate) Start vert./oriz. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Fișiere_separate) Sfârșit vert./oriz. @ {0:.1f}",

    #   Splitter – Generare coduri / QR
    "log_generate_barcode_data": "Generez date pentru cod: {0}",
    "log_barcode_data_shortened": "Datele codului scurtate la {0} caractere.",
    "log_barcode_data_error": "Eroare la generarea datelor pentru cod: {0}",
    "log_compose_barcode_payload": "Compun payload pentru cod ({0}): {1}",
    "log_barcode_payload_shortened": "Payload scurtat la {0} caractere pentru formatul {1}",
    "log_barcode_payload_error": "Eroare la compunerea payload-ului: {0}",
    "log_unknown_anchor_fallback": "Colț de ancorare necunoscut „{0}”, se folosește stânga jos",
    "log_used_default_code_settings": "S-au folosit setările „default” pentru codul {0}/{1}.",
    "log_no_layout_key_fallback": "Nu există aranjamentul „{0}” pentru {1}/{2}. Folosit primul disponibil: „{3}”.",
    "log_code_settings_error": "Setări de cod lipsă/eroare ({0}/{1}/{2}): {3}. S-au folosit valorile implicite.",
    "log_drawing_barcode": "Desenez {0} la ({1:.3f}, {2:.3f}) [bază ({3:.3f}, {4:.3f}) + deplasare ({5:.3f}, {6:.3f})], rotație: {7}°",
    "error_generate_qr_svg": "Generarea SVG pentru codul QR a eșuat.",
    "error_invalid_scale_for_qr": "Dimensiune QR invalidă: {0} mm",
    "error_invalid_qr_scale_factor": "Factor de scală QR invalid: {0}",
    "error_generate_barcode_svg": "Generarea SVG pentru codul de bare a eșuat.",
    "error_invalid_scale_for_barcode": "Dimensiune invalidă pentru codul de bare: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Factor de scală invalid pentru codul de bare: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: dimensiune în configurare={1:.3f} mm, lățime SVG={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: dimensiune în configurare=({1:.3f} mm, {2:.3f} mm), dimensiune SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Eroare la desenarea codului „{0}”: {1}",
    "log_prepared_barcode_info": "Informații despre cod pregătite pentru {0} ({1}, colț={2}): poziție absolută de bază ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Eroare la pregătirea datelor pentru codul {0}: {1}",
    "log_drawing_barcodes_count": "Desenez {0} coduri/QR...",
    "log_missing_barcode_info_key": "Cheie lipsă în informațiile codului la desenare: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Eroare la desenarea codului „{0}” în _draw_all_barcodes: {1}",

    #   Splitter – Proces de tăiere (metodele split_*)
    "log_start_splitting_process": "--- Pornez procesul de tăiere pentru: {0} ---",
    "log_split_settings": "  Setări: {0}×{1} panouri, suprapunere={2} mm, bandă albă={3} mm (+suprapunere: {4})",
    "log_output_dir_info": "  Ieșire: {0} / {1} în „{2}”",
    "log_lines_marks_barcodes_info": "  Linii: separare={0}, început={1}, sfârșit={2} | Marcaje: {3} ({4}), Coduri: {5} ({6})",
    "log_bryt_order_info": "  Ordine: {0}, rotirea panourilor: {1}°",
    "log_invalid_dimensions_in_slice_info": "Dimensiuni invalide în slice_info pentru {0}: {1}×{2}",
    "log_content_transform": "Transformare conținut T_content pentru {0}: {1}",
    "log_merged_content_for_slice": "Conținut îmbinat pentru panoul {0} în new_page",
    "log_slice_reader_created": "Panou complet (PdfReader) creat pentru {0}",
    "log_slice_reader_creation_error": "Eroare la crearea panoului complet pentru {0}: {1}",
    "log_used_get_transform": "S-a folosit _get_transform (doar deplasare): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Start: FIȘIERE SEPARATE (rotație în create_slice_reader) ---",
    "log_creating_file_for_slice": "Creez fișier pentru panoul {0}: {1}",
    "log_invalid_page_size_for_slice": "Dimensiune pagină invalidă ({0}×{1}) pentru {2}. Se omite.",
    "log_blank_page_creation_error": "Eroare la crearea paginii goale pentru {0} (dimensiune {1}×{2}): {3}. Se omite.",
    "log_transform_for_slice": "Transformare T (doar deplasare) pentru {0}: {1}",
    "log_merging_complete_slice": "Îmbinare panou complet {0} cu transformare: {1}",
    "log_skipped_slice_merging": "Îmbinarea panoului complet pentru {0} a fost omisă.",
    "log_file_saved": "Fișier salvat: {0}",
    "log_file_save_error": "Eroare la salvarea fișierului {0}: {1}",
    "log_finished_split_separate_files": "--- Finalizat: FIȘIERE SEPARATE (salvate {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Niciun panou de procesat în split_horizontal.",
    "log_start_split_horizontal": "--- Start: COALĂ COMUNĂ – ORIZONTAL (rotație în create_slice_reader) ---",
    "log_page_dimensions": "Dimensiuni pagină: {0:.1f}×{1:.1f} mm ({2} panouri)",
    "log_page_creation_error": "Eroare la crearea paginii de ieșire ({0}×{1}): {2}. Se întrerupe.",
    "log_slice_at_position": "Panoul {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformare T (doar deplasare) pentru {0}: {1}",
    "log_merging_complete_bryt": "Îmbinare panou complet {0} cu transformare: {1}",
    "log_skipped_merging_bryt": "Îmbinarea panoului complet pentru {0} omisă.",
    "log_file_result_saved": "Fișier rezultat salvat: {0}",
    "log_file_result_save_error": "Eroare la salvarea fișierului rezultat {0}: {1}",
    "log_finished_split_horizontal": "--- Finalizat: COALĂ COMUNĂ – ORIZONTAL ---",
    "log_no_slices_split_vertical": "Niciun panou de procesat în split_vertical.",
    "log_start_split_vertical": "--- Start: COALĂ COMUNĂ – VERTICAL (rotație în create_slice_reader) ---",
    "log_finished_split_vertical": "--- Finalizat: COALĂ COMUNĂ – VERTICAL ---",
    "log_unknown_layout": "Aranjament necunoscut pentru coala comună: „{0}”.",
    "log_unknown_output_type": "Tip de ieșire necunoscut: „{0}”.",
    "log_finished_splitting_success": "--- Procesul de tăiere finalizat pentru: {0} — SUCCES ---",
    "log_finished_splitting_errors": "--- Procesul de tăiere finalizat pentru: {0} — AU EXISTAT ERORI ---",
    "log_value_error_in_splitting": "Eroare de intrare sau de calcul: {0}",
    "log_finished_splitting_critical_error": "--- Procesul de tăiere finalizat pentru: {0} — EROARE CRITICĂ ---",
    "log_unexpected_error_in_splitting": "Eroare neașteptată la tăierea fișierului {0}: {1}",

    #   Splitter – Mod test (__main__)
    "log_script_mode_test": "splitter.py rulat ca script principal (mod test).",
    "log_loaded_config": "Configurație încărcată.",
    "log_error_loading_config": "Încărcarea configurației a eșuat: {0}",
    "log_created_example_pdf": "PDF exemplu creat: {0}",
    "log_cannot_create_example_pdf": "Crearea PDF-ului exemplu a eșuat: {0}",
    "log_start_test_split": "Pornesc tăierea de test pentru fișierul: {0} în {1}",
    "log_test_split_success": "Tăierea de test s-a încheiat cu succes.",
    "log_test_split_errors": "Tăierea de test s-a încheiat cu erori.",

    # --- Loguri – QR/cod de bare (barcode_qr.py) ---
    "log_qr_empty_data": "Încercare de generare cod QR pentru date goale.",
    "log_qr_generated": "SVG pentru codul QR generat pentru: {0}...",
    "log_qr_error": "Eroare la generarea QR pentru datele „{0}”: {1}",
    "log_barcode_empty_data": "Încercare de generare cod de bare pentru date goale.",
    "log_barcode_generated": "SVG pentru codul de bare generat pentru: {0}...",
    "log_barcode_error": "Eroare la generarea codului de bare pentru „{0}”: {1}",
    "log_basic_handler_configured": "Handler de bază configurat pentru logger în barcode_qr.py",
    "log_basic_handler_error": "Eroare la configurarea handler-ului de bază în barcode_qr: {0}",

    # --- Loguri – Configurație/Profiluri (main_config_manager.py) ---
    "loading_profiles_from": "Se încarcă profiluri din",
    "profiles_file": "Fișier de profiluri",
    "does_not_contain_dict": "nu conține un dicționar. Se creează unul nou",
    "not_found_creating_new": "nu a fost găsit. Se creează unul nou gol",
    "json_profiles_read_error": "Eroare la citirea JSON-ului de profiluri",
    "file_will_be_overwritten": "Fișierul va fi suprascris la salvare",
    "json_decode_error_in_profiles": "Eroare de decodare JSON în fișierul de profiluri",
    "cannot_load_profiles_file": "Nu se poate încărca fișierul de profiluri",
    "unexpected_profiles_read_error": "Eroare neașteptată la citirea profilurilor",
    "saving_profiles_to": "Se salvează profiluri în",
    "cannot_save_profiles_file": "Nu se poate salva fișierul de profiluri",
    "profiles_save_error": "Eroare la salvarea profilurilor în fișier",
    "logger_profile_saved": "Profil salvat: {profile}",
    "logger_profile_not_found": "Profilul pentru încărcare nu a fost găsit: {profile}",
    "logger_profile_loaded": "Profil încărcat: {profile}",
    "logger_profile_delete_not_exist": "Încercare de ștergere a unui profil inexistent: {profile}",
    "logger_profile_deleted": "Profil șters: {profile}",
    "logger_start_save_settings": "A fost pornită salvarea setărilor din GUI.",
    "logger_invalid_value": "Valoare invalidă pentru „{key}”. Setată la 0.0.",
    "logger_end_save_settings": "Salvarea setărilor din GUI s-a încheiat.",
    "logger_conversion_error": "Eroare de conversie a valorilor din GUI: {error}",
    "conversion_failed": "Conversia valorilor din GUI a eșuat",
    "logger_unexpected_save_error": "Eroare neașteptată la salvarea setărilor: {error}",
    "logger_settings_saved": "Setări salvate în fișierul: {file}",

    # --- Loguri – Licențiere (main_license.py) ---
    "public_key_load_error_log": "Eroare la încărcarea cheii publice",
    "license_key_decode_error": "Eroare la decodarea cheii de licență",
    "license_activation_error": "Eroare la activarea licenței",

    # --- Loguri – Modul principal (main.py) ---
    "ui_created": "Interfața utilizator a fost creată.",
    "error_tab_home": "Eroare la crearea interfeței „Acasă”",
    "error_tab_settings": "Eroare la crearea interfeței „Setări”",
    "error_tab_help": "Eroare la crearea interfeței „Ajutor”",
    "error_creating_license_ui": "Eroare la crearea interfeței „Licență”",
    "error_loading_ui": "Eroare generală la încărcarea interfeței: {error}",
    "error_creating_home_ui": "Eroare la crearea interfeței „Acasă”",
    "error_creating_settings_ui": "Eroare la crearea interfeței „Setări”",
    "error_creating_help_ui": "Eroare la crearea interfeței „Ajutor”",
    "logger_update_gui": "A pornit actualizarea GUI din configurație.",
    "logger_end_update_gui": "Actualizarea GUI din configurație s-a încheiat.",
    "logger_update_gui_error": "Eroare neașteptată la actualizarea GUI: {error}",
    "logger_invalid_output_dir": "Folder de ieșire invalid sau inexistent: {directory}",
    "logger_invalid_input_file": "Fișier de intrare invalid sau inexistent: {file}",
    "logger_start_pdf": "A pornit procesul de generare PDF.",
    "logger_pdf_save_error": "Generarea PDF a fost întreruptă: salvarea setărilor curente a eșuat.",
    "logger_pdf_success": "Generarea PDF s-a încheiat cu succes.",
    "logger_pdf_exception": "Excepție în procesul principal de generare PDF.",
    "icon_set_error": "Eroare la setarea iconiței aplicației: {error}",
    "accent_button_style_error": "Eroare la setarea stilului butonului de accent: {error}",
    "logger_file_save_error": "Eroare la salvarea fișierului {file}: {error}",

    #   Loguri – Previzualizare (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Eroare la generarea miniaturii",
    "output_preview_update_called": "A fost apelată actualizarea previzualizării ieșirii",
    "output_preview_canvas_missing": "Lipsește canvas-ul previzualizării ieșirii",
    "pdf_found_in_output_dir": "PDF găsit în folderul de ieșire",
    "preparing_thumbnail": "Se pregătește miniatura",
    "thumbnail_generated_successfully": "Miniatură generată cu succes",
    "thumbnail_generation_error": "Eroare la generarea miniaturii pentru",
    "no_pdf_for_common_sheet": "Nu există PDF pentru previzualizarea coalei comune",
    "no_pdf_for_separate_files": "Nu există PDF-uri generate pentru previzualizare",
    "cannot_load_thumbnail": "Nu se poate încărca miniatura din",

    #   Loguri – Intern pentru dezvoltare (main.py)
    "missing_gui_var_created": "Variabilă GUI lipsă creată pentru cheia: {key}",
    "missing_gui_structure_created": "Structură GUI lipsă creată pentru: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Variabilă GUI lipsă creată pentru: {code_type}/{output_type}/{layout}/{param}",

    # Chei suplimentare pentru main_ui_help.py
    "help_text": """
    Billboard Splitter – Ghidul utilizatorului\n\n
    Scopul programului:\n
    Billboard Splitter împarte automat proiectele de billboard în panouri gata de tipar.
    Programul este conceput pentru a lucra cu fișiere la scara 1:10.\n
    Valorile din secțiunile: Suprapunere, Bandă albă și Setări se introduc la scara 1:1.
    Programul permite salvarea panourilor tăiate în PDF conform aranjamentului ales:\n
    • Coală comună: toate panourile într-un singur document.\n
    • Fișiere separate: fiecare panou într-un PDF separat.\n\n
    De asemenea, programul permite:\n
    • Alegerea aranjamentului – vertical sau orizontal (în vertical, liniile de separare sunt sus și jos,
      în orizontal – stânga și dreapta).\n
    • Rotirea panourilor la 180° (inversiunea întregului proiect).\n
    • Adăugarea de marcaje de înregistrare (cruce sau linie) pentru poziționare precisă la lipire.\n
    • Adăugarea de coduri QR sau coduri de bare – generate din datele de intrare pentru identificarea panourilor.\n
    • Salvarea configurațiilor ca profiluri care pot fi încărcate, modificate și șterse – comutare rapidă între proiecte.\n\n
    Pași de bază:\n\n
    1. Selectarea fișierului de intrare:\n
    • Pe fila „Acasă” selectați un PDF, JPG sau TIFF cu proiectul billboardului.\n
    • Dacă nu specificați o cale proprie, se va folosi un fișier demonstrativ implicit.\n\n
    2. Setări de tăiere:\n
    • Introduceți numărul de rânduri și coloane în care se împarte proiectul.\n
    • Setați dimensiunea suprapunerii.\n
    • Opțional, setați lățimea benzii albe care se adaugă la suprapunerea efectivă.\n\n
    3. Aranjamentul ieșirii:\n
    • Vertical: panourile sunt aranjate vertical pe pagina PDF.\n
    • Orizontal: panourile sunt aranjate orizontal.\n\n
    4. Tipul de ieșire:\n
    • Coală comună – un singur PDF.\n
    • Fișiere separate – un PDF pentru fiecare panou.\n
    • Pe „Acasă” puteți activa și regla marcajele – cruce sau linie.\n
    • Opțional, activați QR sau cod de bare – va fi generat din datele proiectului.\n
    • Parametrii codului (scală, deplasare, rotație, poziție) se ajustează pe fila „Setări”.\n\n
    5. Gestionarea configurațiilor:\n
    • Pe fila „Setări” ajustați fin parametrii grafici (margini, grosimi de linii, spațieri) și setările codurilor.\n
    • Salvați configurația curentă ca profil pentru încărcare sau modificare ulterioară.\n
    • Profilurile (profiles.json) permit comutarea rapidă între seturi de setări.\n\n
    6. Generarea PDF:\n
    • După configurare, faceți clic pe „Generează PDF”.\n
    • Rezultatele se salvează în folderul „output” (sau altul ales), iar jurnalele (cu rotație zilnică) în „logs”.\n\n
    Dacă apar probleme:\n
    • Verificați jurnalele din folderul „logs”. În fiecare zi se creează un nou fișier jurnal cu data în nume.\n
    • Asigurați-vă că toate directoarele necesare sunt definite.\n
    • Suport: tech@printworks.pl (zile lucrătoare, 8–16)\n
    """
}
