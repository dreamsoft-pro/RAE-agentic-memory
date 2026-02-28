# lang_en.py
"""
File containing translations for the English language.
"""

LANG = {
    # ==========================
    #  Application - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Error",  # Generic error title
    "no_file": "No file",  # Generic 'no file' text
    "language": "Language",  # Label in menu or settings
    "language_switch": "Language switch",  # Window/section title
    "choose_language": "Choose language:",  # Label
    "apply_language": "Apply",  # Button
    "language_changed": "Language has been changed. Some changes will be visible after restarting the application.",  # Post-change notice

    # ========================================
    #  User Interface (GUI) Elements
    # ========================================

    # --- Main Tabs ---
    "tab_home": " Home ",
    "tab_settings": " Settings ",
    "tab_help": " Help ",
    "tab_license": " License ",

    # --- General Buttons ---
    "button_browse": "Browse...",
    "browse_folder": "Browse folder...",  # Often used when choosing a directory
    "button_save": "Save",
    "button_delete": "Delete",
    "button_close": "Close",
    "save_all_settings": "Save all settings",  # Button in Settings tab

    # --- Field Labels (Home Tab) ---
    "label_rows": "Vertical split (rows):",
    "label_columns": "Horizontal split (columns):",
    "label_overlap": "Overlap [mm]:",
    "label_white_stripe": "White stripe [mm]:",
    "label_add_white_stripe": "Add white stripe to effective overlap",  # Checkbox
    "label_layout": "Output layout:",
    "label_output_type": "Output type:",
    "label_enable_reg_marks": "Enable registration marks:",  # Checkbox
    "label_enable_codes": "Enable codes:",  # Checkbox
    "label_enable_sep_lines": "Enable separation lines (between panels)",  # Checkbox
    "label_enable_start_line": "Enable start/top line of sheet",  # Checkbox
    "label_enable_end_line": "Enable end/bottom line of sheet",  # Checkbox
    "label_bryt_order": "Panels order:",
    "label_slice_rotation": "Panels rotation:",
    "label_create_order_folder": "Create folder with order number",

    # --- Sections/Frames (Home Tab) ---
    "section_input_file": " Input file ",
    "section_scale_and_dimensions": " Scale and output dimensions ",
    "label_original_size": "Original size:",
    "label_scale_non_uniform": "Scale non-uniformly",
    "label_scale": "Scale: 1:",
    "label_scale_x": "Scale X: 1:",
    "label_scale_y": "Scale Y: 1:",
    "label_output_dimensions": "Output file dimensions:",
    "label_width_cm": "Width [cm]:",
    "label_height_cm": "Height [cm]:",
    "section_split_settings": " Split settings ",
    "section_profiles": " Settings profiles ",
    "section_save_location": " Save location ",
    "section_input_preview": " Input file preview ",
    "section_output_preview": " Output file preview ",

    # --- Option Values (Combobox, Radiobutton etc.) ---
    "layout_vertical": "Vertical",
    "layout_horizontal": "Horizontal",
    "output_common_sheet": "Common sheet",
    "output_separate_files": "Separate files",
    "output_both": "Common sheet and separate files",
    "output_common": "Common sheet",   # Also used as frame label in code settings
    "output_separate": "Separate files",  # Also used as frame label in code settings
    "reg_mark_cross": "Cross",
    "reg_mark_line": "Line",
    "code_qr": "QR Code",
    "code_barcode": "Barcode",
    "bryt_order_1": "A1-An, B1-Bn, .. Standard, from top",
    "bryt_order_2": "A1-An, Bn-B1, .. Snake by rows, from top",
    "bryt_order_3": "A1..B1, A2..B2, .. By columns, from top",
    "bryt_order_4": "A1-A2..B2-B1.. Snake by columns, from top",
    "bryt_order_5": "N1-Nn, (N-1)1-(N-1)n, .. Standard, from bottom",
    "bryt_order_6": "N1-Nn, (N-1)n-(N-1)1, .. Snake by rows, from bottom",
    "logging_console": "console",  # Logging mode: console only
    "logging_file": "file",        # Logging mode: file only
    "logging_both": "both",        # Logging mode: console and file

    # --- Sections/Frames (Settings Tab) ---
    "section_processing_mode": " Cutting operations ",
    "processing_mode_ram": "RAM (in memory)",
    "processing_mode_hdd": "HDD (on disk)",
    "graphic_settings": "Graphic settings",
    "code_settings": "QR / Barcode settings",
    "logging_settings": "Logging settings",
    "barcode_text_position_label": "Barcode text position:",
    "barcode_text_bottom": "below",
    "barcode_text_side": "beside",
    "barcode_text_none": "none",

    # --- Field Labels (Settings Tab - Graphics) ---
    "extra_margin_label": "Margin around panels [mm]:",
    "margin_top_label": "Top margin [mm]:",
    "margin_bottom_label": "Bottom margin [mm]:",
    "margin_left_label": "Left margin [mm]:",
    "margin_right_label": "Right margin [mm]:",
    "reg_mark_width_label": "Registration mark - Width [mm]:",
    "reg_mark_height_label": "Registration mark - Height [mm]:",
    "reg_mark_white_line_width_label": "Registration mark - White line thickness [mm]:",
    "reg_mark_black_line_width_label": "Registration mark - Black line thickness [mm]:",
    "sep_line_black_width_label": "Separation line - Black line thickness [mm]:",
    "sep_line_white_width_label": "Separation line - White line thickness [mm]:",
    "slice_gap_label": "Gap between panels [mm]:",
    "label_draw_slice_border": "Draw border around panel (cut line)",

    # --- Field Labels (Settings Tab - Codes) ---
    "scale_label": "Size [mm]:",      # For QR Code
    "scale_x_label": "Width X [mm]:", # For Barcode
    "scale_y_label": "Height Y [mm]:",# For Barcode
    "offset_x_label": "Offset X [mm]:",
    "offset_y_label": "Offset Y [mm]:",
    "rotation_label": "Rotation (°):",
    "anchor_label": "Corner:",

    # --- Field Labels (Settings Tab - Logging) ---
    "logging_mode_label": "Logging mode:",
    "log_file_label": "Log file:",
    "settings_log_filename_label": "Log file name:",
    "settings_log_level_label": "Log level:",
    "settings_log_to_file_label": "Save logs to file",

    "rasterization_title": "Input Rasterization",
    "rasterization_enable": "Enable rasterization",
    "rasterization_dpi": "Resolution (DPI)",
    "rasterization_compression": "Compression",
    "rasterization_compression_none": "None",
    "rasterization_compression_lzw": "LZW (lossless)",

    "actual_size": "Actual size",
    "size_read_error": "Error reading size",
    "preview_error": "Preview error",

    "section_product_mode": "Product Mode",
    "product_mode_billboard": "Billboard",
    "product_mode_poster": "Poster",
    "product_mode_pos": "POS",
    "section_poster_settings": "Poster Settings",
    "poster_repetitions": "Repetitions",
    "poster_external_margin": "External Margin",
    "poster_separation_lines": "Separation Lines",
    "poster_input_rotation": "Input Rotation",
    "poster_vertical_cut_marks": "Vertical Cut Marks",
    "poster_gap": "Gap Between Posters",

    "section_manufacturer_spec": "Manufacturer Specification",
    "spec_enable": "Use manufacturer specification",
    "spec_name": "Specification name",

    "help_title": "Help & Information",
    "help_content": "This is the help content...",
    "info_title": "About the application",

    # --- Buttons / Actions (Home Tab) ---
    "button_load": "Load",  # Profile button
    "button_save_settings": "Save current settings",  # Profile button
    "button_generate_pdf": "Generate PDF",  # Main action button
    "button_refresh_preview": "Refresh preview",  # Input preview button
    "button_refresh_layout": "Refresh layout",  # (?) Maybe refresh output preview?

    # --- License (GUI) ---
    "hwid_frame_title": "Unique hardware identifier (HWID)",
    "copy_hwid": "Copy HWID",  # Button
    "license_frame_title": "License activation",
    "enter_license_key": "Enter the license key:",  # Label
    "activate": "Activate",  # Button
    "status_trial": "Trial mode",  # License status
    "license_active": "License active",  # License status

    # ================================================
    #  User Messages (Windows, Status Bar)
    # ================================================

    # --- Profiles ---
    "msg_no_profile_name": "No name",  # Error title
    "msg_enter_profile_name": "Enter a profile name to save.",  # Error/warning text
    "msg_profile_saved": "Profile saved",  # Success title
    "profile_saved_title": "Profile saved",  # Title in logger/window? (from main.py)
    "msg_profile_saved_detail": "Profile '{0}' has been saved.",  # Success text
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profile '{profile}' has been saved and applied.",  # Success text (from main.py)
    "msg_no_profile": "No profile",  # Error title
    "warning_no_profile": "No profile",  # Error title (from main.py)
    "msg_select_profile": "Select a profile name from the list to load.",  # Error/warning text
    "select_profile": "Select a profile name from the list to load.",  # Error/warning text (from main.py)
    "profile_loaded_title": "Profile loaded",  # Info title (from main.py)
    "profile_loaded": "Profile '{profile}' has been loaded.",  # Info text (from main.py)
    "warning_no_profile_delete": "No profile",  # Delete error title (from main.py)
    "warning_no_profile_delete_message": "Select a profile from the list to delete.",  # Delete error text (from main.py)
    "profile_not_found": "Profile '{profile}' was not found.",  # Error message (from main.py)
    "profile_not_exist": "Profile '{profile}' does not exist.",  # Delete error (from main.py)
    "confirm_delete_title": "Confirm deletion",  # Confirm window title (from main.py)
    "confirm_delete_profile": "Are you sure you want to delete profile '{profile}'?",  # Confirmation text (from main.py)
    "profile_deleted_title": "Profile deleted",  # Success title (from main.py)
    "profile_deleted": "Profile '{profile}' has been deleted.",  # Success text (from main.py)

    # --- Files / Directories ---
    "msg_no_input_file": "No input file",  # Error title
    "msg_unsupported_format": "Unsupported format",  # Error title
    "select_file_title": "Select input file",  # Dialog title
    "supported_files": "Supported files",  # File filter
    "all_files": "All files",  # File filter
    "select_dir_title": "Select output directory",  # Dialog title
    "select_log_dir_title": "Select directory for log files",  # Dialog title
    "error_output_dir_title": "Output directory error",  # Error title (from main.py)
    "error_output_dir": "The specified output directory is invalid or does not exist:\n{directory}",  # Error text (from main.py)
    "error_input_file_title": "Input file error",  # Error title (from main.py)
    "error_input_file": "The specified input file is invalid or does not exist:\n{file}",  # Error text (from main.py)
    "save_file_error_title": "File save error",  # Error title (from main.py)
    "save_file_error": "Failed to save file: {error}",  # Error text (from main.py)

    # --- PDF Processing / Preview ---
    "msg_pdf_processing_error": "Failed to process PDF file",  # Error title
    "msg_thumbnail_error": "Thumbnail loading error",  # Error title
    "msg_no_pdf_output": "No PDF output",  # Info/warning title (for preview)
    "no_pdf_pages": "No pages in PDF file",  # Preview message (from main.py)
    "unsupported_output": "Unsupported output type for preview",  # Preview message (from main.py)
    "pdf_generated_title": "Generation completed",  # Success title (from main.py)
    "pdf_generated": "PDF file(s) have been successfully generated in the directory:\n{directory}",  # Success text (from main.py)
    "pdf_generation_error_title": "Generation error",  # Error title (from main.py)
    "pdf_generation_error": "Errors occurred while generating the PDF. Check the logs for more information.",  # Error text (from main.py)
    "critical_pdf_error_title": "Critical PDF generation error",  # Error title (from main.py)
    "critical_pdf_error": "A critical error occurred while generating the PDF:\n{error}\nCheck the logs.",  # Error text (from main.py)

    # --- Settings ---
    "settings_saved_title": "Settings saved",  # Info title (from main.py)
    "settings_saved": "Settings have been saved to the file:\n{filepath}",  # Info text (from main.py)
    "settings_save_error_title": "Settings save error",  # Error title (from main.py)
    "settings_save_error": "Failed to save settings: {error}",  # Error text (from main.py)
    "conversion_error_title": "Conversion error",  # Error title (from main.py)
    "conversion_error": "Error while converting values from the GUI: {error}",  # Error text (from main.py)
    "update_gui_error_title": "GUI update error",  # Error title (from main.py)
    "update_gui_error": "An error occurred while updating the interface: {error}",  # Error text (from main.py)

    # --- License ---
    "hwid_copied_to_clipboard": "HWID has been copied to the clipboard",  # Info message
    "computer_hwid": "Computer HWID",  # Label (?)
    "public_key_load_error": "Error loading public key: {error}",  # Error message
    "invalid_license_format": "Invalid license key format: {error}",  # Error message
    "activation_success": "License has been successfully activated.",  # Success message
    "activation_error": "License activation error: {error}",  # Error message
    "log_trial_mode_active": "Trial mode is active",
    "log_trial_mode_inactive": "Trial mode is inactive",

    # --- Initialization ---
    "init_error_title": "Initialization error",  # Error title (from main.py)
    "init_error": "Error initializing directories: {error}",  # Error text (from main.py)
    "poppler_path_info": "Poppler path information",  # Window title (from main.py - get_poppler_path)
    "ttkthemes_not_installed": "Warning: The ttkthemes library is not installed. Using the default Tkinter style.",  # Warning (from main.py)

    # =====================================
    #  Logs (Logger Messages)
    # =====================================

    # --- General Logging / Configuration ---
    "log_configured": "Logging configured: level={0}, mode={1}, file={2}",
    "log_no_handlers": "Warning: No logging handlers configured (mode: {0}).",
    "log_critical_error": "Critical logging configuration error: {0}",
    "log_basic_config": "Basic logging configuration used due to an error.",
    "log_dir_create_error": "Critical error: Cannot create logs directory {0}: {1}",  # Could also be in Init section

    # --- Logs - Initialization / Directories (`init_directories.py`) ---
    "error_critical_init": "CRITICAL ERROR during initialization: {0}",  # Generic init error
    "logger_init_error": "Directory initialization error: {error}",  # Log from main.py
    "directory_created": "Created directory: {0}",
    "directory_creation_error": "Failed to create directory {0}: {1}",
    "sample_file_copied": "Sample file copied to {0}",
    "sample_file_copy_error": "Error copying sample file: {0}",
    "log_created_output_dir": "Output directory created: {0}",  # From split_* methods
    "log_cannot_create_output_dir": "Cannot create output directory {0}: {1}",  # From split_* methods

    # --- Logs - Splitter (`splitter.py`) ---
    #   Splitter - Initialization and Loading
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
    "log_input_file_not_exists": "Input file does not exist or path is empty: '{0}'",  # From split() method
    "log_cannot_load_or_empty_pdf": "Failed to load input file or PDF is empty/corrupted.",  # From split()
    "log_pdf_dimensions_info": "  PDF dimensions: {0:.1f}mm x {1:.1f}mm",  # From split()
    "log_invalid_pdf_dimensions": "Invalid PDF page dimensions: {0}x{1} pt.",  # From split()

    #   Splitter - Dimension Calculations
    "log_extra_margin": "Extra margin set to {0:.3f} pt",
    "log_invalid_rows_cols": "Invalid number of rows ({0}) or columns ({1}).",
    "error_invalid_rows_cols": "Rows and columns must be positive integers.",  # User error
    "log_invalid_overlap_white_stripe": "Invalid overlap ({0}) or white stripe ({1}) values. They must be numbers.",
    "error_invalid_overlap_white_stripe": "Overlap and white stripe must be numeric values (mm).",  # User error
    "log_stripe_usage": "Set use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Base overlap (graphics): {0:.3f} mm, White stripe: {1:.3f} mm, Effective overlap: {2:.3f} mm",
    "log_computed_dimensions": "Computed dimensions: PDF: {0:.3f}mm x {1:.3f}mm. Panel: {2:.3f}pt ({3:.3f}mm) x {4:.3f}pt ({5:.3f}mm). Core: {6:.3f}pt x {7:.3f}pt. Effective overlap: {8:.3f}mm",
    "log_invalid_dimensions": "Computed panel ({0:.3f}x{1:.3f}) or core ({2:.3f}x{3:.3f}) dimensions are invalid for overlap={4}, stripe={5}, r={6}, c={7}, W={8}mm, H={9}mm",  # Improved dimension error log
    "error_invalid_slice_dimensions": "Computed panel/core dimensions are invalid or negative.",  # User error

    #   Splitter - Generating Panels Info and Order
    "log_generating_slice_info": "Generating panel info: {0}",
    "log_no_slices_info_generated": "Failed to generate panels info.",
    "log_applying_rotated_order": "Applying order for 180-degree rotation: {0}",  # Sorting logic
    "log_applying_standard_order": "Applying order for 0-degree rotation (standard): {0}",  # Sorting logic
    "log_unknown_bryt_order": "Unknown panels order: '{0}'. Using default.",  # From split()
    "log_final_slices_order": "  Final panels order ({0}): [{1}]",  # From split()

    #   Splitter - Creating Overlays and Merging
    "log_invalid_dimensions_overlay": "Attempt to create an overlay with invalid dimensions: {0}. Skipping.",
    "log_empty_overlay": "Created an empty or nearly empty overlay PDF. Skipping merge.",
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
    "log_merging_code_overlay_for_slice": "Code overlay for {0} merged without rotation.",  # For separate files
    "log_merging_separation_overlay_for_slice": "Separation lines overlay for {0} merged without rotation.",  # For separate files

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

    # Watermark
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
    "error_generate_qr_svg": "Failed to generate QR code SVG.",  # User error
    "error_invalid_scale_for_qr": "Invalid scale for QR: {0}mm",  # User error
    "error_invalid_qr_scale_factor": "Invalid scale factor for QR: {0}",  # User error
    "error_generate_barcode_svg": "Failed to generate barcode SVG.",  # User error
    "error_invalid_scale_for_barcode": "Invalid scale for Barcode: {0}x{1}mm",  # User error
    "error_invalid_barcode_scale_factor": "Invalid scale factor for Barcode: ({0:.4f}, {1:.4f})",  # User error
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
    "log_invalid_dimensions_in_slice_info": "Invalid dimensions in slice_info for {0}: {1}x{2}",  # When creating reader
    "log_content_transform": "Content transformation T_content for {0}: {1}",  # When creating reader
    "log_merged_content_for_slice": "Merged content for panel {0} on new_page",  # When creating reader
    "log_slice_reader_created": "Created complete slice (PdfReader) for panel {0}",  # When creating reader
    "log_slice_reader_creation_error": "Error creating complete slice for panel {0}: {1}",  # When creating reader
    "log_used_get_transform": "Used _get_transform (translation only): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Starting: SEPARATE FILES (Rotation handled in create_slice_reader) ---",
    "log_creating_file_for_slice": "Creating file for panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Invalid page size ({0}x{1}) for {2}. Skipping.",  # For separate files
    "log_blank_page_creation_error": "Error creating page for {0} (size {1}x{2}): {3}. Skipping.",  # For separate files
    "log_transform_for_slice": "Transform T (translation only) for {0}: {1}",  # For separate files
    "log_merging_complete_slice": "Merging complete panel {0} with transform: {1}",  # For separate files
    "log_skipped_slice_merging": "Skipped merging complete panel for {0}.",  # For separate files
    "log_file_saved": "File saved: {0}",  # For separate files
    "log_file_save_error": "File save error {0}: {1}",  # For separate files and final
    "log_finished_split_separate_files": "--- Finished: SEPARATE FILES (Saved {0}/{1}) ---",
    "log_no_slices_split_horizontal": "No panels to process in split_horizontal.",
    "log_start_split_horizontal": "--- Starting: COMMON SHEET - HORIZONTAL (Rotation handled in create_slice_reader) ---",
    "log_page_dimensions": "Page dimensions: {0:.1f}mm x {1:.1f}mm ({2} panels)",  # For common sheet H/V
    "log_page_creation_error": "Error creating result page ({0}x{1}): {2}. Aborting.",  # For common sheet H/V
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",  # For common sheet H/V
    "log_transform_t_only": "Transform T (translation only) for {0}: {1}",  # For common sheet H/V
    "log_merging_complete_bryt": "Merging complete panel {0} with transform: {1}",  # For common sheet H/V
    "log_skipped_merging_bryt": "Skipped merging complete panel for {0}.",  # For common sheet H/V
    "log_file_result_saved": "Result file saved: {0}",  # For common sheet H/V
    "log_file_result_save_error": "Result file save error {0}: {1}",  # For common sheet H/V
    "log_finished_split_horizontal": "--- Finished: COMMON SHEET - HORIZONTAL ---",
    "log_no_slices_split_vertical": "No panels to process in split_vertical.",
    "log_start_split_vertical": "--- Starting: COMMON SHEET - VERTICAL (Rotation handled in create_slice_reader) ---",
    "log_finished_split_vertical": "--- Finished: COMMON SHEET - VERTICAL ---",
    "log_unknown_layout": "Unknown layout for common sheet: '{0}'.",  # Logic error in split()
    "log_unknown_output_type": "Unknown output type: '{0}'.",  # Logic error in split()
    "log_finished_splitting_success": "--- Finished split process for: {0} - SUCCESS ---",  # Split summary
    "log_finished_splitting_errors": "--- Finished split process for: {0} - ERRORS OCCURRED ---",  # Split summary
    "log_value_error_in_splitting": "Input data or calculation error: {0}",  # Error in split()
    "log_finished_splitting_critical_error": "--- Finished split process for: {0} - CRITICAL ERROR ---",  # Split summary
    "log_unexpected_error_in_splitting": "Unexpected error while splitting file {0}: {1}",  # Error in split()

    #   Splitter - Test Mode (__main__)
    "log_script_mode_test": "splitter.py launched as main script (test mode).",
    "log_loaded_config": "Configuration loaded.",  # In test mode
    "log_error_loading_config": "Failed to load configuration: {0}",  # In test mode
    "log_created_example_pdf": "Created sample PDF file: {0}",  # In test mode
    "log_cannot_create_example_pdf": "Failed to create sample PDF: {0}",  # In test mode
    "log_start_test_split": "Starting test split of file: {0} to {1}",  # In test mode
    "log_test_split_success": "Test split completed successfully.",  # In test mode
    "log_test_split_errors": "Test split finished with errors.",  # In test mode

    # --- Logs - QR/Barcode (`barcode_qr.py`) ---
    "log_qr_empty_data": "Attempt to generate QR code for empty data.",
    "log_qr_generated": "QR code SVG generated for: {0}...",
    "log_qr_error": "QR code generation error for data '{0}': {1}",
    "log_barcode_empty_data": "Attempt to generate barcode for empty data.",
    "log_barcode_generated": "Barcode SVG generated for: {0}...",
    "log_barcode_error": "Barcode generation error for data '{0}': {1}",
    "log_basic_handler_configured": "Basic handler configured for logger in barcode_qr.py",  # If it uses its own fallback logger
    "log_basic_handler_error": "Failed to configure basic logger handler in barcode_qr: {0}",  # If it uses its own fallback logger

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
    "logger_profile_saved": "Profile saved: {profile}",  # Log from main.py
    "logger_profile_not_found": "Profile not found to load: {profile}",  # Log from main.py
    "logger_profile_loaded": "Profile loaded: {profile}",  # Log from main.py
    "logger_profile_delete_not_exist": "Attempt to delete non-existent profile: {profile}",  # Log from main.py
    "logger_profile_deleted": "Profile deleted: {profile}",  # Log from main.py
    "logger_start_save_settings": "Started saving settings from GUI.",  # Log from main.py
    "logger_invalid_value": "Invalid value for '{key}'. Set to 0.0.",  # Log from main.py (conversion)
    "logger_end_save_settings": "Finished saving settings from GUI.",  # Log from main.py
    "logger_conversion_error": "Value conversion error from GUI: {error}",  # Log from main.py
    "conversion_failed": "Conversion of GUI values failed",
    "logger_unexpected_save_error": "Unexpected error saving settings: {error}",  # Log from main.py
    "logger_settings_saved": "Settings saved to file: {file}",  # Log from main.py

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
    "error_loading_ui": "Error loading interface: {error}",  # General UI loading error
    "error_creating_home_ui": "Error creating 'Home' tab UI",  # Duplicate?
    "error_creating_settings_ui": "Error creating 'Settings' tab UI",  # Duplicate?
    "error_creating_help_ui": "Error creating 'Help' tab UI",  # Duplicate?
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
    "logger_file_save_error": "File save error {file}: {error}",  # Generic save error log

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
    Billboard Splitter – User Guide\n\n
    Purpose of the program:\n
    Billboard Splitter is used to automatically cut billboard projects into print‑ready panels.
    The program is prepared to work on files designed at 1:10 scale.\n
    Values in the sections: Overlap, White stripe, Settings are entered at 1:1 scale.
    The program allows arranging the cut panels on PDF sheets depending on the selected layout:\n
    • Common sheet: All panels are placed on one document.\n
    • Separate files: Each panel is saved in a separate PDF file.\n\n
    Additionally the program allows:\n
    • Choosing a layout – vertical or horizontal (accordingly: in the vertical layout separation lines appear at the top and bottom,
      and in the horizontal layout on the left and right side).\n
    • Rotating panels by 180° (flipping the whole project).\n
    • Adding registration marks (e.g., crosses or lines) to facilitate precise positioning during gluing.\n
    • Adding QR codes or barcodes – generated based on input data to help
      identify individual panels.\n
    • Saving settings as profiles that can be loaded, modified, and deleted, making it easy to
      switch between different project configurations.\n\n
    Main steps to use the program:\n\n
    1. Choose input file:\n
    • In the 'Home' tab choose a PDF, JPG, or TIFF file containing the billboard design.\n
    • If you do not set your own path, the program sets a sample file by default.\n\n
    2. Cutting settings:\n
    • Specify the number of rows and columns into which the project will be divided.\n
    • Set the overlap size.\n
    • Optionally specify the width of the white stripe that will be added to the effective overlap.\n\n
    3. Select output layout:\n
    • Vertical: All panels will be arranged on a PDF sheet vertically.\n
    • Horizontal: All panels will be arranged on a PDF sheet horizontally.\n\n
    4. Select output type:\n
    • Common sheet: All panels will be arranged on one common PDF sheet.\n
    • Separate files: Each panel will be saved in a separate PDF file.\n
    • In the 'Home' tab you can enable and configure registration marks – choosing between cross and line.\n
    • Optionally enable a QR code or a barcode which will be generated from project data.\n
    • Code parameters (scaling, offset, rotation, position) can be finely tuned in the 'Settings' tab.\n\n
    5. Managing settings:\n
    • In the 'Settings' tab you can precisely modify graphic parameters (margins, line thicknesses, gaps) and
      code settings.\n
    • Save the current settings as a profile so you can easily load or modify them later.\n
    • Settings profiles (saved in the profiles.json file) allow quick switching between different\n
      project configurations.\n\n
    6. Generating PDF:\n
    • After configuring all parameters click 'Generate PDF'.\n
    • Result files will be saved in the 'output' directory or another indicated one, and logs (with daily rotation) in the 'logs'
      directory or another indicated one.\n\n
    If problems occur:\n
    • Check the logs located in the 'logs' folder. Each day generates a separate log file with the date in its name.\n
    • Make sure all required folders are set.\n
    • Technical support: tech@printworks.pl (business days, 8-16)\n
    """    "barcode_font_size_label": "Barcode description font size [pt]:",
}
