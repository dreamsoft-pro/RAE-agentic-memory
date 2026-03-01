# lang_id.py
# -*- coding: utf-8 -*-
"""
Indonesian (Indonesia) translations — LTR.
"""

LANG = {
    "barcode_font_size_label": "Ukuran font deskripsi barcode [pt]:",
    "__meta__": {
        "language_name_native": "Bahasa Indonesia",
        "language_name_en": "Indonesian (Indonesia)",
        "locale": "id-ID",
        "direction": "ltr",
        "font_hint": "Noto Sans, Noto Serif"
    },

    # General
    "app_title": "Billboard Splitter v1.8",
    "error": "Kesalahan",
    "no_file": "Tidak ada berkas",
    "language": "Bahasa",
    "language_switch": "Ganti bahasa",
    "choose_language": "Pilih bahasa:",
    "apply_language": "Terapkan",
    "language_changed": "Bahasa telah diubah. Beberapa perubahan akan muncul setelah aplikasi dimulai ulang.",

    # Tabs
    "tab_home": " Beranda ",
    "tab_settings": " Pengaturan ",
    "tab_help": " Bantuan ",
    "tab_license": " Lisensi ",

    # Buttons
    "button_browse": "Jelajahi…",
    "browse_folder": "Pilih folder…",
    "button_save": "Simpan",
    "button_delete": "Hapus",
    "button_close": "Tutup",
    "save_all_settings": "Simpan semua pengaturan",

    # Home labels
    "label_rows": "Pembagian vertikal (baris):",
    "label_columns": "Pembagian horizontal (kolom):",
    "label_overlap": "Overlap [mm]:",
    "label_white_stripe": "Garis putih [mm]:",
    "label_add_white_stripe": "Masukkan garis putih ke overlap efektif",
    "label_layout": "Tata letak:",
    "label_output_type": "Jenis keluaran:",
    "label_enable_reg_marks": "Aktifkan tanda registrasi:",
    "label_enable_codes": "Aktifkan kode:",
    "label_enable_sep_lines": "Aktifkan garis pemisah (antar panel)",
    "label_enable_start_line": "Aktifkan garis atas/mulai lembar",
    "label_enable_end_line": "Aktifkan garis bawah/akhir lembar",
    "label_bryt_order": "Urutan panel:",
    "label_slice_rotation": "Rotasi panel:",
    "label_create_order_folder": "Buat folder dengan nomor pesanan",

    # Sections
    "section_input_file": " Berkas masukan ",
    "section_scale_and_dimensions": " Skala dan dimensi output ",
    "label_original_size": "Ukuran asli:",
    "label_scale_non_uniform": "Skala tidak seragam",
    "label_scale": "Skala: 1:",
    "label_scale_x": "Skala X: 1:",
    "label_scale_y": "Skala Y: 1:",
    "label_output_dimensions": "Dimensi file output:",
    "label_width_cm": "Lebar [cm]:",
    "label_height_cm": "Tinggi [cm]:",
    "section_split_settings": " Pengaturan pembagian ",
    "section_profiles": " Profil ",
    "section_save_location": " Lokasi simpan ",
    "section_input_preview": " Pratinjau masukan ",
    "section_output_preview": " Pratinjau keluaran ",

    # Options
    "layout_vertical": "Vertikal",
    "layout_horizontal": "Horizontal",
    "output_common_sheet": "Lembar gabungan",
    "output_separate_files": "Berkas terpisah",
    "output_both": "Lembar gabungan & Berkas terpisah",
    "output_common": "Lembar gabungan",
    "output_separate": "Berkas terpisah",
    "reg_mark_cross": "Silang",
    "reg_mark_line": "Garis",
    "code_qr": "Kode QR",
    "code_barcode": "Kode batang",
    "bryt_order_1": "A1–An, B1–Bn … Standar, dari atas",
    "bryt_order_2": "A1–An, Bn–B1 … Zigzag (per baris), dari atas",
    "bryt_order_3": "A1..B1, A2..B2 … Per kolom, dari atas",
    "bryt_order_4": "A1–A2..B2–B1 … Zigzag (per kolom), dari atas",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … Standar, dari bawah",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … Zigzag (baris), dari bawah",
    "logging_console": "Konsol",
    "logging_file": "Berkas",
    "logging_both": "Keduanya",

    # Settings sections
    "section_processing_mode": " Pekerjaan pemotongan ",
    "processing_mode_ram": "RAM (memori)",
    "processing_mode_hdd": "HDD (diska)",
    "graphic_settings": "Pengaturan grafis",
    "code_settings": "Pengaturan QR / kode batang",
    "logging_settings": "Pengaturan log",
    "barcode_text_position_label": "Posisi teks kode batang:",
    "barcode_text_bottom": "Bawah",
    "barcode_text_side": "Samping",
    "barcode_text_none": "Tidak ada",

    # Graphics
    "extra_margin_label": "Margin di sekitar panel [mm]:",
    "margin_top_label": "Margin atas [mm]:",
    "margin_bottom_label": "Margin bawah [mm]:",
    "margin_left_label": "Margin kiri [mm]:",
    "margin_right_label": "Margin kanan [mm]:",
    "reg_mark_width_label": "Tanda registrasi — Lebar [mm]:",
    "reg_mark_height_label": "Tanda registrasi — Tinggi [mm]:",
    "reg_mark_white_line_width_label": "Tanda registrasi — Ketebalan garis putih [mm]:",
    "reg_mark_black_line_width_label": "Tanda registrasi — Ketebalan garis hitam [mm]:",
    "sep_line_black_width_label": "Garis pemisah — Ketebalan garis hitam [mm]:",
    "sep_line_white_width_label": "Garis pemisah — Ketebalan garis putih [mm]:",
    "slice_gap_label": "Jarak antar panel [mm]:",
    "label_draw_slice_border": "Gambar bingkai panel (garis potong)",

    # Codes
    "scale_label": "Skala [mm]:",
    "scale_x_label": "Lebar X [mm]:",
    "scale_y_label": "Tinggi Y [mm]:",
    "offset_x_label": "Ofset X [mm]:",
    "offset_y_label": "Ofset Y [mm]:",
    "rotation_label": "Rotasi (°):",
    "anchor_label": "Jangkar:",

    # Logging (GUI)
    "logging_mode_label": "Mode log:",
    "log_file_label": "Berkas log:",
    "logging_level_label": "Level log:",

    # Home actions
    "button_load": "Muat",
    "button_save_settings": "Simpan pengaturan saat ini",
    "button_generate_pdf": "Buat PDF",
    "button_refresh_preview": "Segarkan pratinjau",
    "button_refresh_layout": "Segarkan tata letak",

    # License (GUI)
    "hwid_frame_title": "ID Perangkat Keras (HWID)",
    "copy_hwid": "Salin HWID",
    "license_frame_title": "Aktivasi lisensi",
    "enter_license_key": "Masukkan kunci lisensi:",
    "activate": "Aktifkan",
    "status_trial": "Mode uji coba",
    "license_active": "Lisensi aktif",

    # Messages — Profiles
    "msg_no_profile_name": "Tanpa nama",
    "msg_enter_profile_name": "Masukkan nama profil untuk menyimpan.",
    "msg_profile_saved": "Profil disimpan",
    "profile_saved_title": "Profil disimpan",
    "msg_profile_saved_detail": "Profil '{0}' telah disimpan.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Profil '{profile}' telah disimpan dan diterapkan.",
    "msg_no_profile": "Tidak ada profil",
    "warning_no_profile": "Tidak ada profil",
    "msg_select_profile": "Pilih profil dari daftar untuk dimuat.",
    "select_profile": "Pilih profil dari daftar untuk dimuat.",
    "profile_loaded_title": "Profil dimuat",
    "profile_loaded": "Profil '{profile}' telah dimuat.",
    "warning_no_profile_delete": "Tidak ada profil",
    "warning_no_profile_delete_message": "Pilih profil dari daftar untuk dihapus.",
    "profile_not_found": "Profil '{profile}' tidak ditemukan.",
    "profile_not_exist": "Profil '{profile}' tidak ada.",
    "confirm_delete_title": "Konfirmasi penghapusan",
    "confirm_delete_profile": "Yakin ingin menghapus profil '{profile}'?",
    "profile_deleted_title": "Profil dihapus",
    "profile_deleted": "Profil '{profile}' telah dihapus.",

    # Files / Dirs
    "msg_no_input_file": "Tidak ada berkas masukan",
    "msg_unsupported_format": "Format tidak didukung",
    "select_file_title": "Pilih berkas masukan",
    "supported_files": "Berkas yang didukung",
    "all_files": "Semua berkas",
    "select_dir_title": "Pilih folder keluaran",
    "select_log_dir_title": "Pilih folder log",
    "error_output_dir_title": "Kesalahan folder keluaran",
    "error_output_dir": "Folder keluaran yang dipilih tidak valid atau tidak ada:\n{directory}",
    "error_input_file_title": "Kesalahan berkas masukan",
    "error_input_file": "Berkas masukan yang dipilih tidak valid atau tidak ada:\n{file}",
    "save_file_error_title": "Kesalahan menyimpan berkas",
    "save_file_error": "Berkas tidak dapat disimpan: {error}",

    # PDF / Preview
    "msg_pdf_processing_error": "Gagal memproses berkas PDF",
    "msg_thumbnail_error": "Kesalahan memuat gambar mini",
    "msg_no_pdf_output": "Belum ada keluaran PDF",
    "no_pdf_pages": "Berkas PDF tidak memiliki halaman",
    "unsupported_output": "Jenis keluaran ini tidak didukung untuk pratinjau",
    "pdf_generated_title": "Pembuatan selesai",
    "pdf_generated": "Berkas PDF berhasil dibuat di folder:\n{directory}",
    "pdf_generation_error_title": "Kesalahan pembuatan",
    "pdf_generation_error": "Terjadi kesalahan saat membuat PDF. Lihat log untuk detail.",
    "critical_pdf_error_title": "Kesalahan kritis pembuatan PDF",
    "critical_pdf_error": "Terjadi kesalahan kritis saat membuat PDF:\n{error}\nSilakan periksa log.",

    # Settings save/update
    "settings_saved_title": "Pengaturan disimpan",
    "settings_saved": "Pengaturan disimpan ke berkas:\n{filepath}",
    "settings_save_error_title": "Kesalahan menyimpan pengaturan",
    "settings_save_error": "Pengaturan tidak dapat disimpan: {error}",
    "conversion_error_title": "Kesalahan konversi",
    "conversion_error": "Kesalahan saat mengonversi nilai dari GUI: {error}",
    "update_gui_error_title": "Kesalahan pembaruan antarmuka",
    "update_gui_error": "Terjadi kesalahan saat memperbarui antarmuka: {error}",

    # License ops (GUI messages)
    "hwid_copied_to_clipboard": "HWID disalin ke papan klip",
    "computer_hwid": "HWID komputer",
    "public_key_load_error": "Kesalahan memuat kunci publik: {error}",
    "invalid_license_format": "Format kunci lisensi tidak valid: {error}",
    "activation_success": "Lisensi berhasil diaktifkan.",
    "activation_error": "Kesalahan aktivasi lisensi: {error}",
    "log_trial_mode_active": "Mode uji coba aktif",
    "log_trial_mode_inactive": "Mode uji coba nonaktif",

    # Initialization (GUI)
    "init_error_title": "Kesalahan inisialisasi",
    "init_error": "Kesalahan saat membuat direktori: {error}",
    "poppler_path_info": "Informasi path Poppler",
    "ttkthemes_not_installed": "Peringatan: 'ttkthemes' tidak terpasang. Gaya bawaan Tkinter akan digunakan.",

    # Logs (English)
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
Billboard Splitter — Panduan pengguna

Tujuan:
Billboard Splitter membagi desain billboard menjadi panel siap cetak secara otomatis.
Program mengasumsikan skala 1:10. Masukkan nilai overlap, garis putih, dll. berdasarkan skala 1:1.

Jenis keluaran:
• Lembar gabungan: semua panel dalam satu PDF.
• Berkas terpisah: setiap panel sebagai PDF terpisah.

Fitur tambahan:
• Tata letak vertikal/horizontal.
• Rotasi panel 180°.
• Tanda registrasi (silang/garis).
• Tambah QR/kode batang (atur skala/ofset/posisi).
• Simpan, muat, hapus pengaturan sebagai profil.

Langkah dasar:
1) Di 'Beranda' pilih berkas PDF/JPG/TIFF.
2) Atur baris/kolom, overlap, dan garis putih.
3) Pilih tata letak (vertikal/horizontal) dan keluaran (lembar gabungan/berkas terpisah).
4) Aktifkan tanda/kode dan atur rinciannya di 'Pengaturan'.
5) (Opsional) simpan profil dan klik 'Buat PDF'.

Pemecahan masalah:
• Periksa log di folder 'logs'.
• Pastikan path/folder valid.
• Dukungan teknis: tech@printworks.pl (hari kerja 8–16)
"""
}
