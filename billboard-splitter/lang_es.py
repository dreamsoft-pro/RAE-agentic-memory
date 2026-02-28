# lang_es.py
"""
Archivo con traducciones para el idioma español.
"""

LANG = {
    "barcode_font_size_label": "Tamaño de fuente de la descripción del código de barras [pt]:",
    # ==========================
    #  Aplicación - General
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Error",
    "no_file": "Sin archivo",
    "language": "Idioma",
    "language_switch": "Cambio de idioma",
    "choose_language": "Elige el idioma:",
    "apply_language": "Aplicar",
    "language_changed": "El idioma ha sido cambiado. Algunos cambios serán visibles después de reiniciar la aplicación.",

    # ========================================
    #  Elementos de la Interfaz de Usuario (GUI)
    # ========================================

    # --- Pestañas principales ---
    "tab_home": " Inicio ",
    "tab_settings": " Configuración ",
    "tab_help": " Ayuda ",
    "tab_license": " Licencia ",

    # --- Botones generales ---
    "button_browse": "Examinar...",
    "browse_folder": "Examinar carpeta...",
    "button_save": "Guardar",
    "button_delete": "Eliminar",
    "button_close": "Cerrar",
    "save_all_settings": "Guardar toda la configuración",

    # --- Etiquetas de campos (Pestaña Inicio) ---
    "label_rows": "División vertical (filas):",
    "label_columns": "División horizontal (columnas):",
    "label_overlap": "Solape [mm]:",
    "label_white_stripe": "Franja blanca [mm]:",
    "label_add_white_stripe": "Añadir franja blanca al solape efectivo",
    "label_layout": "Disposición de salida:",
    "label_output_type": "Tipo de salida:",
    "label_enable_reg_marks": "Habilitar marcas de registro:",
    "label_enable_codes": "Habilitar códigos:",
    "label_enable_sep_lines": "Habilitar líneas de separación (entre paneles)",
    "label_enable_start_line": "Habilitar línea de inicio/superior de la hoja",
    "label_enable_end_line": "Habilitar línea de fin/inferior de la hoja",
    "label_bryt_order": "Orden de paneles:",
    "label_slice_rotation": "Rotación de paneles:",
    "label_create_order_folder": "Crear carpeta con número de pedido",

    # --- Secciones/Grupos (Pestaña Inicio) ---
    "section_input_file": " Archivo de entrada ",
    "section_scale_and_dimensions": " Escala y dimensiones de salida ",
    "label_original_size": "Tamaño original:",
    "label_scale_non_uniform": "Escalar no uniformemente",
    "label_scale": "Escala: 1:",
    "label_scale_x": "Escala X: 1:",
    "label_scale_y": "Escala Y: 1:",
    "label_output_dimensions": "Dimensiones del archivo de salida:",
    "label_width_cm": "Ancho [cm]:",
    "label_height_cm": "Alto [cm]:",
    "section_split_settings": " Configuración de corte ",
    "section_profiles": " Perfiles de configuración ",
    "section_save_location": " Ubicación de guardado ",
    "section_input_preview": " Vista previa del archivo de entrada ",
    "section_output_preview": " Vista previa de salida ",

    # --- Valores de opciones (Combobox, Radiobutton, etc.) ---
    "layout_vertical": "Vertical",
    "layout_horizontal": "Horizontal",
    "output_common_sheet": "Hoja común",
    "output_separate_files": "Archivos separados",
    "output_both": "Hoja común y archivos separados",
    "output_common": "Hoja común",
    "output_separate": "Archivos separados",
    "reg_mark_cross": "Cruz",
    "reg_mark_line": "Línea",
    "code_qr": "Código QR",
    "code_barcode": "Código de barras",
    "bryt_order_1": "A1-An, B1-Bn, .. Estándar, desde arriba",
    "bryt_order_2": "A1-An, Bn-B1, .. Serpiente por filas, desde arriba",
    "bryt_order_3": "A1..B1, A2..B2, .. Por columnas, desde arriba",
    "bryt_order_4": "A1-A2..B2-B1.. Serpiente por columnas, desde arriba",
    "bryt_order_5": "N1-Nn, (N-1)1-(N-1)n, .. Estándar, desde abajo",
    "bryt_order_6": "N1-Nn, (N-1)n-(N-1)1, .. Serpiente por filas, desde abajo",
    "logging_console": "consola",
    "logging_file": "archivo",
    "logging_both": "ambos",

    # --- Secciones/Grupos (Pestaña Configuración) ---
    "section_processing_mode": " Operaciones de corte ",
    "processing_mode_ram": "RAM (en memoria)",
    "processing_mode_hdd": "Disco (en almacenamiento)",
    "graphic_settings": "Configuración gráfica",
    "code_settings": "Configuración de QR / Código de barras",
    "logging_settings": "Configuración de registro (logs)",
    "barcode_text_position_label": "Posición del texto del código:",
    "barcode_text_bottom": "debajo",
    "barcode_text_side": "al lado",
    "barcode_text_none": "ninguno",

    # --- Etiquetas (Configuración - Gráficos) ---
    "extra_margin_label": "Margen alrededor de los paneles [mm]:",
    "margin_top_label": "Margen superior [mm]:",
    "margin_bottom_label": "Margen inferior [mm]:",
    "margin_left_label": "Margen izquierdo [mm]:",
    "margin_right_label": "Margen derecho [mm]:",
    "reg_mark_width_label": "Marca de registro - Ancho [mm]:",
    "reg_mark_height_label": "Marca de registro - Alto [mm]:",
    "reg_mark_white_line_width_label": "Marca de registro - Grosor de línea blanca [mm]:",
    "reg_mark_black_line_width_label": "Marca de registro - Grosor de línea negra [mm]:",
    "sep_line_black_width_label": "Línea de separación - Grosor de línea negra [mm]:",
    "sep_line_white_width_label": "Línea de separación - Grosor de línea blanca [mm]:",
    "slice_gap_label": "Espacio entre paneles [mm]:",
    "label_draw_slice_border": "Dibujar borde alrededor del panel (línea de corte)",

    # --- Etiquetas (Configuración - Códigos) ---
    "scale_label": "Tamaño [mm]:",
    "scale_x_label": "Ancho X [mm]:",
    "scale_y_label": "Alto Y [mm]:",
    "offset_x_label": "Desplazamiento X [mm]:",
    "offset_y_label": "Desplazamiento Y [mm]:",
    "rotation_label": "Rotación (°):",
    "anchor_label": "Esquina:",

    # --- Etiquetas (Configuración - Logs) ---
    "logging_mode_label": "Modo de registro:",
    "log_file_label": "Archivo de log:",
    "logging_level_label": "Nivel de registro:",

    # --- Botones / Acciones (Pestaña Inicio) ---
    "button_load": "Cargar",
    "button_save_settings": "Guardar configuración actual",
    "button_generate_pdf": "Generar PDF",
    "button_refresh_preview": "Actualizar vista previa",
    "button_refresh_layout": "Actualizar disposición",

    # --- Licencia (GUI) ---
    "hwid_frame_title": "Identificador único de hardware (HWID)",
    "copy_hwid": "Copiar HWID",
    "license_frame_title": "Activación de licencia",
    "enter_license_key": "Introduce la clave de licencia:",
    "activate": "Activar",
    "status_trial": "Modo de prueba",
    "license_active": "Licencia activa",

    # ================================================
    #  Mensajes para el usuario (Ventanas, Barra de estado)
    # ================================================

    # --- Perfiles ---
    "msg_no_profile_name": "Sin nombre",
    "msg_enter_profile_name": "Introduce un nombre de perfil para guardar.",
    "msg_profile_saved": "Perfil guardado",
    "profile_saved_title": "Perfil guardado",
    "msg_profile_saved_detail": "El perfil '{0}' ha sido guardado.",
    "profile_saved": "El perfil '{profile}' ha sido guardado.",
    "profile_saved_and_applied": "El perfil '{profile}' ha sido guardado y aplicado.",
    "msg_no_profile": "Sin perfil",
    "warning_no_profile": "Sin perfil",
    "msg_select_profile": "Selecciona un nombre de perfil de la lista para cargar.",
    "select_profile": "Selecciona un nombre de perfil de la lista para cargar.",
    "profile_loaded_title": "Perfil cargado",
    "profile_loaded": "El perfil '{profile}' ha sido cargado.",
    "warning_no_profile_delete": "Sin perfil",
    "warning_no_profile_delete_message": "Selecciona un perfil de la lista para eliminar.",
    "profile_not_found": "No se encontró el perfil '{profile}'.",
    "profile_not_exist": "El perfil '{profile}' no existe.",
    "confirm_delete_title": "Confirmar eliminación",
    "confirm_delete_profile": "¿Seguro que deseas eliminar el perfil '{profile}'?",
    "profile_deleted_title": "Perfil eliminado",
    "profile_deleted": "El perfil '{profile}' ha sido eliminado.",

    # --- Archivos / Directorios ---
    "msg_no_input_file": "Sin archivo de entrada",
    "msg_unsupported_format": "Formato no compatible",
    "select_file_title": "Seleccionar archivo de entrada",
    "supported_files": "Archivos compatibles",
    "all_files": "Todos los archivos",
    "select_dir_title": "Seleccionar directorio de salida",
    "select_log_dir_title": "Seleccionar directorio para archivos de log",
    "error_output_dir_title": "Error en el directorio de salida",
    "error_output_dir": "El directorio de salida especificado es inválido o no existe:\n{directory}",
    "error_input_file_title": "Error de archivo de entrada",
    "error_input_file": "El archivo de entrada especificado es inválido o no existe:\n{file}",
    "save_file_error_title": "Error al guardar archivo",
    "save_file_error": "No se pudo guardar el archivo: {error}",

    # --- Procesado PDF / Vista previa ---
    "msg_pdf_processing_error": "Fallo al procesar el archivo PDF",
    "msg_thumbnail_error": "Error al cargar la miniatura",
    "msg_no_pdf_output": "Sin salida PDF",
    "no_pdf_pages": "No hay páginas en el archivo PDF",
    "unsupported_output": "Tipo de salida no compatible para vista previa",
    "pdf_generated_title": "Generación completada",
    "pdf_generated": "El/los archivo(s) PDF se han generado correctamente en el directorio:\n{directory}",
    "pdf_generation_error_title": "Error de generación",
    "pdf_generation_error": "Se produjeron errores al generar el PDF. Revisa los registros para más información.",
    "critical_pdf_error_title": "Error crítico de generación de PDF",
    "critical_pdf_error": "Ocurrió un error crítico al generar el PDF:\n{error}\nRevisa los registros.",
    "settings_saved_title": "Configuración guardada",
    "settings_saved": "La configuración se ha guardado en el archivo:\n{filepath}",
    "settings_save_error_title": "Error al guardar configuración",
    "settings_save_error": "No se pudo guardar la configuración: {error}",
    "conversion_error_title": "Error de conversión",
    "conversion_error": "Error al convertir valores desde la interfaz: {error}",
    "update_gui_error_title": "Error de actualización de la interfaz",
    "update_gui_error": "Ocurrió un error al actualizar la interfaz: {error}",

    # --- Licencia ---
    "hwid_copied_to_clipboard": "El HWID se ha copiado al portapapeles",
    "computer_hwid": "HWID del equipo",
    "public_key_load_error": "Error al cargar la clave pública: {error}",
    "invalid_license_format": "Formato de clave de licencia inválido: {error}",
    "activation_success": "La licencia se ha activado correctamente.",
    "activation_error": "Error de activación de licencia: {error}",
    "log_trial_mode_active": "El modo de prueba está activo",
    "log_trial_mode_inactive": "El modo de prueba no está activo",

    # --- Inicialización ---
    "init_error_title": "Error de inicialización",
    "init_error": "Error al inicializar directorios: {error}",
    "poppler_path_info": "Información de la ruta de Poppler",
    "ttkthemes_not_installed": "Aviso: La biblioteca ttkthemes no está instalada. Se usará el estilo por defecto de Tkinter.",

    # =====================================
    #  Logs (Mensajes del registrador)
    # =====================================

    # --- General / Configuración ---
    "log_configured": "Registro configurado: nivel={0}, modo={1}, archivo={2}",
    "log_no_handlers": "Aviso: No hay controladores de registro configurados (modo: {0}).",
    "log_critical_error": "Error crítico en la configuración del registro: {0}",
    "log_basic_config": "Se usó la configuración básica de registro debido a un error.",
    "log_dir_create_error": "Error crítico: No se puede crear el directorio de logs {0}: {1}",

    # --- Logs - Inicialización / Directorios (init_directories.py) ---
    "error_critical_init": "ERROR CRÍTICO durante la inicialización: {0}",
    "logger_init_error": "Error de inicialización de directorios: {error}",
    "directory_created": "Directorio creado: {0}",
    "directory_creation_error": "No se pudo crear el directorio {0}: {1}",
    "sample_file_copied": "Archivo de muestra copiado a {0}",
    "sample_file_copy_error": "Error al copiar el archivo de muestra: {0}",
    "log_created_output_dir": "Directorio de salida creado: {0}",
    "log_cannot_create_output_dir": "No se puede crear el directorio de salida {0}: {1}",

    # --- Logs - Splitter (splitter.py) ---
    "log_graphic_settings_error": "Fallo al cargar la configuración gráfica durante la inicialización: {0}",
    "log_loading_pdf": "Cargando archivo PDF: {0}",
    "log_loading_bitmap": "Cargando archivo de mapa de bits: {0}",
    "log_invalid_dpi": "DPI leído inválido ({0}). Usando {1} DPI por defecto.",
    "log_image_dimensions": "Dimensiones de imagen: {0}x{1}px, Modo: {2}, DPI: {3:.1f} -> {4:.3f}x{5:.3f}pt",
    "log_image_processing_color": "Procesando imagen con modo de color original: {0}",
    "log_unusual_color_mode": "Modo de color inusual: '{0}'. ReportLab/Pillow podrían no manejarlo correctamente.",
    "log_draw_image_error": "Error durante ReportLab drawImage para el modo {0}: {1}",
    "log_unsupported_format": "Formato de entrada no compatible: {0}",
    "log_input_file_not_found": "Archivo de entrada no encontrado: {0}",
    "log_load_process_error": "Error al cargar o procesar el archivo {0}: {1}",
    "log_input_file_not_exists": "El archivo de entrada no existe o la ruta está vacía: '{0}'",
    "log_cannot_load_or_empty_pdf": "Fallo al cargar el archivo de entrada o el PDF está vacío/corrupto.",
    "log_pdf_dimensions_info": "  Dimensiones del PDF: {0:.1f}mm x {1:.1f}mm",
    "log_invalid_pdf_dimensions": "Dimensiones de página PDF inválidas: {0}x{1} pt.",

    #   Splitter - Cálculos de dimensiones
    "log_extra_margin": "Margen extra establecido en {0:.3f} pt",
    "log_invalid_rows_cols": "Número inválido de filas ({0}) o columnas ({1}).",
    "error_invalid_rows_cols": "Las filas y columnas deben ser enteros positivos.",
    "log_invalid_overlap_white_stripe": "Valores inválidos de solape ({0}) o franja blanca ({1}). Deben ser numéricos.",
    "error_invalid_overlap_white_stripe": "El solape y la franja blanca deben ser valores numéricos (mm).",
    "log_stripe_usage": "Establecido use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Solape base (gráfica): {0:.3f} mm, Franja blanca: {1:.3f} mm, Solape efectivo: {2:.3f} mm",
    "log_computed_dimensions": "Dimensiones calculadas: PDF: {0:.3f}mm x {1:.3f}mm. Panel: {2:.3f}pt ({3:.3f}mm) x {4:.3f}pt ({5:.3f}mm). Núcleo: {6:.3f}pt x {7:.3f}pt. Solape efectivo: {8:.3f}mm",
    "log_invalid_dimensions": "Dimensiones calculadas inválidas de panel ({0:.3f}x{1:.3f}) o núcleo ({2:.3f}x{3:.3f}) para solape={4}, franja={5}, f={6}, c={7}, W={8}mm, H={9}mm",
    "error_invalid_slice_dimensions": "Las dimensiones calculadas del panel/núcleo son inválidas o negativas.",

    #   Splitter - Generación de información y orden de paneles
    "log_generating_slice_info": "Generando información de panel: {0}",
    "log_no_slices_info_generated": "Fallo al generar información de paneles.",
    "log_applying_rotated_order": "Aplicando orden para rotación de 180 grados: {0}",
    "log_applying_standard_order": "Aplicando orden para 0 grados (estándar): {0}",
    "log_unknown_bryt_order": "Orden de paneles desconocido: '{0}'. Usando el predeterminado.",
    "log_final_slices_order": "  Orden final de paneles ({0}): [{1}]",

    #   Splitter - Creación de superposiciones (overlays) y mezcla
    "log_invalid_dimensions_overlay": "Intento de crear un overlay con dimensiones inválidas: {0}. Omitiendo.",
    "log_empty_overlay": "Se creó un PDF de overlay vacío o casi vacío. Omitiendo combinación.",
    "log_overlay_error": "Error al crear el PDF de overlay: {0}",
    "log_merge_error": "Intento de combinar un overlay sin páginas. Omitiendo.",
    "log_merge_page_error": "Error al combinar el PDF de overlay: {0}",
    "log_fallback_draw_rotating_elements": "No se pudieron obtener filas/columnas para _draw_rotating_elements, se usó 1x1.",
    "log_overlay_created_for_slice": "Overlay de franjas/marcas creado para el panel {0}",
    "log_overlay_creation_failed_for_slice": "Fallo al crear overlay de franjas/marcas para {0}",
    "log_merging_rotated_overlay": "Combinando overlay ROTADO para {0} con T={1}",
    "log_merging_nonrotated_overlay": "Combinando overlay NO rotado para {0}",
    "log_merging_all_codes_overlay": "Combinando overlay de todos los códigos (sin rotación)",
    "log_merging_separation_lines_overlay": "Combinando overlay de líneas de separación (sin rotación)",
    "log_merging_code_overlay_for_slice": "Overlay de código para {0} combinado sin rotación.",
    "log_merging_separation_overlay_for_slice": "Overlay de líneas de separación para {0} combinado sin rotación.",

    #   Splitter - Dibujo de elementos gráficos (franjas, marcas, líneas)
    "log_drawing_top_stripe": "[Canvas Draw] Dibujando franja superior para {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas Draw] Dibujando franja derecha para {0}: x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas Draw] Rellenando y contorneando esquina para {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Dibujando cruz centrada en ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Dibujando líneas de registro para {0} en el área desde ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Dibujando línea vertical derecha: x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  Dibujando línea horizontal superior: y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "Dibujando línea de separación (blanca sobre negro): ({0}) @ ({1:.3f}, {2:.3f}), long={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Dibujando cruces para {0} [{1},{2}] / [{3},{4}] en el área desde ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Centros calculados: TL({0:.1f},{1:.1f}), TR({2:.1f},{3:.1f}), BL({4:.1f},{5:.1f}), BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Dibujando TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Dibujando TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Dibujando BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Dibujando BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Omitida {0} según regla para posición [{1},{2}]",
    "log_trial_common_sheet": "Aplicando marca de agua TRIAL en la hoja común",

    # Marca de agua
    "log_trial_watermark_added": "Se ha añadido la marca de agua TRIAL",
    "error_drawing_trial_text": "Error al dibujar la marca de agua: {error}",

    #   Splitter - Dibujo de líneas de separación (página completa)
    "log_drawing_separation_lines_for_page": "Dibujando líneas de separación para la página (disposición={0}, total_paneles={1}, índice_panel={2})",
    "log_vertical_line_between_slices": "  Línea vertical entre paneles {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Inicio de línea vertical @ x={0:.1f}",
    "log_vertical_line_end": "  Fin de línea vertical @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Línea horizontal entre paneles {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Inicio de línea horizontal @ y={0:.1f}",
    "log_horizontal_line_end": "  Fin de línea horizontal @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Archivos_separados) Inicio de línea vertical/horizontal @ {0:.1f}",
    "log_sep_line_end_separate": "  (Archivos_separados) Fin de línea vertical/horizontal @ {0:.1f}",

    #   Splitter - Generación de códigos / QR
    "log_generate_barcode_data": "Generando datos para el código: {0}",
    "log_barcode_data_shortened": "Datos del código acortados a {0} caracteres.",
    "log_barcode_data_error": "Error al generar los datos del código: {0}",
    "log_compose_barcode_payload": "Componiendo carga útil del código ({0}): {1}",
    "log_barcode_payload_shortened": "Carga útil acortada a {0} caracteres para el formato {1}",
    "log_barcode_payload_error": "Error al componer la carga útil: {0}",
    "log_unknown_anchor_fallback": "Anclaje desconocido '{0}', usando esquina inferior izquierda",
    "log_used_default_code_settings": "Se usó configuración 'default' para el código {0}/{1}.",
    "log_no_layout_key_fallback": "No hay disposición '{0}' para {1}/{2}. Se usó la primera disponible: '{3}'.",
    "log_code_settings_error": "No encontrada o error al obtener configuración de código ({0}/{1}/{2}): {3}. Usando valores por defecto.",
    "log_drawing_barcode": "Dibujando {0} en ({1:.3f}, {2:.3f}) [base ({3:.3f}, {4:.3f}) + desplazamiento ({5:.3f}, {6:.3f})], rotación: {7}°",
    "error_generate_qr_svg": "Fallo al generar el SVG del código QR.",
    "error_invalid_scale_for_qr": "Escala inválida para QR: {0}mm",
    "error_invalid_qr_scale_factor": "Factor de escala inválido para QR: {0}",
    "error_generate_barcode_svg": "Fallo al generar el SVG del código de barras.",
    "error_invalid_scale_for_barcode": "Escala inválida para código de barras: {0}x{1}mm",
    "error_invalid_barcode_scale_factor": "Factor de escala inválido para código de barras: ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}: escala config={1:.3f}mm, ancho SVG={2:.3f}pt, fe={3:.4f}",
    "log_barcode_scale_code128": "  {0}: escala config=({1:.3f}mm, {2:.3f}mm), tamaño SVG=({3:.3f}pt, {4:.3f}pt), fe=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Error al dibujar el código '{0}': {1}",
    "log_prepared_barcode_info": "Información de código preparada para {0} ({1}, anclaje={2}): posición absoluta base ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Error preparando datos del código para {0}: {1}",
    "log_drawing_barcodes_count": "Dibujando {0} códigos/códigos QR...",
    "log_missing_barcode_info_key": "Falta clave en la información del código al dibujar: {0}. Info: {1}",
    "log_error_drawing_barcode_in_draw_all": "Error al dibujar el código '{0}' en _draw_all_barcodes: {1}",

    #   Splitter - Proceso de corte (métodos split_*)
    "log_start_splitting_process": "--- Iniciando proceso de corte para: {0} ---",
    "log_split_settings": "  Configuración: {0}x{1} paneles, Solape={2}mm, Franja blanca={3}mm (+solape: {4})",
    "log_output_dir_info": "  Salida: {0} / {1} en '{2}'",
    "log_lines_marks_barcodes_info": "  Líneas: Separación={0}, Inicio={1}, Fin={2} | Marcas: {3} ({4}), Códigos: {5} ({6})",
    "log_bryt_order_info": "  Orden: {0}, Rotación de paneles: {1}°",
    "log_invalid_dimensions_in_slice_info": "Dimensiones inválidas en slice_info para {0}: {1}x{2}",
    "log_content_transform": "Transformación de contenido T_content para {0}: {1}",
    "log_merged_content_for_slice": "Contenido fusionado para el panel {0} en new_page",
    "log_slice_reader_created": "Panel completo (PdfReader) creado para {0}",
    "log_slice_reader_creation_error": "Error al crear el panel completo para {0}: {1}",
    "log_used_get_transform": "Se usó _get_transform (solo traslación): x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Iniciando: ARCHIVOS SEPARADOS (Rotación manejada en create_slice_reader) ---",
    "log_creating_file_for_slice": "Creando archivo para el panel {0}: {1}",
    "log_invalid_page_size_for_slice": "Tamaño de página inválido ({0}x{1}) para {2}. Omitiendo.",
    "log_blank_page_creation_error": "Error al crear página para {0} (tamaño {1}x{2}): {3}. Omitiendo.",
    "log_transform_for_slice": "Transformación T (solo traslación) para {0}: {1}",
    "log_merging_complete_slice": "Combinando panel completo {0} con transformación: {1}",
    "log_skipped_slice_merging": "Se omitió la combinación del panel completo para {0}.",
    "log_file_saved": "Archivo guardado: {0}",
    "log_file_save_error": "Error al guardar archivo {0}: {1}",
    "log_finished_split_separate_files": "--- Finalizado: ARCHIVOS SEPARADOS (Guardados {0}/{1}) ---",
    "log_no_slices_split_horizontal": "No hay paneles para procesar en split_horizontal.",
    "log_start_split_horizontal": "--- Iniciando: HOJA COMÚN - HORIZONTAL (Rotación manejada en create_slice_reader) ---",
    "log_page_dimensions": "Dimensiones de página: {0:.1f}mm x {1:.1f}mm ({2} paneles)",
    "log_page_creation_error": "Error al crear la página de resultado ({0}x{1}): {2}. Abortando.",
    "log_slice_at_position": "Panel {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformación T (solo traslación) para {0}: {1}",
    "log_merging_complete_bryt": "Combinando panel completo {0} con transformación: {1}",
    "log_skipped_merging_bryt": "Se omitió la combinación del panel completo para {0}.",
    "log_file_result_saved": "Archivo de resultado guardado: {0}",
    "log_file_result_save_error": "Error al guardar archivo de resultado {0}: {1}",
    "log_finished_split_horizontal": "--- Finalizado: HOJA COMÚN - HORIZONTAL ---",
    "log_no_slices_split_vertical": "No hay paneles para procesar en split_vertical.",
    "log_start_split_vertical": "--- Iniciando: HOJA COMÚN - VERTICAL (Rotación manejada en create_slice_reader) ---",
    "log_finished_split_vertical": "--- Finalizado: HOJA COMÚN - VERTICAL ---",
    "log_unknown_layout": "Disposición desconocida para hoja común: '{0}'.",
    "log_unknown_output_type": "Tipo de salida desconocido: '{0}'.",
    "log_finished_splitting_success": "--- Proceso de corte finalizado para: {0} - ÉXITO ---",
    "log_finished_splitting_errors": "--- Proceso de corte finalizado para: {0} - OCURRIERON ERRORES ---",
    "log_value_error_in_splitting": "Error de entrada o de cálculo: {0}",
    "log_finished_splitting_critical_error": "--- Proceso de corte finalizado para: {0} - ERROR CRÍTICO ---",
    "log_unexpected_error_in_splitting": "Error inesperado al cortar el archivo {0}: {1}",

    #   Splitter - Modo de prueba (__main__)
    "log_script_mode_test": "splitter.py lanzado como script principal (modo prueba).",
    "log_loaded_config": "Configuración cargada.",
    "log_error_loading_config": "Fallo al cargar la configuración: {0}",
    "log_created_example_pdf": "Archivo PDF de ejemplo creado: {0}",
    "log_cannot_create_example_pdf": "Fallo al crear el PDF de ejemplo: {0}",
    "log_start_test_split": "Iniciando corte de prueba del archivo: {0} a {1}",
    "log_test_split_success": "Corte de prueba completado correctamente.",
    "log_test_split_errors": "Corte de prueba finalizado con errores.",

    # --- Logs - QR/Código de barras (barcode_qr.py) ---
    "log_qr_empty_data": "Intento de generar código QR para datos vacíos.",
    "log_qr_generated": "SVG de código QR generado para: {0}...",
    "log_qr_error": "Error al generar código QR para datos '{0}': {1}",
    "log_barcode_empty_data": "Intento de generar código de barras para datos vacíos.",
    "log_barcode_generated": "SVG de código de barras generado para: {0}...",
    "log_barcode_error": "Error al generar código de barras para datos '{0}': {1}",
    "log_basic_handler_configured": "Controlador básico configurado para el registrador en barcode_qr.py",
    "log_basic_handler_error": "Fallo al configurar el controlador básico en barcode_qr: {0}",

    # --- Logs - Config/Perfiles (main_config_manager.py) ---
    "loading_profiles_from": "Cargando perfiles desde",
    "profiles_file": "Archivo de perfiles",
    "does_not_contain_dict": "no contiene un diccionario. Creando uno nuevo",
    "not_found_creating_new": "no encontrado. Creando uno nuevo vacío",
    "json_profiles_read_error": "Error al leer el archivo JSON de perfiles",
    "file_will_be_overwritten": "El archivo será sobrescrito al guardar",
    "json_decode_error_in_profiles": "Error de decodificación JSON en el archivo de perfiles",
    "cannot_load_profiles_file": "No se puede cargar el archivo de perfiles",
    "unexpected_profiles_read_error": "Error inesperado al leer los perfiles",
    "saving_profiles_to": "Guardando perfiles en",
    "cannot_save_profiles_file": "No se puede guardar el archivo de perfiles",
    "profiles_save_error": "Error al guardar perfiles en el archivo",
    "logger_profile_saved": "Perfil guardado: {profile}",
    "logger_profile_not_found": "Perfil no encontrado para cargar: {profile}",
    "logger_profile_loaded": "Perfil cargado: {profile}",
    "logger_profile_delete_not_exist": "Intento de eliminar un perfil inexistente: {profile}",
    "logger_profile_deleted": "Perfil eliminado: {profile}",
    "logger_start_save_settings": "Se inició el guardado de la configuración desde la GUI.",
    "logger_invalid_value": "Valor inválido para '{key}'. Establecido a 0.0.",
    "logger_end_save_settings": "Finalizado el guardado de la configuración desde la GUI.",
    "logger_conversion_error": "Error de conversión de valores desde la GUI: {error}",
    "conversion_failed": "Falló la conversión de valores de la GUI",
    "logger_unexpected_save_error": "Error inesperado al guardar la configuración: {error}",
    "logger_settings_saved": "Configuración guardada en el archivo: {file}",

    # --- Logs - Licenciamiento (main_license.py) ---
    "public_key_load_error_log": "Error al cargar la clave pública",
    "license_key_decode_error": "Error al decodificar la clave de licencia",
    "license_activation_error": "Error de activación de licencia",

    # --- Logs - Módulo principal (main.py) ---
    "ui_created": "La interfaz de usuario ha sido creada.",
    "error_tab_home": "Error al crear la interfaz de 'Inicio'",
    "error_tab_settings": "Error al crear la interfaz de 'Configuración'",
    "error_tab_help": "Error al crear la interfaz de 'Ayuda'",
    "error_creating_license_ui": "Error al crear la interfaz de 'Licencia'",
    "error_loading_ui": "Error general al cargar la interfaz: {error}",
    "error_creating_home_ui": "Error al crear la interfaz de 'Inicio'",
    "error_creating_settings_ui": "Error al crear la interfaz de 'Configuración'",
    "error_creating_help_ui": "Error al crear la interfaz de 'Ayuda'",
    "logger_update_gui": "Se inició la actualización de la GUI desde la configuración.",
    "logger_end_update_gui": "Finalizada la actualización de la GUI desde la configuración.",
    "logger_update_gui_error": "Error inesperado al actualizar la GUI: {error}",
    "logger_invalid_output_dir": "Directorio de salida inválido o inexistente: {directory}",
    "logger_invalid_input_file": "Archivo de entrada inválido o inexistente: {file}",
    "logger_start_pdf": "Se inició el proceso de generación de PDF.",
    "logger_pdf_save_error": "Generación de PDF abortada: fallo al guardar la configuración actual.",
    "logger_pdf_success": "Generación de PDF completada correctamente.",
    "logger_pdf_exception": "Excepción durante el proceso principal de generación de PDF.",
    "icon_set_error": "Fallo al establecer el icono de la aplicación: {error}",
    "accent_button_style_error": "Fallo al establecer el estilo del botón de acento: {error}",
    "logger_file_save_error": "Error al guardar archivo {file}: {error}",

    #   Logs - Vista previa (main.py - update_preview, update_output_preview)
    "thumbnail_error_log": "Error al generar miniatura",
    "output_preview_update_called": "Se llamó a la actualización de la vista previa de salida",
    "output_preview_canvas_missing": "Falta el canvas de la vista previa de salida",
    "pdf_found_in_output_dir": "Se encontró PDF en el directorio de salida",
    "preparing_thumbnail": "Preparando miniatura",
    "thumbnail_generated_successfully": "Miniatura generada correctamente",
    "thumbnail_generation_error": "Error de generación de miniatura para",
    "no_pdf_for_common_sheet": "No hay archivo PDF para la vista previa de hoja común",
    "no_pdf_for_separate_files": "No hay archivos PDF generados para la vista previa",
    "cannot_load_thumbnail": "No se puede cargar la miniatura desde",

    #   Logs - Desarrollador / Internos de GUI (main.py)
    "missing_gui_var_created": "Variable de GUI faltante creada para la clave: {key}",
    "missing_gui_structure_created": "Estructura de GUI faltante creada para: {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Variable de GUI faltante creada para: {code_type}/{output_type}/{layout}/{param}",

    # Claves adicionales para main_ui_help.py
    "help_text": """
    Billboard Splitter – Guía de usuario\n\n
    Propósito del programa:\n
    Billboard Splitter se utiliza para cortar automáticamente proyectos de vallas publicitarias en paneles listos para imprimir.
    El programa está preparado para trabajar con archivos diseñados a escala 1:10.\n
    Los valores en las secciones: Solape, Franja blanca y Configuración se introducen a escala 1:1.
    El programa permite disponer los paneles cortados en hojas PDF según la disposición seleccionada:\n
    • Hoja común: Todos los paneles se colocan en un único documento.\n
    • Archivos separados: Cada panel se guarda en un archivo PDF independiente.\n\n
    Adicionalmente el programa permite:\n
    • Elegir la disposición – vertical u horizontal (en vertical las líneas de separación aparecen arriba y abajo,
      y en horizontal en los lados izquierdo y derecho).\n
    • Rotar los paneles 180° (invertir todo el proyecto).\n
    • Añadir marcas de registro (p. ej., cruces o líneas) para facilitar el posicionamiento preciso durante el pegado.\n
    • Añadir códigos QR o códigos de barras – generados a partir de datos de entrada para ayudar
      a identificar paneles individuales.\n
    • Guardar configuraciones como perfiles que se pueden cargar, modificar y eliminar, facilitando
      el cambio entre distintas configuraciones de proyecto.\n\n
    Pasos principales para usar el programa:\n\n
    1. Elige el archivo de entrada:\n
    • En la pestaña 'Inicio' elige un archivo PDF, JPG o TIFF que contenga el diseño de la valla.\n
    • Si no estableces tu propia ruta, el programa define un archivo de muestra por defecto.\n\n
    2. Configuración de corte:\n
    • Especifica el número de filas y columnas en las que se dividirá el proyecto.\n
    • Define el tamaño del solape.\n
    • Opcionalmente indica el ancho de la franja blanca que se añadirá al solape efectivo.\n\n
    3. Selecciona la disposición de salida:\n
    • Vertical: Todos los paneles se dispondrán verticalmente en la hoja PDF.\n
    • Horizontal: Todos los paneles se dispondrán horizontalmente en la hoja PDF.\n\n
    4. Selecciona el tipo de salida:\n
    • Hoja común: Todos los paneles se colocan en un único PDF.\n
    • Archivos separados: Cada panel se guarda en un PDF independiente.\n
    • En la pestaña 'Inicio' puedes habilitar y configurar marcas de registro – elegir entre cruz y línea.\n
    • Opcionalmente habilita un código QR o un código de barras que se generará a partir de los datos del proyecto.\n
    • Los parámetros del código (escala, desplazamiento, rotación, posición) se pueden afinar en la pestaña 'Configuración'.\n\n
    5. Gestión de configuraciones:\n
    • En la pestaña 'Configuración' puedes modificar con precisión los parámetros gráficos (márgenes, grosores de línea, espacios) y
      la configuración de los códigos.\n
    • Guarda la configuración actual como un perfil para poder cargarla o modificarla más tarde.\n
    • Los perfiles de configuración (guardados en el archivo profiles.json) permiten cambiar rápidamente entre distintas
      configuraciones de proyecto.\n\n
    6. Generación de PDF:\n
    • Después de configurar todos los parámetros, haz clic en 'Generar PDF'.\n
    • Los archivos resultantes se guardarán en el directorio 'output' u otro indicado, y los logs (con rotación diaria) en el directorio 'logs'
      u otro indicado.\n\n
    Si surgen problemas:\n
    • Revisa los logs ubicados en la carpeta 'logs'. Cada día se genera un archivo de log con la fecha en su nombre.\n
    • Asegúrate de que todas las carpetas requeridas estén definidas.\n
    • Soporte técnico: tech@printworks.pl (días laborables, 8-16)\n
    """
}
