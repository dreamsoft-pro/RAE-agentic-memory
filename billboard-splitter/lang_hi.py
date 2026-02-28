# lang_hi.py
# -*- coding: utf-8 -*-
"""
Hindi (India) translations — LTR.
"""

LANG = {
    "barcode_font_size_label": "बारकोड विवरण फ़ॉन्ट आकार [pt]:",
    # ---------------------------
    # Metadata (safe to ignore)
    # ---------------------------
    "__meta__": {
        "language_name_native": "हिन्दी (भारत)",
        "language_name_en": "Hindi (India)",
        "locale": "hi-IN",
        "direction": "ltr",              # left-to-right
        "font_hint": "Noto Sans Devanagari, Noto Serif Devanagari"
    },

    # ==========================
    #  Application - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "त्रुटि",
    "no_file": "कोई फ़ाइल नहीं",
    "language": "भाषा",
    "language_switch": "भाषा बदलें",
    "choose_language": "भाषा चुनें:",
    "apply_language": "लागू करें",
    "language_changed": "भाषा बदल दी गई है। कुछ परिवर्तन ऐप पुनः आरंभ करने के बाद दिखेंगे।",

    # ========================================
    #  User Interface (GUI) Elements
    # ========================================

    # --- Main Tabs ---
    "tab_home": " होम ",
    "tab_settings": " सेटिंग्स ",
    "tab_help": " मदद ",
    "tab_license": " लाइसेंस ",

    # --- General Buttons ---
    "button_browse": "ब्राउज़…",
    "browse_folder": "फ़ोल्डर ब्राउज़…",
    "button_save": "सहेजें",
    "button_delete": "हटाएँ",
    "button_close": "बंद करें",
    "save_all_settings": "सभी सेटिंग्स सहेजें",

    # --- Field Labels (Home Tab) ---
    "label_rows": "ऊर्ध्वाधर विभाजन (पंक्तियाँ):",
    "label_columns": "क्षैतिज विभाजन (स्तम्भ):",
    "label_overlap": "ओवरलैप (सेमी):",
    "label_white_stripe": "सफ़ेद स्ट्राइप (सेमी):",
    "label_add_white_stripe": "प्रभावी ओवरलैप में सफ़ेद स्ट्राइप जोड़ें",
    "label_layout": "लेआउट:",
    "label_output_type": "आउटपुट प्रकार:",
    "label_enable_reg_marks": "रजिस्ट्रेशन मार्क सक्षम करें:",
    "label_enable_codes": "कोड सक्षम करें:",
    "label_enable_sep_lines": "विभाजन रेखाएँ सक्षम करें (पैनलों के बीच)",
    "label_enable_start_line": "शीट की शीर्ष/आरंभ रेखा सक्षम करें",
    "label_enable_end_line": "शीट की निचली/अंत रेखा सक्षम करें",
    "label_bryt_order": "पैनलों का क्रम:",
    "label_slice_rotation": "पैनल रोटेशन:",
    "label_create_order_folder": "आर्डर नम्बर के नाम से फ़ोल्डर बनाएँ",

    # --- Sections/Frames (Home Tab) ---
    "section_input_file": " इनपुट फ़ाइल ",
    "section_scale_and_dimensions": " स्केल और आउटपुट आयाम ",
    "label_original_size": "मूल आकार:",
    "label_scale_non_uniform": "गैर-आनुपातिक रूप से स्केल करें",
    "label_scale": "स्केल: 1:",
    "label_scale_x": "स्केल X: 1:",
    "label_scale_y": "स्केल Y: 1:",
    "label_output_dimensions": "आउटपुट फ़ाइल के आयाम:",
    "label_width_cm": "चौड़ाई [सेमी]:",
    "label_height_cm": "ऊंचाई [सेमी]:",
    "section_split_settings": " विभाजन सेटिंग्स ",
    "section_profiles": " प्रोफ़ाइल ",
    "section_save_location": " सहेजने का स्थान ",
    "section_input_preview": " इनपुट प्रीव्यू ",
    "section_output_preview": " आउटपुट प्रीव्यू ",

    # --- Option Values (Combobox, Radiobutton etc.) ---
    "layout_vertical": "ऊर्ध्वाधर",
    "layout_horizontal": "क्षैतिज",
    "output_common_sheet": "कॉमन शीट",
    "output_separate_files": "अलग-अलग फ़ाइलें",
    "output_both": "कॉमन शीट और अलग फ़ाइलें",
    "output_common": "कॉमन शीट",
    "output_separate": "अलग फ़ाइलें",
    "reg_mark_cross": "क्रॉस",
    "reg_mark_line": "रेखा",
    "code_qr": "क्यूआर कोड",
    "code_barcode": "बारकोड",
    "bryt_order_1": "A1–An, B1–Bn … मानक, ऊपर से",
    "bryt_order_2": "A1–An, Bn–B1 … सर्पाकार (पंक्तियों अनुसार), ऊपर से",
    "bryt_order_3": "A1..B1, A2..B2 … स्तम्भ अनुसार, ऊपर से",
    "bryt_order_4": "A1–A2..B2–B1 … सर्पाकार (स्तम्भ), ऊपर से",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … मानक, नीचे से",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … सर्पाकार (पंक्तियाँ), नीचे से",
    "logging_console": "कंसोल",
    "logging_file": "फ़ाइल",
    "logging_both": "दोनों",

    # --- Sections/Frames (Settings Tab) ---
    "section_processing_mode": " कटिंग ऑपरेशंस ",
    "processing_mode_ram": "रैम (मेमोरी)",
    "processing_mode_hdd": "एचडीडी (डिस्क)",
    "graphic_settings": "ग्राफ़िक सेटिंग्स",
    "code_settings": "क्यूआर/बारकोड सेटिंग्स",
    "logging_settings": "लॉगिंग सेटिंग्स",
    "barcode_text_position_label": "बारकोड टेक्स्ट की स्थिति:",
    "barcode_text_bottom": "नीचे",
    "barcode_text_side": "बगल में",
    "barcode_text_none": "कोई नहीं",

    # --- Field Labels (Settings Tab - Graphics) ---
    "extra_margin_label": "पैनलों के चारों ओर मार्जिन (सेमी):",
    "margin_top_label": "ऊपरी मार्जिन (सेमी):",
    "margin_bottom_label": "निचला मार्जिन (सेमी):",
    "margin_left_label": "बायाँ मार्जिन (सेमी):",
    "margin_right_label": "दायाँ मार्जिन ( सेमी ):",
    "reg_mark_width_label": "रजिस्ट्रेशन मार्क — चौड़ाई (सेमी):",
    "reg_mark_height_label": "रजिस्ट्रेशन मार्क — ऊँचाई (सेमी):",
    "reg_mark_white_line_width_label": "रजिस्ट्रेशन मार्क — सफ़ेद रेखा मोटाई (सेमी):",
    "reg_mark_black_line_width_label": "रजिस्ट्रेशन मार्क — काली रेखा मोटाई (सेमी):",
    "sep_line_black_width_label": "विभाजन रेखा — काली रेखा मोटाई (सेमी):",
    "sep_line_white_width_label": "विभाजन रेखा — सफ़ेद रेखा मोटाई (सेमी):",
    "slice_gap_label": "पैनलों के बीच गैप (सेमी):",
    "label_draw_slice_border": "पैनल बॉर्डर (कट लाइन) खींचें",

    # --- Field Labels (Settings Tab - Codes) ---
    "scale_label": "स्केल (सेमी):",
    "scale_x_label": "चौड़ाई X (सेमी):",
    "scale_y_label": "ऊँचाई Y (सेमी):",
    "offset_x_label": "ऑफ़सेट X (सेमी):",
    "offset_y_label": "ऑफ़सेट Y (सेमी):",
    "rotation_label": "रोटेशन (°):",
    "anchor_label": "ऐंकर:",

    # --- Field Labels (Settings Tab - Logging) ---
    "logging_mode_label": "लॉगिंग मोड:",
    "log_file_label": "लॉग फ़ाइल:",
    "logging_level_label": "लॉगिंग स्तर:",

    # --- Buttons / Actions (Home Tab) ---
    "button_load": "लोड करें",
    "button_save_settings": "वर्तमान सेटिंग्स सहेजें",
    "button_generate_pdf": "PDF बनाएँ",
    "button_refresh_preview": "प्रीव्यू ताज़ा करें",
    "button_refresh_layout": "लेआउट ताज़ा करें",

    # --- License (GUI) ---
    "hwid_frame_title": "हार्डवेयर आईडी (HWID)",
    "copy_hwid": "HWID कॉपी करें",
    "license_frame_title": "लाइसेंस सक्रियण",
    "enter_license_key": "लाइसेंस कुंजी दर्ज करें:",
    "activate": "सक्रिय करें",
    "status_trial": "ट्रायल मोड",
    "license_active": "लाइसेंस सक्रिय है",

    # ================================================
    #  User Messages (Windows, Status Bar)
    # ================================================

    # --- Profiles ---
    "msg_no_profile_name": "कोई नाम नहीं",
    "msg_enter_profile_name": "सहेजने के लिए प्रोफ़ाइल नाम दर्ज करें।",
    "msg_profile_saved": "प्रोफ़ाइल सहेजी गई",
    "profile_saved_title": "प्रोफ़ाइल सहेजी गई",
    "msg_profile_saved_detail": "प्रोफ़ाइल '{0}' सहेजी गई है।",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "प्रोफ़ाइल '{profile}' सहेजा और लागू किया गया है।",
    "msg_no_profile": "कोई प्रोफ़ाइल नहीं",
    "warning_no_profile": "कोई प्रोफ़ाइल नहीं",
    "msg_select_profile": "लोड करने के लिए सूची से प्रोफ़ाइल चुनें।",
    "select_profile": "लोड करने के लिए सूची से प्रोफ़ाइल चुनें।",
    "profile_loaded_title": "प्रोफ़ाइल लोड हो गई",
    "profile_loaded": "प्रोफ़ाइल '{profile}' लोड हो गई है।",
    "warning_no_profile_delete": "कोई प्रोफ़ाइल नहीं",
    "warning_no_profile_delete_message": "हटाने के लिए सूची से प्रोफ़ाइल चुनें।",
    "profile_not_found": "प्रोफ़ाइल '{profile}' नहीं मिली।",
    "profile_not_exist": "प्रोफ़ाइल '{profile}' मौजूद नहीं है।",
    "confirm_delete_title": "हटाने की पुष्टि",
    "confirm_delete_profile": "क्या आप वाकई प्रोफ़ाइल '{profile}' हटाना चाहते हैं?",
    "profile_deleted_title": "प्रोफ़ाइल हटाई गई",
    "profile_deleted": "प्रोफ़ाइल '{profile}' हटा दी गई है।",

    # --- Files / Directories ---
    "msg_no_input_file": "इनपुट फ़ाइल मौजूद नहीं",
    "msg_unsupported_format": "असमर्थित फ़ॉर्मेट",
    "select_file_title": "इनपुट फ़ाइल चुनें",
    "supported_files": "समर्थित फ़ाइलें",
    "all_files": "सभी फ़ाइलें",
    "select_dir_title": "आउटपुट फ़ोल्डर चुनें",
    "select_log_dir_title": "लॉग फ़ोल्डर चुनें",
    "error_output_dir_title": "आउटपुट फ़ोल्डर त्रुटि",
    "error_output_dir": "चयनित आउटपुट फ़ोल्डर गलत है या मौजूद नहीं:\n{directory}",
    "error_input_file_title": "इनपुट फ़ाइल त्रुटि",
    "error_input_file": "चयनित इनपुट फ़ाइल गलत है या मौजूद नहीं:\n{file}",
    "save_file_error_title": "फ़ाइल सहेजने में त्रुटि",
    "save_file_error": "फ़ाइल सहेजी नहीं जा सकी: {error}",

    # --- PDF Processing / Preview ---
    "msg_pdf_processing_error": "PDF फ़ाइल प्रोसेस करने में विफल",
    "msg_thumbnail_error": "थंबनेल लोड करने में त्रुटि",
    "msg_no_pdf_output": "कोई PDF आउटपुट मौजूद नहीं",
    "no_pdf_pages": "PDF फ़ाइल में पृष्ठ नहीं हैं",
    "unsupported_output": "इस आउटपुट प्रकार का प्रीव्यू समर्थित नहीं",
    "pdf_generated_title": "जनरेशन पूर्ण",
    "pdf_generated": "PDF फ़ाइल(ें) सफलतापूर्वक इस फ़ोल्डर में बनीं:\n{directory}",
    "pdf_generation_error_title": "जनरेशन त्रुटि",
    "pdf_generation_error": "PDF बनाते समय त्रुटियाँ हुईं। विवरण के लिए लॉग देखें।",
    "critical_pdf_error_title": "गंभीर PDF जनरेशन त्रुटि",
    "critical_pdf_error": "PDF बनाते समय गंभीर त्रुटि हुई:\n{error}\nकृपया लॉग जाँचें।",

    # --- Settings ---
    "settings_saved_title": "सेटिंग्स सहेजी गईं",
    "settings_saved": "सेटिंग्स इस फ़ाइल में सहेजी गई हैं:\n{filepath}",
    "settings_save_error_title": "सेटिंग्स सहेजने में त्रुटि",
    "settings_save_error": "सेटिंग्स सहेजी नहीं जा सकीं: {error}",
    "conversion_error_title": "कन्वर्ज़न त्रुटि",
    "conversion_error": "GUI से मानों को बदलते समय त्रुटि: {error}",
    "update_gui_error_title": "इंटरफ़ेस अपडेट त्रुटि",
    "update_gui_error": "इंटरफ़ेस अपडेट करते समय त्रुटि हुई: {error}",

    # --- License ---
    "hwid_copied_to_clipboard": "HWID क्लिपबोर्ड पर कॉपी किया गया",
    "computer_hwid": "कंप्यूटर HWID",
    "public_key_load_error": "पब्लिक की लोड करने में त्रुटि: {error}",
    "invalid_license_format": "लाइसेंस कुंजी का फ़ॉर्मेट अमान्य: {error}",
    "activation_success": "लाइसेंस सफलतापूर्वक सक्रिय हुआ।",
    "activation_error": "लाइसेंस सक्रियण में त्रुटि: {error}",
    "log_trial_mode_active": "ट्रायल मोड सक्रिय है",
    "log_trial_mode_inactive": "ट्रायल मोड निष्क्रिय है",

    # --- Initialization ---
    "init_error_title": "आरंभीकरण (Initialization) त्रुटि",
    "init_error": "डायरेक्टरी बनाने में त्रुटि: {error}",
    "poppler_path_info": "Poppler पाथ जानकारी",
    "ttkthemes_not_installed": "चेतावनी: 'ttkthemes' इंस्टॉल नहीं है। डिफ़ॉल्ट Tkinter शैली उपयोग होगी।",

    # =====================================
    #  Logs (Logger Messages)
    # =====================================
    # Developer-facing logs retained in English intentionally
    "log_configured": "Logging configured: level={0}, mode={1}, file={2}",
    "log_no_handlers": "Warning: No logging handlers configured (mode: {0}).",
    "log_critical_error": "Critical logging configuration error: {0}",
    "log_basic_config": "Basic logging configuration used due to an error.",
    "log_dir_create_error": "Critical error: Cannot create logs directory {0}: {1}",

    # --- Logs - Initialization / Directories (`init_directories.py`) ---
    "error_critical_init": "CRITICAL ERROR during initialization: {0}",
    "logger_init_error": "Directory initialization error: {error}",
    "directory_created": "Created directory: {0}",
    "directory_creation_error": "Failed to create directory {0}: {1}",
    "sample_file_copied": "Sample file copied to {0}",
    "sample_file_copy_error": "Error copying sample file: {0}",
    "log_created_output_dir": "Output directory created: {0}",
    "log_cannot_create_output_dir": "Cannot create output directory {0}: {1}",

    # --- Logs - Splitter (`splitter.py`) ---
    "log_graphic_settings_error": "Failed to load graphic settings during initialization: {0}",
    "log_loading_pdf": "Loading PDF file: {0}",
    "log_loading_bitmap": "Loading bitmap file: {0}",
    "log_invalid_dpi": "Invalid DPI read ({0}). Using default {1} DPI.",
    "log_image_dimensions": "Image dimensions: {0}x{1}px, Mode: {2}, DPI: {3:.1f} -> {4:.3f}x{5:.3f}pt",
    "log_image_processing_color": "Processing image with original color mode: {0}",
    "log_unusual_color_mode": "Unusual image color mode: '{0}'. ReportLab/Pillow may not handle it correctly.",
    "log_draw_image_error": "Error during ReportLab drawImage for mode {0}: {1}",
    "log_unsupported_format": "Unsupported input file format: {0}",
    "log_input_file_not_found": "Input file not found: {0}",
    "log_load_process_error": "Error while loading or processing file {0}: {1}",
    "log_input_file_not_exists": "Input file does not exist or path is empty: '{0}'",
    "log_cannot_load_or_empty_pdf": "Failed to load input file or PDF is empty/corrupted.",
    "log_pdf_dimensions_info": "  PDF dimensions: {0:.1f}mm x {1:.1f}mm",
    "log_invalid_pdf_dimensions": "Invalid PDF page dimensions: {0}x{1} pt.",

    #   Splitter - Dimension Calculations
    "log_extra_margin": "Extra margin set to {0:.3f} pt",
    "log_invalid_rows_cols": "Invalid number of rows ({0}) or columns ({1}).",
    "error_invalid_rows_cols": "Rows and columns must be positive integers.",
    "log_invalid_overlap_white_stripe": "Invalid overlap ({0}) or white stripe ({1}) values. They must be numbers.",
    "error_invalid_overlap_white_stripe": "Overlap and white stripe must be numeric values (mm).",
    "log_stripe_usage": "Set use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Base overlap (graphics): {0:.3f} mm, White stripe: {1:.3f} mm, Effective overlap: {2:.3f} mm",
    "log_computed_dimensions": "Computed dimensions: PDF: {0:.3f}mm x {1:.3f}mm. Panel: {2:.3f}pt ({3:.3f}mm) x {4:.3f}pt ({5:.3f}mm). Core: {6:.3f}pt x {7:.3f}pt. Effective overlap: {8:.3f}mm",
    "log_invalid_dimensions": "Computed panel ({0:.3f}x{1:.3f}) or core ({2:.3f}x{3:.3f}) dimensions are invalid for overlap={4}, stripe={5}, r={6}, c={7}, W={8}mm, H={9}mm",
    "error_invalid_slice_dimensions": "Computed panel/core dimensions are invalid or negative.",

    #   Splitter - Generating Panels Info and Order
    "log_generating_slice_info": "Generating panel info: {0}",
    "log_no_slices_info_generated": "Failed to generate panels info.",
    "log_applying_rotated_order": "Applying order for 180-degree rotation: {0}",
    "log_applying_standard_order": "Applying order for 0-degree rotation (standard): {0}",
    "log_unknown_bryt_order": "Unknown panels order: '{0}'. Using default.",
    "log_final_slices_order": "  Final panels order ({0}): [{1}]",

    #   Splitter - Creating Overlays and Merging
    "log_invalid_dimensions_overlay": "Attempt to create an overlay with invalid dimensions: {0}. Skipping.",
    "log_empty_overlay": "Created an empty or nearly empty overlay PDF. Skipping.",
    "log_overlay_error": "Overlay PDF creation error: {0}",
    "log_merge_error": "Attempt to merge overlay without pages. Skipping.",
    "log_merge_page_error": "Error while merging overlay PDF: {0}",
    "log_fallback_draw_rotating_elements": "Could not get rows/cols for _draw_rotating_elements, used 1x1.",
    "log_overlay_created_for_slice": "Created stripes/marks overlay for panel {0}",
    "log_overlay_creation_failed_for_slice": "Failed to create stripes/marks overlay for {0}",
    "log_merging_rotated_overlay": "Merging ROTATED stripes/marks overlay for {0} with T={1}",
    "log_merging_nonrotated_overlay": "Merging NON-rotated stripes/marks overlay for {0}",
    "log_merging_all_codes_overlay": "Merging overlay of all codes (without rotation)",
    "log_merging_separation_lines_overlay": "Merging overlay of separation lines (without rotation)",
    "log_merging_code_overlay_for_slice": "Code overlay for {0} merged without rotation.",
    "log_merging_separation_overlay_for_slice": "Separation lines overlay for {0} merged without rotation.",

    #   Splitter - Drawing Graphic Elements (Stripes, Marks, Lines)
    "log_drawing_top_stripe": "[Canvas Draw] Drawing top stripe for {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas Draw] Drawing right stripe for {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas Draw] Filling and stroking corner for {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Drawing centered cross at ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Drawing registration lines for {0} in area from ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Drawing right vertical line: x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  Drawing top horizontal line: y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "Drawing separation line (white on black): ({0}) @ ({1:.3f}, {2:.3f}), len={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Drawing crosses for {0} [{1},{2}] / [{3},{4}] in area from ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Calculated centers: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Drawing TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Drawing TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Drawing BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Drawing BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Omitted {0} according to rule for position [{1},{2}]",
    "log_trial_common_sheet": "Applying TRIAL watermark text on common sheet",
    "log_trial_watermark_added": "TRIAL watermark has been added",
    "error_drawing_trial_text": "Error while drawing watermark: {error}",

    #   Splitter - Drawing Separation Lines (Whole Page)
    "log_drawing_separation_lines_for_page": "Drawing separation lines for page (layout={0}, total_slices={1}, slice_index={2})",
    "log_vertical_line_between_slices": "  Vertical line between panels {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Vertical line start @ x={0:.1f}",
    "log_vertical_line_end": "  Vertical line end @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Horizontal line between panels {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Horizontal line start @ y={0:.1f}",
    "log_horizontal_line_end": "  Horizontal line end @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Separate_files) Vertical/Horizontal line start @ {0:.1f}",
    "log_sep_line_end_separate": "  (Separate_files) Vertical/Horizontal line end @ {0:.1f}",

    #   Splitter - Generating Barcodes / QR
    "log_generate_barcode_data": "Generating barcode data: {0}",
    "log_barcode_data_shortened": "Barcode data shortened to {0} characters.",
    "log_barcode_data_error": "Barcode data generation error: {0}",
    "log_compose_barcode_payload": "Composing barcode payload ({0}): {1}",
    "log_barcode_payload_shortened": "Payload shortened to {0} characters for format {1}",
    "log_barcode_payload_error": "Error while composing payload: {0}",
    "log_unknown_anchor_fallback": "Unknown anchor '{0}', using bottom-left",
    "log_used_default_code_settings": "Used 'default' settings for code {0}/{1}.",
    "log_no_layout_key_fallback": "No layout '{0}' for {1}/{2}. Used the first available: '{3}'.",
    "log_code_settings_error": "Not found or error while retrieving code settings ({0}/{1}/{2}): {3}. Using defaults.",
    "log_drawing_barcode": "Drawing {0} at ({1:.3f}, {2:.3f}) [base ({3:.3f}, {4:.3f}) + offset ({5:.3f}, {6:.3f})], rotation: {7}°",
    "error_generate_qr_svg": "Failed to generate QR code SVG.",
    "error_invalid_scale_for_qr": "Invalid scale for QR: {0}mm",
    "error_invalid_qr_scale_factor": "Invalid scale factor for QR: {0}",
    "error_generate_barcode_svg": "Failed to generate barcode SVG.",
    "error_invalid_scale_for_barcode": "Invalid scale for Barcode: {0}x{1}mm",
    "error_invalid_barcode_scale_factor": "Invalid scale factor for Barcode: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: scale config={1:.3f}mm, SVG width={2:.3f}pt, sf={3:.4f}",
    "log_barcode_scale_code128": "  {0}: scale config=({1:.3f}mm, {2:.3f}mm), SVG size=({3:.3f}pt, {4:.3f}pt), sf=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Error while drawing code '{0}': {1}",
    "log_prepared_barcode_info": "Prepared code info for {0} ({1}, anchor={2}): base absolute position ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Error preparing code data for {0}: {1}",
    "log_drawing_barcodes_count": "Drawing {0} barcodes/QR codes...",
    "log_missing_barcode_info_key": "Missing key in barcode info while drawing: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Error while drawing code '{0}' in _draw_all_barcodes: {1}",

    #   Splitter - Splitting Process (split_* methods)
    "log_start_splitting_process": "--- Starting split process for: {0} ---",
    "log_split_settings": "  Settings: {0}x{1} panels, Overlap={2}mm, White stripe={3}mm (+overlap: {4})",
    "log_output_dir_info": "  Output: {0} / {1} to '{2}'",
    "log_lines_marks_barcodes_info": "  Lines: Separation={0}, Start={1}, End={2} | Marks: {3} ({4}), Codes: {5} ({6})",
    "log_bryt_order_info": "  Order: {0}, Panels rotation: {1}°",
    "log_invalid_dimensions_in_slice_info": "Invalid dimensions in slice_info for {0}: {1}x{2}",
    "log_content_transform": "Content transformation T_content for {0}: {1}",
    "log_merged_content_for_slice": "Merged content for panel {0} on new_page",
    "log_slice_reader_created": "Created complete slice (PdfReader) for panel {0}",
    "log_slice_reader_creation_error": "Error creating complete slice for panel {0}: {1}",
    "log_used_get_transform": "Used _get_transform (translation only): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Starting: SEPARATE FILES (Rotation handled in create_slice_reader) ---",
    "log_creating_file_for_slice": "Creating file for panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Invalid page size ({0}x{1}) for {2}. Skipping.",
    "log_blank_page_creation_error": "Error creating page for {0} (size {1}x{2}): {3}. Skipping.",
    "log_transform_for_slice": "Transform T (translation only) for {0}: {1}",
    "log_merging_complete_slice": "Merging complete panel {0} with transform: {1}",
    "log_skipped_slice_merging": "Skipped merging complete panel for {0}.",
    "log_file_saved": "File saved: {0}",
    "log_file_save_error": "File save error {0}: {1}",
    "log_finished_split_separate_files": "--- Finished: SEPARATE FILES (Saved {0}/{1}) ---",
    "log_no_slices_split_horizontal": "No panels to process in split_horizontal.",
    "log_start_split_horizontal": "--- Starting: COMMON SHEET - HORIZONTAL (Rotation handled in create_slice_reader) ---",
    "log_page_dimensions": "Page dimensions: {0:.1f}mm x {1:.1f}mm ({2} panels)",
    "log_page_creation_error": "Error creating result page ({0}x{1}): {2}. Aborting.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transform T (translation only) for {0}: {1}",
    "log_merging_complete_bryt": "Merging complete panel {0} with transform: {1}",
    "log_skipped_merging_bryt": "Skipped merging complete panel for {0}.",
    "log_file_result_saved": "Result file saved: {0}",
    "log_file_result_save_error": "Result file save error {0}: {1}",
    "log_finished_split_horizontal": "--- Finished: COMMON SHEET - HORIZONTAL ---",
    "log_no_slices_split_vertical": "No panels to process in split_vertical.",
    "log_start_split_vertical": "--- Starting: COMMON SHEET - VERTICAL (Rotation handled in create_slice_reader) ---",
    "log_finished_split_vertical": "--- Finished: COMMON SHEET - VERTICAL ---",
    "log_unknown_layout": "Unknown layout for common sheet: '{0}'.",
    "log_unknown_output_type": "Unknown output type: '{0}'.",
    "log_finished_splitting_success": "--- Finished split process for: {0} - SUCCESS ---",
    "log_finished_splitting_errors": "--- Finished split process for: {0} - ERRORS OCCURRED ---",
    "log_value_error_in_splitting": "Input data or calculation error: {0}",
    "log_finished_splitting_critical_error": "--- Finished split process for: {0} - CRITICAL ERROR ---",
    "log_unexpected_error_in_splitting": "Unexpected error while splitting file {0}: {1}",

    #   Splitter - Test Mode (__main__)
    "log_script_mode_test": "splitter.py launched as main script (test mode).",
    "log_loaded_config": "Configuration loaded.",
    "log_error_loading_config": "Failed to load configuration: {0}",
    "log_created_example_pdf": "Created sample PDF file: {0}",
    "log_cannot_create_example_pdf": "Failed to create sample PDF: {0}",
    "log_start_test_split": "Starting test split of file: {0} to {1}",
    "log_test_split_success": "Test split completed successfully.",
    "log_test_split_errors": "Test split finished with errors.",

    # --- Logs - QR/Barcode (`barcode_qr.py`) ---
    "log_qr_empty_data": "Attempt to generate QR code for empty data.",
    "log_qr_generated": "QR code SVG generated for: {0}...",
    "log_qr_error": "QR code generation error for data '{0}': {1}",
    "log_barcode_empty_data": "Attempt to generate barcode for empty data.",
    "log_barcode_generated": "Barcode SVG generated for: {0}...",
    "log_barcode_error": "Barcode generation error for data '{0}': {1}",
    "log_basic_handler_configured": "Basic handler configured for logger in barcode_qr.py",
    "log_basic_handler_error": "Failed to configure basic logger handler in barcode_qr: {0}",

    # --- Logs - Config/Profiles (`main_config_manager.py`) ---
    "loading_profiles_from": "Loading profiles from",
    "profiles_file": "Profiles file",
    "does_not_contain_dict": "does not contain a dictionary. Creating a new one",
    "not_found_creating_new": "not found. Creating a new empty one",
    "json_profiles_read_error": "Error reading JSON profiles file",
    "file_will_be_overwritten": "File will be overwritten on save",
    "json_decode_error_in_profiles": "JSON decode error in profiles file",
    "cannot_load_profiles_file": "Cannot load profiles file",
    "unexpected_profiles_read_error": "Unexpected error reading profiles",
    "saving_profiles_to": "Saving profiles to",
    "cannot_save_profiles_file": "Cannot save profiles file",
    "profiles_save_error": "Error saving profiles to file",
    "logger_profile_saved": "Profile saved: {profile}",
    "logger_profile_not_found": "Profile not found to load: {profile}",
    "logger_profile_loaded": "Profile loaded: {profile}",
    "logger_profile_delete_not_exist": "Attempt to delete non-existent profile: {profile}",
    "logger_profile_deleted": "Profile deleted: {profile}",
    "logger_start_save_settings": "Started saving settings from GUI.",
    "logger_invalid_value": "Invalid value for '{key}'. Set to 0.0.",
    "logger_end_save_settings": "Finished saving settings from GUI.",
    "logger_conversion_error": "Value conversion error from GUI: {error}",
    "conversion_failed": "Conversion of GUI values failed",
    "logger_unexpected_save_error": "Unexpected error saving settings: {error}",
    "logger_settings_saved": "Settings saved to file: {file}",

    # --- Logs - Licensing (`main_license.py`) ---
    "public_key_load_error_log": "Public key loading error",
    "license_key_decode_error": "License key decoding error",
    "license_activation_error": "License activation error",

    # --- Logs - Main Module (`main.py`) ---
    "ui_created": "User interface has been created.",
    "error_tab_home": "Error creating 'Home' tab UI",
    "error_tab_settings": "Error creating 'Settings' tab UI",
    "error_tab_help": "Error creating 'Help' tab UI",
    "error_creating_license_ui": "Error creating 'License' tab UI",
    "error_loading_ui": "Error loading interface: {error}",
    "error_creating_home_ui": "Error creating 'Home' tab UI",
    "error_creating_settings_ui": "Error creating 'Settings' tab UI",
    "error_creating_help_ui": "Error creating 'Help' tab UI",
    "logger_update_gui": "Started updating GUI from configuration.",
    "logger_end_update_gui": "Finished updating GUI from configuration.",
    "logger_update_gui_error": "Unexpected error while updating GUI: {error}",
    "logger_invalid_output_dir": "Invalid or non-existent output directory: {directory}",
    "logger_invalid_input_file": "Invalid or non-existent input file: {file}",
    "logger_start_pdf": "Started PDF generation process.",
    "logger_pdf_save_error": "PDF generation aborted - failed to save current settings.",
    "logger_pdf_success": "PDF generation completed successfully.",
    "logger_pdf_exception": "Exception during main PDF generation process.",
    "icon_set_error": "Failed to set application icon: {error}",
    "accent_button_style_error": "Failed to set style for accent button: {error}",
    "logger_file_save_error": "File save error {file}: {error}",

    #   Logs - Preview (`main.py` - update_preview, update_output_preview)
    "thumbnail_error_log": "Thumbnail generation error",
    "output_preview_update_called": "Output preview update called",
    "output_preview_canvas_missing": "Output preview canvas missing",
    "pdf_found_in_output_dir": "PDF found in output directory",
    "preparing_thumbnail": "Preparing thumbnail",
    "thumbnail_generated_successfully": "Thumbnail generated successfully",
    "thumbnail_generation_error": "Thumbnail generation error for",
    "no_pdf_for_common_sheet": "No PDF file for common sheet preview",
    "no_pdf_for_separate_files": "No generated separate PDF files for preview",
    "cannot_load_thumbnail": "Cannot load thumbnail from",

    #   Logs - Developer / GUI internals (`main.py`)
    "missing_gui_var_created": "Created missing GUI variable for key: {key}",
    "missing_gui_structure_created": "Created missing GUI structure for: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Created missing GUI variable for: {code_type}/{output_type}/{layout}/{param}",

    # Additional keys for main_ui_help.py
    "help_text": """
बिलबोर्ड स्प्लिटर — उपयोगकर्ता मार्गदर्शिका

उद्देश्य:
बिलबोर्ड स्प्लिटर बिलबोर्ड डिज़ाइनों को स्वतः प्रिंट-योग्य पैनलों में विभाजित करता है।
प्रोग्राम 1:10 स्केल डिज़ाइनों के लिए बनाया गया है। ओवरलैप, सफ़ेद स्ट्राइप आदि मान 1:1 स्केल के अनुसार दर्ज करें।

आउटपुट प्रकार:
• कॉमन शीट: सभी पैनल एक ही PDF में।
• अलग फ़ाइलें: प्रत्येक पैनल अलग PDF फ़ाइल में।

अतिरिक्त क्षमताएँ:
• ऊर्ध्व/क्षैतिज लेआउट।
• पैनलों को 180° घुमाना।
• रजिस्ट्रेशन मार्क (क्रॉस/रेखा)।
• क्यूआर/बारकोड जोड़ना (समायोज्य स्केल/ऑफसेट/स्थान)।
• प्रोफ़ाइल के रूप में सेटिंग्स सहेजना, लोड करना और हटाना।

मूल चरण:
1) 'होम' में PDF/JPG/TIFF चुनें।
2) पंक्तियाँ/स्तम्भ, ओवरलैप और सफ़ेद स्ट्राइप सेट करें।
3) लेआउट (ऊर्ध्व/क्षैतिज) और आउटपुट (कॉमन/अलग) चुनें।
4) मार्क/कोड सक्षम करें और 'सेटिंग्स' में समायोजित करें।
5) प्रोफ़ाइल सहेजें (वैकल्पिक) और 'PDF बनाएँ' दबाएँ।

समस्या निवारण:
• 'logs' फ़ोल्डर में लॉग देखें।
• फ़ोल्डर/पथ सही हों यह सुनिश्चित करें।
• तकनीकी सहायता: tech@printworks.pl (कार्यदिवस, 8–16)
"""
}
