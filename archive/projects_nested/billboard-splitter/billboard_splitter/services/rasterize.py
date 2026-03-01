# billboard_splitter/services/rasterize.py
import os
import sys
import time
import tempfile
import logging
import fitz  # PyMuPDF
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

logger = logging.getLogger('BillboardSplitter')

# Prosty cache w pamięci, aby uniknąć wielokrotnej rasteryzacji tego samego pliku w jednej sesji
RASTER_CACHE = {}

def clear_raster_cache():
    """Clears the in-memory cache and deletes the associated temporary files."""
    global RASTER_CACHE
    logger.info(f"Clearing rasterization cache ({len(RASTER_CACHE)} items).")
    for key, value in list(RASTER_CACHE.items()):
        try:
            if isinstance(value, dict) and 'path' in value and os.path.exists(value['path']):
                os.remove(value['path'])
                logger.debug(f"Removed cached rasterized file: {value['path']}")
        except Exception as e:
            logger.error(f"Error removing cached file {value.get('path', '')}: {e}")
    RASTER_CACHE.clear()


def rasterize_input(src_path: str, settings: dict) -> dict:
    """
    Rasteryzuje plik wejściowy (PDF lub bitmapę) do tymczasowego, 1-stronicowego pliku PDF,
    jeśli opcja rasteryzacji jest włączona w ustawieniach.

    Args:
        src_path (str): Ścieżka do pliku wejściowego.
        settings (dict): Słownik ustawień aplikacji.

    Returns:
        dict: Słownik z wynikiem operacji.
              - {"kind": "passthrough"} jeśli rasteryzacja jest wyłączona.
              - {"kind": "rasterized", "path": temp_pdf_path, "dpi": dpi, "width_cm": width_cm, "height_cm": height_cm} po sukcesie.
              - {"kind": "error", "message": error_message} w przypadku błędu.
    """
    raster_settings = settings.get("rasterization", {})
    if not raster_settings.get("enabled"):
        return {"kind": "passthrough"}

    if not src_path or not os.path.exists(src_path):
        return {"kind": "error", "message": "Source file not found"}

    try:
        file_stat = os.stat(src_path)
        mtime = file_stat.st_mtime
        fsize = file_stat.st_size
        dpi = raster_settings.get("dpi", 300)
        compression = raster_settings.get("compression", "LZW")

        cache_key = (src_path, mtime, fsize, dpi, compression)
        if cache_key in RASTER_CACHE:
            cached_result = RASTER_CACHE[cache_key]
            if os.path.exists(cached_result["path"]):
                logger.info(f"Using cached rasterized PDF: {cached_result['path']}")
                return cached_result
            else:
                del RASTER_CACHE[cache_key] # Usunięcie nieaktualnego wpisu

        logger.info(f"Rasterizing '{os.path.basename(src_path)}' at {dpi} DPI with {compression} compression...")

        # Utworzenie tymczasowego pliku na zrasteryzowany obraz
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_image_file:
            tmp_image_path = tmp_image_file.name

        page_width_pt, page_height_pt = 0, 0
        
        # Krok 1: Renderowanie wejścia do obrazu PNG
        file_ext = os.path.splitext(src_path)[1].lower()
        if file_ext == ".pdf":
            doc = fitz.open(src_path)
            page = doc.load_page(0)
            
            # Zachowanie oryginalnych wymiarów w punktach
            page_width_pt, page_height_pt = page.rect.width, page.rect.height

            # Renderowanie do pixmapy z zadanym DPI
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            pix.save(tmp_image_path)
            doc.close()

        elif file_ext in ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp']:
            with Image.open(src_path) as img:
                # Konwersja do RGB, jeśli jest to konieczne (np. dla CMYK)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                img.save(tmp_image_path, 'png')
                
                # Obliczenie wymiarów w punktach
                img_dpi = img.info.get('dpi', (dpi, dpi))
                if not isinstance(img_dpi, (tuple, list)) or len(img_dpi) != 2:
                    img_dpi = (dpi, dpi)
                
                px_w, px_h = img.size
                page_width_pt = px_w * 72.0 / img_dpi[0]
                page_height_pt = px_h * 72.0 / img_dpi[1]
        else:
            os.remove(tmp_image_path)
            return {"kind": "error", "message": f"Unsupported file type for rasterization: {file_ext}"}

        # Krok 2: Opakowanie obrazu w nowy, 1-stronicowy PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf_file:
            temp_pdf_path = tmp_pdf_file.name

        c = canvas.Canvas(temp_pdf_path, pagesize=(page_width_pt, page_height_pt))
        
        # Użycie ImageReader do obsługi kompresji
        img_reader = ImageReader(tmp_image_path)
        
        # Wstawienie obrazu na całą stronę
        c.drawImage(img_reader, 0, 0, width=page_width_pt, height=page_height_pt, mask='auto')
        
        # Ustawienie kompresji (ReportLab domyślnie używa FlateDecode, co jest bezstratne)
        if compression == "None":
            c.setPageCompression(0)
        else: # "LZW" lub domyślnie
            c.setPageCompression(1)

        c.save()
        
        # Usunięcie tymczasowego pliku obrazu
        os.remove(tmp_image_path)

        width_cm = page_width_pt * 2.54 / 72
        height_cm = page_height_pt * 2.54 / 72

        result = {
            "kind": "rasterized",
            "path": temp_pdf_path,
            "dpi": dpi,
            "width_cm": width_cm,
            "height_cm": height_cm
        }
        
        RASTER_CACHE[cache_key] = result
        logger.info(f"Rasterized to PDF at {dpi} DPI (lossless) -> {temp_pdf_path}")
        
        return result

    except Exception as e:
        logger.error(f"Error during rasterization of '{src_path}': {e}", exc_info=True)
        # Sprzątanie po błędzie
        if 'tmp_image_path' in locals() and os.path.exists(tmp_image_path):
            os.remove(tmp_image_path)
        if 'temp_pdf_path' in locals() and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        return {"kind": "error", "message": str(e)}