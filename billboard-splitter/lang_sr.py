# lang_sr.py
"""
Datoteka sa prevodima za srpski jezik (latinica).
"""

LANG = {
    "barcode_font_size_label": "Veličina fonta opisa bar koda [pt]:",
    # ==========================
    #  Aplikacija – Opšte
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Greška",
    "no_file": "Nema datoteke",
    "language": "Jezik",
    "language_switch": "Promena jezika",
    "choose_language": "Izaberite jezik:",
    "apply_language": "Primeni",
    "language_changed": "Jezik je promenjen. Deo izmena biće vidljiv tek nakon ponovnog pokretanja aplikacije.",

    # ========================================
    #  Grafički interfejs (GUI)
    # ========================================

    # --- Glavne kartice ---
    "tab_home": " Početna ",
    "tab_settings": " Podešavanja ",
    "tab_help": " Pomoć ",
    "tab_license": " Licenca ",

    # --- Opšta dugmad ---
    "button_browse": "Pregledaj...",
    "browse_folder": "Pregledaj fasciklu...",
    "button_save": "Sačuvaj",
    "button_delete": "Obriši",
    "button_close": "Zatvori",
    "save_all_settings": "Sačuvaj sva podešavanja",

    # --- Oznake polja (Početna) ---
    "label_rows": "Vertikalna podela (redovi):",
    "label_columns": "Horizontalna podela (kolone):",
    "label_overlap": "Preklop [mm]:",
    "label_white_stripe": "Bela traka [mm]:",
    "label_add_white_stripe": "Dodaj belu traku efektivnom preklopu",
    "label_layout": "Raspored izlaza:",
    "label_output_type": "Tip izlaza:",
    "label_enable_reg_marks": "Uključi registracione oznake:",
    "label_enable_codes": "Uključi kodove:",
    "label_enable_sep_lines": "Uključi razdelne linije (između panela)",
    "label_enable_start_line": "Uključi liniju početka/gornju ivicu lista",
    "label_enable_end_line": "Uključi liniju kraja/donju ivicu lista",
    "label_bryt_order": "Redosled panela:",
    "label_slice_rotation": "Rotacija panela:",
    "label_create_order_folder": "Kreiraj fasciklu sa brojem narudžbine",

    # --- Sekcije (Početna) ---
    "section_input_file": " Ulazna datoteka ",
    "section_scale_and_dimensions": " Skala i izlazne dimenzije ",
    "label_original_size": "Originalna veličina:",
    "label_scale_non_uniform": "Nesrazmerno skaliranje",
    "label_scale": "Skala: 1:",
    "label_scale_x": "Skala X: 1:",
    "label_scale_y": "Skala Y: 1:",
    "label_output_dimensions": "Dimenzije izlazne datoteke:",
    "label_width_cm": "Širina [cm]:",
    "label_height_cm": "Visina [cm]:",
    "section_split_settings": " Podešavanja sečenja ",
    "section_profiles": " Profili podešavanja ",
    "section_save_location": " Mesto čuvanja ",
    "section_input_preview": " Pregled ulaza ",
    "section_output_preview": " Pregled izlaza ",

    # --- Vrednosti opcija ---
    "layout_vertical": "Vertikalno",
    "layout_horizontal": "Horizontalno",
    "output_common_sheet": "Zajednički list",
    "output_separate_files": "Odvojene datoteke",
    "output_both": "Zajednički list i odvojene datoteke",
    "output_common": "Zajednički list",
    "output_separate": "Odvojene datoteke",
    "reg_mark_cross": "Krst",
    "reg_mark_line": "Linija",
    "code_qr": "QR kod",
    "code_barcode": "Barkod",
    "bryt_order_1": "A1–An, B1–Bn, .. Standard, odozgo",
    "bryt_order_2": "A1–An, Bn–B1, .. Zmijasto po redovima, odozgo",
    "bryt_order_3": "A1..B1, A2..B2, .. Po kolonama, odozgo",
    "bryt_order_4": "A1–A2..B2–B1.. Zmijasto po kolonama, odozgo",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Standard, odozdo",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Zmijasto po redovima, odozdo",
    "logging_console": "konsola",
    "logging_file": "datoteka",
    "logging_both": "oboje",

    # --- Sekcije (Podešavanja) ---
    "section_processing_mode": " Režimi obrade ",
    "processing_mode_ram": "RAM (u memoriji)",
    "processing_mode_hdd": "Disk (na skladištu)",
    "graphic_settings": "Grafička podešavanja",
    "code_settings": "Podešavanja QR/barkoda",
    "logging_settings": "Podešavanja logovanja",
    "barcode_text_position_label": "Položaj natpisa uz kod:",
    "barcode_text_bottom": "dole",
    "barcode_text_side": "sa strane",
    "barcode_text_none": "bez",

    # --- Oznake (Podešavanja – Grafika) ---
    "extra_margin_label": "Margina oko panela [mm]:",
    "margin_top_label": "Gornja margina [mm]:",
    "margin_bottom_label": "Donja margina [mm]:",
    "margin_left_label": "Leva margina [mm]:",
    "margin_right_label": "Desna margina [mm]:",
    "reg_mark_width_label": "Registraciona oznaka – širina [mm]:",
    "reg_mark_height_label": "Registraciona oznaka – visina [mm]:",
    "reg_mark_white_line_width_label": "Registraciona oznaka – debljina bele linije [mm]:",
    "reg_mark_black_line_width_label": "Registraciona oznaka – debljina crne linije [mm]:",
    "sep_line_black_width_label": "Razdelna – debljina crne linije [mm]:",
    "sep_line_white_width_label": "Razdelna – debljina bele linije [mm]:",
    "slice_gap_label": "Razmak između panela [mm]:",
    "label_draw_slice_border": "Crtaj okvir oko panela (linija reza)",

    # --- Oznake (Podešavanja – Kodovi) ---
    "scale_label": "Veličina [mm]:",
    "scale_x_label": "Širina X [mm]:",
    "scale_y_label": "Visina Y [mm]:",
    "offset_x_label": "Pomeraj X [mm]:",
    "offset_y_label": "Pomeraj Y [mm]:",
    "rotation_label": "Rotacija (°):",
    "anchor_label": "Ugao:",

    # --- Oznake (Podešavanja – Logovi) ---
    "logging_mode_label": "Režim logovanja:",
    "log_file_label": "Datoteka loga:",
    "logging_level_label": "Nivo logovanja:",

    # --- Dugmad / akcije (Početna) ---
    "button_load": "Učitaj",
    "button_save_settings": "Sačuvaj trenutna podešavanja",
    "button_generate_pdf": "Generiši PDF",
    "button_refresh_preview": "Osveži pregled",
    "button_refresh_layout": "Osveži raspored",

    # --- Licenca (GUI) ---
    "hwid_frame_title": "Jedinstveni identifikator hardvera (HWID)",
    "copy_hwid": "Kopiraj HWID",
    "license_frame_title": "Aktivacija licence",
    "enter_license_key": "Unesite licencni ključ:",
    "activate": "Aktiviraj",
    "status_trial": "Probni režim",
    "license_active": "Licenca je aktivna",

    # ================================================
    #  Poruke korisniku (prozorčići, statusna traka)
    # ================================================

    # --- Profili ---
    "msg_no_profile_name": "Bez naziva",
    "msg_enter_profile_name": "Unesite naziv profila za čuvanje.",
    "msg_profile_saved": "Profil sačuvan",
    "profile_saved_title": "Profil sačuvan",
    "msg_profile_saved_detail": "Profil „{0}” je sačuvan.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profil '{profile}' je sačuvan i primenjen.",
    "msg_no_profile": "Nema profila",
    "warning_no_profile": "Nema profila",
    "msg_select_profile": "Izaberite naziv profila sa liste za učitavanje.",
    "select_profile": "Izaberite naziv profila sa liste za učitavanje.",
    "profile_loaded_title": "Profil učitan",
    "profile_loaded": "Profil „{profile}” je učitan.",
    "warning_no_profile_delete": "Nema profila",
    "warning_no_profile_delete_message": "Izaberite profil sa liste za brisanje.",
    "profile_not_found": "Profil „{profile}” nije pronađen.",
    "profile_not_exist": "Profil „{profile}” ne postoji.",
    "confirm_delete_title": "Potvrdite brisanje",
    "confirm_delete_profile": "Zaista želite obrisati profil „{profile}”?",
    "profile_deleted_title": "Profil obrisan",
    "profile_deleted": "Profil „{profile}” je obrisan.",

    # --- Datoteke / fascikle ---
    "msg_no_input_file": "Nema ulazne datoteke",
    "msg_unsupported_format": "Nepodržani format",
    "select_file_title": "Izbor ulazne datoteke",
    "supported_files": "Podržane datoteke",
    "all_files": "Sve datoteke",
    "select_dir_title": "Izbor izlazne fascikle",
    "select_log_dir_title": "Izbor fascikle za logove",
    "error_output_dir_title": "Greška izlazne fascikle",
    "error_output_dir": "Navedena izlazna fascikla je neispravna ili ne postoji:\n{directory}",
    "error_input_file_title": "Greška ulazne datoteke",
    "error_input_file": "Navedena ulazna datoteka je neispravna ili ne postoji:\n{file}",
    "save_file_error_title": "Greška čuvanja datoteke",
    "save_file_error": "Datoteku nije moguće sačuvati: {error}",

    # --- Obrada PDF-a / pregled ---
    "msg_pdf_processing_error": "Neuspešna obrada PDF datoteke",
    "msg_thumbnail_error": "Greška pri učitavanju umanjenog prikaza",
    "msg_no_pdf_output": "Nema PDF izlaza",
    "no_pdf_pages": "PDF ne sadrži stranice",
    "unsupported_output": "Nepodržan tip izlaza za pregled",
    "pdf_generated_title": "Generisanje završeno",
    "pdf_generated": "PDF datoteka(e) uspešno generisane u fasciklu:\n{directory}",
    "pdf_generation_error_title": "Greška generisanja",
    "pdf_generation_error": "Tokom generisanja PDF-a došlo je do grešaka. Proverite logove.",
    "critical_pdf_error_title": "Kritična greška generisanja PDF-a",
    "critical_pdf_error": "Došlo je do kritične greške pri generisanju PDF-a:\n{error}\nVideti logove.",
    "settings_saved_title": "Podešavanja sačuvana",
    "settings_saved": "Podešavanja su sačuvana u datoteku:\n{filepath}",
    "settings_save_error_title": "Greška čuvanja podešavanja",
    "settings_save_error": "Nije moguće sačuvati podešavanja: {error}",
    "conversion_error_title": "Greška konverzije",
    "conversion_error": "Greška pri konverziji vrednosti iz interfejsa: {error}",
    "update_gui_error_title": "Greška ažuriranja interfejsa",
    "update_gui_error": "Došlo je do greške pri ažuriranju interfejsa: {error}",

    # --- Licenca ---
    "hwid_copied_to_clipboard": "HWID je kopiran u privremenu memoriju",
    "computer_hwid": "HWID računara",
    "public_key_load_error": "Greška učitavanja javnog ključa: {error}",
    "invalid_license_format": "Neispravan format licencnog ključa: {error}",
    "activation_success": "Licenca je uspešno aktivirana.",
    "activation_error": "Greška aktivacije licence: {error}",
    "log_trial_mode_active": "Probni režim je aktivan",
    "log_trial_mode_inactive": "Probni režim nije aktivan",

    # --- Inicijalizacija ---
    "init_error_title": "Greška inicijalizacije",
    "init_error": "Greška pri inicijalizaciji fascikli: {error}",
    "poppler_path_info": "Informacije o putanji Popplera",
    "ttkthemes_not_installed": "Napomena: biblioteka ttkthemes nije instalirana. Koristi se podrazumevani stil Tkintera.",

    # =====================================
    #  Logovi (poruke zapisnika)
    # =====================================

    # --- Opšte / Konfiguracija ---
    "log_configured": "Logovanje konfigurisano: nivo={0}, režim={1}, datoteka={2}",
    "log_no_handlers": "Upozorenje: rukovaoci logova nisu konfigurisani (režim: {0}).",
    "log_critical_error": "Kritična greška konfiguracije logovanja: {0}",
    "log_basic_config": "Zbog greške korišćena je osnovna konfiguracija logovanja.",
    "log_dir_create_error": "Kritična greška: nije moguće kreirati fasciklu logova {0}: {1}",

    # --- Logovi – Inicijalizacija / Fascikle (init_directories.py) ---
    "error_critical_init": "KRITIČNA GREŠKA tokom inicijalizacije: {0}",
    "logger_init_error": "Greška inicijalizacije fascikli: {error}",
    "directory_created": "Kreirana fascikla: {0}",
    "directory_creation_error": "Nije moguće kreirati fasciklu {0}: {1}",
    "sample_file_copied": "Primer datoteka kopirana u {0}",
    "sample_file_copy_error": "Greška kopiranja primer datoteke: {0}",
    "log_created_output_dir": "Kreirana izlazna fascikla: {0}",
    "log_cannot_create_output_dir": "Nije moguće kreirati izlaznu fasciklu {0}: {1}",

    # --- Logovi – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Neuspešno učitavanje grafičkih podešavanja pri inicijalizaciji: {0}",
    "log_loading_pdf": "Učitavanje PDF datoteke: {0}",
    "log_loading_bitmap": "Učitavanje rasterske datoteke: {0}",
    "log_invalid_dpi": "Učitano nevažeće DPI ({0}). Koristi se podrazumevano {1} DPI.",
    "log_image_dimensions": "Dimenzije slike: {0}×{1}px, režim: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Obrada slike u izvornom kolor režimu: {0}",
    "log_unusual_color_mode": "Neuobičajen kolor režim: „{0}“. ReportLab/Pillow možda neće ispravno raditi.",
    "log_draw_image_error": "Greška ReportLab drawImage za režim {0}: {1}",
    "log_unsupported_format": "Nepodržan ulazni format: {0}",
    "log_input_file_not_found": "Ulazna datoteka nije pronađena: {0}",
    "log_load_process_error": "Greška pri učitavanju ili obradi datoteke {0}: {1}",
    "log_input_file_not_exists": "Ulazna datoteka ne postoji ili je putanja prazna: „{0}”",
    "log_cannot_load_or_empty_pdf": "Nije moguće učitati ulaznu datoteku ili je PDF prazan/oštećen.",
    "log_pdf_dimensions_info": "  Dimenzije PDF-a: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Nevažeće dimenzije PDF stranice: {0}×{1} pt.",

    #   Splitter – Izračuni dimenzija
    "log_extra_margin": "Dodatna margina postavljena na {0:.3f} pt",
    "log_invalid_rows_cols": "Nevažeći broj redova ({0}) ili kolona ({1}).",
    "error_invalid_rows_cols": "Redovi i kolone moraju biti pozitivni celi brojevi.",
    "log_invalid_overlap_white_stripe": "Nevažeće vrednosti preklopa ({0}) ili bele trake ({1}). Moraju biti numeričke.",
    "error_invalid_overlap_white_stripe": "Preklop i bela traka moraju biti numeričke vrednosti (mm).",
    "log_stripe_usage": "Postavljeno use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Osnovni preklop (grafika): {0:.3f} mm, bela traka: {1:.3f} mm, efektivni preklop: {2:.3f} mm",
    "log_computed_dimensions": "Izračunato: PDF {0:.3f}×{1:.3f} mm. Panel: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Jezgro: {6:.3f}×{7:.3f} pt. Efekt. preklop: {8:.3f} mm",
    "log_invalid_dimensions": "Nevažeće dimenzije panela ({0:.3f}×{1:.3f}) ili jezgra ({2:.3f}×{3:.3f}) za per={4}, traka={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Izračunate dimenzije panela/jezgra su nevažeće ili negativne.",

    #   Splitter – Generisanje informacija i redosleda
    "log_generating_slice_info": "Generišem informacije o panelu: {0}",
    "log_no_slices_info_generated": "Nije moguće generisati informacije o panelima.",
    "log_applying_rotated_order": "Primena redosleda za rotaciju 180°: {0}",
    "log_applying_standard_order": "Primena redosleda za 0° (standard): {0}",
    "log_unknown_bryt_order": "Nepoznat redosled panela: „{0}“. Koristi se podrazumevani.",
    "log_final_slices_order": "  Konačni redosled panela ({0}): [{1}]",

    #   Splitter – Preklapanja (overlay) i spajanje
    "log_invalid_dimensions_overlay": "Pokušaj izrade overlay-a sa nevažećim dimenzijama: {0}. Preskačem.",
    "log_empty_overlay": "Kreiran prazan ili gotovo prazan overlay PDF. Spajanje preskočeno.",
    "log_overlay_error": "Greška pri kreiranju overlay PDF-a: {0}",
    "log_merge_error": "Pokušaj spajanja overlay-a bez stranica. Preskačem.",
    "log_merge_page_error": "Greška spajanja overlay PDF-a: {0}",
    "log_fallback_draw_rotating_elements": "Nije moguće dobiti redove/kolone za _draw_rotating_elements, korišćeno 1×1.",
    "log_overlay_created_for_slice": "Overlay traka/oznaka kreiran za panel {0}",
    "log_overlay_creation_failed_for_slice": "Neuspešno kreiranje overlay-a za {0}",
    "log_merging_rotated_overlay": "Spajanje ROTIRANOG overlay-a za {0} sa T={1}",
    "log_merging_nonrotated_overlay": "Spajanje NEROTIRANOG overlay-a za {0}",
    "log_merging_all_codes_overlay": "Spajanje overlay-a svih kodova (bez rotacije)",
    "log_merging_separation_lines_overlay": "Spajanje overlay-a razdelnih linija (bez rotacije)",
    "log_merging_code_overlay_for_slice": "Overlay koda za {0} spojen bez rotacije.",
    "log_merging_separation_overlay_for_slice": "Overlay razdelnih linija za {0} spojen bez rotacije.",

    #   Splitter – Crtanje (trake, oznake, linije)
    "log_drawing_top_stripe": "[Canvas] Crtam gornju traku za {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Crtam desnu traku za {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Popunjavam i obrubljujem ugao za {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Crtam krst sa centrom u ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Crtam registracione linije za {0} u oblasti od ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Crtam desnu vertikalnu liniju: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Crtam gornju horizontalnu liniju: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Crtam razdelnu liniju (bela preko crne): ({0}) @ ({1:.3f}, {2:.3f}), dužina={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Crtam krstove za {0} [{1},{2}] / [{3},{4}] u oblasti od ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Izračunati centri: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Crtam TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Crtam TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Crtam BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Crtam BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Oznaka {0} izostavljena prema pravilu za poziciju [{1},{2}]",
    "log_trial_common_sheet": "Primenujem TRIAL vodeni žig na zajedničkom listu",

    # Vodeni žig
    "log_trial_watermark_added": "Dodat TRIAL vodeni žig",
    "error_drawing_trial_text": "Greška pri crtanju vodenog žiga: {error}",

    #   Splitter – Razdelne linije (cela stranica)
    "log_drawing_separation_lines_for_page": "Crtam razdelne linije za stranicu (raspored={0}, broj panela={1}, indeks panela={2})",
    "log_vertical_line_between_slices": "  Vertikalna linija između panela {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Početak vertikalne linije @ x={0:.1f}",
    "log_vertical_line_end": "  Kraj vertikalne linije @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Horizontalna linija između panela {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Početak horizontalne linije @ y={0:.1f}",
    "log_horizontal_line_end": "  Kraj horizontalne linije @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Odvojene_datoteke) Početak vert./horiz. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Odvojene_datoteke) Kraj vert./horiz. @ {0:.1f}",

    #   Splitter – Generisanje kodova / QR
    "log_generate_barcode_data": "Generišem podatke za kod: {0}",
    "log_barcode_data_shortened": "Podaci koda skraćeni na {0} znakova.",
    "log_barcode_data_error": "Greška generisanja podataka koda: {0}",
    "log_compose_barcode_payload": "Sastavljam payload koda ({0}): {1}",
    "log_barcode_payload_shortened": "Payload skraćen na {0} znakova za format {1}",
    "log_barcode_payload_error": "Greška sastavljanja payloada: {0}",
    "log_unknown_anchor_fallback": "Nepoznat sidreni ugao „{0}“, koristi se donji levi",
    "log_used_default_code_settings": "Korišćena su podrazumevana podešavanja za kod {0}/{1}.",
    "log_no_layout_key_fallback": "Nema rasporeda „{0}” za {1}/{2}. Korišćen prvi dostupni: „{3}”.",
    "log_code_settings_error": "Nema/Nije moguće dohvatiti podešavanja koda ({0}/{1}/{2}): {3}. Korišćene podrazumevane vrednosti.",
    "log_drawing_barcode": "Crtam {0} na ({1:.3f}, {2:.3f}) [baza ({3:.3f}, {4:.3f}) + pomeraj ({5:.3f}, {6:.3f})], rotacija: {7}°",
    "error_generate_qr_svg": "Neuspešno generisanje SVG QR koda.",
    "error_invalid_scale_for_qr": "Nevažeća veličina QR-a: {0} mm",
    "error_invalid_qr_scale_factor": "Nevažeći faktor skale QR-a: {0}",
    "error_generate_barcode_svg": "Neuspešno generisanje SVG barkoda.",
    "error_invalid_scale_for_barcode": "Nevažeća veličina barkoda: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Nevažeći faktor skale barkoda: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: veličina u konfiguraciji={1:.3f} mm, širina SVG={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: veličina u konfiguraciji=({1:.3f} mm, {2:.3f} mm), dimenzija SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Greška crtanja koda „{0}“: {1}",
    "log_prepared_barcode_info": "Pripremljene informacije o kodu za {0} ({1}, sidro={2}): osnovna apsolutna pozicija ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Greška pripreme podataka koda za {0}: {1}",
    "log_drawing_barcodes_count": "Crtam {0} kodova/QR...",
    "log_missing_barcode_info_key": "Nedostaje ključ u informacijama koda pri crtanju: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Greška crtanja koda „{0}“ u _draw_all_barcodes: {1}",

    #   Splitter – Proces sečenja (metode split_*)
    "log_start_splitting_process": "--- Pokrećem proces sečenja za: {0} ---",
    "log_split_settings": "  Podešavanja: {0}×{1} panela, preklop={2} mm, bela traka={3} mm (+preklop: {4})",
    "log_output_dir_info": "  Izlaz: {0} / {1} u „{2}”",
    "log_lines_marks_barcodes_info": "  Linije: razdelne={0}, početak={1}, kraj={2} | Oznake: {3} ({4}), Kodovi: {5} ({6})",
    "log_bryt_order_info": "  Redosled: {0}, rotacija panela: {1}°",
    "log_invalid_dimensions_in_slice_info": "Nevažeće dimenzije u slice_info za {0}: {1}×{2}",
    "log_content_transform": "Transformacija sadržaja T_content za {0}: {1}",
    "log_merged_content_for_slice": "Sadržaj spojen za panel {0} u new_page",
    "log_slice_reader_created": "Kompletan panel (PdfReader) kreiran za {0}",
    "log_slice_reader_creation_error": "Greška kreiranja kompletnog panela za {0}: {1}",
    "log_used_get_transform": "Korišćen _get_transform (samo pomeraj): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Start: ODVOJENE DATOTEKE (rotacija u create_slice_reader) ---",
    "log_creating_file_for_slice": "Kreiram datoteku za panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Nevažeća veličina stranice ({0}×{1}) za {2}. Preskačem.",
    "log_blank_page_creation_error": "Greška kreiranja prazne stranice za {0} (dimenzija {1}×{2}): {3}. Preskačem.",
    "log_transform_for_slice": "Transformacija T (samo pomeraj) za {0}: {1}",
    "log_merging_complete_slice": "Spajanje kompletnog panela {0} sa transformacijom: {1}",
    "log_skipped_slice_merging": "Spajanje kompletnog panela za {0} preskočeno.",
    "log_file_saved": "Datoteka sačuvana: {0}",
    "log_file_save_error": "Greška čuvanja datoteke {0}: {1}",
    "log_finished_split_separate_files": "--- Završeno: ODVOJENE DATOTEKE (sačuvano {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Nema panela za obradu u split_horizontal.",
    "log_start_split_horizontal": "--- Start: ZAJEDNIČKI LIST – HORIZONTALNO (rotacija u create_slice_reader) ---",
    "log_page_dimensions": "Dimenzije stranice: {0:.1f}×{1:.1f} mm ({2} panela)",
    "log_page_creation_error": "Greška kreiranja izlazne stranice ({0}×{1}): {2}. Prekidam.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformacija T (samo pomeraj) za {0}: {1}",
    "log_merging_complete_bryt": "Spajanje kompletnog panela {0} sa transformacijom: {1}",
    "log_skipped_merging_bryt": "Spajanje kompletnog panela za {0} preskočeno.",
    "log_file_result_saved": "Rezultujuća datoteka sačuvana: {0}",
    "log_file_result_save_error": "Greška čuvanja rezultujuće datoteke {0}: {1}",
    "log_finished_split_horizontal": "--- Završeno: ZAJEDNIČKI LIST – HORIZONTALNO ---",
    "log_no_slices_split_vertical": "Nema panela za obradu u split_vertical.",
    "log_start_split_vertical": "--- Start: ZAJEDNIČKI LIST – VERTIKALNO (rotacija u create_slice_reader) ---",
    "log_finished_split_vertical": "--- Završeno: ZAJEDNIČKI LIST – VERTIKALNO ---",
    "log_unknown_layout": "Nepoznat raspored za zajednički list: „{0}”.",
    "log_unknown_output_type": "Nepoznat tip izlaza: „{0}”.",
    "log_finished_splitting_success": "--- Proces sečenja završen za: {0} — USPEH ---",
    "log_finished_splitting_errors": "--- Proces sečenja završen za: {0} — BILO JE GREŠAKA ---",
    "log_value_error_in_splitting": "Greška ulaza ili izračuna: {0}",
    "log_finished_splitting_critical_error": "--- Proces sečenja završen za: {0} — KRITIČNA GREŠKA ---",
    "log_unexpected_error_in_splitting": "Neočekivana greška pri sečenju datoteke {0}: {1}",

    #   Splitter – Test režim (__main__)
    "log_script_mode_test": "splitter.py pokrenut kao glavni skript (test režim).",
    "log_loaded_config": "Konfiguracija učitana.",
    "log_error_loading_config": "Neuspešno učitavanje konfiguracije: {0}",
    "log_created_example_pdf": "Kreiran primer PDF: {0}",
    "log_cannot_create_example_pdf": "Neuspešno kreiranje primer PDF-a: {0}",
    "log_start_test_split": "Pokrećem test sečenje datoteke: {0} u {1}",
    "log_test_split_success": "Test sečenje uspešno završeno.",
    "log_test_split_errors": "Test sečenje završeno sa greškama.",

    # --- Logovi – QR/barkod (barcode_qr.py) ---
    "log_qr_empty_data": "Pokušaj generisanja QR koda za prazne podatke.",
    "log_qr_generated": "SVG QR koda generisan za: {0}...",
    "log_qr_error": "Greška generisanja QR-a za podatke „{0}“: {1}",
    "log_barcode_empty_data": "Pokušaj generisanja barkoda za prazne podatke.",
    "log_barcode_generated": "SVG barkoda generisan za: {0}...",
    "log_barcode_error": "Greška generisanja barkoda za „{0}“: {1}",
    "log_basic_handler_configured": "Osnovni rukovalac postavljen za logger u barcode_qr.py",
    "log_basic_handler_error": "Greška postavljanja osnovnog rukovaoca u barcode_qr: {0}",

    # --- Logovi – Konfiguracija/Profili (main_config_manager.py) ---
    "loading_profiles_from": "Učitavam profile iz",
    "profiles_file": "Datoteka profila",
    "does_not_contain_dict": "ne sadrži rečnik. Kreira se novi",
    "not_found_creating_new": "nije pronađena. Kreira se nova prazna",
    "json_profiles_read_error": "Greška čitanja JSON datoteke profila",
    "file_will_be_overwritten": "Datoteka će biti prebrisana pri čuvanju",
    "json_decode_error_in_profiles": "Greška dekodiranja JSON-a u datoteci profila",
    "cannot_load_profiles_file": "Nije moguće učitati datoteku profila",
    "unexpected_profiles_read_error": "Neočekivana greška čitanja profila",
    "saving_profiles_to": "Čuvam profile u",
    "cannot_save_profiles_file": "Nije moguće sačuvati datoteku profila",
    "profiles_save_error": "Greška čuvanja profila u datoteku",
    "logger_profile_saved": "Profil sačuvan: {profile}",
    "logger_profile_not_found": "Profil za učitavanje nije pronađen: {profile}",
    "logger_profile_loaded": "Profil učitan: {profile}",
    "logger_profile_delete_not_exist": "Pokušaj brisanja nepostojećeg profila: {profile}",
    "logger_profile_deleted": "Profil obrisan: {profile}",
    "logger_start_save_settings": "Pokrenuto čuvanje podešavanja iz GUI-ja.",
    "logger_invalid_value": "Nevažeća vrednost za „{key}“. Postavljeno na 0.0.",
    "logger_end_save_settings": "Čuvanje podešavanja iz GUI-ja završeno.",
    "logger_conversion_error": "Greška konverzije vrednosti iz GUI-ja: {error}",
    "conversion_failed": "Neuspešna konverzija vrednosti iz GUI-ja",
    "logger_unexpected_save_error": "Neočekivana greška čuvanja podešavanja: {error}",
    "logger_settings_saved": "Podešavanja sačuvana u datoteku: {file}",

    # --- Logovi – Licenciranje (main_license.py) ---
    "public_key_load_error_log": "Greška učitavanja javnog ključa",
    "license_key_decode_error": "Greška dekodiranja licencnog ključa",
    "license_activation_error": "Greška aktivacije licence",

    # --- Logovi – Glavni modul (main.py) ---
    "ui_created": "Korisnički interfejs je kreiran.",
    "error_tab_home": "Greška pri kreiranju interfejsa „Početna”",
    "error_tab_settings": "Greška pri kreiranju interfejsa „Podešavanja”",
    "error_tab_help": "Greška pri kreiranju interfejsa „Pomoć”",
    "error_creating_license_ui": "Greška pri kreiranju interfejsa „Licenca”",
    "error_loading_ui": "Opšta greška učitavanja interfejsa: {error}",
    "error_creating_home_ui": "Greška pri kreiranju interfejsa „Početna”",
    "error_creating_settings_ui": "Greška pri kreiranju interfejsa „Podešavanja”",
    "error_creating_help_ui": "Greška pri kreiranju interfejsa „Pomoć”",
    "logger_update_gui": "Pokrenuto ažuriranje GUI-ja iz konfiguracije.",
    "logger_end_update_gui": "Ažuriranje GUI-ja iz konfiguracije završeno.",
    "logger_update_gui_error": "Neočekivana greška ažuriranja GUI-ja: {error}",
    "logger_invalid_output_dir": "Nevažeća ili nepostojeća izlazna fascikla: {directory}",
    "logger_invalid_input_file": "Nevažeća ili nepostojeća ulazna datoteka: {file}",
    "logger_start_pdf": "Pokrenut proces generisanja PDF-a.",
    "logger_pdf_save_error": "Generisanje PDF-a prekinuto: čuvanje trenutnih podešavanja nije uspelo.",
    "logger_pdf_success": "Generisanje PDF-a uspešno završeno.",
    "logger_pdf_exception": "Izuzetak u glavnom procesu generisanja PDF-a.",
    "icon_set_error": "Greška postavljanja ikone aplikacije: {error}",
    "accent_button_style_error": "Greška postavljanja stila akcentnog dugmeta: {error}",
    "logger_file_save_error": "Greška čuvanja datoteke {file}: {error}",

    #   Logovi – Pregled (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Greška generisanja umanjenog prikaza",
    "output_preview_update_called": "Pozvano ažuriranje pregleda izlaza",
    "output_preview_canvas_missing": "Nedostaje platno (canvas) pregleda izlaza",
    "pdf_found_in_output_dir": "PDF pronađen u izlaznoj fascikli",
    "preparing_thumbnail": "Priprema umanjenog prikaza",
    "thumbnail_generated_successfully": "Umanjeni prikaz uspešno generisan",
    "thumbnail_generation_error": "Greška generisanja umanjenog prikaza za",
    "no_pdf_for_common_sheet": "Nema PDF-a za pregled zajedničkog lista",
    "no_pdf_for_separate_files": "Nema generisanih PDF-ova za pregled",
    "cannot_load_thumbnail": "Nije moguće učitati umanjen prikaz iz",

    #   Logovi – Interno za razvoj (main.py)
    "missing_gui_var_created": "Kreirana nedostajuća GUI promenljiva za ključ: {key}",
    "missing_gui_structure_created": "Kreirana nedostajuća GUI struktura za: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Kreirana nedostajuća GUI promenljiva za: {code_type}/{output_type}/{layout}/{param}",

    # Dodatni ključevi za main_ui_help.py
    "help_text": """
    Billboard Splitter – Korisničko uputstvo\n\n
    Svrha programa:\n
    Billboard Splitter automatski deli projekte bilborda na panele spremne za štampu.
    Program je namenjen radu sa fajlovima u razmeri 1:10.\n
    Vrednosti u odeljcima: Preklop, Bela traka i Podešavanja unose se u razmeri 1:1.
    Program omogućava slaganje isečenih panela u PDF prema izabranom rasporedu:\n
    • Zajednički list: svi paneli u jednom dokumentu.\n
    • Odvojene datoteke: svaki panel u posebnom PDF-u.\n\n
    Dodatno program omogućava:\n
    • Izbor rasporeda – vertikalno ili horizontalno (kod vertikalnog su razdelne linije gore i dole,
      kod horizontalnog levo i desno).\n
    • Rotiranje panela za 180° (inverzija celog projekta).\n
    • Dodavanje registracionih oznaka (krst ili linija) za precizno pozicioniranje pri lepljenju.\n
    • Dodavanje QR kodova ili barkodova – generisanih iz ulaznih podataka radi identifikacije panela.\n
    • Čuvanje podešavanja kao profila, koji se mogu učitavati, menjati i brisati – brzo prebacivanje između projekata.\n\n
    Osnovni koraci:\n\n
    1. Izbor ulazne datoteke:\n
    • Na kartici „Početna” izaberite PDF, JPG ili TIFF sa dizajnom bilborda.\n
    • Ako ne zadate sopstvenu putanju, koristi se podrazumevani primer fajla.\n\n
    2. Podešavanja sečenja:\n
    • Unesite broj redova i kolona na koje se projekat deli.\n
    • Podesite veličinu preklopa.\n
    • Po potrebi podesite širinu bele trake koja se pribraja efektivnom preklopu.\n\n
    3. Raspored izlaza:\n
    • Vertikalno: paneli se slažu vertikalno na PDF stranici.\n
    • Horizontalno: paneli se slažu horizontalno.\n\n
    4. Tip izlaza:\n
    • Zajednički list – jedan PDF.\n
    • Odvojene datoteke – po jedan PDF po panelu.\n
    • Na „Početnoj” možete uključiti i podesiti registracione oznake – krst ili liniju.\n
    • Po potrebi uključite QR ili barkod – generisaće se iz podataka projekta.\n
    • Parametre koda (skala, pomeraj, rotacija, položaj) podešavate na kartici „Podešavanja”.\n\n
    5. Upravljanje konfiguracijama:\n
    • Na kartici „Podešavanja” detaljno se podešavaju grafički parametri (margine, debljine linija, razmaci) i podešavanja kodova.\n
    • Sačuvajte trenutnu konfiguraciju kao profil za kasnije učitavanje ili izmenu.\n
    • Profili (profiles.json) omogućavaju brzo prebacivanje između različitih setova podešavanja.\n\n
    6. Generisanje PDF-a:\n
    • Kliknite „Generiši PDF”.\n
    • Rezultati se čuvaju u fasciklu „output” (ili drugu zadatu), a logovi (sa dnevnom rotacijom) u „logs”.\n\n
    Ako dođe do problema:\n
    • Proverite logove u fascikli „logs”. Svakog dana se kreira novi log fajl sa datumom u nazivu.\n
    • Proverite da li su definisane sve potrebne fascikle.\n
    • Podrška: tech@printworks.pl (radnim danima, 8–16)\n
    """
}
