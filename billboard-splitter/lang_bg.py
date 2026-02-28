# lang_bg.py
"""
Файл с преводи за български език.
"""

LANG = {
    "barcode_font_size_label": "Размер на шрифта за описание на баркод [pt]:",
    # ==========================
    #  Приложение – Общи
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Грешка",
    "no_file": "Няма файл",
    "language": "Език",
    "language_switch": "Смяна на езика",
    "choose_language": "Изберете език:",
    "apply_language": "Приложи",
    "language_changed": "Езикът е сменен. Част от промените ще са видими след рестартиране на приложението.",

    # ========================================
    #  Графичен интерфейс (GUI)
    # ========================================

    # --- Основни раздели ---
    "tab_home": " Начало ",
    "tab_settings": " Настройки ",
    "tab_help": " Помощ ",
    "tab_license": " Лиценз ",

    # --- Общи бутони ---
    "button_browse": "Преглед...",
    "browse_folder": "Преглед на папка...",
    "button_save": "Запази",
    "button_delete": "Изтрий",
    "button_close": "Затвори",
    "save_all_settings": "Запази всички настройки",

    # --- Полета (Начало) ---
    "label_rows": "Вертикално делене (редове):",
    "label_columns": "Хоризонтално делене (колони):",
    "label_overlap": "Припокриване (см):",
    "label_white_stripe": "Бяла лента (см):",
    "label_add_white_stripe": "Добави бяла лента към ефективното припокриване",
    "label_layout": "Оформление на изхода:",
    "label_output_type": "Тип изход:",
    "label_enable_reg_marks": "Включи регистрационни марки:",
    "label_enable_codes": "Включи кодове:",
    "label_enable_sep_lines": "Включи разделителни линии (между панелите)",
    "label_enable_start_line": "Включи начална/горна линия на листа",
    "label_enable_end_line": "Включи крайна/долна линия на листа",
    "label_bryt_order": "Ред на панелите:",
    "label_slice_rotation": "Ротация на панелите:",
    "label_create_order_folder": "Създай папка с номер на поръчка",

    # --- Секции (Начало) ---
    "section_input_file": " Входен файл ",
    "section_scale_and_dimensions": " Мащаб и изходни размери ",
    "label_original_size": "Оригинален размер:",
    "label_scale_non_uniform": "Непропорционално мащабиране",
    "label_scale": "Мащаб: 1:",
    "label_scale_x": "Мащаб X: 1:",
    "label_scale_y": "Мащаб Y: 1:",
    "label_output_dimensions": "Размери на изходния файл:",
    "label_width_cm": "Ширина [см]:",
    "label_height_cm": "Височина [см]:",
    "section_split_settings": " Настройки на рязане ",
    "section_profiles": " Профили с настройки ",
    "section_save_location": " Място за запис ",
    "section_input_preview": " Преглед на входа ",
    "section_output_preview": " Преглед на изхода ",

    # --- Стойности на опциите ---
    "layout_vertical": "Вертикално",
    "layout_horizontal": "Хоризонтално",
    "output_common_sheet": "Общ лист",
    "output_separate_files": "Отделни файлове",
    "output_both": "Общ лист и отделни файлове",
    "output_common": "Общ лист",
    "output_separate": "Отделни файлове",
    "reg_mark_cross": "Кръст",
    "reg_mark_line": "Линия",
    "code_qr": "QR код",
    "code_barcode": "Баркод",
    "bryt_order_1": "A1–An, B1–Bn, .. Стандарт, отгоре",
    "bryt_order_2": "A1–An, Bn–B1, .. Змия по редове, отгоре",
    "bryt_order_3": "A1..B1, A2..B2, .. По колони, отгоре",
    "bryt_order_4": "A1–A2..B2–B1.. Змия по колони, отгоре",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Стандарт, отдолу",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Змия по редове, отдолу",
    "logging_console": "конзола",
    "logging_file": "файл",
    "logging_both": "и двете",

    # --- Секции (Настройки) ---
    "section_processing_mode": " Режими на обработка ",
    "processing_mode_ram": "RAM (в паметта)",
    "processing_mode_hdd": "Диск (на съхранение)",
    "graphic_settings": "Графични настройки",
    "code_settings": "Настройки на QR/баркод",
    "logging_settings": "Настройки на логването",
    "barcode_text_position_label": "Позиция на текста към кода:",
    "barcode_text_bottom": "долу",
    "barcode_text_side": "странично",
    "barcode_text_none": "без текст",

    # --- Етикети (Настройки – Графика) ---
    "extra_margin_label": "Поле около панелите (см):",
    "margin_top_label": "Горно поле (см):",
    "margin_bottom_label": "Долно поле (см):",
    "margin_left_label": "Ляво поле (см):",
    "margin_right_label": "Дясно поле (см):",
    "reg_mark_width_label": "Рег. марка – ширина (см):",
    "reg_mark_height_label": "Рег. марка – височина (см):",
    "reg_mark_white_line_width_label": "Рег. марка – дебелина на бялата линия (см):",
    "reg_mark_black_line_width_label": "Рег. марка – дебелина на черната линия (см):",
    "sep_line_black_width_label": "Разделител – дебелина на черната линия (см):",
    "sep_line_white_width_label": "Разделител – дебелина на бялата линия (см):",
    "slice_gap_label": "Разстояние между панелите (см):",
    "label_draw_slice_border": "Рисувай рамка около панела (линия на рязане)",

    # --- Етикети (Настройки – Кодове) ---
    "scale_label": "Размер (см):",
    "scale_x_label": "Ширина X (см):",
    "scale_y_label": "Височина Y (см):",
    "offset_x_label": "Отместване X (см):",
    "offset_y_label": "Отместване Y (см):",
    "rotation_label": "Завъртане (°):",
    "anchor_label": "Ъгъл:",

    # --- Етикети (Настройки – Логове) ---
    "logging_mode_label": "Режим на логване:",
    "log_file_label": "Файл за лог:",
    "logging_level_label": "Ниво на логване:",

    # --- Бутони / действия (Начало) ---
    "button_load": "Зареди",
    "button_save_settings": "Запази текущите настройки",
    "button_generate_pdf": "Генерирай PDF",
    "button_refresh_preview": "Опресни прегледа",
    "button_refresh_layout": "Опресни оформлението",

    # --- Лиценз (GUI) ---
    "hwid_frame_title": "Уникален хардуерен идентификатор (HWID)",
    "copy_hwid": "Копирай HWID",
    "license_frame_title": "Активиране на лиценз",
    "enter_license_key": "Въведете лицензен ключ:",
    "activate": "Активирай",
    "status_trial": "Пробен режим",
    "license_active": "Лицензът е активен",

    # ================================================
    #  Съобщения към потребителя (диалози, статус)
    # ================================================

    # --- Профили ---
    "msg_no_profile_name": "Без име",
    "msg_enter_profile_name": "Въведете име на профил за запазване.",
    "msg_profile_saved": "Профилът е запазен",
    "profile_saved_title": "Профилът е запазен",
    "msg_profile_saved_detail": "Профил „{0}“ е запазен.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Профилът '{profile}' е запазен и приложен.",
    "msg_no_profile": "Няма профил",
    "warning_no_profile": "Няма профил",
    "msg_select_profile": "Изберете име на профил от списъка за зареждане.",
    "select_profile": "Изберете име на профил от списъка за зареждане.",
    "profile_loaded_title": "Профилът е зареден",
    "profile_loaded": "Профил „{profile}“ е зареден.",
    "warning_no_profile_delete": "Няма профил",
    "warning_no_profile_delete_message": "Изберете профил от списъка за изтриване.",
    "profile_not_found": "Профил „{profile}“ не е намерен.",
    "profile_not_exist": "Профил „{profile}“ не съществува.",
    "confirm_delete_title": "Потвърдете изтриването",
    "confirm_delete_profile": "Наистина ли искате да изтриете профил „{profile}“?",
    "profile_deleted_title": "Профилът е изтрит",
    "profile_deleted": "Профил „{profile}“ е изтрит.",

    # --- Файлове / директории ---
    "msg_no_input_file": "Няма входен файл",
    "msg_unsupported_format": "Неподдържан формат",
    "select_file_title": "Избор на входен файл",
    "supported_files": "Поддържани файлове",
    "all_files": "Всички файлове",
    "select_dir_title": "Избор на изходна папка",
    "select_log_dir_title": "Избор на папка за логове",
    "error_output_dir_title": "Грешка в изходната папка",
    "error_output_dir": "Посочената изходна папка е невалидна или не съществува:\n{directory}",
    "error_input_file_title": "Грешка във входния файл",
    "error_input_file": "Посоченият входен файл е невалиден или не съществува:\n{file}",
    "save_file_error_title": "Грешка при запис на файл",
    "save_file_error": "Файлът не може да бъде записан: {error}",

    # --- Обработка на PDF / преглед ---
    "msg_pdf_processing_error": "Неуспешна обработка на PDF файла",
    "msg_thumbnail_error": "Грешка при зареждане на миниатюра",
    "msg_no_pdf_output": "Няма PDF изход",
    "no_pdf_pages": "PDF не съдържа страници",
    "unsupported_output": "Неподдържан тип изход за преглед",
    "pdf_generated_title": "Генерирането приключи",
    "pdf_generated": "PDF файл(ове) бяха успешно генерирани в папка:\n{directory}",
    "pdf_generation_error_title": "Грешка при генериране",
    "pdf_generation_error": "Възникнаха грешки при генериране на PDF. Проверете логовете.",
    "critical_pdf_error_title": "Критична грешка при генериране на PDF",
    "critical_pdf_error": "Възникна критична грешка при генериране на PDF:\n{error}\nВижте логовете.",
    "settings_saved_title": "Настройките са записани",
    "settings_saved": "Настройките са записани във файл:\n{filepath}",
    "settings_save_error_title": "Грешка при запис на настройки",
    "settings_save_error": "Настройките не могат да бъдат записани: {error}",
    "conversion_error_title": "Грешка при конвертиране",
    "conversion_error": "Грешка при конвертиране на стойности от интерфейса: {error}",
    "update_gui_error_title": "Грешка при обновяване на интерфейса",
    "update_gui_error": "Възникна грешка при обновяване на интерфейса: {error}",

    # --- Лиценз ---
    "hwid_copied_to_clipboard": "HWID е копиран в клипборда",
    "computer_hwid": "HWID на компютъра",
    "public_key_load_error": "Грешка при зареждане на публичен ключ: {error}",
    "invalid_license_format": "Невалиден формат на лицензен ключ: {error}",
    "activation_success": "Лицензът е успешно активиран.",
    "activation_error": "Грешка при активиране на лиценз: {error}",
    "log_trial_mode_active": "Пробният режим е активен",
    "log_trial_mode_inactive": "Пробният режим не е активен",

    # --- Инициализация ---
    "init_error_title": "Грешка при инициализация",
    "init_error": "Грешка при инициализация на директориите: {error}",
    "poppler_path_info": "Информация за пътя до Poppler",
    "ttkthemes_not_installed": "Забележка: библиотеката ttkthemes не е инсталирана. Ще се използва стандартният стил на Tkinter.",

    # =====================================
    #  Логове (съобщения на logger-а)
    # =====================================

    # --- Общи / Конфигурация ---
    "log_configured": "Логването е конфигурирано: ниво={0}, режим={1}, файл={2}",
    "log_no_handlers": "Внимание: обработчици на логове не са конфигурирани (режим: {0}).",
    "log_critical_error": "Критична грешка при конфигуриране на логването: {0}",
    "log_basic_config": "Поради грешка е използвана базова конфигурация на логването.",
    "log_dir_create_error": "Критична грешка: не може да се създаде папка за логове {0}: {1}",

    # --- Логове – Инициализация / Директории (init_directories.py) ---
    "error_critical_init": "КРИТИЧНА ГРЕШКА по време на инициализация: {0}",
    "logger_init_error": "Грешка при инициализация на директориите: {error}",
    "directory_created": "Създадена директория: {0}",
    "directory_creation_error": "Не може да се създаде директория {0}: {1}",
    "sample_file_copied": "Образец файл копиран в {0}",
    "sample_file_copy_error": "Грешка при копиране на образец файл: {0}",
    "log_created_output_dir": "Създадена изходна папка: {0}",
    "log_cannot_create_output_dir": "Не може да се създаде изходна папка {0}: {1}",

    # --- Логове – Splitter (splitter.py) ---
    "log_graphic_settings_error": "Неуспешно зареждане на графични настройки при инициализация: {0}",
    "log_loading_pdf": "Зареждане на PDF файл: {0}",
    "log_loading_bitmap": "Зареждане на растерен файл: {0}",
    "log_invalid_dpi": "Прочетено е невалидно DPI ({0}). Използва се по подразбиране {1} DPI.",
    "log_image_dimensions": "Размери на изображението: {0}×{1}px, режим: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Обработка в оригинален цветови режим: {0}",
    "log_unusual_color_mode": "Нетипичен цветови режим: „{0}“. ReportLab/Pillow може да не работят коректно.",
    "log_draw_image_error": "Грешка ReportLab drawImage за режим {0}: {1}",
    "log_unsupported_format": "Неподдържан входен формат: {0}",
    "log_input_file_not_found": "Входният файл не е намерен: {0}",
    "log_load_process_error": "Грешка при зареждане или обработка на файл {0}: {1}",
    "log_input_file_not_exists": "Входният файл не съществува или пътят е празен: „{0}“",
    "log_cannot_load_or_empty_pdf": "Не може да се зареди входният файл или PDF е празен/повреден.",
    "log_pdf_dimensions_info": "  PDF размери: {0:.1f} мм × {1:.1f} мм",
    "log_invalid_pdf_dimensions": "Невалидни размери на PDF страница: {0}×{1} pt.",

    #   Splitter – Изчисляване на размери
    "log_extra_margin": "Допълнително поле зададено на {0:.3f} pt",
    "log_invalid_rows_cols": "Невалиден брой редове ({0}) или колони ({1}).",
    "error_invalid_rows_cols": "Редовете и колоните трябва да са положителни цели числа.",
    "log_invalid_overlap_white_stripe": "Невалидни стойности за припокриване ({0}) или бяла лента ({1}). Трябва да са числови.",
    "error_invalid_overlap_white_stripe": "Припокриването и бялата лента трябва да са числови стойности (мм).",
    "log_stripe_usage": "Зададено use_white_stripe={0}, white_stripe={1:.3f} мм",
    "log_effective_overlap": "Базово припокриване (графика): {0:.3f} мм, бяла лента: {1:.3f} мм, ефективно припокриване: {2:.3f} мм",
    "log_computed_dimensions": "Изчислено: PDF {0:.3f}×{1:.3f} мм. Панел: {2:.3f} pt ({3:.3f} мм) × {4:.3f} pt ({5:.3f} мм). Ядро: {6:.3f}×{7:.3f} pt. Ефект. припокриване: {8:.3f} мм",
    "log_invalid_dimensions": "Невалидни размери на панела ({0:.3f}×{1:.3f}) или ядрото ({2:.3f}×{3:.3f}) при per={4}, лента={5}, r={6}, c={7}, W={8} мм, H={9} мм",
    "error_invalid_slice_dimensions": "Изчислените размери на панела/ядрото са невалидни или отрицателни.",

    #   Splitter – Информация за панели и ред
    "log_generating_slice_info": "Генериране на информация за панел: {0}",
    "log_no_slices_info_generated": "Неуспешно генериране на информация за панелите.",
    "log_applying_rotated_order": "Прилагане на ред за ротация 180°: {0}",
    "log_applying_standard_order": "Прилагане на стандартен ред (0°): {0}",
    "log_unknown_bryt_order": "Непознат ред на панелите: „{0}“. Използва се по подразбиране.",
    "log_final_slices_order": "  Краен ред на панелите ({0}): [{1}]",

    #   Splitter – Overlays и сливане
    "log_invalid_dimensions_overlay": "Опит за създаване на overlay с невалидни размери: {0}. Пропуска се.",
    "log_empty_overlay": "Създаден празен или почти празен overlay PDF. Сливането се пропуска.",
    "log_overlay_error": "Грешка при създаване на overlay PDF: {0}",
    "log_merge_error": "Опит за сливане на overlay без страници. Пропуска се.",
    "log_merge_page_error": "Грешка при сливане на overlay PDF: {0}",
    "log_fallback_draw_rotating_elements": "Неуспешно извличане на редове/колони за _draw_rotating_elements, използва се 1×1.",
    "log_overlay_created_for_slice": "Overlay за ленти/марки е създаден за панел {0}",
    "log_overlay_creation_failed_for_slice": "Неуспешно създаване на overlay за {0}",
    "log_merging_rotated_overlay": "Сливане на РОТИРАН overlay за {0} с T={1}",
    "log_merging_nonrotated_overlay": "Сливане на НЕРОТИРАН overlay за {0}",
    "log_merging_all_codes_overlay": "Сливане на overlay с всички кодове (без ротация)",
    "log_merging_separation_lines_overlay": "Сливане на overlay с разделителни линии (без ротация)",
    "log_merging_code_overlay_for_slice": "Overlay с код за {0} е слят без ротация.",
    "log_merging_separation_overlay_for_slice": "Overlay с разделителни линии за {0} е слят без ротация.",

    #   Splitter – Рисуване (ленти, марки, линии)
    "log_drawing_top_stripe": "[Canvas] Рисувам горна лента за {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Рисувам дясна лента за {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Запълвам и очертавам ъгъл за {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Рисувам кръст с център в ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Рисувам регистрационни линии за {0} в област от ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Рисувам дясна вертикална линия: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Рисувам горна хоризонтална линия: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Рисувам разделителна линия (бяло върху черно): ({0}) @ ({1:.3f}, {2:.3f}), дължина={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Рисувам кръстове за {0} [{1},{2}] / [{3},{4}] в област от ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Изчислени центрове: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Рисувам TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Рисувам TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Рисувам BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Рисувам BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Пропускам {0} според правилото за позиция [{1},{2}]",
    "log_trial_common_sheet": "Добавям воден знак TRIAL към общия лист",

    # Воден знак
    "log_trial_watermark_added": "Добавен е воден знак TRIAL",
    "error_drawing_trial_text": "Грешка при рисуване на водния знак: {error}",

    #   Splitter – Разделителни линии (цяла страница)
    "log_drawing_separation_lines_for_page": "Рисувам разделителни линии за страницата (оформление={0}, панели={1}, индекс={2})",
    "log_vertical_line_between_slices": "  Вертикална линия между панели {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Начало на вертикална линия @ x={0:.1f}",
    "log_vertical_line_end": "  Край на вертикална линия @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Хоризонтална линия между панели {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Начало на хоризонтална линия @ y={0:.1f}",
    "log_horizontal_line_end": "  Край на хоризонтална линия @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Отделни_файлове) Старт верт./хориз. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Отделни_файлове) Край верт./хориз. @ {0:.1f}",

    #   Splitter – Генериране на кодове / QR
    "log_generate_barcode_data": "Генерирам данни за код: {0}",
    "log_barcode_data_shortened": "Данните за кода са съкратени до {0} знака.",
    "log_barcode_data_error": "Грешка при генериране на данни за код: {0}",
    "log_compose_barcode_payload": "Съставям payload за кода ({0}): {1}",
    "log_barcode_payload_shortened": "Payload е съкратен до {0} знака за формат {1}",
    "log_barcode_payload_error": "Грешка при съставяне на payload: {0}",
    "log_unknown_anchor_fallback": "Непознат котвен ъгъл „{0}“, използва се долен ляв",
    "log_used_default_code_settings": "Използвани са „default“ настройки за кода {0}/{1}.",
    "log_no_layout_key_fallback": "Няма оформление „{0}“ за {1}/{2}. Използван е първият наличен: „{3}“.",
    "log_code_settings_error": "Липсващи/грешни настройки на кода ({0}/{1}/{2}): {3}. Използвани са стойности по подразбиране.",
    "log_drawing_barcode": "Рисувам {0} при ({1:.3f}, {2:.3f}) [база ({3:.3f}, {4:.3f}) + отместване ({5:.3f}, {6:.3f})], ротация: {7}°",
    "error_generate_qr_svg": "Неуспешно генериране на SVG за QR код.",
    "error_invalid_scale_for_qr": "Невалиден размер на QR: {0} мм",
    "error_invalid_qr_scale_factor": "Невалиден мащабен фактор за QR: {0}",
    "error_generate_barcode_svg": "Неуспешно генериране на SVG за баркод.",
    "error_invalid_scale_for_barcode": "Невалиден размер на баркод: {0}×{1} мм",
    "error_invalid_barcode_scale_factor": "Невалиден мащабен фактор за баркод: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: размер в конфигурацията={1:.3f} мм, SVG ширина={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: размер в конфигурацията=({1:.3f} мм, {2:.3f} мм), SVG размер=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Грешка при рисуване на код „{0}“: {1}",
    "log_prepared_barcode_info": "Подготвена информация за код за {0} ({1}, ъгъл={2}): базова абсолютна позиция ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Грешка при подготовка на данни за кода {0}: {1}",
    "log_drawing_barcodes_count": "Рисувам {0} кода/QR...",
    "log_missing_barcode_info_key": "Липсващ ключ в информацията за кода по време на рисуване: {0}. Инфо: {1}",
    "log_error_drawing_barcode_in_draw_all": "Грешка при рисуване на код „{0}“ в _draw_all_barcodes: {1}",

    #   Splitter – Процес на рязане (методи split_*)
    "log_start_splitting_process": "--- Стартиране на процеса по рязане за: {0} ---",
    "log_split_settings": "  Настройки: {0}×{1} панела, припокриване={2} мм, бяла лента={3} мм (+припокриване: {4})",
    "log_output_dir_info": "  Изход: {0} / {1} в „{2}“",
    "log_lines_marks_barcodes_info": "  Линии: разделителни={0}, начало={1}, край={2} | Марки: {3} ({4}), Кодове: {5} ({6})",
    "log_bryt_order_info": "  Ред: {0}, ротация на панелите: {1}°",
    "log_invalid_dimensions_in_slice_info": "Невалидни размери в slice_info за {0}: {1}×{2}",
    "log_content_transform": "Трансформация на съдържанието T_content за {0}: {1}",
    "log_merged_content_for_slice": "Съдържание е слято за панел {0} в new_page",
    "log_slice_reader_created": "Създаден е пълен панел (PdfReader) за {0}",
    "log_slice_reader_creation_error": "Грешка при създаване на пълен панел за {0}: {1}",
    "log_used_get_transform": "Използван _get_transform (само преместване): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Старт: ОТДЕЛНИ ФАЙЛОВЕ (ротация в create_slice_reader) ---",
    "log_creating_file_for_slice": "Създавам файл за панел {0}: {1}",
    "log_invalid_page_size_for_slice": "Невалиден размер на страница ({0}×{1}) за {2}. Пропуска се.",
    "log_blank_page_creation_error": "Грешка при създаване на празна страница за {0} (размер {1}×{2}): {3}. Пропуска се.",
    "log_transform_for_slice": "Трансформация T (само преместване) за {0}: {1}",
    "log_merging_complete_slice": "Сливане на пълен панел {0} с трансформация: {1}",
    "log_skipped_slice_merging": "Сливането на пълен панел за {0} е пропуснато.",
    "log_file_saved": "Файлът е записан: {0}",
    "log_file_save_error": "Грешка при запис на файл {0}: {1}",
    "log_finished_split_separate_files": "--- Завършено: ОТДЕЛНИ ФАЙЛОВЕ (запазени {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Няма панели за обработка в split_horizontal.",
    "log_start_split_horizontal": "--- Старт: ОБЩ ЛИСТ – ХОРИЗОНТАЛНО (ротация в create_slice_reader) ---",
    "log_page_dimensions": "Размери на страница: {0:.1f}×{1:.1f} мм ({2} панела)",
    "log_page_creation_error": "Грешка при създаване на изходна страница ({0}×{1}): {2}. Прекратяване.",
    "log_slice_at_position": "Панел {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Трансформация T (само преместване) за {0}: {1}",
    "log_merging_complete_bryt": "Сливане на пълен панел {0} с трансформация: {1}",
    "log_skipped_merging_bryt": "Сливането на пълен панел за {0} е пропуснато.",
    "log_file_result_saved": "Резултатният файл е записан: {0}",
    "log_file_result_save_error": "Грешка при запис на резултатен файл {0}: {1}",
    "log_finished_split_horizontal": "--- Завършено: ОБЩ ЛИСТ – ХОРИЗОНТАЛНО ---",
    "log_no_slices_split_vertical": "Няма панели за обработка в split_vertical.",
    "log_start_split_vertical": "--- Старт: ОБЩ ЛИСТ – ВЕРТИКАЛНО (ротация в create_slice_reader) ---",
    "log_finished_split_vertical": "--- Завършено: ОБЩ ЛИСТ – ВЕРТИКАЛНО ---",
    "log_unknown_layout": "Непознато оформление за общ лист: „{0}“.",
    "log_unknown_output_type": "Непознат тип изход: „{0}“.",
    "log_finished_splitting_success": "--- Процесът на рязане завърши за: {0} — УСПЕХ ---",
    "log_finished_splitting_errors": "--- Процесът на рязане завърши за: {0} — ИМА ГРЕШКИ ---",
    "log_value_error_in_splitting": "Грешка във вход или изчисления: {0}",
    "log_finished_splitting_critical_error": "--- Процесът на рязане завърши за: {0} — КРИТИЧНА ГРЕШКА ---",
    "log_unexpected_error_in_splitting": "Неочаквана грешка при рязане на файл {0}: {1}",

    #   Splitter – Тестов режим (__main__)
    "log_script_mode_test": "splitter.py е стартиран като основен скрипт (тестов режим).",
    "log_loaded_config": "Конфигурацията е заредена.",
    "log_error_loading_config": "Неуспешно зареждане на конфигурация: {0}",
    "log_created_example_pdf": "Създаден е примерен PDF: {0}",
    "log_cannot_create_example_pdf": "Неуспешно създаване на примерен PDF: {0}",
    "log_start_test_split": "Стартирам тестово рязане за файл: {0} → {1}",
    "log_test_split_success": "Тестовото рязане приключи успешно.",
    "log_test_split_errors": "Тестовото рязане приключи с грешки.",

    # --- Логове – QR/баркод (barcode_qr.py) ---
    "log_qr_empty_data": "Опит за генериране на QR код за празни данни.",
    "log_qr_generated": "SVG за QR код е генериран за: {0}...",
    "log_qr_error": "Грешка при генериране на QR за данни „{0}“: {1}",
    "log_barcode_empty_data": "Опит за генериране на баркод за празни данни.",
    "log_barcode_generated": "SVG за баркод е генериран за: {0}...",
    "log_barcode_error": "Грешка при генериране на баркод за „{0}“: {1}",
    "log_basic_handler_configured": "Базов обработчик е конфигуриран за logger в barcode_qr.py",
    "log_basic_handler_error": "Грешка при конфигурация на базов обработчик в barcode_qr: {0}",

    # --- Логове – Конфигурация/Профили (main_config_manager.py) ---
    "loading_profiles_from": "Зареждане на профили от",
    "profiles_file": "Файл с профили",
    "does_not_contain_dict": "не съдържа речник. Създава се нов",
    "not_found_creating_new": "не е намерен. Създава се нов празен",
    "json_profiles_read_error": "Грешка при четене на JSON на профилите",
    "file_will_be_overwritten": "Файлът ще бъде презаписан при запис",
    "json_decode_error_in_profiles": "Грешка при декодиране на JSON в файла с профили",
    "cannot_load_profiles_file": "Файлът с профили не може да бъде зареден",
    "unexpected_profiles_read_error": "Неочаквана грешка при четене на профили",
    "saving_profiles_to": "Запис на профили в",
    "cannot_save_profiles_file": "Файлът с профили не може да бъде записан",
    "profiles_save_error": "Грешка при запис на профили във файл",
    "logger_profile_saved": "Профилът е запазен: {profile}",
    "logger_profile_not_found": "Профил за зареждане не е намерен: {profile}",
    "logger_profile_loaded": "Профилът е зареден: {profile}",
    "logger_profile_delete_not_exist": "Опит за изтриване на несъществуващ профил: {profile}",
    "logger_profile_deleted": "Профилът е изтрит: {profile}",
    "logger_start_save_settings": "Стартирано е записване на настройки от GUI.",
    "logger_invalid_value": "Невалидна стойност за „{key}“. Зададена е 0.0.",
    "logger_end_save_settings": "Записването на настройки от GUI приключи.",
    "logger_conversion_error": "Грешка при конвертиране на стойности от GUI: {error}",
    "conversion_failed": "Неуспешно конвертиране на стойности от GUI",
    "logger_unexpected_save_error": "Неочаквана грешка при запис на настройки: {error}",
    "logger_settings_saved": "Настройките са записани във файл: {file}",

    # --- Логове – Лицензиране (main_license.py) ---
    "public_key_load_error_log": "Грешка при зареждане на публичен ключ",
    "license_key_decode_error": "Грешка при декодиране на лицензен ключ",
    "license_activation_error": "Грешка при активиране на лиценз",

    # --- Логове – Основен модул (main.py) ---
    "ui_created": "Потребителският интерфейс е създаден.",
    "error_tab_home": "Грешка при създаване на изглед „Начало“",
    "error_tab_settings": "Грешка при създаване на изглед „Настройки“",
    "error_tab_help": "Грешка при създаване на изглед „Помощ“",
    "error_creating_license_ui": "Грешка при създаване на изглед „Лиценз“",
    "error_loading_ui": "Обща грешка при зареждане на интерфейса: {error}",
    "error_creating_home_ui": "Грешка при създаване на изглед „Начало“",
    "error_creating_settings_ui": "Грешка при създаване на изглед „Настройки“",
    "error_creating_help_ui": "Грешка при създаване на изглед „Помощ“",
    "logger_update_gui": "Стартирано е обновяване на GUI от конфигурация.",
    "logger_end_update_gui": "Обновяването на GUI от конфигурация приключи.",
    "logger_update_gui_error": "Неочаквана грешка при обновяване на GUI: {error}",
    "logger_invalid_output_dir": "Невалидна или липсваща изходна папка: {directory}",
    "logger_invalid_input_file": "Невалиден или липсващ входен файл: {file}",
    "logger_start_pdf": "Стартиран е процесът по генериране на PDF.",
    "logger_pdf_save_error": "Генерирането на PDF е прекъснато: записът на текущите настройки се провали.",
    "logger_pdf_success": "Генерирането на PDF завърши успешно.",
    "logger_pdf_exception": "Изключение в основния процес на генериране на PDF.",
    "icon_set_error": "Грешка при задаване на икона на приложението: {error}",
    "accent_button_style_error": "Грешка при задаване стил на акцентен бутон: {error}",
    "logger_file_save_error": "Грешка при запис на файл {file}: {error}",

    #   Логове – Преглед (main.py – update_preview, update_output_preview)
    "thumbnail_error_log": "Грешка при генериране на миниатюра",
    "output_preview_update_called": "Извикано е обновяване на прегледа на изхода",
    "output_preview_canvas_missing": "Липсва canvas за преглед на изхода",
    "pdf_found_in_output_dir": "Открит е PDF в изходната папка",
    "preparing_thumbnail": "Подготовка на миниатюра",
    "thumbnail_generated_successfully": "Миниатюрата е генерирана успешно",
    "thumbnail_generation_error": "Грешка при генериране на миниатюра за",
    "no_pdf_for_common_sheet": "Няма PDF за преглед на общия лист",
    "no_pdf_for_separate_files": "Няма генерирани PDF файлове за преглед",
    "cannot_load_thumbnail": "Миниатюрата не може да бъде заредена от",

    #   Логове – Вътрешни за разработка (main.py)
    "missing_gui_var_created": "Създадена липсваща GUI променлива за ключ: {key}",
    "missing_gui_structure_created": "Създадена липсваща GUI структура за: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Създадена липсваща GUI променлива за: {code_type}/{output_type}/{layout}/{param}",

    # Допълнителен текст за main_ui_help.py
    "help_text": """
    Billboard Splitter – Ръководство за потребителя\n\n
    Цел на програмата:\n
    Billboard Splitter автоматично разделя проекти за билборд на панели, готови за печат.
    Програмата е предназначена за работа с файлове в мащаб 1:10.\n
    Стойностите в секциите: Припокриване, Бяла лента и Настройки се въвеждат в мащаб 1:1.
    Програмата може да подрежда изрязаните панели в PDF според избраното оформление:\n
    • Общ лист: всички панели в един документ.\n
    • Отделни файлове: всеки панел в отделен PDF.\n\n
    Допълнително програмата позволява:\n
    • Избор на оформление – вертикално или хоризонтално (при вертикално разделителните линии са горе и долу,
      при хоризонтално – вляво и вдясно).\n
    • Завъртане на панелите на 180° (инверсия на целия проект).\n
    • Добавяне на регистрационни марки (кръст или линия) за точно позициониране при лепене.\n
    • Добавяне на QR кодове или баркодове – генерирани от входните данни за идентификация на панелите.\n
    • Запазване на настройките като профили, които могат да се зареждат, редактират и изтриват – бърза смяна между проекти.\n\n
    Основни стъпки:\n\n
    1. Избор на входен файл:\n
    • В раздел „Начало“ изберете PDF, JPG или TIFF с дизайна на билборда.\n
    • Ако не е зададен собствен път, се използва примерен файл по подразбиране.\n\n
    2. Настройки на рязане:\n
    • Въведете броя редове и колони, на които се разделя проектът.\n
    • Задайте размера на припокриването.\n
    • По желание задайте ширина на бялата лента, която се добавя към ефективното припокриване.\n\n
    3. Оформление на изхода:\n
    • Вертикално: панелите се подреждат вертикално на PDF страницата.\n
    • Хоризонтално: панелите се подреждат хоризонтално.\n\n
    4. Тип изход:\n
    • Общ лист – един PDF.\n
    • Отделни файлове – по един PDF за панел.\n
    • В „Начало“ можете да включите и настроите регистрационните марки – кръст или линия.\n
    • По желание включете QR или баркод – генерира се от данните на проекта.\n
    • Параметрите на кода (мащаб, отместване, ротация, позиция) се настройват в раздел „Настройки“.\n\n
    5. Управление на конфигурации:\n
    • В „Настройки“ прецизно се настройват графичните параметри (полета, дебелини на линии, разстояния) и кодовете.\n
    • Запазете текущата конфигурация като профил за по-нататъшно зареждане/редакция.\n
    • Профилите (profiles.json) позволяват бързо превключване между различни набори от настройки.\n\n
    6. Генериране на PDF:\n
    • Когато сте готови, натиснете „Генерирай PDF“.\n
    • Резултатите се записват в папка „output“ (или друга зададена), а логовете (с дневна ротация) – в „logs“.\n\n
    При проблеми:\n
    • Проверете логовете в папка „logs“. Всеки ден се създава нов лог файл с дата в името.\n
    • Уверете се, че всички необходими директории са дефинирани.\n
    • Поддръжка: tech@printworks.pl (делнични дни, 8–16)\n
    """
}
