# main_ui_settings.py
import tkinter as tk
from tkinter import ttk, messagebox
from main_utils import _on_mousewheel, _apply_direction
import config
from lang_manager import translate, update_ui_language
import logging
from main_ui_scaling import ScalingSection

logger = logging.getLogger('BillboardSplitter')

class SettingsTabUI:
    def __init__(self, parent_frame: ttk.Frame, app):
        """Inicjalizuje UI zakładki Ustawienia."""
        self.parent = parent_frame
        self.app = app
        self.logger = app.logger
        self.comboboxes = {}
        self.label_frames = {}
        self.graphic_vars = {}
        self.code_gui_vars = {}
        self.margin_labels = {}
        self.translatable_widgets = []
        self._setup_ui()

    def _setup_ui(self):
        """Tworzy zawartość zakładki 'Ustawienia'."""
        self.translatable_widgets = []

        # 1. Główny, przewijany kontener
        settings_scroll_frame = ttk.Frame(self.parent)
        settings_scroll_frame.pack(fill="both", expand=True)
        settings_canvas = tk.Canvas(settings_scroll_frame, highlightthickness=0)
        settings_canvas.pack(side="left", fill="both", expand=True)
        settings_scrollbar = ttk.Scrollbar(settings_scroll_frame, orient="vertical", command=settings_canvas.yview)
        settings_scrollbar.pack(side="right", fill="y")
        settings_canvas.configure(yscrollcommand=settings_scrollbar.set)
        inner_settings_frame = ttk.Frame(settings_canvas, padding="10")
        canvas_window = settings_canvas.create_window((0, 0), window=inner_settings_frame, anchor="nw")
        
        def on_configure(event):
            settings_canvas.configure(scrollregion=settings_canvas.bbox("all"))
            settings_canvas.itemconfig(canvas_window, width=event.width)

        inner_settings_frame.bind("<Configure>", lambda e: settings_canvas.configure(scrollregion=settings_canvas.bbox("all")))
        settings_canvas.bind("<Configure>", on_configure)

        # Konfiguracja siatki dla układu 2-kolumnowego
        inner_settings_frame.columnconfigure(0, weight=1, minsize=350)
        inner_settings_frame.columnconfigure(1, weight=1, minsize=350)

        # --- KONTENER NA DWIE GÓRNE KOLUMNY ---
        top_columns_container = ttk.Frame(inner_settings_frame)
        top_columns_container.grid(row=0, column=0, columnspan=2, sticky="new")
        top_columns_container.columnconfigure(0, weight=1)
        top_columns_container.columnconfigure(1, weight=1)

        # --- LEWA KOLUMNA ---
        left_column_frame = ttk.Frame(top_columns_container)
        left_column_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # Sekcja: Operacje cięcia (Tryb przetwarzania)
        processing_mode_key = "section_processing_mode"
        processing_frame = ttk.LabelFrame(left_column_frame, text=translate(processing_mode_key), padding="10")
        processing_frame.pack(fill="x", padx=5, pady=(5, 10))
        self.translatable_widgets.append((processing_frame, processing_mode_key))
        _apply_direction(processing_frame)
        
        rb1 = ttk.Radiobutton(processing_frame, text=translate("processing_mode_hdd"), variable=self.app.processing_mode, value="hdd")
        rb1.pack(side="left", padx=10)
        self.translatable_widgets.append((rb1, "processing_mode_hdd"))
        _apply_direction(rb1)

        rb2 = ttk.Radiobutton(processing_frame, text=translate("processing_mode_ram"), variable=self.app.processing_mode, value="ram")
        rb2.pack(side="left", padx=10)
        self.translatable_widgets.append((rb2, "processing_mode_ram"))
        _apply_direction(rb2)

        # Sekcja: Ustawienia graficzne
        graphic_settings_key = "graphic_settings"
        graphic_frame = ttk.LabelFrame(left_column_frame, text=" " + translate(graphic_settings_key) + " ", padding="10")
        graphic_frame.pack(fill="x", padx=5, pady=5)
        self.translatable_widgets.append((graphic_frame, graphic_settings_key))
        _apply_direction(graphic_frame)
        graphic_frame.columnconfigure(1, weight=1)

        gf_fields = [
            ("margin_top_label", "margin_top", 2.0),
            ("margin_bottom_label", "margin_bottom", 2.0),
            ("margin_left_label", "margin_left", 2.0),
            ("margin_right_label", "margin_right", 2.0),
            ("reg_mark_width_label", "reg_mark_width", 5.0),
            ("reg_mark_height_label", "reg_mark_height", 5.0),
            ("reg_mark_white_line_width_label", "reg_mark_white_line_width", 0.5),
            ("reg_mark_black_line_width_label", "reg_mark_black_line_width", 0.7),
            ("sep_line_black_width_label", "sep_line_black_width", 0.5),
            ("sep_line_white_width_label", "sep_line_white_width", 0.3),
            ("slice_gap_label", "slice_gap", 2.0),
            ("barcode_font_size_label", "barcode_font_size", 4.0),
        ]
        
        g_row = 0
        for label_key, config_key, default_val in gf_fields:
            label = ttk.Label(graphic_frame, text=translate(label_key))
            label.grid(row=g_row, column=0, sticky="w", padx=5, pady=2)
            self.translatable_widgets.append((label, label_key))
            _apply_direction(label)
            
            if config_key in ["margin_top", "margin_bottom", "margin_left", "margin_right"]:
                self.margin_labels[config_key] = label

            if config_key not in self.app.graphic_vars:
                self.app.graphic_vars[config_key] = tk.StringVar()
            var = self.app.graphic_vars[config_key]
            entry = ttk.Entry(graphic_frame, textvariable=var, width=10)
            entry.grid(row=g_row, column=1, sticky="w", padx=5, pady=2)
            _apply_direction(entry)
            g_row += 1

        # --- PRAWA KOLUMNA ---
        right_column_frame = ttk.Frame(top_columns_container)
        right_column_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        right_column_frame.columnconfigure(0, weight=1)
        right_column_frame.rowconfigure(1, weight=1) # Allow product settings to expand
        right_column_frame.rowconfigure(2, weight=0) # Profile section should not expand

        # Create and place the ScalingSection
        self.scaling_section = ScalingSection(right_column_frame, self.app)
        self.scaling_section.scale_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Sekcja: Wybór trybu produktu (Billboard/Poster)
        mode_frame = ttk.LabelFrame(right_column_frame, text=" " + translate("section_product_mode") + " ", padding="10")
        mode_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((mode_frame, "section_product_mode"))
        _apply_direction(mode_frame)

        def _update_product_mode_ui(*args):
            mode = self.app.product_mode.get()
            if mode == 'poster':
                self.poster_settings_frame.tkraise()
            elif mode == 'pos':
                if hasattr(self, 'pos_settings_frame'): self.pos_settings_frame.tkraise()
            else: # billboard
                self.split_settings_frame.tkraise()

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

        # Container for product-specific settings frames
        product_settings_container = ttk.Frame(right_column_frame)
        product_settings_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        product_settings_container.grid_rowconfigure(1, weight=1)
        product_settings_container.grid_columnconfigure(0, weight=1)

        mode_frame = ttk.LabelFrame(product_settings_container, text=" " + translate("section_product_mode") + " ", padding="10")
        mode_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.translatable_widgets.append((mode_frame, "section_product_mode"))
        _apply_direction(mode_frame)

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

        # Sekcja: Ustawienia podziału (Billboard)
        self.split_settings_frame = ttk.LabelFrame(product_settings_container, text=" " + translate("section_split_settings") + " ", padding="10")
        self.split_settings_frame.grid(row=1, column=0, sticky="nsew")
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

        # Sekcja: Ustawienia posteru (Poster)
        self.poster_settings_frame = ttk.LabelFrame(product_settings_container, text=" " + translate("section_poster_settings") + " ", padding="10")
        self.poster_settings_frame.grid(row=1, column=0, sticky="nsew")
        self.translatable_widgets.append((self.poster_settings_frame, "section_poster_settings"))
        _apply_direction(self.poster_settings_frame)
        self.poster_settings_frame.columnconfigure(1, weight=1)
        self.poster_settings_frame.columnconfigure(3, weight=1)

        p_row = 0

        # Repetitions
        label_reps = ttk.Label(self.poster_settings_frame, text=translate("poster_repetitions"))
        label_reps.grid(row=p_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_reps, "poster_repetitions"))
        spin_reps = ttk.Spinbox(self.poster_settings_frame, from_=1, to=10, textvariable=self.app.poster_repetitions, width=5)
        spin_reps.grid(row=p_row, column=1, sticky="w", padx=5)

        # Input Rotation
        label_rot = ttk.Label(self.poster_settings_frame, text=translate("poster_input_rotation"))
        label_rot.grid(row=p_row, column=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label_rot, "poster_input_rotation"))
        combo_rot = ttk.Combobox(self.poster_settings_frame, textvariable=self.app.poster_input_rotation, values=[0, 90, 180, 270], width=5, state="readonly")
        combo_rot.grid(row=p_row, column=3, sticky="w", padx=5)
        p_row += 1

        # Vertical Cut Marks
        check_cut = ttk.Checkbutton(self.poster_settings_frame, text=translate("poster_vertical_cut_marks"), variable=self.app.poster_vertical_cut_marks)
        check_cut.grid(row=p_row, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_cut, "poster_vertical_cut_marks"))
        p_row += 1

        # Enable Codes (reusing from billboard)
        check_barcode_poster = ttk.Checkbutton(self.poster_settings_frame, text=translate("label_enable_codes"), variable=self.app.enable_barcode)
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
        check_start_line_poster = ttk.Checkbutton(self.poster_settings_frame, text=translate("label_enable_start_line"), variable=self.app.add_line_at_start)
        check_start_line_poster.grid(row=p_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_start_line_poster, "label_enable_start_line"))
        p_row += 1

        check_end_line_poster = ttk.Checkbutton(self.poster_settings_frame, text=translate("label_enable_end_line"), variable=self.app.add_line_at_end)
        check_end_line_poster.grid(row=p_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_end_line_poster, "label_enable_end_line"))
        p_row += 1

        # Sekcja: Ustawienia POS (POS)
        self.pos_settings_frame = ttk.LabelFrame(product_settings_container, text="POS Settings", padding="10")
        self.pos_settings_frame.grid(row=1, column=0, sticky="nsew")
        self.pos_settings_frame.columnconfigure(1, weight=1)

        pos_row = 0

        # Enable Codes Checkbox
        check_enable_codes_pos = ttk.Checkbutton(self.pos_settings_frame, text=translate("label_enable_codes"), variable=self.app.enable_barcode)
        check_enable_codes_pos.grid(row=pos_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((check_enable_codes_pos, "label_enable_codes"))

        # Code Type Combobox
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

        # Sekcja: Zarządzanie profilami
        profile_frame = ttk.LabelFrame(right_column_frame, text=translate("section_profiles"), padding="10")
        profile_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((profile_frame, "section_profiles"))
        _apply_direction(profile_frame)
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

        # --- SEKCJE PEŁNEJ SZEROKOŚCI ---
        row_counter = 1

        # Sekcja: Ustawienia kodów
        code_settings_key = "code_settings"
        code_settings_frame = ttk.LabelFrame(inner_settings_frame, text=" " + translate(code_settings_key) + " ", padding="10")
        code_settings_frame.grid(row=row_counter, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((code_settings_frame, code_settings_key))
        _apply_direction(code_settings_frame)
        row_counter += 1

        code_container = ttk.Frame(code_settings_frame)
        code_container.pack(fill='x', expand=True)
        code_container.columnconfigure(0, weight=1)
        code_container.columnconfigure(1, weight=1)

        # --- Lewa kolumna kodów: Kod Kreskowy ---
        barcode_frame = ttk.LabelFrame(code_container, text=f" {translate('code_barcode')} ", padding="10")
        barcode_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.translatable_widgets.append((barcode_frame, 'code_barcode'))
        _apply_direction(barcode_frame)
        self._build_code_settings_ui(barcode_frame, "code_barcode")

        # --- Prawa kolumna kodów: QR Code ---
        qr_code_frame = ttk.LabelFrame(code_container, text=f" {translate('code_qr')} ", padding="10")
        qr_code_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.translatable_widgets.append((qr_code_frame, 'code_qr'))
        _apply_direction(qr_code_frame)
        self._build_code_settings_ui(qr_code_frame, "code_qr")

        # Sekcja: Rasteryzacja wejścia
        raster_key = "rasterization_title"
        raster_frame = ttk.LabelFrame(inner_settings_frame, text=" " + translate(raster_key) + " ", padding="10")
        raster_frame.grid(row=row_counter, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((raster_frame, raster_key))
        _apply_direction(raster_frame)
        row_counter += 1
        raster_frame.columnconfigure(1, weight=0)
        raster_frame.columnconfigure(2, weight=0)
        raster_frame.columnconfigure(3, weight=1)

        r_row = 0
        # Enable Checkbox
        enable_check = ttk.Checkbutton(raster_frame, text=translate("rasterization_enable"), variable=self.app.rasterization_enabled)
        enable_check.grid(row=r_row, column=0, columnspan=4, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((enable_check, "rasterization_enable"))
        _apply_direction(enable_check)
        r_row += 1

        # DPI Label and Spinbox
        dpi_label = ttk.Label(raster_frame, text=translate("rasterization_dpi"))
        dpi_label.grid(row=r_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((dpi_label, "rasterization_dpi"))
        _apply_direction(dpi_label)
        dpi_spinbox = ttk.Spinbox(raster_frame, from_=72, to=1200, textvariable=self.app.rasterization_dpi, width=10)
        dpi_spinbox.grid(row=r_row, column=1, sticky="w", padx=5, pady=2)
        _apply_direction(dpi_spinbox)

        # Compression Label and Combobox
        comp_label = ttk.Label(raster_frame, text=translate("rasterization_compression"))
        comp_label.grid(row=r_row, column=2, sticky="w", padx=(20, 5), pady=2)
        self.translatable_widgets.append((comp_label, "rasterization_compression"))
        _apply_direction(comp_label)
        comp_values = ["LZW", "None"]
        comp_combo = ttk.Combobox(raster_frame, textvariable=self.app.rasterization_compression, values=comp_values, width=15, state="readonly")
        comp_combo.grid(row=r_row, column=3, sticky="w", padx=5, pady=2)
        _apply_direction(comp_combo)
        self.comboboxes['rasterization_compression'] = comp_combo
        
        # Sekcja: Ustawienia logowania
        logging_settings_key = "logging_settings"
        login_frame = ttk.LabelFrame(inner_settings_frame, text=" " + translate(logging_settings_key) + " ", padding="10")
        login_frame.grid(row=row_counter, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((login_frame, logging_settings_key))
        _apply_direction(login_frame)
        row_counter += 1
        login_frame.columnconfigure(1, weight=1)
        l_row = 0
        
        label = ttk.Label(login_frame, text=translate("logging_mode_label"))
        label.grid(row=l_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label, "logging_mode_label"))
        _apply_direction(label)
        logging_mode_values = [translate("logging_console"), translate("logging_file"), translate("logging_both")]
        logging_mode_combo = ttk.Combobox(login_frame, textvariable=self.app.logging_mode, values=logging_mode_values, width=10, state="readonly")
        logging_mode_combo.grid(row=l_row, column=1, sticky="w", padx=5, pady=2)
        _apply_direction(logging_mode_combo)
        self.comboboxes['logging_mode'] = logging_mode_combo
        l_row += 1

        label = ttk.Label(login_frame, text=translate("log_file_label"))
        label.grid(row=l_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label, "log_file_label"))
        _apply_direction(label)
        log_entry = ttk.Entry(login_frame, textvariable=self.app.log_file_path, width=50)
        log_entry.grid(row=l_row, column=1, columnspan=2, sticky="ew", padx=5, pady=2)
        _apply_direction(log_entry)
        btn = ttk.Button(login_frame, text=translate("browse_folder"), command=self.app.browse_log_folder)
        btn.grid(row=l_row, column=3, padx=5)
        self.translatable_widgets.append((btn, "browse_folder"))
        _apply_direction(btn)
        l_row += 1

        label = ttk.Label(login_frame, text=translate("logging_level_label"))
        label.grid(row=l_row, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label, "logging_level_label"))
        _apply_direction(label)
        logging_level_values = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        logging_level_combo = ttk.Combobox(login_frame, textvariable=self.app.logging_level, values=logging_level_values, width=10, state="readonly")
        logging_level_combo.grid(row=l_row, column=1, sticky="w", padx=5, pady=2)
        _apply_direction(logging_level_combo)
        self.comboboxes['logging_level'] = logging_level_combo
        l_row += 1

        # Sekcja: Język
        language_switch_key = "language_switch"
        language_switch_frame = ttk.LabelFrame(inner_settings_frame, text=" " + translate(language_switch_key) + " ", padding="10")
        language_switch_frame.grid(row=row_counter, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.translatable_widgets.append((language_switch_frame, language_switch_key))
        _apply_direction(language_switch_frame)
        row_counter += 1
        
        label = ttk.Label(language_switch_frame, text=translate("choose_language"))
        label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((label, "choose_language"))
        _apply_direction(label)
        self.language_var = tk.StringVar(value=config.settings.get("language", "pl"))
        language_options = [
            ("pl", "Polski"), ("en", "English"), ("ar", "العربية"), ("zn", "中文"),
            ("da", "Dansk"), ("de", "Deutsch"), ("es", "Español"), ("fr", "Français"),
            ("it", "Italiano"), ("nb", "Norsk Bokmål"), ("nl", "Nederlands"),
            ("pt", "Português"), ("ru", "Русский"), ("sv", "Svenska"), ("tr", "Türkçe"),
            ("uk", "Українська"), ("hu", "Magyar"), ("el", "Ελληνικά"), ("bg", "Български"),
            ("ro", "Română"), ("sr", "Srpski"), ("hr", "Hrvatski"), ("fi", "Suomi"),
            ("sk", "Slovenčina"), ("cs", "Čeština"), ("th", "ไทย"), ("fil", "Filipino"),
            ("km", "ខ្មែរ"), ("id", "Bahasa Indonesia"), ("ms", "Bahasa Melayu"),
            ("vi", "Tiếng Việt"), ("ja", "日本語"), ("ko", "한국어"), ("hi", "हिन्दी"),
            ("ur", "اردو")
        ]
        language_display_values = [option[1] for option in language_options]
        self.language_map = {display: code for code, display in language_options}
        self.reverse_language_map = {code: display for code, display in language_options}

        self.language_combo = ttk.Combobox(language_switch_frame, textvariable=self.language_var, values=language_display_values, state="readonly", width=10)
        _apply_direction(self.language_combo)

        initial_lang_code = self.language_var.get()
        display_value = self.reverse_language_map.get(initial_lang_code, language_display_values[0])
        self.language_combo.set(display_value)

        self.language_combo.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.comboboxes['language'] = self.language_combo
        btn = ttk.Button(language_switch_frame, text=translate("apply_language"), command=self.apply_language)
        btn.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.translatable_widgets.append((btn, "apply_language"))
        _apply_direction(btn)

        # Bind mousewheel to all children for scrolling
        self._bind_mousewheel_recursively(inner_settings_frame, settings_canvas)

    def _bind_mousewheel_recursively(self, widget, canvas):
        """Rekursywnie binduje kółko myszy do widgetu i wszystkich jego dzieci."""
        # Główne bindowanie dla Windows/macOS
        widget.bind("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        # Dodatkowe bindowania dla Linux
        widget.bind("<Button-4>", lambda event: canvas.yview_scroll(-1, "units"))
        widget.bind("<Button-5>", lambda event: canvas.yview_scroll(1, "units"))

        for child in widget.winfo_children():
            # Niektóre widgety (jak pole Entry w Combobox) mogą nie istnieć w momencie bindowania
            try:
                if child.winfo_exists():
                    self._bind_mousewheel_recursively(child, canvas)
            except tk.TclError:
                # Ignoruj błędy dla widgetów, które już nie istnieją
                pass

    def _build_code_settings_ui(self, parent_frame, code_key):
        """Helper do budowania UI dla danego typu kodu (QR/kreskowy)."""
        code_params = {
            "code_qr": [("scale_label", "scale", 10.0)],
            "code_barcode": [("scale_x_label", "scale_x", 50.0), ("scale_y_label", "scale_y", 10.0)]
        }
        common_params = [
            ("offset_x_label", "offset_x", 0.0),
            ("offset_y_label", "offset_y", 0.0),
            ("rotation_label", "rotation", 0.0),
            ("anchor_label", "anchor", "bottom-left")
        ]
        anchor_values = ["bottom-left", "bottom-right", "top-left", "top-right", "center", "center-bottom", "center-top", "center-left", "center-right"]
        output_type_keys_internal = ["common_sheet", "separate_files"]
        layout_keys_internal = ["horizontal", "vertical"]

        if code_key not in self.app.code_gui_vars:
            self.app.code_gui_vars[code_key] = {}

        for output_key_internal in output_type_keys_internal:
            output_label_key = "output_common" if output_key_internal == "common_sheet" else "output_separate"
            output_type_frame = ttk.LabelFrame(parent_frame, text=f" {translate(output_label_key)} ", padding="5")
            output_type_frame.pack(fill="x", padx=5, pady=5)
            self.translatable_widgets.append((output_type_frame, output_label_key))
            _apply_direction(output_type_frame)

            if output_key_internal not in self.app.code_gui_vars[code_key]:
                self.app.code_gui_vars[code_key][output_key_internal] = {}

            for layout_key_internal in layout_keys_internal:
                layout_label_key = "layout_" + layout_key_internal
                layout_frame = ttk.LabelFrame(output_type_frame, text=f" {translate(layout_label_key)} ", padding="5")
                layout_frame.pack(fill="x", padx=5, pady=5)
                self.translatable_widgets.append((layout_frame, layout_label_key))
                _apply_direction(layout_frame)

                if layout_key_internal not in self.app.code_gui_vars[code_key][output_key_internal]:
                    self.app.code_gui_vars[code_key][output_key_internal][layout_key_internal] = {}

                layout_frame.columnconfigure(1, weight=1)
                l_row = 0
                specific_params = code_params.get(code_key, [])
                all_display_params = common_params + specific_params

                for label_text_key, param_key, default_val in all_display_params:
                    if param_key not in self.app.code_gui_vars[code_key][output_key_internal][layout_key_internal]:
                        self.app.code_gui_vars[code_key][output_key_internal][layout_key_internal][param_key] = tk.StringVar()

                    var = self.app.code_gui_vars[code_key][output_key_internal][layout_key_internal][param_key]

                    label = ttk.Label(layout_frame, text=translate(label_text_key))
                    label.grid(row=l_row, column=0, sticky="w", padx=5, pady=2)
                    self.translatable_widgets.append((label, label_text_key))
                    _apply_direction(label)

                    if param_key == "anchor":
                        anchor_combo = ttk.Combobox(layout_frame, textvariable=var, values=anchor_values, width=15, state="readonly")
                        anchor_combo.grid(row=l_row, column=1, sticky="w", padx=5, pady=2)
                        _apply_direction(anchor_combo)
                        self.comboboxes[f"{code_key}_{output_key_internal}_{layout_key_internal}_anchor"] = anchor_combo
                    else:
                        entry = ttk.Entry(layout_frame, textvariable=var, width=10)
                        entry.grid(row=l_row, column=1, sticky="w", padx=5, pady=2)
                        _apply_direction(entry)
                    l_row += 1

    def apply_language(self):
        """Zmienia język aplikacji i aktualizuje interfejs."""
        selected_display_name = self.language_combo.get()
        new_lang_code = self.language_map.get(selected_display_name, "pl")

        config.settings["language"] = new_lang_code
        from lang_manager import set_language, translate
        set_language(new_lang_code)

        update_ui_language(self.app)

        self.language_var.set(selected_display_name)

        # Re-apply direction for all widgets in this tab
        for widget, key in self.translatable_widgets:
            if widget.winfo_exists():
                _apply_direction(widget)
        for combo in self.comboboxes.values():
            if combo.winfo_exists():
                _apply_direction(combo)

        messagebox.showinfo(translate("language"), translate("language_changed"))
        self.logger.info(f"Zmieniono język na: {new_lang_code}")

    def save_and_apply_settings(self):
        """Zapisuje ustawienia i stosuje zmiany języka natychmiast."""
        settings_saved_successfully = self.app.save_settings()

        if settings_saved_successfully:
             current_lang_code_in_config = config.settings.get("language", "pl")
             selected_display_name = self.language_combo.get()
             selected_lang_code = self.language_map.get(selected_display_name, "pl")

             if current_lang_code_in_config != selected_lang_code:
                 self.apply_language()
             else:
                 self.app.update_gui_from_config()
                 self.update_combobox_values()

    def save_settings(self):
        """Zapisuje aktualne ustawienia, natychmiast je stosuje i informuje użytkownika."""
        self.logger.debug(translate("logger_start_save_settings"))
        if self.save_settings_local():
            try:
                import config
                config.save_settings("settings.json")
                self.logger.info(translate("logger_settings_saved").format(file="settings.json"))
                from tkinter import messagebox
                messagebox.showinfo(
                    translate("settings_saved_title"),
                    translate("settings_saved").format(filepath="settings.json")
                )

                self.app.splitter.config = config
                self.app.splitter.update_graphic_settings()
                self.app.update_gui_from_config()
                self.app.home_tab_instance.update_preview()
                self.app.home_tab_instance.update_output_preview()

            except Exception as e:
                self.logger.error(translate("logger_unexpected_save_error").format(error=e), exc_info=True)
                from tkinter import messagebox
                messagebox.showerror(
                    translate("settings_save_error_title"),
                    translate("settings_save_error").format(error=e)
                )
        else:
            self.logger.error(translate("logger_conversion_error").format(error="conversion_failed"))

    def save_settings_local(self) -> bool:
        """Pobiera wartości z GUI i aktualizuje globalny słownik config.settings."""
        self.logger.debug(translate("logger_start_save_settings"))
        try:
            config.settings["file_path"]                = self.app.file_path.get()
            config.settings["split_rows"]               = int(self.app.rows.get())
            config.settings["split_cols"]               = int(self.app.cols.get())
            config.settings["overlap"]                  = float(self.app.overlap.get())
            config.settings["white_stripe"]             = float(self.app.white_stripe.get())
            config.settings["add_white_to_overlap"]     = self.app.add_white_to_overlap.get()
            config.settings["layout"]                   = self.app.layout.get()
            config.settings["output_type"]              = self.app.output_type.get()
            config.settings["registration_mark_type"]   = self.app.reg_mark.get()
            config.settings["barcode_type"]             = self.app.barcode_type.get()
            config.settings["bryt_order"]               = self.app.bryt_order.get()
            config.settings["enable_reg_marks"]         = self.app.enable_reg_marks.get()
            config.settings["enable_barcode"]           = self.app.enable_barcode.get()
            config.settings["enable_separation_lines"]  = self.app.enable_separation_lines.get()
            config.settings["add_line_at_start"]        = self.app.add_line_at_start.get()
            config.settings["add_line_at_end"]          = self.app.add_line_at_end.get()
            config.settings["output_dir"]               = self.app.output_dir.get()
            config.settings["slice_rotation"]           = int(self.app.slice_rotation.get())
            config.settings["create_order_folder"]      = self.app.create_order_folder.get()
            config.settings["barcode_text_position"]    = self.app.barcode_text_position.get()
            config.settings["processing_mode"]          = self.app.processing_mode.get()

            if "rasterization" not in config.settings:
                config.settings["rasterization"] = {}
            config.settings["rasterization"]["enabled"] = self.app.rasterization_enabled.get()
            try:
                config.settings["rasterization"]["dpi"] = int(self.app.rasterization_dpi.get())
            except (ValueError, tk.TclError):
                config.settings["rasterization"]["dpi"] = 300
            config.settings["rasterization"]["compression"] = self.app.rasterization_compression.get()

            if "graphic_settings" not in config.settings:
                config.settings["graphic_settings"] = {}
            for key, var in self.graphic_vars.items():
                try:
                    config.settings["graphic_settings"][key] = float(var.get())
                except ValueError:
                    config.settings["graphic_settings"][key] = 0.0
                    self.logger.warning(translate("logger_invalid_value").format(key=key))

            config.settings["logging_mode"]  = self.app.logging_mode.get()
            config.settings["log_file_path"] = self.app.log_file_path.get()
            config.settings["logging_level"] = self.app.logging_level.get()

            if "code_settings" not in config.settings["graphic_settings"]:
                config.settings["graphic_settings"]["code_settings"] = {}
            code_settings_target = config.settings["graphic_settings"]["code_settings"]

            for code_type, output_types in self.code_gui_vars.items():
                code_settings_target.setdefault(code_type, {})
                for out_key, layouts in output_types.items():
                    code_settings_target[code_type].setdefault(out_key, {})
                    for layout_key, params in layouts.items():
                        code_settings_target[code_type][out_key].setdefault(layout_key, {})
                        for param_key, var in params.items():
                            value = var.get()
                            target = code_settings_target[code_type][out_key][layout_key]
                            if param_key == "anchor":
                                target[param_key] = value
                            else:
                                try:
                                    target[param_key] = float(value)
                                except ValueError:
                                    target[param_key] = 0.0
                                    self.logger.warning(translate("logger_invalid_value").format(key=param_key))

            self.logger.debug(translate("logger_end_save_settings"))
            return True

        except ValueError as e:
            messagebox.showerror(
                translate("conversion_error_title"),
                translate("conversion_error").format(error=e)
            )
            self.logger.error(translate("logger_conversion_error").format(error=e))
            return False

        except Exception as e:
            messagebox.showerror(
                translate("settings_save_error_title"),
                translate("settings_save_error").format(error=e)
            )
            self.logger.error(translate("logger_unexpected_save_error").format(error=e), exc_info=True)
            return False

    def _update_widget_labels(self):
        """Aktualizuje tekst na wszystkich zapisanych widgetach, które tego wymagają."""
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
                logger.warning(f"Nie udało się zaktualizować widgetu dla klucza '{key}': {e}")

    def update_combobox_values(self):
        """Aktualizuje wartości w komboboxach i etykiety ramek po zmianie języka."""
        self._update_widget_labels()

        if 'logging_mode' in self.comboboxes:
            current_key = config.settings.get("logging_mode", "logging_console")
            new_values = [translate("logging_console"), translate("logging_file"), translate("logging_both")]
            self.comboboxes['logging_mode']['values'] = new_values
            self.comboboxes['logging_mode'].set(translate(current_key))
            _apply_direction(self.comboboxes['logging_mode'])

        if 'barcode_text_position' in self.comboboxes:
            current_key = self.app.barcode_text_position.get()
            new_values = [translate("barcode_text_bottom"), translate("barcode_text_side"), translate("barcode_text_none")]
            self.comboboxes['barcode_text_position']['values'] = new_values
            key_map = {
                "bottom": translate("barcode_text_bottom"),
                "side": translate("barcode_text_side"),
                "none": translate("barcode_text_none")
            }
            self.comboboxes['barcode_text_position'].set(key_map.get(current_key, translate("barcode_text_side")))
            _apply_direction(self.comboboxes['barcode_text_position'])
        
        self.logger.debug("Odświeżono wartości comboboxów i etykiety w zakładce Ustawienia.")

    def _create_recent_profile_buttons_simple(self, container):
        """Tworzy przyciski szybkiego dostępu do ostatnio używanych profili."""
        for widget in container.winfo_children():
            widget.destroy()
        
        # Zmieniono limit z 5 na 10
        recent_profiles = self.app.profile_list[:10]
        row = 0
        col = 0
        
        # Konfiguracja kolumn kontenera
        for i in range(5):
            container.columnconfigure(i, weight=1)

        for profile in recent_profiles:
            # Skróć nazwę
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