# config.py
import sys
import os
import json
import shutil
import logging

default_settings = {
    "language": "pl",
    "create_order_folder": False,
    "processing_mode": "hdd",
    "barcode_text_position": "side",
    "graphic_settings": {
        "code_settings": {
            "code_qr": {
                "common_sheet": {
                    "horizontal": {"offset_x": 2.0, "offset_y": 0.0, "scale": 3.0, "rotation": 0.0, "anchor": "bottom-left"},
                    "vertical": {"offset_x": 2.0, "offset_y": 0.0, "scale": 3.0, "rotation": 0.0, "anchor": "bottom-left"}
                },
                "separate_files": {
                    "horizontal": {"offset_x": 2.0, "offset_y": 0.0, "scale": 3.0, "rotation": 0.0, "anchor": "bottom-left"},
                    "vertical": {"offset_x": 2.0, "offset_y": 0.0, "scale": 3.0, "rotation": 0.0, "anchor": "bottom-left"}
                }
            },
            "code_barcode": {
                "common_sheet": {
                    "horizontal": {"offset_x": 2.0, "offset_y": 0.0, "scale_x": 8.0, "scale_y": 2.0, "rotation": 0.0, "anchor": "bottom-left"},
                    "vertical": {"offset_x": 2.0, "offset_y": 0.0, "scale_x": 8.0, "scale_y": 2.0, "rotation": 0.0, "anchor": "bottom-left"}
                },
                "separate_files": {
                    "horizontal": {"offset_x": 2.0, "offset_y": 0.0, "scale_x": 8.0, "scale_y": 2.0, "rotation": 0.0, "anchor": "bottom-left"},
                    "vertical": {"offset_x": 2.0, "offset_y": 0.0, "scale_x": 8.0, "scale_y": 2.0, "rotation": 0.0, "anchor": "bottom-left"}
                }
            }
        },
        "margin_top": 5.669, "margin_bottom": 5.669, "margin_left": 5.669, "margin_right": 5.669,
        "reg_mark_width": 5.0, "reg_mark_height": 5.0, "reg_mark_white_line_width": 0.5,
        "reg_mark_black_line_width": 0.7, "sep_line_black_width": 0.3, "sep_line_white_width": 0.3,
        "slice_gap": 2.0
    },
    "rasterization": {"enabled": False, "dpi": 300, "compression": "LZW"},
    "product_mode": "billboard",
    "billboard_settings": {
        "rows": 2,
        "cols": 5,
        "overlap": 20.0,
        "white_stripe": 10.0,
        "add_white_to_overlap": True,
        "layout": "layout_vertical",
        "output_type": "output_common_sheet",
        "enable_reg_marks": True,
        "registration_mark_type": "reg_mark_cross",
        "enable_barcode": True,
        "barcode_type": "code_qr",
        "enable_separation_lines": True,
        "add_line_at_start": False,
        "add_line_at_end": False,
        "draw_slice_border": False,
        "bryt_order": "bryt_order_1",
        "slice_rotation": 0
    },
    "poster_settings": {
        "repetitions": 1, "margin_external": 2.0, "separation_lines": False,
        "input_rotation": 0, "vertical_cut_marks": False, "poster_gap": 2.0
    },
    "pos_settings": {
        "codes_enabled": False, "code_type": "barcode"
    },
    "manufacturer_spec": {
        "enabled": False, "name": "default",
        "specs": {
            "default": {
                "margin_top": 5.0, "margin_bottom": 5.0, "margin_left": 5.0,
                "margin_right": 5.0, "slice_gap": 0.0, "overlap": 0.0
            }
        }
    }
}

# Inicjalizujemy settings na poziomie modułu, aby był dostępny przy imporcie
settings = default_settings.copy()

def get(key, default=None):
    """
    Umożliwia wywołania w stylu config.get('logger', None) 
    tak jak przy pracy z dict. Zwraza wartość z settings lub default.
    """
    return settings.get(key, default)

def validate_rasterization_settings(settings_dict):
    """Validates rasterization settings, especially DPI, and falls back to defaults if invalid."""
    raster_settings = settings_dict.get("rasterization")
    if not isinstance(raster_settings, dict):
        settings_dict["rasterization"] = default_settings["rasterization"].copy()
        logging.warning("Rasterization settings missing or corrupt. Restoring defaults.")
        return

    # Validate DPI
    dpi = raster_settings.get("dpi", 300)
    if not isinstance(dpi, int) or not (72 <= dpi <= 1200):
        raster_settings["dpi"] = 300
        logging.warning(f"Invalid DPI value '{dpi}'. Falling back to 300 DPI.")

    # Validate enabled flag
    if not isinstance(raster_settings.get("enabled"), bool):
        raster_settings["enabled"] = False

    # Validate compression
    allowed_compressions = ["LZW", "None"]
    if raster_settings.get("compression") not in allowed_compressions:
        raster_settings["compression"] = "LZW"


def load_settings(filepath="settings.json"):
    global settings

    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        bundled_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bundled_dir = base_dir

    full_path = os.path.join(base_dir, filepath)

    if not os.path.exists(full_path):
        source_path = os.path.join(bundled_dir, filepath)
        if os.path.exists(source_path):
            shutil.copyfile(source_path, full_path)
        else:
            settings = default_settings.copy()
            save_settings(filepath)
            return settings

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            loaded_settings = json.load(f)
            settings = default_settings.copy()
            settings.update(loaded_settings)
    except Exception:
        settings = default_settings.copy()
        save_settings(filepath)

    if getattr(sys, 'frozen', False):
        settings["default_input_dir"] = os.path.join(base_dir, "input")
        if not settings.get("file_path"):
            sample_input = os.path.join(base_dir, "input", "bilboard3.pdf")
            if os.path.exists(sample_input):
                 settings["file_path"] = sample_input
        
        # --- POCZĄTEK ZMIANY ---
        # Ustaw domyślny katalog wyjściowy tylko, jeśli nie jest już zdefiniowany w ustawieniach.
        if not settings.get("output_dir"):
            settings["output_dir"] = os.path.join(base_dir, "output")
        
        # Ustaw domyślną ścieżkę logów tylko, jeśli nie jest już zdefiniowana.
        if not settings.get("log_file_path"):
            settings["log_file_path"] = os.path.join(base_dir, "logs", "app.log")
        # --- KONIEC ZMIANY ---
    
    validate_rasterization_settings(settings)

    return settings



def save_settings(filepath="settings.json"):
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filepath)
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)