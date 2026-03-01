# lang_da.py
"""
Fil med oversættelser til dansk.
"""
 
LANG = {
    "barcode_font_size_label": "Stregkodebeskrivelses skriftstørrelse [pt]:",
    # ==========================
    #  Application - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Fejl",
    "no_file": "Ingen fil",
    "language": "Sprog",
    "language_switch": "Skift sprog",
    "choose_language": "Vælg sprog:",
    "apply_language": "Anvend",
    "language_changed": "Sproget er ændret. Nogle ændringer vil først være synlige efter genstart af programmet.",

    # ========================================
    #  User Interface (GUI) Elements
    # ========================================

    # --- Main Tabs ---
    "tab_home": " Hjem ",
    "tab_settings": " Indstillinger ",
    "tab_help": " Hjælp ",
    "tab_license": " Licens ",

    # --- General Buttons ---
    "button_browse": "Gennemse...",
    "browse_folder": "Gennemse mappe...",
    "button_save": "Gem",
    "button_delete": "Slet",
    "button_close": "Luk",
    "save_all_settings": "Gem alle indstillinger",

    # --- Field Labels (Home Tab) ---
    "label_rows": "Lodret opdeling (rækker):",
    "label_columns": "Vandret opdeling (kolonner):",
    "label_overlap": "Overlap [mm]:",
    "label_white_stripe": "Hvid stribe [mm]:",
    "label_add_white_stripe": "Tilføj hvid stribe til effektivt overlap",
    "label_layout": "Udgangslayout:",
    "label_output_type": "Udgangstype:",
    "label_enable_reg_marks": "Aktiver registermærker:",
    "label_enable_codes": "Aktiver koder:",
    "label_enable_sep_lines": "Aktiver separationslinjer (mellem paneler)",
    "label_enable_start_line": "Aktiver start/øverste linje på arket",
    "label_enable_end_line": "Aktiver slut/nederste linje på arket",
    "label_bryt_order": "Rækkefølge af paneler:",
    "label_slice_rotation": "Rotation af paneler:",
    "label_create_order_folder": "Opret mappe med ordrenummer",

    # --- Sections/Frames (Home Tab) ---
    "section_input_file": " Inputfil ",
    "section_scale_and_dimensions": " Skala og outputdimensioner ",
    "label_original_size": "Original størrelse:",
    "label_scale_non_uniform": "Skaler uproportionelt",
    "label_scale": "Skala: 1:",
    "label_scale_x": "Skala X: 1:",
    "label_scale_y": "Skala Y: 1:",
    "label_output_dimensions": "Outputfilens dimensioner:",
    "label_width_cm": "Bredde [cm]:",
    "label_height_cm": "Højde [cm]:",
    "section_split_settings": " Indstillinger for opdeling ",
    "section_profiles": " Indstillingsprofiler ",
    "section_save_location": " Placering for gemte filer ",
    "section_input_preview": " Forhåndsvisning af inputfil ",
    "section_output_preview": " Forhåndsvisning af output ",

    # --- Option Values (Combobox, Radiobutton etc.) ---
    "layout_vertical": "Lodret",
    "layout_horizontal": "Vandret",
    "output_common_sheet": "Fælles ark",
    "output_separate_files": "Separate filer",
    "output_both": "Fælles ark og separate filer",
    "output_common": "Fælles ark",
    "output_separate": "Separate filer",
    "reg_mark_cross": "Kryds",
    "reg_mark_line": "Linje",
    "code_qr": "QR‑kode",
    "code_barcode": "Stregkode",
    "bryt_order_1": "A1-An, B1-Bn, .. Standard, fra toppen",
    "bryt_order_2": "A1-An, Bn-B1, .. Slange efter rækker, fra toppen",
    "bryt_order_3": "A1..B1, A2..B2, .. Efter kolonner, fra toppen",
    "bryt_order_4": "A1-A2..B2-B1.. Slange efter kolonner, fra toppen",
    "bryt_order_5": "N1-Nn, (N-1)1-(N-1)n, .. Standard, fra bunden",
    "bryt_order_6": "N1-Nn, (N-1)n-(N-1)1, .. Slange efter rækker, fra bunden",
    "logging_console": "konsol",
    "logging_file": "fil",
    "logging_both": "begge",

    # --- Sections/Frames (Settings Tab) ---
    "section_processing_mode": " Skæreoperationer ",
    "processing_mode_ram": "RAM (i hukommelsen)",
    "processing_mode_hdd": "Disk (på drev)",
    "graphic_settings": "Grafiske indstillinger",
    "code_settings": "QR / Stregkode indstillinger",
    "logging_settings": "Logningsindstillinger",
    "barcode_text_position_label": "Placering af stregkodetekst:",
    "barcode_text_bottom": "nedenfor",
    "barcode_text_side": "ved siden af",
    "barcode_text_none": "ingen",

    # --- Field Labels (Settings Tab - Graphics) ---
    "extra_margin_label": "Margin omkring paneler [mm]:",
    "margin_top_label": "Øverste margin [mm]:",
    "margin_bottom_label": "Nederste margin [mm]:",
    "margin_left_label": "Venstre margin [mm]:",
    "margin_right_label": "Højre margin [mm]:",
    "reg_mark_width_label": "Registermærke – bredde [mm]:",
    "reg_mark_height_label": "Registermærke – højde [mm]:",
    "reg_mark_white_line_width_label": "Registermærke – hvid linjetykkelse [mm]:",
    "reg_mark_black_line_width_label": "Registermærke – sort linjetykkelse [mm]:",
    "sep_line_black_width_label": "Separationslinje – sort linjetykkelse [mm]:",
    "sep_line_white_width_label": "Separationslinje – hvid linjetykkelse [mm]:",
    "slice_gap_label": "Mellemrum mellem paneler [mm]:",
    "label_draw_slice_border": "Tegn kant omkring panelet (skærelinje)",

    # --- Field Labels (Settings Tab - Codes) ---
    "scale_label": "Størrelse [mm]:",
    "scale_x_label": "Bredde X [mm]:",
    "scale_y_label": "Højde Y [mm]:",
    "offset_x_label": "Forskydning X [mm]:",
    "offset_y_label": "Forskydning Y [mm]:",
    "rotation_label": "Rotation (°):",
    "anchor_label": "Hjørne:",

    # --- Field Labels (Settings Tab - Logging) ---
    "logging_mode_label": "Logningstilstand:",
    "log_file_label": "Logfil:",
    "logging_level_label": "Logningsniveau:",

    # --- Buttons / Actions (Home Tab) ---
    "button_load": "Indlæs",
    "button_save_settings": "Gem aktuelle indstillinger",
    "button_generate_pdf": "Generér PDF",
    "button_refresh_preview": "Opdatér forhåndsvisning",
    "button_refresh_layout": "Opdatér layout",

    # --- License (GUI) ---
    "hwid_frame_title": "Unik hardware‑identifikator (HWID)",
    "copy_hwid": "Kopiér HWID",
    "license_frame_title": "Aktivering af licens",
    "enter_license_key": "Indtast licensnøgle:",
    "activate": "Aktivér",
    "status_trial": "Prøvetilstand",
    "license_active": "Licens aktiv",

    # ================================================
    #  User Messages (Windows, Status Bar)
    # ================================================

    # --- Profiles ---
    "msg_no_profile_name": "Intet navn",
    "msg_enter_profile_name": "Indtast et profilnavn for at gemme.",
    "msg_profile_saved": "Profil gemt",
    "profile_saved_title": "Profil gemt",
    "msg_profile_saved_detail": "Profilen '{0}' er gemt.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profilen '{profile}' er blevet gemt og anvendt.",
    "msg_no_profile": "Ingen profil",
    "warning_no_profile": "Ingen profil",
    "msg_select_profile": "Vælg et profilnavn fra listen for at indlæse.",
    "select_profile": "Vælg et profilnavn fra listen for at indlæse.",
    "profile_loaded_title": "Profil indlæst",
    "profile_loaded": "Profilen '{profile}' er indlæst.",
    "warning_no_profile_delete": "Ingen profil",
    "warning_no_profile_delete_message": "Vælg en profil på listen for at slette.",
    "profile_not_found": "Profilen '{profile}' blev ikke fundet.",
    "profile_not_exist": "Profilen '{profile}' findes ikke.",
    "confirm_delete_title": "Bekræft sletning",
    "confirm_delete_profile": "Er du sikker på, at du vil slette profilen '{profile}'?",
    "profile_deleted_title": "Profil slettet",
    "profile_deleted": "Profilen '{profile}' er slettet.",

    # --- Files / Directories ---
    "msg_no_input_file": "Ingen inputfil",
    "msg_unsupported_format": "Ikke understøttet format",
    "select_file_title": "Vælg inputfil",
    "supported_files": "Understøttede filer",
    "all_files": "Alle filer",
    "select_dir_title": "Vælg outputmappe",
    "select_log_dir_title": "Vælg mappe til logfiler",
    "error_output_dir_title": "Fejl i outputmappe",
    "error_output_dir": "Den angivne outputmappe er ugyldig eller findes ikke:\n{directory}",
    "error_input_file_title": "Fejl i inputfil",
    "error_input_file": "Den angivne inputfil er ugyldig eller findes ikke:\n{file}",
    "save_file_error_title": "Fejl ved gemning af fil",
    "save_file_error": "Kunne ikke gemme fil: {error}",

    # --- PDF Processing / Preview ---
    "msg_pdf_processing_error": "Kunne ikke behandle PDF‑fil",
    "msg_thumbnail_error": "Fejl ved indlæsning af miniature",
    "msg_no_pdf_output": "Intet PDF‑output",
    "no_pdf_pages": "Ingen sider i PDF‑filen",
    "unsupported_output": "Ikke understøttet udgangstype for forhåndsvisning",
    "pdf_generated_title": "Generering fuldført",
    "pdf_generated": "PDF‑fil(er) er blevet genereret i mappen:\n{directory}",
    "pdf_generation_error_title": "Fejl ved generering",
    "pdf_generation_error": "Der opstod fejl under genereringen af PDF. Tjek loggene for flere oplysninger.",
    "critical_pdf_error_title": "Kritisk fejl ved PDF‑generering",
    "critical_pdf_error": "Der opstod en kritisk fejl under genereringen af PDF:\n{error}\nTjek loggene.",
    "settings_saved_title": "Indstillinger gemt",
    "settings_saved": "Indstillingerne er gemt i filen:\n{filepath}",
    "settings_save_error_title": "Fejl ved lagring af indstillinger",
    "settings_save_error": "Kunne ikke gemme indstillinger: {error}",
    "conversion_error_title": "Konverteringsfejl",
    "conversion_error": "Fejl ved konvertering af værdier fra GUI: {error}",
    "update_gui_error_title": "Fejl ved opdatering af GUI",
    "update_gui_error": "Der opstod en fejl under opdatering af grænsefladen: {error}",

    # --- License ---
    "hwid_copied_to_clipboard": "HWID er kopieret til udklipsholderen",
    "computer_hwid": "Computer HWID",
    "public_key_load_error": "Fejl ved indlæsning af offentlig nøgle: {error}",
    "invalid_license_format": "Ugyldigt format for licensnøgle: {error}",
    "activation_success": "Licensen er aktiveret.",
    "activation_error": "Fejl ved aktivering af licens: {error}",
    "log_trial_mode_active": "Prøvetilstand er aktiv",
    "log_trial_mode_inactive": "Prøvetilstand er inaktiv",

    # --- Initialization ---
    "init_error_title": "Initialiseringsfejl",
    "init_error": "Fejl ved initialisering af mapper: {error}",
    "poppler_path_info": "Information om Poppler‑sti",
    "ttkthemes_not_installed": "Advarsel: Biblioteket ttkthemes er ikke installeret. Standard‑Tkinter‑stil bruges.",

    # =====================================
    #  Logs (Logger Messages)
    # =====================================

    # --- General Logging / Configuration ---
    "log_configured": "Logning konfigureret: niveau={0}, tilstand={1}, fil={2}",
    "log_no_handlers": "Advarsel: Ingen lognings‑handlers konfigureret (tilstand: {0}).",
    "log_critical_error": "Kritisk fejl i logningskonfiguration: {0}",
    "log_basic_config": "Grundlæggende logningskonfiguration anvendt pga. fejl.",
    "log_dir_create_error": "Kritisk fejl: Kan ikke oprette logmappe {0}: {1}",

    # --- Logs - Initialization / Directories (`init_directories.py`) ---
    "error_critical_init": "KRITISK FEJL under initialisering: {0}",
    "logger_init_error": "Fejl ved initialisering af mapper: {error}",
    "directory_created": "Mappe oprettet: {0}",
    "directory_creation_error": "Kunne ikke oprette mappe {0}: {1}",
    "sample_file_copied": "Eksempelfil kopieret til {0}",
    "sample_file_copy_error": "Fejl ved kopiering af eksempelfil: {0}",
    "log_created_output_dir": "Outputmappe oprettet: {0}",
    "log_cannot_create_output_dir": "Kan ikke oprette outputmappe {0}: {1}",

    # --- Logs - Splitter (`splitter.py`) ---
    "log_graphic_settings_error": "Kunne ikke indlæse grafiske indstillinger under initialisering: {0}",
    "log_loading_pdf": "Indlæser PDF‑fil: {0}",
    "log_loading_bitmap": "Indlæser bitmapfil: {0}",
    "log_invalid_dpi": "Ugyldig DPI læst ({0}). Bruger standard {1} DPI.",
    "log_image_dimensions": "Billeddimensioner: {0}x{1}px, Tilstand: {2}, DPI: {3:.1f} -> {4:.3f}x{5:.3f}pt",
    "log_image_processing_color": "Behandler billede med oprindelig farvetilstand: {0}",
    "log_unusual_color_mode": "Usædvanlig farvetilstand: '{0}'. ReportLab/Pillow håndterer det muligvis ikke korrekt.",
    "log_draw_image_error": "Fejl under ReportLab drawImage for tilstand {0}: {1}",
    "log_unsupported_format": "Ikke understøttet inputfilformat: {0}",
    "log_input_file_not_found": "Inputfil ikke fundet: {0}",
    "log_load_process_error": "Fejl under indlæsning eller behandling af fil {0}: {1}",
    "log_input_file_not_exists": "Inputfilen findes ikke eller stien er tom: '{0}'",
    "log_cannot_load_or_empty_pdf": "Kunne ikke indlæse inputfil, eller PDF er tom/korrupt.",
    "log_pdf_dimensions_info": "  PDF‑dimensioner: {0:.1f}mm x {1:.1f}mm",
    "log_invalid_pdf_dimensions": "Ugyldige PDF‑sidedimensioner: {0}x{1} pt.",

    #   Splitter - Dimension Calculations
    "log_extra_margin": "Ekstra margin sat til {0:.3f} pt",
    "log_invalid_rows_cols": "Ugyldigt antal rækker ({0}) eller kolonner ({1}).",
    "error_invalid_rows_cols": "Rækker og kolonner skal være positive heltal.",
    "log_invalid_overlap_white_stripe": "Ugyldige værdier for overlap ({0}) eller hvid stribe ({1}). De skal være tal.",
    "error_invalid_overlap_white_stripe": "Overlap og hvid stribe skal være numeriske værdier (mm).",
    "log_stripe_usage": "Sæt use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Basis‑overlap (grafik): {0:.3f} mm, Hvid stribe: {1:.3f} mm, Effektivt overlap: {2:.3f} mm",
    "log_computed_dimensions": "Beregnet: PDF: {0:.3f}mm x {1:.3f}mm. Panel: {2:.3f}pt ({3:.3f}mm) x {4:.3f}pt ({5:.3f}mm). Kerne: {6:.3f}pt x {7:.3f}pt. Effektivt overlap: {8:.3f}mm",
    "log_invalid_dimensions": "Beregnet panel ({0:.3f}x{1:.3f}) eller kerne ({2:.3f}x{3:.3f}) er ugyldig for overlap={4}, stribe={5}, r={6}, c={7}, W={8}mm, H={9}mm",
    "error_invalid_slice_dimensions": "Beregnet panel/kerne dimensioner er ugyldige eller negative.",

    #   Splitter - Generating Panels Info and Order
    "log_generating_slice_info": "Genererer panelinfo: {0}",
    "log_no_slices_info_generated": "Kunne ikke generere panelinformation.",
    "log_applying_rotated_order": "Anvender rækkefølge for 180‑graders rotation: {0}",
    "log_applying_standard_order": "Anvender rækkefølge for 0‑graders rotation (standard): {0}",
    "log_unknown_bryt_order": "Ukendt rækkefølge af paneler: '{0}'. Bruger standard.",
    "log_final_slices_order": "  Endelig panelrækkefølge ({0}): [{1}]",

    #   Splitter - Creating Overlays and Merging
    "log_invalid_dimensions_overlay": "Forsøg på at oprette overlay med ugyldige dimensioner: {0}. Springer over.",
    "log_empty_overlay": "Oprettet et tomt eller næsten tomt overlay‑PDF. Springer over.",
    "log_overlay_error": "Fejl ved oprettelse af overlay‑PDF: {0}",
    "log_merge_error": "Forsøg på at flette overlay uden sider. Springer over.",
    "log_merge_page_error": "Fejl ved fletning af overlay‑PDF: {0}",
    "log_fallback_draw_rotating_elements": "Kunne ikke hente rækker/kolonner for _draw_rotating_elements, brugte 1x1.",
    "log_overlay_created_for_slice": "Oprettet striber/mærker overlay for panel {0}",
    "log_overlay_creation_failed_for_slice": "Kunne ikke oprette striber/mærker overlay for {0}",
    "log_merging_rotated_overlay": "Fletter ROTERET overlay for {0} med T={1}",
    "log_merging_nonrotated_overlay": "Fletter IKKE‑roteret overlay for {0}",
    "log_merging_all_codes_overlay": "Fletter overlay for alle koder (uden rotation)",
    "log_merging_separation_lines_overlay": "Fletter overlay for separationslinjer (uden rotation)",
    "log_merging_code_overlay_for_slice": "Kode‑overlay for {0} flettet uden rotation.",
    "log_merging_separation_overlay_for_slice": "Separationslinje‑overlay for {0} flettet uden rotation.",

    #   Splitter - Drawing Graphic Elements (Stripes, Marks, Lines)
    "log_drawing_top_stripe": "[Canvas] Tegner øverste stribe for {0}: x={1:.3f}, y={2:.3f}, b={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Tegner højre stribe for {0}: x={1:.3f}, y={2:.3f}, b={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Fylder og optegner hjørne for {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Tegner centreret kryds ved ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Tegner registerlinjer for {0} i område fra ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Tegner højre lodrette linje: x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  Tegner øverste vandrette linje: y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "Tegner separationslinje (hvid på sort): ({0}) @ ({1:.3f}, {2:.3f}), len={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Tegner krydser for {0} [{1},{2}] / [{3},{4}] i område fra ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Beregnede centre: ØV({0:.1f},{1:.1f}), ØH({2:.1f},{3:.1f}), NV({4:.1f},{5:.1f}), NH({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Tegner ØV @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Tegner ØH @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Tegner NV @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Tegner NH @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Udelod {0} i henhold til regel for position [{1},{2}]",
    "log_trial_common_sheet": "Anvender TRIAL vandmærketekst på fælles ark",

    # Watermark
    "log_trial_watermark_added": "TRIAL vandmærke er tilføjet",
    "error_drawing_trial_text": "Fejl ved tegning af vandmærke: {error}",

    #   Splitter - Drawing Separation Lines (Whole Page)
    "log_drawing_separation_lines_for_page": "Tegner separationslinjer for side (layout={0}, total_panels={1}, panel_index={2})",
    "log_vertical_line_between_slices": "  Lodret linje mellem paneler {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Lodret linje start @ x={0:.1f}",
    "log_vertical_line_end": "  Lodret linje slut @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Vandret linje mellem paneler {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Vandret linje start @ y={0:.1f}",
    "log_horizontal_line_end": "  Vandret linje slut @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Separate filer) Lodret/Vandret linje start @ {0:.1f}",
    "log_sep_line_end_separate": "  (Separate filer) Lodret/Vandret linje slut @ {0:.1f}",

    #   Splitter - Generating Barcodes / QR
    "log_generate_barcode_data": "Genererer kodedata: {0}",
    "log_barcode_data_shortened": "Kodedata afkortet til {0} tegn.",
    "log_barcode_data_error": "Fejl ved generering af kodedata: {0}",
    "log_compose_barcode_payload": "Sammensætter kode‑payload ({0}): {1}",
    "log_barcode_payload_shortened": "Payload afkortet til {0} tegn for format {1}",
    "log_barcode_payload_error": "Fejl ved sammensætning af payload: {0}",
    "log_unknown_anchor_fallback": "Ukendt anker '{0}', bruger nederst‑venstre",
    "log_used_default_code_settings": "Brugte 'default' indstillinger for kode {0}/{1}.",
    "log_no_layout_key_fallback": "Ingen layout '{0}' for {1}/{2}. Brugte den første tilgængelige: '{3}'.",
    "log_code_settings_error": "Ikke fundet eller fejl ved hentning af kodeindstillinger ({0}/{1}/{2}): {3}. Bruger standard.",
    "log_drawing_barcode": "Tegner {0} ved ({1:.3f}, {2:.3f}) [basis ({3:.3f}, {4:.3f}) + forskydning ({5:.3f}, {6:.3f})], rotation: {7}°",
    "error_generate_qr_svg": "Kunne ikke generere QR‑kode SVG.",
    "error_invalid_scale_for_qr": "Ugyldig skala for QR: {0}mm",
    "error_invalid_qr_scale_factor": "Ugyldig skalafaktor for QR: {0}",
    "error_generate_barcode_svg": "Kunne ikke generere stregkode‑SVG.",
    "error_invalid_scale_for_barcode": "Ugyldig skala for stregkode: {0}x{1}mm",
    "error_invalid_barcode_scale_factor": "Ugyldig skalafaktor for stregkode: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: skalakonfig={1:.3f}mm, SVG‑bredde={2:.3f}pt, sf={3:.4f}",
    "log_barcode_scale_code128": "  {0}: skalakonfig=({1:.3f}mm, {2:.3f}mm), SVG‑størrelse=({3:.3f}pt, {4:.3f}pt), sf=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Fejl ved tegning af kode '{0}': {1}",
    "log_prepared_barcode_info": "Forberedte kodeoplysninger for {0} ({1}, anker={2}): basis absolut position ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Fejl ved forberedelse af kodedata for {0}: {1}",
    "log_drawing_barcodes_count": "Tegner {0} stregkoder/QR‑koder...",
    "log_missing_barcode_info_key": "Manglende nøgle i kodedata under tegning: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Fejl ved tegning af kode '{0}' i _draw_all_barcodes: {1}",

    #   Splitter - Splitting Process (split_* methods)
    "log_start_splitting_process": "--- Starter splitproces for: {0} ---",
    "log_split_settings": "  Indstillinger: {0}x{1} paneler, Overlap={2}mm, Hvid stribe={3}mm (+overlap: {4})",
    "log_output_dir_info": "  Output: {0} / {1} til '{2}'",
    "log_lines_marks_barcodes_info": "  Linjer: Separation={0}, Start={1}, Slut={2} | Mærker: {3} ({4}), Koder: {5} ({6})",
    "log_bryt_order_info": "  Rækkefølge: {0}, Panelrotation: {1}°",
    "log_invalid_dimensions_in_slice_info": "Ugyldige dimensioner i slice_info for {0}: {1}x{2}",
    "log_content_transform": "Indholdstransformation T_content for {0}: {1}",
    "log_merged_content_for_slice": "Flettede indhold for panel {0} på new_page",
    "log_slice_reader_created": "Oprettede komplet panel (PdfReader) for {0}",
    "log_slice_reader_creation_error": "Fejl ved oprettelse af komplet panel for {0}: {1}",
    "log_used_get_transform": "Brugte _get_transform (kun translation): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Starter: SEPARATE FILER (Rotation håndteres i create_slice_reader) ---",
    "log_creating_file_for_slice": "Opretter fil for panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Ugyldig sidestørrelse ({0}x{1}) for {2}. Springer over.",
    "log_blank_page_creation_error": "Fejl ved oprettelse af side for {0} (størrelse {1}x{2}): {3}. Springer over.",
    "log_transform_for_slice": "Transformation T (kun translation) for {0}: {1}",
    "log_merging_complete_slice": "Fletter komplet panel {0} med transformation: {1}",
    "log_skipped_slice_merging": "Sprang fletning af komplet panel for {0} over.",
    "log_file_saved": "Fil gemt: {0}",
    "log_file_save_error": "Fejl ved gemning af fil {0}: {1}",
    "log_finished_split_separate_files": "--- Færdig: SEPARATE FILER (Gemt {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Ingen paneler at behandle i split_horizontal.",
    "log_start_split_horizontal": "--- Starter: FÆLLES ARK - VANDRET (Rotation håndteres i create_slice_reader) ---",
    "log_page_dimensions": "Sidedimensioner: {0:.1f}mm x {1:.1f}mm ({2} paneler)",
    "log_page_creation_error": "Fejl ved oprettelse af resultatside ({0}x{1}): {2}. Afbryder.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformation T (kun translation) for {0}: {1}",
    "log_merging_complete_bryt": "Fletter komplet panel {0} med transformation: {1}",
    "log_skipped_merging_bryt": "Sprang fletning af komplet panel over for {0}.",
    "log_file_result_saved": "Resultatfil gemt: {0}",
    "log_file_result_save_error": "Fejl ved gemning af resultatfil {0}: {1}",
    "log_finished_split_horizontal": "--- Færdig: FÆLLES ARK - VANDRET ---",
    "log_no_slices_split_vertical": "Ingen paneler at behandle i split_vertical.",
    "log_start_split_vertical": "--- Starter: FÆLLES ARK - LODRET (Rotation håndteres i create_slice_reader) ---",
    "log_finished_split_vertical": "--- Færdig: FÆLLES ARK - LODRET ---",
    "log_unknown_layout": "Ukendt layout for fælles ark: '{0}'.",
    "log_unknown_output_type": "Ukendt outputtype: '{0}'.",
    "log_finished_splitting_success": "--- Færdig splitproces for: {0} - SUCCESS ---",
    "log_finished_splitting_errors": "--- Færdig splitproces for: {0} - FEJL OPSTOD ---",
    "log_value_error_in_splitting": "Inputdata eller beregningsfejl: {0}",
    "log_finished_splitting_critical_error": "--- Færdig splitproces for: {0} - KRITISK FEJL ---",
    "log_unexpected_error_in_splitting": "Uventet fejl under opdeling af fil {0}: {1}",

    #   Splitter - Test Mode (__main__)
    "log_script_mode_test": "splitter.py startet som hovedscript (testtilstand).",
    "log_loaded_config": "Konfiguration indlæst.",
    "log_error_loading_config": "Kunne ikke indlæse konfiguration: {0}",
    "log_created_example_pdf": "Oprettet eksempel‑PDF: {0}",
    "log_cannot_create_example_pdf": "Kunne ikke oprette eksempel‑PDF: {0}",
    "log_start_test_split": "Starter testopdeling af fil: {0} til {1}",
    "log_test_split_success": "Testopdeling fuldført med succes.",
    "log_test_split_errors": "Testopdeling afsluttet med fejl.",

    # --- Logs - QR/Barcode (`barcode_qr.py`) ---
    "log_qr_empty_data": "Forsøg på at generere QR‑kode for tomme data.",
    "log_qr_generated": "QR‑kode SVG genereret for: {0}...",
    "log_qr_error": "Fejl ved generering af QR‑kode for data '{0}': {1}",
    "log_barcode_empty_data": "Forsøg på at generere stregkode for tomme data.",
    "log_barcode_generated": "Stregkode‑SVG genereret for: {0}...",
    "log_barcode_error": "Fejl ved generering af stregkode for data '{0}': {1}",
    "log_basic_handler_configured": "Grundlæggende handler konfigureret for logger i barcode_qr.py",
    "log_basic_handler_error": "Kunne ikke konfigurere grundlæggende logger‑handler i barcode_qr: {0}",

    # --- Logs - Config/Profiles (`main_config_manager.py`) ---
    "loading_profiles_from": "Indlæser profiler fra",
    "profiles_file": "Profilfil",
    "does_not_contain_dict": "indeholder ikke en ordbog. Opretter en ny",
    "not_found_creating_new": "ikke fundet. Opretter en ny tom",
    "json_profiles_read_error": "Fejl ved læsning af JSON‑profilfil",
    "file_will_be_overwritten": "Filen vil blive overskrevet ved lagring",
    "json_decode_error_in_profiles": "JSON‑decode‑fejl i profilfil",
    "cannot_load_profiles_file": "Kan ikke indlæse profilfil",
    "unexpected_profiles_read_error": "Uventet fejl ved læsning af profiler",
    "saving_profiles_to": "Gemmer profiler til",
    "cannot_save_profiles_file": "Kan ikke gemme profilfil",
    "profiles_save_error": "Fejl ved lagring af profiler til fil",
    "logger_profile_saved": "Profil gemt: {profile}",
    "logger_profile_not_found": "Profil ikke fundet til indlæsning: {profile}",
    "logger_profile_loaded": "Profil indlæst: {profile}",
    "logger_profile_delete_not_exist": "Forsøg på at slette ikke‑eksisterende profil: {profile}",
    "logger_profile_deleted": "Profil slettet: {profile}",
    "logger_start_save_settings": "Startede lagring af indstillinger fra GUI.",
    "logger_invalid_value": "Ugyldig værdi for '{key}'. Sat til 0.0.",
    "logger_end_save_settings": "Færdig med at gemme indstillinger fra GUI.",
    "logger_conversion_error": "Fejl ved konvertering af værdier fra GUI: {error}",
    "conversion_failed": "Konvertering af GUI‑værdier mislykkedes",
    "logger_unexpected_save_error": "Uventet fejl ved lagring af indstillinger: {error}",
    "logger_settings_saved": "Indstillinger gemt til fil: {file}",

    # --- Logs - Licensing (`main_license.py`) ---
    "public_key_load_error_log": "Fejl ved indlæsning af offentlig nøgle",
    "license_key_decode_error": "Fejl ved dekodning af licensnøgle",
    "license_activation_error": "Fejl ved aktivering af licens",

    # --- Logs - Main Module (`main.py`) ---
    "ui_created": "Brugerfladen er oprettet.",
    "error_tab_home": "Fejl ved oprettelse af 'Hjem'‑fanen",
    "error_tab_settings": "Fejl ved oprettelse af 'Indstillinger'‑fanen",
    "error_tab_help": "Fejl ved oprettelse af 'Hjælp'‑fanen",
    "error_creating_license_ui": "Fejl ved oprettelse af 'Licens'‑fanen",
    "error_loading_ui": "Fejl ved indlæsning af grænseflade: {error}",
    "error_creating_home_ui": "Fejl ved oprettelse af 'Hjem'‑fanen",
    "error_creating_settings_ui": "Fejl ved oprettelse af 'Indstillinger'‑fanen",
    "error_creating_help_ui": "Fejl ved oprettelse af 'Hjælp'‑fanen",
    "logger_update_gui": "Startede opdatering af GUI fra konfiguration.",
    "logger_end_update_gui": "Afsluttede opdatering af GUI fra konfiguration.",
    "logger_update_gui_error": "Uventet fejl ved opdatering af GUI: {error}",
    "logger_invalid_output_dir": "Ugyldig eller ikke‑eksisterende outputmappe: {directory}",
    "logger_invalid_input_file": "Ugyldig eller ikke‑eksisterende inputfil: {file}",
    "logger_start_pdf": "Startede PDF‑genereringsproces.",
    "logger_pdf_save_error": "PDF‑generering afbrudt – kunne ikke gemme aktuelle indstillinger.",
    "logger_pdf_success": "PDF‑generering fuldført.",
    "logger_pdf_exception": "Undtagelse under hoved‑PDF‑genereringsproces.",
    "icon_set_error": "Kunne ikke sætte programikon: {error}",
    "accent_button_style_error": "Kunne ikke sætte stil for accent‑knap: {error}",
    "logger_file_save_error": "Fejl ved gemning af fil {file}: {error}",

    #   Logs - Preview (`main.py` - update_preview, update_output_preview)
    "thumbnail_error_log": "Fejl ved generering af miniature",
    "output_preview_update_called": "Opdatering af outputforhåndsvisning kaldt",
    "output_preview_canvas_missing": "Canvas til outputforhåndsvisning mangler",
    "pdf_found_in_output_dir": "PDF fundet i outputmappe",
    "preparing_thumbnail": "Forbereder miniature",
    "thumbnail_generated_successfully": "Miniature genereret korrekt",
    "thumbnail_generation_error": "Fejl ved generering af miniature for",
    "no_pdf_for_common_sheet": "Ingen PDF‑fil til forhåndsvisning af fælles ark",
    "no_pdf_for_separate_files": "Ingen genererede separate PDF‑filer til forhåndsvisning",
    "cannot_load_thumbnail": "Kan ikke indlæse miniature fra",

    #   Logs - Developer / GUI internals (`main.py`)
    "missing_gui_var_created": "Oprettede manglende GUI‑variabel for nøgle: {key}",
    "missing_gui_structure_created": "Oprettede manglende GUI‑struktur for: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Oprettede manglende GUI‑variabel for: {code_type}/{output_type}/{layout}/{param}",

    # Additional keys for main_ui_help.py
    "help_text": """
    Billboard Splitter – Brugervejledning\n\n
    Formål med programmet:\n
    Billboard Splitter bruges til automatisk at skære billboard‑projekter i trykklare paneler.
    Programmet er forberedt til arbejde med filer designet i skala 1:10.\n
    Værdier i sektionerne: Overlap, Hvid stribe, Indstillinger angives i skala 1:1.
    Programmet gør det muligt at placere de udskårne paneler på PDF‑ark afhængigt af valgt layout:\n
    • Fælles ark: Alle paneler placeres i ét dokument.\n
    • Separate filer: Hvert panel gemmes i en separat PDF‑fil.\n\n
    Derudover muliggør programmet:\n
    • Valg af layout – lodret eller vandret (henholdsvis: i det lodrette layout vises separationslinjer øverst og nederst,
      og i det vandrette layout på venstre og højre side).\n
    • Rotation af paneler med 180° (vending af hele projektet).\n
    • Tilføjelse af registermærker (f.eks. kryds eller linjer) for at lette præcis positionering under samling.\n
    • Tilføjelse af QR‑koder eller stregkoder – genereret baseret på inputdata for at hjælpe
      med at identificere individuelle paneler.\n
    • Gemme indstillinger som profiler, der kan indlæses, ændres og slettes, hvilket gør det nemt at
      skifte mellem forskellige projektkonfigurationer.\n\n
    Hovedtrin for brug af programmet:\n\n
    1. Vælg inputfil:\n
    • I fanen 'Hjem' vælg en PDF, JPG eller TIFF med billboard‑designet.\n
    • Hvis du ikke angiver din egen sti, sætter programmet en eksempelfil som standard.\n\n
    2. Indstillinger for opdeling:\n
    • Angiv antal rækker og kolonner, som projektet skal opdeles i.\n
    • Indstil størrelsen på overlap.\n
    • Angiv eventuelt bredden på den hvide stribe, som lægges til det effektive overlap.\n\n
    3. Vælg udgangslayout:\n
    • Lodret: Alle paneler placeres på et PDF‑ark lodret.\n
    • Vandret: Alle paneler placeres på et PDF‑ark vandret.\n\n
    4. Vælg udgangstype:\n
    • Fælles ark: Alle paneler placeres på ét fælles PDF‑ark.\n
    • Separate filer: Hvert panel gemmes i en separat PDF‑fil.\n
    • I fanen 'Hjem' kan du aktivere og konfigurere registermærker – vælg mellem kryds og linje.\n
    • Aktiver eventuelt en QR‑kode eller stregkode, som genereres ud fra projektdata.\n
    • Kodeparametre (skalering, forskydning, rotation, position) kan finjusteres i fanen 'Indstillinger'.\n\n
    5. Håndtering af indstillinger:\n
    • I fanen 'Indstillinger' kan du præcist ændre grafiske parametre (margener, linjetykkelser, mellemrum) og
      kodeindstillinger.\n
    • Gem de aktuelle indstillinger som en profil, så du let kan indlæse eller ændre dem senere.\n
    • Indstillingsprofiler (gemt i filen profiles.json) gør det nemt hurtigt at skifte mellem forskellige\n
      projektkonfigurationer.\n\n
    6. Generering af PDF:\n
    • Klik 'Generér PDF', når alle parametre er konfigureret.\n
    • Resultatfiler gemmes i mappen 'output' eller en anden angivet, og logs (med daglig rotation) i mappen 'logs'\n
      eller en anden angivet.\n\n
    Hvis der opstår problemer:\n
    • Tjek loggene i mappen 'logs'. Hver dag oprettes en separat logfil med dato i navnet.\n
    • Sørg for, at alle nødvendige mapper er sat.\n
    • Teknisk support: tech@printworks.pl (hverdage, 8‑16)\n
    """
}
