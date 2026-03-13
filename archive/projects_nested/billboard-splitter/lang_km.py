# lang_km.py
# -*- coding: utf-8 -*-
"""
Khmer (Cambodia) translations — LTR.
"""

LANG = {
    "barcode_font_size_label": "ទំហំពុម្ពអក្សរនៃលេខកូដផលិតផល [pt]:",
    "__meta__": {
        "language_name_native": "ខ្មែរ (កម្ពុជា)",
        "language_name_en": "Khmer (Cambodia)",
        "locale": "km-KH",
        "direction": "ltr",
        "font_hint": "Noto Sans Khmer, Noto Serif Khmer"
    },

    # General
    "app_title": "Billboard Splitter v1.8",
    "error": "កំហុស",
    "no_file": "គ្មានឯកសារ",
    "language": "ភាសា",
    "language_switch": "ប្តូរភាសា",
    "choose_language": "ជ្រើសរើសភាសា:",
    "apply_language": "អនុវត្ត",
    "language_changed": "ភាសាត្រូវបានប្តូរ។ ការផ្លាស់ប្ដូរខ្លះនឹងចូលជាធរមានក្រោយពេលបើកកម្មវិធីឡើងវិញ។",

    # Tabs
    "tab_home": " ទំព័រដើម ",
    "tab_settings": " ការកំណត់ ",
    "tab_help": " ជំនួយ ",
    "tab_license": " លីសិនស៍ ",

    # Buttons
    "button_browse": "រកមើល…",
    "browse_folder": "ជ្រើសរើសថត…",
    "button_save": "រក្សាទុក",
    "button_delete": "លុប",
    "button_close": "បិទ",
    "save_all_settings": "រក្សាទុកការកំណត់ទាំងអស់",

    # Home labels
    "label_rows": "ចែកបញ្ច្រាសឈរ (ជួរ):",
    "label_columns": "ចែកផ្តេក (ជួរឈរ):",
    "label_overlap": "ការភ្លៀងគ្នា (ស.ម.):",
    "label_white_stripe": "បន្ទាត់ស (ស.ម.):",
    "label_add_white_stripe": "រួមបញ្ចូលបន្ទាត់សក្នុងការភ្លៀងគ្នាដែលមានប្រសិទ្ធិភាព",
    "label_layout": "ប្លង់:",
    "label_output_type": "ប្រភេទលទ្ធផល:",
    "label_enable_reg_marks": "បើកសញ្ញាចុះបញ្ជី:",
    "label_enable_codes": "បើកកូដ:",
    "label_enable_sep_lines": "បើកបន្ទាត់បំបែក (រវាងបន្ទះ)",
    "label_enable_start_line": "បើកបន្ទាត់ខាងលើ/ចាប់ផ្តើមនៃសន្លឹក",
    "label_enable_end_line": "បើកបន្ទាត់ខាងក្រោម/បញ្ចប់នៃសន្លឹក",
    "label_bryt_order": "លំដាប់បន្ទះ:",
    "label_slice_rotation": "បង្វិលបន្ទះ:",
    "label_create_order_folder": "បង្កើតថតតាមលេខបញ្ជា",

    # Sections
    "section_input_file": " ឯកសារចូល ",
    "section_scale_and_dimensions": " មាត្រដ្ឋាន និងទំហំទិន្នផល ",
    "label_original_size": "ទំហំដើម:",
    "label_scale_non_uniform": "ធ្វើមាត្រដ្ឋានមិនសមាមាត្រ",
    "label_scale": "មាត្រដ្ឋាន: 1:",
    "label_scale_x": "មាត្រដ្ឋាន X: 1:",
    "label_scale_y": "មាត្រដ្ឋាន Y: 1:",
    "label_output_dimensions": "ទំហំឯកសារទិន្នផល:",
    "label_width_cm": "ទទឹង [cm]:",
    "label_height_cm": "កម្ពស់ [cm]:",
    "section_split_settings": " ការកំណត់បំបែក ",
    "section_profiles": " ប្រូហ្វាល ",
    "section_save_location": " ទីតាំងរក្សាទុក ",
    "section_input_preview": " មើលជាមុនឯកសារចូល ",
    "section_output_preview": " មើលជាមុនលទ្ធផល ",

    # Options
    "layout_vertical": "ឈរ",
    "layout_horizontal": "ផ្តេក",
    "output_common_sheet": "សន្លឹករួម",
    "output_separate_files": "ឯកសារផ្តាច់មុខ",
    "output_both": "សន្លឹករួម និងឯកសារផ្តាច់មុខ",
    "output_common": "សន្លឹករួម",
    "output_separate": "ឯកសារផ្តាច់មុខ",
    "reg_mark_cross": "ឈើឆ្កាង",
    "reg_mark_line": "បន្ទាត់",
    "code_qr": "QR កូដ",
    "code_barcode": "បាកូដ",
    "bryt_order_1": "A1–An, B1–Bn … ស្តង់ដារ ពីលើចុះក្រោម",
    "bryt_order_2": "A1–An, Bn–B1 … សាក់ស្ការ (តាមជួរ) ពីលើចុះក្រោម",
    "bryt_order_3": "A1..B1, A2..B2 … តាមជួរឈរ ពីលើចុះក្រោម",
    "bryt_order_4": "A1–A2..B2–B1 … សាក់ស្ការ (តាមជួរឈរ) ពីលើចុះក្រោម",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … ស្តង់ដារ ពីក្រោមឡើងលើ",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … សាក់ស្ការ (តាមជួរ) ពីក្រោមឡើងលើ",
    "logging_console": "កុងសូល",
    "logging_file": "ឯកសារ",
    "logging_both": "ទាំងពីរ",

    # Settings sections
    "section_processing_mode": " ការងារកាត់ ",
    "processing_mode_ram": "RAM (អង្គចងចាំ)",
    "processing_mode_hdd": "HDD (ឌីស)",
    "graphic_settings": "ការកំណត់ក្រាហ្វិក",
    "code_settings": "ការកំណត់ QR/បាកូដ",
    "logging_settings": "ការកំណត់កំណត់ហេតុ",
    "barcode_text_position_label": "ទីតាំងអក្សរបាកូដ:",
    "barcode_text_bottom": "ខាងក្រោម",
    "barcode_text_side": "ខាងជាប់",
    "barcode_text_none": "គ្មាន",

    # Graphics
    "extra_margin_label": "រឹមជុំវិញបន្ទះ (ស.ម.):",
    "margin_top_label": "រឹមលើ (ស.ម.):",
    "margin_bottom_label": "រឹមក្រោម (ស.ម.):",
    "margin_left_label": "រឹមឆ្វេង (ស.ម.):",
    "margin_right_label": "រឹមស្ដាំ (ស.ម.):",
    "reg_mark_width_label": "សញ្ញាចុះបញ្ជី — ទទឹង (ស.ម.):",
    "reg_mark_height_label": "សញ្ញាចុះបញ្ជី — កម្ពស់ (ស.ម.):",
    "reg_mark_white_line_width_label": "សញ្ញាចុះបញ្ជី — កម្រាស់បន្ទាត់ស (ស.ម.):",
    "reg_mark_black_line_width_label": "សញ្ញាចុះបញ្ជី — កម្រាស់បន្ទាត់ខ្មៅ (ស.ម.):",
    "sep_line_black_width_label": "បន្ទាត់បំបែក — កម្រាស់បន្ទាត់ខ្មៅ (ស.ម.):",
    "sep_line_white_width_label": "បន្ទាត់បំបែក — កម្រាស់បន្ទាត់ស (ស.ម.):",
    "slice_gap_label": "ចន្លោះរវាងបន្ទះ (ស.ម.):",
    "label_draw_slice_border": "គូសស៊ុមបន្ទះ (បន្ទាត់កាត់)",

    # Codes
    "scale_label": "មាត្រដ្ឋាន (ស.ម.):",
    "scale_x_label": "ទទឹង X (ស.ម.):",
    "scale_y_label": "កម្ពស់ Y (ស.ម.):",
    "offset_x_label": "អុហ្វសិត X (ស.ម.):",
    "offset_y_label": "អុហ្វសិត Y (ស.ម.):",
    "rotation_label": "បង្វិល (°):",
    "anchor_label": "ចំណុច anchore:",

    # Logging (GUI)
    "logging_mode_label": "របៀបកំណត់ហេតុ:",
    "log_file_label": "ឯកសារកំណត់ហេតុ:",
    "logging_level_label": "កម្រិតកំណត់ហេតុ:",

    # Home actions
    "button_load": "ផ្ទុក",
    "button_save_settings": "រក្សាទុកការកំណត់បច្ចុប្បន្ន",
    "button_generate_pdf": "បង្កើត PDF",
    "button_refresh_preview": "ធ្វើបច្ចុប្បន្នភាពមើលជាមុន",
    "button_refresh_layout": "ធ្វើបច្ចុប្បន្នភាពប្លង់",

    # License (GUI)
    "hwid_frame_title": "លេខសម្គាល់ផ្នែករឹង (HWID)",
    "copy_hwid": "ថតចម្លង HWID",
    "license_frame_title": "ការធ្វើឱ្យសកម្មលីសិនស៍",
    "enter_license_key": "បញ្ចូលលេខគ្រាប់លីសិនស៍:",
    "activate": "ធ្វើឱ្យសកម្ម",
    "status_trial": "របៀបសាកល្បង",
    "license_active": "លីសិនស៍សកម្ម",

    # Messages — Profiles
    "msg_no_profile_name": "គ្មានឈ្មោះ",
    "msg_enter_profile_name": "បញ្ចូលឈ្មោះប្រូហ្វាលដើម្បីរក្សាទុក។",
    "msg_profile_saved": "បានរក្សាទុកប្រូហ្វាល",
    "profile_saved_title": "រក្សាទុកប្រូហ្វាល",
    "msg_profile_saved_detail": "បានរក្សាទុកប្រូហ្វាល '{0}'.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "โปรไฟล์ '{profile}' ត្រូវបានบันทึก និងអនុវត្ត។",
    "msg_no_profile": "គ្មានប្រូហ្វាល",
    "warning_no_profile": "គ្មានប្រូហ្វាល",
    "msg_select_profile": "ជ្រើសប្រូហ្វាលពីបញ្ជីដើម្បីផ្ទុក។",
    "select_profile": "ជ្រើសប្រូហ្វាលពីបញ្ជីដើម្បីផ្ទុក។",
    "profile_loaded_title": "បានផ្ទុកប្រូហ្វាល",
    "profile_loaded": "បានផ្ទុកប្រូហ្វាល '{profile}'.",
    "warning_no_profile_delete": "គ្មានប្រូហ្វាល",
    "warning_no_profile_delete_message": "ជ្រើសប្រូហ្វាលពីបញ្ជីដើម្បីលុប។",
    "profile_not_found": "រកមិនឃើញប្រូហ្វាល '{profile}'.",
    "profile_not_exist": "ប្រូហ្វាល '{profile}' មិនមានទេ។",
    "confirm_delete_title": "អះអាងការលុប",
    "confirm_delete_profile": "តើអ្នកប្រាកដថាចង់លុបប្រូហ្វាល '{profile}' មែនទេ?",
    "profile_deleted_title": "បានលុបប្រូហ្វាល",
    "profile_deleted": "បានលុបប្រូហ្វាល '{profile}'.",

    # Files / Dirs
    "msg_no_input_file": "គ្មានឯកសារចូល",
    "msg_unsupported_format": "ទ្រង់ទ្រាយមិនត្រូវបានគាំទ្រ",
    "select_file_title": "ជ្រើសឯកសារចូល",
    "supported_files": "ឯកសារគាំទ្រ",
    "all_files": "ឯកសារទាំងអស់",
    "select_dir_title": "ជ្រើសថតលទ្ធផល",
    "select_log_dir_title": "ជ្រើសថតកំណត់ហេតុ",
    "error_output_dir_title": "កំហុសថតលទ្ធផល",
    "error_output_dir": "ថតលទ្ធផលដែលបានជ្រើសមិនត្រឹមត្រូវ ឬមិនមាន:\n{directory}",
    "error_input_file_title": "កំហុសឯកសារចូល",
    "error_input_file": "ឯកសារចូលដែលបានជ្រើសមិនត្រឹមត្រូវ ឬមិនមាន:\n{file}",
    "save_file_error_title": "កំហុសរក្សាទុកឯកសារ",
    "save_file_error": "មិនអាចរក្សាទុកឯកសារ: {error}",

    # PDF / Preview
    "msg_pdf_processing_error": "បរាជ័យក្នុងការដំណើរការ PDF",
    "msg_thumbnail_error": "កំហុសក្នុងការផ្ទុករូបភម្រួល",
    "msg_no_pdf_output": "មិនទាន់មានលទ្ធផល PDF",
    "no_pdf_pages": "ឯកសារ PDF គ្មានទំព័រ",
    "unsupported_output": "ប្រភេទលទ្ធផលនេះមិនគាំទ្រការមើលជាមុនទេ",
    "pdf_generated_title": "បញ្ចប់ការបង្កើត",
    "pdf_generated": "ឯកសារ PDF បានបង្កើតដោយជោគជ័យនៅក្នុងថត:\n{directory}",
    "pdf_generation_error_title": "កំហុសបង្កើត",
    "pdf_generation_error": "កំហុសកើតឡើងខណៈពេលបង្កើត PDF។ សូមពិនិត្យកំណត់ហេតុ។",
    "critical_pdf_error_title": "កំហុសធ្ងន់ធ្ងរពេលបង្កើត PDF",
    "critical_pdf_error": "កំហុសធ្ងន់ធ្ងរនៅពេលបង្កើត PDF:\n{error}\nសូមពិនិត្យកំណត់ហេតុ។",

    # Settings save/update
    "settings_saved_title": "បានរក្សាទុកការកំណត់",
    "settings_saved": "បានរក្សាទុកការកំណត់ទៅឯកសារ:\n{filepath}",
    "settings_save_error_title": "កំហុសរក្សាទុកការកំណត់",
    "settings_save_error": "មិនអាចរក្សាទុកការកំណត់: {error}",
    "conversion_error_title": "កំហុសបម្លែង",
    "conversion_error": "កំហុសពេលបម្លែងតម្លៃពី GUI: {error}",
    "update_gui_error_title": "កំហុសធ្វើបច្ចុប្បន្នភាពចំណុចប្រទាក់",
    "update_gui_error": "កំហុសពេលធ្វើបច្ចុប្បន្នភាពចំណុចប្រទាក់: {error}",

    # License ops (GUI messages)
    "hwid_copied_to_clipboard": "HWID ត្រូវបានចម្លងទៅក្តារតម្បៀតខ្ទាស់",
    "computer_hwid": "HWID កុំព្យូទ័រ",
    "public_key_load_error": "កំហុសផ្ទុកសោសាធារណៈ: {error}",
    "invalid_license_format": "ទ្រង់ទ្រាយកូនសោលីសិនស៍មិនត្រឹមត្រូវ: {error}",
    "activation_success": "បានធ្វើឱ្យសកម្មលីសិនស៍ដោយជោគជ័យ។",
    "activation_error": "កំហុសពេលធ្វើឱ្យសកម្មលីសិនស៍: {error}",
    "log_trial_mode_active": "របៀបសាកល្បងកំពុងដំណើរការ",
    "log_trial_mode_inactive": "របៀបសាកល្បងត្រូវបានបិទ",

    # Initialization (GUI)
    "init_error_title": "កំហុសចាប់ផ្តើម",
    "init_error": "កំហុសពេលបង្កើតថត: {error}",
    "poppler_path_info": "ព័ត៌មានផ្លូវ Poppler",
    "ttkthemes_not_installed": "ព្រមាន: មិនបានដំឡើង 'ttkthemes' ទេ។ នឹងប្រើស្ទីឡើ Tkinter លំនាំដើម។",

    # Logs — kept in English intentionally
    "log_configured": "Logging configured: level={0}, mode={1}, file={2}",
    "log_no_handlers": "Warning: No logging handlers configured (mode: {0}).",
    "log_critical_error": "Critical logging configuration error: {0}",
    "log_basic_config": "Basic logging configuration used due to an error.",
    "log_dir_create_error": "Critical error: Cannot create logs directory {0}: {1}",

    "error_critical_init": "CRITICAL ERROR during initialization: {0}",
    "logger_init_error": "Directory initialization error: {error}",
    "directory_created": "Created directory: {0}",
    "directory_creation_error": "Failed to create directory {0}: {1}",
    "sample_file_copied": "Sample file copied to {0}",
    "sample_file_copy_error": "Error copying sample file: {0}",
    "log_created_output_dir": "Output directory created: {0}",
    "log_cannot_create_output_dir": "Cannot create output directory {0}: {1}",

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

    "log_generating_slice_info": "Generating panel info: {0}",
    "log_no_slices_info_generated": "Failed to generate panels info.",
    "log_applying_rotated_order": "Applying order for 180-degree rotation: {0}",
    "log_applying_standard_order": "Applying order for 0-degree rotation (standard): {0}",
    "log_unknown_bryt_order": "Unknown panels order: '{0}'. Using default.",
    "log_final_slices_order": "  Final panels order ({0}): [{1}]",

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

    "log_drawing_separation_lines_for_page": "Drawing separation lines for page (layout={0}, total_slices={1}, slice_index={2})",
    "log_vertical_line_between_slices": "  Vertical line between panels {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Vertical line start @ x={0:.1f}",
    "log_vertical_line_end": "  Vertical line end @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Horizontal line between panels {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Horizontal line start @ y={0:.1f}",
    "log_horizontal_line_end": "  Horizontal line end @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Separate_files) Vertical/Horizontal line start @ {0:.1f}",
    "log_sep_line_end_separate": "  (Separate_files) Vertical/Horizontal line end @ {0:.1f}",

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

    # Help
    "help_text": """
Billboard Splitter — សៀវភៅណែនាំអ្នកប្រើ

គោលបំណង:
Billboard Splitter បំបែកគម្រោងបដាពាណិជ្ជកម្មទៅជាបន្ទះដែលរួចរាល់សម្រាប់បោះពុម្ពដោយស្វ័យប្រវត្តិ។
កម្មវិធីសន្មត់មាត្រដ្ឋាន 1:10។ បញ្ចូលតម្លៃការភ្លៀងគ្នា និងបន្ទាត់ស ដោយយោង 1:1។

ប្រភេទលទ្ធផល:
• សន្លឹករួម: បន្ទះទាំងអស់ក្នុង PDF ដោយមួយ។
• ឯកសារផ្តាច់មុខ: រៀងៗខ្លួនជាឯកសារ PDF មួយ។

លក្ខណៈបន្ថែម:
• ប្លង់ឈរ/ផ្តេក, បង្វិលបន្ទះ 180°,
• សញ្ញាចុះបញ្ជី (ឈើឆ្កាង/បន្ទាត់),
• បន្ថែម QR/បាកូដ (កំណត់មាត្រដ្ឋាន/អុហ្វសិត/ទីតាំង),
• រក្សាទុក/ផ្ទុក/លុបការកំណត់ជាប្រូហ្វាល។

ជំហានមូលដ្ឋាន:
1) ជ្រើស PDF/JPG/TIFF នៅ 'ទំព័រដើម'.
2) កំណត់ជួរ/ជួរឈរ ការភ្លៀងគ្នា និងបន្ទាត់ស។
3) ជ្រើសប្លង់ និងប្រភេទលទ្ធផល។
4) បើកសញ្ញា/កូដ និងលៃតម្រូវនៅ 'ការកំណត់'។
5) (ជម្រើស) រក្សាទុកប្រូហ្វាល ហើយចុច 'បង្កើត PDF'។

ដោះស្រាយបញ្ហា:
• ពិនិត្យកំណត់ហេតុក្នុងថត 'logs'។
• ប្រាកដថាផ្លូវ/ថតត្រឹមត្រូវ។
• ជំនួយបច្ចេកទេស: tech@printworks.pl (ថ្ងៃធ្វើការ 8–16)
"""
}
