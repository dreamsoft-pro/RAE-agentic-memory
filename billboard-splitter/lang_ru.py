# lang_ru.py
"""
Файл переводов для русского языка.
"""

LANG = {
    "barcode_font_size_label": "Размер шрифта описания штрих-кода [pt]:",
    # ==========================
    #  Приложение — Общее
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Ошибка",
    "no_file": "Нет файла",
    "language": "Язык",
    "language_switch": "Смена языка",
    "choose_language": "Выберите язык:",
    "apply_language": "Применить",
    "language_changed": "Язык был изменён. Часть изменений станет видна после перезапуска приложения.",

    # ========================================
    #  Элементы графического интерфейса (GUI)
    # ========================================

    # --- Основные вкладки ---
    "tab_home": " Главная ",
    "tab_settings": " Настройки ",
    "tab_help": " Справка ",
    "tab_license": " Лицензия ",

    # --- Общие кнопки ---
    "button_browse": "Обзор...",
    "browse_folder": "Обзор папки...",
    "button_save": "Сохранить",
    "button_delete": "Удалить",
    "button_close": "Закрыть",
    "save_all_settings": "Сохранить все настройки",

    # --- Подписи полей (вкладка Главная) ---
    "label_rows": "Вертикальное деление (строки):",
    "label_columns": "Горизонтальное деление (столбцы):",
    "label_overlap": "Перехлёст (см):",
    "label_white_stripe": "Белая полоса (см):",
    "label_add_white_stripe": "Добавить белую полосу к эффективному перехлёсту",
    "label_layout": "Схема выкладки:",
    "label_output_type": "Тип вывода:",
    "label_enable_reg_marks": "Включить метки совмещения:",
    "label_enable_codes": "Включить коды:",
    "label_enable_sep_lines": "Включить разделительные линии (между панелями)",
    "label_enable_start_line": "Включить линию начала/верх листа",
    "label_enable_end_line": "Включить линию конца/низ листа",
    "label_bryt_order": "Порядок панелей:",
    "label_slice_rotation": "Поворот панелей:",
    "label_create_order_folder": "Создавать папку с номером заказа",

    # --- Секции/группы (вкладка Главная) ---
    "section_input_file": " Входной файл ",
    "section_scale_and_dimensions": " Масштаб и выходные размеры ",
    "label_original_size": "Исходный размер:",
    "label_scale_non_uniform": "Непропорциональное масштабирование",
    "label_scale": "Масштаб: 1:",
    "label_scale_x": "Масштаб X: 1:",
    "label_scale_y": "Масштаб Y: 1:",
    "label_output_dimensions": "Размеры выходного файла:",
    "label_width_cm": "Ширина [см]:",
    "label_height_cm": "Высота [см]:",
    "section_split_settings": " Параметры резки ",
    "section_profiles": " Профили настроек ",
    "section_save_location": " Папка сохранения ",
    "section_input_preview": " Предпросмотр входного файла ",
    "section_output_preview": " Предпросмотр результата ",

    # --- Значения опций (combobox, radiobutton и т.п.) ---
    "layout_vertical": "Вертикальная",
    "layout_horizontal": "Горизонтальная",
    "output_common_sheet": "Общий лист",
    "output_separate_files": "Отдельные файлы",
    "output_both": "Общий лист и отдельные файлы",
    "output_common": "Общий лист",
    "output_separate": "Отдельные файлы",
    "reg_mark_cross": "Крест",
    "reg_mark_line": "Линия",
    "code_qr": "QR-код",
    "code_barcode": "Штрих-код",
    "bryt_order_1": "A1–An, B1–Bn, .. Стандарт, сверху",
    "bryt_order_2": "A1–An, Bn–B1, .. Змейкой по строкам, сверху",
    "bryt_order_3": "A1..B1, A2..B2, .. По столбцам, сверху",
    "bryt_order_4": "A1–A2..B2–B1.. Змейкой по столбцам, сверху",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n, .. Стандарт, снизу",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1, .. Змейкой по строкам, снизу",
    "logging_console": "консоль",
    "logging_file": "файл",
    "logging_both": "оба",

    # --- Секции/группы (вкладка Настройки) ---
    "section_processing_mode": " Режимы обработки ",
    "processing_mode_ram": "RAM (в памяти)",
    "processing_mode_hdd": "Диск (на носителе)",
    "graphic_settings": "Графические параметры",
    "code_settings": "Настройки QR / штрих-кода",
    "logging_settings": "Настройки журналирования (логов)",
    "barcode_text_position_label": "Положение подписи кода:",
    "barcode_text_bottom": "снизу",
    "barcode_text_side": "сбоку",
    "barcode_text_none": "нет",

    # --- Подписи (Настройки — Графика) ---
    "extra_margin_label": "Отступ вокруг панелей (см):",
    "margin_top_label": "Верхний отступ (см):",
    "margin_bottom_label": "Нижний отступ (см):",
    "margin_left_label": "Левый отступ (см):",
    "margin_right_label": "Правый отступ (см):",
    "reg_mark_width_label": "Метка совмещения — ширина (см):",
    "reg_mark_height_label": "Метка совмещения — высота (см):",
    "reg_mark_white_line_width_label": "Метка — толщина белой линии (см):",
    "reg_mark_black_line_width_label": "Метка — толщина чёрной линии (см):",
    "sep_line_black_width_label": "Разделительная — толщина чёрной линии (см):",
    "sep_line_white_width_label": "Разделительная — толщина белой линии (см):",
    "slice_gap_label": "Зазор между панелями (см):",
    "label_draw_slice_border": "Рисовать рамку вокруг панели (линия реза)",

    # --- Подписи (Настройки — Коды) ---
    "scale_label": "Размер (см):",
    "scale_x_label": "Ширина X (см):",
    "scale_y_label": "Высота Y (см):",
    "offset_x_label": "Смещение X (см):",
    "offset_y_label": "Смещение Y (см):",
    "rotation_label": "Поворот (°):",
    "anchor_label": "Угол:",

    # --- Подписи (Настройки — Логи) ---
    "logging_mode_label": "Режим логирования:",
    "log_file_label": "Файл лога:",
    "logging_level_label": "Уровень логирования:",

    # --- Кнопки / действия (вкладка Главная) ---
    "button_load": "Загрузить",
    "button_save_settings": "Сохранить текущие настройки",
    "button_generate_pdf": "Сгенерировать PDF",
    "button_refresh_preview": "Обновить предпросмотр",
    "button_refresh_layout": "Обновить выкладку",

    # --- Лицензия (GUI) ---
    "hwid_frame_title": "Уникальный идентификатор оборудования (HWID)",
    "copy_hwid": "Скопировать HWID",
    "license_frame_title": "Активация лицензии",
    "enter_license_key": "Введите лицензионный ключ:",
    "activate": "Активировать",
    "status_trial": "Пробный режим",
    "license_active": "Лицензия активна",

    # ================================================
    #  Сообщения пользователю (окна, строка состояния)
    # ================================================

    # --- Профили ---
    "msg_no_profile_name": "Нет названия",
    "msg_enter_profile_name": "Введите имя профиля для сохранения.",
    "msg_profile_saved": "Профиль сохранён",
    "profile_saved_title": "Профиль сохранён",
    "msg_profile_saved_detail": "Профиль «{0}» был сохранён.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Профиль '{profile}' сохранен и применен.",
    "msg_no_profile": "Нет профиля",
    "warning_no_profile": "Нет профиля",
    "msg_select_profile": "Выберите имя профиля в списке для загрузки.",
    "select_profile": "Выберите имя профиля в списке для загрузки.",
    "profile_loaded_title": "Профиль загружен",
    "profile_loaded": "Профиль «{profile}» был загружен.",
    "warning_no_profile_delete": "Нет профиля",
    "warning_no_profile_delete_message": "Выберите профиль в списке для удаления.",
    "profile_not_found": "Профиль «{profile}» не найден.",
    "profile_not_exist": "Профиль «{profile}» не существует.",
    "confirm_delete_title": "Подтвердите удаление",
    "confirm_delete_profile": "Вы действительно хотите удалить профиль «{profile}»?",
    "profile_deleted_title": "Профиль удалён",
    "profile_deleted": "Профиль «{profile}» был удалён.",

    # --- Файлы / каталоги ---
    "msg_no_input_file": "Нет входного файла",
    "msg_unsupported_format": "Неподдерживаемый формат",
    "select_file_title": "Выбор входного файла",
    "supported_files": "Поддерживаемые файлы",
    "all_files": "Все файлы",
    "select_dir_title": "Выбор выходной папки",
    "select_log_dir_title": "Выбор папки для логов",
    "error_output_dir_title": "Ошибка выходной папки",
    "error_output_dir": "Указанная выходная папка некорректна или не существует:\n{directory}",
    "error_input_file_title": "Ошибка входного файла",
    "error_input_file": "Указанный входной файл некорректен или не существует:\n{file}",
    "save_file_error_title": "Ошибка сохранения файла",
    "save_file_error": "Не удалось сохранить файл: {error}",

    # --- Обработка PDF / предпросмотр ---
    "msg_pdf_processing_error": "Сбой обработки PDF-файла",
    "msg_thumbnail_error": "Ошибка загрузки миниатюры",
    "msg_no_pdf_output": "Нет PDF-вывода",
    "no_pdf_pages": "В PDF нет страниц",
    "unsupported_output": "Неподдерживаемый тип вывода для предпросмотра",
    "pdf_generated_title": "Генерация завершена",
    "pdf_generated": "PDF-файл(ы) успешно сгенерированы в папке:\n{directory}",
    "pdf_generation_error_title": "Ошибка генерации",
    "pdf_generation_error": "Во время генерации PDF возникли ошибки. Проверьте логи.",
    "critical_pdf_error_title": "Критическая ошибка генерации PDF",
    "critical_pdf_error": "Произошла критическая ошибка при генерации PDF:\n{error}\nСм. журналы.",
    "settings_saved_title": "Настройки сохранены",
    "settings_saved": "Настройки сохранены в файле:\n{filepath}",
    "settings_save_error_title": "Ошибка сохранения настроек",
    "settings_save_error": "Не удалось сохранить настройки: {error}",
    "conversion_error_title": "Ошибка преобразования",
    "conversion_error": "Ошибка преобразования значений из интерфейса: {error}",
    "update_gui_error_title": "Ошибка обновления интерфейса",
    "update_gui_error": "Произошла ошибка при обновлении интерфейса: {error}",

    # --- Лицензия ---
    "hwid_copied_to_clipboard": "HWID скопирован в буфер обмена",
    "computer_hwid": "HWID компьютера",
    "public_key_load_error": "Ошибка загрузки открытого ключа: {error}",
    "invalid_license_format": "Недопустимый формат лицензионного ключа: {error}",
    "activation_success": "Лицензия успешно активирована.",
    "activation_error": "Ошибка активации лицензии: {error}",
    "log_trial_mode_active": "Пробный режим активен",
    "log_trial_mode_inactive": "Пробный режим не активен",

    # --- Инициализация ---
    "init_error_title": "Ошибка инициализации",
    "init_error": "Ошибка инициализации каталогов: {error}",
    "poppler_path_info": "Информация о пути Poppler",
    "ttkthemes_not_installed": "Внимание: библиотека ttkthemes не установлена. Будет использован стандартный стиль Tkinter.",

    # =====================================
    #  Логи (сообщения логгера)
    # =====================================

    # --- Общее / Настройка ---
    "log_configured": "Логирование настроено: уровень={0}, режим={1}, файл={2}",
    "log_no_handlers": "Внимание: обработчики логов не настроены (режим: {0}).",
    "log_critical_error": "Критическая ошибка конфигурации логирования: {0}",
    "log_basic_config": "Из-за ошибки использована базовая конфигурация логирования.",
    "log_dir_create_error": "Критическая ошибка: невозможно создать папку логов {0}: {1}",

    # --- Логи — Инициализация / Каталоги (init_directories.py) ---
    "error_critical_init": "КРИТИЧЕСКАЯ ОШИБКА во время инициализации: {0}",
    "logger_init_error": "Ошибка инициализации каталогов: {error}",
    "directory_created": "Каталог создан: {0}",
    "directory_creation_error": "Не удалось создать каталог {0}: {1}",
    "sample_file_copied": "Файл примера скопирован в {0}",
    "sample_file_copy_error": "Ошибка копирования файла примера: {0}",
    "log_created_output_dir": "Создана выходная папка: {0}",
    "log_cannot_create_output_dir": "Не удаётся создать выходную папку {0}: {1}",

    # --- Логи — Splitter (splitter.py) ---
    "log_graphic_settings_error": "Сбой загрузки графических настроек при инициализации: {0}",
    "log_loading_pdf": "Загрузка PDF-файла: {0}",
    "log_loading_bitmap": "Загрузка растрового файла: {0}",
    "log_invalid_dpi": "Считано недопустимое DPI ({0}). Используется значение по умолчанию {1} DPI.",
    "log_image_dimensions": "Размеры изображения: {0}×{1}px, режим: {2}, DPI: {3:.1f} → {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Обработка изображения с исходным цветовым режимом: {0}",
    "log_unusual_color_mode": "Необычный цветовой режим: «{0}». ReportLab/Pillow могут работать некорректно.",
    "log_draw_image_error": "Ошибка ReportLab drawImage для режима {0}: {1}",
    "log_unsupported_format": "Неподдерживаемый входной формат: {0}",
    "log_input_file_not_found": "Входной файл не найден: {0}",
    "log_load_process_error": "Ошибка загрузки или обработки файла {0}: {1}",
    "log_input_file_not_exists": "Входного файла не существует или путь пуст: «{0}»",
    "log_cannot_load_or_empty_pdf": "Не удалось загрузить входной файл, либо PDF пуст/повреждён.",
    "log_pdf_dimensions_info": "  Размеры PDF: {0:.1f} мм × {1:.1f} мм",
    "log_invalid_pdf_dimensions": "Недопустимые размеры страницы PDF: {0}×{1} pt.",

    #   Splitter — Расчёт размеров
    "log_extra_margin": "Доп. отступ установлен: {0:.3f} pt",
    "log_invalid_rows_cols": "Недопустимое число строк ({0}) или столбцов ({1}).",
    "error_invalid_rows_cols": "Строки и столбцы должны быть положительными целыми.",
    "log_invalid_overlap_white_stripe": "Недопустимые значения перехлёста ({0}) или белой полосы ({1}). Должны быть числовыми.",
    "error_invalid_overlap_white_stripe": "Перехлёст и белая полоса должны быть числовыми значениями (мм).",
    "log_stripe_usage": "Установлено use_white_stripe={0}, white_stripe={1:.3f} мм",
    "log_effective_overlap": "Базовый перехлёст (графика): {0:.3f} мм, белая полоса: {1:.3f} мм, эффективный перехлёст: {2:.3f} мм",
    "log_computed_dimensions": "Вычислено: PDF {0:.3f}×{1:.3f} мм. Панель: {2:.3f} pt ({3:.3f} мм) × {4:.3f} pt ({5:.3f} мм). Ядро: {6:.3f}×{7:.3f} pt. Эфф. перехлёст: {8:.3f} мм",
    "log_invalid_dimensions": "Недопустимые размеры панели ({0:.3f}×{1:.3f}) или ядра ({2:.3f}×{3:.3f}) при per={4}, stripe={5}, r={6}, c={7}, W={8} мм, H={9} мм",
    "error_invalid_slice_dimensions": "Вычисленные размеры панели/ядра недопустимы или отрицательны.",

    #   Splitter — Генерация информации и порядка панелей
    "log_generating_slice_info": "Генерация информации о панели: {0}",
    "log_no_slices_info_generated": "Не удалось сгенерировать информацию о панелях.",
    "log_applying_rotated_order": "Применение порядка для поворота на 180°: {0}",
    "log_applying_standard_order": "Применение порядка для 0° (стандарт): {0}",
    "log_unknown_bryt_order": "Неизвестный порядок панелей: «{0}». Используется по умолчанию.",
    "log_final_slices_order": "  Итоговый порядок панелей ({0}): [{1}]",

    #   Splitter — Создание наложений (overlays) и смешивание
    "log_invalid_dimensions_overlay": "Попытка создать overlay с недопустимыми размерами: {0}. Пропуск.",
    "log_empty_overlay": "Создан пустой или почти пустой overlay-PDF. Пропуск объединения.",
    "log_overlay_error": "Ошибка создания overlay-PDF: {0}",
    "log_merge_error": "Попытка объединить overlay без страниц. Пропуск.",
    "log_merge_page_error": "Ошибка объединения overlay-PDF: {0}",
    "log_fallback_draw_rotating_elements": "Не удалось получить строки/столбцы для _draw_rotating_elements, использовано 1×1.",
    "log_overlay_created_for_slice": "Overlay полос/меток создан для панели {0}",
    "log_overlay_creation_failed_for_slice": "Не удалось создать overlay для {0}",
    "log_merging_rotated_overlay": "Объединение ПОВЁРНУТОГО overlay для {0} с T={1}",
    "log_merging_nonrotated_overlay": "Объединение НЕповёрнутого overlay для {0}",
    "log_merging_all_codes_overlay": "Объединение overlay всех кодов (без поворота)",
    "log_merging_separation_lines_overlay": "Объединение overlay разделительных линий (без поворота)",
    "log_merging_code_overlay_for_slice": "Overlay кода для {0} объединён без поворота.",
    "log_merging_separation_overlay_for_slice": "Overlay разделительных линий для {0} объединён без поворота.",

    #   Splitter — Рисование графических элементов (полосы, метки, линии)
    "log_drawing_top_stripe": "[Canvas] Рисование верхней полосы для {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Рисование правой полосы для {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Заливка и обводка угла для {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Рисование креста с центром в ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Рисование линий совмещения для {0} в области от ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Рисование правой вертикальной: x={0:.3f}, y={1:.3f} → {2:.3f}",
    "log_drawing_top_horizontal_line": "  Рисование верхней горизонтальной: y={0:.3f}, x={1:.3f} → {2:.3f}",
    "log_drawing_separation_line": "Рисование разделительной (белая поверх чёрной): ({0}) @ ({1:.3f}, {2:.3f}), длина={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Рисование крестов для {0} [{1},{2}] / [{3},{4}] в области от ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Рассчитаны центры: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Рисование TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Рисование TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Рисование BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Рисование BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Пропущена {0} согласно правилу для позиции [{1},{2}]",
    "log_trial_common_sheet": "Применяется водяной знак TRIAL на общем листе",

    # Водяной знак
    "log_trial_watermark_added": "Добавлен водяной знак TRIAL",
    "error_drawing_trial_text": "Ошибка рисования водяного знака: {error}",

    #   Splitter — Разделительные линии (страница целиком)
    "log_drawing_separation_lines_for_page": "Рисование разделительных линий для страницы (схема={0}, всего панелей={1}, индекс={2})",
    "log_vertical_line_between_slices": "  Вертикальная линия между панелями {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Начало вертикальной @ x={0:.1f}",
    "log_vertical_line_end": "  Конец вертикальной @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Горизонтальная линия между панелями {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Начало горизонтальной @ y={0:.1f}",
    "log_horizontal_line_end": "  Конец горизонтальной @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Отдельные_файлы) Начало вертик./гориз. @ {0:.1f}",
    "log_sep_line_end_separate": "  (Отдельные_файлы) Конец вертик./гориз. @ {0:.1f}",

    #   Splitter — Генерация кодов / QR
    "log_generate_barcode_data": "Генерация данных для кода: {0}",
    "log_barcode_data_shortened": "Данные кода сокращены до {0} символов.",
    "log_barcode_data_error": "Ошибка генерации данных кода: {0}",
    "log_compose_barcode_payload": "Формирование полезной нагрузки кода ({0}): {1}",
    "log_barcode_payload_shortened": "Полезная нагрузка сокращена до {0} символов для формата {1}",
    "log_barcode_payload_error": "Ошибка формирования полезной нагрузки: {0}",
    "log_unknown_anchor_fallback": "Неизвестный якорь «{0}», используется левый нижний угол",
    "log_used_default_code_settings": "Использованы настройки «default» для кода {0}/{1}.",
    "log_no_layout_key_fallback": "Нет схемы «{0}» для {1}/{2}. Использована первая доступная: «{3}».",
    "log_code_settings_error": "Не найдены/ошибка получения настроек кода ({0}/{1}/{2}): {3}. Используются значения по умолчанию.",
    "log_drawing_barcode": "Рисование {0} в ({1:.3f}, {2:.3f}) [база ({3:.3f}, {4:.3f}) + смещение ({5:.3f}, {6:.3f})], поворот: {7}°",
    "error_generate_qr_svg": "Сбой генерации SVG QR-кода.",
    "error_invalid_scale_for_qr": "Недопустимый размер QR: {0} мм",
    "error_invalid_qr_scale_factor": "Недопустимый масштаб QR: {0}",
    "error_generate_barcode_svg": "Сбой генерации SVG штрих-кода.",
    "error_invalid_scale_for_barcode": "Недопустимый размер штрих-кода: {0}×{1} мм",
    "error_invalid_barcode_scale_factor": "Недопустимый масштаб штрих-кода: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: размер в конфиге={1:.3f} мм, ширина SVG={2:.3f} pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: размер в конфиге=({1:.3f} мм, {2:.3f} мм), размер SVG=({3:.3f} pt, {4:.3f} pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Ошибка рисования кода «{0}»: {1}",
    "log_prepared_barcode_info": "Информация кода подготовлена для {0} ({1}, якорь={2}): базовая абсолютная позиция ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Ошибка подготовки данных кода для {0}: {1}",
    "log_drawing_barcodes_count": "Рисование кодов/QR: {0} шт...",
    "log_missing_barcode_info_key": "Отсутствует ключ в информации кода при рисовании: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Ошибка рисования кода «{0}» в _draw_all_barcodes: {1}",

    #   Splitter — Процесс резки (методы split_*)
    "log_start_splitting_process": "--- Запуск процесса резки для: {0} ---",
    "log_split_settings": "  Настройки: {0}×{1} панелей, перехлёст={2} мм, белая полоса={3} мм (+перехлёст: {4})",
    "log_output_dir_info": "  Вывод: {0} / {1} в «{2}»",
    "log_lines_marks_barcodes_info": "  Линии: разделительные={0}, начало={1}, конец={2} | Метки: {3} ({4}), Коды: {5} ({6})",
    "log_bryt_order_info": "  Порядок: {0}, поворот панелей: {1}°",
    "log_invalid_dimensions_in_slice_info": "Недопустимые размеры в slice_info для {0}: {1}×{2}",
    "log_content_transform": "Трансформация содержимого T_content для {0}: {1}",
    "log_merged_content_for_slice": "Содержимое объединено для панели {0} в new_page",
    "log_slice_reader_created": "Полная панель (PdfReader) создана для {0}",
    "log_slice_reader_creation_error": "Ошибка создания полной панели для {0}: {1}",
    "log_used_get_transform": "Использован _get_transform (только перенос): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Старт: ОТДЕЛЬНЫЕ ФАЙЛЫ (поворот в create_slice_reader) ---",
    "log_creating_file_for_slice": "Создание файла для панели {0}: {1}",
    "log_invalid_page_size_for_slice": "Недопустимый размер страницы ({0}×{1}) для {2}. Пропуск.",
    "log_blank_page_creation_error": "Ошибка создания страницы для {0} (размер {1}×{2}): {3}. Пропуск.",
    "log_transform_for_slice": "Трансформация T (только перенос) для {0}: {1}",
    "log_merging_complete_slice": "Объединение полной панели {0} с трансформацией: {1}",
    "log_skipped_slice_merging": "Объединение полной панели для {0} пропущено.",
    "log_file_saved": "Файл сохранён: {0}",
    "log_file_save_error": "Ошибка сохранения файла {0}: {1}",
    "log_finished_split_separate_files": "--- Завершено: ОТДЕЛЬНЫЕ ФАЙЛЫ (сохранено {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Нет панелей для обработки в split_horizontal.",
    "log_start_split_horizontal": "--- Старт: ОБЩИЙ ЛИСТ — ГОРИЗОНТАЛЬНЫЙ (поворот в create_slice_reader) ---",
    "log_page_dimensions": "Размеры страницы: {0:.1f}×{1:.1f} мм ({2} панелей)",
    "log_page_creation_error": "Ошибка создания выходной страницы ({0}×{1}): {2}. Прерывание.",
    "log_slice_at_position": "Панель {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Трансформация T (только перенос) для {0}: {1}",
    "log_merging_complete_bryt": "Объединение полной панели {0} с трансформацией: {1}",
    "log_skipped_merging_bryt": "Объединение полной панели для {0} пропущено.",
    "log_file_result_saved": "Файл результата сохранён: {0}",
    "log_file_result_save_error": "Ошибка сохранения файла результата {0}: {1}",
    "log_finished_split_horizontal": "--- Завершено: ОБЩИЙ ЛИСТ — ГОРИЗОНТАЛЬНЫЙ ---",
    "log_no_slices_split_vertical": "Нет панелей для обработки в split_vertical.",
    "log_start_split_vertical": "--- Старт: ОБЩИЙ ЛИСТ — ВЕРТИКАЛЬНЫЙ (поворот в create_slice_reader) ---",
    "log_finished_split_vertical": "--- Завершено: ОБЩИЙ ЛИСТ — ВЕРТИКАЛЬНЫЙ ---",
    "log_unknown_layout": "Неизвестная схема выкладки для общего листа: «{0}».",
    "log_unknown_output_type": "Неизвестный тип вывода: «{0}».",
    "log_finished_splitting_success": "--- Процесс резки завершён для: {0} — УСПЕХ ---",
    "log_finished_splitting_errors": "--- Процесс резки завершён для: {0} — БЫЛИ ОШИБКИ ---",
    "log_value_error_in_splitting": "Ошибка входных данных или расчёта: {0}",
    "log_finished_splitting_critical_error": "--- Процесс резки завершён для: {0} — КРИТИЧЕСКАЯ ОШИБКА ---",
    "log_unexpected_error_in_splitting": "Неожиданная ошибка при резке файла {0}: {1}",

    #   Splitter — Тестовый режим (__main__)
    "log_script_mode_test": "splitter.py запущен как главный скрипт (тестовый режим).",
    "log_loaded_config": "Конфигурация загружена.",
    "log_error_loading_config": "Сбой загрузки конфигурации: {0}",
    "log_created_example_pdf": "Создан пример PDF: {0}",
    "log_cannot_create_example_pdf": "Сбой создания PDF-примера: {0}",
    "log_start_test_split": "Старт тестовой резки файла: {0} в {1}",
    "log_test_split_success": "Тестовая резка успешно завершена.",
    "log_test_split_errors": "Тестовая резка завершена с ошибками.",

    # --- Логи — QR/штрих-код (barcode_qr.py) ---
    "log_qr_empty_data": "Попытка сгенерировать QR-код для пустых данных.",
    "log_qr_generated": "SVG QR-кода создан для: {0}...",
    "log_qr_error": "Ошибка генерации QR для данных «{0}»: {1}",
    "log_barcode_empty_data": "Попытка сгенерировать штрих-код для пустых данных.",
    "log_barcode_generated": "SVG штрих-кода создан для: {0}...",
    "log_barcode_error": "Ошибка генерации штрих-кода для «{0}»: {1}",
    "log_basic_handler_configured": "Базовый обработчик настроен для логгера в barcode_qr.py",
    "log_basic_handler_error": "Сбой настройки базового обработчика в barcode_qr: {0}",

    # --- Логи — Конфиг/Профили (main_config_manager.py) ---
    "loading_profiles_from": "Загрузка профилей из",
    "profiles_file": "Файл профилей",
    "does_not_contain_dict": "не содержит словаря. Создаётся новый",
    "not_found_creating_new": "не найден. Создаётся новый пустой",
    "json_profiles_read_error": "Ошибка чтения JSON-файла профилей",
    "file_will_be_overwritten": "Файл будет перезаписан при сохранении",
    "json_decode_error_in_profiles": "Ошибка декодирования JSON в файле профилей",
    "cannot_load_profiles_file": "Невозможно загрузить файл профилей",
    "unexpected_profiles_read_error": "Неожиданная ошибка чтения профилей",
    "saving_profiles_to": "Сохранение профилей в",
    "cannot_save_profiles_file": "Невозможно сохранить файл профилей",
    "profiles_save_error": "Ошибка сохранения профилей в файл",
    "logger_profile_saved": "Профиль сохранён: {profile}",
    "logger_profile_not_found": "Профиль не найден для загрузки: {profile}",
    "logger_profile_loaded": "Профиль загружен: {profile}",
    "logger_profile_delete_not_exist": "Попытка удалить несуществующий профиль: {profile}",
    "logger_profile_deleted": "Профиль удалён: {profile}",
    "logger_start_save_settings": "Запущено сохранение настроек из GUI.",
    "logger_invalid_value": "Недопустимое значение для «{key}». Установлено 0.0.",
    "logger_end_save_settings": "Сохранение настроек из GUI завершено.",
    "logger_conversion_error": "Ошибка преобразования значений из GUI: {error}",
    "conversion_failed": "Сбой преобразования значений из GUI",
    "logger_unexpected_save_error": "Неожиданная ошибка сохранения настроек: {error}",
    "logger_settings_saved": "Настройки сохранены в файл: {file}",

    # --- Логи — Лицензирование (main_license.py) ---
    "public_key_load_error_log": "Ошибка загрузки открытого ключа",
    "license_key_decode_error": "Ошибка декодирования лицензионного ключа",
    "license_activation_error": "Ошибка активации лицензии",

    # --- Логи — Главный модуль (main.py) ---
    "ui_created": "Пользовательский интерфейс создан.",
    "error_tab_home": "Ошибка создания интерфейса «Главная»",
    "error_tab_settings": "Ошибка создания интерфейса «Настройки»",
    "error_tab_help": "Ошибка создания интерфейса «Справка»",
    "error_creating_license_ui": "Ошибка создания интерфейса «Лицензия»",
    "error_loading_ui": "Общая ошибка загрузки интерфейса: {error}",
    "error_creating_home_ui": "Ошибка создания интерфейса «Главная»",
    "error_creating_settings_ui": "Ошибка создания интерфейса «Настройки»",
    "error_creating_help_ui": "Ошибка создания интерфейса «Справка»",
    "logger_update_gui": "Запущено обновление GUI из конфигурации.",
    "logger_end_update_gui": "Обновление GUI из конфигурации завершено.",
    "logger_update_gui_error": "Неожиданная ошибка обновления GUI: {error}",
    "logger_invalid_output_dir": "Недопустимая или отсутствующая выходная папка: {directory}",
    "logger_invalid_input_file": "Недопустимый или отсутствующий входной файл: {file}",
    "logger_start_pdf": "Запущен процесс генерации PDF.",
    "logger_pdf_save_error": "Генерация PDF прервана: сбой сохранения текущих настроек.",
    "logger_pdf_success": "Генерация PDF успешно завершена.",
    "logger_pdf_exception": "Исключение в основном процессе генерации PDF.",
    "icon_set_error": "Сбой установки иконки приложения: {error}",
    "accent_button_style_error": "Сбой установки стилядля accent-кнопки: {error}",
    "logger_file_save_error": "Ошибка сохранения файла {file}: {error}",

    #   Логи — Предпросмотр (main.py — update_preview, update_output_preview)
    "thumbnail_error_log": "Ошибка генерации миниатюры",
    "output_preview_update_called": "Вызвано обновление предпросмотра результата",
    "output_preview_canvas_missing": "Отсутствует canvas предпросмотра результата",
    "pdf_found_in_output_dir": "PDF найден в выходной папке",
    "preparing_thumbnail": "Подготовка миниатюры",
    "thumbnail_generated_successfully": "Миниатюра успешно создана",
    "thumbnail_generation_error": "Ошибка генерации миниатюры для",
    "no_pdf_for_common_sheet": "Нет PDF для предпросмотра общего листа",
    "no_pdf_for_separate_files": "Нет сгенерированных PDF для предпросмотра",
    "cannot_load_thumbnail": "Невозможно загрузить миниатюру из",

    #   Логи — Внутреннее для разработчика (main.py)
    "missing_gui_var_created": "Создана отсутствующая GUI-переменная для ключа: {key}",
    "missing_gui_structure_created": "Создана отсутствующая структура GUI для: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Создана отсутствующая GUI-переменная для: {code_type}/{output_type}/{layout}/{param}",

    # Доп. ключи для main_ui_help.py
    "help_text": """
    Billboard Splitter — Руководство пользователя\n\n
    Назначение программы:\n
    Billboard Splitter автоматически делит макеты билбордов на панели, готовые к печати.
    Программа рассчитана на работу с файлами в масштабе 1:10.\n
    Значения в разделах: Перехлёст, Белая полоса и Настройки вводятся в масштабе 1:1.
    Программа позволяет размещать разрезанные панели в PDF по выбранной схеме:\n
    • Общий лист: все панели в одном документе.\n
    • Отдельные файлы: каждая панель в отдельном PDF.\n\n
    Дополнительно программа позволяет:\n
    • Выбирать схему — вертикальную или горизонтальную (в вертикальной разделительные линии наверху и внизу,
      в горизонтальной — слева и справа).\n
    • Поворачивать панели на 180° (инверсия проекта).\n
    • Добавлять метки совмещения (кресты или линии) для точного позиционирования при наклейке.\n
    • Добавлять QR-коды или штрих-коды, генерируемые из входных данных для идентификации панелей.\n
    • Сохранять настройки как профили: их можно загружать, изменять и удалять для быстрого переключения.\n\n
    Основные шаги работы:\n\n
    1. Выбор входного файла:\n
    • На вкладке «Главная» выберите PDF, JPG или TIFF с макетом билборда.\n
    • Если путь не задан, по умолчанию используется демонстрационный файл.\n\n
    2. Параметры резки:\n
    • Укажите число строк и столбцов.\n
    • Задайте величину перехлёста.\n
    • При необходимости задайте ширину белой полосы, добавляемой к эффективному перехлёсту.\n\n
    3. Схема выкладки:\n
    • Вертикальная: все панели выкладываются вертикально на странице PDF.\n
    • Горизонтальная: все панели выкладываются горизонтально.\n\n
    4. Тип вывода:\n
    • Общий лист — один PDF.\n
    • Отдельные файлы — по одному PDF на панель.\n
    • На «Главной» можно включить и настроить метки совмещения — крест или линию.\n
    • При необходимости включите QR или штрих-код — он будет сформирован из данных проекта.\n
    • Параметры кода (масштаб, смещение, поворот, положение) настраиваются на вкладке «Настройки».\n\n
    5. Управление конфигурациями:\n
    • На вкладке «Настройки» детально регулируются графические параметры (отступы, толщины линий, зазоры) и настройки кодов.\n
    • Сохраните текущую конфигурацию как профиль, чтобы затем загрузить/изменить.\n
    • Профили (profiles.json) позволяют быстро переключаться между наборами настроек.\n\n
    6. Генерация PDF:\n
    • Нажмите «Сгенерировать PDF».\n
    • Результаты сохраняются в папке output (или другой указанной), а логи — в папке logs (или другой).\n\n
    Если возникли проблемы:\n
    • Проверьте логи в каталоге «logs». Каждый день создаётся файл лога с датой в имени.\n
    • Убедитесь, что все требуемые каталоги заданы.\n
    • Техподдержка: tech@printworks.pl (будни, 8–16)\n
    """
}
