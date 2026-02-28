# lang_hr.py
"""
Datoteka s prijevodima za hrvatski jezik.
"""

LANG = {
    "barcode_font_size_label": "Veličina fonta opisa crtičnog koda [pt]:",
    # ==========================
    #  Aplikacija – Općenito
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Pogreška",
    "no_file": "Nema datoteke",
    "language": "Jezik",
    "language_switch": "Promjena jezika",
    "choose_language": "Odaberite jezik:",
    "apply_language": "Primijeni",
    "language_changed": "Jezik je promijenjen. Dio promjena bit će vidljiv tek nakon ponovnog pokretanja aplikacije.",

    # ========================================
    #  Grafičko sučelje (GUI)
    # ========================================

    # --- Glavne kartice ---
    "tab_home": " Početna ",
    "tab_settings": " Postavke ",
    "tab_help": " Pomoć ",
    "tab_license": " Licenca ",

    # --- Opći gumbi ---
    "button_browse": "Pregledaj...",
    "browse_folder": "Pregledaj mapu...",
    "button_save": "Spremi",
    "button_delete": "Izbriši",
    "button_close": "Zatvori",
    "save_all_settings": "Spremi sve postavke",

    # --- Oznake polja (Početna) ---
    "label_rows": "Okomito dijeljenje (redovi):",
    "label_columns": "Vodoravno dijeljenje (stupci):",
    "label_overlap": "Preklop [mm]:",
    "label_white_stripe": "Bijela traka [mm]:",
    "label_add_white_stripe": "Dodaj bijelu traku efektivnom preklopu",
    "label_layout": "Raspored izlaza:",
    "label_output_type": "Vrsta izlaza:",
    "label_enable_reg_marks": "Uključi registracijske oznake:",
    "label_enable_codes": "Uključi kodove:",
    "label_enable_sep_lines": "Uključi razdjelne linije (između panela)",
    "label_enable_start_line": "Uključi liniju početka/gornjeg ruba lista",
    "label_enable_end_line": "Uključi liniju kraja/donjeg ruba lista",
    "label_bryt_order": "Redoslijed panela:",
    "label_slice_rotation": "Rotacija panela:",
    "label_create_order_folder": "Kreiraj mapu s brojem narudžbe",

    # --- Sekcije (Početna) ---
    "section_input_file": " Ulazna datoteka ",
    "section_scale_and_dimensions": " Mjerilo i izlazne dimenzije ",
    "label_original_size": "Originalna veličina:",
    "label_scale_non_uniform": "Neproporcionalno skaliranje",
    "label_scale": "Mjerilo: 1:",
    "label_scale_x": "Mjerilo X: 1:",
    "label_scale_y": "Mjerilo Y: 1:",
    "label_output_dimensions": "Dimenzije izlazne datoteke:",
    "label_width_cm": "Širina [cm]:",
    "label_height_cm": "Visina [cm]:",
    "section_split_settings": " Postavke rezanja ",
    "section_profiles": " Profili postavki ",
    "section_save_location": " Mjesto spremanja ",
    "section_input_preview": " Pregled ulaza ",
    "section_output_preview": " Pregled izlaza ",

    # --- Vrijednosti opcija ---
    "layout_vertical": "Okomito",
    "layout_horizontal": "Vodoravno",
    "output_common_sheet": "Zajednički list",
    "output_separate_files": "Odvojene datoteke",
    "output_both": "Zajednički list i odvojene datoteke",
    "output_common": "Zajednički list",
    "output_separate": "Odvojene datoteke",
    "reg_mark_cross": "Križ",
    "reg_mark_line": "Linija",
    "code_qr": "QR kod",
    "code_barcode": "Barkod",
    "bryt_order_1": "A1–An, B1–Bn, .. Standardno, odozgo",
    "bryt_order_2": "A1–An, Bn–B1, .. Zmijasto po redovima, odozgo",
    "bryt_order_3": "A1..B1, A2..B2, .. Po stupcima, odozgo",
    "bryt_order_4": "A1–A2..B2–B1.. Zmijasto po stupcima, odozgo",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Standardno, odozdo",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Zmijasto po redovima, odozdo",
    "logging_console": "konzola",
    "logging_file": "datoteka",
    "logging_both": "oboje",

    # --- Sekcije (Postavke) ---
    "section_processing_mode": " Načini obrade ",
    "processing_mode_ram": "RAM (u memoriji)",
    "processing_mode_hdd": "Disk (na pohrani)",
    "graphic_settings": "Grafičke postavke",
    "code_settings": "Postavke QR/barkoda",
    "logging_settings": "Postavke zapisnika (logova)",
    "barcode_text_position_label": "Položaj natpisa uz kod:",
    "barcode_text_bottom": "dolje",
    "barcode_text_side": "sa strane",
    "barcode_text_none": "bez",

    # --- Oznake (Postavke – Grafika) ---
    "extra_margin_label": "Margina oko panela [mm]:",
    "margin_top_label": "Gornja margina [mm]:",
    "margin_bottom_label": "Donja margina [mm]:",
    "margin_left_label": "Lijeva margina [mm]:",
    "margin_right_label": "Desna margina [mm]:",
    "reg_mark_width_label": "Registracijska oznaka – širina [mm]:",
    "reg_mark_height_label": "Registracijska oznaka – visina [mm]:",
    "reg_mark_white_line_width_label": "Registracijska oznaka – debljina bijele linije [mm]:",
    "reg_mark_black_line_width_label": "Registracijska oznaka – debljina crne linije [mm]:",
    "sep_line_black_width_label": "Razdjelna – debljina crne linije [mm]:",
    "sep_line_white_width_label": "Razdjelna – debljina bijele linije [mm]:",
    "slice_gap_label": "Razmak između panela [mm]:",
    "label_draw_slice_border": "Crtaj okvir oko panela (linija reza)",

    # --- Oznake (Postavke – Kodovi) ---
    "scale_label": "Veličina [mm]:",
    "scale_x_label": "Širina X [mm]:",
    "scale_y_label": "Visina Y [mm]:",
    "offset_x_label": "Pomak X [mm]:",
    "offset_y_label": "Pomak Y [mm]:",
    "rotation_label": "Rotacija (°):",
    "anchor_label": "Kut:",

    # --- Oznake (Postavke – Logovi) ---
    "logging_mode_label": "Način zapisivanja:",
    "log_file_label": "Datoteka zapisnika:",
    "logging_level_label": "Razina zapisivanja:",

    # --- Gumbi / radnje (Početna) ---
    "button_load": "Učitaj",
    "button_save_settings": "Spremi trenutačne postavke",
    "button_generate_pdf": "Generiraj PDF",
    "button_refresh_preview": "Osvježi pregled",
    "button_refresh_layout": "Osvježi raspored",

    # --- Licenca (GUI) ---
    "hwid_frame_title": "Jedinstveni identifikator hardvera (HWID)",
    "copy_hwid": "Kopiraj HWID",
    "license_frame_title": "Aktivacija licence",
    "enter_license_key": "Unesite licencni ključ:",
    "activate": "Aktiviraj",
    "status_trial": "Probni način",
    "license_active": "Licenca je aktivna",

    # ================================================
    #  Poruke korisniku (prozorčići, statusna traka)
    # ================================================

    # --- Profili ---
    "msg_no_profile_name": "Bez naziva",
    "msg_enter_profile_name": "Unesite naziv profila za spremanje.",
    "msg_profile_saved": "Profil spremljen",
    "profile_saved_title": "Profil spremljen",
    "msg_profile_saved_detail": "Profil „{0}” je spremljen.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profil '{profile}' je spremljen i primijenjen.",
    "msg_no_profile": "Nema profila",
    "warning_no_profile": "Nema profila",
    "msg_select_profile": "Odaberite naziv profila s popisa za učitavanje.",
    "select_profile": "Odaberite naziv profila s popisa za učitavanje.",
    "profile_loaded_title": "Profil učitan",
    "profile_loaded": "Profil „{profile}” je učitan.",
    "warning_no_profile_delete": "Nema profila",
    "warning_no_profile_delete_message": "Odaberite profil s popisa za brisanje.",
    "profile_not_found": "Profil „{profile}” nije pronađen.",
    "profile_not_exist": "Profil „{profile}” ne postoji.",
    "confirm_delete_title": "Potvrdite brisanje",
    "confirm_delete_profile": "Zaista želite izbrisati profil „{profile}”?",
    "profile_deleted_title": "Profil izbrisan",
    "profile_deleted": "Profil „{profile}” je izbrisan.",

    # --- Datoteke / direktoriji ---
    "msg_no_input_file": "Nema ulazne datoteke",
    "msg_unsupported_format": "Nepodržani format",
    "select_file_title": "Odabir ulazne datoteke",
    "supported_files": "Podržane datoteke",
    "all_files": "Sve datoteke",
    "select_dir_title": "Odabir izlazne mape",
    "select_log_dir_title": "Odabir mape za logove",
    "error_output_dir_title": "Pogreška izlazne mape",
    "error_output_dir": "Navedena izlazna mapa je neispravna ili ne postoji:\n{directory}",
    "error_input_file_title": "Pogreška ulazne datoteke",
    "error_input_file": "Navedena ulazna datoteka je neispravna ili ne postoji:\n{file}",
    "save_file_error_title": "Pogreška spremanja datoteke",
    "save_file_error": "Datoteku nije moguće spremiti: {error}",

    # --- Obrada PDF-a / pregled ---
    "msg_pdf_processing_error": "Neuspjela obrada PDF datoteke",
    "msg_thumbnail_error": "Pogreška pri učitavanju minijature",
    "msg_no_pdf_output": "Nema PDF izlaza",
    "no_pdf_pages": "PDF ne sadrži stranice",
    "unsupported_output": "Nepodržana vrsta izlaza za pregled",
    "pdf_generated_title": "Generiranje završeno",
    "pdf_generated": "PDF datoteka(e) uspješno generirane u mapu:\n{directory}",
    "pdf_generation_error_title": "Pogreška generiranja",
    "pdf_generation_error": "Tijekom generiranja PDF-a došlo je do pogrešaka. Provjerite logove.",
    "critical_pdf_error_title": "Kritična pogreška generiranja PDF-a",
    "critical_pdf_error": "Došlo je do kritične pogreške pri generiranju PDF-a:\n{error}\nVidi zapisnike.",
    "settings_saved_title": "Postavke spremljene",
    "settings_saved": "Postavke su spremljene u datoteku:\n{filepath}",
    "settings_save_error_title": "Pogreška spremanja postavki",
    "settings_save_error": "Nije moguće spremiti postavke: {error}",
    "conversion_error_title": "Pogreška pretvorbe",
    "conversion_error": "Pogreška pri pretvorbi vrijednosti iz sučelja: {error}",
    "update_gui_error_title": "Pogreška ažuriranja sučelja",
    "update_gui_error": "Došlo je do pogreške pri ažuriranju sučelja: {error}",

    # --- Licenca ---
    "hwid_copied_to_clipboard": "HWID kopiran u međuspremnik",
    "computer_hwid": "HWID računala",
    "public_key_load_error": "Pogreška učitavanja javnog ključa: {error}",
    "invalid_license_format": "Neispravan format licencnog ključa: {error}",
    "activation_success": "Licenca je uspješno aktivirana.",
    "activation_error": "Pogreška aktivacije licence: {error}",
    "log_trial_mode_active": "Probni način je aktivan",
    "log_trial_mode_inactive": "Probni način nije aktivan",

    # --- Inicijalizacija ---
    "init_error_title": "Pogreška inicijalizacije",
    "init_error": "Pogreška inicijalizacije direktorija: {error}",
    "poppler_path_info": "Informacije o putanji Popplera",
    "ttkthemes_not_installed": "Napomena: knjižnica ttkthemes nije instalirana. Koristit će se zadani stil Tkintera.",

    # =====================================
    #  Logovi (poruke zapisnika)
    # =====================================

    # --- Općenito / Konfiguracija ---
    "log_configured": "Zapisivanje konfigurirano: razina={0}, način={1}, datoteka={2}",
    "log_no_handlers": "Upozorenje: rukovatelji zapisnika nisu konfigurirani (način: {0}).",
    "log_critical_error": "Kritična pogreška konfiguracije zapisivanja: {0}",
    "log_basic_config": "Zbog pogreške korištena je osnovna konfiguracija zapisivanja.",
    "log_dir_create_error": "Kritična pogreška: nije moguće stvoriti mapu logova {0}: {1}",

    # --- Logovi – Inicijalizacija / Direktoriji (init_directories.py) ---
    "error_critical_init": "KRITIČNA POGREŠKA tijekom inicijalizacije: {0}",
    "logger_init_error": "Pogreška inicijalizacije direktorija: {error}",
    "directory_created": "Direktorij stvoren: {0}",
    "directory_creation_error": "Nije moguće stvoriti direktorij {0}: {1}",
    "sample_file_copied": "Primjer datoteka kopirana u {0}",
    "sample_file_copy_error": "Pogreška kopiranja primjer datoteke: {0}",
    "log_created_output_dir": "Kreirana izlazna mapa: {0}",
    "log_cannot_create_output_dir": "Nije moguće stvoriti izlaznu mapu {0}: {1}",

    # --- Logovi – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Neuspjelo učitavanje grafičkih postavki pri inicijalizaciji: {0}",
    "log_loading_pdf": "Učitavanje PDF datoteke: {0}",
    "log_loading_bitmap": "Učitavanje rasterske datoteke: {0}",
    "log_invalid_dpi": "Učitano nevaljano DPI ({0}). Koristi se zadano {1} DPI.",
    "log_image_dimensions": "Dimenzije slike: {0}×{1}px, mod: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Obrada slike u izvornom kolor modu: {0}",
    "log_unusual_color_mode": "Neuobičajen kolor mod: „{0}”. ReportLab/Pillow možda neće ispravno raditi.",
    "log_draw_image_error": "Pogreška ReportLab drawImage za mod {0}: {1}",
    "log_unsupported_format": "Nepodržani ulazni format: {0}",
    "log_input_file_not_found": "Ulazna datoteka nije pronađena: {0}",
    "log_load_process_error": "Pogreška pri učitavanju ili obradi datoteke {0}: {1}",
    "log_input_file_not_exists": "Ulazna datoteka ne postoji ili je putanja prazna: „{0}”",
    "log_cannot_load_or_empty_pdf": "Nije moguće učitati ulaznu datoteku ili je PDF prazan/oštećen.",
    "log_pdf_dimensions_info": "  Dimenzije PDF-a: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Nevaljane dimenzije PDF stranice: {0}×{1} pt.",

    #   Splitter – Izračuni dimenzija
    "log_extra_margin": "Dodatna margina postavljena na {0:.3f} pt",
    "log_invalid_rows_cols": "Nevaljan broj redova ({0}) ili stupaca ({1}).",
    "error_invalid_rows_cols": "Redovi i stupci moraju biti pozitivni cijeli brojevi.",
    "log_invalid_overlap_white_stripe": "Nevaljane vrijednosti preklopa ({0}) ili bijele trake ({1}). Moraju biti numeričke.",
    "error_invalid_overlap_white_stripe": "Preklop i bijela traka moraju biti numeričke vrijednosti (mm).",
    "log_stripe_usage": "Postavljeno use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Osnovni preklop (grafika): {0:.3f} mm, bijela traka: {1:.3f} mm, efektivni preklop: {2:.3f} mm",
    "log_computed_dimensions": "Izračunato: PDF {0:.3f}×{1:.3f} mm. Panel: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Jezgra: {6:.3f}×{7:.3f} pt. Efekt. preklop: {8:.3f} mm",
    "log_invalid_dimensions": "Nevaljane dimenzije panela ({0:.3f}×{1:.3f}) ili jezgre ({2:.3f}×{3:.3f}) pri per={4}, stripe={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Izračunate dimenzije panela/jezgre su nevaljane ili negativne.",

    #   Splitter – Generiranje info i redoslijeda
    "log_generating_slice_info": "Generiranje informacija o panelu: {0}",
    "log_no_slices_info_generated": "Nije moguće generirati informacije o panelima.",
    "log_applying_rotated_order": "Primjena redoslijeda za rotaciju 180°: {0}",
    "log_applying_standard_order": "Primjena redoslijeda za 0° (standardno): {0}",
    "log_unknown_bryt_order": "Nepoznat redoslijed panela: „{0}”. Koristi se zadani.",
    "log_final_slices_order": "  Konačni redoslijed panela ({0}): [{1}]",

    #   Splitter – Preklapanja (overlay) i spajanje
    "log_invalid_dimensions_overlay": "Pokušaj izrade overlay-a s nevaljanim dimenzijama: {0}. Preskačem.",
    "log_empty_overlay": "Stvoren prazan ili gotovo prazan overlay PDF. Spajanje preskočeno.",
    "log_overlay_error": "Pogreška izrade overlay PDF-a: {0}",
    "log_merge_error": "Pokušaj spajanja overlay-a bez stranica. Preskačem.",
    "log_merge_page_error": "Pogreška spajanja overlay PDF-a: {0}",
    "log_fallback_draw_rotating_elements": "Nije moguće dobiti redove/stupce za _draw_rotating_elements, korišteno 1×1.",
    "log_overlay_created_for_slice": "Overlay traka/oznaka stvoren za panel {0}",
    "log_overlay_creation_failed_for_slice": "Neuspjelo stvaranje overlay-a za {0}",
    "log_merging_rotated_overlay": "Spajanje ROTIRANOG overlay-a za {0} s T={1}",
    "log_merging_nonrotated_overlay": "Spajanje NEROTIRANOG overlay-a za {0}",
    "log_merging_all_codes_overlay": "Spajanje overlay-a svih kodova (bez rotacije)",
    "log_merging_separation_lines_overlay": "Spajanje overlay-a razdj. linija (bez rotacije)",
    "log_merging_code_overlay_for_slice": "Overlay koda za {0} spojen bez rotacije.",
    "log_merging_separation_overlay_for_slice": "Overlay razdj. linija za {0} spojen bez rotacije.",

    #   Splitter – Crtanje (trake, oznake, linije)
    "log_drawing_top_stripe": "[Canvas] Crtam gornju traku za {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Crtam desnu traku za {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Ispunjavam i obrubljujem kut za {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Crtam križ sa središtem u ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Crtam registracijske linije za {0} u području od ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Crtam desnu okomitu liniju: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Crtam gornju vodoravnu liniju: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Crtam razdjelnicu (bijela preko crne): ({0}) @ ({1:.3f}, {2:.3f}), duljina={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Crtam križeve za {0} [{1},{2}] / [{3},{4}] u području od ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Izračunata središta: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Crtam TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Crtam TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Crtam BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Crtam BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Oznaka {0} izostavljena prema pravilu za poziciju [{1},{2}]",
    "log_trial_common_sheet": "Primjenjujem TRIAL vodeni žig na zajedničkom listu",

    # Vodeni žig
    "log_trial_watermark_added": "Dodan TRIAL vodeni žig",
    "error_drawing_trial_text": "Pogreška crtanja vodenog žiga: {error}",

    #   Splitter – Razdjelne linije (cijela stranica)
    "log_drawing_separation_lines_for_page": "Crtam razdjelne linije za stranicu (raspored={0}, broj panela={1}, indeks={2})",
    "log_vertical_line_between_slices": "  Okomita linija između panela {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Početak okomite linije @ x={0:.1f}",
    "log_vertical_line_end": "  Kraj okomite linije @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Vodoravna linija između panela {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Početak vodoravne linije @ y={0:.1f}",
    "log_horizontal_line_end": "  Kraj vodoravne linije @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Odvojene_datoteke) Početak okom./vodor. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Odvojene_datoteke) Kraj okom./vodor. @ {0:.1f}",

    #   Splitter – Generiranje kodova / QR
    "log_generate_barcode_data": "Generiram podatke za kod: {0}",
    "log_barcode_data_shortened": "Podaci koda skraćeni na {0} znakova.",
    "log_barcode_data_error": "Pogreška generiranja podataka koda: {0}",
    "log_compose_barcode_payload": "Sastavljam payload koda ({0}): {1}",
    "log_barcode_payload_shortened": "Payload skraćen na {0} znakova za format {1}",
    "log_barcode_payload_error": "Pogreška sastavljanja payloada: {0}",
    "log_unknown_anchor_fallback": "Nepoznat sidreni kut „{0}”, koristi se donji lijevi",
    "log_used_default_code_settings": "Korištene postavke „default” za kod {0}/{1}.",
    "log_no_layout_key_fallback": "Nema rasporeda „{0}” za {1}/{2}. Korišten prvi dostupni: „{3}”.",
    "log_code_settings_error": "Nema/nije moguće dohvatiti postavke koda ({0}/{1}/{2}): {3}. Korištene zadane vrijednosti.",
    "log_drawing_barcode": "Crtam {0} na ({1:.3f}, {2:.3f}) [baza ({3:.3f}, {4:.3f}) + pomak ({5:.3f}, {6:.3f})], rotacija: {7}°",
    "error_generate_qr_svg": "Neuspjelo generiranje SVG QR koda.",
    "error_invalid_scale_for_qr": "Nevaljana veličina QR-a: {0} mm",
    "error_invalid_qr_scale_factor": "Nevaljan faktor mjerila QR-a: {0}",
    "error_generate_barcode_svg": "Neuspjelo generiranje SVG barkoda.",
    "error_invalid_scale_for_barcode": "Nevaljana veličina barkoda: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Nevaljan faktor mjerila barkoda: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: veličina u konfiguraciji={1:.3f} mm, širina SVG-a={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: veličina u konfiguraciji=({1:.3f} mm, {2:.3f} mm), dimenzija SVG-a=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Pogreška crtanja koda „{0}”: {1}",
    "log_prepared_barcode_info": "Pripremljene informacije o kodu za {0} ({1}, sidro={2}): osnovna apsolutna pozicija ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Pogreška pripreme podataka koda za {0}: {1}",
    "log_drawing_barcodes_count": "Crtam kodove/QR: {0} kom...",
    "log_missing_barcode_info_key": "Nedostaje ključ u informacijama koda pri crtanju: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Pogreška crtanja koda „{0}” u _draw_all_barcodes: {1}",

    #   Splitter – Proces rezanja (metode split_*)
    "log_start_splitting_process": "--- Pokretanje procesa rezanja za: {0} ---",
    "log_split_settings": "  Postavke: {0}×{1} panela, preklop={2} mm, bijela traka={3} mm (+preklop: {4})",
    "log_output_dir_info": "  Izlaz: {0} / {1} u „{2}”",
    "log_lines_marks_barcodes_info": "  Linije: razdjelnice={0}, početak={1}, kraj={2} | Oznake: {3} ({4}), Kodovi: {5} ({6})",
    "log_bryt_order_info": "  Redoslijed: {0}, rotacija panela: {1}°",
    "log_invalid_dimensions_in_slice_info": "Nevaljane dimenzije u slice_info za {0}: {1}×{2}",
    "log_content_transform": "Transformacija sadržaja T_content za {0}: {1}",
    "log_merged_content_for_slice": "Sadržaj spojen za panel {0} u new_page",
    "log_slice_reader_created": "Kompletan panel (PdfReader) stvoren za {0}",
    "log_slice_reader_creation_error": "Pogreška stvaranja kompletnog panela za {0}: {1}",
    "log_used_get_transform": "Korišten _get_transform (samo pomak): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Start: ODVOJENE DATOTEKE (rotacija u create_slice_reader) ---",
    "log_creating_file_for_slice": "Stvaram datoteku za panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Nevaljana veličina stranice ({0}×{1}) za {2}. Preskačem.",
    "log_blank_page_creation_error": "Pogreška stvaranja prazne stranice za {0} (veličina {1}×{2}): {3}. Preskačem.",
    "log_transform_for_slice": "Transformacija T (samo pomak) za {0}: {1}",
    "log_merging_complete_slice": "Spajanje kompletnog panela {0} s transformacijom: {1}",
    "log_skipped_slice_merging": "Spajanje kompletnog panela za {0} preskočeno.",
    "log_file_saved": "Datoteka spremljena: {0}",
    "log_file_save_error": "Pogreška spremanja datoteke {0}: {1}",
    "log_finished_split_separate_files": "--- Završeno: ODVOJENE DATOTEKE (spremljeno {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Nema panela za obradu u split_horizontal.",
    "log_start_split_horizontal": "--- Start: ZAJEDNIČKI LIST – VODORAVNO (rotacija u create_slice_reader) ---",
    "log_page_dimensions": "Dimenzije stranice: {0:.1f}×{1:.1f} mm ({2} panela)",
    "log_page_creation_error": "Pogreška stvaranja izlazne stranice ({0}×{1}): {2}. Prekidam.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformacija T (samo pomak) za {0}: {1}",
    "log_merging_complete_bryt": "Spajanje kompletnog panela {0} s transformacijom: {1}",
    "log_skipped_merging_bryt": "Spajanje kompletnog panela za {0} preskočeno.",
    "log_file_result_saved": "Rezultatska datoteka spremljena: {0}",
    "log_file_result_save_error": "Pogreška spremanja rezultatske datoteke {0}: {1}",
    "log_finished_split_horizontal": "--- Završeno: ZAJEDNIČKI LIST – VODORAVNO ---",
    "log_no_slices_split_vertical": "Nema panela za obradu u split_vertical.",
    "log_start_split_vertical": "--- Start: ZAJEDNIČKI LIST – OKOMITO (rotacija u create_slice_reader) ---",
    "log_finished_split_vertical": "--- Završeno: ZAJEDNIČKI LIST – OKOMITO ---",
    "log_unknown_layout": "Nepoznat raspored za zajednički list: „{0}”.",
    "log_unknown_output_type": "Nepoznata vrsta izlaza: „{0}”.",
    "log_finished_splitting_success": "--- Proces rezanja završen za: {0} — USPJEH ---",
    "log_finished_splitting_errors": "--- Proces rezanja završen za: {0} — BILO JE POGREŠAKA ---",
    "log_value_error_in_splitting": "Pogreška ulaza ili izračuna: {0}",
    "log_finished_splitting_critical_error": "--- Proces rezanja završen za: {0} — KRITIČNA POGREŠKA ---",
    "log_unexpected_error_in_splitting": "Neočekivana pogreška pri rezanju datoteke {0}: {1}",

    #   Splitter – Testni način (__main__)
    "log_script_mode_test": "splitter.py pokrenut kao glavni skript (testni način).",
    "log_loaded_config": "Konfiguracija učitana.",
    "log_error_loading_config": "Neuspjelo učitavanje konfiguracije: {0}",
    "log_created_example_pdf": "Stvoren primjer PDF: {0}",
    "log_cannot_create_example_pdf": "Neuspjelo stvaranje primjer PDF-a: {0}",
    "log_start_test_split": "Pokrećem testno rezanje datoteke: {0} u {1}",
    "log_test_split_success": "Testno rezanje uspješno završeno.",
    "log_test_split_errors": "Testno rezanje završeno s pogreškama.",

    # --- Logovi – QR/barkod (barcode_qr.py) ---
    "log_qr_empty_data": "Pokus generiranja QR koda za prazne podatke.",
    "log_qr_generated": "SVG QR koda generiran za: {0}...",
    "log_qr_error": "Pogreška generiranja QR-a za podatke „{0}”: {1}",
    "log_barcode_empty_data": "Pokus generiranja barkoda za prazne podatke.",
    "log_barcode_generated": "SVG barkoda generiran za: {0}...",
    "log_barcode_error": "Pogreška generiranja barkoda za „{0}”: {1}",
    "log_basic_handler_configured": "Osnovni rukovatelj postavljen za logger u barcode_qr.py",
    "log_basic_handler_error": "Pogreška postavljanja osnovnog rukovatelja u barcode_qr: {0}",

    # --- Logovi – Konfiguracija/Profili (main_config_manager.py) ---
    "loading_profiles_from": "Učitavanje profila iz",
    "profiles_file": "Datoteka profila",
    "does_not_contain_dict": "ne sadrži rječnik. Stvara se novi",
    "not_found_creating_new": "nije pronađena. Stvara se nova prazna",
    "json_profiles_read_error": "Pogreška čitanja JSON datoteke profila",
    "file_will_be_overwritten": "Datoteka će biti prebrisana pri spremanju",
    "json_decode_error_in_profiles": "Pogreška dekodiranja JSON-a u datoteci profila",
    "cannot_load_profiles_file": "Nije moguće učitati datoteku profila",
    "unexpected_profiles_read_error": "Neočekivana pogreška čitanja profila",
    "saving_profiles_to": "Spremanje profila u",
    "cannot_save_profiles_file": "Nije moguće spremiti datoteku profila",
    "profiles_save_error": "Pogreška spremanja profila u datoteku",
    "logger_profile_saved": "Profil spremljen: {profile}",
    "logger_profile_not_found": "Profil za učitavanje nije pronađen: {profile}",
    "logger_profile_loaded": "Profil učitan: {profile}",
    "logger_profile_delete_not_exist": "Pokus brisanja nepostojećeg profila: {profile}",
    "logger_profile_deleted": "Profil izbrisan: {profile}",
    "logger_start_save_settings": "Pokrenuto spremanje postavki iz GUI-ja.",
    "logger_invalid_value": "Nevaljana vrijednost za „{key}”. Postavljeno na 0.0.",
    "logger_end_save_settings": "Spremanje postavki iz GUI-ja završeno.",
    "logger_conversion_error": "Pogreška pretvorbe vrijednosti iz GUI-ja: {error}",
    "conversion_failed": "Neuspjela pretvorba vrijednosti iz GUI-ja",
    "logger_unexpected_save_error": "Neočekivana pogreška spremanja postavki: {error}",
    "logger_settings_saved": "Postavke spremljene u datoteku: {file}",

    # --- Logovi – Licenciranje (main_license.py) ---
    "public_key_load_error_log": "Pogreška učitavanja javnog ključa",
    "license_key_decode_error": "Pogreška dekodiranja licencnog ključa",
    "license_activation_error": "Pogreška aktivacije licence",

    # --- Logovi – Glavni modul (main.py) ---
    "ui_created": "Korisničko sučelje je stvoreno.",
    "error_tab_home": "Pogreška pri stvaranju sučelja „Početna”",
    "error_tab_settings": "Pogreška pri stvaranju sučelja „Postavke”",
    "error_tab_help": "Pogreška pri stvaranju sučelja „Pomoć”",
    "error_creating_license_ui": "Pogreška pri stvaranju sučelja „Licenca”",
    "error_loading_ui": "Opća pogreška učitavanja sučelja: {error}",
    "error_creating_home_ui": "Pogreška pri stvaranju sučelja „Početna”",
    "error_creating_settings_ui": "Pogreška pri stvaranju sučelja „Postavke”",
    "error_creating_help_ui": "Pogreška pri stvaranju sučelja „Pomoć”",
    "logger_update_gui": "Pokrenuto ažuriranje GUI-ja iz konfiguracije.",
    "logger_end_update_gui": "Ažuriranje GUI-ja iz konfiguracije završeno.",
    "logger_update_gui_error": "Neočekivana pogreška ažuriranja GUI-ja: {error}",
    "logger_invalid_output_dir": "Nevaljana ili nepostojeća izlazna mapa: {directory}",
    "logger_invalid_input_file": "Nevaljana ili nepostojeća ulazna datoteka: {file}",
    "logger_start_pdf": "Pokrenut proces generiranja PDF-a.",
    "logger_pdf_save_error": "Generiranje PDF-a prekinuto: spremanje trenutačnih postavki nije uspjelo.",
    "logger_pdf_success": "Generiranje PDF-a uspješno završeno.",
    "logger_pdf_exception": "Iznimka u glavnom procesu generiranja PDF-a.",
    "icon_set_error": "Pogreška postavljanja ikone aplikacije: {error}",
    "accent_button_style_error": "Pogreška postavljanja stila istaknutog gumba: {error}",
    "logger_file_save_error": "Pogreška spremanja datoteke {file}: {error}",

    #   Logovi – Pregled (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Pogreška generiranja minijature",
    "output_preview_update_called": "Pozvano ažuriranje pregleda izlaza",
    "output_preview_canvas_missing": "Nedostaje canvas pregleda izlaza",
    "pdf_found_in_output_dir": "PDF pronađen u izlaznoj mapi",
    "preparing_thumbnail": "Priprema minijature",
    "thumbnail_generated_successfully": "Minijatura uspješno generirana",
    "thumbnail_generation_error": "Pogreška generiranja minijature za",
    "no_pdf_for_common_sheet": "Nema PDF-a za pregled zajedničkog lista",
    "no_pdf_for_separate_files": "Nema generiranih PDF-ova za pregled",
    "cannot_load_thumbnail": "Nije moguće učitati minijaturu iz",

    #   Logovi – Interno za razvoj (main.py)
    "missing_gui_var_created": "Stvorena nedostajuća GUI varijabla za ključ: {key}",
    "missing_gui_structure_created": "Stvorena nedostajuća GUI struktura za: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Stvorena nedostajuća GUI varijabla za: {code_type}/{output_type}/{layout}/{param}",

    # Dodatni ključevi za main_ui_help.py
    "help_text": """
    Billboard Splitter – Korisnički priručnik\n\n
    Svrha programa:\n
    Billboard Splitter automatski dijeli projekte billboarda na panele spremne za tisak.
    Program je namijenjen radu s datotekama u mjerilu 1:10.\n
    Vrijednosti u odjeljcima: Preklop, Bijela traka i Postavke unose se u mjerilu 1:1.
    Program omogućuje slaganje izrezanih panela u PDF prema odabranom rasporedu:\n
    • Zajednički list: svi paneli u jednom dokumentu.\n
    • Odvojene datoteke: svaki panel u zasebnom PDF-u.\n\n
    Dodatno program omogućuje:\n
    • Odabir rasporeda – okomito ili vodoravno (u okomitom su razdjelne linije gore i dolje,
      u vodoravnom lijevo i desno).\n
    • Rotiranje panela za 180° (inverzija projekta).\n
    • Dodavanje registracijskih oznaka (križ ili linija) za precizno pozicioniranje pri lijepljenju.\n
    • Dodavanje QR kodova ili barkodova, generiranih iz ulaznih podataka radi identifikacije panela.\n
    • Spremanje postavki kao profila: mogu se učitavati, mijenjati i brisati za brzo prebacivanje.\n\n
    Osnovni koraci rada:\n\n
    1. Odabir ulazne datoteke:\n
    • Na kartici „Početna” odaberite PDF, JPG ili TIFF s izgledom billboarda.\n
    • Ako put nije zadan, koristi se demonstracijska datoteka.\n\n
    2. Postavke rezanja:\n
    • Unesite broj redova i stupaca.\n
    • Postavite veličinu preklopa.\n
    • Po potrebi postavite širinu bijele trake koja se pribraja efektivnom preklopu.\n\n
    3. Raspored izlaza:\n
    • Okomito: svi paneli slažu se okomito na PDF stranici.\n
    • Vodoravno: svi paneli slažu se vodoravno.\n\n
    4. Vrsta izlaza:\n
    • Zajednički list – jedan PDF.\n
    • Odvojene datoteke – po jedan PDF po panelu.\n
    • Na „Početnoj” možete uključiti i podesiti registracijske oznake – križ ili liniju.\n
    • Po potrebi uključite QR ili barkod – generirat će se iz podataka projekta.\n
    • Parametri koda (mjerilo, pomak, rotacija, položaj) podešavaju se na kartici „Postavke”.\n\n
    5. Upravljanje konfiguracijama:\n
    • Na kartici „Postavke” detaljno se podešavaju grafički parametri (margine, debljine linija, razmaci) i postavke kodova.\n
    • Spremite trenutačnu konfiguraciju kao profil za kasnije učitavanje/izmjenu.\n
    • Profili (profiles.json) omogućuju brzo prebacivanje između setova postavki.\n\n
    6. Generiranje PDF-a:\n
    • Kliknite „Generiraj PDF”.\n
    • Rezultati se spremaju u mapu „output” (ili drugu zadanu), a logovi u mapu „logs”.\n\n
    Ako dođe do problema:\n
    • Provjerite logove u mapi „logs”. Svakog dana stvara se nova datoteka zapisnika s datumom u nazivu.\n
    • Provjerite jesu li zadani svi potrebni direktoriji.\n
    • Podrška: tech@printworks.pl (radnim danima, 8–16)\n
    """
}
