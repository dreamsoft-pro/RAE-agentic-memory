# lang_vi.py
# -*- coding: utf-8 -*-
"""
Vietnamese (Vietnam) translations — LTR.
"""

LANG = {
    "barcode_font_size_label": "Cỡ chữ mô tả mã vạch [pt]:",
    # ---------------------------
    # Metadata (safe to ignore)
    # ---------------------------
    "__meta__": {
        "language_name_native": "Tiếng Việt (Việt Nam)",
        "language_name_en": "Vietnamese (Vietnam)",
        "locale": "vi-VN",
        "direction": "ltr",              # left-to-right
        "font_hint": "Noto Sans, Noto Serif"
    },

    # ==========================
    #  Application - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Lỗi",
    "no_file": "Không có tệp",
    "language": "Ngôn ngữ",
    "language_switch": "Đổi ngôn ngữ",
    "choose_language": "Chọn ngôn ngữ:",
    "apply_language": "Áp dụng",
    "language_changed": "Đã đổi ngôn ngữ. Một số thay đổi sẽ hiển thị sau khi khởi động lại ứng dụng.",

    # ========================================
    #  User Interface (GUI) Elements
    # ========================================

    # --- Main Tabs ---
    "tab_home": " Trang chủ ",
    "tab_settings": " Cài đặt ",
    "tab_help": " Trợ giúp ",
    "tab_license": " Giấy phép ",

    # --- General Buttons ---
    "button_browse": "Duyệt…",
    "browse_folder": "Chọn thư mục…",
    "button_save": "Lưu",
    "button_delete": "Xoá",
    "button_close": "Đóng",
    "save_all_settings": "Lưu tất cả cài đặt",

    # --- Field Labels (Home Tab) ---
    "label_rows": "Chia dọc (hàng):",
    "label_columns": "Chia ngang (cột):",
    "label_overlap": "Chồng mép [mm]:",
    "label_white_stripe": "Dải trắng [mm]:",
    "label_add_white_stripe": "Tính dải trắng vào chồng mép hiệu dụng",
    "label_layout": "Bố cục:",
    "label_output_type": "Kiểu xuất:",
    "label_enable_reg_marks": "Bật dấu đăng ký:",
    "label_enable_codes": "Bật mã:",
    "label_enable_sep_lines": "Bật đường phân tách (giữa các panel)",
    "label_enable_start_line": "Bật đường đầu trang / bắt đầu",
    "label_enable_end_line": "Bật đường cuối trang / kết thúc",
    "label_bryt_order": "Thứ tự panel:",
    "label_slice_rotation": "Xoay panel:",
    "label_create_order_folder": "Tạo thư mục theo số đơn hàng",

    # --- Sections/Frames (Home Tab) ---
    "section_input_file": " Tệp đầu vào ",
    "section_scale_and_dimensions": " Tỷ lệ và kích thước đầu ra ",
    "label_original_size": "Kích thước gốc:",
    "label_scale_non_uniform": "Tỷ lệ không đồng đều",
    "label_scale": "Tỷ lệ: 1:",
    "label_scale_x": "Tỷ lệ X: 1:",
    "label_scale_y": "Tỷ lệ Y: 1:",
    "label_output_dimensions": "Kích thước tệp đầu ra:",
    "label_width_cm": "Chiều rộng [cm]:",
    "label_height_cm": "Chiều cao [cm]:",
    "section_split_settings": " Cài đặt chia ",
    "section_profiles": " Hồ sơ ",
    "section_save_location": " Nơi lưu ",
    "section_input_preview": " Xem trước đầu vào ",
    "section_output_preview": " Xem trước đầu ra ",

    # --- Option Values (Combobox, Radiobutton etc.) ---
    "layout_vertical": "Dọc",
    "layout_horizontal": "Ngang",
    "output_common_sheet": "Tờ chung",
    "output_separate_files": "Tệp riêng",
    "output_both": "Tờ chung & Tệp riêng",
    "output_common": "Tờ chung",
    "output_separate": "Tệp riêng",
    "reg_mark_cross": "Dấu cộng",
    "reg_mark_line": "Đường thẳng",
    "code_qr": "Mã QR",
    "code_barcode": "Mã vạch",
    "bryt_order_1": "A1–An, B1–Bn … Chuẩn, từ trên xuống",
    "bryt_order_2": "A1–An, Bn–B1 … Răng lược (theo hàng), từ trên xuống",
    "bryt_order_3": "A1..B1, A2..B2 … Theo cột, từ trên xuống",
    "bryt_order_4": "A1–A2..B2–B1 … Răng lược (theo cột), từ trên xuống",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … Chuẩn, từ dưới lên",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … Răng lược (hàng), từ dưới lên",
    "logging_console": "Bảng điều khiển",
    "logging_file": "Tệp",
    "logging_both": "Cả hai",

    # --- Sections/Frames (Settings Tab) ---
    "section_processing_mode": " Tác vụ cắt ",
    "processing_mode_ram": "RAM (bộ nhớ)",
    "processing_mode_hdd": "HDD (đĩa)",
    "graphic_settings": "Cài đặt đồ hoạ",
    "code_settings": "Cài đặt QR / mã vạch",
    "logging_settings": "Cài đặt ghi log",
    "barcode_text_position_label": "Vị trí chữ dưới mã vạch:",
    "barcode_text_bottom": "Bên dưới",
    "barcode_text_side": "Bên cạnh",
    "barcode_text_none": "Không có",

    # --- Field Labels (Settings Tab - Graphics) ---
    "extra_margin_label": "Lề quanh panel [mm]:",
    "margin_top_label": "Lề trên [mm]:",
    "margin_bottom_label": "Lề dưới [mm]:",
    "margin_left_label": "Lề trái [mm]:",
    "margin_right_label": "Lề phải [mm]:",
    "reg_mark_width_label": "Dấu đăng ký — Rộng [mm]:",
    "reg_mark_height_label": "Dấu đăng ký — Cao [mm]:",
    "reg_mark_white_line_width_label": "Dấu đăng ký — Dày đường trắng [mm]:",
    "reg_mark_black_line_width_label": "Dấu đăng ký — Dày đường đen [mm]:",
    "sep_line_black_width_label": "Đường phân tách — Dày đường đen [mm]:",
    "sep_line_white_width_label": "Đường phân tách — Dày đường trắng [mm]:",
    "slice_gap_label": "Khoảng cách giữa panel [mm]:",
    "label_draw_slice_border": "Vẽ viền panel (đường cắt)",

    # --- Field Labels (Settings Tab - Codes) ---
    "scale_label": "Tỷ lệ [mm]:",
    "scale_x_label": "Rộng X [mm]:",
    "scale_y_label": "Cao Y [mm]:",
    "offset_x_label": "Dịch X [mm]:",
    "offset_y_label": "Dịch Y [mm]:",
    "rotation_label": "Xoay (°):",
    "anchor_label": "Neo:",

    # --- Field Labels (Settings Tab - Logging) ---
    "logging_mode_label": "Chế độ log:",
    "log_file_label": "Tệp log:",
    "logging_level_label": "Mức log:",

    # --- Buttons / Actions (Home Tab) ---
    "button_load": "Tải",
    "button_save_settings": "Lưu cài đặt hiện tại",
    "button_generate_pdf": "Tạo PDF",
    "button_refresh_preview": "Làm mới xem trước",
    "button_refresh_layout": "Làm mới bố cục",

    # --- License (GUI) ---
    "hwid_frame_title": "Mã phần cứng (HWID)",
    "copy_hwid": "Sao chép HWID",
    "license_frame_title": "Kích hoạt giấy phép",
    "enter_license_key": "Nhập khoá giấy phép:",
    "activate": "Kích hoạt",
    "status_trial": "Chế độ dùng thử",
    "license_active": "Giấy phép đang hoạt động",

    # ================================================
    #  User Messages (Windows, Status Bar)
    # ================================================

    # --- Profiles ---
    "msg_no_profile_name": "Không tên",
    "msg_enter_profile_name": "Nhập tên hồ sơ để lưu.",
    "msg_profile_saved": "Đã lưu hồ sơ",
    "profile_saved_title": "Đã lưu hồ sơ",
    "msg_profile_saved_detail": "Đã lưu hồ sơ '{0}'.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Hồ sơ '{profile}' đã được lưu và áp dụng.",
    "msg_no_profile": "Không có hồ sơ",
    "warning_no_profile": "Không có hồ sơ",
    "msg_select_profile": "Chọn hồ sơ trong danh sách để tải.",
    "select_profile": "Chọn hồ sơ trong danh sách để tải.",
    "profile_loaded_title": "Đã tải hồ sơ",
    "profile_loaded": "Đã tải hồ sơ '{profile}'.",
    "warning_no_profile_delete": "Không có hồ sơ",
    "warning_no_profile_delete_message": "Chọn hồ sơ trong danh sách để xoá.",
    "profile_not_found": "Không tìm thấy hồ sơ '{profile}'.",
    "profile_not_exist": "Hồ sơ '{profile}' không tồn tại.",
    "confirm_delete_title": "Xác nhận xoá",
    "confirm_delete_profile": "Bạn có chắc muốn xoá hồ sơ '{profile}'?",
    "profile_deleted_title": "Đã xoá hồ sơ",
    "profile_deleted": "Đã xoá hồ sơ '{profile}'.",

    # --- Files / Directories ---
    "msg_no_input_file": "Không có tệp đầu vào",
    "msg_unsupported_format": "Định dạng không được hỗ trợ",
    "select_file_title": "Chọn tệp đầu vào",
    "supported_files": "Tệp được hỗ trợ",
    "all_files": "Tất cả tệp",
    "select_dir_title": "Chọn thư mục đầu ra",
    "select_log_dir_title": "Chọn thư mục log",
    "error_output_dir_title": "Lỗi thư mục đầu ra",
    "error_output_dir": "Thư mục đầu ra được chọn sai hoặc không tồn tại:\n{directory}",
    "error_input_file_title": "Lỗi tệp đầu vào",
    "error_input_file": "Tệp đầu vào được chọn sai hoặc không tồn tại:\n{file}",
    "save_file_error_title": "Lỗi lưu tệp",
    "save_file_error": "Không thể lưu tệp: {error}",

    # --- PDF Processing / Preview ---
    "msg_pdf_processing_error": "Xử lý tệp PDF thất bại",
    "msg_thumbnail_error": "Lỗi tải ảnh thu nhỏ",
    "msg_no_pdf_output": "Chưa có đầu ra PDF",
    "no_pdf_pages": "Tệp PDF không có trang",
    "unsupported_output": "Kiểu đầu ra này không hỗ trợ xem trước",
    "pdf_generated_title": "Hoàn tất tạo",
    "pdf_generated": "Đã tạo thành công tệp PDF tại:\n{directory}",
    "pdf_generation_error_title": "Lỗi tạo",
    "pdf_generation_error": "Có lỗi khi tạo PDF. Xem log để biết chi tiết.",
    "critical_pdf_error_title": "Lỗi nghiêm trọng khi tạo PDF",
    "critical_pdf_error": "Gặp lỗi nghiêm trọng khi tạo PDF:\n{error}\nVui lòng kiểm tra log.",

    # --- Settings ---
    "settings_saved_title": "Đã lưu cài đặt",
    "settings_saved": "Đã lưu cài đặt vào tệp:\n{filepath}",
    "settings_save_error_title": "Lỗi lưu cài đặt",
    "settings_save_error": "Không thể lưu cài đặt: {error}",
    "conversion_error_title": "Lỗi chuyển đổi",
    "conversion_error": "Lỗi khi chuyển đổi giá trị từ GUI: {error}",
    "update_gui_error_title": "Lỗi cập nhật giao diện",
    "update_gui_error": "Gặp lỗi khi cập nhật giao diện: {error}",

    # --- License ---
    "hwid_copied_to_clipboard": "Đã sao chép HWID vào bộ nhớ tạm",
    "computer_hwid": "HWID máy tính",
    "public_key_load_error": "Lỗi nạp khoá công khai: {error}",
    "invalid_license_format": "Định dạng khoá giấy phép không hợp lệ: {error}",
    "activation_success": "Kích hoạt giấy phép thành công.",
    "activation_error": "Lỗi kích hoạt giấy phép: {error}",
    "log_trial_mode_active": "Chế độ dùng thử đang bật",
    "log_trial_mode_inactive": "Chế độ dùng thử đang tắt",

    # --- Initialization ---
    "init_error_title": "Lỗi khởi tạo",
    "init_error": "Lỗi tạo thư mục: {error}",
    "poppler_path_info": "Thông tin đường dẫn Poppler",
    "ttkthemes_not_installed": "Cảnh báo: 'ttkthemes' chưa được cài. Sẽ dùng kiểu mặc định của Tkinter.",

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
Billboard Splitter — Hướng dẫn sử dụng

Mục đích:
Billboard Splitter tự động chia thiết kế billboard thành các panel sẵn sàng in.
Chương trình giả định thiết kế theo tỉ lệ 1:10. Nhập các giá trị chồng mép, dải trắng… theo tỉ lệ 1:1.

Kiểu đầu ra:
• Tờ chung: tất cả panel trong một PDF.
• Tệp riêng: mỗi panel là một tệp PDF riêng.

Khả năng bổ sung:
• Bố cục dọc/ngang.
• Xoay panel 180°.
• Dấu đăng ký (dấu cộng/đường thẳng).
• Thêm QR/mã vạch (điều chỉnh tỉ lệ/vị trí/dịch).
• Lưu, tải, xoá cài đặt dưới dạng hồ sơ (profile).

Các bước cơ bản:
1) Ở 'Trang chủ' chọn tệp PDF/JPG/TIFF.
2) Đặt số hàng/cột, chồng mép và dải trắng.
3) Chọn bố cục (dọc/ngang) và kiểu xuất (tờ chung/ tệp riêng).
4) Bật dấu/mã và tinh chỉnh trong 'Cài đặt'.
5) (Tuỳ chọn) lưu hồ sơ và bấm 'Tạo PDF'.

Xử lý sự cố:
• Kiểm tra log trong thư mục 'logs'.
• Đảm bảo đường dẫn/thư mục hợp lệ.
• Hỗ trợ kỹ thuật: tech@printworks.pl (ngày làm việc 8–16)
"""
}
