# lang_ar.py
# -*- coding: utf-8 -*-
"""
ملف ترجمات للغة العربية (اتجاه الكتابة من اليمين إلى اليسار).
"""

LANG = {
    "barcode_font_size_label": "حجم خط وصف الباركود [pt]:",
    # ==========================
    #  التطبيق – عام
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "خطأ",
    "no_file": "لا يوجد ملف",
    "language": "اللغة",
    "language_switch": "تبديل اللغة",
    "choose_language": "اختر اللغة:",
    "apply_language": "تطبيق",
    "language_changed": "تم تغيير اللغة. بعض التغييرات ستظهر بعد إعادة تشغيل التطبيق.",

    # ========================================
    #  الواجهة الرسومية (GUI)
    # ========================================

    # --- الألسنة الرئيسية ---
    "tab_home": " الرئيسية ",
    "tab_settings": " الإعدادات ",
    "tab_help": " المساعدة ",
    "tab_license": " الترخيص ",

    # --- أزرار عامة ---
    "button_browse": "استعراض...",
    "browse_folder": "استعراض المجلد...",
    "button_save": "حفظ",
    "button_delete": "حذف",
    "button_close": "إغلاق",
    "save_all_settings": "حفظ جميع الإعدادات",

    # --- تسميات الحقول (الرئيسية) ---
    "label_rows": "تقسيم رأسي (صفوف):",
    "label_columns": "تقسيم أفقي (أعمدة):",
    "label_overlap": "التداخل (سم):",
    "label_white_stripe": "الشريط الأبيض (سم):",
    "label_add_white_stripe": "إضافة الشريط الأبيض إلى التداخل الفعلي",
    "label_layout": "تنسيق الإخراج:",
    "label_output_type": "نوع الإخراج:",
    "label_enable_reg_marks": "تفعيل علامات المطابقة:",
    "label_enable_codes": "تفعيل الرموز:",
    "label_enable_sep_lines": "تفعيل خطوط الفصل (بين الألواح)",
    "label_enable_start_line": "تفعيل خط بداية/أعلى الصفحة",
    "label_enable_end_line": "تفعيل خط نهاية/أسفل الصفحة",
    "label_bryt_order": "ترتيب الألواح:",
    "label_slice_rotation": "تدوير الألواح:",
    "label_create_order_folder": "إنشاء مجلد برقم الطلب",

    # --- الأقسام (الرئيسية) ---
    "section_input_file": " ملف الإدخال ",
    "section_scale_and_dimensions": " القياس والأبعاد الناتجة ",
    "label_original_size": "الحجم الأصلي:",
    "label_scale_non_uniform": "تحجيم غير متناسب",
    "label_scale": "مقياس: 1:",
    "label_scale_x": "مقياس X: 1:",
    "label_scale_y": "مقياس Y: 1:",
    "label_output_dimensions": "أبعاد الملف الناتج:",
    "label_width_cm": "العرض [سم]:",
    "label_height_cm": "الارتفاع [سم]:",
    "section_split_settings": " إعدادات القص ",
    "section_profiles": " ملفات الإعدادات ",
    "section_save_location": " موقع الحفظ ",
    "section_input_preview": " معاينة الإدخال ",
    "section_output_preview": " معاينة الإخراج ",

    # --- قيم الخيارات ---
    "layout_vertical": "رأسي",
    "layout_horizontal": "أفقي",
    "output_common_sheet": "ورقة مشتركة",
    "output_separate_files": "ملفات منفصلة",
    "output_both": "ورقة مشتركة وملفات منفصلة",
    "output_common": "ورقة مشتركة",
    "output_separate": "ملفات منفصلة",
    "reg_mark_cross": "علامة (+)",
    "reg_mark_line": "خط",
    "code_qr": "رمز QR",
    "code_barcode": "باركود",
    "bryt_order_1": "A1–An, B1–Bn .. قياسي من الأعلى",
    "bryt_order_2": "A1–An, Bn–B1 .. متعرج حسب الصفوف من الأعلى",
    "bryt_order_3": "A1..B1, A2..B2 .. حسب الأعمدة من الأعلى",
    "bryt_order_4": "A1–A2..B2–B1.. متعرج حسب الأعمدة من الأعلى",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n .. قياسي من الأسفل",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 .. متعرج حسب الصفوف من الأسفل",
    "logging_console": "وحدة التحكم",
    "logging_file": "ملف",
    "logging_both": "كلاهما",

    # --- الأقسام (الإعدادات) ---
    "section_processing_mode": " أوضاع المعالجة ",
    "processing_mode_ram": "الذاكرة RAM (داخل الذاكرة)",
    "processing_mode_hdd": "القرص (التخزين)",
    "graphic_settings": "إعدادات الرسومات",
    "code_settings": "إعدادات QR/الباركود",
    "logging_settings": "إعدادات السجلات",
    "barcode_text_position_label": "موضع النص بجانب الرمز:",
    "barcode_text_bottom": "أسفل",
    "barcode_text_side": "جانبي",
    "barcode_text_none": "بدون نص",

    # --- تسميات (الإعدادات – الرسوم) ---
    "extra_margin_label": "هامش حول الألواح (سم):",
    "margin_top_label": "الهامش العلوي (سم):",
    "margin_bottom_label": "الهامش السفلي (سم):",
    "margin_left_label": "الهامش الأيسر (سم):",
    "margin_right_label": "الهامش الأيمن (سم):",
    "reg_mark_width_label": "عرض علامة المطابقة (سم):",
    "reg_mark_height_label": "ارتفاع علامة المطابقة (سم):",
    "reg_mark_white_line_width_label": "سماكة الخط الأبيض للعلامة (سم):",
    "reg_mark_black_line_width_label": "سماكة الخط الأسود للعلامة (سم):",
    "sep_line_black_width_label": "سماكة الخط الأسود للفصل (سم):",
    "sep_line_white_width_label": "سماكة الخط الأبيض للفصل (سم):",
    "slice_gap_label": "مسافة بين الألواح (سم):",
    "label_draw_slice_border": "رسم إطار حول اللوح (خط قص)",

    # --- تسميات (الإعدادات – الرموز) ---
    "scale_label": "الحجم (سم):",
    "scale_x_label": "العرض X (سم):",
    "scale_y_label": "الارتفاع Y (سم):",
    "offset_x_label": "الإزاحة X (سم):",
    "offset_y_label": "الإزاحة Y (سم):",
    "rotation_label": "الدوران (°):",
    "anchor_label": "الزاوية:",

    # --- تسميات (الإعدادات – السجلات) ---
    "logging_mode_label": "وضع التسجيل:",
    "log_file_label": "ملف السجل:",
    "logging_level_label": "مستوى التسجيل:",

    # --- الأزرار / الأفعال (الرئيسية) ---
    "button_load": "تحميل",
    "button_save_settings": "حفظ الإعدادات الحالية",
    "button_generate_pdf": "توليد PDF",
    "button_refresh_preview": "تحديث المعاينة",
    "button_refresh_layout": "تحديث التنسيق",

    # --- الترخيص (GUI) ---
    "hwid_frame_title": "معرّف العتاد الفريد (HWID)",
    "copy_hwid": "نسخ HWID",
    "license_frame_title": "تفعيل الترخيص",
    "enter_license_key": "أدخل مفتاح الترخيص:",
    "activate": "تفعيل",
    "status_trial": "نسخة تجريبية",
    "license_active": "الترخيص فعّال",

    # ================================================
    #  رسائل للمستخدم (حوارات، شريط الحالة)
    # ================================================

    # --- الملفات الشخصية (Profiles) ---
    "msg_no_profile_name": "بدون اسم",
    "msg_enter_profile_name": "أدخل اسم ملف إعدادات للحفظ.",
    "msg_profile_saved": "تم حفظ الملف الشخصي",
    "profile_saved_title": "تم الحفظ",
    "msg_profile_saved_detail": "تم حفظ الملف الشخصي «{0}».",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "تم حفظ وتطبيق الملف الشخصي '{profile}'.",
    "msg_no_profile": "لا يوجد ملف شخصي",
    "warning_no_profile": "لا يوجد ملف شخصي",
    "msg_select_profile": "اختر اسم ملف شخصي من القائمة للتحميل.",
    "select_profile": "اختر اسم ملف شخصي من القائمة للتحميل.",
    "profile_loaded_title": "تم تحميل الملف الشخصي",
    "profile_loaded": "تم تحميل الملف الشخصي «{profile}».",
    "warning_no_profile_delete": "لا يوجد ملف شخصي",
    "warning_no_profile_delete_message": "اختر ملفًا شخصيًا من القائمة للحذف.",
    "profile_not_found": "الملف الشخصي «{profile}» غير موجود.",
    "profile_not_exist": "الملف الشخصي «{profile}» غير موجود.",
    "confirm_delete_title": "تأكيد الحذف",
    "confirm_delete_profile": "هل تريد حذف الملف الشخصي «{profile}»؟",
    "profile_deleted_title": "تم الحذف",
    "profile_deleted": "تم حذف الملف الشخصي «{profile}».",

    # --- الملفات / الدلائل ---
    "msg_no_input_file": "لا يوجد ملف إدخال",
    "msg_unsupported_format": "صيغة غير مدعومة",
    "select_file_title": "اختيار ملف الإدخال",
    "supported_files": "الملفات المدعومة",
    "all_files": "كل الملفات",
    "select_dir_title": "اختيار مجلد الإخراج",
    "select_log_dir_title": "اختيار مجلد السجلات",
    "error_output_dir_title": "خطأ في مجلد الإخراج",
    "error_output_dir": "مجلد الإخراج المحدد غير صالح أو غير موجود:\n{directory}",
    "error_input_file_title": "خطأ في ملف الإدخال",
    "error_input_file": "ملف الإدخال المحدد غير صالح أو غير موجود:\n{file}",
    "save_file_error_title": "خطأ في حفظ الملف",
    "save_file_error": "تعذّر حفظ الملف: {error}",

    # --- معالجة PDF / المعاينة ---
    "msg_pdf_processing_error": "فشل معالجة ملف PDF",
    "msg_thumbnail_error": "خطأ في تحميل المصغّر",
    "msg_no_pdf_output": "لا يوجد مخرجات PDF",
    "no_pdf_pages": "ملف PDF لا يحتوي على صفحات",
    "unsupported_output": "نوع إخراج غير مدعوم للمعاينة",
    "pdf_generated_title": "اكتمل التوليد",
    "pdf_generated": "تم إنشاء ملف/ملفات PDF بنجاح في المجلد:\n{directory}",
    "pdf_generation_error_title": "خطأ أثناء التوليد",
    "pdf_generation_error": "حدثت أخطاء أثناء توليد PDF. راجع السجلات.",
    "critical_pdf_error_title": "خطأ بالغ في توليد PDF",
    "critical_pdf_error": "حدث خطأ بالغ أثناء توليد PDF:\n{error}\nيرجى مراجعة السجلات.",
    "settings_saved_title": "تم حفظ الإعدادات",
    "settings_saved": "تم حفظ الإعدادات في الملف:\n{filepath}",
    "settings_save_error_title": "خطأ حفظ الإعدادات",
    "settings_save_error": "تعذّر حفظ الإعدادات: {error}",
    "conversion_error_title": "خطأ تحويل",
    "conversion_error": "خطأ في تحويل القيم من الواجهة: {error}",
    "update_gui_error_title": "خطأ في تحديث الواجهة",
    "update_gui_error": "حدث خطأ أثناء تحديث الواجهة: {error}",

    # --- الترخيص ---
    "hwid_copied_to_clipboard": "تم نسخ HWID إلى الحافظة",
    "computer_hwid": "HWID الجهاز",
    "public_key_load_error": "خطأ في تحميل المفتاح العام: {error}",
    "invalid_license_format": "صيغة مفتاح الترخيص غير صالحة: {error}",
    "activation_success": "تم تفعيل الترخيص بنجاح.",
    "activation_error": "خطأ في تفعيل الترخيص: {error}",
    "log_trial_mode_active": "الوضع التجريبي مفعل",
    "log_trial_mode_inactive": "الوضع التجريبي غير مفعل",

    # --- التهيئة ---
    "init_error_title": "خطأ في التهيئة",
    "init_error": "خطأ في تهيئة الدلائل: {error}",
    "poppler_path_info": "معلومات مسار Poppler",
    "ttkthemes_not_installed": "ملاحظة: مكتبة ttkthemes غير مثبتة. سيُستخدم نمط Tkinter الافتراضي.",

    # =====================================
    #  السجلات (رسائل المُسجِّل)
    # =====================================

    # --- عام / الضبط ---
    "log_configured": "تم ضبط التسجيل: المستوى={0}، الوضع={1}، الملف={2}",
    "log_no_handlers": "تحذير: لم يتم ضبط معالجات للسجلات (الوضع: {0}).",
    "log_critical_error": "خطأ بالغ في ضبط التسجيل: {0}",
    "log_basic_config": "بسبب خطأ تم استخدام ضبط أساسي للتسجيل.",
    "log_dir_create_error": "خطأ بالغ: تعذر إنشاء مجلد السجلات {0}: {1}",

    # --- السجلات – التهيئة/الدلائل (init_directories.py) ---
    "error_critical_init": "خطأ بالغ أثناء التهيئة: {0}",
    "logger_init_error": "خطأ في تهيئة الدلائل: {error}",
    "directory_created": "تم إنشاء الدليل: {0}",
    "directory_creation_error": "تعذّر إنشاء الدليل {0}: {1}",
    "sample_file_copied": "تم نسخ ملف العينة إلى {0}",
    "sample_file_copy_error": "خطأ عند نسخ ملف العينة: {0}",
    "log_created_output_dir": "تم إنشاء مجلد الإخراج: {0}",
    "log_cannot_create_output_dir": "تعذّر إنشاء مجلد الإخراج {0}: {1}",

    # --- السجلات – Splitter (splitter.py) ---
    "log_graphic_settings_error": "فشل تحميل إعدادات الرسوم عند التهيئة: {0}",
    "log_loading_pdf": "جارٍ تحميل ملف PDF: {0}",
    "log_loading_bitmap": "جارٍ تحميل ملف نقطي: {0}",
    "log_invalid_dpi": "تمت قراءة DPI غير صالح ({0}). سيتم استخدام {1} DPI الافتراضي.",
    "log_image_dimensions": "أبعاد الصورة: {0}×{1} بكسل، النمط: {2}، DPI: {3:.1f} → {4:.3f}×{5:.3f} نقطة",
    "log_image_processing_color": "معالجة الصورة في وضع الألوان الأصلي: {0}",
    "log_unusual_color_mode": "وضع ألوان غير معتاد: «{0}». قد لا يعمل ReportLab/Pillow بشكل صحيح.",
    "log_draw_image_error": "خطأ drawImage في ReportLab للوضع {0}: {1}",
    "log_unsupported_format": "صيغة إدخال غير مدعومة: {0}",
    "log_input_file_not_found": "ملف الإدخال غير موجود: {0}",
    "log_load_process_error": "خطأ في تحميل/معالجة الملف {0}: {1}",
    "log_input_file_not_exists": "ملف الإدخال غير موجود أو المسار فارغ: «{0}»",
    "log_cannot_load_or_empty_pdf": "تعذّر تحميل ملف الإدخال أو أن PDF فارغ/تالف.",
    "log_pdf_dimensions_info": "  أبعاد PDF: {0:.1f} مم × {1:.1f} مم",
    "log_invalid_pdf_dimensions": "أبعاد صفحة PDF غير صالحة: {0}×{1} نقطة.",

    #   Splitter – حسابات الأبعاد
    "log_extra_margin": "تم ضبط الهامش الإضافي على {0:.3f} نقطة",
    "log_invalid_rows_cols": "عدد صفوف ({0}) أو أعمدة ({1}) غير صالح.",
    "error_invalid_rows_cols": "يجب أن تكون الصفوف والأعمدة أعدادًا صحيحة موجبة.",
    "log_invalid_overlap_white_stripe": "قِيَم التداخل ({0}) أو الشريط الأبيض ({1}) غير صالحة. يجب أن تكون رقمية.",
    "error_invalid_overlap_white_stripe": "يجب أن تكون قيم التداخل والشريط الأبيض رقمية (مم).",
    "log_stripe_usage": "تم ضبط use_white_stripe={0}، white_stripe={1:.3f} مم",
    "log_effective_overlap": "التداخل الأساسي (رسوم): {0:.3f} مم، الشريط الأبيض: {1:.3f} مم، التداخل الفعلي: {2:.3f} مم",
    "log_computed_dimensions": "تم الحساب: PDF {0:.3f}×{1:.3f} مم. لوح: {2:.3f} نقطة ({3:.3ف} مم) × {4:.3f} نقطة ({5:.3f} مم). اللب: {6:.3f}×{7:.3f} نقطة. التداخل الفعلي: {8:.3f} مم",
    "log_invalid_dimensions": "أبعاد لوح غير صالحة ({0:.3f}×{1:.3f}) أو لب ({2:.3f}×{3:.3f}) عند per={4}, stripe={5}, r={6}, c={7}, W={8} مم, H={9} مم",
    "error_invalid_slice_dimensions": "الأبعاد المحسوبة للّوح/اللب غير صالحة أو سالبة.",

    #   Splitter – معلومات الألواح والترتيب
    "log_generating_slice_info": "توليد معلومات اللوح: {0}",
    "log_no_slices_info_generated": "تعذّر توليد معلومات الألواح.",
    "log_applying_rotated_order": "تطبيق ترتيب تدوير 180°: {0}",
    "log_applying_standard_order": "تطبيق الترتيب القياسي (0°): {0}",
    "log_unknown_bryt_order": "ترتيب ألواح غير معروف: «{0}». سيتم استخدام الافتراضي.",
    "log_final_slices_order": "  الترتيب النهائي للألواح ({0}): [{1}]",

    #   Splitter – الطبقات (overlay) والدمج
    "log_invalid_dimensions_overlay": "محاولة إنشاء طبقة بأبعاد غير صالحة: {0}. سيتم التخطي.",
    "log_empty_overlay": "تم إنشاء ملف Overlay PDF فارغ أو شبه فارغ. سيتم تخطي الدمج.",
    "log_overlay_error": "خطأ عند إنشاء ملف overlay: {0}",
    "log_merge_error": "محاولة دمج overlay بدون صفحات. يتم التخطي.",
    "log_merge_page_error": "خطأ عند دمج overlay PDF: {0}",
    "log_fallback_draw_rotating_elements": "تعذّر الحصول على الصفوف/الأعمدة لـ _draw_rotating_elements، سيتم استخدام 1×1.",
    "log_overlay_created_for_slice": "تم إنشاء طبقة الشرائط/العلامات للوح {0}",
    "log_overlay_creation_failed_for_slice": "فشل إنشاء الطبقة لـ {0}",
    "log_merging_rotated_overlay": "دمج طبقة مُدارة للوح {0} مع T={1}",
    "log_merging_nonrotated_overlay": "دمج طبقة غير مُدارة للوح {0}",
    "log_merging_all_codes_overlay": "دمج طبقة جميع الرموز (بدون تدوير)",
    "log_merging_separation_lines_overlay": "دمج طبقة خطوط الفصل (بدون تدوير)",
    "log_merging_code_overlay_for_slice": "تم دمج طبقة الرمز لـ {0} بدون تدوير.",
    "log_merging_separation_overlay_for_slice": "تم دمج طبقة خطوط الفصل لـ {0} بدون تدوير.",

    #   Splitter – الرسم (شرائط، علامات، خطوط)
    "log_drawing_top_stripe": "[Canvas] رسم الشريط العلوي لـ {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] رسم الشريط الأيمن لـ {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] تعبئة وتحديد الزاوية لـ {0} عند ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "رسم علامة (+) بمركز عند ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "رسم خطوط المطابقة لـ {0} في النطاق ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  رسم خط عمودي أيمن: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  رسم خط أفقي علوي: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "رسم خط فصل (أبيض فوق أسود): ({0}) @ ({1:.3f}, {2:.3f})، الطول={3:.3f}",
    "log_drawing_reg_marks_for_slice": "رسم علامات (+) لـ {0} [{1},{2}] / [{3},{4}] في النطاق ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  المراكز المحسوبة: TL({0:.1f},{1:.1f})، TR({2:.1f},{3:.1f})، BL({4:.1f},{5:.1f})، BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    رسم TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    رسم TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    رسم BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    رسم BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    تم تجاوز {0} وفقًا لقاعدة الموضع [{1},{2}]",
    "log_trial_common_sheet": "تطبيق علامة مائية TRIAL على الورقة المشتركة",

    # العلامة المائية
    "log_trial_watermark_added": "تمت إضافة العلامة المائية TRIAL",
    "error_drawing_trial_text": "خطأ في رسم نص العلامة المائية: {error}",

    #   Splitter – خطوط الفصل (صفحة كاملة)
    "log_drawing_separation_lines_for_page": "رسم خطوط الفصل للصفحة (التنسيق={0}، الألواح={1}، الفهرس={2})",
    "log_vertical_line_between_slices": "  خط عمودي بين الألواح {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  بداية خط عمودي @ x={0:.1f}",
    "log_vertical_line_end": "  نهاية خط عمودي @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  خط أفقي بين الألواح {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  بداية خط أفقي @ y={0:.1f}",
    "log_horizontal_line_end": "  نهاية خط أفقي @ y={0:.1f}",
    "log_sep_line_start_separate": "  (ملفات_منفصلة) بدء عمودي/أفقي @ {0:.1f}",
    "log_sep_line_end_separate": "  (ملفات_منفصلة) نهاية عمودي/أفقي @ {0:.1f}",

    #   Splitter – توليد الرموز / QR
    "log_generate_barcode_data": "توليد بيانات الرمز: {0}",
    "log_barcode_data_shortened": "تم اختصار بيانات الرمز إلى {0} محارف.",
    "log_barcode_data_error": "خطأ في توليد بيانات الرمز: {0}",
    "log_compose_barcode_payload": "تجميع حمولة الرمز ({0}): {1}",
    "log_barcode_payload_shortened": "تم اختصار الحمولة إلى {0} محارف لصيغة {1}",
    "log_barcode_payload_error": "خطأ عند تجميع الحمولة: {0}",
    "log_unknown_anchor_fallback": "زاوية تثبيت غير معروفة «{0}»، سيتم استخدام الزاوية اليسرى السفلية",
    "log_used_default_code_settings": "تم استخدام الإعدادات الافتراضية للرمز {0}/{1}.",
    "log_no_layout_key_fallback": "لا يوجد تنسيق «{0}» لـ {1}/{2}. تم استخدام الأول المتاح: «{3}».",
    "log_code_settings_error": "إعدادات الرمز ناقصة/خاطئة ({0}/{1}/{2}): {3}. تم استخدام القيم الافتراضية.",
    "log_drawing_barcode": "رسم {0} عند ({1:.3f}, {2:.3f}) [الأساس ({3:.3f}, {4:.3f}) + الإزاحة ({5:.3f}, {6:.3f})]، دوران: {7}°",
    "error_generate_qr_svg": "فشل توليد SVG لرمز QR.",
    "error_invalid_scale_for_qr": "حجم QR غير صالح: {0} مم",
    "error_invalid_qr_scale_factor": "معامل مقياس QR غير صالح: {0}",
    "error_generate_barcode_svg": "فشل توليد SVG للباركود.",
    "error_invalid_scale_for_barcode": "حجم باركود غير صالح: {0}×{1} مم",
    "error_invalid_barcode_scale_factor": "معامل مقياس الباركود غير صالح: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: الحجم في الإعداد={1:.3f} مم، عرض SVG={2:.3f} نقطة، fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: الحجم في الإعداد=({1:.3f} مم, {2:.3f} مم)، أبعاد SVG=({3:.3f} نقطة, {4:.3f} نقطة)، fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "خطأ في رسم الرمز «{0}»: {1}",
    "log_prepared_barcode_info": "تم تحضير معلومات الرمز لـ {0} ({1}, الزاوية={2}): الموضع المطلق الأساس ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "خطأ في تحضير بيانات الرمز لـ {0}: {1}",
    "log_drawing_barcodes_count": "رسم {0} رموز/QR...",
    "log_missing_barcode_info_key": "مفتاح مفقود في معلومات الرمز أثناء الرسم: {0}. معلومات: {1}",
    "log_error_drawing_barcode_in_draw_all": "خطأ في رسم الرمز «{0}» داخل _draw_all_barcodes: {1}",

    #   Splitter – عملية القص (الدوال split_*)
    "log_start_splitting_process": "--- بدء عملية القص للملف: {0} ---",
    "log_split_settings": "  الإعدادات: {0}×{1} لوح، التداخل={2} مم، الشريط الأبيض={3} مم (+تداخل: {4})",
    "log_output_dir_info": "  الإخراج: {0} / {1} في «{2}»",
    "log_lines_marks_barcodes_info": "  الخطوط: فصل={0}، بداية={1}، نهاية={2} | العلامات: {3} ({4})، الرموز: {5} ({6})",
    "log_bryt_order_info": "  الترتيب: {0}، تدوير الألواح: {1}°",
    "log_invalid_dimensions_in_slice_info": "أبعاد غير صالحة في slice_info لـ {0}: {1}×{2}",
    "log_content_transform": "تحويل المحتوى T_content لـ {0}: {1}",
    "log_merged_content_for_slice": "تم دمج المحتوى للوح {0} في صفحة جديدة",
    "log_slice_reader_created": "تم إنشاء لوح كامل (PdfReader) لـ {0}",
    "log_slice_reader_creation_error": "خطأ في إنشاء لوح كامل لـ {0}: {1}",
    "log_used_get_transform": "استخدام _get_transform (إزاحة فقط): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- البدء: ملفات منفصلة (التدوير في create_slice_reader) ---",
    "log_creating_file_for_slice": "إنشاء ملف للّوح {0}: {1}",
    "log_invalid_page_size_for_slice": "حجم صفحة غير صالح ({0}×{1}) لـ {2}. سيتم التخطي.",
    "log_blank_page_creation_error": "خطأ في إنشاء صفحة فارغة لـ {0} (الحجم {1}×{2}): {3}. سيتم التخطي.",
    "log_transform_for_slice": "تحويل T (إزاحة فقط) لـ {0}: {1}",
    "log_merging_complete_slice": "دمج لوح كامل {0} مع تحويل: {1}",
    "log_skipped_slice_merging": "تم تخطي دمج اللوح الكامل لـ {0}.",
    "log_file_saved": "تم حفظ الملف: {0}",
    "log_file_save_error": "خطأ في حفظ الملف {0}: {1}",
    "log_finished_split_separate_files": "--- اكتمل: ملفات منفصلة (تم الحفظ {0}/{1}) ---",
    "log_no_slices_split_horizontal": "لا توجد ألواح للمعالجة في split_horizontal.",
    "log_start_split_horizontal": "--- البدء: ورقة مشتركة – أفقي (التدوير في create_slice_reader) ---",
    "log_page_dimensions": "أبعاد الصفحة: {0:.1f}×{1:.1f} مم ({2} لوحًا)",
    "log_page_creation_error": "خطأ في إنشاء صفحة الإخراج ({0}×{1}): {2}. تم الإنهاء.",
    "log_slice_at_position": "لوح {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "تحويل T (إزاحة فقط) لـ {0}: {1}",
    "log_merging_complete_bryt": "دمج لوح كامل {0} مع تحويل: {1}",
    "log_skipped_merging_bryt": "تم تخطي دمج اللوح الكامل لـ {0}.",
    "log_file_result_saved": "تم حفظ ملف النتيجة: {0}",
    "log_file_result_save_error": "خطأ في حفظ ملف النتيجة {0}: {1}",
    "log_finished_split_horizontal": "--- اكتمل: ورقة مشتركة – أفقي ---",
    "log_no_slices_split_vertical": "لا توجد ألواح للمعالجة في split_vertical.",
    "log_start_split_vertical": "--- البدء: ورقة مشتركة – رأسي (التدوير في create_slice_reader) ---",
    "log_finished_split_vertical": "--- اكتمل: ورقة مشتركة – رأسي ---",
    "log_unknown_layout": "تنسيق غير معروف للورقة المشتركة: «{0}».",
    "log_unknown_output_type": "نوع إخراج غير معروف: «{0}».",
    "log_finished_splitting_success": "--- انتهت عملية القص للملف: {0} — بنجاح ---",
    "log_finished_splitting_errors": "--- انتهت عملية القص للملف: {0} — مع وجود أخطاء ---",
    "log_value_error_in_splitting": "خطأ في الإدخال أو الحساب: {0}",
    "log_finished_splitting_critical_error": "--- انتهت عملية القص للملف: {0} — خطأ بالغ ---",
    "log_unexpected_error_in_splitting": "خطأ غير متوقع أثناء قص الملف {0}: {1}",

    #   Splitter – وضع الاختبار (__main__)
    "log_script_mode_test": "تم تشغيل splitter.py كسكربت أساسي (وضع اختبار).",
    "log_loaded_config": "تم تحميل الإعدادات.",
    "log_error_loading_config": "فشل تحميل الإعدادات: {0}",
    "log_created_example_pdf": "تم إنشاء ملف PDF تجريبي: {0}",
    "log_cannot_create_example_pdf": "فشل إنشاء PDF تجريبي: {0}",
    "log_start_test_split": "بدء قص تجريبي للملف: {0} → {1}",
    "log_test_split_success": "تم اكتمال القص التجريبي بنجاح.",
    "log_test_split_errors": "اكتمل القص التجريبي مع وجود أخطاء.",

    # --- السجلات – QR/الباركود (barcode_qr.py) ---
    "log_qr_empty_data": "محاولة توليد QR لبيانات فارغة.",
    "log_qr_generated": "تم توليد SVG لرمز QR لـ: {0}...",
    "log_qr_error": "خطأ في توليد QR للبيانات «{0}»: {1}",
    "log_barcode_empty_data": "محاولة توليد باركود لبيانات فارغة.",
    "log_barcode_generated": "تم توليد SVG للباركود لـ: {0}...",
    "log_barcode_error": "خطأ في توليد الباركود لـ «{0}»: {1}",
    "log_basic_handler_configured": "تم ضبط معالج أساسي للمسجل في barcode_qr.py",
    "log_basic_handler_error": "خطأ في ضبط المعالج الأساسي في barcode_qr: {0}",

    # --- السجلات – الضبط/الملفات الشخصية (main_config_manager.py) ---
    "loading_profiles_from": "تحميل الملفات الشخصية من",
    "profiles_file": "ملف الملفات الشخصية",
    "does_not_contain_dict": "لا يحتوي قاموسًا. سيتم إنشاء جديد",
    "not_found_creating_new": "غير موجود. سيتم إنشاء ملف فارغ",
    "json_profiles_read_error": "خطأ في قراءة JSON لملف الملفات الشخصية",
    "file_will_be_overwritten": "سيتم استبدال الملف عند الحفظ",
    "json_decode_error_in_profiles": "خطأ في فك JSON لملف الملفات الشخصية",
    "cannot_load_profiles_file": "تعذّر تحميل ملف الملفات الشخصية",
    "unexpected_profiles_read_error": "خطأ غير متوقع عند قراءة الملفات الشخصية",
    "saving_profiles_to": "حفظ الملفات الشخصية إلى",
    "cannot_save_profiles_file": "تعذّر حفظ ملف الملفات الشخصية",
    "profiles_save_error": "خطأ في حفظ الملفات الشخصية إلى الملف",
    "logger_profile_saved": "تم حفظ الملف الشخصي: {profile}",
    "logger_profile_not_found": "الملف الشخصي المطلوب تحميله غير موجود: {profile}",
    "logger_profile_loaded": "تم تحميل الملف الشخصي: {profile}",
    "logger_profile_delete_not_exist": "محاولة حذف ملف شخصي غير موجود: {profile}",
    "logger_profile_deleted": "تم حذف الملف الشخصي: {profile}",
    "logger_start_save_settings": "بدء حفظ الإعدادات من الواجهة.",
    "logger_invalid_value": "قيمة غير صالحة للمفتاح «{key}». تم ضبطها على 0.0.",
    "logger_end_save_settings": "انتهى حفظ الإعدادات من الواجهة.",
    "logger_conversion_error": "خطأ تحويل قيم الواجهة: {error}",
    "conversion_failed": "فشل تحويل قيم الواجهة",
    "logger_unexpected_save_error": "خطأ غير متوقع عند حفظ الإعدادات: {error}",
    "logger_settings_saved": "تم حفظ الإعدادات في الملف: {file}",

    # --- السجلات – الترخيص (main_license.py) ---
    "public_key_load_error_log": "خطأ في تحميل المفتاح العام",
    "license_key_decode_error": "خطأ في فك مفتاح الترخيص",
    "license_activation_error": "خطأ في تفعيل الترخيص",

    # --- السجلات – الوحدة الرئيسية (main.py) ---
    "ui_created": "تم إنشاء واجهة المستخدم.",
    "error_tab_home": "خطأ في إنشاء واجهة «الرئيسية»",
    "error_tab_settings": "خطأ في إنشاء واجهة «الإعدادات»",
    "error_tab_help": "خطأ في إنشاء واجهة «المساعدة»",
    "error_creating_license_ui": "خطأ في إنشاء واجهة «الترخيص»",
    "error_loading_ui": "خطأ عام في تحميل الواجهة: {error}",
    "error_creating_home_ui": "خطأ عند إنشاء واجهة «الرئيسية»",
    "error_creating_settings_ui": "خطأ عند إنشاء واجهة «الإعدادات»",
    "error_creating_help_ui": "خطأ عند إنشاء واجهة «المساعدة»",
    "logger_update_gui": "بدء تحديث الواجهة من الإعدادات.",
    "logger_end_update_gui": "انتهى تحديث الواجهة من الإعدادات.",
    "logger_update_gui_error": "خطأ غير متوقع عند تحديث الواجهة: {error}",
    "logger_invalid_output_dir": "مجلد إخراج غير صالح أو غير موجود: {directory}",
    "logger_invalid_input_file": "ملف إدخال غير صالح أو غير موجود: {file}",
    "logger_start_pdf": "تم بدء عملية توليد PDF.",
    "logger_pdf_save_error": "تم إيقاف توليد PDF: فشل حفظ الإعدادات الحالية.",
    "logger_pdf_success": "تم توليد PDF بنجاح.",
    "logger_pdf_exception": "استثناء في العملية الرئيسية لتوليد PDF.",
    "icon_set_error": "خطأ في تعيين أيقونة التطبيق: {error}",
    "accent_button_style_error": "خطأ في تعيين نمط الزر المميز: {error}",
    "logger_file_save_error": "خطأ في حفظ الملف {file}: {error}",

    #   السجلات – المعاينة (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "خطأ في توليد المصغّر",
    "output_preview_update_called": "تم استدعاء تحديث معاينة الإخراج",
    "output_preview_canvas_missing": "لوحة معاينة الإخراج (canvas) مفقودة",
    "pdf_found_in_output_dir": "تم العثور على PDF في مجلد الإخراج",
    "preparing_thumbnail": "تحضير المصغّر",
    "thumbnail_generated_successfully": "تم توليد المصغّر بنجاح",
    "thumbnail_generation_error": "خطأ في توليد المصغّر لـ",
    "no_pdf_for_common_sheet": "لا يوجد PDF لمعاينة الورقة المشتركة",
    "no_pdf_for_separate_files": "لا توجد ملفات PDF مولدة للمعاينة",
    "cannot_load_thumbnail": "تعذّر تحميل المصغّر من",

    #   السجلات – داخلية للتطوير (main.py)
    "missing_gui_var_created": "تم إنشاء متغير GUI مفقود للمفتاح: {key}",
    "missing_gui_structure_created": "تم إنشاء بنية GUI مفقودة لـ: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "تم إنشاء متغير GUI مفقود لـ: {code_type}/{output_type}/{layout}/{param}",

    # نص إضافي لـ main_ui_help.py
    "help_text": """
    Billboard Splitter – دليل المستخدم\n\n
    الهدف من البرنامج:\n
    يقوم Billboard Splitter بتقسيم مشاريع اللوحات الإعلانية تلقائيًا إلى ألواح جاهزة للطباعة.
    صُمم البرنامج للعمل مع ملفات بمقياس 1:10.\n
    يتم إدخال القيم في أقسام: التداخل، الشريط الأبيض والإعدادات بمقياس 1:1.
    يمكن للبرنامج ترتيب الألواح المقطوعة في PDF وفق التنسيق المختار:\n
    • ورقة مشتركة: جميع الألواح في مستند واحد.\n
    • ملفات منفصلة: كل لوح في ملف PDF منفصل.\n\n
    إمكانيات إضافية:\n
    • اختيار التنسيق – رأسي أو أفقي (في الرأسي تكون خطوط الفصل أعلى/أسفل،
      وفي الأفقي تكون يسار/يمين).\n
    • تدوير الألواح 180° (عكس المشروع بالكامل).\n
    • إضافة علامات مطابقة (علامة + أو خط) لضمان الدقة عند اللصق.\n
    • إضافة رموز QR أو باركود – تُولد من بيانات الإدخال لتعريف الألواح.\n
    • حفظ الإعدادات كملفات شخصية (Profiles) يمكن تحميلها وتعديلها وحذفها للتبديل السريع بين المشاريع.\n\n
    الخطوات الأساسية:\n\n
    1) اختيار ملف الإدخال:\n
    • في تبويب «الرئيسية» اختر ملف PDF أو JPG أو TIFF يحتوي تصميم اللوحة.\n
    • إن لم تحدد مسارًا خاصًا فسيُستخدم ملف عيّنة افتراضي.\n\n
    2) إعدادات القص:\n
    • أدخل عدد الصفوف والأعمدة المطلوب تقسيم المشروع إليها.\n
    • اضبط مقدار التداخل.\n
    • اختياريًا: اضبط عرض الشريط الأبيض الذي يُضاف إلى التداخل الفعلي.\n\n
    3) تنسيق الإخراج:\n
    • رأسي: تُرتّب الألواح رأسيًا على صفحة PDF.\n
    • أفقي: تُرتّب الألواح أفقيًا.\n\n
    4) نوع الإخراج:\n
    • ورقة مشتركة – ملف PDF واحد.\n
    • ملفات منفصلة – ملف PDF لكل لوح.\n
    • من «الرئيسية» يمكنك تفعيل علامات المطابقة – علامة (+) أو خط – وضبطها.\n
    • اختياريًا فعّل QR/الباركود – يُولد من بيانات المشروع.\n
    • تُضبط معاملات الرمز (المقياس، الإزاحة، الدوران، الموضع) من «الإعدادات».\n\n
    5) إدارة الإعدادات:\n
    • من «الإعدادات» يمكنك ضبط المعاملات الرسومية بدقة (الهوامش، سماكات الخطوط، المسافات) والرموز.\n
    • احفظ التهيئة الحالية كملف شخصي لإعادة الاستخدام.\n
    • تتيح الملفات الشخصية (profiles.json) التبديل السريع بين مجموعات إعدادات مختلفة.\n\n
    6) توليد PDF:\n
    • عند الجاهزية اضغط «توليد PDF».\n
    • تُحفَظ النتائج في مجلد «output» (أو المحدد)، وتُحفظ السجلات اليومية في «logs».\n\n
    في حال حدوث مشاكل:\n
    • راجع السجلات في مجلد «logs». يُنشأ ملف سجل جديد يوميًا يتضمن التاريخ في اسمه.\n
    • تأكّد من تعريف كل الدلائل المطلوبة.\n
    • الدعم: tech@printworks.pl (أيام العمل 8–16)\n
    """
}
