# main_utils.py
import os
import sys
import tkinter as tk
from lang_manager import translate
import logging

def get_base_dir():
    """Określa bazowy katalog aplikacji."""
    if getattr(sys, 'frozen', False):
        # Uruchomiono jako .exe (zamrożone przez PyInstaller)
        return sys._MEIPASS  # Używamy sys._MEIPASS, gdzie PyInstaller rozpakowuje zasoby
    else:
        # Uruchomiono jako skrypt .py
        return os.path.dirname(os.path.abspath(__file__))

def _on_mousewheel(widget: tk.Canvas):
    """
    Ustawia obsługę kółka myszy dla przewijania wskazanego widgetu Canvas.
    Dla Windows/macOS oraz Linux – rejestruje bindingi dla odpowiednich zdarzeń.
    """
    def _mousewheel(event):
        # Dla Windows i macOS (event.delta)
        if event.delta:
            widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Dla Linux (zdarzenia Button-4/5)
        elif event.num == 4:  # Scroll up
            widget.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll down
            widget.yview_scroll(1, "units")

    # Bind dla różnych platform
    widget.bind("<MouseWheel>", _mousewheel)
    widget.bind("<Button-4>", _mousewheel)
    widget.bind("<Button-5>", _mousewheel)

def _apply_direction(widget, *, for_multiline=False):
    try:
        from lang_manager import text_align, text_justify, is_rtl
        align = text_align()
        justify = text_justify()
        # ttk.Label/ttk.Button: anchor steruje położeniem w komórce; justify – wyrównanie tekstu wieloliniowego
        if hasattr(widget, "configure"):
            # anchor dla etykiet/ramek/przycisków
            if "anchor" in widget.configure():
                widget.configure(anchor="e" if is_rtl() else "w")
            # justify dla tekstu wieloliniowego
            if for_multiline and "justify" in widget.configure():
                widget.configure(justify=justify)
        # Entry/Text – ustaw kierunek logiczny poprzez justify/right-left
        if widget.winfo_class() in ("TEntry", "Entry"):
            if "justify" in widget.configure():
                widget.configure(justify="right" if is_rtl() else "left")
        # Combobox: wyrównanie tekstu
        if widget.winfo_class() in ("TCombobox",):
            if "justify" in widget.configure():
                widget.configure(justify="right" if is_rtl() else "left")
    except Exception as e:
        logger = logging.getLogger('BillboardSplitter')
        logger.debug(f"_apply_direction failed: {e}")
