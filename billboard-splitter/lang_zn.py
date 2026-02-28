# lang_zh_cn.py
"""
简体中文语言文件 / Simplified Chinese language file.
约定：将“bryt”统一译为“面板（panel）”以保持术语一致。
"""

LANG = {
    "barcode_font_size_label": "条形码描述字体大小[pt]:",
    # ==========================
    #  应用 - 通用
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "错误",
    "no_file": "没有文件",
    "language": "语言",
    "language_switch": "语言切换",
    "choose_language": "选择语言：",
    "apply_language": "应用",
    "language_changed": "语言已更改。部分变更将在重新启动应用后生效。",

    # ========================================
    #  用户界面（GUI）元素
    # ========================================

    # --- 主选项卡 ---
    "tab_home": " 首页 ",
    "tab_settings": " 设置 ",
    "tab_help": " 帮助 ",
    "tab_license": " 许可 ",

    # --- 通用按钮 ---
    "button_browse": "浏览…",
    "browse_folder": "浏览文件夹…",
    "button_save": "保存",
    "button_delete": "删除",
    "button_close": "关闭",
    "save_all_settings": "保存所有设置",

    # --- 字段标签（首页） ---
    "label_rows": "纵向切分（行）：",
    "label_columns": "横向切分（列）：",
    "label_overlap": "搭接（cm）：",
    "label_white_stripe": "白边（cm）：",
    "label_add_white_stripe": "将白边加入有效搭接",  # 复选框
    "label_layout": "输出排版：",
    "label_output_type": "输出类型：",
    "label_enable_reg_marks": "启用定位标记：",
    "label_enable_codes": "启用编码：",
    "label_enable_sep_lines": "启用分隔线（面板之间）",
    "label_enable_start_line": "启用纸张开始/顶部线",
    "label_enable_end_line": "启用纸张结束/底部线",
    "label_bryt_order": "面板顺序：",
    "label_slice_rotation": "面板旋转：",
    "label_create_order_folder": "创建包含订单号的文件夹",

    # --- 分区/框（首页） ---
    "section_input_file": " 输入文件 ",
    "section_scale_and_dimensions": " 缩放和输出尺寸 ",
    "label_original_size": "原始尺寸:",
    "label_scale_non_uniform": "非均匀缩放",
    "label_scale": "比例: 1:",
    "label_scale_x": "比例 X: 1:",
    "label_scale_y": "比例 Y: 1:",
    "label_output_dimensions": "输出文件尺寸:",
    "label_width_cm": "宽度 [厘米]:",
    "label_height_cm": "高度 [厘米]:",
    "section_split_settings": " 切分设置 ",
    "section_profiles": " 设置配置 ",
    "section_save_location": " 保存位置 ",
    "section_input_preview": " 输入文件预览 ",
    "section_output_preview": " 输出文件预览 ",

    # --- 选项值（下拉/单选等） ---
    "layout_vertical": "纵向",
    "layout_horizontal": "横向",
    "output_common_sheet": "公共拼版",
    "output_separate_files": "独立文件",
    "output_both": "公共拼版与独立文件",
    "output_common": "公共拼版",
    "output_separate": "独立文件",
    "reg_mark_cross": "十字",
    "reg_mark_line": "直线",
    "code_qr": "QR 码",
    "code_barcode": "条码",
    "bryt_order_1": "A1-An, B1-Bn，标准，自上而下",
    "bryt_order_2": "A1-An, Bn-B1，按行蛇形，自上而下",
    "bryt_order_3": "A1..B1, A2..B2，按列，自上而下",
    "bryt_order_4": "A1-A2..B2-B1，按列蛇形，自上而下",
    "bryt_order_5": "N1-Nn, (N-1)1-(N-1)n，标准，自下而上",
    "bryt_order_6": "N1-Nn, (N-1)n-(N-1)1，按行蛇形，自下而上",
    "logging_console": "控制台",
    "logging_file": "文件",
    "logging_both": "二者皆用",

    # --- 分区/框（设置页） ---
    "section_processing_mode": " 切割操作 ",
    "processing_mode_ram": "内存模式（RAM）",
    "processing_mode_hdd": "磁盘模式（HDD）",
    "graphic_settings": "图形设置",
    "code_settings": "二维码 / 条码设置",
    "logging_settings": "日志设置",
    "barcode_text_position_label": "条码文字位置：",
    "barcode_text_bottom": "下方",
    "barcode_text_side": "侧边",
    "barcode_text_none": "无",

    # --- 字段标签（设置页 - 图形） ---
    "extra_margin_label": "面板外边距（cm）：",
    "margin_top_label": "上边距（cm）：",
    "margin_bottom_label": "下边距（cm）：",
    "margin_left_label": "左边距（cm）：",
    "margin_right_label": "右边距（cm）：",
    "reg_mark_width_label": "定位标记 - 宽度（cm）：",
    "reg_mark_height_label": "定位标记 - 高度（cm）：",
    "reg_mark_white_line_width_label": "定位标记 - 白线粗细（cm）：",
    "reg_mark_black_line_width_label": "定位标记 - 黑线粗细（cm）：",
    "sep_line_black_width_label": "分隔线 - 黑线粗细（cm）：",
    "sep_line_white_width_label": "分隔线 - 白线粗细（cm）：",
    "slice_gap_label": "面板间距（cm）：",
    "label_draw_slice_border": "绘制面板边框（裁切线）",

    # --- 字段标签（设置页 - 编码） ---
    "scale_label": "尺寸（cm）：",
    "scale_x_label": "宽度 X（cm）：",
    "scale_y_label": "高度 Y（cm）：",
    "offset_x_label": "偏移 X（cm）：",
    "offset_y_label": "偏移 Y（cm）：",
    "rotation_label": "旋转（°）：",
    "anchor_label": "基准角：",

    # --- 字段标签（设置页 - 日志） ---
    "logging_mode_label": "日志模式：",
    "log_file_label": "日志文件：",
    "logging_level_label": "日志级别：",

    # --- 按钮 / 动作（首页） ---
    "button_load": "加载",
    "button_save_settings": "保存当前设置",
    "button_generate_pdf": "生成 PDF",
    "button_refresh_preview": "刷新预览",
    "button_refresh_layout": "刷新排版",

    # --- 许可（GUI） ---
    "hwid_frame_title": "硬件唯一标识（HWID）",
    "copy_hwid": "复制 HWID",
    "license_frame_title": "许可激活",
    "enter_license_key": "输入许可密钥：",
    "activate": "激活",
    "status_trial": "试用模式",
    "license_active": "许可已激活",

    # ================================================
    #  用户消息（窗口 / 状态栏）
    # ================================================

    # --- 配置 ---
    "msg_no_profile_name": "无名称",
    "msg_enter_profile_name": "请输入要保存的配置名称。",
    "msg_profile_saved": "配置已保存",
    "profile_saved_title": "配置已保存",
    "msg_profile_saved_detail": "配置“{0}”已保存。",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "配置文件 '{profile}' 已保存并应用。",
    "msg_no_profile": "没有配置",
    "warning_no_profile": "没有配置",
    "msg_select_profile": "请从列表选择要加载的配置名称。",
    "select_profile": "请从列表选择要加载的配置名称。",
    "profile_loaded_title": "配置已加载",
    "profile_loaded": "配置“{profile}”已加载。",
    "warning_no_profile_delete": "没有配置",
    "warning_no_profile_delete_message": "请从列表选择要删除的配置。",
    "profile_not_found": "未找到配置“{profile}”。",
    "profile_not_exist": "配置“{profile}”不存在。",
    "confirm_delete_title": "确认删除",
    "confirm_delete_profile": "确定要删除配置“{profile}”吗？",
    "profile_deleted_title": "配置已删除",
    "profile_deleted": "配置“{profile}”已删除。",

    # --- 文件 / 目录 ---
    "msg_no_input_file": "没有输入文件",
    "msg_unsupported_format": "不支持的格式",
    "select_file_title": "选择输入文件",
    "supported_files": "支持的文件",
    "all_files": "所有文件",
    "select_dir_title": "选择输出目录",
    "select_log_dir_title": "选择日志目录",
    "error_output_dir_title": "输出目录错误",
    "error_output_dir": "指定的输出目录无效或不存在：\n{directory}",
    "error_input_file_title": "输入文件错误",
    "error_input_file": "指定的输入文件无效或不存在：\n{file}",
    "save_file_error_title": "文件保存错误",
    "save_file_error": "保存文件失败：{error}",

    # --- PDF 处理 / 预览 ---
    "msg_pdf_processing_error": "处理 PDF 文件失败",
    "msg_thumbnail_error": "缩略图加载错误",
    "msg_no_pdf_output": "没有 PDF 输出",
    "no_pdf_pages": "PDF 文件没有页面",
    "unsupported_output": "不支持该输出类型的预览",
    "pdf_generated_title": "生成完成",
    "pdf_generated": "PDF 文件已成功生成并保存在目录：\n{directory}",
    "pdf_generation_error_title": "生成错误",
    "pdf_generation_error": "生成 PDF 时发生错误。请查看日志以获取更多信息。",
    "critical_pdf_error_title": "PDF 生成严重错误",
    "critical_pdf_error": "生成 PDF 时发生严重错误：\n{error}\n请检查日志。",

    # --- 设置 ---
    "settings_saved_title": "设置已保存",
    "settings_saved": "设置已保存至文件：\n{filepath}",
    "settings_save_error_title": "设置保存错误",
    "settings_save_error": "保存设置失败：{error}",
    "conversion_error_title": "转换错误",
    "conversion_error": "从界面转换值时发生错误：{error}",
    "update_gui_error_title": "界面更新错误",
    "update_gui_error": "更新界面时发生错误：{error}",

    # --- 许可 ---
    "hwid_copied_to_clipboard": "HWID 已复制到剪贴板",
    "computer_hwid": "计算机 HWID",
    "public_key_load_error": "加载公钥出错：{error}",
    "invalid_license_format": "许可密钥格式无效：{error}",
    "activation_success": "许可已成功激活。",
    "activation_error": "许可激活错误：{error}",
    "log_trial_mode_active": "试用模式已启用",
    "log_trial_mode_inactive": "试用模式未启用",

    # --- 初始化 ---
    "init_error_title": "初始化错误",
    "init_error": "初始化目录时出错：{error}",
    "poppler_path_info": "Poppler 路径信息",
    "ttkthemes_not_installed": "警告：未安装 ttkthemes。将使用默认 Tkinter 样式。",

    # =====================================
    #  日志（Logger 消息）
    # =====================================

    # --- 日志 - 通用 / 配置 ---
    "log_configured": "日志已配置：level={0}, mode={1}, file={2}",
    "log_no_handlers": "警告：未配置日志处理器（mode: {0}）。",
    "log_critical_error": "日志配置严重错误：{0}",
    "log_basic_config": "发生错误，已使用基础日志配置。",
    "log_dir_create_error": "严重错误：无法创建日志目录 {0}：{1}",

    # --- 日志 - 初始化 / 目录（init_directories.py） ---
    "error_critical_init": "初始化期间发生严重错误：{0}",
    "logger_init_error": "目录初始化错误：{error}",
    "directory_created": "已创建目录：{0}",
    "directory_creation_error": "创建目录失败 {0}：{1}",
    "sample_file_copied": "示例文件已复制到 {0}",
    "sample_file_copy_error": "复制示例文件出错：{0}",
    "log_created_output_dir": "已创建输出目录：{0}",
    "log_cannot_create_output_dir": "无法创建输出目录 {0}：{1}",

    # --- 日志 - 分割器（splitter.py） ---
    #   分割器 - 初始化与加载
    "log_graphic_settings_error": "初始化期间加载图形设置失败：{0}",
    "log_loading_pdf": "正在加载 PDF 文件：{0}",
    "log_loading_bitmap": "正在加载位图文件：{0}",
    "log_invalid_dpi": "读取到无效 DPI（{0}）。使用默认 {1} DPI。",
    "log_image_dimensions": "图像尺寸：{0}x{1}px，模式：{2}，DPI：{3:.1f} -> {4:.3f}x{5:.3f}pt",
    "log_image_processing_color": "按原始颜色模式处理图像：{0}",
    "log_unusual_color_mode": "非常见图像模式：‘{0}’。ReportLab/Pillow 可能无法正确处理。",
    "log_draw_image_error": "ReportLab drawImage 处理模式 {0} 时出错：{1}",
    "log_unsupported_format": "不支持的输入文件格式：{0}",
    "log_input_file_not_found": "未找到输入文件：{0}",
    "log_load_process_error": "加载或处理文件 {0} 时发生错误：{1}",
    "log_input_file_not_exists": "输入文件不存在或路径为空：‘{0}’",
    "log_cannot_load_or_empty_pdf": "无法加载输入文件，或 PDF 为空/损坏。",
    "log_pdf_dimensions_info": "  PDF 尺寸：{0:.1f}mm × {1:.1f}mm",
    "log_invalid_pdf_dimensions": "PDF 页面尺寸无效：{0}×{1} pt。",

    #   分割器 - 尺寸计算
    "log_extra_margin": "额外边距设置为 {0:.3f} pt",
    "log_invalid_rows_cols": "无效的行数（{0}）或列数（{1}）。",
    "error_invalid_rows_cols": "行与列必须是正整数。",
    "log_invalid_overlap_white_stripe": "无效的搭接（{0}）或白边（{1}）值。必须是数字。",
    "error_invalid_overlap_white_stripe": "搭接与白边必须是数值（mm）。",
    "log_stripe_usage": "设置 use_white_stripe={0}，white_stripe={1:.3f} mm",
    "log_effective_overlap": "基础搭接（图形）：{0:.3f} mm，白边：{1:.3f} mm，有效搭接：{2:.3f} mm",
    "log_computed_dimensions": "计算尺寸：PDF：{0:.3f}mm × {1:.3f}mm。面板：{2:.3f}pt（{3:.3f}mm） × {4:.3f}pt（{5:.3f}mm）。核心：{6:.3f}pt × {7:.3f}pt。有效搭接：{8:.3f}mm",
    "log_invalid_dimensions": "计算得到的面板（{0:.3f}×{1:.3f}）或核心（{2:.3f}×{3:.3f}）尺寸无效，overlap={4}，stripe={5}，r={6}，c={7}，W={8}mm，H={9}mm",
    "error_invalid_slice_dimensions": "面板/核心尺寸无效或为负。",

    #   分割器 - 生成面板信息与顺序
    "log_generating_slice_info": "正在生成面板信息：{0}",
    "log_no_slices_info_generated": "未能生成面板信息。",
    "log_applying_rotated_order": "应用 180° 旋转顺序：{0}",
    "log_applying_standard_order": "应用 0° 旋转顺序（标准）：{0}",
    "log_unknown_bryt_order": "未知的面板顺序：‘{0}’。已使用默认值。",
    "log_final_slices_order": "  最终面板顺序（{0}）：[{1}]",

    #   分割器 - 叠加与合并
    "log_invalid_dimensions_overlay": "尝试以无效尺寸创建叠加：{0}。已跳过。",
    "log_empty_overlay": "创建了空或近乎空的叠加 PDF。已跳过合并。",
    "log_overlay_error": "创建叠加 PDF 出错：{0}",
    "log_merge_error": "尝试合并不含页面的叠加。已跳过。",
    "log_merge_page_error": "合并叠加 PDF 时出错：{0}",
    "log_fallback_draw_rotating_elements": "无法获取 _draw_rotating_elements 的行/列，已使用 1×1。",
    "log_overlay_created_for_slice": "已为面板 {0} 创建白边/标记叠加",
    "log_overlay_creation_failed_for_slice": "为 {0} 创建白边/标记叠加失败",
    "log_merging_rotated_overlay": "正在为 {0} 合并【旋转】白边/标记叠加，T={1}",
    "log_merging_nonrotated_overlay": "正在为 {0} 合并【未旋转】白边/标记叠加",
    "log_merging_all_codes_overlay": "正在合并所有编码叠加（不旋转）",
    "log_merging_separation_lines_overlay": "正在合并分隔线叠加（不旋转）",
    "log_merging_code_overlay_for_slice": "已为 {0} 合并编码叠加（不旋转）。",
    "log_merging_separation_overlay_for_slice": "已为 {0} 合并分隔线叠加（不旋转）。",

    #   分割器 - 绘制图形元素（白边、标记、线）
    "log_drawing_top_stripe": "[Canvas 绘制] 为 {0} 绘制顶部白边：x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas 绘制] 为 {0} 绘制右侧白边：x={1:.3f}, y={2:.3f}, w={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas 绘制] 为 {0} 填充并描边拐角 @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "绘制中心十字 @ ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "为 {0} 绘制定位线，区域：({1:.3f},{2:.3f}) 起",
    "log_drawing_right_vertical_line": "  绘制右侧竖线：x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  绘制顶部横线：y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "绘制分隔线（黑底白线）：({0}) @ ({1:.3f}, {2:.3f})，长度={3:.3f}",
    "log_drawing_reg_marks_for_slice": "为 {0} [{1},{2}] / [{3},{4}] 绘制十字，区域起点：({5:.1f},{6:.1f})",
    "log_coord_calculation": "  计算中心：TL({0:.1f},{1:.1f})，TR({2:.1f},{3:.1f})，BL({4:.1f},{5:.1f})，BR({6:.1f},{7:.1f})",
    "log_drawing_tl": "    绘制 TL @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    绘制 TR @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    绘制 BL @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    绘制 BR @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    根据位置规则省略 {0}，坐标 [{1},{2}]",
    "log_trial_common_sheet": "在公共拼版上应用 TRIAL 水印文本",

    # 水印
    "log_trial_watermark_added": "已添加 TRIAL 水印",
    "error_drawing_trial_text": "绘制水印时出错：{error}",

    #   分割器 - 整页分隔线
    "log_drawing_separation_lines_for_page": "为页面绘制分隔线（layout={0}, total_slices={1}, slice_index={2}）",
    "log_vertical_line_between_slices": "  面板 {0}-{1} 之间竖线 @ x={2:.1f}",
    "log_vertical_line_start": "  竖线起点 @ x={0:.1f}",
    "log_vertical_line_end": "  竖线终点 @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  面板 {0}-{1} 之间横线 @ y={2:.1f}",
    "log_horizontal_line_start": "  横线起点 @ y={0:.1f}",
    "log_horizontal_line_end": "  横线终点 @ y={0:.1f}",
    "log_sep_line_start_separate": "  （独立文件）竖/横线起点 @ {0:.1f}",
    "log_sep_line_end_separate": "  （独立文件）竖/横线终点 @ {0:.1f}",

    #   分割器 - 生成条码 / QR
    "log_generate_barcode_data": "生成编码数据：{0}",
    "log_barcode_data_shortened": "编码数据已缩短至 {0} 个字符。",
    "log_barcode_data_error": "生成编码数据时出错：{0}",
    "log_compose_barcode_payload": "组装编码载荷（{0}）：{1}",
    "log_barcode_payload_shortened": "载荷已缩短至 {0} 个字符（格式 {1}）",
    "log_barcode_payload_error": "组装载荷时出错：{0}",
    "log_unknown_anchor_fallback": "未知基准角‘{0}’，已使用左下角。",
    "log_used_default_code_settings": "编码 {0}/{1} 使用默认设置。",
    "log_no_layout_key_fallback": "没有 {1}/{2} 的布局‘{0}’。已使用首个可用布局：‘{3}’",
    "log_code_settings_error": "未找到或获取编码设置（{0}/{1}/{2}）时出错：{3}。已使用默认值。",
    "log_drawing_barcode": "在 ({1:.3f}, {2:.3f}) 绘制 {0} [基准 ({3:.3f}, {4:.3f}) + 偏移 ({5:.3f}, {6:.3f})]，旋转：{7}°",
    "error_generate_qr_svg": "生成 QR 码 SVG 失败。",
    "error_invalid_scale_for_qr": "QR 尺寸无效：{0}mm",
    "error_invalid_qr_scale_factor": "QR 缩放系数无效：{0}",
    "error_generate_barcode_svg": "生成条码 SVG 失败。",
    "error_invalid_scale_for_barcode": "条码尺寸无效：{0}×{1}mm",
    "error_invalid_barcode_scale_factor": "条码缩放系数无效：({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0}：配置尺寸={1:.3f}mm，SVG 宽度={2:.3f}pt，sf={3:.4f}",
    "log_barcode_scale_code128": "  {0}：配置尺寸=({1:.3f}mm, {2:.3f}mm)，SVG 尺寸=({3:.3f}pt, {4:.3f}pt)，sf=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "绘制编码‘{0}’时出错：{1}",
    "log_prepared_barcode_info": "已为 {0} 准备编码信息（{1}, anchor={2}）：绝对基准位置 ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "为 {0} 准备编码数据时出错：{1}",
    "log_drawing_barcodes_count": "正在绘制 {0} 个条码/QR 码…",
    "log_missing_barcode_info_key": "绘制时编码信息缺少键：{0}。信息：{1}",
    "log_error_drawing_barcode_in_draw_all": "在 _draw_all_barcodes 中绘制编码‘{0}’时出错：{1}",

    #   分割器 - 切分流程（split_* 方法）
    "log_start_splitting_process": "--- 开始切分：{0} ---",
    "log_split_settings": "  设置：{0}×{1} 面板，搭接={2}mm，白边={3}mm（+搭接：{4}）",
    "log_output_dir_info": "  输出：{0} / {1} 到 ‘{2}’",
    "log_lines_marks_barcodes_info": "  线：分隔={0}，起始={1}，结束={2} | 标记：{3}（{4}），编码：{5}（{6}）",
    "log_bryt_order_info": "  顺序：{0}，面板旋转：{1}°",
    "log_invalid_dimensions_in_slice_info": "面板 {0} 的 slice_info 尺寸无效：{1}×{2}",
    "log_content_transform": "{0} 的内容变换 T_content：{1}",
    "log_merged_content_for_slice": "已在 new_page 上合并面板 {0} 的内容",
    "log_slice_reader_created": "已为面板 {0} 创建完整 PdfReader",
    "log_slice_reader_creation_error": "为面板 {0} 创建完整内容失败：{1}",
    "log_used_get_transform": "使用 _get_transform（仅平移）：x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- 开始：独立文件（旋转在 create_slice_reader 中处理） ---",
    "log_creating_file_for_slice": "为面板 {0} 创建文件：{1}",
    "log_invalid_page_size_for_slice": "页面尺寸无效（{0}×{1}），目标：{2}。已跳过。",
    "log_blank_page_creation_error": "为 {0} 创建页面（{1}×{2}）时出错：{3}。已跳过。",
    "log_transform_for_slice": "{0} 的平移变换 T：{1}",
    "log_merging_complete_slice": "合并完整面板 {0}，变换：{1}",
    "log_skipped_slice_merging": "已跳过合并面板 {0}。",
    "log_file_saved": "文件已保存：{0}",
    "log_file_save_error": "文件保存错误 {0}：{1}",
    "log_finished_split_separate_files": "--- 完成：独立文件（已保存 {0}/{1}） ---",
    "log_no_slices_split_horizontal": "split_horizontal 中没有可处理的面板。",
    "log_start_split_horizontal": "--- 开始：公共拼版 - 横向（旋转在 create_slice_reader 中处理） ---",
    "log_page_dimensions": "页面尺寸：{0:.1f}mm × {1:.1f}mm（{2} 个面板）",
    "log_page_creation_error": "创建结果页面（{0}×{1}）时出错：{2}。已中止。",
    "log_slice_at_position": "面板 {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "仅平移变换 T（{0}）：{1}",
    "log_merging_complete_bryt": "合并完整面板 {0}，变换：{1}",
    "log_skipped_merging_bryt": "已跳过合并面板 {0}。",
    "log_file_result_saved": "结果文件已保存：{0}",
    "log_file_result_save_error": "结果文件保存错误 {0}：{1}",
    "log_finished_split_horizontal": "--- 完成：公共拼版 - 横向 ---",
    "log_no_slices_split_vertical": "split_vertical 中没有可处理的面板。",
    "log_start_split_vertical": "--- 开始：公共拼版 - 纵向（旋转在 create_slice_reader 中处理） ---",
    "log_finished_split_vertical": "--- 完成：公共拼版 - 纵向 ---",
    "log_unknown_layout": "未知公共拼版布局：‘{0}’",
    "log_unknown_output_type": "未知输出类型：‘{0}’",
    "log_finished_splitting_success": "--- 完成切分：{0} - 成功 ---",
    "log_finished_splitting_errors": "--- 完成切分：{0} - 出现错误 ---",
    "log_value_error_in_splitting": "输入数据或计算错误：{0}",
    "log_finished_splitting_critical_error": "--- 完成切分：{0} - 严重错误 ---",
    "log_unexpected_error_in_splitting": "切分文件 {0} 时发生意外错误：{1}",

    #   分割器 - 测试模式（__main__）
    "log_script_mode_test": "splitter.py 以主脚本（测试模式）运行。",
    "log_loaded_config": "已加载配置。",
    "log_error_loading_config": "加载配置失败：{0}",
    "log_created_example_pdf": "已创建示例 PDF 文件：{0}",
    "log_cannot_create_example_pdf": "创建示例 PDF 失败：{0}",
    "log_start_test_split": "开始测试切分：{0} -> {1}",
    "log_test_split_success": "测试切分成功完成。",
    "log_test_split_errors": "测试切分完成，但存在错误。",

    # --- 日志 - QR/条码（barcode_qr.py） ---
    "log_qr_empty_data": "尝试为空数据生成 QR 码。",
    "log_qr_generated": "已为 {0}… 生成 QR 码 SVG",
    "log_qr_error": "为数据‘{0}’生成 QR 码时出错：{1}",
    "log_barcode_empty_data": "尝试为空数据生成条码。",
    "log_barcode_generated": "已为 {0}… 生成条码 SVG",
    "log_barcode_error": "为 {0} 生成条码时出错：{1}",
    "log_basic_handler_configured": "barcode_qr.py 已配置基础日志处理器",
    "log_basic_handler_error": "在 barcode_qr 中配置基础日志处理器失败：{0}",

    # --- 日志 - 配置/配置文件（main_config_manager.py） ---
    "loading_profiles_from": "从此处加载配置",
    "profiles_file": "配置文件",
    "does_not_contain_dict": "不包含字典。将创建一个新的。",
    "not_found_creating_new": "未找到。将创建一个空的。",
    "json_profiles_read_error": "读取 JSON 配置文件出错",
    "file_will_be_overwritten": "保存时将覆盖该文件",
    "json_decode_error_in_profiles": "配置文件 JSON 解码错误",
    "cannot_load_profiles_file": "无法加载配置文件",
    "unexpected_profiles_read_error": "读取配置时出现意外错误",
    "saving_profiles_to": "保存配置到",
    "cannot_save_profiles_file": "无法保存配置文件",
    "profiles_save_error": "保存配置到文件时出错",
    "logger_profile_saved": "配置已保存：{profile}",
    "logger_profile_not_found": "要加载的配置未找到：{profile}",
    "logger_profile_loaded": "配置已加载：{profile}",
    "logger_profile_delete_not_exist": "尝试删除不存在的配置：{profile}",
    "logger_profile_deleted": "配置已删除：{profile}",
    "logger_start_save_settings": "开始从 GUI 保存设置。",
    "logger_invalid_value": "‘{key}’ 的值无效，已设为 0.0。",
    "logger_end_save_settings": "完成从 GUI 保存设置。",
    "logger_conversion_error": "从 GUI 转换值出错：{error}",
    "conversion_failed": "GUI 值转换失败",
    "logger_unexpected_save_error": "保存设置时出现意外错误：{error}",
    "logger_settings_saved": "设置已保存到文件：{file}",

    # --- 日志 - 许可（main_license.py） ---
    "public_key_load_error_log": "公钥加载错误",
    "license_key_decode_error": "许可密钥解码错误",
    "license_activation_error": "许可激活错误",

    # --- 日志 - 主模块（main.py） ---
    "ui_created": "用户界面已创建。",
    "error_tab_home": "创建“首页”选项卡 UI 时出错",
    "error_tab_settings": "创建“设置”选项卡 UI 时出错",
    "error_tab_help": "创建“帮助”选项卡 UI 时出错",
    "error_creating_license_ui": "创建“许可”选项卡 UI 时出错",
    "error_loading_ui": "加载界面出错：{error}",
    "error_creating_home_ui": "创建“首页”选项卡 UI 时出错",
    "error_creating_settings_ui": "创建“设置”选项卡 UI 时出错",
    "error_creating_help_ui": "创建“帮助”选项卡 UI 时出错",
    "logger_update_gui": "开始从配置更新 GUI。",
    "logger_end_update_gui": "完成从配置更新 GUI。",
    "logger_update_gui_error": "更新 GUI 时出现意外错误：{error}",
    "logger_invalid_output_dir": "输出目录无效或不存在：{directory}",
    "logger_invalid_input_file": "输入文件无效或不存在：{file}",
    "logger_start_pdf": "开始 PDF 生成过程。",
    "logger_pdf_save_error": "PDF 生成中止——保存当前设置失败。",
    "logger_pdf_success": "PDF 生成成功完成。",
    "logger_pdf_exception": "主 PDF 生成过程中产生异常。",
    "icon_set_error": "设置应用图标失败：{error}",
    "accent_button_style_error": "设置强调按钮样式失败：{error}",
    "logger_file_save_error": "文件保存错误 {file}：{error}",

    #   日志 - 预览（main.py - update_preview, update_output_preview）
    "thumbnail_error_log": "缩略图生成错误",
    "output_preview_update_called": "已调用输出预览更新",
    "output_preview_canvas_missing": "缺少输出预览画布",
    "pdf_found_in_output_dir": "在输出目录中找到 PDF",
    "preparing_thumbnail": "正在准备缩略图",
    "thumbnail_generated_successfully": "缩略图生成成功",
    "thumbnail_generation_error": "生成缩略图时出错：",
    "no_pdf_for_common_sheet": "没有用于公共拼版预览的 PDF 文件",
    "no_pdf_for_separate_files": "没有生成用于预览的独立 PDF 文件",
    "cannot_load_thumbnail": "无法从此处加载缩略图：",

    #   日志 - 开发者 / GUI 内部（main.py）
    "missing_gui_var_created": "已为键 {key} 创建缺失的 GUI 变量",
    "missing_gui_structure_created": "已为 {code_type}/{output_type}/{layout} 创建缺失的 GUI 结构",
    "missing_gui_var_detailed_created": "已为 {code_type}/{output_type}/{layout}/{param} 创建缺失的 GUI 变量",

    # 额外：帮助（main_ui_help.py）
    "help_text": """
    Billboard Splitter – 使用指南\n\n
    程序用途：\n
    Billboard Splitter 用于将广告牌设计自动切分为可印刷的面板（panel）。
    程序默认按 1:10 设计比例工作。\n
    在“搭接”“白边”“设置”等区域中填写的数值使用 1:1 实际比例。\n
    程序可按所选排版将切分后的面板放置到 PDF 文档：\n
    • 公共拼版：所有面板置于一个文档。\n
    • 独立文件：每个面板保存为单独的 PDF 文件。\n\n
    另外，程序支持：\n
    • 选择排版——纵向或横向（对应地：纵向在上下绘制分隔线，横向在左右绘制分隔线）。\n
    • 将面板整体旋转 180°。\n
    • 添加定位标记（十字或直线），用于粘贴时的精准定位。\n
    • 添加 QR 码或条码——基于输入数据生成，用于识别单个面板。\n
    • 将设置保存为“配置”，可加载、修改或删除，便于在不同项目间快速切换。\n\n
    基本使用步骤：\n\n
    1. 选择输入文件：\n
    • 在“首页”选择包含广告牌设计的 PDF/JPG/TIFF 文件。\n
    • 若未设置自定义路径，程序会默认设置一个示例文件。\n\n
    2. 切分设置：\n
    • 指定将项目分为多少“行 × 列”。\n
    • 设置搭接尺寸。\n
    • 可选：设置白边宽度（将加入到有效搭接）。\n\n
    3. 选择输出排版：\n
    • 纵向：所有面板在 PDF 上纵向排列。\n
    • 横向：所有面板在 PDF 上横向排列。\n\n
    4. 选择输出类型：\n
    • 公共拼版：所有面板放在一个 PDF 文档。\n
    • 独立文件：每个面板保存为一个独立 PDF 文件。\n
    • 在“首页”可启用并配置定位标记（十字或直线）。\n
    • 可选启用 QR 码或条码（由项目数据生成）。\n
    • 编码参数（缩放、偏移、旋转、位置）在“设置”页精细调整。\n\n
    5. 管理设置：\n
    • 在“设置”页精确修改图形参数（边距、线宽、间距）与编码设置。\n
    • 将当前设置保存为“配置”，以便后续加载或修改。\n
    • 设置配置（保存于 profiles.json）支持在不同项目间快速切换。\n\n
    6. 生成 PDF：\n
    • 一切就绪后，点击“生成 PDF”。\n
    • 输出文件保存至“output”（或自定义目录），日志（按日轮转）保存至“logs”（或自定义目录）。\n\n
    如遇问题：\n
    • 查看“logs”文件夹中的日志。每天会生成带日期的日志文件。\n
    • 确认所有必要的文件夹已正确设置。\n
    • 技术支持：tech@printworks.pl（工作日 8–16）\n
    """
}
