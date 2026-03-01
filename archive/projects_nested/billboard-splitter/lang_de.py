# lang_de.py
"""
Deutsch (de) Sprachdatei.
Konvention: „bryt“ wird einheitlich als „Panel“ übersetzt.
"""

LANG = {
    "barcode_font_size_label": "Schriftgröße der Barcode-Beschreibung [pt]:",
    # ==========================
    #  Anwendung – Allgemein
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Fehler",
    "no_file": "Keine Datei",
    "language": "Sprache",
    "language_switch": "Sprachumschaltung",
    "choose_language": "Sprache auswählen:",
    "apply_language": "Anwenden",
    "language_changed": "Die Sprache wurde geändert. Einige Änderungen werden erst nach einem Neustart der Anwendung sichtbar.",

    # ========================================
    #  Benutzeroberfläche (GUI)
    # ========================================

    # --- Haupt-Tabs ---
    "tab_home": " Start ",
    "tab_settings": " Einstellungen ",
    "tab_help": " Hilfe ",
    "tab_license": " Lizenz ",

    # --- Allgemeine Buttons ---
    "button_browse": "Durchsuchen…",
    "browse_folder": "Ordner durchsuchen…",
    "button_save": "Speichern",
    "button_delete": "Löschen",
    "button_close": "Schließen",
    "save_all_settings": "Alle Einstellungen speichern",

    # --- Feldbezeichnungen (Start) ---
    "label_rows": "Vertikale Teilung (Zeilen):",
    "label_columns": "Horizontale Teilung (Spalten):",
    "label_overlap": "Überlappung [mm]:",
    "label_white_stripe": "Weißer Streifen [mm]:",
    "label_add_white_stripe": "Weißen Streifen zur effektiven Überlappung hinzufügen",
    "label_layout": "Ausgabe-Layout:",
    "label_output_type": "Ausgabetyp:",
    "label_enable_reg_marks": "Passermarken aktivieren:",
    "label_enable_codes": "Codes aktivieren:",
    "label_enable_sep_lines": "Trennlinien aktivieren (zwischen Panels)",
    "label_enable_start_line": "Start-/Obere Linie des Bogens aktivieren",
    "label_enable_end_line": "End-/Untere Linie des Bogens aktivieren",
    "label_bryt_order": "Panel-Reihenfolge:",
    "label_slice_rotation": "Panel-Rotation:",
    "label_create_order_folder": "Ordner mit Auftragsnummer erstellen",

    # --- Bereiche/Rahmen (Start) ---
    "section_input_file": " Eingabedatei ",
    "section_scale_and_dimensions": " Skalierung und Ausgabegröße ",
    "label_original_size": "Originalgröße:",
    "label_scale_non_uniform": "Nicht proportional skalieren",
    "label_scale": "Maßstab: 1:",
    "label_scale_x": "Maßstab X: 1:",
    "label_scale_y": "Maßstab Y: 1:",
    "label_output_dimensions": "Ausgabedateiabmessungen:",
    "label_width_cm": "Breite [cm]:",
    "label_height_cm": "Höhe [cm]:",
    "section_split_settings": " Schneideeinstellungen ",
    "section_profiles": " Einstellungsprofile ",
    "section_save_location": " Speicherort ",
    "section_input_preview": " Vorschau der Eingabedatei ",
    "section_output_preview": " Vorschau der Ausgabedatei ",

    # --- Optionswerte ---
    "layout_vertical": "Vertikal",
    "layout_horizontal": "Horizontal",
    "output_common_sheet": "Gemeinsames Blatt",
    "output_separate_files": "Einzelne Dateien",
    "output_both": "Gemeinsames Blatt und einzelne Dateien",
    "output_common": "Gemeinsames Blatt",
    "output_separate": "Einzelne Dateien",
    "reg_mark_cross": "Kreuz",
    "reg_mark_line": "Linie",
    "code_qr": "QR-Code",
    "code_barcode": "Barcode",
    "bryt_order_1": "A1–An, B1–Bn … Standard, von oben",
    "bryt_order_2": "A1–An, Bn–B1 … Schlangenlinie nach Zeilen, von oben",
    "bryt_order_3": "A1..B1, A2..B2 … Nach Spalten, von oben",
    "bryt_order_4": "A1–A2..B2–B1 … Schlangenlinie nach Spalten, von oben",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … Standard, von unten",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … Schlangenlinie nach Zeilen, von unten",
    "logging_console": "Konsole",
    "logging_file": "Datei",
    "logging_both": "Beides",

    # --- Bereiche/Rahmen (Einstellungen) ---
    "section_processing_mode": " Schneidvorgänge ",
    "processing_mode_ram": "RAM (im Speicher)",
    "processing_mode_hdd": "HDD (auf Festplatte)",
    "graphic_settings": "Grafikeinstellungen",
    "code_settings": "QR-/Barcode-Einstellungen",
    "logging_settings": "Protokollierung",
    "barcode_text_position_label": "Position des Barcode-Textes:",
    "barcode_text_bottom": "unten",
    "barcode_text_side": "seitlich",
    "barcode_text_none": "keine",

    # --- Felder (Einstellungen – Grafik) ---
    "extra_margin_label": "Rand um Panels [mm]:",
    "margin_top_label": "Oberer Rand [mm]:",
    "margin_bottom_label": "Unterer Rand [mm]:",
    "margin_left_label": "Linker Rand [mm]:",
    "margin_right_label": "Rechter Rand [mm]:",
    "reg_mark_width_label": "Passermarke – Breite [mm]:",
    "reg_mark_height_label": "Passermarke – Höhe [mm]:",
    "reg_mark_white_line_width_label": "Passermarke – Weiße Linienbreite [mm]:",
    "reg_mark_black_line_width_label": "Passermarke – Schwarze Linienbreite [mm]:",
    "sep_line_black_width_label": "Trennlinie – Schwarze Linienbreite [mm]:",
    "sep_line_white_width_label": "Trennlinie – Weiße Linienbreite [mm]:",
    "slice_gap_label": "Abstand zwischen Panels [mm]:",
    "label_draw_slice_border": "Rand um Panel zeichnen (Schnittlinie)",

    # --- Felder (Einstellungen – Codes) ---
    "scale_label": "Größe [mm]:",
    "scale_x_label": "Breite X [mm]:",
    "scale_y_label": "Höhe Y [mm]:",
    "offset_x_label": "Versatz X [mm]:",
    "offset_y_label": "Versatz Y [mm]:",
    "rotation_label": "Drehung (°):",
    "anchor_label": "Ecke:",

    # --- Felder (Einstellungen – Logging) ---
    "logging_mode_label": "Protokollierungsmodus:",
    "log_file_label": "Logdatei:",
    "logging_level_label": "Log-Level:",

    # --- Buttons / Aktionen (Start) ---
    "button_load": "Laden",
    "button_save_settings": "Aktuelle Einstellungen speichern",
    "button_generate_pdf": "PDF erzeugen",
    "button_refresh_preview": "Vorschau aktualisieren",
    "button_refresh_layout": "Layout aktualisieren",

    # --- Lizenz (GUI) ---
    "hwid_frame_title": "Eindeutige Hardware-ID (HWID)",
    "copy_hwid": "HWID kopieren",
    "license_frame_title": "Lizenzaktivierung",
    "enter_license_key": "Lizenzschlüssel eingeben:",
    "activate": "Aktivieren",
    "status_trial": "Testmodus",
    "license_active": "Lizenz aktiv",

    # ================================================
    #  Meldungen (Fenster, Statusleiste)
    # ================================================

    # --- Profile ---
    "msg_no_profile_name": "Kein Name",
    "msg_enter_profile_name": "Bitte geben Sie einen Namen zum Speichern des Profils ein.",
    "msg_profile_saved": "Profil gespeichert",
    "profile_saved_title": "Profil gespeichert",
    "msg_profile_saved_detail": "Profil „{0}“ wurde gespeichert.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profil '{profile}' wurde gespeichert und angewendet.",
    "msg_no_profile": "Kein Profil",
    "warning_no_profile": "Kein Profil",
    "msg_select_profile": "Wählen Sie zum Laden einen Profilnamen aus der Liste.",
    "select_profile": "Wählen Sie zum Laden einen Profilnamen aus der Liste.",
    "profile_loaded_title": "Profil geladen",
    "profile_loaded": "Profil „{profile}“ wurde geladen.",
    "warning_no_profile_delete": "Kein Profil",
    "warning_no_profile_delete_message": "Wählen Sie zum Löschen ein Profil aus der Liste.",
    "profile_not_found": "Profil „{profile}“ wurde nicht gefunden.",
    "profile_not_exist": "Profil „{profile}“ existiert nicht.",
    "confirm_delete_title": "Löschen bestätigen",
    "confirm_delete_profile": "Möchten Sie das Profil „{profile}“ wirklich löschen?",
    "profile_deleted_title": "Profil gelöscht",
    "profile_deleted": "Profil „{profile}“ wurde gelöscht.",

    # --- Dateien / Verzeichnisse ---
    "msg_no_input_file": "Keine Eingabedatei",
    "msg_unsupported_format": "Nicht unterstütztes Format",
    "select_file_title": "Eingabedatei auswählen",
    "supported_files": "Unterstützte Dateien",
    "all_files": "Alle Dateien",
    "select_dir_title": "Ausgabeverzeichnis auswählen",
    "select_log_dir_title": "Verzeichnis für Logdateien auswählen",
    "error_output_dir_title": "Fehler im Ausgabeverzeichnis",
    "error_output_dir": "Das angegebene Ausgabeverzeichnis ist ungültig oder existiert nicht:\n{directory}",
    "error_input_file_title": "Fehler bei Eingabedatei",
    "error_input_file": "Die angegebene Eingabedatei ist ungültig oder existiert nicht:\n{file}",
    "save_file_error_title": "Fehler beim Speichern",
    "save_file_error": "Datei konnte nicht gespeichert werden: {error}",

    # --- PDF-Verarbeitung / Vorschau ---
    "msg_pdf_processing_error": "PDF-Datei konnte nicht verarbeitet werden",
    "msg_thumbnail_error": "Fehler beim Laden der Miniaturansicht",
    "msg_no_pdf_output": "Kein PDF-Ausgabedatei",
    "no_pdf_pages": "Keine Seiten in der PDF-Datei",
    "unsupported_output": "Nicht unterstützter Ausgabetyp für Vorschau",
    "pdf_generated_title": "Erzeugung abgeschlossen",
    "pdf_generated": "PDF-Datei(en) wurde(n) erfolgreich im Verzeichnis gespeichert:\n{directory}",
    "pdf_generation_error_title": "Erzeugungsfehler",
    "pdf_generation_error": "Beim Erzeugen des PDF ist ein Fehler aufgetreten. Prüfen Sie die Logs für weitere Informationen.",
    "critical_pdf_error_title": "Kritischer PDF-Erzeugungsfehler",
    "critical_pdf_error": "Ein kritischer Fehler trat bei der PDF-Erzeugung auf:\n{error}\nBitte prüfen Sie die Logs.",

    # --- Einstellungen ---
    "settings_saved_title": "Einstellungen gespeichert",
    "settings_saved": "Einstellungen wurden in die Datei gespeichert:\n{filepath}",
    "settings_save_error_title": "Fehler beim Speichern der Einstellungen",
    "settings_save_error": "Speichern der Einstellungen fehlgeschlagen: {error}",
    "conversion_error_title": "Konvertierungsfehler",
    "conversion_error": "Fehler beim Konvertieren von Werten aus der GUI: {error}",
    "update_gui_error_title": "GUI-Aktualisierungsfehler",
    "update_gui_error": "Beim Aktualisieren der Oberfläche ist ein Fehler aufgetreten: {error}",

    # --- Lizenz ---
    "hwid_copied_to_clipboard": "HWID wurde in die Zwischenablage kopiert",
    "computer_hwid": "Computer-HWID",
    "public_key_load_error": "Fehler beim Laden des öffentlichen Schlüssels: {error}",
    "invalid_license_format": "Ungültiges Lizenzformat: {error}",
    "activation_success": "Lizenz wurde erfolgreich aktiviert.",
    "activation_error": "Fehler bei der Lizenzaktivierung: {error}",
    "log_trial_mode_active": "Testmodus ist aktiv",
    "log_trial_mode_inactive": "Testmodus ist inaktiv",

    # --- Initialisierung ---
    "init_error_title": "Initialisierungsfehler",
    "init_error": "Fehler beim Initialisieren der Verzeichnisse: {error}",
    "poppler_path_info": "Poppler-Pfadinformationen",
    "ttkthemes_not_installed": "Warnung: Die Bibliothek ttkthemes ist nicht installiert. Standard-Tkinter-Stil wird verwendet.",

    # =====================================
    #  Logs (Protokollmeldungen)
    # =====================================

    # --- Allgemeine Protokollierung / Konfiguration ---
    "log_configured": "Logging konfiguriert: level={0}, mode={1}, file={2}",
    "log_no_handlers": "Warnung: Keine Logging-Handler konfiguriert (Modus: {0}).",
    "log_critical_error": "Kritischer Fehler in der Logging-Konfiguration: {0}",
    "log_basic_config": "Aufgrund eines Fehlers wurde die Basis-Logging-Konfiguration verwendet.",
    "log_dir_create_error": "Kritischer Fehler: Protokollverzeichnis {0} kann nicht erstellt werden: {1}",

    # --- Initialisierung / Verzeichnisse (init_directories.py) ---
    "error_critical_init": "KRITISCHER FEHLER während der Initialisierung: {0}",
    "logger_init_error": "Fehler bei der Verzeichnisinitialisierung: {error}",
    "directory_created": "Verzeichnis erstellt: {0}",
    "directory_creation_error": "Verzeichnis {0} konnte nicht erstellt werden: {1}",
    "sample_file_copied": "Beispieldatei wurde nach {0} kopiert",
    "sample_file_copy_error": "Fehler beim Kopieren der Beispieldatei: {0}",
    "log_created_output_dir": "Ausgabeverzeichnis erstellt: {0}",
    "log_cannot_create_output_dir": "Ausgabeverzeichnis {0} kann nicht erstellt werden: {1}",

    # --- Splitter (splitter.py) ---
    #   Splitter – Initialisierung & Laden
    "log_graphic_settings_error": "Grafikeinstellungen konnten während der Initialisierung nicht geladen werden: {0}",
    "log_loading_pdf": "PDF-Datei wird geladen: {0}",
    "log_loading_bitmap": "Bitmap-Datei wird geladen: {0}",
    "log_invalid_dpi": "Ungültiger DPI-Wert gelesen ({0}). Standard {1} DPI wird verwendet.",
    "log_image_dimensions": "Bildabmessungen: {0}×{1}px, Modus: {2}, DPI: {3:.1f} -> {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Bild wird mit ursprünglichem Farbmodus verarbeitet: {0}",
    "log_unusual_color_mode": "Ungewöhnlicher Farbmodus: „{0}“. ReportLab/Pillow könnten Probleme haben.",
    "log_draw_image_error": "Fehler bei ReportLab drawImage für Modus {0}: {1}",
    "log_unsupported_format": "Nicht unterstütztes Eingabeformat: {0}",
    "log_input_file_not_found": "Eingabedatei nicht gefunden: {0}",
    "log_load_process_error": "Fehler beim Laden/Verarbeiten der Datei {0}: {1}",
    "log_input_file_not_exists": "Eingabedatei existiert nicht oder Pfad ist leer: „{0}“",
    "log_cannot_load_or_empty_pdf": "Eingabedatei kann nicht geladen werden oder PDF ist leer/beschädigt.",
    "log_pdf_dimensions_info": "  PDF-Abmessungen: {0:.1f}mm × {1:.1f}mm",
    "log_invalid_pdf_dimensions": "Ungültige PDF-Seitenabmessungen: {0}×{1} pt.",

    #   Splitter – Maßberechnungen
    "log_extra_margin": "Zusätzlicher Rand: {0:.3f} pt",
    "log_invalid_rows_cols": "Ungültige Anzahl Zeilen ({0}) oder Spalten ({1}).",
    "error_invalid_rows_cols": "Zeilen und Spalten müssen positive ganze Zahlen sein.",
    "log_invalid_overlap_white_stripe": "Ungültige Werte für Überlappung ({0}) oder weißen Streifen ({1}).",
    "error_invalid_overlap_white_stripe": "Überlappung und weißer Streifen müssen numerisch sein (mm).",
    "log_stripe_usage": "use_white_stripe={0}, white_stripe={1:.3f} mm gesetzt",
    "log_effective_overlap": "Basis-Überlappung (Grafik): {0:.3f} mm, Weißer Streifen: {1:.3f} mm, Effektive Überlappung: {2:.3f} mm",
    "log_computed_dimensions": "Berechnete Abmessungen: PDF: {0:.3f}mm × {1:.3f}mm. Panel: {2:.3f}pt ({3:.3f}mm) × {4:.3f}pt ({5:.3f}mm). Kern: {6:.3f}pt × {7:.3f}pt. Effektive Überlappung: {8:.3f}mm",
    "log_invalid_dimensions": "Ungültige Panel- ({0:.3f}×{1:.3f}) oder Kernabmessungen ({2:.3f}×{3:.3f}) bei overlap={4}, stripe={5}, r={6}, c={7}, W={8}mm, H={9}mm",
    "error_invalid_slice_dimensions": "Berechnete Panel-/Kernabmessungen sind ungültig oder negativ.",

    #   Splitter – Panelinfos & Reihenfolge
    "log_generating_slice_info": "Panel-Informationen werden erstellt: {0}",
    "log_no_slices_info_generated": "Panel-Informationen konnten nicht erstellt werden.",
    "log_applying_rotated_order": "Reihenfolge für 180°-Rotation wird angewendet: {0}",
    "log_applying_standard_order": "Reihenfolge für 0°-Rotation (Standard) wird angewendet: {0}",
    "log_unknown_bryt_order": "Unbekannte Panel-Reihenfolge: „{0}“. Standard wird verwendet.",
    "log_final_slices_order": "  Endgültige Panel-Reihenfolge ({0}): [{1}]",

    #   Splitter – Overlays & Zusammenführen
    "log_invalid_dimensions_overlay": "Overlay mit ungültigen Abmessungen versucht: {0}. Übersprungen.",
    "log_empty_overlay": "Leeres oder nahezu leeres Overlay-PDF erstellt. Zusammenführung übersprungen.",
    "log_overlay_error": "Fehler beim Erstellen des Overlay-PDF: {0}",
    "log_merge_error": "Versuch, Overlay ohne Seiten zusammenzuführen. Übersprungen.",
    "log_merge_page_error": "Fehler beim Zusammenführen des Overlay-PDF: {0}",
    "log_fallback_draw_rotating_elements": "Konnte Zeilen/Spalten für _draw_rotating_elements nicht bestimmen, 1×1 verwendet.",
    "log_overlay_created_for_slice": "Overlay (Streifen/Marken) für Panel {0} erstellt",
    "log_overlay_creation_failed_for_slice": "Overlay (Streifen/Marken) für {0} fehlgeschlagen",
    "log_merging_rotated_overlay": "ROTIERENDES Overlay (Streifen/Marken) für {0} wird zusammengeführt, T={1}",
    "log_merging_nonrotated_overlay": "NICHT ROTIERENDES Overlay (Streifen/Marken) für {0} wird zusammengeführt",
    "log_merging_all_codes_overlay": "Overlay aller Codes (ohne Rotation) wird zusammengeführt",
    "log_merging_separation_lines_overlay": "Overlay der Trennlinien (ohne Rotation) wird zusammengeführt",
    "log_merging_code_overlay_for_slice": "Code-Overlay für {0} ohne Rotation zusammengeführt.",
    "log_merging_separation_overlay_for_slice": "Trennlinien-Overlay für {0} ohne Rotation zusammengeführt.",

    #   Splitter – Grafische Elemente (Streifen, Marken, Linien)
    "log_drawing_top_stripe": "[Canvas] Oberen Streifen für {0} zeichnen: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Rechten Streifen für {0} zeichnen: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Ecke für {0} füllen und umranden @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Zentriertes Kreuz zeichnen @ ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Passerlinien für {0} im Bereich ab ({1:.3f},{2:.3f}) zeichnen",
    "log_drawing_right_vertical_line": "  Rechte Vertikallinie: x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  Obere Horizontallinie: y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "Trennlinie (weiß auf schwarz) zeichnen: ({0}) @ ({1:.3f}, {2:.3f}), Länge={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Kreuze für {0} [{1},{2}] / [{3},{4}] im Bereich ab ({5:.1f},{6:.1f}) zeichnen",
    "log_coord_calculation": "  Berechnete Zentren: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    TL zeichnen @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    TR zeichnen @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    BL zeichnen @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    BR zeichnen @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    {0} gemäß Regel für Position [{1},{2}] ausgelassen",
    "log_trial_common_sheet": "TRIAL-Wasserzeichen auf gemeinsamem Blatt anwenden",

    # Wasserzeichen
    "log_trial_watermark_added": "TRIAL-Wasserzeichen wurde hinzugefügt",
    "error_drawing_trial_text": "Fehler beim Zeichnen des Wasserzeichens: {error}",

    #   Trennlinien (ganze Seite)
    "log_drawing_separation_lines_for_page": "Trennlinien für Seite zeichnen (layout={0}, total_slices={1}, slice_index={2})",
    "log_vertical_line_between_slices": "  Vertikale Linie zwischen Panels {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Vertikallinie Start @ x={0:.1f}",
    "log_vertical_line_end": "  Vertikallinie Ende @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Horizontale Linie zwischen Panels {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Horizontallinie Start @ y={0:.1f}",
    "log_horizontal_line_end": "  Horizontallinie Ende @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Einzeldateien) Vertikal-/Horizontallinie Start @ {0:.1f}",
    "log_sep_line_end_separate": "  (Einzeldateien) Vertikal-/Horizontallinie Ende @ {0:.1f}",

    #   Barcodes / QR
    "log_generate_barcode_data": "Barcode-Daten erzeugen: {0}",
    "log_barcode_data_shortened": "Barcode-Daten auf {0} Zeichen gekürzt.",
    "log_barcode_data_error": "Fehler beim Erzeugen der Barcode-Daten: {0}",
    "log_compose_barcode_payload": "Barcode-Payload zusammensetzen ({0}): {1}",
    "log_barcode_payload_shortened": "Payload auf {0} Zeichen gekürzt (Format {1})",
    "log_barcode_payload_error": "Fehler beim Zusammenstellen der Payload: {0}",
    "log_unknown_anchor_fallback": "Unbekannte Ecke „{0}“, links unten wird verwendet",
    "log_used_default_code_settings": "„default“-Einstellungen für Code {0}/{1} verwendet.",
    "log_no_layout_key_fallback": "Kein Layout „{0}“ für {1}/{2}. Erstes verfügbares Layout verwendet: „{3}“.",
    "log_code_settings_error": "Nicht gefunden oder Fehler beim Lesen der Code-Einstellungen ({0}/{1}/{2}): {3}. Standardwerte verwendet.",
    "log_drawing_barcode": "{0} bei ({1:.3f}, {2:.3f}) zeichnen [Basis ({3:.3f}, {4:.3f}) + Versatz ({5:.3f}, {6:.3f})], Drehung: {7}°",
    "error_generate_qr_svg": "QR-SVG konnte nicht erzeugt werden.",
    "error_invalid_scale_for_qr": "Ungültige QR-Größe: {0}mm",
    "error_invalid_qr_scale_factor": "Ungültiger QR-Skalierungsfaktor: {0}",
    "error_generate_barcode_svg": "Barcode-SVG konnte nicht erzeugt werden.",
    "error_invalid_scale_for_barcode": "Ungültige Barcode-Größe: {0}×{1}mm",
    "error_invalid_barcode_scale_factor": "Ungültiger Barcode-Skalierungsfaktor: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: Skalierungskonfig={1:.3f}mm, SVG-Breite={2:.3f}pt, sf={3:.4f}",
    "log_barcode_scale_code128": "  {0}: Skalierungskonfig=({1:.3f}mm, {2:.3f}mm), SVG-Größe=({3:.3f}pt, {4:.3f}pt), sf=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Fehler beim Zeichnen des Codes „{0}“: {1}",
    "log_prepared_barcode_info": "Code-Infos für {0} vorbereitet ({1}, anchor={2}): absolute Basisposition ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Fehler beim Vorbereiten der Code-Daten für {0}: {1}",
    "log_drawing_barcodes_count": "{0} Barcodes/QR-Codes werden gezeichnet…",
    "log_missing_barcode_info_key": "Fehlender Schlüssel in Code-Infos beim Zeichnen: {0}. Infos: {1}",
    "log_error_drawing_barcode_in_draw_all": "Fehler beim Zeichnen des Codes „{0}“ in _draw_all_barcodes: {1}",

    #   Split-Prozess (split_*)
    "log_start_splitting_process": "--- Split-Prozess starten für: {0} ---",
    "log_split_settings": "  Einstellungen: {0}×{1} Panels, Überlappung={2}mm, Weißer Streifen={3}mm (+Überlappung: {4})",
    "log_output_dir_info": "  Ausgabe: {0} / {1} nach „{2}“",
    "log_lines_marks_barcodes_info": "  Linien: Trennung={0}, Start={1}, Ende={2} | Marken: {3} ({4}), Codes: {5} ({6})",
    "log_bryt_order_info": "  Reihenfolge: {0}, Panel-Rotation: {1}°",
    "log_invalid_dimensions_in_slice_info": "Ungültige Abmessungen in slice_info für {0}: {1}×{2}",
    "log_content_transform": "Inhaltstransformation T_content für {0}: {1}",
    "log_merged_content_for_slice": "Inhalt für Panel {0} auf new_page zusammengeführt",
    "log_slice_reader_created": "Vollständiger Slice (PdfReader) für Panel {0} erstellt",
    "log_slice_reader_creation_error": "Fehler beim Erstellen des vollständigen Slices für Panel {0}: {1}",
    "log_used_get_transform": "_get_transform verwendet (nur Translation): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Start: EINZELDATEIEN (Rotation in create_slice_reader behandelt) ---",
    "log_creating_file_for_slice": "Datei für Panel {0} wird erstellt: {1}",
    "log_invalid_page_size_for_slice": "Ungültige Seitengröße ({0}×{1}) für {2}. Übersprungen.",
    "log_blank_page_creation_error": "Fehler beim Erstellen der Seite für {0} (Größe {1}×{2}): {3}. Übersprungen.",
    "log_transform_for_slice": "Transformation T (nur Translation) für {0}: {1}",
    "log_merging_complete_slice": "Vollständiges Panel {0} wird mit Transformation zusammengeführt: {1}",
    "log_skipped_slice_merging": "Zusammenführung des vollständigen Panels für {0} übersprungen.",
    "log_file_saved": "Datei gespeichert: {0}",
    "log_file_save_error": "Dateispeicherfehler {0}: {1}",
    "log_finished_split_separate_files": "--- Fertig: EINZELDATEIEN (gespeichert {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Keine Panels in split_horizontal zu verarbeiten.",
    "log_start_split_horizontal": "--- Start: GEMEINSAMES BLATT – HORIZONTAL (Rotation in create_slice_reader) ---",
    "log_page_dimensions": "Seitenabmessungen: {0:.1f}mm × {1:.1f}mm ({2} Panels)",
    "log_page_creation_error": "Fehler beim Erstellen der Ergebnisseite ({0}×{1}): {2}. Abbruch.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformation T (nur Translation) für {0}: {1}",
    "log_merging_complete_bryt": "Vollständiges Panel {0} wird zusammengeführt: {1}",
    "log_skipped_merging_bryt": "Zusammenführung des vollständigen Panels für {0} übersprungen.",
    "log_file_result_saved": "Ergebnisdatei gespeichert: {0}",
    "log_file_result_save_error": "Fehler beim Speichern der Ergebnisdatei {0}: {1}",
    "log_finished_split_horizontal": "--- Fertig: GEMEINSAMES BLATT – HORIZONTAL ---",
    "log_no_slices_split_vertical": "Keine Panels in split_vertical zu verarbeiten.",
    "log_start_split_vertical": "--- Start: GEMEINSAMES BLATT – VERTIKAL (Rotation in create_slice_reader) ---",
    "log_finished_split_vertical": "--- Fertig: GEMEINSAMES BLATT – VERTIKAL ---",
    "log_unknown_layout": "Unbekanntes Layout für gemeinsames Blatt: „{0}“.",
    "log_unknown_output_type": "Unbekannter Ausgabetyp: „{0}“.",
    "log_finished_splitting_success": "--- Split-Prozess beendet: {0} – ERFOLG ---",
    "log_finished_splitting_errors": "--- Split-Prozess beendet: {0} – FEHLER AUFGETRETEN ---",
    "log_value_error_in_splitting": "Eingabedaten- oder Berechnungsfehler: {0}",
    "log_finished_splitting_critical_error": "--- Split-Prozess beendet: {0} – KRITISCHER FEHLER ---",
    "log_unexpected_error_in_splitting": "Unerwarteter Fehler beim Splitten der Datei {0}: {1}",

    #   Testmodus (__main__)
    "log_script_mode_test": "splitter.py als Hauptskript (Testmodus) gestartet.",
    "log_loaded_config": "Konfiguration geladen.",
    "log_error_loading_config": "Konfiguration konnte nicht geladen werden: {0}",
    "log_created_example_pdf": "Beispiel-PDF erstellt: {0}",
    "log_cannot_create_example_pdf": "Beispiel-PDF konnte nicht erstellt werden: {0}",
    "log_start_test_split": "Test-Split starten: {0} nach {1}",
    "log_test_split_success": "Test-Split erfolgreich abgeschlossen.",
    "log_test_split_errors": "Test-Split mit Fehlern abgeschlossen.",

    # --- QR/Barcode (barcode_qr.py) ---
    "log_qr_empty_data": "Versuch, QR-Code für leere Daten zu erzeugen.",
    "log_qr_generated": "QR-Code-SVG erzeugt für: {0}…",
    "log_qr_error": "Fehler beim Erzeugen des QR-Codes für „{0}“: {1}",
    "log_barcode_empty_data": "Versuch, Barcode für leere Daten zu erzeugen.",
    "log_barcode_generated": "Barcode-SVG erzeugt für: {0}…",
    "log_barcode_error": "Fehler beim Erzeugen des Barcodes für {0}: {1}",
    "log_basic_handler_configured": "Basis-Handler für Logger in barcode_qr.py konfiguriert",
    "log_basic_handler_error": "Fehler beim Konfigurieren des Basis-Handlers in barcode_qr: {0}",

    # --- Profile/Config (main_config_manager.py) ---
    "loading_profiles_from": "Profile werden geladen von",
    "profiles_file": "Profildatei",
    "does_not_contain_dict": "enthält kein Dictionary. Es wird eine neue angelegt",
    "not_found_creating_new": "nicht gefunden. Es wird eine leere angelegt",
    "json_profiles_read_error": "Fehler beim Lesen der JSON-Profildatei",
    "file_will_be_overwritten": "Datei wird beim Speichern überschrieben",
    "json_decode_error_in_profiles": "JSON-Decode-Fehler in Profildatei",
    "cannot_load_profiles_file": "Profildatei kann nicht geladen werden",
    "unexpected_profiles_read_error": "Unerwarteter Fehler beim Lesen der Profile",
    "saving_profiles_to": "Profile werden gespeichert nach",
    "cannot_save_profiles_file": "Profildatei kann nicht gespeichert werden",
    "profiles_save_error": "Fehler beim Speichern der Profildatei",
    "logger_profile_saved": "Profil gespeichert: {profile}",
    "logger_profile_not_found": "Profil zum Laden nicht gefunden: {profile}",
    "logger_profile_loaded": "Profil geladen: {profile}",
    "logger_profile_delete_not_exist": "Versuch, nicht existentes Profil zu löschen: {profile}",
    "logger_profile_deleted": "Profil gelöscht: {profile}",
    "logger_start_save_settings": "Speichern der Einstellungen aus der GUI gestartet.",
    "logger_invalid_value": "Ungültiger Wert für „{key}“. Auf 0.0 gesetzt.",
    "logger_end_save_settings": "Speichern der Einstellungen aus der GUI abgeschlossen.",
    "logger_conversion_error": "Fehler bei der Umwandlung von GUI-Werten: {error}",
    "conversion_failed": "Konvertierung der GUI-Werte fehlgeschlagen",
    "logger_unexpected_save_error": "Unerwarteter Fehler beim Speichern der Einstellungen: {error}",
    "logger_settings_saved": "Einstellungen in Datei gespeichert: {file}",

    # --- Lizenzierung (main_license.py) ---
    "public_key_load_error_log": "Fehler beim Laden des öffentlichen Schlüssels",
    "license_key_decode_error": "Fehler beim Dekodieren des Lizenzschlüssels",
    "license_activation_error": "Fehler bei der Lizenzaktivierung",

    # --- Hauptmodul (main.py) ---
    "ui_created": "Benutzeroberfläche wurde erstellt.",
    "error_tab_home": "Fehler beim Erstellen des „Start“-Tabs",
    "error_tab_settings": "Fehler beim Erstellen des „Einstellungen“-Tabs",
    "error_tab_help": "Fehler beim Erstellen des „Hilfe“-Tabs",
    "error_creating_license_ui": "Fehler beim Erstellen des „Lizenz“-Tabs",
    "error_loading_ui": "Fehler beim Laden der Oberfläche: {error}",
    "error_creating_home_ui": "Fehler beim Erstellen des „Start“-Tabs",
    "error_creating_settings_ui": "Fehler beim Erstellen des „Einstellungen“-Tabs",
    "error_creating_help_ui": "Fehler beim Erstellen des „Hilfe“-Tabs",
    "logger_update_gui": "Aktualisierung der GUI aus der Konfiguration gestartet.",
    "logger_end_update_gui": "Aktualisierung der GUI aus der Konfiguration abgeschlossen.",
    "logger_update_gui_error": "Unerwarteter Fehler beim Aktualisieren der GUI: {error}",
    "logger_invalid_output_dir": "Ungültiges oder nicht existentes Ausgabeverzeichnis: {directory}",
    "logger_invalid_input_file": "Ungültige oder nicht existente Eingabedatei: {file}",
    "logger_start_pdf": "PDF-Erzeugung gestartet.",
    "logger_pdf_save_error": "PDF-Erzeugung abgebrochen – Speichern der aktuellen Einstellungen fehlgeschlagen.",
    "logger_pdf_success": "PDF-Erzeugung erfolgreich abgeschlossen.",
    "logger_pdf_exception": "Ausnahme während des Haupt-PDF-Erzeugungsprozesses.",
    "icon_set_error": "Anwendungssymbol konnte nicht gesetzt werden: {error}",
    "accent_button_style_error": "Stil für Akzent-Button konnte nicht gesetzt werden: {error}",
    "logger_file_save_error": "Dateispeicherfehler {file}: {error}",

    # --- Vorschau (main.py – update_preview, update_output_preview) ---
    "thumbnail_error_log": "Fehler bei der Miniaturbilderstellung",
    "output_preview_update_called": "Aktualisierung der Ausgabevorschau aufgerufen",
    "output_preview_canvas_missing": "Canvas der Ausgabevorschau fehlt",
    "pdf_found_in_output_dir": "PDF im Ausgabeverzeichnis gefunden",
    "preparing_thumbnail": "Miniatur wird vorbereitet",
    "thumbnail_generated_successfully": "Miniatur erfolgreich erzeugt",
    "thumbnail_generation_error": "Fehler bei der Miniaturerzeugung für",
    "no_pdf_for_common_sheet": "Kein PDF für Vorschau des gemeinsamen Blatts",
    "no_pdf_for_separate_files": "Keine erzeugten Einzel-PDFs für die Vorschau",
    "cannot_load_thumbnail": "Miniatur kann nicht geladen werden aus",

    # --- Entwickler / GUI intern (main.py) ---
    "missing_gui_var_created": "Fehlende GUI-Variable für Schlüssel erstellt: {key}",
    "missing_gui_structure_created": "Fehlende GUI-Struktur erstellt für: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Fehlende GUI-Variable erstellt für: {code_type}/{output_type}/{layout}/{param}",

    # --- Hilfe (main_ui_help.py) ---
    "help_text": """
    Billboard Splitter – Benutzerhandbuch\n\n
    Zweck des Programms:\n
    Billboard Splitter dient zum automatischen Zuschneiden von Billboard-Projekten in druckfertige Panels.
    Das Programm ist für Dateien im Maßstab 1:10 ausgelegt.\n
    Werte in den Bereichen: Überlappung, Weißer Streifen, Einstellungen werden im Maßstab 1:1 eingegeben.\n
    Das Programm kann die zugeschnittenen Panels je nach gewähltem Layout auf PDF-Seiten anordnen:\n
    • Gemeinsames Blatt: Alle Panels in einem Dokument.\n
    • Einzelne Dateien: Jedes Panel wird als separate PDF-Datei gespeichert.\n\n
    Zusätzlich ermöglicht das Programm:\n
    • Layout-Auswahl – vertikal oder horizontal (entsprechend erscheinen die Trennlinien im vertikalen Layout oben/unten, im horizontalen links/rechts).\n
    • Panels um 180° zu drehen (gesamtes Projekt spiegeln).\n
    • Passermarken (z. B. Kreuze oder Linien) hinzuzufügen, um das präzise Positionieren beim Verkleben zu erleichtern.\n
    • QR-Codes oder Barcodes hinzuzufügen – basierend auf Eingabedaten zur Identifikation einzelner Panels.\n
    • Einstellungen als Profile zu speichern, zu laden, zu ändern und zu löschen, um schnell zwischen Projektkonfigurationen zu wechseln.\n\n
    Schritte zur Nutzung:\n\n
    1. Eingabedatei wählen:\n
    • Im Tab „Start“ eine PDF-, JPG- oder TIFF-Datei mit dem Billboard-Design wählen.\n
    • Ohne eigenen Pfad setzt das Programm eine Beispieldatei.\n\n
    2. Schneideeinstellungen:\n
    • Anzahl der Zeilen und Spalten angeben, in die das Projekt geteilt wird.\n
    • Überlappung festlegen.\n
    • Optional die Breite des weißen Streifens angeben, der zur effektiven Überlappung addiert wird.\n\n
    3. Ausgabe-Layout wählen:\n
    • Vertikal: Alle Panels werden vertikal auf einer PDF-Seite angeordnet.\n
    • Horizontal: Alle Panels werden horizontal auf einer PDF-Seite angeordnet.\n\n
    4. Ausgabetyp wählen:\n
    • Gemeinsames Blatt: Alle Panels in einem gemeinsamen PDF.\n
    • Einzelne Dateien: Jedes Panel als separate PDF.\n
    • Passermarken im Tab „Start“ aktivieren/konfigurieren – Kreuz oder Linie.\n
    • Optional QR-/Barcodes aus Projektdaten aktivieren.\n
    • Code-Parameter (Skalierung, Versatz, Rotation, Position) im Tab „Einstellungen“ feinjustieren.\n\n
    5. Einstellungen verwalten:\n
    • Im Tab „Einstellungen“ Grafikparameter (Ränder, Linienstärken, Abstände) und Codes präzise ändern.\n
    • Aktuelle Einstellungen als Profil speichern und später laden/ändern.\n
    • Profile (gespeichert in profiles.json) erlauben schnelles Umschalten zwischen Konfigurationen.\n\n
    6. PDF erzeugen:\n
    • Nach der Konfiguration „PDF erzeugen“ klicken.\n
    • Ergebnisdateien werden im Ordner „output“ (oder benutzerdefiniert) gespeichert, Logs (tägliche Rotation) im Ordner „logs“ (oder benutzerdefiniert).\n\n
    Bei Problemen:\n
    • Logs im Ordner „logs“ prüfen. Es wird täglich eine Datei mit Datum erzeugt.\n
    • Sicherstellen, dass alle benötigten Ordner vorhanden sind.\n
    • Technischer Support: tech@printworks.pl (Werktage 8–16)\n
    """
}
