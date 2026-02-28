# main_license
import tkinter as tk
from tkinter import ttk, messagebox
import config
from lang_manager import translate
import license_manager

class LicenseTabUI:
    def __init__(self, parent_frame: ttk.Frame, app):
        """
        Inicjalizuje UI zakładki Licencja, umożliwiając użytkownikowi odczyt unikalnego HWID
        oraz wprowadzenie i aktywację klucza licencyjnego.
        """
        self.parent = parent_frame
        self.app = app
        self.logger = app.logger
        self._setup_ui()

    def _setup_ui(self):
        # Ramka wyświetlająca HWID
        hwid_frame = ttk.LabelFrame(self.parent, text=translate("hwid_frame_title"), padding="10")
        hwid_frame.pack(fill="x", padx=5, pady=5)

        hwid = license_manager.get_hwid()
        self.hwid_entry = ttk.Entry(hwid_frame, width=40)
        self.hwid_entry.insert(0, hwid)
        self.hwid_entry.config(state="readonly")
        self.hwid_entry.pack(side="left", padx=5, pady=5)

        copy_btn = ttk.Button(hwid_frame, text=translate("copy_hwid"), command=self.copy_hwid)
        copy_btn.pack(side="left", padx=5, pady=5)

        # Ramka aktywacji licencji
        license_frame = ttk.LabelFrame(self.parent, text=translate("license_frame_title"), padding="10")
        license_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(license_frame, text=translate("enter_license_key")).pack(side="left", padx=5, pady=5)
        self.license_entry = ttk.Entry(license_frame, width=30)
        self.license_entry.pack(side="left", padx=5, pady=5)

        activate_btn = ttk.Button(license_frame, text=translate("activate"), command=self.activate_license)
        activate_btn.pack(side="left", padx=5, pady=5)

        self.status_label = ttk.Label(license_frame, text=translate("status_trial"), foreground="red")
        self.status_label.pack(side="left", padx=5, pady=5)
        
        if not self.app.trial_mode:
            self.status_label.config(text=translate("license_active"), foreground="green")

    def copy_hwid(self):
        """Kopiuje HWID do schowka systemowego."""
        self.parent.clipboard_clear()
        self.parent.clipboard_append(self.hwid_entry.get())
        self.logger.info(translate("hwid_copied_to_clipboard"))

    def activate_license(self):
        license_key = self.license_entry.get().strip()
        success, error_message = license_manager.activate_license(license_key, self.logger)
        if success:
            self.app.trial_mode = False
            messagebox.showinfo(translate("license_active"), translate("activation_success"))
            self.status_label.config(text=translate("license_active"), foreground="green")
            # Po aktywacji licencji zapisz ustawienia, aby podczas kolejnych uruchomień licencja była zachowana
            from main_config_manager import save_settings_to_file  # lub odpowiednia funkcja zapisu ustawień
            save_settings_to_file(config.settings)  # Upewnij się, że funkcja zapisuje aktualny stan config.settings do pliku (np. settings.json)
        else:
            messagebox.showerror(translate("error"), error_message)

