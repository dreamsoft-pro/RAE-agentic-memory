# license_generator_billboard-splitter.py
import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from lang_manager import LANG

def load_private_key(path):
    """
    Ładuje prywatny klucz RSA z pliku PEM.
    Jeśli klucz jest zaszyfrowany, należy przekazać hasło (tutaj zakładamy brak hasła).
    """
    with open(path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )
    return private_key

def generate_license(hwid, private_key):
    """
    Podpisuje podany HWID przy użyciu klucza prywatnego i zwraca klucz licencyjny zakodowany w Base64.
    """
    signature = private_key.sign(
        hwid.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    license_key = base64.b64encode(signature).decode('utf-8')
    return license_key

def on_generate():
    # Pobierz HWID wprowadzony przez użytkownika
    hwid = hwid_entry.get().strip()
    if not hwid:
        messagebox.showerror(LANG["error"], LANG["enter_hwid"])
        return
    try:
        private_key = load_private_key("private_key.pem")
    except Exception as e:
        messagebox.showerror(LANG["error"], LANG["private_key_load_error"].format(error=e))
        return
    try:
        lic = generate_license(hwid, private_key)
        result_entry.config(state="normal")
        result_entry.delete(0, tk.END)
        result_entry.insert(0, lic)
        result_entry.config(state="readonly")
    except Exception as e:
        messagebox.showerror(LANG["error"], LANG["license_generation_error"].format(error=e))

# Konfiguracja interfejsu
root = tk.Tk()
root.title(LANG.get("title_license_generator", "Generator licencji"))
root.geometry("600x150")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# Pole na wprowadzenie HWID
ttk.Label(
    main_frame,
    text=LANG.get("hwid_prompt", "Wprowadź HWID:")
).grid(row=0, column=0, padx=5, pady=5, sticky="w")
hwid_entry = ttk.Entry(main_frame, width=50)
hwid_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
# Opcjonalnie automatycznie wstaw HWID, np.:
# hwid_entry.insert(0, str(uuid.getnode()))
# hwid_entry.config(state="readonly")

# Przycisk generowania licencji
generate_button = ttk.Button(main_frame, text=LANG.get("generate_license", "Generuj licencję"), command=on_generate)
generate_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

# Pole wyświetlające wygenerowany klucz licencyjny
ttk.Label(main_frame, text=LANG.get("license_code", "Kod licencji")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
result_entry = ttk.Entry(main_frame, width=50)
result_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
result_entry.config(state="readonly")

root.mainloop()
