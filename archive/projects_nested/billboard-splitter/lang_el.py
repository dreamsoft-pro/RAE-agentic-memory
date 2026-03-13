# lang_el.py
"""
Αρχείο μεταφράσεων για την ελληνική γλώσσα.
"""

LANG = {
    "barcode_font_size_label": "Μέγεθος γραμματοσειράς περιγραφής γραμμωτού κώδικα [pt]:",
    # ==========================
    #  Εφαρμογή – Γενικά
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Σφάλμα",
    "no_file": "Δεν υπάρχει αρχείο",
    "language": "Γλώσσα",
    "language_switch": "Αλλαγή γλώσσας",
    "choose_language": "Επιλέξτε γλώσσα:",
    "apply_language": "Εφαρμογή",
    "language_changed": "Η γλώσσα άλλαξε. Ορισμένες αλλαγές θα εμφανιστούν μετά την επανεκκίνηση της εφαρμογής.",

    # ========================================
    #  Γραφικό περιβάλλον (GUI)
    # ========================================

    # --- Κύριες καρτέλες ---
    "tab_home": " Αρχική ",
    "tab_settings": " Ρυθμίσεις ",
    "tab_help": " Βοήθεια ",
    "tab_license": " Άδεια ",

    # --- Γενικά κουμπιά ---
    "button_browse": "Περιήγηση...",
    "browse_folder": "Περιήγηση φακέλου...",
    "button_save": "Αποθήκευση",
    "button_delete": "Διαγραφή",
    "button_close": "Κλείσιμο",
    "save_all_settings": "Αποθήκευση όλων των ρυθμίσεων",

    # --- Ετικέτες πεδίων (Αρχική) ---
    "label_rows": "Κάθετος διαχωρισμός (σειρές):",
    "label_columns": "Οριζόντιος διαχωρισμός (στήλες):",
    "label_overlap": "Επικάλυψη [mm]:",
    "label_white_stripe": "Λευκή λωρίδα [mm]:",
    "label_add_white_stripe": "Προσθήκη λευκής λωρίδας στην αποτελεσματική επικάλυψη",
    "label_layout": "Διάταξη εξόδου:",
    "label_output_type": "Τύπος εξόδου:",
    "label_enable_reg_marks": "Ενεργοποίηση σημάτων καταχώρισης:",
    "label_enable_codes": "Ενεργοποίηση κωδικών:",
    "label_enable_sep_lines": "Ενεργοποίηση γραμμών διαχωρισμού (μεταξύ πάνελ)",
    "label_enable_start_line": "Ενεργοποίηση γραμμής αρχής/άνω άκρου φύλλου",
    "label_enable_end_line": "Ενεργοποίηση γραμμής τέλους/κάτω άκρου φύλλου",
    "label_bryt_order": "Σειρά πάνελ:",
    "label_slice_rotation": "Περιστροφή πάνελ:",
    "label_create_order_folder": "Δημιουργία φακέλου με αριθμό παραγγελίας",

    # --- Ενότητες (Αρχική) ---
    "section_input_file": " Αρχείο εισόδου ",
    "section_scale_and_dimensions": " Κλίμακα και διαστάσεις εξόδου ",
    "label_original_size": "Αρχικό μέγεθος:",
    "label_scale_non_uniform": "Μη αναλογική κλιμάκωση",
    "label_scale": "Κλίμακα: 1:",
    "label_scale_x": "Κλίμακα X: 1:",
    "label_scale_y": "Κλίμακα Y: 1:",
    "label_output_dimensions": "Διαστάσεις αρχείου εξόδου:",
    "label_width_cm": "Πλάτος [cm]:",
    "label_height_cm": "Ύψος [cm]:",
    "section_split_settings": " Ρυθμίσεις κοπής ",
    "section_profiles": " Προφίλ ρυθμίσεων ",
    "section_save_location": " Θέση αποθήκευσης ",
    "section_input_preview": " Προεπισκόπηση εισόδου ",
    "section_output_preview": " Προεπισκόπηση εξόδου ",

    # --- Τιμές επιλογών ---
    "layout_vertical": "Κάθετα",
    "layout_horizontal": "Οριζόντια",
    "output_common_sheet": "Κοινό φύλλο",
    "output_separate_files": "Ξεχωριστά αρχεία",
    "output_both": "Κοινό φύλλο και ξεχωριστά αρχεία",
    "output_common": "Κοινό φύλλο",
    "output_separate": "Ξεχωριστά αρχεία",
    "reg_mark_cross": "Σταυρός",
    "reg_mark_line": "Γραμμή",
    "code_qr": "QR κωδικός",
    "code_barcode": "Γραμμωτός κώδικας",
    "bryt_order_1": "A1–An, B1–Bn, .. Τυπικό, από πάνω",
    "bryt_order_2": "A1–An, Bn–B1, .. Φιδωτό ανά σειρά, από πάνω",
    "bryt_order_3": "A1..B1, A2..B2, .. Κατά στήλες, από πάνω",
    "bryt_order_4": "A1–A2..B2–B1.. Φιδωτό κατά στήλες, από πάνω",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Τυπικό, από κάτω",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Φιδωτό ανά σειρά, από κάτω",
    "logging_console": "κονσόλα",
    "logging_file": "αρχείο",
    "logging_both": "και τα δύο",

    # --- Ενότητες (Ρυθμίσεις) ---
    "section_processing_mode": " Τρόποι επεξεργασίας ",
    "processing_mode_ram": "RAM (στη μνήμη)",
    "processing_mode_hdd": "Δίσκος (αποθήκευση)",
    "graphic_settings": "Γραφικές ρυθμίσεις",
    "code_settings": "Ρυθμίσεις QR/γραμμωτού κώδικα",
    "logging_settings": "Ρυθμίσεις καταγραφής",
    "barcode_text_position_label": "Θέση κειμένου δίπλα στον κωδικό:",
    "barcode_text_bottom": "κάτω",
    "barcode_text_side": "πλάγια",
    "barcode_text_none": "καθόλου",

    # --- Ετικέτες (Ρυθμίσεις – Γραφικά) ---
    "extra_margin_label": "Περιθώριο γύρω από τα πάνελ [mm]:",
    "margin_top_label": "Άνω περιθώριο [mm]:",
    "margin_bottom_label": "Κάτω περιθώριο [mm]:",
    "margin_left_label": "Αριστερό περιθώριο [mm]:",
    "margin_right_label": "Δεξί περιθώριο [mm]:",
    "reg_mark_width_label": "Σήμα καταχώρισης – πλάτος [mm]:",
    "reg_mark_height_label": "Σήμα καταχώρισης – ύψος [mm]:",
    "reg_mark_white_line_width_label": "Σήμα – πάχος λευκής γραμμής [mm]:",
    "reg_mark_black_line_width_label": "Σήμα – πάχος μαύρης γραμμής [mm]:",
    "sep_line_black_width_label": "Διαχωριστική – πάχος μαύρης γραμμής [mm]:",
    "sep_line_white_width_label": "Διαχωριστική – πάχος λευκής γραμμής [mm]:",
    "slice_gap_label": "Κενό μεταξύ πάνελ [mm]:",
    "label_draw_slice_border": "Σχεδίαση περιγράμματος γύρω από το πάνελ (γραμμή κοπής)",

    # --- Ετικέτες (Ρυθμίσεις – Κωδικοί) ---
    "scale_label": "Μέγεθος [mm]:",
    "scale_x_label": "Πλάτος X [mm]:",
    "scale_y_label": "Ύψος Y [mm]:",
    "offset_x_label": "Μετατόπιση X [mm]:",
    "offset_y_label": "Μετατόπιση Y [mm]:",
    "rotation_label": "Περιστροφή (°):",
    "anchor_label": "Γωνία:",

    # --- Ετικέτες (Ρυθμίσεις – Καταγραφή) ---
    "logging_mode_label": "Λειτουργία καταγραφής:",
    "log_file_label": "Αρχείο log:",
    "logging_level_label": "Επίπεδο καταγραφής:",

    # --- Κουμπιά / ενέργειες (Αρχική) ---
    "button_load": "Φόρτωση",
    "button_save_settings": "Αποθήκευση τρεχουσών ρυθμίσεων",
    "button_generate_pdf": "Δημιουργία PDF",
    "button_refresh_preview": "Ανανέωση προεπισκόπησης",
    "button_refresh_layout": "Ανανέωση διάταξης",

    # --- Άδεια (GUI) ---
    "hwid_frame_title": "Μοναδικός αναγνωριστικός κωδικός υλικού (HWID)",
    "copy_hwid": "Αντιγραφή HWID",
    "license_frame_title": "Ενεργοποίηση άδειας",
    "enter_license_key": "Εισαγάγετε κλειδί άδειας:",
    "activate": "Ενεργοποίηση",
    "status_trial": "Δοκιμαστική λειτουργία",
    "license_active": "Η άδεια είναι ενεργή",

    # ================================================
    #  Μηνύματα προς τον χρήστη (διαλόγοι, γραμμή κατάστασης)
    # ================================================

    # --- Προφίλ ---
    "msg_no_profile_name": "Χωρίς όνομα",
    "msg_enter_profile_name": "Εισαγάγετε όνομα προφίλ για αποθήκευση.",
    "msg_profile_saved": "Το προφίλ αποθηκεύτηκε",
    "profile_saved_title": "Το προφίλ αποθηκεύτηκε",
    "msg_profile_saved_detail": "Το προφίλ «{0}» αποθηκεύτηκε.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Το προφίλ '{profile}' αποθηκεύτηκε και εφαρμόστηκε.",
    "msg_no_profile": "Δεν υπάρχει προφίλ",
    "warning_no_profile": "Δεν υπάρχει προφίλ",
    "msg_select_profile": "Επιλέξτε όνομα προφίλ από τη λίστα για φόρτωση.",
    "select_profile": "Επιλέξτε όνομα προφίλ από τη λίστα για φόρτωση.",
    "profile_loaded_title": "Το προφίλ φορτώθηκε",
    "profile_loaded": "Το προφίλ «{profile}» φορτώθηκε.",
    "warning_no_profile_delete": "Δεν υπάρχει προφίλ",
    "warning_no_profile_delete_message": "Επιλέξτε προφίλ από τη λίστα για διαγραφή.",
    "profile_not_found": "Το προφίλ «{profile}» δεν βρέθηκε.",
    "profile_not_exist": "Το προφίλ «{profile}» δεν υπάρχει.",
    "confirm_delete_title": "Επιβεβαίωση διαγραφής",
    "confirm_delete_profile": "Θέλετε σίγουρα να διαγράψετε το προφίλ «{profile}»;",
    "profile_deleted_title": "Το προφίλ διαγράφηκε",
    "profile_deleted": "Το προφίλ «{profile}» διαγράφηκε.",

    # --- Αρχεία / φάκελοι ---
    "msg_no_input_file": "Δεν υπάρχει αρχείο εισόδου",
    "msg_unsupported_format": "Μη υποστηριζόμενη μορφή",
    "select_file_title": "Επιλογή αρχείου εισόδου",
    "supported_files": "Υποστηριζόμενα αρχεία",
    "all_files": "Όλα τα αρχεία",
    "select_dir_title": "Επιλογή φακέλου εξόδου",
    "select_log_dir_title": "Επιλογή φακέλου για logs",
    "error_output_dir_title": "Σφάλμα φακέλου εξόδου",
    "error_output_dir": "Ο καθορισμένος φάκελος εξόδου είναι άκυρος ή δεν υπάρχει:\n{directory}",
    "error_input_file_title": "Σφάλμα αρχείου εισόδου",
    "error_input_file": "Το καθορισμένο αρχείο εισόδου είναι άκυρο ή δεν υπάρχει:\n{file}",
    "save_file_error_title": "Σφάλμα αποθήκευσης αρχείου",
    "save_file_error": "Δεν είναι δυνατή η αποθήκευση του αρχείου: {error}",

    # --- Επεξεργασία PDF / προεπισκόπηση ---
    "msg_pdf_processing_error": "Αποτυχία επεξεργασίας αρχείου PDF",
    "msg_thumbnail_error": "Σφάλμα φόρτωσης μικρογραφίας",
    "msg_no_pdf_output": "Δεν υπάρχει έξοδος PDF",
    "no_pdf_pages": "Το PDF δεν περιέχει σελίδες",
    "unsupported_output": "Μη υποστηριζόμενος τύπος εξόδου για προεπισκόπηση",
    "pdf_generated_title": "Η δημιουργία ολοκληρώθηκε",
    "pdf_generated": "Τα αρχεία PDF δημιουργήθηκαν με επιτυχία στον φάκελο:\n{directory}",
    "pdf_generation_error_title": "Σφάλμα δημιουργίας",
    "pdf_generation_error": "Παρουσιάστηκαν σφάλματα κατά τη δημιουργία του PDF. Ελέγξτε τα logs.",
    "critical_pdf_error_title": "Κρίσιμο σφάλμα δημιουργίας PDF",
    "critical_pdf_error": "Προέκυψε κρίσιμο σφάλμα κατά τη δημιουργία PDF:\n{error}\nΔείτε τα αρχεία καταγραφής.",
    "settings_saved_title": "Οι ρυθμίσεις αποθηκεύτηκαν",
    "settings_saved": "Οι ρυθμίσεις αποθηκεύτηκαν στο αρχείο:\n{filepath}",
    "settings_save_error_title": "Σφάλμα αποθήκευσης ρυθμίσεων",
    "settings_save_error": "Δεν ήταν δυνατή η αποθήκευση ρυθμίσεων: {error}",
    "conversion_error_title": "Σφάλμα μετατροπής",
    "conversion_error": "Σφάλμα μετατροπής τιμών από το περιβάλλον χρήστη: {error}",
    "update_gui_error_title": "Σφάλμα ενημέρωσης διεπαφής",
    "update_gui_error": "Προέκυψε σφάλμα κατά την ενημέρωση της διεπαφής: {error}",

    # --- Άδεια ---
    "hwid_copied_to_clipboard": "Το HWID αντιγράφηκε στο πρόχειρο",
    "computer_hwid": "HWID υπολογιστή",
    "public_key_load_error": "Σφάλμα φόρτωσης δημόσιου κλειδιού: {error}",
    "invalid_license_format": "Μη έγκυρη μορφή κλειδιού άδειας: {error}",
    "activation_success": "Η άδεια ενεργοποιήθηκε με επιτυχία.",
    "activation_error": "Σφάλμα ενεργοποίησης άδειας: {error}",
    "log_trial_mode_active": "Η δοκιμαστική λειτουργία είναι ενεργή",
    "log_trial_mode_inactive": "Η δοκιμαστική λειτουργία δεν είναι ενεργή",

    # --- Αρχικοποίηση ---
    "init_error_title": "Σφάλμα αρχικοποίησης",
    "init_error": "Σφάλμα αρχικοποίησης καταλόγων: {error}",
    "poppler_path_info": "Πληροφορίες διαδρομής Poppler",
    "ttkthemes_not_installed": "Σημείωση: η βιβλιοθήκη ttkthemes δεν είναι εγκατεστημένη. Θα χρησιμοποιηθεί το προεπιλεγμένο στυλ του Tkinter.",

    # =====================================
    #  Καταγραφές (μηνύματα logger)
    # =====================================

    # --- Γενικά / Διαμόρφωση ---
    "log_configured": "Η καταγραφή διαμορφώθηκε: επίπεδο={0}, λειτουργία={1}, αρχείο={2}",
    "log_no_handlers": "Προειδοποίηση: δεν έχουν διαμορφωθεί χειριστές καταγραφής (λειτουργία: {0}).",
    "log_critical_error": "Κρίσιμο σφάλμα διαμόρφωσης καταγραφής: {0}",
    "log_basic_config": "Λόγω σφάλματος χρησιμοποιήθηκε βασική διαμόρφωση καταγραφής.",
    "log_dir_create_error": "Κρίσιμο σφάλμα: αδυναμία δημιουργίας φακέλου logs {0}: {1}",

    # --- Καταγραφές – Αρχικοποίηση / Κατάλογοι (init_directories.py) ---
    "error_critical_init": "ΚΡΙΣΙΜΟ ΣΦΑΛΜΑ κατά την αρχικοποίηση: {0}",
    "logger_init_error": "Σφάλμα αρχικοποίησης καταλόγων: {error}",
    "directory_created": "Δημιουργήθηκε κατάλογος: {0}",
    "directory_creation_error": "Αδυναμία δημιουργίας καταλόγου {0}: {1}",
    "sample_file_copied": "Το δείγμα αρχείου αντιγράφηκε στο {0}",
    "sample_file_copy_error": "Σφάλμα αντιγραφής δείγματος αρχείου: {0}",
    "log_created_output_dir": "Δημιουργήθηκε φάκελος εξόδου: {0}",
    "log_cannot_create_output_dir": "Αδυναμία δημιουργίας φακέλου εξόδου {0}: {1}",

    # --- Καταγραφές – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Αποτυχία φόρτωσης γραφικών ρυθμίσεων κατά την αρχικοποίηση: {0}",
    "log_loading_pdf": "Φόρτωση αρχείου PDF: {0}",
    "log_loading_bitmap": "Φόρτωση αρχείου bitmap: {0}",
    "log_invalid_dpi": "Αναγνώστηκε μη έγκυρο DPI ({0}). Χρήση προεπιλεγμένου {1} DPI.",
    "log_image_dimensions": "Διαστάσεις εικόνας: {0}×{1}px, λειτουργία: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Επεξεργασία εικόνας στην αρχική λειτουργία χρώματος: {0}",
    "log_unusual_color_mode": "Ασυνήθιστη λειτουργία χρώματος: «{0}». Τα ReportLab/Pillow ίσως δεν λειτουργούν σωστά.",
    "log_draw_image_error": "Σφάλμα ReportLab drawImage για λειτουργία {0}: {1}",
    "log_unsupported_format": "Μη υποστηριζόμενη μορφή εισόδου: {0}",
    "log_input_file_not_found": "Το αρχείο εισόδου δεν βρέθηκε: {0}",
    "log_load_process_error": "Σφάλμα φόρτωσης ή επεξεργασίας αρχείου {0}: {1}",
    "log_input_file_not_exists": "Το αρχείο εισόδου δεν υπάρχει ή η διαδρομή είναι κενή: «{0}»",
    "log_cannot_load_or_empty_pdf": "Αδυναμία φόρτωσης αρχείου εισόδου ή το PDF είναι κενό/κατεστραμμένο.",
    "log_pdf_dimensions_info": "  Διαστάσεις PDF: {0:.1f} mm × {1:.1f} mm",
    "log_invalid_pdf_dimensions": "Μη έγκυρες διαστάσεις σελίδας PDF: {0}×{1} pt.",

    #   Splitter – Υπολογισμοί διαστάσεων
    "log_extra_margin": "Το πρόσθετο περιθώριο ορίστηκε σε {0:.3f} pt",
    "log_invalid_rows_cols": "Μη έγκυρος αριθμός σειρών ({0}) ή στηλών ({1}).",
    "error_invalid_rows_cols": "Οι σειρές και οι στήλες πρέπει να είναι θετικοί ακέραιοι.",
    "log_invalid_overlap_white_stripe": "Μη έγκυρες τιμές επικάλυψης ({0}) ή λευκής λωρίδας ({1}). Πρέπει να είναι αριθμητικές.",
    "error_invalid_overlap_white_stripe": "Η επικάλυψη και η λευκή λωρίδα πρέπει να είναι αριθμητικές τιμές (mm).",
    "log_stripe_usage": "Ορίστηκε use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Βασική επικάλυψη (γραφικά): {0:.3f} mm, λευκή λωρίδα: {1:.3f} mm, αποτελεσματική επικάλυψη: {2:.3f} mm",
    "log_computed_dimensions": "Υπολογίστηκε: PDF {0:.3f}×{1:.3f} mm. Πάνελ: {2:.3f} pt ({3:.3f} mm) × {4:.3f} pt ({5:.3f} mm). Πυρήνας: {6:.3f}×{7:.3f} pt. Αποτ. επικάλυψη: {8:.3f} mm",
    "log_invalid_dimensions": "Μη έγκυρες διαστάσεις πάνελ ({0:.3f}×{1:.3f}) ή πυρήνα ({2:.3f}×{3:.3f}) για per={4}, stripe={5}, r={6}, c={7}, W={8} mm, H={9} mm",
    "error_invalid_slice_dimensions": "Οι υπολογισμένες διαστάσεις πάνελ/πυρήνα είναι μη έγκυρες ή αρνητικές.",

    #   Splitter – Δημιουργία πληροφοριών και σειράς
    "log_generating_slice_info": "Δημιουργία πληροφοριών για πάνελ: {0}",
    "log_no_slices_info_generated": "Αδυναμία δημιουργίας πληροφοριών για τα πάνελ.",
    "log_applying_rotated_order": "Εφαρμογή σειράς για περιστροφή 180°: {0}",
    "log_applying_standard_order": "Εφαρμογή σειράς για 0° (τυπικό): {0}",
    "log_unknown_bryt_order": "Άγνωστη σειρά πάνελ: «{0}». Χρήση προεπιλογής.",
    "log_final_slices_order": "  Τελική σειρά πάνελ ({0}): [{1}]",

    #   Splitter – Επικαλύψεις (overlay) και συγχώνευση
    "log_invalid_dimensions_overlay": "Απόπειρα δημιουργίας overlay με μη έγκυρες διαστάσεις: {0}. Παράλειψη.",
    "log_empty_overlay": "Δημιουργήθηκε κενό ή σχεδόν κενό overlay PDF. Η συγχώνευση παραλείπεται.",
    "log_overlay_error": "Σφάλμα δημιουργίας overlay PDF: {0}",
    "log_merge_error": "Απόπειρα συγχώνευσης overlay χωρίς σελίδες. Παράλειψη.",
    "log_merge_page_error": "Σφάλμα συγχώνευσης overlay PDF: {0}",
    "log_fallback_draw_rotating_elements": "Αδυναμία λήψης σειρών/στηλών για _draw_rotating_elements, χρησιμοποιήθηκε 1×1.",
    "log_overlay_created_for_slice": "Δημιουργήθηκε overlay λωρίδων/σημάτων για το πάνελ {0}",
    "log_overlay_creation_failed_for_slice": "Αποτυχία δημιουργίας overlay για {0}",
    "log_merging_rotated_overlay": "Συγχώνευση ΠΕΡΙΣΤΡΑΜΜΕΝΟΥ overlay για {0} με T={1}",
    "log_merging_nonrotated_overlay": "Συγχώνευση ΜΗ ΠΕΡΙΣΤΡΑΜΜΕΝΟΥ overlay για {0}",
    "log_merging_all_codes_overlay": "Συγχώνευση overlay όλων των κωδικών (χωρίς περιστροφή)",
    "log_merging_separation_lines_overlay": "Συγχώνευση overlay γραμμών διαχωρισμού (χωρίς περιστροφή)",
    "log_merging_code_overlay_for_slice": "Το overlay κωδικού για {0} συγχωνεύτηκε χωρίς περιστροφή.",
    "log_merging_separation_overlay_for_slice": "Το overlay γραμμών διαχωρισμού για {0} συγχωνεύτηκε χωρίς περιστροφή.",

    #   Splitter – Σχεδίαση (λωρίδες, σήματα, γραμμές)
    "log_drawing_top_stripe": "[Canvas] Σχεδιάζω άνω λωρίδα για {0}: x={1:.3f}, y={2:.3f}, π={3:.3f}, ύ={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Σχεδιάζω δεξιά λωρίδα για {0}: x={1:.3f}, y={2:.3f}, π={3:.3f}, ύ={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Γεμίζω και περιγράφω γωνία για {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Σχεδιάζω σταυρό με κέντρο στο ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Σχεδιάζω γραμμές καταχώρισης για {0} στην περιοχή από ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Σχεδιάζω δεξιά κατακόρυφη γραμμή: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Σχεδιάζω άνω οριζόντια γραμμή: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Σχεδιάζω διαχωριστική γραμμή (λευκό πάνω σε μαύρο): ({0}) @ ({1:.3f}, {2:.3f}), μήκος={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Σχεδιάζω σταυρούς για {0} [{1},{2}] / [{3},{4}] στην περιοχή από ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Υπολογισμένα κέντρα: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Σχεδιάζω TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Σχεδιάζω TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Σχεδιάζω BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Σχεδιάζω BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Το σήμα {0} παραλείπεται σύμφωνα με τον κανόνα για τη θέση [{1},{2}]",
    "log_trial_common_sheet": "Εφαρμόζω υδατογράφημα TRIAL στο κοινό φύλλο",

    # Υδατογράφημα
    "log_trial_watermark_added": "Προστέθηκε υδατογράφημα TRIAL",
    "error_drawing_trial_text": "Σφάλμα σχεδίασης υδατογραφήματος: {error}",

    #   Splitter – Γραμμές διαχωρισμού (ολόκληρη σελίδα)
    "log_drawing_separation_lines_for_page": "Σχεδιάζω γραμμές διαχωρισμού για τη σελίδα (διάταξη={0}, πάνελ={1}, δείκτης={2})",
    "log_vertical_line_between_slices": "  Κατακόρυφη γραμμή μεταξύ πάνελ {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Έναρξη κατακόρυφης γραμμής @ x={0:.1f}",
    "log_vertical_line_end": "  Τέλος κατακόρυφης γραμμής @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Οριζόντια γραμμή μεταξύ πάνελ {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Έναρξη οριζόντιας γραμμής @ y={0:.1f}",
    "log_horizontal_line_end": "  Τέλος οριζόντιας γραμμής @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Ξεχωριστά_αρχεία) Έναρξη καθ./ορ. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Ξεχωριστά_αρχεία) Τέλος καθ./ορ. @ {0:.1f}",

    #   Splitter – Δημιουργία κωδικών / QR
    "log_generate_barcode_data": "Δημιουργώ δεδομένα για κωδικό: {0}",
    "log_barcode_data_shortened": "Τα δεδομένα κωδικού μειώθηκαν σε {0} χαρακτήρες.",
    "log_barcode_data_error": "Σφάλμα δημιουργίας δεδομένων κωδικού: {0}",
    "log_compose_barcode_payload": "Συνθέτω payload κωδικού ({0}): {1}",
    "log_barcode_payload_shortened": "Το payload μειώθηκε σε {0} χαρακτήρες για μορφή {1}",
    "log_barcode_payload_error": "Σφάλμα σύνθεσης payload: {0}",
    "log_unknown_anchor_fallback": "Άγνωστη γωνία αγκύρωσης «{0}», χρήση κάτω αριστερά",
    "log_used_default_code_settings": "Χρησιμοποιήθηκαν οι προεπιλεγμένες ρυθμίσεις για τον κωδικό {0}/{1}.",
    "log_no_layout_key_fallback": "Δεν υπάρχει διάταξη «{0}» για {1}/{2}. Χρησιμοποιήθηκε η πρώτη διαθέσιμη: «{3}».",
    "log_code_settings_error": "Λείπουν/μη διαθέσιμες ρυθμίσεις κωδικού ({0}/{1}/{2}): {3}. Χρήση προεπιλογών.",
    "log_drawing_barcode": "Σχεδιάζω {0} στο ({1:.3f}, {2:.3f}) [βάση ({3:.3f}, {4:.3f}) + μετατόπιση ({5:.3f}, {6:.3f})], περιστροφή: {7}°",
    "error_generate_qr_svg": "Αποτυχία δημιουργίας SVG για QR.",
    "error_invalid_scale_for_qr": "Μη έγκυρο μέγεθος QR: {0} mm",
    "error_invalid_qr_scale_factor": "Μη έγκυρος συντελεστής κλίμακας QR: {0}",
    "error_generate_barcode_svg": "Αποτυχία δημιουργίας SVG για γραμμωτό κώδικα.",
    "error_invalid_scale_for_barcode": "Μη έγκυρο μέγεθος γραμμωτού κώδικα: {0}×{1} mm",
    "error_invalid_barcode_scale_factor": "Μη έγκυρος συντελεστής κλίμακας γραμμωτού κώδικα: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: μέγεθος στη ρύθμιση={1:.3f} mm, πλάτος SVG={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: μέγεθος στη ρύθμιση=({1:.3f} mm, {2:.3f} mm), διαστ. SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Σφάλμα σχεδίασης κωδικού «{0}»: {1}",
    "log_prepared_barcode_info": "Προετοιμασμένες πληροφορίες κωδικού για {0} ({1}, γωνία={2}): βασική απόλυτη θέση ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Σφάλμα προετοιμασίας δεδομένων κωδικού για {0}: {1}",
    "log_drawing_barcodes_count": "Σχεδιάζω {0} κωδικούς/QR...",
    "log_missing_barcode_info_key": "Λείπει κλειδί στις πληροφορίες κωδικού κατά τη σχεδίαση: {0}. Πληρ.: {1}",
    "log_error_drawing_barcode_in_draw_all": "Σφάλμα σχεδίασης κωδικού «{0}» στο _draw_all_barcodes: {1}",

    #   Splitter – Διαδικασία κοπής (μέθοδοι split_*)
    "log_start_splitting_process": "--- Έναρξη διαδικασίας κοπής για: {0} ---",
    "log_split_settings": "  Ρυθμίσεις: {0}×{1} πάνελ, επικάλυψη={2} mm, λευκή λωρίδα={3} mm (+επικάλυψη: {4})",
    "log_output_dir_info": "  Έξοδος: {0} / {1} στο «{2}»",
    "log_lines_marks_barcodes_info": "  Γραμμές: διαχωριστικές={0}, αρχή={1}, τέλος={2} | Σήματα: {3} ({4}), Κωδικοί: {5} ({6})",
    "log_bryt_order_info": "  Σειρά: {0}, περιστροφή πάνελ: {1}°",
    "log_invalid_dimensions_in_slice_info": "Μη έγκυρες διαστάσεις στο slice_info για {0}: {1}×{2}",
    "log_content_transform": "Μετασχηματισμός περιεχομένου T_content για {0}: {1}",
    "log_merged_content_for_slice": "Το περιεχόμενο συγχωνεύτηκε για το πάνελ {0} σε new_page",
    "log_slice_reader_created": "Δημιουργήθηκε πλήρες πάνελ (PdfReader) για {0}",
    "log_slice_reader_creation_error": "Σφάλμα δημιουργίας πλήρους πάνελ για {0}: {1}",
    "log_used_get_transform": "Χρήση _get_transform (μόνο μετατόπιση): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Έναρξη: ΞΕΧΩΡΙΣΤΑ ΑΡΧΕΙΑ (περιστροφή στο create_slice_reader) ---",
    "log_creating_file_for_slice": "Δημιουργία αρχείου για το πάνελ {0}: {1}",
    "log_invalid_page_size_for_slice": "Μη έγκυρο μέγεθος σελίδας ({0}×{1}) για {2}. Παράλειψη.",
    "log_blank_page_creation_error": "Σφάλμα δημιουργίας κενής σελίδας για {0} (μέγεθος {1}×{2}): {3}. Παράλειψη.",
    "log_transform_for_slice": "Μετασχηματισμός T (μόνο μετατόπιση) για {0}: {1}",
    "log_merging_complete_slice": "Συγχώνευση πλήρους πάνελ {0} με μετασχηματισμό: {1}",
    "log_skipped_slice_merging": "Η συγχώνευση πλήρους πάνελ για {0} παραλείφθηκε.",
    "log_file_saved": "Το αρχείο αποθηκεύτηκε: {0}",
    "log_file_save_error": "Σφάλμα αποθήκευσης αρχείου {0}: {1}",
    "log_finished_split_separate_files": "--- Ολοκληρώθηκε: ΞΕΧΩΡΙΣΤΑ ΑΡΧΕΙΑ (αποθηκεύτηκαν {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Δεν υπάρχουν πάνελ προς επεξεργασία στο split_horizontal.",
    "log_start_split_horizontal": "--- Έναρξη: ΚΟΙΝΟ ΦΥΛΛΟ – ΟΡΙΖΟΝΤΙΑ (περιστροφή στο create_slice_reader) ---",
    "log_page_dimensions": "Διαστάσεις σελίδας: {0:.1f}×{1:.1f} mm ({2} πάνελ)",
    "log_page_creation_error": "Σφάλμα δημιουργίας σελίδας εξόδου ({0}×{1}): {2}. Τερματισμός.",
    "log_slice_at_position": "Πάνελ {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Μετασχηματισμός T (μόνο μετατόπιση) για {0}: {1}",
    "log_merging_complete_bryt": "Συγχώνευση πλήρους πάνελ {0} με μετασχηματισμό: {1}",
    "log_skipped_merging_bryt": "Η συγχώνευση πλήρους πάνελ για {0} παραλείφθηκε.",
    "log_file_result_saved": "Το τελικό αρχείο αποθηκεύτηκε: {0}",
    "log_file_result_save_error": "Σφάλμα αποθήκευσης τελικού αρχείου {0}: {1}",
    "log_finished_split_horizontal": "--- Ολοκληρώθηκε: ΚΟΙΝΟ ΦΥΛΛΟ – ΟΡΙΖΟΝΤΙΑ ---",
    "log_no_slices_split_vertical": "Δεν υπάρχουν πάνελ προς επεξεργασία στο split_vertical.",
    "log_start_split_vertical": "--- Έναρξη: ΚΟΙΝΟ ΦΥΛΛΟ – ΚΑΘΕΤΑ (περιστροφή στο create_slice_reader) ---",
    "log_finished_split_vertical": "--- Ολοκληρώθηκε: ΚΟΙΝΟ ΦΥΛΛΟ – ΚΑΘΕΤΑ ---",
    "log_unknown_layout": "Άγνωστη διάταξη για κοινό φύλλο: «{0}».",
    "log_unknown_output_type": "Άγνωστος τύπος εξόδου: «{0}».",
    "log_finished_splitting_success": "--- Η διαδικασία κοπής ολοκληρώθηκε για: {0} — ΕΠΙΤΥΧΙΑ ---",
    "log_finished_splitting_errors": "--- Η διαδικασία κοπής ολοκληρώθηκε για: {0} — ΥΠΗΡΞΑΝ ΣΦΑΛΜΑΤΑ ---",
    "log_value_error_in_splitting": "Σφάλμα εισόδου ή υπολογισμού: {0}",
    "log_finished_splitting_critical_error": "--- Η διαδικασία κοπής ολοκληρώθηκε για: {0} — ΚΡΙΣΙΜΟ ΣΦΑΛΜΑ ---",
    "log_unexpected_error_in_splitting": "Απρόσμενο σφάλμα κατά την κοπή του αρχείου {0}: {1}",

    #   Splitter – Λειτουργία δοκιμής (__main__)
    "log_script_mode_test": "Το splitter.py εκτελέστηκε ως κύριο σκριπτ (λειτουργία δοκιμής).",
    "log_loaded_config": "Η διαμόρφωση φορτώθηκε.",
    "log_error_loading_config": "Αποτυχία φόρτωσης διαμόρφωσης: {0}",
    "log_created_example_pdf": "Δημιουργήθηκε αρχείο PDF παραδείγματος: {0}",
    "log_cannot_create_example_pdf": "Αποτυχία δημιουργίας PDF παραδείγματος: {0}",
    "log_start_test_split": "Έναρξη δοκιμαστικής κοπής για το αρχείο: {0} σε {1}",
    "log_test_split_success": "Η δοκιμαστική κοπή ολοκληρώθηκε με επιτυχία.",
    "log_test_split_errors": "Η δοκιμαστική κοπή ολοκληρώθηκε με σφάλματα.",

    # --- Καταγραφές – QR/γραμμωτός κώδικας (barcode_qr.py) ---
    "log_qr_empty_data": "Απόπειρα δημιουργίας QR για κενά δεδομένα.",
    "log_qr_generated": "Δημιουργήθηκε SVG QR για: {0}...",
    "log_qr_error": "Σφάλμα δημιουργίας QR για τα δεδομένα «{0}»: {1}",
    "log_barcode_empty_data": "Απόπειρα δημιουργίας γραμμωτού κώδικα για κενά δεδομένα.",
    "log_barcode_generated": "Δημιουργήθηκε SVG γραμμωτού κώδικα για: {0}...",
    "log_barcode_error": "Σφάλμα δημιουργίας γραμμωτού κώδικα για «{0}»: {1}",
    "log_basic_handler_configured": "Ρυθμίστηκε βασικός handler για τον logger στο barcode_qr.py",
    "log_basic_handler_error": "Σφάλμα ρύθμισης βασικού handler στο barcode_qr: {0}",

    # --- Καταγραφές – Διαμόρφωση/Προφίλ (main_config_manager.py) ---
    "loading_profiles_from": "Φόρτωση προφίλ από",
    "profiles_file": "Αρχείο προφίλ",
    "does_not_contain_dict": "δεν περιέχει λεξικό. Δημιουργείται νέο",
    "not_found_creating_new": "δεν βρέθηκε. Δημιουργείται νέο κενό",
    "json_profiles_read_error": "Σφάλμα ανάγνωσης JSON αρχείου προφίλ",
    "file_will_be_overwritten": "Το αρχείο θα αντικατασταθεί κατά την αποθήκευση",
    "json_decode_error_in_profiles": "Σφάλμα αποκωδικοποίησης JSON στο αρχείο προφίλ",
    "cannot_load_profiles_file": "Αδυναμία φόρτωσης αρχείου προφίλ",
    "unexpected_profiles_read_error": "Απρόσμενο σφάλμα ανάγνωσης προφίλ",
    "saving_profiles_to": "Αποθήκευση προφίλ σε",
    "cannot_save_profiles_file": "Αδυναμία αποθήκευσης αρχείου προφίλ",
    "profiles_save_error": "Σφάλμα αποθήκευσης προφίλ στο αρχείο",
    "logger_profile_saved": "Αποθηκεύτηκε προφίλ: {profile}",
    "logger_profile_not_found": "Το προφίλ για φόρτωση δεν βρέθηκε: {profile}",
    "logger_profile_loaded": "Φορτώθηκε προφίλ: {profile}",
    "logger_profile_delete_not_exist": "Απόπειρα διαγραφής ανύπαρκτου προφίλ: {profile}",
    "logger_profile_deleted": "Διαγράφηκε προφίλ: {profile}",
    "logger_start_save_settings": "Έναρξη αποθήκευσης ρυθμίσεων από το GUI.",
    "logger_invalid_value": "Μη έγκυρη τιμή για «{key}». Ορίστηκε σε 0.0.",
    "logger_end_save_settings": "Η αποθήκευση ρυθμίσεων από το GUI ολοκληρώθηκε.",
    "logger_conversion_error": "Σφάλμα μετατροπής τιμών από το GUI: {error}",
    "conversion_failed": "Αποτυχία μετατροπής τιμών από το GUI",
    "logger_unexpected_save_error": "Απρόσμενο σφάλμα αποθήκευσης ρυθμίσεων: {error}",
    "logger_settings_saved": "Οι ρυθμίσεις αποθηκεύτηκαν στο αρχείο: {file}",

    # --- Καταγραφές – Αδειοδότηση (main_license.py) ---
    "public_key_load_error_log": "Σφάλμα φόρτωσης δημόσιου κλειδιού",
    "license_key_decode_error": "Σφάλμα αποκωδικοποίησης κλειδιού άδειας",
    "license_activation_error": "Σφάλμα ενεργοποίησης άδειας",

    # --- Καταγραφές – Κύρια μονάδα (main.py) ---
    "ui_created": "Το περιβάλλον χρήστη δημιουργήθηκε.",
    "error_tab_home": "Σφάλμα δημιουργίας διεπαφής «Αρχική»",
    "error_tab_settings": "Σφάλμα δημιουργίας διεπαφής «Ρυθμίσεις»",
    "error_tab_help": "Σφάλμα δημιουργίας διεπαφής «Βοήθεια»",
    "error_creating_license_ui": "Σφάλμα δημιουργίας διεπαφής «Άδεια»",
    "error_loading_ui": "Γενικό σφάλμα φόρτωσης διεπαφής: {error}",
    "error_creating_home_ui": "Σφάλμα δημιουργίας διεπαφής «Αρχική»",
    "error_creating_settings_ui": "Σφάλμα δημιουργίας διεπαφής «Ρυθμίσεις»",
    "error_creating_help_ui": "Σφάλμα δημιουργίας διεπαφής «Βοήθεια»",
    "logger_update_gui": "Έναρξη ενημέρωσης GUI από τη διαμόρφωση.",
    "logger_end_update_gui": "Η ενημέρωση GUI από τη διαμόρφωση ολοκληρώθηκε.",
    "logger_update_gui_error": "Απρόσμενο σφάλμα ενημέρωσης GUI: {error}",
    "logger_invalid_output_dir": "Μη έγκυρος ή ανύπαρκτος φάκελος εξόδου: {directory}",
    "logger_invalid_input_file": "Μη έγκυρο ή ανύπαρκτο αρχείο εισόδου: {file}",
    "logger_start_pdf": "Ξεκίνησε η διαδικασία δημιουργίας PDF.",
    "logger_pdf_save_error": "Διακοπή δημιουργίας PDF: αποτυχία αποθήκευσης τρεχουσών ρυθμίσεων.",
    "logger_pdf_success": "Η δημιουργία PDF ολοκληρώθηκε με επιτυχία.",
    "logger_pdf_exception": "Εξαίρεση στην κύρια διαδικασία δημιουργίας PDF.",
    "icon_set_error": "Σφάλμα ορισμού εικονιδίου εφαρμογής: {error}",
    "accent_button_style_error": "Σφάλμα ορισμού στυλ κουμπιού επισήμανσης: {error}",
    "logger_file_save_error": "Σφάλμα αποθήκευσης αρχείου {file}: {error}",

    #   Καταγραφές – Προεπισκόπηση (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Σφάλμα δημιουργίας μικρογραφίας",
    "output_preview_update_called": "Κλήθηκε ενημέρωση προεπισκόπησης εξόδου",
    "output_preview_canvas_missing": "Λείπει ο καμβάς προεπισκόπησης εξόδου",
    "pdf_found_in_output_dir": "Βρέθηκε PDF στον φάκελο εξόδου",
    "preparing_thumbnail": "Προετοιμασία μικρογραφίας",
    "thumbnail_generated_successfully": "Η μικρογραφία δημιουργήθηκε με επιτυχία",
    "thumbnail_generation_error": "Σφάλμα δημιουργίας μικρογραφίας για",
    "no_pdf_for_common_sheet": "Δεν υπάρχει PDF για προεπισκόπηση κοινού φύλλου",
    "no_pdf_for_separate_files": "Δεν υπάρχουν δημιουργημένα PDF για προεπισκόπηση",
    "cannot_load_thumbnail": "Αδυναμία φόρτωσης μικρογραφίας από",

    #   Καταγραφές – Εσωτερικά για ανάπτυξη (main.py)
    "missing_gui_var_created": "Δημιουργήθηκε ελλείπουσα μεταβλητή GUI για κλειδί: {key}",
    "missing_gui_structure_created": "Δημιουργήθηκε ελλείπουσα δομή GUI για: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Δημιουργήθηκε ελλείπουσα μεταβλητή GUI για: {code_type}/{output_type}/{layout}/{param}",

    # Πρόσθετο κείμενο για main_ui_help.py
    "help_text": """
    Billboard Splitter – Οδηγός χρήσης\n\n
    Σκοπός προγράμματος:\n
    Το Billboard Splitter χωρίζει αυτόματα έργα billboard σε πάνελ έτοιμα για εκτύπωση.
    Το πρόγραμμα έχει σχεδιαστεί για αρχεία κλίμακας 1:10.\n
    Οι τιμές στις ενότητες: Επικάλυψη, Λευκή λωρίδα και Ρυθμίσεις εισάγονται σε κλίμακα 1:1.
    Το πρόγραμμα επιτρέπει τη διάταξη των κομμένων πάνελ σε PDF σύμφωνα με την επιλογή σας:\n
    • Κοινό φύλλο: όλα τα πάνελ σε ένα έγγραφο.\n
    • Ξεχωριστά αρχεία: κάθε πάνελ σε ξεχωριστό PDF.\n\n
    Επιπλέον δυνατότητες:\n
    • Επιλογή διάταξης – κάθετα ή οριζόντια (στο κάθετο οι διαχωριστικές γραμμές είναι πάνω/κάτω,
      στο οριζόντιο αριστερά/δεξιά).\n
    • Περιστροφή πάνελ κατά 180° (αντιστροφή έργου).\n
    • Προσθήκη σημάτων καταχώρισης (σταυρός ή γραμμή) για ακριβή τοποθέτηση κατά την επικόλληση.\n
    • Προσθήκη QR ή γραμμωτών κωδικών – παράγονται από τα δεδομένα εισόδου για αναγνώριση πάνελ.\n
    • Αποθήκευση ρυθμίσεων ως προφίλ: μπορούν να φορτωθούν, τροποποιηθούν και διαγραφούν για γρήγορη εναλλαγή.\n\n
    Βασικά βήματα:\n\n
    1. Επιλογή αρχείου εισόδου:\n
    • Στην καρτέλα «Αρχική» επιλέξτε PDF, JPG ή TIFF με το σχέδιο του billboard.\n
    • Αν δεν ορίσετε δική σας διαδρομή, χρησιμοποιείται προεπιλεγμένο δείγμα.\n\n
    2. Ρυθμίσεις κοπής:\n
    • Εισαγάγετε αριθμό σειρών και στηλών.\n
    • Ορίστε μέγεθος επικάλυψης.\n
    • Προαιρετικά ορίστε πλάτος λευκής λωρίδας που προστίθεται στην αποτελεσματική επικάλυψη.\n\n
    3. Διάταξη εξόδου:\n
    • Κάθετα: τα πάνελ τοποθετούνται κάθετα στη σελίδα PDF.\n
    • Οριζόντια: τα πάνελ τοποθετούνται οριζόντια.\n\n
    4. Τύπος εξόδου:\n
    • Κοινό φύλλο – ένα PDF.\n
    • Ξεχωριστά αρχεία – ένα PDF ανά πάνελ.\n
    • Στην «Αρχική» μπορείτε να ενεργοποιήσετε και να ρυθμίσετε τα σήματα – σταυρό ή γραμμή.\n
    • Προαιρετικά ενεργοποιήστε QR ή γραμμωτό – θα δημιουργηθεί από τα δεδομένα έργου.\n
    • Οι παράμετροι κώδικα (κλίμακα, μετατόπιση, περιστροφή, θέση) ρυθμίζονται στην «Ρυθμίσεις».\n\n
    5. Διαχείριση ρυθμίσεων:\n
    • Στην «Ρυθμίσεις» ρυθμίζετε λεπτομερώς γραφικές παραμέτρους (περιθώρια, πάχη γραμμών, αποστάσεις) και κωδικούς.\n
    • Αποθηκεύστε την τρέχουσα διαμόρφωση ως προφίλ για μελλοντική χρήση.\n
    • Τα προφίλ (profiles.json) επιτρέπουν ταχεία εναλλαγή μεταξύ πακέτων ρυθμίσεων.\n\n
    6. Δημιουργία PDF:\n
    • Όταν είστε έτοιμοι, κάντε κλικ στο «Δημιουργία PDF».\n
    • Τα αποτελέσματα αποθηκεύονται στο «output» (ή άλλον φάκελο), και τα logs (με ημερήσια εναλλαγή) στο «logs».\n\n
    Αν παρουσιαστούν προβλήματα:\n
    • Ελέγξτε τα logs στον φάκελο «logs». Κάθε μέρα δημιουργείται νέο αρχείο με την ημερομηνία.\n
    • Βεβαιωθείτε ότι έχουν οριστεί όλοι οι απαιτούμενοι κατάλογοι.\n
    • Υποστήριξη: tech@printworks.pl (εργάσιμες ημέρες, 8–16)\n
    """
}
