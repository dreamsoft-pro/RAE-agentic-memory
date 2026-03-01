import os
import sys
import tkinter as tk
from tkinter import ttk
from main_utils import _on_mousewheel, _apply_direction
from PIL import Image, ImageDraw, ImageTk, ImageFont
from lang_manager import translate
from pdf2image import convert_from_path, pdfinfo_from_path
import pymupdf as fitz
import logging
import threading
import config
from pathlib import Path
from main_ui_scaling import ScalingSection

logger = logging.getLogger('BillboardSplitter')

OUTPUT_PREVIEW_CANVAS_SIZE = 400

def get_poppler_path():
    import os, sys
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    poppler_path = os.path.join(base_dir, "poppler", "bin")
    logger.debug(f"{translate('poppler_path_info')}: {poppler_path}")
    return poppler_path

class HomeTabUI:
    def __init__(self, parent_frame: ttk.Frame, app):
        self.parent = parent_frame
        self.app = app
        self.logger = app.logger
        self.recent_profile_buttons = {}
        self.preview_canvas = None
        self.output_preview_canvas = None
        self.input_preview_canvas = None
        self.preview_image = None
        self.output_preview_image = None
        self.preview_progress = None
        self.output_preview_progress = None
        self.input_preview_progress = None
        self.comboboxes = {}
        self.translatable_widgets = []
        self._last_result_paths = {
            "common_sheet_path": None,
            "separate_files_paths": [],
        }
        self._input_width_mm = None
        self._input_height_mm = None
        self._preview_update_job = None

        self._setup_ui()

        self.parent.after(100, self.update_input_preview)
        self.parent.after(100, lambda: self.update_output_preview(manage_progress=False))

    def start_progress(self, canvas, progress_bar):
        if canvas and progress_bar:
            progress_bar.lift()
            progress_bar.start(15)

    def stop_progress(self, canvas, progress_bar):
        if canvas and progress_bar:
            progress_bar.stop()
            progress_bar.lower()

    def _setup_ui(self):
        self.translatable_widgets = []
        scroll_container = ttk.Frame(self.parent)
        scroll_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_container, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        inner_content_frame = ttk.Frame(canvas, padding="10")
        canvas.create_window((0, 0), window=inner_content_frame, anchor="nw")

        inner_content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        _on_mousewheel(canvas)

        main_container = ttk.Frame(inner_content_frame)
        main_container.pack(fill="both", expand=True)
        main_container.columnconfigure(0, weight=13, minsize=650)
        main_container.columnconfigure(1, weight=7, minsize=350)

        left_frame = ttk.Frame(main_container)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=10)

        row_counter = 0

        file_frame = ttk.LabelFrame(left_frame, text=" " + translate("section_input_file") + " ", padding="10")
        file_frame.grid(row=row_counter, column=0, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((file_frame, "section_input_file"))
        _apply_direction(file_frame)
        row_counter += 1
        file_frame.columnconfigure(0, weight=1)
        entry_file = ttk.Entry(file_frame, textvariable=self.app.file_path, width=60)
        entry_file.grid(row=0, column=0, sticky="ew", padx=(0,5))
        _apply_direction(entry_file)
        btn_browse = ttk.Button(file_frame, text=translate("button_browse"), command=self.app.browse_file)
        btn_browse.grid(row=0, column=1)
        self.translatable_widgets.append((btn_browse, "button_browse"))
        _apply_direction(btn_browse)

        # Create and place the ScalingSection
        self.scaling_section = ScalingSection(left_frame, self.app)
        # The ScalingSection's frame will be placed by its own grid call, so we just need to increment the row counter
        row_counter += 1

        mode_frame = ttk.LabelFrame(left_frame, text=" " + translate("section_product_mode") + " ", padding="10")
        mode_frame.grid(row=row_counter, column=0, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((mode_frame, "section_product_mode"))
        _apply_direction(mode_frame)
        row_counter += 1

        def _update_product_mode_ui(*args):
            mode = self.app.product_mode.get()
            if mode == 'poster':
                self.poster_settings_frame.tkraise()
            elif mode == 'pos':
                if hasattr(self, 'pos_settings_frame'): self.pos_settings_frame.tkraise()
            else: # billboard
                self.split_settings_frame.tkraise()
            self.update_input_preview()

        self.app.product_mode.trace_add("write", _update_product_mode_ui)

        rb_billboard = ttk.Radiobutton(mode_frame, text=translate("product_mode_billboard"), variable=self.app.product_mode, value="billboard")
        rb_billboard.pack(side="left", padx=10)
        self.translatable_widgets.append((rb_billboard, "product_mode_billboard"))
        _apply_direction(rb_billboard)

        rb_poster = ttk.Radiobutton(mode_frame, text=translate("product_mode_poster"), variable=self.app.product_mode, value="poster")
        rb_poster.pack(side="left", padx=10)
        self.translatable_widgets.append((rb_poster, "product_mode_poster"))
        _apply_direction(rb_poster)

        rb_pos = ttk.Radiobutton(mode_frame, text=translate("product_mode_pos"), variable=self.app.product_mode, value="pos")
        rb_pos.pack(side="left", padx=10)
        self.translatable_widgets.append((rb_pos, "product_mode_pos"))
        _apply_direction(rb_pos)

        product_settings_container = ttk.Frame(left_frame)
        product_settings_container.grid(row=row_counter, column=0, sticky="ew")
        product_settings_container.grid_rowconfigure(0, weight=1)
        product_settings_container.grid_columnconfigure(0, weight=1)

        self.split_settings_frame = ttk.LabelFrame(product_settings_container, text=" " + translate("section_split_settings") + " ", padding="10")
        self.split_settings_frame.grid(row=0, column=0, sticky="nsew")
        self.translatable_widgets.append((self.split_settings_frame, "section_split_settings"))
        _apply_direction(self.split_settings_frame)
        self.split_settings_frame.columnconfigure(1, weight=1)
        self.split_settings_frame.columnconfigure(3, weight=1)
        s_row = 0
        
        label_rows = ttk.Label(self.split_settings_frame, text=translate("label_rows"))
        label_rows.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_rows, "label_rows"))
        _apply_direction(label_rows)
        entry_rows = ttk.Entry(self.split_settings_frame, textvariable=self.app.rows, width=5)
        entry_rows.grid(row=s_row, column=1, sticky="w", padx=5)
        _apply_direction(entry_rows)
        
        label_cols = ttk.Label(self.split_settings_frame, text=translate("label_columns"))
        label_cols.grid(row=s_row, column=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_cols, "label_columns"))
        _apply_direction(label_cols)
        entry_cols = ttk.Entry(self.split_settings_frame, textvariable=self.app.cols, width=5)
        entry_cols.grid(row=s_row, column=3, sticky="w", padx=5)
        _apply_direction(entry_cols)
        s_row += 1

        label_overlap = ttk.Label(self.split_settings_frame, text=translate("label_overlap"))
        label_overlap.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_overlap, "label_overlap"))
        _apply_direction(label_overlap)
        entry_overlap = ttk.Entry(self.split_settings_frame, textvariable=self.app.overlap, width=5)
        entry_overlap.grid(row=s_row, column=1, sticky="w", padx=5)
        _apply_direction(entry_overlap)

        label_stripe = ttk.Label(self.split_settings_frame, text=translate("label_white_stripe"))
        label_stripe.grid(row=s_row, column=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_stripe, "label_white_stripe"))
        _apply_direction(label_stripe)
        entry_stripe = ttk.Entry(self.split_settings_frame, textvariable=self.app.white_stripe, width=5)
        entry_stripe.grid(row=s_row, column=3, sticky="w", padx=5)
        _apply_direction(entry_stripe)
        s_row += 1

        check_add_stripe = ttk.Checkbutton(self.split_settings_frame, text=translate("label_add_white_stripe"), variable=self.app.add_white_to_overlap)
        check_add_stripe.grid(row=s_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_add_stripe, "label_add_white_stripe"))
        _apply_direction(check_add_stripe)
        s_row += 1

        label_layout = ttk.Label(self.split_settings_frame, text=translate("label_layout"))
        label_layout.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_layout, "label_layout"))
        _apply_direction(label_layout)
        layout_values = [translate("layout_vertical"), translate("layout_horizontal")]
        layout_combo = ttk.Combobox(self.split_settings_frame, values=layout_values, width=10, state="readonly")
        _apply_direction(layout_combo)
        try:
            layout_index = ["vertical", "horizontal"].index(self.app.layout.get())
        except ValueError:
            layout_index = 0
        layout_combo.current(layout_index)
        layout_combo.grid(row=s_row, column=1, sticky="w", padx=5)
        def on_layout_selected(event=None):
            selected = layout_combo.get()
            self.app.layout.set(self.app.find_key_for_value(selected, ["layout_vertical", "layout_horizontal"]))
        layout_combo.bind("<<ComboboxSelected>>", on_layout_selected)
        self.comboboxes['layout'] = layout_combo

        label_output = ttk.Label(self.split_settings_frame, text=translate("label_output_type"))
        label_output.grid(row=s_row, column=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_output, "label_output_type"))
        _apply_direction(label_output)
        output_values = [translate("output_common_sheet"), translate("output_separate_files"), translate("output_both")]
        output_combo = ttk.Combobox(self.split_settings_frame, values=output_values, width=15, state="readonly")
        _apply_direction(output_combo)
        try:
            output_index = ["output_common_sheet", "output_separate_files", "output_both"].index(self.app.output_type.get())
        except ValueError:
            output_index = 0
        output_combo.current(output_index)
        output_combo.grid(row=s_row, column=3, sticky="w", padx=5)
        def on_output_selected(event=None):
            selected = output_combo.get()
            self.app.output_type.set(self.app.find_key_for_value(selected, ["output_common_sheet", "output_separate_files", "output_both"]))
        output_combo.bind("<<ComboboxSelected>>", on_output_selected)
        self.comboboxes['output_type'] = output_combo
        s_row += 1

        check_reg = ttk.Checkbutton(self.split_settings_frame, text=translate("label_enable_reg_marks"), variable=self.app.enable_reg_marks)
        check_reg.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_reg, "label_enable_reg_marks"))
        _apply_direction(check_reg)
        reg_values = [translate("reg_mark_cross"), translate("reg_mark_line")]
        reg_combo = ttk.Combobox(self.split_settings_frame, values=reg_values, width=10, state="readonly")
        _apply_direction(reg_combo)
        try:
            reg_index = ["reg_mark_cross", "reg_mark_line"].index(self.app.reg_mark.get())
        except ValueError:
            reg_index = 0
        reg_combo.current(reg_index)
        reg_combo.grid(row=s_row, column=1, sticky="w", padx=5)
        def on_reg_selected(event=None):
            selected = reg_combo.get()
            self.app.reg_mark.set(self.app.find_key_for_value(selected, ["reg_mark_cross", "reg_mark_line"]))
        reg_combo.bind("<<ComboboxSelected>>", on_reg_selected)
        self.comboboxes['reg_mark'] = reg_combo
        s_row += 1

        check_barcode = ttk.Checkbutton(self.split_settings_frame, text=translate("label_enable_codes"), variable=self.app.enable_barcode)
        check_barcode.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_barcode, "label_enable_codes"))
        _apply_direction(check_barcode)
        barcode_values = [translate("code_qr"), translate("code_barcode")]
        barcode_combo = ttk.Combobox(self.split_settings_frame, values=barcode_values, width=12, state="readonly")
        _apply_direction(barcode_combo)
        try:
            barcode_index = ["code_qr", "code_barcode"].index(self.app.barcode_type.get())
        except ValueError:
            barcode_index = 0
        barcode_combo.current(barcode_index)
        barcode_combo.grid(row=s_row, column=1, sticky="w", padx=5)
        def on_barcode_selected(event=None):
            selected = barcode_combo.get()
            self.app.barcode_type.set(self.app.find_key_for_value(selected, ["code_qr", "code_barcode"]))
        barcode_combo.bind("<<ComboboxSelected>>", on_barcode_selected)
        self.comboboxes['barcode_type'] = barcode_combo
        s_row += 1

        self.sep_lines_check = ttk.Checkbutton(self.split_settings_frame, text=translate("label_enable_sep_lines"), variable=self.app.enable_separation_lines)
        self.sep_lines_check.grid(row=s_row, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((self.sep_lines_check, "label_enable_sep_lines"))
        _apply_direction(self.sep_lines_check)
        def update_separation_lines_state(*args):
            state = "disabled" if self.app.output_type.get() == "output_separate_files" else "normal"
            self.sep_lines_check.configure(state=state)
            if state == "disabled":
                self.app.enable_separation_lines.set(False)
        self.app.output_type.trace_add("write", update_separation_lines_state)
        update_separation_lines_state()
        s_row += 1

        check_start_line = ttk.Checkbutton(self.split_settings_frame, text=translate("label_enable_start_line"), variable=self.app.add_line_at_start)
        check_start_line.grid(row=s_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_start_line, "label_enable_start_line"))
        _apply_direction(check_start_line)
        s_row += 1

        check_end_line = ttk.Checkbutton(self.split_settings_frame, text=translate("label_enable_end_line"), variable=self.app.add_line_at_end)
        check_end_line.grid(row=s_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_end_line, "label_enable_end_line"))
        _apply_direction(check_end_line)
        s_row += 1

        check_border = ttk.Checkbutton(self.split_settings_frame, text=translate("label_draw_slice_border"), variable=self.app.draw_slice_border)
        check_border.grid(row=s_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_border, "label_draw_slice_border"))
        _apply_direction(check_border)
        s_row += 1

        label_order = ttk.Label(self.split_settings_frame, text=translate("label_bryt_order"))
        label_order.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_order, "label_bryt_order"))
        _apply_direction(label_order)
        order_values = [translate("bryt_order_1"), translate("bryt_order_2"), translate("bryt_order_3"), translate("bryt_order_4"), translate("bryt_order_5"), translate("bryt_order_6")]
        bryt_combo = ttk.Combobox(self.split_settings_frame, values=order_values, width=50, state="readonly")
        _apply_direction(bryt_combo)
        try:
            bryt_index = ["bryt_order_1", "bryt_order_2", "bryt_order_3", "bryt_order_4", "bryt_order_5", "bryt_order_6"].index(self.app.bryt_order.get())
        except ValueError:
            bryt_index = 0
        bryt_combo.current(bryt_index)
        bryt_combo.grid(row=s_row, column=1, columnspan=3, sticky="w", padx=5)
        def on_bryt_selected(event=None):
            selected = bryt_combo.get()
            self.app.bryt_order.set(self.app.find_key_for_value(selected, ["bryt_order_1", "bryt_order_2", "bryt_order_3", "bryt_order_4", "bryt_order_5", "bryt_order_6"]))
        bryt_combo.bind("<<ComboboxSelected>>", on_bryt_selected)
        self.comboboxes['bryt_order'] = bryt_combo
        s_row += 1

        label_rotation = ttk.Label(self.split_settings_frame, text=translate("label_slice_rotation"))
        label_rotation.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_rotation, "label_slice_rotation"))
        _apply_direction(label_rotation)
        rotation_combo = ttk.Combobox(self.split_settings_frame, textvariable=self.app.slice_rotation, values=["0", "180"], width=5, state="readonly")
        rotation_combo.grid(row=s_row, column=1, sticky="w", padx=5)
        _apply_direction(rotation_combo)
        s_row += 1

        label_sep_len = ttk.Label(self.split_settings_frame, text=translate("label_sep_line_length"))
        label_sep_len.grid(row=s_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_sep_len, "label_sep_line_length"))
        _apply_direction(label_sep_len)
        entry_sep_len = ttk.Entry(self.split_settings_frame, textvariable=self.app.sep_line_length, width=8)
        entry_sep_len.grid(row=s_row, column=1, sticky="w", padx=5)
        _apply_direction(entry_sep_len)
        s_row += 1

        self.poster_settings_frame = ttk.LabelFrame(product_settings_container, text=" " + translate("section_poster_settings") + " ", padding="10")
        self.poster_settings_frame.grid(row=0, column=0, sticky="nsew")
        self.translatable_widgets.append((self.poster_settings_frame, "section_poster_settings"))
        _apply_direction(self.poster_settings_frame)
        self.poster_settings_frame.columnconfigure(1, weight=1)
        self.poster_settings_frame.columnconfigure(3, weight=1)

        p_row = 0

        label_reps = ttk.Label(self.poster_settings_frame, text=translate("poster_repetitions"))
        label_reps.grid(row=p_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_reps, "poster_repetitions"))
        spin_reps = ttk.Spinbox(self.poster_settings_frame, from_=1, to=10, textvariable=self.app.poster_repetitions, width=5)
        spin_reps.grid(row=p_row, column=1, sticky="w", padx=5)

        label_rot = ttk.Label(self.poster_settings_frame, text=translate("poster_input_rotation"))
        label_rot.grid(row=p_row, column=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_rot, "poster_input_rotation"))
        combo_rot = ttk.Combobox(self.poster_settings_frame, textvariable=self.app.poster_input_rotation, values=["0", "90", "180", "270"], width=5, state="readonly")
        combo_rot.grid(row=p_row, column=3, sticky="w", padx=5)
        p_row += 1

        check_cut = ttk.Checkbutton(self.poster_settings_frame, text=translate("poster_vertical_cut_marks"), variable=self.app.poster_vertical_cut_marks)
        check_cut.grid(row=p_row, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_cut, "poster_vertical_cut_marks"))
        p_row += 1

        check_barcode_poster = ttk.Checkbutton(self.poster_settings_frame, text=translate("label_enable_codes"), variable=self.app.poster_enable_barcode)
        check_barcode_poster.grid(row=p_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_barcode_poster, "label_enable_codes"))

        barcode_values_poster = [translate("code_qr"), translate("code_barcode")]
        barcode_combo_poster = ttk.Combobox(self.poster_settings_frame, values=barcode_values_poster, width=12, state="readonly")
        try:
            barcode_index_poster = ["code_qr", "code_barcode"].index(self.app.barcode_type.get())
        except ValueError:
            barcode_index_poster = 0
        barcode_combo_poster.current(barcode_index_poster)
        barcode_combo_poster.grid(row=p_row, column=1, sticky="w", padx=5)
        def on_barcode_selected_poster(event=None):
            selected = barcode_combo_poster.get()
            self.app.barcode_type.set(self.app.find_key_for_value(selected, ["code_qr", "code_barcode"]))
        barcode_combo_poster.bind("<<ComboboxSelected>>", on_barcode_selected_poster)
        self.comboboxes['barcode_type_poster'] = barcode_combo_poster
        p_row += 1

        # Start/End Lines (reusing from billboard)
        check_start_line_poster = ttk.Checkbutton(self.poster_settings_frame, text=translate("label_enable_start_line"), variable=self.app.poster_add_line_at_start)
        check_start_line_poster.grid(row=p_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_start_line_poster, "label_enable_start_line"))
        p_row += 1

        check_end_line_poster = ttk.Checkbutton(self.poster_settings_frame, text=translate("label_enable_end_line"), variable=self.app.poster_add_line_at_end)
        check_end_line_poster.grid(row=p_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_end_line_poster, "label_enable_end_line"))
        p_row += 1

        self.pos_settings_frame = ttk.LabelFrame(product_settings_container, text="POS Settings", padding="10")
        self.pos_settings_frame.grid(row=0, column=0, sticky="nsew")
        self.pos_settings_frame.columnconfigure(1, weight=1)

        pos_row = 0

        check_enable_codes_pos = ttk.Checkbutton(self.pos_settings_frame, text=translate("label_enable_codes"), variable=self.app.pos_enable_barcode)
        check_enable_codes_pos.grid(row=pos_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_enable_codes_pos, "label_enable_codes"))

        barcode_values_pos = [translate("code_qr"), translate("code_barcode")]
        barcode_combo_pos = ttk.Combobox(self.pos_settings_frame, values=barcode_values_pos, width=12, state="readonly")
        try:
            barcode_index_pos = ["code_qr", "code_barcode"].index(self.app.barcode_type.get())
        except ValueError:
            barcode_index_pos = 0
        barcode_combo_pos.current(barcode_index_pos)
        barcode_combo_pos.grid(row=pos_row, column=1, sticky="w", padx=5)
        def on_barcode_selected_pos(event=None):
            selected = barcode_combo_pos.get()
            self.app.barcode_type.set(self.app.find_key_for_value(selected, ["code_qr", "code_barcode"]))
        barcode_combo_pos.bind("<<ComboboxSelected>>", on_barcode_selected_pos)
        self.comboboxes['barcode_type_pos'] = barcode_combo_pos

        def _toggle_pos_code_types(*args):
            state = "readonly" if self.app.enable_barcode.get() else "disabled"
            barcode_combo_pos.config(state=state)

        self.app.enable_barcode.trace_add("write", _toggle_pos_code_types)
        
        _toggle_pos_code_types()

        _update_product_mode_ui()

        row_counter += 1

        profile_frame = ttk.LabelFrame(left_frame, text=translate("section_profiles"), padding="10")
        profile_frame.grid(row=row_counter, column=0, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((profile_frame, "section_profiles"))
        _apply_direction(profile_frame)
        row_counter += 1
        profile_frame.columnconfigure(0, weight=1)
        self.app.profile_combo = ttk.Combobox(profile_frame, textvariable=self.app.profile_name_var, values=self.app.profile_list, width=30)
        self.app.profile_combo.grid(row=0, column=0, sticky="ew", padx=(0,5))
        _apply_direction(self.app.profile_combo)
        btn_load = ttk.Button(profile_frame, text=translate("button_load"), command=self.app.load_profile)
        btn_load.grid(row=0, column=1, padx=2)
        self.translatable_widgets.append((btn_load, "button_load"))
        _apply_direction(btn_load)
        btn_save = ttk.Button(profile_frame, text=translate("button_save"), command=self.app.save_profile)
        btn_save.grid(row=0, column=2, padx=2)
        self.translatable_widgets.append((btn_save, "button_save"))
        _apply_direction(btn_save)
        btn_delete = ttk.Button(profile_frame, text=translate("button_delete"), command=self.app.delete_profile)
        btn_delete.grid(row=0, column=3, padx=2)
        self.translatable_widgets.append((btn_delete, "button_delete"))
        _apply_direction(btn_delete)

        self.recent_profiles_container = ttk.Frame(profile_frame)
        self.recent_profiles_container.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10,0))
        for col in range(5):
            self.recent_profiles_container.columnconfigure(col, weight=1)
        self._create_recent_profile_buttons_simple(self.recent_profiles_container)

        loc_frame = ttk.LabelFrame(left_frame, text=translate("section_save_location"), padding="10")
        loc_frame.grid(row=row_counter, column=0, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((loc_frame, "section_save_location"))
        _apply_direction(loc_frame)
        row_counter += 1
        loc_frame.columnconfigure(0, weight=1)
        entry_loc = ttk.Entry(loc_frame, textvariable=self.app.output_dir, width=60)
        entry_loc.grid(row=0, column=0, sticky="ew", padx=(0,5))
        _apply_direction(entry_loc)
        btn_browse_out = ttk.Button(loc_frame, text=translate("button_browse"), command=self.app.browse_output_dir)
        btn_browse_out.grid(row=0, column=1)
        self.translatable_widgets.append((btn_browse_out, "button_browse"))
        _apply_direction(btn_browse_out)

        check_create_folder = ttk.Checkbutton(loc_frame, text=translate("label_create_order_folder"), variable=self.app.create_order_folder)
        check_create_folder.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=(5,0))
        self.translatable_widgets.append((check_create_folder, "label_create_order_folder"))
        _apply_direction(check_create_folder)

        right_frame = ttk.Frame(main_container)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 10), pady=10)
        right_frame.rowconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        preview_in_frame = ttk.LabelFrame(right_frame, text=" " + translate("section_input_preview") + " ", padding="10")
        preview_in_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        self.translatable_widgets.append((preview_in_frame, "section_input_preview"))
        _apply_direction(preview_in_frame)
        preview_in_frame.rowconfigure(0, weight=1)
        preview_in_frame.columnconfigure(0, weight=1)

        self.input_preview_canvas = tk.Canvas(preview_in_frame, bg="lightgrey", highlightthickness=0)
        self.input_preview_canvas.grid(row=0, column=0, sticky="nsew")
        self.input_preview_progress = ttk.Progressbar(preview_in_frame, orient='horizontal', mode='indeterminate')
        self.input_preview_progress.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.preview_canvas = self.input_preview_canvas # Alias for backward compatibility if needed
        self.preview_progress = self.input_preview_progress

        preview_out_frame = ttk.LabelFrame(right_frame, text=" " + translate("section_output_preview") + " ", padding="10")
        preview_out_frame.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        self.translatable_widgets.append((preview_out_frame, "section_output_preview"))
        _apply_direction(preview_out_frame)
        preview_out_frame.rowconfigure(0, weight=1)
        preview_out_frame.columnconfigure(0, weight=1)

        self.output_preview_canvas = tk.Canvas(preview_out_frame, bg="lightgrey", highlightthickness=0)
        self.output_preview_canvas.grid(row=0, column=0, sticky="nsew")
        self.output_preview_progress = ttk.Progressbar(preview_out_frame, orient='horizontal', mode='indeterminate')
        self.output_preview_progress.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        self.update_input_preview(manage_progress=False)
        self.update_output_preview(manage_progress=False)

        # Traces to auto-refresh preview on settings change
        self.app.rows.trace_add("write", self._schedule_preview_update)
        self.app.cols.trace_add("write", self._schedule_preview_update)
        self.app.layout.trace_add("write", self._schedule_preview_update)
        self.app.poster_repetitions.trace_add("write", self._schedule_preview_update)
        self.app.poster_input_rotation.trace_add("write", self._schedule_preview_update)

    def update_input_preview(self, manage_progress=True):
        if self.input_preview_canvas is None:
            return

        if manage_progress:
            self.start_progress(self.input_preview_canvas, self.input_preview_progress)

        self.input_preview_canvas.after(100, self._update_input_preview_task, manage_progress)

    def update_preview(self, manage_progress=True):
        """Alias for update_input_preview to maintain backward compatibility."""
        self.update_input_preview(manage_progress)

    def _schedule_preview_update(self, *args):
        if self._preview_update_job:
            self.parent.after_cancel(self._preview_update_job)
        self._preview_update_job = self.parent.after(400, self.update_input_preview)

    def _update_input_preview_task(self, manage_progress):
        canvas = self.input_preview_canvas
        if not canvas:
            if manage_progress:
                self.stop_progress(canvas, self.input_preview_progress)
            return

        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2:
            # If canvas not ready, reschedule
            canvas.after(100, lambda: self._update_input_preview_task(manage_progress))
            return

        path = self.app.file_path.get().strip()
        if not path or not os.path.exists(path):
            if manage_progress:
                self.stop_progress(canvas, self.input_preview_progress)
            self._show_message_on_canvas(canvas, translate("msg_no_input_file"))
            self.app.input_file_size_info.set("")
            return

        def task():
            try:
                base_img = self._render_input_image(path, 1000, 1000)
                if base_img is None:
                    raise ValueError("Failed to render input image.")

                product_mode = self.app.product_mode.get().lower()
                final_img = None

                if product_mode == 'billboard':
                    # Grid drawing moved to after thumbnailing
                    final_img = base_img
                
                elif product_mode in ('pos', 'poster'):
                    final_img = self._simulate_page_with_barcode(base_img, product_mode)
                
                else: # Other modes
                    final_img = base_img

                if final_img:
                    final_img.thumbnail((canvas_w, canvas_h), Image.Resampling.LANCZOS)
                    
                    if product_mode == 'billboard':
                        self._draw_billboard_grid_on_image(final_img)

                    self.preview_image = ImageTk.PhotoImage(final_img)
                    canvas.after(0, self._display_final_image, canvas, self.preview_image)

            except Exception as e:
                self.logger.error(f"Error updating input preview: {e}", exc_info=True)
                canvas.after(0, self._show_message_on_canvas, canvas, translate("msg_thumbnail_error"))
                self.app.input_file_size_info.set(translate("preview_error"))
            finally:
                if manage_progress:
                    canvas.after(0, self.stop_progress, canvas, self.input_preview_progress)

        threading.Thread(target=task, daemon=True).start()

    def _simulate_page_with_barcode(self, base_img, product_mode):
        gs = config.settings.get("graphic_settings", {})
        margin_top_mm = float(gs.get("margin_top", 2.0))
        margin_bottom_mm = float(gs.get("margin_bottom", 2.0))
        margin_left_mm = float(gs.get("margin_left", 2.0))
        margin_right_mm = float(gs.get("margin_right", 2.0))

        width_mm = self._input_width_mm
        px_per_mm = (base_img.width / width_mm) if (width_mm and width_mm > 0) else (72 / 25.4)

        margin_left_px = int(margin_left_mm * px_per_mm)
        margin_right_px = int(margin_right_mm * px_per_mm)
        margin_top_px = int(margin_top_mm * px_per_mm)
        margin_bottom_px = int(margin_bottom_mm * px_per_mm)

        repetitions = 1
        gap_px = 0

        if product_mode == 'poster':
            try:
                repetitions = int(self.app.poster_repetitions.get())
            except (ValueError, tk.TclError):
                repetitions = 1
            gap_mm = float(gs.get("slice_gap", 2.0))
            gap_px = int(gap_mm * px_per_mm)

        content_w = (base_img.width * repetitions) + (gap_px * (repetitions - 1))
        page_w = content_w + margin_left_px + margin_right_px
        page_h = base_img.height + margin_top_px + margin_bottom_px

        page_img = Image.new("RGB", (page_w, page_h), "#E0E0E0")

        for i in range(repetitions):
            x_offset = margin_left_px + (base_img.width + gap_px) * i
            page_img.paste(base_img, (x_offset, margin_top_px))

        if self.app.enable_barcode.get():
            code_type = self.app.barcode_type.get()
            output_type = self.app.output_type.get() if product_mode == 'billboard' else 'common_sheet'
            layout = self.app.layout.get().replace('layout_', '') if product_mode == 'billboard' else 'horizontal'
            
            code_config_path = gs.get("code_settings", {}).get(code_type, {}).get(output_type, {}).get(layout, {})
            if not code_config_path:
                 code_config_path = gs.get("code_settings", {}).get(code_type, {}).get('common_sheet', {}).get('horizontal', {})

            offset_x_mm = float(code_config_path.get("offset_x", 2.0))
            offset_y_mm = float(code_config_path.get("offset_y", 0.0))
            anchor = code_config_path.get("anchor", "bottom-left")

            placeholder_w_mm = 20
            placeholder_h_mm = 5
            if code_type == 'code_qr':
                placeholder_h_mm = 20

            placeholder_w_px = int(placeholder_w_mm * px_per_mm)
            placeholder_h_px = int(placeholder_h_mm * px_per_mm)

            if 'top' in anchor:
                y0 = int(offset_y_mm * px_per_mm)
            else: # bottom
                y0 = page_h - int(offset_y_mm * px_per_mm) - placeholder_h_px

            if 'left' in anchor:
                x0 = int(offset_x_mm * px_per_mm)
            else: # right
                x0 = page_w - int(offset_x_mm * px_per_mm) - placeholder_w_px

            draw = ImageDraw.Draw(page_img)
            draw.rectangle([x0, y0, x0 + placeholder_w_px, y0 + placeholder_h_px], fill="black")

        return page_img


    def _render_input_image(self, path, canvas_w, canvas_h):
        size_info = ""
        width_mm, height_mm = None, None
        
        try:
            # FIX FOR LINUX POPPLER
            poppler_dir = None if sys.platform != "win32" else get_poppler_path()
            
            if path.lower().endswith(".pdf"):
                doc = fitz.open(path)
                page = doc[0]
                
                # Get physical dimensions
                r = page.rect
                width_mm = (r.width / 72.0) * 25.4
                height_mm = (r.height / 72.0) * 25.4
                size_info = f"{(width_mm / 10):.2f}×{(height_mm / 10):.2f} cm"

                # Handle rotation for Poster mode
                rotation = 0
                if self.app.product_mode.get() == 'poster':
                    try:
                        rotation = int(self.app.poster_input_rotation.get())
                    except (ValueError, tk.TclError):
                        rotation = 0

                # Scale to fit canvas
                img_w, img_h = r.width, r.height
                if rotation in [90, 270]:
                    img_w, img_h = img_h, img_w
                
                scale = min((canvas_w - 10) / img_w, (canvas_h - 10) / img_h)
                mat = fitz.Matrix(scale, scale).prerotate(rotation)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                doc.close()
            else:
                # For other image formats
                img = Image.open(path)
                img = img.convert("RGB")
                
                # Get physical dimensions
                dpi = img.info.get("dpi", (72, 72))
                width_mm = (img.width / dpi[0]) * 25.4
                height_mm = (img.height / dpi[1]) * 25.4
                size_info = f"{(width_mm / 10):.2f}×{(height_mm / 10):.2f} cm"

                # Scale to fit canvas
                img.thumbnail((canvas_w - 10, canvas_h - 10), Image.Resampling.LANCZOS)

            self.app.input_file_size_info.set(size_info)
            self._input_width_mm = width_mm
            self._input_height_mm = height_mm
            return img

        except Exception as e:
            self.logger.warning(f"Could not read or render {path}: {e}")
            self.app.input_file_size_info.set(translate("size_read_error"))
            return None

    def _compute_bryt_labels(self, rows: int, cols: int) -> list[list[str]]:
        labels = []
        for r in range(rows):
            row_char = chr(ord('A') + r)
            row_labels = [f"{row_char}{c + 1}" for c in range(cols)]
            labels.append(row_labels)
        return labels

    def _draw_billboard_grid_on_image(self, img):
        try:
            rows = int(self.app.rows.get())
            cols = int(self.app.cols.get())
        except (ValueError, tk.TclError):
            return 

        if rows > 1 or cols > 1:
            draw = ImageDraw.Draw(img)
            img_w, img_h = img.size
            
            # Draw dashed vertical lines
            for i in range(1, cols):
                x = (img_w / cols) * i
                for y in range(0, img_h, 10):
                    draw.line([(x, y), (x, y + 5)], fill="red", width=1)
            
            # Draw dashed horizontal lines
            for i in range(1, rows):
                y = (img_h / rows) * i
                for x in range(0, img_w, 10):
                    draw.line([(x, y), (x + 5, y)], fill="red", width=1)

            # Draw bryt labels
            labels = self._compute_bryt_labels(rows, cols)
            try:
                # Optimized for thumbnail (approx 400px width)
                font = ImageFont.truetype("arial.ttf", 12)
            except IOError:
                font = ImageFont.load_default()

            cell_w = img_w / cols
            cell_h = img_h / rows

            for r in range(rows):
                for c in range(cols):
                    label = labels[r][c]
                    text_w, text_h = draw.textbbox((0, 0), label, font=font)[2:]
                    x = c * cell_w + (cell_w - text_w) / 2
                    y = r * cell_h + (cell_h - text_h) / 2
                    
                    # Draw outline (thinner for thumbnail)
                    offset = 1 
                    for dx in range(-offset, offset + 1, offset):
                        for dy in range(-offset, offset + 1, offset):
                            if dx == 0 and dy == 0:
                                continue
                            draw.text((x + dx, y + dy), label, font=font, fill="white")
                    
                    # Draw text
                    draw.text((x, y), label, font=font, fill="black")

    def _display_final_image(self, canvas, tk_image):
        canvas.delete("all")
        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()
        canvas.create_image(canvas_w / 2, canvas_h / 2, image=tk_image)

    def _show_message_on_canvas(self, canvas, message):
        canvas.delete("all")
        canvas_w = canvas.winfo_width()
        canvas_h = canvas.winfo_height()
        if canvas_w > 1 and canvas_h > 1:
            canvas.create_text(
                canvas_w / 2, canvas_h / 2,
                text=message, fill="gray", font=("Helvetica", 14), justify="center"
            )

    def _update_widget_labels(self):
        self.scaling_section.retranslate_ui()
        for widget, key in self.translatable_widgets:
            try:
                if widget.winfo_exists():
                    if isinstance(widget, ttk.LabelFrame):
                        widget.configure(text=" " + translate(key) + " ")
                    else:
                        widget.configure(text=translate(key))
                    _apply_direction(widget)
            except Exception as e:
                logger.warning(f"Failed to update widget for key '{key}': {e}")

    def update_combobox_values(self):
        self._update_widget_labels()

        if 'layout' in self.comboboxes:
            self.comboboxes['layout']['values'] = [translate("layout_vertical"), translate("layout_horizontal")]
            try:
                idx = ["vertical", "horizontal"].index(self.app.layout.get())
            except ValueError:
                idx = 0
            self.comboboxes['layout'].current(idx)
            _apply_direction(self.comboboxes['layout'])
        if 'output_type' in self.comboboxes:
            self.comboboxes['output_type']['values'] = [translate("output_common_sheet"), translate("output_separate_files"), translate("output_both")]
            try:
                idx = ["output_common_sheet", "output_separate_files", "output_both"].index(self.app.output_type.get())
            except ValueError:
                idx = 0
            self.comboboxes['output_type'].current(idx)
            _apply_direction(self.comboboxes['output_type'])
        if 'reg_mark' in self.comboboxes:
            self.comboboxes['reg_mark']['values'] = [translate("reg_mark_cross"), translate("reg_mark_line")]
            try:
                idx = ["reg_mark_cross", "reg_mark_line"].index(self.app.reg_mark.get())
            except ValueError:
                idx = 0
            self.comboboxes['reg_mark'].current(idx)
            _apply_direction(self.comboboxes['reg_mark'])
        if 'barcode_type' in self.comboboxes:
            self.comboboxes['barcode_type']['values'] = [translate("code_qr"), translate("code_barcode")]
            try:
                idx = ["code_qr", "code_barcode"].index(self.app.barcode_type.get())
            except ValueError:
                idx = 0
            self.comboboxes['barcode_type'].current(idx)
            _apply_direction(self.comboboxes['barcode_type'])
        if 'bryt_order' in self.comboboxes:
            self.comboboxes['bryt_order']['values'] = [
                translate("bryt_order_1"),
                translate("bryt_order_2"),
                translate("bryt_order_3"),
                translate("bryt_order_4"),
                translate("bryt_order_5"),
                translate("bryt_order_6")
            ]
            try:
                idx = ["bryt_order_1", "bryt_order_2", "bryt_order_3", "bryt_order_4", "bryt_order_5", "bryt_order_6"].index(self.app.bryt_order.get())
            except ValueError:
                idx = 0
            self.comboboxes['bryt_order'].current(idx)
            _apply_direction(self.comboboxes['bryt_order'])

    def _create_recent_profile_buttons_simple(self, container):
        for widget in container.winfo_children():
            widget.destroy()
        
        # Zmieniono limit z 5 na 10
        recent_profiles = self.app.profile_list[:10]
        row = 0
        col = 0
        
        # Konfiguracja kolumn kontenera (aby się ładnie skalowały)
        for i in range(5):
            container.columnconfigure(i, weight=1)

        for profile in recent_profiles:
            # Skróć nazwę jeśli za długa
            display_name = profile
            if len(profile) > 15:
                display_name = profile[:12] + "..."
                
            btn = ttk.Button(container, text=display_name, command=lambda name=profile: self._load_profile_by_name(name))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            _apply_direction(btn)
            
            col += 1
            if col >= 5:
                col = 0
                row += 1

    def _load_profile_by_name(self, profile_name):
        self.app.profile_name_var.set(profile_name)
        self.app.load_profile()

    def _select_output_preview_file(self, result_paths: dict | None) -> str | None:
        if not result_paths:
            return None

        product_mode = (result_paths.get("product_mode") or (self.app.product_mode.get() or "")).strip().lower()

        if product_mode == "poster":
            poster_path = result_paths.get("poster_path")
            if poster_path and os.path.isfile(poster_path):
                self.logger.debug(f"Output preview: using poster_path: {poster_path}")
                return poster_path
            return None

        if product_mode == "pos":
            pos_path = result_paths.get("pos_path")
            if pos_path and os.path.isfile(pos_path):
                self.logger.debug(f"Output preview: using pos_path: {pos_path}")
                return pos_path
            return None

        if product_mode == "billboard":
            mode = result_paths.get("mode")
            common_path = result_paths.get("common_sheet_path") or result_paths.get("common_sheet")
            if mode in ("output_common_sheet", "output_both") and common_path and os.path.isfile(common_path):
                self.logger.debug(f"Output preview: using common_sheet_path (billboard): {common_path}")
                return common_path
            if mode == "output_separate_files":
                separate_files = result_paths.get("separate_files", [])
                if separate_files:
                    first_file = separate_files[0]
                    if os.path.isfile(first_file):
                        self.logger.debug(f"Output preview: using separate_files[0] (billboard): {first_file}")
                        return first_file
        
        # Fallback for any case
        preferred = result_paths.get("preview_preferred")
        if preferred and os.path.isfile(preferred):
            self.logger.debug(f"Output preview: using preferred path: {preferred}")
            return preferred

        self.logger.warning("Could not select a suitable output file for preview.")
        return None

    def _show_output_preview_message(self, message: str) -> None:
        c = self.output_preview_canvas
        if not c:
            return
        try:
            c.delete("all")
            w = max(2, int(c.winfo_width() or 0))
            h = max(2, int(c.winfo_height() or 0))
            c.create_text(w // 2, h // 2, text=message, fill="gray",
                        font=("Helvetica", 12), anchor="center", justify="center")
        except Exception:
            pass

    def update_output_preview(self, result_paths: dict | None = None, manage_progress: bool = True):
        if isinstance(result_paths, dict):
            self._last_result_paths = result_paths

        if self.output_preview_canvas is None:
            return

        if manage_progress:
            self.start_progress(self.output_preview_canvas, self.output_preview_progress)

        self.output_preview_canvas.after(60, lambda: self._update_output_preview_task(manage_progress))

    def _open_pdf_first_page_png(self, path: str, max_w: int, max_h: int):
        try:
            if path.lower().endswith(".pdf"):
                with fitz.open(path) as doc:
                    if not doc.page_count:
                        return None
                    page = doc.load_page(0)
                    pw, ph = float(page.rect.width), float(page.rect.height)
                    if pw <= 0 or ph <= 0:
                        return None
                    scale = min(max_w / pw, max_h / ph)
                    if not (scale > 0):
                        return None
                    m = fitz.Matrix(scale, scale)
                    pix = page.get_pixmap(matrix=m, alpha=False)
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            else:
                with Image.open(path) as _im:
                    img = _im.copy()

            if img.width == 0 or img.height == 0:
                return None
            if img.width > max_w or img.height > max_h:
                img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            return img

        except Exception as e:
            self.logger.error(f"Error rendering PDF to bitmap (fitz): {e}", exc_info=True)
            return None

    def _update_output_preview_task(self, manage_progress: bool):
        try:
            c = self.output_preview_canvas
            if c is None:
                return

            cw = max(2, int(c.winfo_width() or 0))
            ch = max(2, int(c.winfo_height() or 0))
            if cw < 3 or ch < 3:
                c.after(100, lambda: self._update_output_preview_task(manage_progress))
                return

            # 1. Try to display a real generated output file
            result_paths = getattr(self, "_last_result_paths", None)
            selected_file = self._select_output_preview_file(result_paths)
            
            if selected_file and os.path.isfile(selected_file):
                img = self._open_pdf_first_page_png(selected_file, cw, ch)
                if img:
                    self.output_preview_image = ImageTk.PhotoImage(img)
                    self._display_final_image(c, self.output_preview_image)
                else:
                    self._show_output_preview_message(translate("preview_error"))
                return

            # 2. If no output file, enter SIMULATION mode
            path_in = self.app.file_path.get().strip()
            if not path_in or not os.path.exists(path_in):
                self._show_output_preview_message(translate("msg_preview_no_file"))
                return

            base_img = self._render_input_image(path_in, 1000, 1000)
            if base_img is None:
                self._show_output_preview_message(translate("preview_error"))
                return

            product_mode = self.app.product_mode.get().lower()
            final_img = None

            if product_mode in ('billboard', 'pos'):
                final_img = self._simulate_page_with_barcode(base_img, product_mode)
            else: # Poster or other modes
                # Poster simulation is more complex, fallback to base image for now
                final_img = base_img

            if final_img:
                final_img.thumbnail((cw, ch), Image.Resampling.LANCZOS)
                self.output_preview_image = ImageTk.PhotoImage(final_img)
                self._display_final_image(c, self.output_preview_image)
            else:
                self._show_output_preview_message(translate("msg_preview_no_file"))

        except Exception as e:
            self.logger.error(f"Error in output preview task: {e}", exc_info=True)
            self._show_output_preview_message(translate("preview_error"))
        finally:
            if manage_progress and self.output_preview_canvas is not None:
                self.stop_progress(self.output_preview_canvas, self.output_preview_progress)
