# main_ui_help.py
import tkinter as tk
from tkinter import ttk
from lang_manager import translate

class HelpTabUI:
    def __init__(self, parent_frame: ttk.Frame, app):
        """Inicjalizuje UI zakładki Pomoc."""
        self.parent = parent_frame
        self.app = app
        self.logger = app.logger
        self._setup_ui()

    def _setup_ui(self):
        help_text = translate("help_text")
        help_label = tk.Text(self.parent, wrap="word")
        help_label.insert("1.0", help_text)
        help_label.config(state="disabled")
        help_label.pack(fill="both", expand=True)
