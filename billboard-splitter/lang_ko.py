# lang_ko.py
# -*- coding: utf-8 -*-
"""
Korean (Korea) translations — LTR.
"""

LANG = {
    "barcode_font_size_label": "바코드 설명 글꼴 크기 [pt]:",
    # ---------------------------
    # Metadata (safe to ignore)
    # ---------------------------
    "__meta__": {
        "language_name_native": "한국어 (대한민국)",
        "language_name_en": "Korean (Korea)",
        "locale": "ko-KR",
        "direction": "ltr",              # left-to-right
        "font_hint": "Noto Sans CJK KR, Noto Serif CJK KR"
    },

    # ==========================
    #  Application - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "오류",
    "no_file": "파일 없음",
    "language": "언어",
    "language_switch": "언어 변경",
    "choose_language": "언어 선택:",
    "apply_language": "적용",
    "language_changed": "언어가 변경되었습니다. 일부 변경 사항은 앱을 다시 시작한 후 적용됩니다.",

    # ========================================
    #  User Interface (GUI) Elements
    # ========================================

    # --- Main Tabs ---
    "tab_home": " 홈 ",
    "tab_settings": " 설정 ",
    "tab_help": " 도움말 ",
    "tab_license": " 라이선스 ",

    # --- General Buttons ---
    "button_browse": "찾아보기…",
    "browse_folder": "폴더 선택…",
    "button_save": "저장",
    "button_delete": "삭제",
    "button_close": "닫기",
    "save_all_settings": "모든 설정 저장",

    # --- Field Labels (Home Tab) ---
    "label_rows": "세로 분할(행):",
    "label_columns": "가로 분할(열):",
    "label_overlap": "오버랩[mm]:",
    "label_white_stripe": "화이트 스트라이프[mm]:",
    "label_add_white_stripe": "유효 오버랩에 화이트 스트라이프 포함",
    "label_layout": "레이아웃:",
    "label_output_type": "출력 유형:",
    "label_enable_reg_marks": "레지스트 마크 사용:",
    "label_enable_codes": "코드 사용:",
    "label_enable_sep_lines": "분리선 사용(패널 사이)",
    "label_enable_start_line": "시트 상단/시작선 사용",
    "label_enable_end_line": "시트 하단/끝선 사용",
    "label_bryt_order": "패널 순서:",
    "label_slice_rotation": "패널 회전:",
    "label_create_order_folder": "주문번호 이름으로 폴더 생성",

    # --- Sections/Frames (Home Tab) ---
    "section_input_file": " 입력 파일 ",
    "section_scale_and_dimensions": " 스케일 및 출력 치수 ",
    "label_original_size": "원본 크기:",
    "label_scale_non_uniform": "비례적이지 않게 스케일링",
    "label_scale": "스케일: 1:",
    "label_scale_x": "스케일 X: 1:",
    "label_scale_y": "스케일 Y: 1:",
    "label_output_dimensions": "출력 파일 치수:",
    "label_width_cm": "너비 [cm]:",
    "label_height_cm": "높이 [cm]:",
    "section_split_settings": " 분할 설정 ",
    "section_profiles": " 프로필 ",
    "section_save_location": " 저장 위치 ",
    "section_input_preview": " 입력 미리보기 ",
    "section_output_preview": " 출력 미리보기 ",

    # --- Option Values (Combobox, Radiobutton etc.) ---
    "layout_vertical": "세로",
    "layout_horizontal": "가로",
    "output_common_sheet": "공통 시트",
    "output_separate_files": "개별 파일",
    "output_both": "공통 시트 + 개별 파일",
    "output_common": "공통 시트",
    "output_separate": "개별 파일",
    "reg_mark_cross": "십자",
    "reg_mark_line": "선",
    "code_qr": "QR 코드",
    "code_barcode": "바코드",
    "bryt_order_1": "A1–An, B1–Bn … 표준(상단부터)",
    "bryt_order_2": "A1–An, Bn–B1 … 지그재그(행 기준), 상단부터",
    "bryt_order_3": "A1..B1, A2..B2 … 열 기준, 상단부터",
    "bryt_order_4": "A1–A2..B2–B1 … 지그재그(열 기준), 상단부터",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … 표준(하단부터)",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … 지그재그(행 기준), 하단부터",
    "logging_console": "콘솔",
    "logging_file": "파일",
    "logging_both": "둘 다",

    # --- Sections/Frames (Settings Tab) ---
    "section_processing_mode": " 커팅 작업 ",
    "processing_mode_ram": "RAM(메모리)",
    "processing_mode_hdd": "HDD(디스크)",
    "graphic_settings": "그래픽 설정",
    "code_settings": "QR/바코드 설정",
    "logging_settings": "로깅 설정",
    "barcode_text_position_label": "바코드 텍스트 위치:",
    "barcode_text_bottom": "아래",
    "barcode_text_side": "옆",
    "barcode_text_none": "없음",

    # --- Field Labels (Settings Tab - Graphics) ---
    "extra_margin_label": "패널 외곽 여백[mm]:",
    "margin_top_label": "상단 여백[mm]:",
    "margin_bottom_label": "하단 여백[mm]:",
    "margin_left_label": "왼쪽 여백[mm]:",
    "margin_right_label": "오른쪽 여백[mm]:",
    "reg_mark_width_label": "레지스트 마크 — 폭[mm]:",
    "reg_mark_height_label": "레지스트 마크 — 높이[mm]:",
    "reg_mark_white_line_width_label": "레지스트 마크 — 흰 선 두께[mm]:",
    "reg_mark_black_line_width_label": "레지스트 마크 — 검은 선 두께[mm]:",
    "sep_line_black_width_label": "분리선 — 검은 선 두께[mm]:",
    "sep_line_white_width_label": "분리선 — 흰 선 두께[mm]:",
    "slice_gap_label": "패널 간 간격[mm]:",
    "label_draw_slice_border": "패널 테두리(컷 라인) 그리기",

    # --- Field Labels (Settings Tab - Codes) ---
    "scale_label": "스케일[mm]:",
    "scale_x_label": "가로 X[mm]:",
    "scale_y_label": "세로 Y[mm]:",
    "offset_x_label": "오프셋 X[mm]:",
    "offset_y_label": "오프셋 Y[mm]:",
    "rotation_label": "회전(°):",
    "anchor_label": "앵커:",

    # --- Field Labels (Settings Tab - Logging) ---
    "logging_mode_label": "로깅 모드:",
    "log_file_label": "로그 파일:",
    "logging_level_label": "로깅 레벨:",

    # --- Buttons / Actions (Home Tab) ---
    "button_load": "불러오기",
    "button_save_settings": "현재 설정 저장",
    "button_generate_pdf": "PDF 생성",
    "button_refresh_preview": "미리보기 새로고침",
    "button_refresh_layout": "레이아웃 새로고침",

    # --- License (GUI) ---
    "hwid_frame_title": "하드웨어 ID(HWID)",
    "copy_hwid": "HWID 복사",
    "license_frame_title": "라이선스 활성화",
    "enter_license_key": "라이선스 키 입력:",
    "activate": "활성화",
    "status_trial": "체험 모드",
    "license_active": "라이선스 활성 상태",

    # ================================================
    #  User Messages (Windows, Status Bar)
    # ================================================

    # --- Profiles ---
    "msg_no_profile_name": "이름 없음",
    "msg_enter_profile_name": "저장할 프로필 이름을 입력하세요.",
    "msg_profile_saved": "프로필이 저장되었습니다",
    "profile_saved_title": "프로필 저장",
    "msg_profile_saved_detail": "프로필 '{0}' 이(가) 저장되었습니다.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "프로필 '{profile}'이(가) 저장되고 적용되었습니다.",
    "msg_no_profile": "프로필 없음",
    "warning_no_profile": "프로필 없음",
    "msg_select_profile": "로드할 프로필을 목록에서 선택하세요.",
    "select_profile": "로드할 프로필을 목록에서 선택하세요.",
    "profile_loaded_title": "프로필 로드",
    "profile_loaded": "프로필 '{profile}' 이(가) 로드되었습니다.",
    "warning_no_profile_delete": "프로필 없음",
    "warning_no_profile_delete_message": "삭제할 프로필을 목록에서 선택하세요.",
    "profile_not_found": "프로필 '{profile}' 을(를) 찾을 수 없습니다.",
    "profile_not_exist": "프로필 '{profile}' 이(가) 존재하지 않습니다.",
    "confirm_delete_title": "삭제 확인",
    "confirm_delete_profile": "정말로 프로필 '{profile}' 을(를) 삭제하시겠습니까?",
    "profile_deleted_title": "프로필 삭제됨",
    "profile_deleted": "프로필 '{profile}' 이(가) 삭제되었습니다.",

    # --- Files / Directories ---
    "msg_no_input_file": "입력 파일이 없습니다",
    "msg_unsupported_format": "지원되지 않는 형식",
    "select_file_title": "입력 파일 선택",
    "supported_files": "지원 파일",
    "all_files": "모든 파일",
    "select_dir_title": "출력 폴더 선택",
    "select_log_dir_title": "로그 폴더 선택",
    "error_output_dir_title": "출력 폴더 오류",
    "error_output_dir": "선택한 출력 폴더가 올바르지 않거나 존재하지 않습니다:\n{directory}",
    "error_input_file_title": "입력 파일 오류",
    "error_input_file": "선택한 입력 파일이 올바르지 않거나 존재하지 않습니다:\n{file}",
    "save_file_error_title": "파일 저장 오류",
    "save_file_error": "파일을 저장할 수 없습니다: {error}",

    # --- PDF Processing / Preview ---
    "msg_pdf_processing_error": "PDF 파일 처리 실패",
    "msg_thumbnail_error": "썸네일 로드 오류",
    "msg_no_pdf_output": "생성된 PDF 출력이 없습니다",
    "no_pdf_pages": "PDF 파일에 페이지가 없습니다",
    "unsupported_output": "이 출력 유형은 미리보기를 지원하지 않습니다",
    "pdf_generated_title": "생성 완료",
    "pdf_generated": "PDF 파일이 다음 폴더에 성공적으로 생성되었습니다:\n{directory}",
    "pdf_generation_error_title": "생성 오류",
    "pdf_generation_error": "PDF 생성 중 오류가 발생했습니다. 자세한 내용은 로그를 확인하세요.",
    "critical_pdf_error_title": "치명적 PDF 생성 오류",
    "critical_pdf_error": "PDF 생성 중 치명적인 오류가 발생했습니다:\n{error}\n로그를 확인하세요.",

    # --- Settings ---
    "settings_saved_title": "설정 저장됨",
    "settings_saved": "설정이 다음 파일에 저장되었습니다:\n{filepath}",
    "settings_save_error_title": "설정 저장 오류",
    "settings_save_error": "설정을 저장할 수 없습니다: {error}",
    "conversion_error_title": "변환 오류",
    "conversion_error": "GUI 값 변환 중 오류: {error}",
    "update_gui_error_title": "인터페이스 업데이트 오류",
    "update_gui_error": "인터페이스 업데이트 중 오류가 발생했습니다: {error}",

    # --- License ---
    "hwid_copied_to_clipboard": "HWID가 클립보드에 복사되었습니다",
    "computer_hwid": "컴퓨터 HWID",
    "public_key_load_error": "공개 키 로드 오류: {error}",
    "invalid_license_format": "라이선스 키 형식이 잘못되었습니다: {error}",
    "activation_success": "라이선스가 성공적으로 활성화되었습니다.",
    "activation_error": "라이선스 활성화 오류: {error}",
    "log_trial_mode_active": "체험 모드가 활성화되어 있습니다",
    "log_trial_mode_inactive": "체험 모드가 비활성화되어 있습니다",

    # --- Initialization ---
    "init_error_title": "초기화 오류",
    "init_error": "디렉터리 생성 중 오류: {error}",
    "poppler_path_info": "Poppler 경로 정보",
    "ttkthemes_not_installed": "경고: 'ttkthemes'가 설치되어 있지 않습니다. 기본 Tkinter 스타일이 사용됩니다.",

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
빌보드 스플리터 — 사용자 안내

목적:
빌보드 스플리터는 빌보드 디자인을 자동으로 인쇄용 패널로 분할합니다.
프로그램은 1:10 스케일 도안을 가정합니다. 오버랩·화이트 스트라이프 등의 값은 1:1 기준으로 입력하세요.

출력 유형:
• 공통 시트: 모든 패널이 하나의 PDF에 저장됩니다.
• 개별 파일: 각 패널이 별도의 PDF로 저장됩니다.

추가 기능:
• 세로/가로 레이아웃.
• 패널 180° 회전.
• 레지스트 마크(십자/선).
• QR/바코드 추가(스케일/오프셋/위치 조절 가능).
• 설정을 프로필로 저장/로드/삭제.

기본 절차:
1) '홈'에서 PDF/JPG/TIFF 파일을 선택합니다.
2) 행/열, 오버랩, 화이트 스트라이프를 설정합니다.
3) 레이아웃(세로/가로)과 출력(공통/개별)을 선택합니다.
4) 마크/코드를 사용하도록 설정하고 '설정'에서 세부값을 조정합니다.
5) (선택) 프로필을 저장한 뒤 'PDF 생성'을 클릭합니다.

문제 해결:
• 'logs' 폴더의 로그를 확인하세요.
• 폴더/경로가 올바른지 점검하세요.
• 기술 지원: tech@printworks.pl (영업일 8–16)
"""
}
