# lang_ja.py
# -*- coding: utf-8 -*-
"""
Japanese (Japan) translations — LTR.
"""

LANG = {
    "barcode_font_size_label": "バーコード説明のフォントサイズ[pt]:",
    # ---------------------------
    # Metadata (safe to ignore)
    # ---------------------------
    "__meta__": {
        "language_name_native": "日本語（日本）",
        "language_name_en": "Japanese (Japan)",
        "locale": "ja-JP",
        "direction": "ltr",
        "font_hint": "Noto Sans CJK JP, Noto Serif CJK JP"
    },

    # ==========================
    #  Application - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "エラー",
    "no_file": "ファイルなし",
    "language": "言語",
    "language_switch": "言語を変更",
    "choose_language": "言語を選択：",
    "apply_language": "適用",
    "language_changed": "言語を変更しました。一部の変更はアプリ再起動後に反映されます。",

    # ========================================
    #  User Interface (GUI) Elements
    # ========================================

    # --- Main Tabs ---
    "tab_home": " ホーム ",
    "tab_settings": " 設定 ",
    "tab_help": " ヘルプ ",
    "tab_license": " ライセンス ",

    # --- General Buttons ---
    "button_browse": "参照…",
    "browse_folder": "フォルダーを参照…",
    "button_save": "保存",
    "button_delete": "削除",
    "button_close": "閉じる",
    "save_all_settings": "すべての設定を保存",

    # --- Field Labels (Home Tab) ---
    "label_rows": "縦分割（行）：",
    "label_columns": "横分割（列）：",
    "label_overlap": "オーバーラップ（cm）：",
    "label_white_stripe": "白ストライプ（cm）：",
    "label_add_white_stripe": "有効オーバーラップに白ストライプを含める",
    "label_layout": "レイアウト：",
    "label_output_type": "出力タイプ：",
    "label_enable_reg_marks": "レジストマークを有効化：",
    "label_enable_codes": "コードを有効化：",
    "label_enable_sep_lines": "分離線を有効化（パネル間）",
    "label_enable_start_line": "シート上端／開始線を有効化",
    "label_enable_end_line": "シート下端／終了線を有効化",
    "label_bryt_order": "パネル順序：",
    "label_slice_rotation": "パネル回転：",
    "label_create_order_folder": "注文番号の名前でフォルダーを作成",

    # --- Sections/Frames (Home Tab) ---
    "section_input_file": " 入力ファイル ",
    "section_scale_and_dimensions": " スケールと出力寸法 ",
    "label_original_size": "元のサイズ:",
    "label_scale_non_uniform": "非均一にスケーリング",
    "label_scale": "スケール: 1:",
    "label_scale_x": "スケール X: 1:",
    "label_scale_y": "スケール Y: 1:",
    "label_output_dimensions": "出力ファイルの寸法:",
    "label_width_cm": "幅 [cm]:",
    "label_height_cm": "高さ [cm]:",
    "section_split_settings": " 分割設定 ",
    "section_profiles": " プロファイル ",
    "section_save_location": " 保存場所 ",
    "section_input_preview": " 入力プレビュー ",
    "section_output_preview": " 出力プレビュー ",

    # --- Option Values (Combobox, Radiobutton etc.) ---
    "layout_vertical": "縦",
    "layout_horizontal": "横",
    "output_common_sheet": "共通シート",
    "output_separate_files": "個別ファイル",
    "output_both": "共通シート＋個別ファイル",
    "output_common": "共通シート",
    "output_separate": "個別ファイル",
    "reg_mark_cross": "十字",
    "reg_mark_line": "線",
    "code_qr": "QRコード",
    "code_barcode": "バーコード",
    "bryt_order_1": "A1–An, B1–Bn … 標準（上から）",
    "bryt_order_2": "A1–An, Bn–B1 … ジグザグ（行基準）上から",
    "bryt_order_3": "A1..B1, A2..B2 … 列基準，上から",
    "bryt_order_4": "A1–A2..B2–B1 … ジグザグ（列基準）上から",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … 標準（下から）",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … ジグザグ（行基準）下から",
    "logging_console": "コンソール",
    "logging_file": "ファイル",
    "logging_both": "両方",

    # --- Sections/Frames (Settings Tab) ---
    "section_processing_mode": " カッティング作業 ",
    "processing_mode_ram": "RAM（メモリ）",
    "processing_mode_hdd": "HDD（ディスク）",
    "graphic_settings": "グラフィック設定",
    "code_settings": "QR／バーコード設定",
    "logging_settings": "ログ設定",
    "barcode_text_position_label": "バーコード文字位置：",
    "barcode_text_bottom": "下",
    "barcode_text_side": "横",
    "barcode_text_none": "なし",

    # --- Field Labels (Settings Tab - Graphics) ---
    "extra_margin_label": "パネル外周マージン（cm）：",
    "margin_top_label": "上マージン（cm）：",
    "margin_bottom_label": "下マージン（cm）：",
    "margin_left_label": "左マージン（cm）：",
    "margin_right_label": "右マージン（cm）：",
    "reg_mark_width_label": "レジストマーク — 幅（cm）：",
    "reg_mark_height_label": "レジストマーク — 高さ（cm）：",
    "reg_mark_white_line_width_label": "レジストマーク — 白線の太さ（cm）：",
    "reg_mark_black_line_width_label": "レジストマーク — 黒線の太さ（cm）：",
    "sep_line_black_width_label": "分離線 — 黒線の太さ（cm）：",
    "sep_line_white_width_label": "分離線 — 白線の太さ（cm）：",
    "slice_gap_label": "パネル間ギャップ（cm）：",
    "label_draw_slice_border": "パネル枠（カットライン）を描画",

    # --- Field Labels (Settings Tab - Codes) ---
    "scale_label": "スケール（cm）：",
    "scale_x_label": "幅 X（cm）：",
    "scale_y_label": "高さ Y（cm）：",
    "offset_x_label": "オフセット X（cm）：",
    "offset_y_label": "オフセット Y（cm）：",
    "rotation_label": "回転（°）：",
    "anchor_label": "アンカー：",

    # --- Field Labels (Settings Tab - Logging) ---
    "logging_mode_label": "ログモード：",
    "log_file_label": "ログファイル：",
    "logging_level_label": "ログレベル：",

    # --- Buttons / Actions (Home Tab) ---
    "button_load": "読込",
    "button_save_settings": "現在の設定を保存",
    "button_generate_pdf": "PDFを生成",
    "button_refresh_preview": "プレビューを更新",
    "button_refresh_layout": "レイアウトを更新",

    # --- License (GUI) ---
    "hwid_frame_title": "ハードウェアID（HWID）",
    "copy_hwid": "HWIDをコピー",
    "license_frame_title": "ライセンス有効化",
    "enter_license_key": "ライセンスキーを入力：",
    "activate": "有効化",
    "status_trial": "トライアルモード",
    "license_active": "ライセンスは有効です",

    # ================================================
    #  User Messages (Windows, Status Bar)
    # ================================================

    # --- Profiles ---
    "msg_no_profile_name": "名称なし",
    "msg_enter_profile_name": "保存するプロファイル名を入力してください。",
    "msg_profile_saved": "プロファイルを保存しました",
    "profile_saved_title": "プロファイル保存",
    "msg_profile_saved_detail": "プロファイル「{0}」を保存しました。",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "プロフィール「{profile}」が保存され、適用されました。",
    "msg_no_profile": "プロファイルがありません",
    "warning_no_profile": "プロファイルがありません",
    "msg_select_profile": "読み込むプロファイルを一覧から選択してください。",
    "select_profile": "読み込むプロファイルを一覧から選択してください。",
    "profile_loaded_title": "プロファイル読込",
    "profile_loaded": "プロファイル「{profile}」を読み込みました。",
    "warning_no_profile_delete": "プロファイルがありません",
    "warning_no_profile_delete_message": "削除するプロファイルを一覧から選択してください。",
    "profile_not_found": "プロファイル「{profile}」が見つかりません。",
    "profile_not_exist": "プロファイル「{profile}」は存在しません。",
    "confirm_delete_title": "削除確認",
    "confirm_delete_profile": "プロファイル「{profile}」を削除してもよろしいですか？",
    "profile_deleted_title": "プロファイル削除",
    "profile_deleted": "プロファイル「{profile}」を削除しました。",

    # --- Files / Directories ---
    "msg_no_input_file": "入力ファイルがありません",
    "msg_unsupported_format": "未対応の形式です",
    "select_file_title": "入力ファイルを選択",
    "supported_files": "対応ファイル",
    "all_files": "すべてのファイル",
    "select_dir_title": "出力フォルダーを選択",
    "select_log_dir_title": "ログフォルダーを選択",
    "error_output_dir_title": "出力フォルダーのエラー",
    "error_output_dir": "選択した出力フォルダーが不正または存在しません：\n{directory}",
    "error_input_file_title": "入力ファイルのエラー",
    "error_input_file": "選択した入力ファイルが不正または存在しません：\n{file}",
    "save_file_error_title": "ファイル保存エラー",
    "save_file_error": "ファイルを保存できません：{error}",

    # --- PDF Processing / Preview ---
    "msg_pdf_processing_error": "PDFの処理に失敗しました",
    "msg_thumbnail_error": "サムネイル読込エラー",
    "msg_no_pdf_output": "生成されたPDF出力がありません",
    "no_pdf_pages": "PDFにページがありません",
    "unsupported_output": "この出力タイプはプレビューに対応していません",
    "pdf_generated_title": "生成完了",
    "pdf_generated": "PDFファイルは次のフォルダーに正常に生成されました：\n{directory}",
    "pdf_generation_error_title": "生成エラー",
    "pdf_generation_error": "PDF生成中にエラーが発生しました。詳細はログを参照してください。",
    "critical_pdf_error_title": "致命的なPDF生成エラー",
    "critical_pdf_error": "PDF生成中に致命的なエラーが発生しました：\n{error}\nログをご確認ください。",

    # --- Settings ---
    "settings_saved_title": "設定を保存しました",
    "settings_saved": "設定は次のファイルに保存されました：\n{filepath}",
    "settings_save_error_title": "設定保存エラー",
    "settings_save_error": "設定を保存できません：{error}",
    "conversion_error_title": "変換エラー",
    "conversion_error": "GUI値の変換中にエラー：{error}",
    "update_gui_error_title": "インターフェース更新エラー",
    "update_gui_error": "インターフェース更新中にエラーが発生しました：{error}",

    # --- License ---
    "hwid_copied_to_clipboard": "HWIDをクリップボードにコピーしました",
    "computer_hwid": "コンピューター HWID",
    "public_key_load_error": "公開鍵の読込エラー：{error}",
    "invalid_license_format": "ライセンスキーの形式が不正です：{error}",
    "activation_success": "ライセンスを正常に有効化しました。",
    "activation_error": "ライセンス有効化エラー：{error}",
    "log_trial_mode_active": "トライアルモードが有効です",
    "log_trial_mode_inactive": "トライアルモードは無効です",

    # --- Initialization ---
    "init_error_title": "初期化エラー",
    "init_error": "ディレクトリ作成中のエラー：{error}",
    "poppler_path_info": "Poppler パス情報",
    "ttkthemes_not_installed": "警告：'ttkthemes' が未インストールです。デフォルトの Tkinter スタイルを使用します。",

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
ビルボードスプリッター — ユーザーガイド

目的:
ビルボードスプリッターは、ビルボード用デザインを自動的に印刷用パネルへ分割します。
本プログラムは 1:10 スケールのデザインを前提としています。オーバーラップや白ストライプ等の値は 1:1 を基準に入力してください。

出力タイプ:
• 共通シート：すべてのパネルを1つのPDFにまとめます。
• 個別ファイル：各パネルを個別のPDFとして保存します。

追加機能:
• 縦／横レイアウト。
• パネルを180°回転。
• レジストマーク（十字／線）。
• QR／バーコードの追加（スケール／オフセット／位置を調整可能）。
• 設定をプロファイルとして保存・読み込み・削除。

基本手順:
1) 「ホーム」で PDF/JPG/TIFF を選択。
2) 行・列、オーバーラップ、白ストライプを設定。
3) レイアウト（縦／横）と出力（共通／個別）を選択。
4) マーク／コードを有効化し、「設定」で詳細を調整。
5) 必要ならプロファイルを保存し、「PDFを生成」をクリック。

トラブルシューティング:
• 「logs」フォルダーのログを確認。
• フォルダー／パスが正しいか確認。
• 技術サポート：tech@printworks.pl（平日 8–16）
"""
}
