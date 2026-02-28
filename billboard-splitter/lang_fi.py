# lang_fi.py
"""
Käännöstiedosto suomen kielelle.
"""

LANG = {
    "barcode_font_size_label": "Viivakoodikuvauksen fonttikoko [pt]:",
    # ==========================
    #  Sovellus – Yleiset
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Virhe",
    "no_file": "Ei tiedostoa",
    "language": "Kieli",
    "language_switch": "Kielen vaihto",
    "choose_language": "Valitse kieli:",
    "apply_language": "Käytä",
    "language_changed": "Kieli on vaihdettu. Osa muutoksista näkyy vasta sovelluksen uudelleenkäynnistyksen jälkeen.",

    # ========================================
    #  Käyttöliittymä (GUI)
    # ========================================

    # --- Päävälilehdet ---
    "tab_home": " Koti ",
    "tab_settings": " Asetukset ",
    "tab_help": " Ohje ",
    "tab_license": " Lisenssi ",

    # --- Yleiset painikkeet ---
    "button_browse": "Selaa...",
    "browse_folder": "Selaa kansiota...",
    "button_save": "Tallenna",
    "button_delete": "Poista",
    "button_close": "Sulje",
    "save_all_settings": "Tallenna kaikki asetukset",

    # --- Kenttien selitteet (Koti) ---
    "label_rows": "Pystysuuntainen jako (rivit):",
    "label_columns": "Vaakasuuntainen jako (sarakkeet):",
    "label_overlap": "Limitys [mm]:",
    "label_white_stripe": "Valkoinen kaista [mm]:",
    "label_add_white_stripe": "Lisää valkoinen kaista tehokkaaseen limitykseen",
    "label_layout": "Tulosteen asettelu:",
    "label_output_type": "Tulosteen tyyppi:",
    "label_enable_reg_marks": "Ota kohdistusmerkit käyttöön:",
    "label_enable_codes": "Ota koodit käyttöön:",
    "label_enable_sep_lines": "Ota jakoviivat käyttöön (paneelien väliin)",
    "label_enable_start_line": "Ota alku-/yläviiva käyttöön",
    "label_enable_end_line": "Ota loppu-/alaviiva käyttöön",
    "label_bryt_order": "Paneelien järjestys:",
    "label_slice_rotation": "Paneelien kierto:",
    "label_create_order_folder": "Luo kansio tilausnumerolla",

    # --- Osiot/ryhmät (Koti) ---
    "section_input_file": " Syöttötiedosto ",
    "section_scale_and_dimensions": " Mittakaava ja tulosteen mitat ",
    "label_original_size": "Alkuperäinen koko:",
    "label_scale_non_uniform": "Skaalaa epäsuhteellisesti",
    "label_scale": "Mittakaava: 1:",
    "label_scale_x": "Mittakaava X: 1:",
    "label_scale_y": "Mittakaava Y: 1:",
    "label_output_dimensions": "Tulostetiedoston mitat:",
    "label_width_cm": "Leveys [cm]:",
    "label_height_cm": "Korkeus [cm]:",
    "section_split_settings": " Leikkausasetukset ",
    "section_profiles": " Asetusprofiilit ",
    "section_save_location": " Tallennussijainti ",
    "section_input_preview": " Syötteen esikatselu ",
    "section_output_preview": " Tulosteen esikatselu ",

    # --- Valintojen arvot ---
    "layout_vertical": "Pysty",
    "layout_horizontal": "Vaaka",
    "output_common_sheet": "Yhteinen arkki",
    "output_separate_files": "Erilliset tiedostot",
    "output_both": "Yhteinen arkki ja erilliset tiedostot",
    "output_common": "Yhteinen arkki",
    "output_separate": "Erilliset tiedostot",
    "reg_mark_cross": "Risti",
    "reg_mark_line": "Viiva",
    "code_qr": "QR-koodi",
    "code_barcode": "Viivakoodi",
    "bryt_order_1": "A1–An, B1–Bn, .. Vakio, ylhäältä",
    "bryt_order_2": "A1–An, Bn–B1, .. Käärme riveittäin, ylhäältä",
    "bryt_order_3": "A1..B1, A2..B2, .. Sarakkeittain, ylhäältä",
    "bryt_order_4": "A1–A2..B2–B1.. Käärme sarakkeittain, ylhäältä",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Vakio, alhaalta",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Käärme riveittäin, alhaalta",
    "logging_console": "konsoli",
    "logging_file": "tiedosto",
    "logging_both": "molemmat",

    # --- Osiot/ryhmät (Asetukset) ---
    "section_processing_mode": " Käsittelytilat ",
    "processing_mode_ram": "RAM (muistissa)",
    "processing_mode_hdd": "Levy (tallennus)",
    "graphic_settings": "Grafiikka-asetukset",
    "code_settings": "QR-/viivakoodin asetukset",
    "logging_settings": "Lokiasetukset",
    "barcode_text_position_label": "Koodin tekstin sijainti:",
    "barcode_text_bottom": "alhaalla",
    "barcode_text_side": "sivulla",
    "barcode_text_none": "ei tekstiä",

    # --- Selitteet (Asetukset – Grafiikka) ---
    "extra_margin_label": "Reuna paneelien ympärillä [mm]:",
    "margin_top_label": "Yläreuna [mm]:",
    "margin_bottom_label": "Alareuna [mm]:",
    "margin_left_label": "Vasen reuna [mm]:",
    "margin_right_label": "Oikea reuna [mm]:",
    "reg_mark_width_label": "Kohdistusmerkki – leveys [mm]:",
    "reg_mark_height_label": "Kohdistusmerkki – korkeus [mm]:",
    "reg_mark_white_line_width_label": "Kohdistusmerkki – valkoisen viivan paksuus [mm]:",
    "reg_mark_black_line_width_label": "Kohdistusmerkki – mustan viivan paksuus [mm]:",
    "sep_line_black_width_label": "Jakoviiva – mustan viivan paksuus [mm]:",
    "sep_line_white_width_label": "Jakoviiva – valkoisen viivan paksuus [mm]:",
    "slice_gap_label": "Väli paneelien välillä [mm]:",
    "label_draw_slice_border": "Piirrä kehys paneelin ympärille (leikkausviiva)",

    # --- Selitteet (Asetukset – Koodit) ---
    "scale_label": "Koko [mm]:",
    "scale_x_label": "Leveys X [mm]:",
    "scale_y_label": "Korkeus Y [mm]:",
    "offset_x_label": "Siirto X [mm]:",
    "offset_y_label": "Siirto Y [mm]:",
    "rotation_label": "Kierto (°):",
    "anchor_label": "Kulma:",

    # --- Selitteet (Asetukset – Lokit) ---
    "logging_mode_label": "Lokin tila:",
    "log_file_label": "Lokitiedosto:",
    "logging_level_label": "Lokituksen taso:",

    # --- Painikkeet / toiminnot (Koti) ---
    "button_load": "Lataa",
    "button_save_settings": "Tallenna nykyiset asetukset",
    "button_generate_pdf": "Luo PDF",
    "button_refresh_preview": "Päivitä esikatselu",
    "button_refresh_layout": "Päivitä asettelu",

    # --- Lisenssi (GUI) ---
    "hwid_frame_title": "Laitteen yksilöivä tunniste (HWID)",
    "copy_hwid": "Kopioi HWID",
    "license_frame_title": "Lisenssin aktivointi",
    "enter_license_key": "Anna lisenssiavain:",
    "activate": "Aktivoi",
    "status_trial": "Kokeilutila",
    "license_active": "Lisenssi on aktiivinen",

    # ================================================
    #  Käyttäjäviestit (ikkunat, tilarivi)
    # ================================================

    # --- Profiilit ---
    "msg_no_profile_name": "Ei nimeä",
    "msg_enter_profile_name": "Anna profiilin nimi tallennusta varten.",
    "msg_profile_saved": "Profiili tallennettu",
    "profile_saved_title": "Profiili tallennettu",
    "msg_profile_saved_detail": "Profiili \"{0}\" on tallennettu.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profiili '{profile}' on tallennettu ja otettu käyttöön.",
    "msg_no_profile": "Ei profiilia",
    "warning_no_profile": "Ei profiilia",
    "msg_select_profile": "Valitse listasta profiilin nimi ladattavaksi.",
    "select_profile": "Valitse listasta profiilin nimi ladattavaksi.",
    "profile_loaded_title": "Profiili ladattu",
    "profile_loaded": "Profiili \"{profile}\" on ladattu.",
    "warning_no_profile_delete": "Ei profiilia",
    "warning_no_profile_delete_message": "Valitse listasta poistettava profiili.",
    "profile_not_found": "Profiilia \"{profile}\" ei löydy.",
    "profile_not_exist": "Profiilia \"{profile}\" ei ole olemassa.",
    "confirm_delete_title": "Vahvista poisto",
    "confirm_delete_profile": "Haluatko varmasti poistaa profiilin \"{profile}\"?",
    "profile_deleted_title": "Profiili poistettu",
    "profile_deleted": "Profiili \"{profile}\" on poistettu.",

    # --- Tiedostot / hakemistot ---
    "msg_no_input_file": "Ei syöttötiedostoa",
    "msg_unsupported_format": "Ei tuettu formaatti",
    "select_file_title": "Valitse syöttötiedosto",
    "supported_files": "Tuetut tiedostot",
    "all_files": "Kaikki tiedostot",
    "select_dir_title": "Valitse tulostekansio",
    "select_log_dir_title": "Valitse lokikansio",
    "error_output_dir_title": "Tulostekansion virhe",
    "error_output_dir": "Määritetty tulostekansio on virheellinen tai sitä ei ole:\n{directory}",
    "error_input_file_title": "Syöttötiedoston virhe",
    "error_input_file": "Määritetty syöttötiedosto on virheellinen tai sitä ei ole:\n{file}",
    "save_file_error_title": "Tiedoston tallennusvirhe",
    "save_file_error": "Tiedostoa ei voitu tallentaa: {error}",

    # --- PDF-käsittely / esikatselu ---
    "msg_pdf_processing_error": "PDF-tiedoston käsittely epäonnistui",
    "msg_thumbnail_error": "Pienoiskuvan latausvirhe",
    "msg_no_pdf_output": "Ei PDF-tulostetta",
    "no_pdf_pages": "PDF ei sisällä sivuja",
    "unsupported_output": "Esikatseluun ei tuettu tulostetyyppi",
    "pdf_generated_title": "Luonti valmis",
    "pdf_generated": "PDF-tiedosto(t) luotiin onnistuneesti hakemistoon:\n{directory}",
    "pdf_generation_error_title": "Luontivirhe",
    "pdf_generation_error": "PDF:n luonnin aikana tapahtui virheitä. Tarkista lokit lisätietoja varten.",
    "critical_pdf_error_title": "Kriittinen PDF-luontivirhe",
    "critical_pdf_error": "Tapahtui kriittinen virhe PDF:ää luotaessa:\n{error}\nKatso lokit.",
    "settings_saved_title": "Asetukset tallennettu",
    "settings_saved": "Asetukset tallennettiin tiedostoon:\n{filepath}",
    "settings_save_error_title": "Asetusten tallennusvirhe",
    "settings_save_error": "Asetuksia ei voitu tallentaa: {error}",
    "conversion_error_title": "Muunnosvirhe",
    "conversion_error": "Arvojen muunto käyttöliittymästä epäonnistui: {error}",
    "update_gui_error_title": "Käyttöliittymän päivitysvirhe",
    "update_gui_error": "Käyttöliittymää päivitettäessä tapahtui virhe: {error}",

    # --- Lisenssi ---
    "hwid_copied_to_clipboard": "HWID kopioitu leikepöydälle",
    "computer_hwid": "Tietokoneen HWID",
    "public_key_load_error": "Julkisen avaimen latausvirhe: {error}",
    "invalid_license_format": "Virheellinen lisenssiavaimen formaatti: {error}",
    "activation_success": "Lisenssi aktivoitu onnistuneesti.",
    "activation_error": "Lisenssin aktivointi epäonnistui: {error}",
    "log_trial_mode_active": "Kokeilutila on aktiivinen",
    "log_trial_mode_inactive": "Kokeilutila ei ole aktiivinen",

    # --- Alustus ---
    "init_error_title": "Alustusvirhe",
    "init_error": "Hakemistojen alustusvirhe: {error}",
    "poppler_path_info": "Poppler-polun tiedot",
    "ttkthemes_not_installed": "Huom: ttkthemes-kirjasto ei ole asennettuna. Käytetään Tkinterin oletustyyliä.",

    # =====================================
    #  Lokit (loggerin viestit)
    # =====================================

    # --- Yleiset / Konfigurointi ---
    "log_configured": "Lokitus konfiguroitu: taso={0}, tila={1}, tiedosto={2}",
    "log_no_handlers": "Huom: lokinkäsittelijöitä ei ole konfiguroitu (tila: {0}).",
    "log_critical_error": "Lokituksen konfiguroinnin kriittinen virhe: {0}",
    "log_basic_config": "Peruslokitus otettiin käyttöön virheen vuoksi.",
    "log_dir_create_error": "Kriittinen virhe: lokihakemistoa {0} ei voida luoda: {1}",

    # --- Lokit – Alustus / Hakemistot (init_directories.py) ---
    "error_critical_init": "KRIITTINEN VIRHE alustuksen aikana: {0}",
    "logger_init_error": "Hakemistojen alustuksen virhe: {error}",
    "directory_created": "Hakemisto luotu: {0}",
    "directory_creation_error": "Hakemiston {0} luonti epäonnistui: {1}",
    "sample_file_copied": "Mall tiedosto kopioitu kohteeseen {0}",
    "sample_file_copy_error": "Mallin kopiointivirhe: {0}",
    "log_created_output_dir": "Tulostehakemisto luotu: {0}",
    "log_cannot_create_output_dir": "Tulostehakemistoa {0} ei voi luoda: {1}",

    # --- Lokit – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Grafiikka-asetusten lataus epäonnistui alustuksessa: {0}",
    "log_loading_pdf": "Ladataan PDF-tiedostoa: {0}",
    "log_loading_bitmap": "Ladataan bittikarttatiedostoa: {0}",
    "log_invalid_dpi": "Luettu DPI on virheellinen ({0}). Käytetään oletusta {1} DPI.",
    "log_image_dimensions": "Kuvan mitat: {0}×{1}px, tila: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Käsitellään kuvaa alkuperäisellä väritilalla: {0}",
    "log_unusual_color_mode": "Epätavallinen väritila: \"{0}\". ReportLab/Pillow ei välttämättä käsittele oikein.",
    "log_draw_image_error": "ReportLab drawImage -virhe tilalle {0}: {1}",
    "log_unsupported_format": "Ei tuettu syöteformaatti: {0}",
    "log_input_file_not_found": "Syöttötiedostoa ei löydy: {0}",
    "log_load_process_error": "Virhe tiedoston {0} latauksessa tai käsittelyssä: {1}",
    "log_input_file_not_exists": "Syöttötiedostoa ei ole tai polku on tyhjä: \"{0}\"",
    "log_cannot_load_or_empty_pdf": "Syöttötiedoston lataus epäonnistui tai PDF on tyhjä/vioittunut.",
    "log_pdf_dimensions_info": "  PDF-mitat: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "PDF-sivun mitat virheelliset: {0}×{1} pt.",

    #   Splitter – Mittojen laskenta
    "log_extra_margin": "Lisäreuna asetettu arvoon {0:.3f} pt",
    "log_invalid_rows_cols": "Rivien ({0}) tai sarakkeiden ({1}) määrä virheellinen.",
    "error_invalid_rows_cols": "Rivien ja sarakkeiden tulee olla positiivisia kokonaislukuja.",
    "log_invalid_overlap_white_stripe": "Limitys ({0}) tai valkoinen kaista ({1}) virheellinen. Arvojen tulee olla numeerisia.",
    "error_invalid_overlap_white_stripe": "Limityksen ja valkoisen kaistan tulee olla numeerisia arvoja (mm).",
    "log_stripe_usage": "Asetettu use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Peruslimitys (grafiikka): {0:.3f} mm, valkoinen kaista: {1:.3f} mm, tehokas limitys: {2:.3f} mm",
    "log_computed_dimensions": "Lasketut mitat: PDF {0:.3f}×{1:.3f} mm. Paneeli: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Ydin: {6:.3f}×{7:.3f} pt. Teh. limitys: {8:.3f} mm",
    "log_invalid_dimensions": "Virheelliset paneelin ({0:.3f}×{1:.3f}) tai ytimen ({2:.3f}×{3:.3f}) mitat arvoilla per={4}, stripe={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Lasketut paneelin/ytimen mitat ovat virheelliset tai negatiiviset.",

    #   Splitter – Paneelitiedot ja -järjestys
    "log_generating_slice_info": "Luodaan paneelin tietoja: {0}",
    "log_no_slices_info_generated": "Paneelitietoja ei saatu luotua.",
    "log_applying_rotated_order": "Sovelletaan 180° kierron järjestystä: {0}",
    "log_applying_standard_order": "Sovelletaan 0° (vakio) järjestystä: {0}",
    "log_unknown_bryt_order": "Tuntematon paneelijärjestys: \"{0}\". Käytetään oletusta.",
    "log_final_slices_order": "  Lopullinen paneelijärjestys ({0}): [{1}]",

    #   Splitter – Overlayt ja yhdistäminen
    "log_invalid_dimensions_overlay": "Yritettiin luoda overlay virheellisillä mitoilla: {0}. Ohitetaan.",
    "log_empty_overlay": "Luotiin tyhjä tai lähes tyhjä overlay-PDF. Yhdistäminen ohitetaan.",
    "log_overlay_error": "Overlay-PDF:n luontivirhe: {0}",
    "log_merge_error": "Yritettiin yhdistää overlay ilman sivuja. Ohitetaan.",
    "log_merge_page_error": "Overlay-PDF:n yhdistysvirhe: {0}",
    "log_fallback_draw_rotating_elements": "Rivejä/sarakkeita ei saatu _draw_rotating_elements -metodille, käytetään 1×1.",
    "log_overlay_created_for_slice": "Puskurit/merkit -overlay luotu paneelille {0}",
    "log_overlay_creation_failed_for_slice": "Overlayn luonti epäonnistui kohteelle {0}",
    "log_merging_rotated_overlay": "Yhdistetään KIERRETTY overlay {0} T={1}",
    "log_merging_nonrotated_overlay": "Yhdistetään EI-kierretty overlay {0}",
    "log_merging_all_codes_overlay": "Yhdistetään kaikkien koodien overlay (ei kiertoa)",
    "log_merging_separation_lines_overlay": "Yhdistetään jakoviivojen overlay (ei kiertoa)",
    "log_merging_code_overlay_for_slice": "Koodin overlay {0} yhdistetty ilman kiertoa.",
    "log_merging_separation_overlay_for_slice": "Jakoviivojen overlay {0} yhdistetty ilman kiertoa.",

    #   Splitter – Piirto (kaistat, merkit, viivat)
    "log_drawing_top_stripe": "[Canvas] Piirretään yläkaista {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Piirretään oikea kaista {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Täytetään ja rajataan kulma {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Piirretään risti keskelle ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Piirretään kohdistusviivoja {0} alueelle ({1:.3f},{2:.3f}) alkaen",
    "log_drawing_right_vertical_line": "  Piirretään oikea pystylinja: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Piirretään ylä vaakalinja: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Piirretään jakoviiva (valkoinen mustan päällä): ({0}) @ ({1:.3f}, {2:.3f}), pituus={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Piirretään ristit {0}:lle [{1},{2}] / [{3},{4}] alueelle alkaen ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Lasketut keskukset: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Piirretään TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Piirretään TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Piirretään BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Piirretään BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Ohitetaan {0} säännön mukaan sijainnissa [{1},{2}]",
    "log_trial_common_sheet": "Lisätään TRIAL-vesileima yhteiseen arkkiin",

    # Vesileima
    "log_trial_watermark_added": "TRIAL-vesileima lisätty",
    "error_drawing_trial_text": "Vesileiman piirto epäonnistui: {error}",

    #   Splitter – Jakoviivat (koko sivu)
    "log_drawing_separation_lines_for_page": "Piirretään jakoviivat sivulle (asettelu={0}, paneeleita={1}, paneeli-indeksi={2})",
    "log_vertical_line_between_slices": "  Pystylinja paneelien {0}-{1} väliin @ x={2:.1f}",
    "log_vertical_line_start": "  Pystylinjan alku @ x={0:.1f}",
    "log_vertical_line_end": "  Pystylinjan loppu @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Vaakalinja paneelien {0}-{1} väliin @ y={2:.1f}",
    "log_horizontal_line_start": "  Vaakalinejan alku @ y={0:.1f}",
    "log_horizontal_line_end": "  Vaakalinejan loppu @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Erilliset_tiedostot) Pysty/vaaka alku @ {0:.1f}",
    "log_sep_line_end_separate": "  (Erilliset_tiedostot) Pysty/vaaka loppu @ {0:.1f}",

    #   Splitter – Koodien / QR:n generointi
    "log_generate_barcode_data": "Luodaan koodin dataa: {0}",
    "log_barcode_data_shortened": "Koodin data lyhennetty {0} merkkiin.",
    "log_barcode_data_error": "Koodin datan luonnin virhe: {0}",
    "log_compose_barcode_payload": "Koostetaan koodin payload ({0}): {1}",
    "log_barcode_payload_shortened": "Payload lyhennettiin {0} merkkiin muodolle {1}",
    "log_barcode_payload_error": "Payloadin koostamisen virhe: {0}",
    "log_unknown_anchor_fallback": "Tuntematon ankkuri \"{0}\", käytetään vasenta alakulmaa",
    "log_used_default_code_settings": "Käytettiin \"default\"-asetuksia koodille {0}/{1}.",
    "log_no_layout_key_fallback": "Asettelua \"{0}\" ei ole kohteelle {1}/{2}. Käytetään ensimmäistä saatavilla olevaa: \"{3}\".",
    "log_code_settings_error": "Koodin asetuksia ei löydy/virhe ({0}/{1}/{2}): {3}. Käytetään oletusarvoja.",
    "log_drawing_barcode": "Piirretään {0} kohtaan ({1:.3f}, {2:.3f}) [perus ({3:.3f}, {4:.3f}) + siirto ({5:.3f}, {6:.3f})], kierto: {7}°",
    "error_generate_qr_svg": "QR-koodin SVG:n generointi epäonnistui.",
    "error_invalid_scale_for_qr": "Virheellinen QR-koko: {0} mm",
    "error_invalid_qr_scale_factor": "Virheellinen QR-mittakerroin: {0}",
    "error_generate_barcode_svg": "Viivakoodin SVG:n generointi epäonnistui.",
    "error_invalid_scale_for_barcode": "Virheellinen viivakoodin koko: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Virheellinen viivakoodin mittakerroin: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: koko asetuksissa={1:.3f} mm, SVG-leveys={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: koko asetuksissa=({1:.3f} mm, {2:.3f} mm), SVG-koko=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Virhe koodin \"{0}\" piirtämisessä: {1}",
    "log_prepared_barcode_info": "Koodin tiedot valmisteltu kohteelle {0} ({1}, ankkuri={2}): perus absoluuttinen sijainti ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Virhe koodin tietojen valmistelussa {0}: {1}",
    "log_drawing_barcodes_count": "Piirretään koodeja/QR-koodeja: {0} kpl...",
    "log_missing_barcode_info_key": "Puuttuva avain koodin tiedoissa piirtämisen aikana: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Virhe koodin \"{0}\" piirtämisessä _draw_all_barcodes -kohdassa: {1}",

    #   Splitter – Leikkausprosessi (split_* -menetelmät)
    "log_start_splitting_process": "--- Leikkausprosessi alkaa kohteelle: {0} ---",
    "log_split_settings": "  Asetukset: {0}×{1} paneelia, limitys={2} mm, valkoinen kaista={3} mm (+limitys: {4})",
    "log_output_dir_info": "  Tuloste: {0} / {1} hakemistoon \"{2}\"",
    "log_lines_marks_barcodes_info": "  Viivat: jakoviivat={0}, alku={1}, loppu={2} | Merkit: {3} ({4}), Koodit: {5} ({6})",
    "log_bryt_order_info": "  Järjestys: {0}, paneelien kierto: {1}°",
    "log_invalid_dimensions_in_slice_info": "Virheelliset mitat slice_info:ssa {0}: {1}×{2}",
    "log_content_transform": "Sisällön muunnos T_content kohteelle {0}: {1}",
    "log_merged_content_for_slice": "Sisältö yhdistetty paneelille {0} new_pageen",
    "log_slice_reader_created": "Täysi paneeli (PdfReader) luotu kohteelle {0}",
    "log_slice_reader_creation_error": "Täyden paneelin luontivirhe kohteelle {0}: {1}",
    "log_used_get_transform": "Käytetty _get_transform (vain siirto): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Alkaa: ERILLISET TIEDOSTOT (kierto create_slice_reader:ssa) ---",
    "log_creating_file_for_slice": "Luodaan tiedosto paneelille {0}: {1}",
    "log_invalid_page_size_for_slice": "Virheellinen sivukoko ({0}×{1}) kohteelle {2}. Ohitetaan.",
    "log_blank_page_creation_error": "Tyhjän sivun luontivirhe {0} (koko {1}×{2}): {3}. Ohitetaan.",
    "log_transform_for_slice": "Muunnos T (vain siirto) kohteelle {0}: {1}",
    "log_merging_complete_slice": "Yhdistetään täysi paneeli {0} muunnoksella: {1}",
    "log_skipped_slice_merging": "Täyden paneelin yhdistäminen ohitettu kohteelle {0}.",
    "log_file_saved": "Tiedosto tallennettu: {0}",
    "log_file_save_error": "Tiedoston {0} tallennusvirhe: {1}",
    "log_finished_split_separate_files": "--- Valmis: ERILLISET TIEDOSTOT (tallennettu {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Ei paneeleja käsiteltäväksi split_horizontal -menetelmässä.",
    "log_start_split_horizontal": "--- Alkaa: YHTEINEN ARKKI – VAAKA (kierto create_slice_reader:ssa) ---",
    "log_page_dimensions": "Sivun mitat: {0:.1f}×{1:.1f} mm ({2} paneelia)",
    "log_page_creation_error": "Tulossivun luontivirhe ({0}×{1}): {2}. Keskeytetään.",
    "log_slice_at_position": "Paneeli {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Muunnos T (vain siirto) kohteelle {0}: {1}",
    "log_merging_complete_bryt": "Yhdistetään täysi paneeli {0} muunnoksella: {1}",
    "log_skipped_merging_bryt": "Täyden paneelin yhdistäminen ohitettu {0}.",
    "log_file_result_saved": "Tulostiedosto tallennettu: {0}",
    "log_file_result_save_error": "Tulostiedoston {0} tallennusvirhe: {1}",
    "log_finished_split_horizontal": "--- Valmis: YHTEINEN ARKKI – VAAKA ---",
    "log_no_slices_split_vertical": "Ei paneeleja käsiteltäväksi split_vertical -menetelmässä.",
    "log_start_split_vertical": "--- Alkaa: YHTEINEN ARKKI – PYSTY (kierto create_slice_reader:ssa) ---",
    "log_finished_split_vertical": "--- Valmis: YHTEINEN ARKKI – PYSTY ---",
    "log_unknown_layout": "Tuntematon asettelu yhteiselle arkille: \"{0}\".",
    "log_unknown_output_type": "Tuntematon tulosteen tyyppi: \"{0}\".",
    "log_finished_splitting_success": "--- Leikkausprosessi valmis kohteelle: {0} – ONNISTUI ---",
    "log_finished_splitting_errors": "--- Leikkausprosessi valmis kohteelle: {0} – TAPAHTUI VIRHEITÄ ---",
    "log_value_error_in_splitting": "Syöte- tai laskentavirhe: {0}",
    "log_finished_splitting_critical_error": "--- Leikkausprosessi valmis kohteelle: {0} – KRIITTINEN VIRHE ---",
    "log_unexpected_error_in_splitting": "Odottamaton virhe tiedoston {0} leikkauksessa: {1}",

    #   Splitter – Testitila (__main__)
    "log_script_mode_test": "splitter.py käynnistetty pääskriptinä (testitila).",
    "log_loaded_config": "Konfiguraatio ladattu.",
    "log_error_loading_config": "Konfiguraation lataus epäonnistui: {0}",
    "log_created_example_pdf": "Esimerkkipdf luotu: {0}",
    "log_cannot_create_example_pdf": "Esimerkkipdf:n luonti epäonnistui: {0}",
    "log_start_test_split": "Aloitetaan testileikkaus tiedostolle: {0} → {1}",
    "log_test_split_success": "Testileikkaus suoritettu onnistuneesti.",
    "log_test_split_errors": "Testileikkaus päättyi virheisiin.",

    # --- Lokit – QR/viivakoodi (barcode_qr.py) ---
    "log_qr_empty_data": "Yritettiin luoda QR-koodi tyhjille tiedoille.",
    "log_qr_generated": "QR-koodin SVG luotu: {0}...",
    "log_qr_error": "QR-koodin generointivirhe datalle \"{0}\": {1}",
    "log_barcode_empty_data": "Yritettiin luoda viivakoodi tyhjille tiedoille.",
    "log_barcode_generated": "Viivakoodin SVG luotu: {0}...",
    "log_barcode_error": "Viivakoodin generointivirhe kohteelle \"{0}\": {1}",
    "log_basic_handler_configured": "Peruskäsittelijä konfiguroitu loggerille tiedostossa barcode_qr.py",
    "log_basic_handler_error": "Peruskäsittelijän konfigurointi epäonnistui barcode_qr:ssa: {0}",

    # --- Lokit – Konfiguraatio/Profiilit (main_config_manager.py) ---
    "loading_profiles_from": "Ladataan profiileja kohteesta",
    "profiles_file": "Profiilitiedosto",
    "does_not_contain_dict": "ei sisällä sanakirjaa. Luodaan uusi",
    "not_found_creating_new": "ei löydy. Luodaan uusi tyhjä",
    "json_profiles_read_error": "Profiilien JSON-lukuvirhe",
    "file_will_be_overwritten": "Tiedosto korvataan tallennettaessa",
    "json_decode_error_in_profiles": "JSON-purkamisvirhe profiilitiedostossa",
    "cannot_load_profiles_file": "Profiilitiedostoa ei voida ladata",
    "unexpected_profiles_read_error": "Odottamaton profiilien lukuvirhe",
    "saving_profiles_to": "Tallennetaan profiileja kohteeseen",
    "cannot_save_profiles_file": "Profiilitiedostoa ei voida tallentaa",
    "profiles_save_error": "Profiilien tallennusvirhe tiedostoon",
    "logger_profile_saved": "Profiili tallennettu: {profile}",
    "logger_profile_not_found": "Profiilia ei löydy ladattavaksi: {profile}",
    "logger_profile_loaded": "Profiili ladattu: {profile}",
    "logger_profile_delete_not_exist": "Yritettiin poistaa olematonta profiilia: {profile}",
    "logger_profile_deleted": "Profiili poistettu: {profile}",
    "logger_start_save_settings": "GUI:sta käynnistettiin asetusten tallennus.",
    "logger_invalid_value": "Virheellinen arvo kentälle \"{key}\". Asetettu 0.0.",
    "logger_end_save_settings": "Asetusten tallennus GUI:sta päättyi.",
    "logger_conversion_error": "Arvojen muunnosvirhe GUI:sta: {error}",
    "conversion_failed": "GUI-arvojen muunnos epäonnistui",
    "logger_unexpected_save_error": "Odottamaton asetusten tallennusvirhe: {error}",
    "logger_settings_saved": "Asetukset tallennettu tiedostoon: {file}",

    # --- Lokit – Lisensointi (main_license.py) ---
    "public_key_load_error_log": "Julkisen avaimen latausvirhe",
    "license_key_decode_error": "Lisenssiavaimen purkuvirhe",
    "license_activation_error": "Lisenssin aktivointivirhe",

    # --- Lokit – Päämoduuli (main.py) ---
    "ui_created": "Käyttöliittymä luotu.",
    "error_tab_home": "Virhe luotaessa 'Koti'-näkymää",
    "error_tab_settings": "Virhe luotaessa 'Asetukset'-näkymää",
    "error_tab_help": "Virhe luotaessa 'Ohje'-näkymää",
    "error_creating_license_ui": "Virhe luotaessa 'Lisenssi'-näkymää",
    "error_loading_ui": "Yleinen käyttöliittymän latausvirhe: {error}",
    "error_creating_home_ui": "Virhe luotaessa 'Koti'-näkymää",
    "error_creating_settings_ui": "Virhe luotaessa 'Asetukset'-näkymää",
    "error_creating_help_ui": "Virhe luotaessa 'Ohje'-näkymää",
    "logger_update_gui": "GUI:n päivitys konfiguraatiosta käynnistetty.",
    "logger_end_update_gui": "GUI:n päivitys konfiguraatiosta valmis.",
    "logger_update_gui_error": "Odottamaton virhe GUI:n päivityksessä: {error}",
    "logger_invalid_output_dir": "Virheellinen tai puuttuva tulostehakemisto: {directory}",
    "logger_invalid_input_file": "Virheellinen tai puuttuva syöttötiedosto: {file}",
    "logger_start_pdf": "PDF:n generointiprosessi käynnistetty.",
    "logger_pdf_save_error": "PDF:n generointi keskeytetty: nykyisten asetusten tallennus epäonnistui.",
    "logger_pdf_success": "PDF:n generointi suoritettu onnistuneesti.",
    "logger_pdf_exception": "Poikkeus pääprosessissa PDF:ää generoitaessa.",
    "icon_set_error": "Sovelluksen kuvakkeen asettaminen epäonnistui: {error}",
    "accent_button_style_error": "Korostuspainikkeen tyylin asetus epäonnistui: {error}",
    "logger_file_save_error": "Tiedoston {file} tallennusvirhe: {error}",

    #   Lokit – Esikatselu (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Pienoiskuvan generointivirhe",
    "output_preview_update_called": "Tulosteen esikatselun päivitys kutsuttu",
    "output_preview_canvas_missing": "Tulosteen esikatselun canvas puuttuu",
    "pdf_found_in_output_dir": "PDF löytyi tulostehakemistosta",
    "preparing_thumbnail": "Valmistellaan pienoiskuvaa",
    "thumbnail_generated_successfully": "Pienoiskuva luotu onnistuneesti",
    "thumbnail_generation_error": "Pienoiskuvan generointivirhe kohteelle",
    "no_pdf_for_common_sheet": "Yhteisen arkin esikatseluun ei ole PDF:ää",
    "no_pdf_for_separate_files": "Esikatseluun ei ole luotuja PDF-tiedostoja",
    "cannot_load_thumbnail": "Pienoiskuvaa ei voida ladata kohteesta",

    #   Lokit – Kehittäjä / GUI:n sisäiset (main.py)
    "missing_gui_var_created": "Puuttuva GUI-muuttuja luotu avaimelle: {key}",
    "missing_gui_structure_created": "Puuttuva GUI-rakenne luotu: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Puuttuva GUI-muuttuja luotu: {code_type}/{output_type}/{layout}/{param}",

    # Lisäavaimet main_ui_help.py:lle
    "help_text": """
    Billboard Splitter – Käyttöopas\n\n
    Ohjelman tarkoitus:\n
    Billboard Splitter jakaa mainostauluprojektit automaattisesti tulostusvalmiiksi paneeleiksi.
    Ohjelma on suunniteltu toimimaan 1:10-mittakaavassa tehtyjen tiedostojen kanssa.\n
    Arvot osioissa: Limitys, Valkoinen kaista ja Asetukset annetaan 1:1-mittakaavassa.
    Ohjelma voi koota leikatut paneelit PDF-tiedostoihin valitun asettelun mukaan:\n
    • Yhteinen arkki: kaikki paneelit yhdessä dokumentissa.\n
    • Erilliset tiedostot: jokainen paneeli omaan PDF:ään.\n\n
    Lisäksi ohjelma mahdollistaa:\n
    • Asettelun valinnan – pysty tai vaaka (pystyssä jakoviivat ylhäällä ja alhaalla,
      vaakasuunnassa vasemmalla ja oikealla).\n
    • Paneelien kääntämisen 180° (koko projektin inversio).\n
    • Kohdistusmerkkien (risti tai viiva) lisäämisen tarkan kohdistuksen helpottamiseksi.\n
    • QR- tai viivakoodien lisäämisen – ne generoidaan syöttötiedoista paneelien tunnistusta varten.\n
    • Asetusten tallentamisen profiileiksi, joita voi ladata, muokata ja poistaa projektien välillä vaihdettaessa.\n\n
    Peruskäyttö:\n\n
    1. Valitse syöttötiedosto:\n
    • Välilehdellä \"Koti\" valitse PDF-, JPG- tai TIFF-tiedosto, joka sisältää mainostaulun suunnitelman.\n
    • Jos omaa polkua ei aseteta, ohjelma käyttää oletusmallia.\n\n
    2. Leikkausasetukset:\n
    • Määritä rivien ja sarakkeiden määrä, joihin projekti jaetaan.\n
    • Aseta limityksen koko.\n
    • Valinnaisesti määritä valkoisen kaistan leveys, joka lisätään tehokkaaseen limitykseen.\n\n
    3. Tulosteen asettelu:\n
    • Pysty: kaikki paneelit pystyyn PDF-sivulle.\n
    • Vaaka: kaikki paneelit vaakaan PDF-sivulle.\n\n
    4. Tulosteen tyyppi:\n
    • Yhteinen arkki – yksi PDF.\n
    • Erilliset tiedostot – yksi PDF per paneeli.\n
    • Välilehdellä \"Koti\" voi ottaa käyttöön ja säätää kohdistusmerkkejä – risti tai viiva.\n
    • Valinnaisesti ota käyttöön QR- tai viivakoodi – se muodostetaan projektin tiedoista.\n
    • Koodin parametreja (koko, siirto, kierto, sijainti) voi hienosäätää välilehdellä \"Asetukset\".\n\n
    5. Asetusprofiilit:\n
    • Välilehdellä \"Asetukset\" voi säätää tarkasti grafiikkaa (reunat, viivojen paksuudet, välit) ja koodiasetuksia.\n
    • Tallenna nykyiset asetukset profiiliksi myöhempää lataamista tai muokkausta varten.\n
    • Profiilit (profiles.json) mahdollistavat nopeat vaihdot eri projektien vaatimusten välillä.\n\n
    6. PDF:n generointi:\n
    • Kun kaikki asetukset ovat valmiit, napsauta \"Luo PDF\".\n
    • Tulokset tallennetaan \"output\"-kansioon (tai muuhun määritettyyn) ja lokit (päivittäin kiertävät) \"logs\"-kansioon (tai muuhun).\n\n
    Ongelmatilanteissa:\n
    • Tarkista lokit \"logs\"-kansiosta. Joka päivä luodaan uusi lokitiedosto päivämäärällä.\n
    • Varmista, että kaikki vaaditut kansiot on määritetty.\n
    • Tuki: tech@printworks.pl (arkisin klo 8–16)\n
    """
}
