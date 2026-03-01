
import tkinter as tk
from tkinter import ttk
from lang_manager import translate
from main_utils import _apply_direction
import logging

logger = logging.getLogger('BillboardSplitter')

class ScalingSection:
    def __init__(self, parent_frame, app):
        self.parent_frame = parent_frame
        self.app = app
        self.logger = app.logger
        self._updating_ui = False

        self.translatable_widgets = []
        self._setup_scaling_vars()
        self._setup_ui()
        self._add_traces()

    def retranslate_ui(self):
        """Updates the text of all translatable widgets in this section."""
        for widget, key in self.translatable_widgets:
            if widget.winfo_exists():
                if isinstance(widget, ttk.LabelFrame):
                    widget.configure(text=" " + translate(key) + " ")
                else:
                    widget.configure(text=translate(key))

    def _setup_scaling_vars(self):
        if not hasattr(self.app, 'scale_non_uniform'):
            self.app.scale_non_uniform = tk.BooleanVar(value=False)
        if not hasattr(self.app, 'scale_den'):
            self.app.scale_den = tk.DoubleVar(value=10.0)
        if not hasattr(self.app, 'scale_den_x'):
            self.app.scale_den_x = tk.DoubleVar(value=10.0)
        if not hasattr(self.app, 'scale_den_y'):
            self.app.scale_den_y = tk.DoubleVar(value=10.0)
        if not hasattr(self.app, 'out_width_cm'):
            self.app.out_width_cm = tk.DoubleVar(value=0.0)
        if not hasattr(self.app, 'out_height_cm'):
            self.app.out_height_cm = tk.DoubleVar(value=0.0)
        if not hasattr(self.app, 'input_file_size_info_scaling'):
            self.app.input_file_size_info_scaling = tk.StringVar(value="")

    def _setup_ui(self):
        self.scale_frame = ttk.LabelFrame(self.parent_frame, text=" " + translate("section_scale_and_dimensions") + " ", padding="10")
        self.translatable_widgets.append((self.scale_frame, "section_scale_and_dimensions"))
        self.scale_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        _apply_direction(self.scale_frame)
        self.scale_frame.columnconfigure(1, weight=1)

        # Row 1: Original size and scale controls
        row1_frame = ttk.Frame(self.scale_frame)
        row1_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
        row1_frame.columnconfigure(0, weight=1)
        row1_frame.columnconfigure(1, weight=1)

        # Left side: Original size
        orig_size_frame = ttk.Frame(row1_frame)
        orig_size_frame.grid(row=0, column=0, sticky="w")
        
        orig_size_label = ttk.Label(orig_size_frame, text=translate("label_original_size"))
        self.translatable_widgets.append((orig_size_label, "label_original_size"))
        orig_size_label.pack(side="left", padx=(0, 5))
        _apply_direction(orig_size_label)
        
        self.orig_size_value_label = ttk.Label(orig_size_frame, textvariable=self.app.input_file_size_info_scaling)
        self.orig_size_value_label.pack(side="left")
        _apply_direction(self.orig_size_value_label)

        # Right side: Scale controls
        scale_controls_frame = ttk.Frame(row1_frame)
        scale_controls_frame.grid(row=0, column=1, sticky="e")

        self.check_non_uniform = ttk.Checkbutton(scale_controls_frame, text=translate("label_scale_non_uniform"), variable=self.app.scale_non_uniform)
        self.translatable_widgets.append((self.check_non_uniform, "label_scale_non_uniform"))
        self.check_non_uniform.pack(side="top", anchor="w")
        _apply_direction(self.check_non_uniform)

        self.uniform_scale_frame = ttk.Frame(scale_controls_frame)
        self.uniform_scale_frame.pack(fill="x", expand=True)
        _apply_direction(self.uniform_scale_frame)
        
        scale_label = ttk.Label(self.uniform_scale_frame, text=translate("label_scale"))
        self.translatable_widgets.append((scale_label, "label_scale"))
        scale_label.pack(side="left", padx=(0, 5))
        _apply_direction(scale_label)
        
        scale_entry = ttk.Entry(self.uniform_scale_frame, textvariable=self.app.scale_den, width=8)
        scale_entry.pack(side="left")
        _apply_direction(scale_entry)

        self.non_uniform_scale_frame = ttk.Frame(scale_controls_frame)
        _apply_direction(self.non_uniform_scale_frame)

        scale_x_label = ttk.Label(self.non_uniform_scale_frame, text=translate("label_scale_x"))
        self.translatable_widgets.append((scale_x_label, "label_scale_x"))
        scale_x_label.pack(side="left", padx=(0, 5))
        _apply_direction(scale_x_label)
        
        scale_x_entry = ttk.Entry(self.non_uniform_scale_frame, textvariable=self.app.scale_den_x, width=8)
        scale_x_entry.pack(side="left", padx=(0, 10))
        _apply_direction(scale_x_entry)

        scale_y_label = ttk.Label(self.non_uniform_scale_frame, text=translate("label_scale_y"))
        self.translatable_widgets.append((scale_y_label, "label_scale_y"))
        scale_y_label.pack(side="left", padx=(0, 5))
        _apply_direction(scale_y_label)
        
        scale_y_entry = ttk.Entry(self.non_uniform_scale_frame, textvariable=self.app.scale_den_y, width=8)
        scale_y_entry.pack(side="left")
        _apply_direction(scale_y_entry)

        # Row 2: Output dimensions
        output_dim_frame = ttk.Frame(self.scale_frame)
        output_dim_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(10, 0))
        
        output_dim_label = ttk.Label(output_dim_frame, text=translate("label_output_dimensions"))
        self.translatable_widgets.append((output_dim_label, "label_output_dimensions"))
        output_dim_label.pack(side="left", padx=(0, 10))
        _apply_direction(output_dim_label)

        width_label = ttk.Label(output_dim_frame, text=translate("label_width_cm"))
        self.translatable_widgets.append((width_label, "label_width_cm"))
        width_label.pack(side="left", padx=(0, 5))
        _apply_direction(width_label)
        
        self.out_width_entry = ttk.Entry(output_dim_frame, textvariable=self.app.out_width_cm, width=12)
        self.out_width_entry.pack(side="left", padx=(0, 10))
        _apply_direction(self.out_width_entry)

        height_label = ttk.Label(output_dim_frame, text=translate("label_height_cm"))
        self.translatable_widgets.append((height_label, "label_height_cm"))
        height_label.pack(side="left", padx=(0, 5))
        _apply_direction(height_label)
        
        self.out_height_entry = ttk.Entry(output_dim_frame, textvariable=self.app.out_height_cm, width=12)
        self.out_height_entry.pack(side="left")
        _apply_direction(self.out_height_entry)

        self._toggle_scale_fields()

    def _add_traces(self):
        self.app.scale_non_uniform.trace_add("write", self._on_toggle_non_uniform)
        self.app.scale_den.trace_add("write", self._on_scale_change)
        self.app.scale_den_x.trace_add("write", self._on_scale_change)
        self.app.scale_den_y.trace_add("write", self._on_scale_change)
        self.app.out_width_cm.trace_add("write", self._on_output_dim_change)
        self.app.out_height_cm.trace_add("write", self._on_output_dim_change)
        self.app.input_file_size_info.trace_add("write", self._on_input_size_change)

    def _on_input_size_change(self, *args):
        self.app.input_file_size_info_scaling.set(self.app.input_file_size_info.get())
        self.recalculate_dimensions()

    def _toggle_scale_fields(self, *args):
        if self.app.scale_non_uniform.get():
            self.uniform_scale_frame.pack_forget()
            self.non_uniform_scale_frame.pack(fill="x", expand=True)
        else:
            self.non_uniform_scale_frame.pack_forget()
            self.uniform_scale_frame.pack(fill="x", expand=True)

    def _on_toggle_non_uniform(self, *args):
        self._toggle_scale_fields()
        self.recalculate_dimensions()

    def _on_scale_change(self, *args):
        if self._updating_ui:
            return
        try:
            # Check if the variable holds a valid float
            self.app.scale_den.get()
            self.app.scale_den_x.get()
            self.app.scale_den_y.get()
        except (tk.TclError, ValueError):
            # This will be triggered if the field is empty or contains non-numeric text
            return
        self.recalculate_dimensions()

    def _on_output_dim_change(self, *args):
        if self._updating_ui:
            return
        try:
            self.app.out_width_cm.get()
            self.app.out_height_cm.get()
        except (tk.TclError, ValueError):
            return
        self.recalculate_scale()

    def get_original_dims_cm(self):
        try:
            # Assumes _input_width_mm and _input_height_mm are available from HomeTabUI
            # This is a weak link, but necessary without major refactoring
            orig_w_mm = self.app.home_tab_instance._input_width_mm
            orig_h_mm = self.app.home_tab_instance._input_height_mm
            if orig_w_mm is not None and orig_h_mm is not None:
                return orig_w_mm / 10.0, orig_h_mm / 10.0
        except Exception as e:
            self.logger.debug(f"Could not get original dimensions: {e}")
        return None, None

    def recalculate_dimensions(self):
        self._updating_ui = True
        try:
            orig_w, orig_h = self.get_original_dims_cm()
            if orig_w is None or orig_h is None:
                self.app.out_width_cm.set(0.0)
                self.app.out_height_cm.set(0.0)
                return

            if self.app.scale_non_uniform.get():
                scale_x = self.app.scale_den_x.get()
                scale_y = self.app.scale_den_y.get()
                if scale_x > 0:
                    new_width = round(orig_w * scale_x, 3)
                    if abs(new_width - self.app.out_width_cm.get()) > 1e-9:
                        self.app.out_width_cm.set(new_width)
                if scale_y > 0:
                    new_height = round(orig_h * scale_y, 3)
                    if abs(new_height - self.app.out_height_cm.get()) > 1e-9:
                        self.app.out_height_cm.set(new_height)
            else:
                scale = self.app.scale_den.get()
                if scale > 0:
                    new_width = round(orig_w * scale, 3)
                    new_height = round(orig_h * scale, 3)
                    if abs(new_width - self.app.out_width_cm.get()) > 1e-9:
                        self.app.out_width_cm.set(new_width)
                    if abs(new_height - self.app.out_height_cm.get()) > 1e-9:
                        self.app.out_height_cm.set(new_height)
        except (tk.TclError, ValueError) as e:
            self.logger.warning(f"Error recalculating dimensions: {e}")
            self.app.out_width_cm.set(0.0)
            self.app.out_height_cm.set(0.0)
        self._updating_ui = False

    def recalculate_scale(self):
        self._updating_ui = True
        try:
            orig_w, orig_h = self.get_original_dims_cm()
            if orig_w is None or orig_h is None or orig_w == 0 or orig_h == 0:
                return

            out_w = self.app.out_width_cm.get()
            out_h = self.app.out_height_cm.get()

            if self.app.scale_non_uniform.get():
                if out_w > 0:
                    self.app.scale_den_x.set(round(out_w / orig_w, 3))
                if out_h > 0:
                    self.app.scale_den_y.set(round(out_h / orig_h, 3))
            else:
                # To decide which dimension drives the change, we need to know which one was edited.
                # This simple implementation will have issues if both are edited simultaneously.
                # A common approach is to track the last edited field.
                # For now, we'll prefer width if it seems to have been the driver.
                
                current_scale = self.app.scale_den.get()
                
                # Check if width change is the likely driver
                if out_w > 0 and abs(orig_w * current_scale - out_w) > 1e-9:
                    new_scale = out_w / orig_w
                    self.app.scale_den.set(round(new_scale, 3))
                    self.app.out_height_cm.set(round(orig_h * new_scale, 3))
                # Check if height change is the likely driver
                elif out_h > 0 and abs(orig_h * current_scale - out_h) > 1e-9:
                    new_scale = out_h / orig_h
                    self.app.scale_den.set(round(new_scale, 3))
                    self.app.out_width_cm.set(round(orig_w * new_scale, 3))

        except (tk.TclError, ValueError, ZeroDivisionError) as e:
            self.logger.warning(f"Error recalculating scale: {e}")
        self._updating_ui = False

    def update_translatable_widgets(self, translatable_widgets_list):
        translatable_widgets_list.append((self.scale_frame, "section_scale_and_dimensions"))
        # Add other widgets from this component that need translation
