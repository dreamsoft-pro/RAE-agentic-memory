# Plik: splitter.py
# Wersja: Ostateczna, z naprawą fundamentalnego błędu wczytywania ustawień

from lang_pl import LANG
from pypdf import PdfReader, Transformation
import os
import sys
import re
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import white, CMYKColor, lightgrey, black
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
import barcode_qr
import config
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import logging
from logging.handlers import TimedRotatingFileHandler
from PIL import Image, ImageDraw
from license_manager import verify_license
import pymupdf as fitz
from billboard_splitter.services.rasterize import rasterize_input

from billboard_splitter.core.scale_context import ScaleContext

# Definicja koloru PANTONE – używana do znaczników i linii
PANTONE_BLACK_C = CMYKColor(0.01, 0.01, 0.01, 1, spotName="PANTONE Black C")

class SplitPDF:
    def __init__(self, config_module):
        self.config = config_module
        self.logger = self.setup_logging()
        self.trial_mode = verify_license(logger=self.logger)
        if self.trial_mode:
            self.logger.info(LANG["log_trial_mode_active"])
        else:
            self.logger.info(LANG["log_trial_mode_inactive"])
        
        self.generated_output_files = []
        self.width = 0
        self.height = 0
        self.core_slice_width = 0
        self.core_slice_height = 0
        self.slice_width = 0
        self.slice_height = 0
        self.margin_top = 0
        self.margin_bottom = 0
        self.margin_left = 0
        self.margin_right = 0
        self.mark_width = 0
        self.mark_height = 0
        self.sep_line_length = 0
        self.overlap_value = 0
        self.effective_overlap = 0
        self.use_white_stripe = False
        self.white_stripe = 0
        self.mm = mm
        self.scale_context = None
        
        self._preview_cache = {}
        self.update_graphic_settings()

    def setup_logging(self):
        logger = logging.getLogger('BillboardSplitter')
        if logger.hasHandlers():
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
        
        logger.propagate = False
        file_handler_added = False

        try:
            log_level_str = self.config.settings.get("logging_level", "INFO").upper()
            log_level = getattr(logging, log_level_str, logging.INFO)
            logger.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            logging_mode = self.config.settings.get("logging_mode", "console")
            log_file_path = self.config.settings.get("log_file_path", "logs/app.log")
            log_dir = os.path.dirname(log_file_path)

            if not os.path.exists(log_dir):
                try:
                    os.makedirs(log_dir, exist_ok=True)
                except OSError as e:
                    logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
                    logger.error(f"Nie udało się utworzyć katalogu logów {log_dir}: {e}")
                    logging_mode = "console"

            if logging_mode in ["logging_console", "logging_both"]:
                ch = logging.StreamHandler(sys.stdout)
                ch.setFormatter(formatter)
                logger.addHandler(ch)

            if logging_mode in ["logging_file", "logging_both"] and os.path.exists(log_dir):
                try:
                    fh = TimedRotatingFileHandler(
                         log_file_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
                    )
                    fh.suffix = "%Y-%m-%d"
                    fh.setFormatter(formatter)
                    logger.addHandler(fh)
                    file_handler_added = True
                except Exception as e_fh:
                    logger.error(f"Nie udało się dodać File Handler dla {log_file_path}: {e_fh}")

            if logger.hasHandlers():
                file_str = log_file_path if file_handler_added else LANG["no_file"]
                logger.info(LANG["log_configured"].format(log_level_str, logging_mode, file_str))
            else:
                 if logging_mode != 'none':
                    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
                    logger = logging.getLogger('BillboardSplitter')
                    logger.warning(LANG["log_no_handlers"].format(logging_mode))
                    logger.warning(LANG["log_basic_config"])
        
        except Exception as e:
            logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
            logger = logging.getLogger('BillboardSplitter')
            logger.error(LANG["log_critical_error"].format(e), exc_info=True)
            logger.warning(LANG["log_basic_config"])
            
        return logger

    def update_graphic_settings(self):
        try:
            gf = self.config.settings.get("graphic_settings", {})
            mm = self.mm
            self.margin_top    = gf.get("margin_top",    2.0) * mm
            self.margin_bottom = gf.get("margin_bottom", 2.0) * mm
            self.margin_left   = gf.get("margin_left",   2.0) * mm
            self.margin_right  = gf.get("margin_right",  2.0) * mm
            self.mark_width    = gf.get("reg_mark_width", 5.0) * mm
            self.mark_height   = gf.get("reg_mark_height",5.0) * mm
            # Szukaj najpierw w głównych ustawieniach (zaktualizowanych przez kwargs), potem w gf
            self.sep_line_length = self.config.settings.get("sep_line_length", gf.get("sep_line_length", 0.0)) * mm
            self.logger.debug(
                f"Graphic settings reloaded (T/B/L/R mm): "
                f"{self.margin_top/mm:.1f}/{self.margin_bottom/mm:.1f}/"
                f"{self.margin_left/mm:.1f}/{self.margin_right/mm:.1f}. Line len: {self.sep_line_length/mm:.1f}"
            )
        except Exception as e:
            self.logger.error(LANG["log_graphic_settings_error"].format(e), exc_info=True)

    def _load_input_as_pdf(self, input_path: str) -> tuple[str | None, bool]:
        ext = os.path.splitext(input_path)[1].lower()
        try:
            if ext == ".pdf":
                self.logger.info(LANG["log_loading_pdf"].format(input_path))
                return input_path, False
            elif ext in [".jpg", ".jpeg", ".tif", ".tiff"]:
                self.logger.info(LANG["log_loading_bitmap"].format(input_path))
                img = Image.open(input_path)
                dpi_info = img.info.get('dpi', (300.0, 300.0))
                dpi_val = dpi_info[0] if isinstance(dpi_info, tuple) else dpi_info
                if dpi_val <= 0:
                    self.logger.warning(LANG["log_invalid_dpi"].format(dpi_val, 300))
                    dpi_val = 300.0
                
                factor = 72.0 / dpi_val
                width_pts, height_pts = img.width * factor, img.height * factor
                
                temp_pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                temp_pdf_path = temp_pdf_file.name
                temp_pdf_file.close()

                c = canvas.Canvas(temp_pdf_path, pagesize=(width_pts, height_pts))
                c.drawImage(ImageReader(img), 0, 0, width=width_pts, height=height_pts, preserveAspectRatio=True, mask='auto')
                c.save()
                img.close()
                self.logger.info(f"Obraz przekonwertowany na tymczasowy PDF: {temp_pdf_path}")
                return temp_pdf_path, True
            else:
                self.logger.error(LANG["log_unsupported_format"].format(ext))
                return None, False
        except FileNotFoundError:
            self.logger.error(LANG["log_input_file_not_found"].format(input_path))
            return None, False
        except Exception as e:
            self.logger.error(LANG["log_load_process_error"].format(input_path, e), exc_info=True)
            return None, False

    def calculate_dimensions(self, overlap, rows, cols, white_stripe, add_white_to_overlap=False, sx=1.0, sy=1.0):
        self.logger.info(f"Calculating dimensions with overlap: {overlap}, scale_x: {sx}, scale_y: {sy}")
        if not (isinstance(rows, int) and rows > 0 and isinstance(cols, int) and cols > 0):
            raise ValueError(LANG["error_invalid_rows_cols"])
        
        W_mm, H_mm = self.width / self.mm, self.height / self.mm
        self.use_white_stripe = add_white_to_overlap
        self.white_stripe = abs(white_stripe) if self.use_white_stripe else 0.0
        self.overlap_value = abs(overlap)
        self.effective_overlap = self.overlap_value + self.white_stripe

        # Adjust the absolute (1:1) overlap value to the scale of the input file.
        # This allows mixing the input file's dimensions (W_mm, H_mm) with the overlap.
        effective_overlap_adjusted_x = self.effective_overlap / sx if sx != 0 else 0
        effective_overlap_adjusted_y = self.effective_overlap / sy if sy != 0 else 0
        
        S_x_mm = (W_mm + (cols - 1) * effective_overlap_adjusted_x) / cols if cols > 0 else 0
        S_y_mm = (H_mm + (rows - 1) * effective_overlap_adjusted_y) / rows if rows > 0 else 0
        
        self.slice_width = S_x_mm * self.mm
        self.slice_height = S_y_mm * self.mm
        self.core_slice_width = self.slice_width - (effective_overlap_adjusted_x * self.mm)
        self.core_slice_height = self.slice_height - (effective_overlap_adjusted_y * self.mm)
        
        if self.slice_width <= 0 or self.slice_height <= 0:
            raise ValueError(LANG["error_invalid_slice_dimensions"])

    def get_slice_info(self, row, col, rows, cols):
        x_offset = col * self.core_slice_width
        y_offset = (rows - 1 - row) * self.core_slice_height
        return {
            "row": row, "col": col,
            "name": f"0{chr(65 + row)}{col + 1:02d}",
            "offset": (round(x_offset, 3), round(y_offset, 3)),
            "width": self.slice_width, "height": self.slice_height
        }

    def _apply_pypdf_overlay(self, page: fitz.Page, pagesize: tuple, draw_callback, offset: tuple = (0.0, 0.0)):
        try:
            overlay_w, overlay_h = pagesize
            off_x, off_y = offset

            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=(overlay_w, overlay_h))
            draw_callback(c)
            c.save()
            buf.seek(0)

            overlay_doc = fitz.open(stream=buf.getvalue(), filetype="pdf")
            if overlay_doc.page_count > 0:
                y_top = page.rect.height - off_y - overlay_h
                rect = fitz.Rect(off_x, y_top, off_x + overlay_w, y_top + overlay_h)
                page.show_pdf_page(rect, overlay_doc, 0)
            overlay_doc.close()
            buf.close()
        except Exception as e:
            self.logger.error(f"Błąd nakładania overlay'a: {e}", exc_info=True)


            
    def get_ordered_slices(self, rows, cols, order_type):
        all_slices_info = [self.get_slice_info(r, c, rows, cols) for r in range(rows) for c in range(cols)]
        order_logic = {
            "bryt_order_1": lambda s: (s["row"], s["col"]),
            "bryt_order_2": lambda s: (s["row"], s["col"] if s["row"] % 2 == 0 else -s["col"]),
            "bryt_order_3": lambda s: (s["col"], s["row"]),
            "bryt_order_4": lambda s: (s["col"], s["row"] if s["col"] % 2 == 0 else -s["row"]),
            "bryt_order_5": lambda s: (-s["row"], s["col"]),
            "bryt_order_6": lambda s: (-s["row"], s["col"] if (rows - 1 - s["row"]) % 2 == 0 else -s["col"])
        }
        key_func = order_logic.get(order_type, order_logic["bryt_order_1"])
        return sorted(all_slices_info, key=key_func)

    # =================================================================================
    # GŁÓWNA METODA STERUJĄCA (DYSPATCHER)
    # =================================================================================

    def split(self, input_pdf_path, output_dir, **kwargs):
        self.logger.info(LANG["log_start_splitting_process"].format(input_pdf_path))
        self.config.settings.update(kwargs)
        
        self.scale_context = ScaleContext(self.config.settings)
        self.update_graphic_settings()

        original_input_path = input_pdf_path

        if self.config.settings.get("rasterization", {}).get("enabled"):
            raster_result = rasterize_input(input_pdf_path, self.config.settings)
            if raster_result["kind"] == "rasterized":
                input_pdf_path = raster_result["path"]
            elif raster_result["kind"] == "error":
                self.logger.error(f"Rasterization failed: {raster_result.get('message')}")
                return False
        
        path_for_naming = original_input_path

        product_mode = self.config.settings.get("product_mode", "billboard")
        self.logger.info(f"Product mode selected: {product_mode}")

        if product_mode == 'poster':
            return self._process_poster(input_pdf_path, output_dir, path_for_naming)
        elif product_mode == 'pos':
            return self._process_pos(input_pdf_path, output_dir, path_for_naming)
        else:
            return self._process_billboard(input_pdf_path, output_dir, path_for_naming)

    # =================================================================================
    # LOGIKA DLA TRYBU "BILLBOARD"
    # =================================================================================

    def _process_billboard(self, input_pdf_path, output_dir, path_for_naming=None):
        path_for_naming = path_for_naming or input_pdf_path
        settings = self.config.settings
        
        overlap = settings.get("overlap", 20.0)
        rows = settings.get("rows", 2)
        cols = settings.get("cols", 5)
        output_type = settings.get("output_type", "output_common_sheet")
        layout = settings.get("layout", "layout_vertical")
        enable_separation_lines = settings.get("enable_separation_lines", True)
        add_line_at_start = settings.get("add_line_at_start", False)
        add_line_at_end = settings.get("add_line_at_end", False)
        enable_reg_marks = settings.get("enable_reg_marks", True)
        registration_mark_type = settings.get("registration_mark_type", "reg_mark_cross")
        enable_barcode = settings.get("enable_barcode", True)
        barcode_type = settings.get("barcode_type", "code_qr")
        bryt_order = settings.get("bryt_order", "bryt_order_1")
        white_stripe = settings.get("white_stripe", 10.0)
        add_white_to_overlap = settings.get("add_white_to_overlap", True)
        
        self.logger.info(LANG["log_split_settings"].format(rows, cols, overlap, white_stripe, add_white_to_overlap))
        self.logger.info(LANG["log_output_dir_info"].format(output_type, layout, output_dir))
        
        processing_mode = settings.get("processing_mode", "hdd")
        source_doc, temp_dir, fragments = None, "", []
        pdf_to_process_path, is_temp_file = None, False

        try:
            pdf_to_process_path, is_temp_file = self._load_input_as_pdf(input_pdf_path)
            if not pdf_to_process_path: return False

            source_doc = fitz.open(pdf_to_process_path)
            if not source_doc.page_count:
                self.logger.error(LANG["log_cannot_load_or_empty_pdf"])
                return False

            page = source_doc.load_page(0)
            self.width, self.height = float(page.rect.width), float(page.rect.height)
            
            sx = self.scale_context.sx if self.scale_context else 1.0
            sy = self.scale_context.sy if self.scale_context else 1.0
            self.calculate_dimensions(overlap, rows, cols, white_stripe, add_white_to_overlap, sx, sy)
            
            ordered_slices = self.get_ordered_slices(rows, cols, bryt_order)
            self.logger.info(LANG["log_final_slices_order"].format(bryt_order, ", ".join(s['name'] for s in ordered_slices)))

            if processing_mode == 'hdd':
                temp_dir = tempfile.mkdtemp()
            
            for slice_info in ordered_slices:
                complete_slice_doc = self._create_complete_slice_doc(source_doc, slice_info, rows, cols)
                if complete_slice_doc:
                    if processing_mode == 'hdd':
                        temp_path = os.path.join(temp_dir, f"{slice_info['name']}.pdf")
                        complete_slice_doc.save(temp_path, garbage=3)
                        fragments.append(temp_path)
                    else:
                        buffer = io.BytesIO()
                        complete_slice_doc.save(buffer, garbage=3)
                        buffer.seek(0)
                        fragments.append(buffer)
                    complete_slice_doc.close()
            
            if len(fragments) != len(ordered_slices):
                raise RuntimeError("Nie udało się utworzyć wszystkich fragmentów.")

            result = False
            if output_type in ["output_separate_files", "output_both"]:
                result = self._assemble_separate_files(ordered_slices, fragments, output_dir, enable_separation_lines, add_line_at_start, add_line_at_end, enable_barcode, barcode_type, path_for_naming, layout)
            
            if output_type in ["output_common_sheet", "output_both"]:
                base_name = os.path.splitext(os.path.basename(path_for_naming))[0]
                sheet_suffix = "_h_separated.pdf" if "horizontal" in layout else "_v_separated.pdf"
                output_path = os.path.join(output_dir, base_name + sheet_suffix)
                common_result = self._assemble_common_sheet(ordered_slices, fragments, output_path, layout, enable_separation_lines, add_line_at_start, add_line_at_end, enable_barcode, barcode_type, path_for_naming)
                result = (result and common_result) if output_type == "output_both" else common_result

            return result
        except Exception as e:
            self.logger.error(LANG["log_unexpected_error_in_splitting"].format(input_pdf_path, e), exc_info=True)
            return False
        finally:
            if source_doc: source_doc.close()
            if is_temp_file and pdf_to_process_path and os.path.exists(pdf_to_process_path):
                try: os.remove(pdf_to_process_path)
                except Exception: pass
            if temp_dir and os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)

    def _create_complete_slice_doc(self, source_doc: fitz.Document, slice_info: dict, rows: int, cols: int) -> fitz.Document | None:
        try:
            W, H = slice_info["width"], slice_info["height"]
            if W <= 0 or H <= 0: return None

            # Powrót do braku fizycznego skalowania strony (format 1:10)
            slice_doc = fitz.open()
            slice_page = slice_doc.new_page(width=W, height=H)

            offset_x, offset_y = slice_info["offset"]
            top_y = self.height - offset_y - H
            clip_rect = fitz.Rect(offset_x, top_y, offset_x + W, top_y + H)
            slice_page.show_pdf_page(slice_page.rect, source_doc, 0, clip=clip_rect)
            
            # --- Inlined Overlay Logic ---
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=(W, H))
            
            enable_reg_marks = self.config.settings.get("enable_reg_marks", True)
            reg_mark_type = self.config.settings.get("registration_mark_type", "reg_mark_cross")
            
            # Przekazujemy rzeczywistą skalę (np. 10), aby elementy Grupy 2 (paski, pasery)
            # mogły zostać odpowiednio pomniejszone (skalowane wraz z treścią).
            current_sx = self.scale_context.sx if self.scale_context else 1.0
            self._draw_rotating_elements(c, slice_info, rows, cols, enable_reg_marks, reg_mark_type, sx=current_sx)
            c.save()
            overlay_bytes = buf.getvalue()
            buf.close()

            if overlay_bytes:
                overlay_doc = fitz.open(stream=overlay_bytes, filetype="pdf")
                if overlay_doc.page_count > 0:
                    slice_page.show_pdf_page(slice_page.rect, overlay_doc, 0)
                overlay_doc.close()
            # --- End Inlined Logic ---

            rotation = self.config.settings.get("slice_rotation", 0)
            if rotation == 180:
                slice_page.set_rotation(180)

            return slice_doc
        except Exception as e:
            self.logger.error(f"Błąd tworzenia brytu '{slice_info.get('name')}': {e}", exc_info=True)
            return None

    def _draw_rotating_elements(self, c, slice_info, rows, cols, enable_reg_marks, registration_mark_type, sx=1.0):
        self._draw_white_stripes_on_canvas(c, slice_info, rows, cols, sx=sx)
        
        if enable_reg_marks:
            if registration_mark_type == "reg_mark_cross":
                self.draw_registration_marks_custom_grid(c, 0, 0, slice_info, rows, cols, sx=sx)
            elif registration_mark_type == "reg_mark_line":
                # self.draw_registration_lines(c, 0, 0, slice_info, rows, cols, sx=sx)
                pass

        if self.config.settings.get("draw_slice_border", False):
            self._draw_full_slice_border(c, slice_info['width'], slice_info['height'], sx=sx)
    
    def _draw_full_slice_border(self, c, slice_width, slice_height, sx=1.0):
        c.saveState()
        # Absolute width, no scaling
        c.setStrokeColor(PANTONE_BLACK_C)
        c.setLineWidth(0.1 * self.mm)
        c.rect(0, 0, slice_width, slice_height, stroke=1, fill=0)
        c.restoreState()

    def _generate_legacy_overlay(self, width_pt, height_pt, slice_info, rows, cols, sx=1.0) -> bytes:
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(width_pt, height_pt))
        
        enable_reg_marks = self.config.settings.get("enable_reg_marks", True)
        reg_mark_type = self.config.settings.get("registration_mark_type", "reg_mark_cross")
        
        self._draw_rotating_elements(c, slice_info, rows, cols, enable_reg_marks, reg_mark_type, sx=sx)
        
        c.save()
        return buf.getvalue()

    # =================================================================================
    # LOGIKA DLA TRYBU "POSTER" - PRZEPISANA W CAŁOŚCI
    # =================================================================================
    
    def _process_poster(self, input_pdf_path, output_dir, path_for_naming=None):
        """Poster:
        - obrót wejścia PRZED układaniem (preview + wynik),
        - odstęp między powtórzeniami jak w billboardach (slice_gap_horizontal/slice_gap w mm),
        - poziome separatory: środek górnego i dolnego marginesu,
        - pionowe znaczniki cięcia: cienkie czarne linie na KAŻDEJ pionowej krawędzi użytku
        przez całą wysokość arkusza (gdy włączone w ustawieniach)."""
        path_for_naming = path_for_naming or input_pdf_path
        self.logger.info(f"Starting poster processing for {input_pdf_path}")
        pdf_to_process_path, is_temp_file = self._load_input_as_pdf(input_pdf_path)
        if not pdf_to_process_path:
            return False

        source_doc = None
        try:
            source_doc = fitz.open(pdf_to_process_path)
            if not source_doc.page_count:
                self.logger.error("Poster source PDF has no pages.")
                return False

            s  = self.config.settings
            gs = s.get("graphic_settings", {})

            sx = self.scale_context.sx if self.scale_context else 1.0
            sy = self.scale_context.sy if self.scale_context else 1.0

            # --- ROTACJA: przyjmij różne możliwe klucze, znormalizuj do 0/90/180/270
            rot_raw = next((s.get(k) for k in (
                "input_rotation_deg", "input_rotation", "poster_rotation",
                "slice_rotation", "rotation"
            ) if k in s), 0)
            try:
                rotation = int(rot_raw) % 360
            except Exception:
                rotation = 0
            if rotation not in (0, 90, 180, 270):
                rotation = (round(rotation / 90) * 90) % 360

            repetitions = int(s.get("repetitions", 1))

            # --- GAP: jak w billboardach (mm) + fallback na stary poster_gap_cm
            abs_scale      = self._get_abs_scale(sx)
            default_gap_mm = float(gs.get("slice_gap", 0.0))
            gap_h_mm       = float(gs.get("slice_gap_horizontal", default_gap_mm))
            poster_gap_fb  = float(s.get("poster_gap_cm", 0.0))  # value in mm
            gap_mm         = gap_h_mm if gap_h_mm > 0 else poster_gap_fb
            gap            = gap_mm * self.mm * abs_scale

            # --- LINIE: Użyj dedykowanych kluczy dla Postera ---
            add_line_at_start = bool(s.get("add_line_at_start", False))
            add_line_at_end = bool(s.get("add_line_at_end", False))
            enable_cut_marks = bool(s.get("vertical_cut_marks", False))

            self.logger.debug(
                f"Poster settings used: rotation={rotation}, repetitions={repetitions}, "
                f"gap_mm={gap_mm}, start_line={add_line_at_start}, end_line={add_line_at_end}, cut_marks={enable_cut_marks}"
            )

            # --- WYMIARY JEDNOSTKOWE po obrocie (rotacja PRZED układaniem)
            src_page = source_doc.load_page(0)
            img_w, img_h = float(src_page.rect.width), float(src_page.rect.height)
            if rotation in (90, 270):
                img_w, img_h = img_h, img_w

            # --- PŁÓTNO (SKALOWANE) ---
            img_w_scaled = img_w * sx
            img_h_scaled = img_h * sy
            # Odstęp jest wartością absolutną, nie skalujemy go dodatkowo (już w gap)
            gap_abs = gap

            canvas_w = self.margin_left + self.margin_right + (img_w_scaled * repetitions) + (gap_abs * (repetitions - 1))
            canvas_h = self.margin_top + self.margin_bottom + img_h_scaled

            # Powiększ arkusz jeśli linia separacyjna tego wymaga
            if self.sep_line_length > canvas_w:
                canvas_w = self.sep_line_length
            if self.sep_line_length > canvas_h and enable_cut_marks:
                canvas_h = self.sep_line_length

            output_doc = fitz.open()
            page = output_doc.new_page(width=canvas_w, height=canvas_h)

            # --- RENDER UŻYTKÓW (rect już po obrocie, render z rotate=rotation)
            effective_rotation = rotation
            if rotation == 90:
                effective_rotation = 270
            elif rotation == 270:
                effective_rotation = 90

            for i in range(repetitions):
                x_pos = self.margin_left + i * (img_w_scaled + gap_abs)
                y_pos = self.margin_top
                rect = fitz.Rect(x_pos, y_pos, x_pos + img_w_scaled, y_pos + img_h_scaled)
                page.show_pdf_page(rect, source_doc, 0, rotate=effective_rotation)

            # --- OVERLAY: poziome separatory + (opcjonalnie) pionowe znaczniki na KAŻDEJ krawędzi użytku
            if add_line_at_start or add_line_at_end or enable_cut_marks:
                self._apply_pypdf_overlay(
                    page, (canvas_w, canvas_h),
                    lambda c: self._draw_poster_lines(
                        c, canvas_w, canvas_h, repetitions, img_w_scaled, gap_abs,
                        add_line_at_start, add_line_at_end, enable_cut_marks, sx=sx
                    )
                )

            # --- (opcjonalnie) trial/kody – bez zmian istniejącej logiki
            all_codes = []
            if bool(s.get("enable_barcode", True)):
                for i in range(repetitions):
                    x_pos = self.margin_left + i * (img_w_scaled + gap_abs)
                    info = self._prepare_barcode_info(
                        {"name": f"P{i+1}"}, path_for_naming, x_pos, self.margin_bottom,
                        s.get("barcode_type", "code_qr"), "common_sheet", "horizontal",
                        img_w_scaled, img_h_scaled
                    )
                    if info: all_codes.append(info)
                if all_codes:
                    self._apply_pypdf_overlay(page, (canvas_w, canvas_h),
                                            lambda c: self._draw_all_barcodes(c, all_codes))

            if self.trial_mode:
                self._apply_pypdf_overlay(page, (canvas_w, canvas_h),
                                        lambda c: self._draw_trial_text(c))

            base_name  = os.path.splitext(os.path.basename(path_for_naming))[0]
            output_path = os.path.join(output_dir, f"{base_name}_poster.pdf")
            output_doc.save(output_path, garbage=3, deflate=True)
            self.generated_output_files.append(output_path)
            return True

        except Exception as e:
            self.logger.error(f"Critical error during poster processing: {e}", exc_info=True)
            return False
        finally:
            if source_doc:
                source_doc.close()
            if is_temp_file and os.path.exists(pdf_to_process_path):
                try: os.remove(pdf_to_process_path)
                except: pass


    # =================================================================================
    # LOGIKA DLA TRYBU "POS" – BEZ CIĘCIA, TYLKO USTAWIENIA GRAFICZNE + KOD
    # =================================================================================
    def _process_pos(self, input_pdf_path, output_dir, path_for_naming=None):
        """
        POS:
        - brak jakiegokolwiek podziału / brytów,
        - użyj aktualnych ustawień graficznych (marginesy),
        - narysuj kody (jak w poster), opcjonalnie w liczbie 1 (bez powtórzeń),
        - wygeneruj pojedynczy PDF o rozmiarze: (marginesy + oryginalny obraz).
        """
        path_for_naming = path_for_naming or input_pdf_path
        self.logger.info(f"Starting POS processing for {input_pdf_path}")

        pdf_to_process_path, is_temp_file = self._load_input_as_pdf(input_pdf_path)
        if not pdf_to_process_path:
            return False

        source_doc = None
        try:
            source_doc = fitz.open(pdf_to_process_path)
            if not source_doc.page_count:
                self.logger.error("POS source PDF has no pages.")
                return False

            # 1) Źródłowa strona i rozmiar
            page0 = source_doc.load_page(0)
            img_w_pt = float(page0.rect.width)
            img_h_pt = float(page0.rect.height)

            # Pobierz skalowanie
            sx = self.scale_context.sx if self.scale_context else 1.0
            sy = self.scale_context.sy if self.scale_context else 1.0

            img_w_scaled = img_w_pt * sx
            img_h_scaled = img_h_pt * sy

            # 2) Marginesy z update_graphic_settings() (już wywołane w split())
            margin_left   = self.margin_left
            margin_right  = self.margin_right
            margin_top    = self.margin_top
            margin_bottom = self.margin_bottom

            # 3) Rozmiar wynikowego „arkusza” POS (uwzględniając skalowanie)
            canvas_w = margin_left + img_w_scaled + margin_right
            canvas_h = margin_bottom + img_h_scaled + margin_top

            # 4) Złóż wynik
            output_doc = fitz.open()
            page = output_doc.new_page(width=canvas_w, height=canvas_h)

            # wklej cały oryginał, skalując go do docelowego rozmiaru, z przesunięciem o marginesy
            page.show_pdf_page(
                fitz.Rect(margin_left, margin_top, margin_left + img_w_scaled, margin_top + img_h_scaled),
                source_doc, 0
            )

            # 5) (Opcjonalnie) KOD – dokładnie ta sama ścieżka co w poster,
            #    ale bez powtórzeń i bez linii/separatorów
            s = self.config.settings
            all_codes = []
            if s.get("enable_barcode", True):
                # umiejscawiamy kod przy dolnym marginesie, na prawym dolnym rogu użytku
                x_pos = margin_left      # lewy początek użytku
                info = self._prepare_barcode_info(
                    {"name": "POS"}, path_for_naming, x_pos, margin_bottom,
                    s.get("barcode_type", "code_qr"), "common_sheet", "horizontal",
                    img_w_scaled, img_h_scaled
                )
                if info:
                    all_codes.append(info)

            if all_codes:
                self._apply_pypdf_overlay(
                    page, (canvas_w, canvas_h),
                    lambda c: self._draw_all_barcodes(c, all_codes)
                )

            # 6) Trial watermark (jeśli włączony) – bez zmian względem innych trybów
            if self.trial_mode:
                self._apply_pypdf_overlay(page, (canvas_w, canvas_h),
                                          lambda c: self._draw_trial_text(c))

            # 7) Zapis
            base_name  = os.path.splitext(os.path.basename(path_for_naming))[0]
            output_path = os.path.join(output_dir, f"{base_name}_pos.pdf")
            output_doc.save(output_path, garbage=3, deflate=True)
            self.generated_output_files.append(output_path)

            self.logger.info("POS PDF generated successfully.")
            return True

        except Exception as e:
            self.logger.error(f"Critical error during POS processing: {e}", exc_info=True)
            return False
        finally:
            if source_doc:
                source_doc.close()
            if is_temp_file and os.path.exists(pdf_to_process_path):
                try:
                    os.remove(pdf_to_process_path)
                except:
                    pass



        def _draw_poster_lines(self, c, page_w, page_h, reps, img_w, gap, add_line_at_start, add_line_at_end, enable_cut_marks, sx=1.0):



            """Poster:



            - Poziome separatory: środek górnego i dolnego marginesu (jak billboard/separate),



            - Pionowe znaczniki cięcia: cienkie czarne linie na KAŻDEJ pionowej krawędzi użytku,



            przez całą wysokość arkusza (pozostają pionowe niezależnie od obrotu wejścia)."""



    



            # --- Poziome (góra/dół, środek marginesu)



            if add_line_at_start:



                if self.margin_top > 0:



                    y_top = page_h - (self.margin_top / 2.0)



                    self.draw_single_separation_line(c, 0, y_top, page_w, horizontal=True, sx=sx)



            if add_line_at_end:



                if self.margin_bottom > 0:



                    y_bottom = self.margin_bottom / 2.0



                    self.draw_single_separation_line(c, 0, y_bottom, page_w, horizontal=True, sx=sx)



    



                    # --- Pionowe: na krawędziach KAŻDEGO użytku, pełna wysokość, cienkie czarne



    



                    if enable_cut_marks and reps >= 1:



    



                        for i in range(reps):



    



                            x_left  = self.margin_left + i * (img_w + gap)



    



                            x_right = x_left + img_w



    



                            self.draw_single_separation_line(c, x_left, 0, page_h, horizontal=False, sx=sx)



    



                            self.draw_single_separation_line(c, x_right, 0, page_h, horizontal=False, sx=sx)



    



        def _draw_poster_side_ticks(self, c, page_w, page_h, reps, img_w, img_h, gap, sx=1.0):



            """Dla każdego użytku (rep>1): krótkie 'kreski na bokach' po lewej i prawej krawędzi użytku,



            umieszczone w połowie wysokości plakatu, wysunięte do środka arkusza."""



            if reps <= 1:



                return



    



            # Absolute dimensions



            tick_len = self.mark_height  # długość kreski



            y_mid = self.margin_bottom + (img_h / 2.0)



    



            c.saveState()



            gs = self.config.settings.get("graphic_settings", {})



            black_lw = gs.get("sep_line_black_width", 0.5) * self.mm



            white_lw = gs.get("sep_line_white_width", 0.3) * self.mm



    



            for i in range(reps):



                # lewa krawędź użytku



                x_left_edge = self.margin_left + i * (img_w + gap)



                # prawa krawędź użytku



                x_right_edge = x_left_edge + img_w



    



                # rysujemy krótkie POZIOME kreski wchodzące do środka (na arkusz)



                # lewa strona: od krawędzi do środka



                if black_lw > 0:



                    c.setStrokeColor(PANTONE_BLACK_C)



                    c.setLineWidth(black_lw)



                    c.line(x_left_edge, y_mid, x_left_edge + tick_len, y_mid)



                    c.line(x_right_edge - tick_len, y_mid, x_right_edge, y_mid)



                if white_lw > 0:



                    c.setStrokeColor(white)



                    c.setLineWidth(white_lw)



                    c.line(x_left_edge, y_mid, x_left_edge + tick_len, y_mid)



                    c.line(x_right_edge - tick_len, y_mid, x_right_edge, y_mid)



    



            c.restoreState()
            


    # =================================================================================
    # METODY SKŁADAJĄCE (COMMON & SEPARATE)
    # =================================================================================

    def _assemble_common_sheet(self, ordered_slices, fragments, output_path, layout, enable_sep, add_start, add_end, enable_barcode, barcode_type, path_for_naming):
        if not fragments: return False
        
        total = len(fragments)
        is_horizontal = "horizontal" in layout
        
        gs = self.config.settings.get("graphic_settings", {})
        default_gap_val = gs.get("slice_gap", 0.0)
        gap_h = float(gs.get("slice_gap_horizontal", default_gap_val)) * self.mm
        gap_v = float(gs.get("slice_gap_vertical", default_gap_val)) * self.mm
        used_gap = gap_h if is_horizontal else gap_v
        
        scale_x = self.scale_context.sx
        scale_y = self.scale_context.sy

        if is_horizontal:
            slice_w_rot_scaled = self.slice_height * scale_y
            slice_h_rot_scaled = self.slice_width * scale_x
            content_w_scaled = slice_w_rot_scaled
            content_h_scaled = total * slice_h_rot_scaled + (total - 1) * used_gap
        else:
            slice_w_scaled = self.slice_width * scale_x
            slice_h_scaled = self.slice_height * scale_y
            content_w_scaled = slice_w_scaled
            content_h_scaled = total * slice_h_scaled + (total - 1) * used_gap

        page_w = self.margin_left + content_w_scaled + self.margin_right
        # Jeśli długość linii separacyjnej jest większa niż szerokość arkusza, powiększ arkusz
        if self.sep_line_length > page_w:
            page_w = self.sep_line_length

        page_h = self.margin_top + content_h_scaled + self.margin_bottom

        output_doc = fitz.open()
        page = output_doc.new_page(width=page_w, height=page_h)
        all_codes = []

        try:
            for i, (slice_info, fragment) in enumerate(zip(ordered_slices, fragments)):
                frag_doc = fitz.open(stream=fragment) if isinstance(fragment, io.BytesIO) else fitz.open(fragment)
                
                base_rotation = frag_doc[0].rotation
                
                if is_horizontal:
                    slice_w_rot_scaled, slice_h_rot_scaled = self.slice_height * scale_y, self.slice_width * scale_x
                    x_left = self.margin_left
                    y_top = self.margin_top + i * (slice_h_rot_scaled + used_gap)
                    rect = fitz.Rect(x_left, y_top, x_left + slice_w_rot_scaled, y_top + slice_h_rot_scaled)
                    page.show_pdf_page(rect, frag_doc, 0, rotate=(base_rotation + 90))
                    
                    if enable_barcode:
                        barcode_base_y = page_h - (y_top + slice_h_rot_scaled)
                        info = self._prepare_barcode_info(slice_info, path_for_naming, x_left, barcode_base_y, barcode_type, "common_sheet", "horizontal", slice_w_rot_scaled, slice_h_rot_scaled)
                        if info: all_codes.append(info)
                else:
                    slice_w_scaled, slice_h_scaled = self.slice_width * scale_x, self.slice_height * scale_y
                    x_left = self.margin_left
                    y_top = self.margin_top + i * (slice_h_scaled + used_gap)
                    rect = fitz.Rect(x_left, y_top, x_left + slice_w_scaled, y_top + slice_h_scaled)
                    page.show_pdf_page(rect, frag_doc, 0, rotate=base_rotation)

                    if enable_barcode:
                        barcode_base_y = page_h - (y_top + slice_h_scaled)
                        info = self._prepare_barcode_info(slice_info, path_for_naming, x_left, barcode_base_y, barcode_type, "common_sheet", "vertical", slice_w_scaled, slice_h_scaled)
                        if info: all_codes.append(info)
                frag_doc.close()
            
            if enable_sep or add_start or add_end:
                slice_h_final = slice_h_rot_scaled if is_horizontal else slice_h_scaled
                self._apply_pypdf_overlay(page, (page_w, page_h), lambda c: self._draw_separation_lines_for_page(c, page_w, page_h, total, None, layout, used_gap, enable_sep, add_start, add_end, slice_h_on_page=slice_h_final, sx=scale_x))
            if all_codes:
                self._apply_pypdf_overlay(page, (page_w, page_h), lambda c: self._draw_all_barcodes(c, all_codes, sx=scale_x))
            if self.trial_mode:
                self._apply_pypdf_overlay(page, (page_w, page_h), lambda c: self._draw_trial_text(c))

            output_doc.save(output_path, garbage=3, deflate=True)
            self.generated_output_files.append(output_path)
            return True
        except Exception as e:
            self.logger.error(f"Błąd generowania wspólnego arkusza: {e}", exc_info=True)
            return False
        finally:
            output_doc.close()

    def _assemble_separate_files(self, ordered_slices, fragments, output_dir, enable_sep, add_start, add_end, enable_barcode, barcode_type, path_for_naming, layout):
        if not fragments: return False

        base_name = os.path.splitext(os.path.basename(path_for_naming))[0]
        match = re.match(r"^(\d+)_(\d+)_.*", base_name)
        file_base = f"{match.group(1)}_{match.group(2)}" if match else base_name
        
        is_horizontal = "horizontal" in layout
        saved_files = []

        for i, (slice_info, fragment) in enumerate(zip(ordered_slices, fragments)):
            frag_doc = fitz.open(stream=fragment) if isinstance(fragment, io.BytesIO) else fitz.open(fragment)
            slice_name = slice_info["name"]
            
            try:
                frag_page = frag_doc.load_page(0)
                W, H = frag_page.rect.width, frag_page.rect.height
                
                content_w, content_h = (H, W) if is_horizontal else (W, H)
                page_w = self.margin_left + content_w + self.margin_right
                if self.sep_line_length > page_w:
                    page_w = self.sep_line_length
                
                page_h = self.margin_top + content_h + self.margin_bottom

                output_doc = fitz.open()
                page = output_doc.new_page(width=page_w, height=page_h)
                target_rect = fitz.Rect(self.margin_left, self.margin_top, self.margin_left + content_w, self.margin_top + content_h)

                base_rotation = frag_page.rotation
                final_rotation = (base_rotation + 90) if is_horizontal else base_rotation
                page.show_pdf_page(target_rect, frag_doc, 0, rotate=final_rotation)

                all_codes = []
                if enable_barcode:
                    barcode_base_x, barcode_base_y = self.margin_left, self.margin_bottom
                    info = self._prepare_barcode_info(slice_info, path_for_naming, barcode_base_x, barcode_base_y, barcode_type, "separate_files", layout, content_w, content_h)
                    if info: all_codes.append(info)
                
                if enable_sep or add_start or add_end:
                    h_brytu = content_h
                    self._apply_pypdf_overlay(page, (page_w, page_h), lambda c, idx=i: self._draw_separation_lines_for_page(c, page_w, page_h, 1, idx, layout, 0.0, False, add_start, add_end, slice_h_on_page=h_brytu, sx=self.scale_context.sx))
                if all_codes:
                    self._apply_pypdf_overlay(page, (page_w, page_h), lambda c: self._draw_all_barcodes(c, all_codes, sx=self.scale_context.sx))
                if self.trial_mode:
                    self._apply_pypdf_overlay(page, (page_w, page_h), lambda c: self._draw_trial_text(c))

                suffix = "_h.pdf" if is_horizontal else "_v.pdf"
                out_path = os.path.join(output_dir, f"{file_base}_{slice_name}{suffix}")
                output_doc.save(out_path, garbage=3, deflate=True)
                saved_files.append(out_path)
            
            except Exception as e:
                self.logger.error(f"Błąd tworzenia pliku dla '{slice_name}': {e}", exc_info=True)
            finally:
                if 'output_doc' in locals(): output_doc.close()
                frag_doc.close()

        self.generated_output_files = saved_files
        return True

    # =================================================================================
    # METODY RYSUJĄCE (Paski, Pasery, Linie, Kody)
    # =================================================================================

    def _get_abs_scale(self, current_sx=None):
        """
        Returns the scale factor for decorations.
        If we are drawing on a scaled-down tile (e.g. 1:10 source), we need to draw decorations 
        smaller (divide by scale) so they appear correct physical size when printed/blown up.
        If drawing on a 1:1 canvas (common sheet), sx should be 1.0.
        """
        if current_sx is None:
            # Default to 1.0 (no scaling) if not specified
            return 1.0
        
        # If sx is 0 or negative, fallback to 1.0 to avoid division by zero
        if current_sx <= 0:
            return 1.0
            
        return 1.0 / current_sx

    def _draw_white_stripes_on_canvas(self, c, slice_info, total_rows, total_cols, sx=1.0):
        if not self.use_white_stripe or self.white_stripe <= 0: return

        abs_scale = self._get_abs_scale(sx)
        ws_pt = self.white_stripe * self.mm * abs_scale
        row, col = slice_info["row"], slice_info["col"]
        W, H = self.slice_width, self.slice_height

        c.saveState()
        c.setFillColor(white)
        c.setStrokeColor(PANTONE_BLACK_C)
        c.setLineWidth(0.1 * self.mm * abs_scale)

        is_top_row, is_lower_row = (row == 0), (row > 0)
        is_last_col = (col == total_cols - 1)

        if is_top_row and not is_last_col:
            # Vertical stripe on the right
            x, y, w, h = W - ws_pt, 0, ws_pt, H
            c.rect(x, y, w, h, stroke=0, fill=1)
            c.line(x + w, y, x + w, y + h)
            c.line(x, y + h, x + w, y + h)
            c.line(x, y, x + w, y)
        elif is_lower_row:
            if not is_last_col:
                # Horizontal stripe on top
                c.rect(0, H - ws_pt, W - ws_pt, ws_pt, stroke=0, fill=1)
                # Vertical stripe on right
                c.rect(W - ws_pt, 0, ws_pt, H, stroke=0, fill=1)
                # Border lines
                path = c.beginPath()
                path.moveTo(0, H)
                path.lineTo(W, H)
                path.lineTo(W, 0)
                c.drawPath(path, stroke=1, fill=0)
            else: # Last column
                # Horizontal stripe on top only
                x, y, w, h = 0, H - ws_pt, W, ws_pt
                c.rect(x, y, w, h, stroke=0, fill=1)
                c.line(x, y + h, x + w, y + h)
                c.line(x, y, x, y + h)
                c.line(x + w, y, x + w, y + h)
        
        c.restoreState()

    def add_registration_mark(self, c, x, y, sx=1.0):
        c.saveState()
        c.translate(x, y)
        
        abs_scale = self._get_abs_scale(sx)
        half_w, half_h = (self.mark_width * abs_scale) / 2.0, (self.mark_height * abs_scale) / 2.0
        
        gs = self.config.settings["graphic_settings"]
        white_lw = gs.get("reg_mark_white_line_width", 0.5) * self.mm * abs_scale
        black_lw = gs.get("reg_mark_black_line_width", 0.7) * self.mm * abs_scale
        
        if white_lw > 0:
            c.setStrokeColor(white)
            c.setLineWidth(white_lw)
            c.line(-half_w, 0, half_w, 0); c.line(0, -half_h, 0, half_h)
        if black_lw > 0:
            c.setStrokeColor(PANTONE_BLACK_C)
            c.setLineWidth(black_lw)
            c.line(-half_w, 0, half_w, 0); c.line(0, -half_h, 0, half_h)
        c.restoreState()
    
    def draw_registration_marks_custom_grid(self, c, x_pos, y_pos, slice_info, total_rows, total_cols, sx=1.0):
        row, col = slice_info["row"], slice_info["col"]
        
        slice_h = self.slice_height
        core_w = self.core_slice_width

        # These values are absolute, real-world dimensions from settings
        abs_scale = self._get_abs_scale(sx)
        half_mark_w, half_mark_h = (self.mark_width * abs_scale) / 2.0, (self.mark_height * abs_scale) / 2.0
        v_overlap_pt = self.effective_overlap * self.mm * abs_scale
        # NOTE: v_overlap_pt used for positioning might need adjustment if logic relies on scaled vs unscaled coords
        # But here we assume coords are in the 'tile space' which is unscaled (1:10)
        # Wait, if the tile is 1:10, and we draw 1:10 marks, they will be correct.
        # But `self.effective_overlap` is calculated based on input settings.
        # If input is 1:10, self.effective_overlap should be scaled down? 
        # In `calculate_dimensions`: `effective_overlap_adjusted_x = self.effective_overlap / sx`
        # So `self.core_slice_height` already accounts for overlap.
        # We need unscaled overlap in points for drawing calculation if drawing on unscaled canvas.
        
        # Correct logic: We are drawing on a canvas that corresponds to the tile size.
        # If the tile is 1:10 of final size, we want marks to be 1:10 size.
        # So abs_scale = 1/sx does exactly that.
        # However, positions (x_pos, y_pos) are passed in.
        
        # Let's revert v_overlap_pt to use simple conversion, as position logic handles the overlap offset.
        v_overlap_mm = self.effective_overlap # This is the full overlap value from settings
        # On the 1:10 tile, the overlap area is 1:10th of this value?
        # No, `self.effective_overlap` is the physical overlap (e.g. 20mm).
        # On a 1:10 tile, it occupies 2mm.
        # So we must scale it down.
        v_overlap_pt = v_overlap_mm * self.mm * abs_scale
        
        center_bottom_y = y_pos + half_mark_h
        center_top_y = (y_pos + (slice_h - v_overlap_pt) + half_mark_h if row > 0 else y_pos + slice_h - half_mark_h)
        center_left_x = x_pos + half_mark_w
        center_right_x = x_pos + core_w + half_mark_w

        is_first_row, is_last_row = (row == 0), (row == total_rows - 1)
        is_first_col, is_last_col = (col == 0), (col == total_cols - 1)
        
        draw_tl = draw_tr = draw_bl = draw_br = True
        if total_rows == 1 and total_cols == 1:
            draw_tl = draw_br = False
        elif is_first_row:
             draw_tl = not is_first_col
             draw_tr = not is_last_col
        elif is_last_row:
             draw_bl = not is_first_col
             draw_br = not is_last_col

        if draw_tl: self.add_registration_mark(c, center_left_x, center_top_y, sx=sx)
        if draw_tr: self.add_registration_mark(c, center_right_x, center_top_y, sx=sx)
        if draw_bl: self.add_registration_mark(c, center_left_x, center_bottom_y, sx=sx)
        if draw_br: self.add_registration_mark(c, center_right_x, center_bottom_y, sx=sx)

    def draw_single_separation_line(self, c, x, y, length, horizontal=True, sx=1.0):
        c.saveState()
        gs = self.config.settings["graphic_settings"]
        abs_scale = self._get_abs_scale(sx)
        black_lw = gs.get("sep_line_black_width", 0.5) * self.mm * abs_scale
        white_lw = gs.get("sep_line_white_width", 0.3) * self.mm * abs_scale

        # Line length is physical dimension, so scale it down
        line_length = self.sep_line_length * abs_scale

        # Jeśli zdefiniowano długość linii, wymuś ją (centrując)
        if line_length > 0:
            offset = (length - line_length) / 2.0
            if horizontal:
                x += offset
            else:
                y += offset
            length = line_length

        if black_lw > 0:
            c.setStrokeColor(PANTONE_BLACK_C)
            c.setLineWidth(black_lw)
            if horizontal: c.line(x, y, x + length, y)
            else: c.line(x, y, x, y + length)
        if white_lw > 0:
            c.setStrokeColor(white)
            c.setLineWidth(white_lw)
            if horizontal: c.line(x, y, x + length, y)
            else: c.line(x, y, x, y + length)
        c.restoreState()

    def _draw_separation_lines_for_page(self, c, page_w, page_h, total_slices, slice_idx, layout, gap, enable_between, enable_start, enable_end, slice_h_on_page=None, sx=None):
        if slice_h_on_page is None:
            is_horizontal = "horizontal" in layout
            slice_h_on_page = self.slice_width if is_horizontal else self.slice_height
            
        y0 = self.margin_bottom
        x_start, line_len = 0.0, page_w

        if enable_between and total_slices > 1:
            for i in range(1, total_slices):
                y_line = y0 + i * slice_h_on_page + (i * gap) - (gap / 2.0)
                self.draw_single_separation_line(c, x_start, y_line, line_len, horizontal=True, sx=sx)
                self.logger.debug(f"Linia 'between' i={i} na y={y_line/self.mm:.2f} mm")

        if enable_start:
            y_line = page_h - (self.margin_top / 2.0)
            self.draw_single_separation_line(c, x_start, y_line, line_len, horizontal=True, sx=sx)
            self.logger.debug(f"Linia 'start' na środku marginesu y={y_line/self.mm:.2f} mm")

        if enable_end:
            y_line = self.margin_bottom / 2.0
            self.draw_single_separation_line(c, x_start, y_line, line_len, horizontal=True, sx=sx)
            self.logger.debug(f"Linia 'end' na środku marginesu y={y_line/self.mm:.2f} mm")

    def _draw_all_barcodes(self, c, barcode_infos, sx=1.0):
        self.logger.info(LANG["log_drawing_barcodes_count"].format(len(barcode_infos)))
        for info in barcode_infos:
            try:
                self.draw_barcode(c, info['barcode_type'], info['data'], info['x'], info['y'], info['layout'], info['output_type'], sx=sx)
            except Exception as e:
                self.logger.error(f"Error drawing barcode for data '{info.get('data')}': {e}", exc_info=True)
    
    def _draw_trial_text(self, c):
        try:
            w, h = c._pagesize
            c.saveState()
            c.setFillAlpha(0.15); c.setFillColor(black)
            c.setFont("Helvetica-Bold", 72)
            c.translate(w / 2, h / 2); c.rotate(45)
            txt = "TRIAL VERSION"
            c.drawString(-c.stringWidth(txt, "Helvetica-Bold", 72) / 2, -10, txt)
            c.restoreState()
        except Exception as e:
            self.logger.error(LANG["error_drawing_trial_text"].format(error=e))

    # =================================================================================
    # LOGIKA KODÓW KRESKOWYCH
    # =================================================================================
    
    def generate_barcode_data(self, file_path, slice_name):
        try:
            filename = os.path.splitext(os.path.basename(file_path))[0]
            match = re.search(r"(\d+)_(\d{1,3})_", filename)
            if match:
                prefix = f"{match.group(1)}_{match.group(2)}"
                return f"{prefix}_{slice_name}" if slice_name else prefix
            else:
                return filename
        except Exception as e:
            self.logger.exception(f"Błąd w generate_barcode_data: {e}")
            return os.path.splitext(os.path.basename(file_path))[0]
            
    def get_code_settings(self, output_type, layout, barcode_type):
        try:
            is_horizontal = "horizontal" in str(layout).lower()
            layout_key = "horizontal" if is_horizontal else "vertical"
            
            code_root = self.config.settings.get("graphic_settings", {}).get("code_settings", {})
            type_settings = code_root.get(barcode_type, {})
            output_settings = type_settings.get(output_type, {})
            layout_settings = output_settings.get(layout_key)

            if layout_settings is None:
                self.logger.warning(f"Brak ustawień kodu dla {barcode_type}/{output_type}/{layout_key}. Używam 'default'.")
                layout_settings = output_settings.get("default", {})
            
            if not layout_settings:
                raise KeyError("Brak jakichkolwiek ustawień dla kodu.")
                
            return layout_settings.copy()
        except Exception:
            self.logger.error(f"Krytyczny błąd pobierania ustawień kodu, używam sztywno zakodowanych wartości.")
            return {"anchor": "bottom-left", "offset_x": 0.0, "offset_y": 0.0, "rotation": 0.0, "scale": 20, "scale_x": 80, "scale_y": 10}

    def _anchor_to_offset(self, anchor: str, bg_width: float, bg_height: float) -> tuple[float, float]:
        a = (anchor or "").lower().strip()
        if a in ("bottom-right", "right-bottom"): return -bg_width, 0.0
        if a in ("top-left", "left-top"):         return 0.0, -bg_height
        if a in ("top-right", "right-top"):       return -bg_width, -bg_height
        if a == "center":                         return -bg_width/2.0, -bg_height/2.0
        if a == "center-bottom":                  return -bg_width/2.0, 0.0
        if a == "center-top":                     return -bg_width/2.0, -bg_height
        if a == "center-left":                    return 0.0, -bg_height/2.0
        if a == "center-right":                   return -bg_width, -bg_height/2.0
        return 0.0, 0.0
        
    def _prepare_barcode_info(self, slice_info, file_path, x_pos, y_pos, barcode_type, output_type, layout, slice_w, slice_h) -> dict | None:
        try:
            data = self.generate_barcode_data(file_path, slice_info.get('name'))
            if not data: return None

            settings = self.get_code_settings(output_type, layout, barcode_type)
            anchor = settings.get("anchor", "bottom-left").lower()

            ax, ay = {
                "bottom-left": (0, 0), "bottom-right": (slice_w, 0),
                "top-left": (0, slice_h), "top-right": (slice_w, slice_h),
                "center": (slice_w/2, slice_h/2), "center-bottom": (slice_w/2, 0),
                "center-top": (slice_w/2, slice_h), "center-left": (0, slice_h/2),
                "center-right": (slice_w, slice_h/2)
            }.get(anchor, (0, 0))

            x_draw, y_draw = x_pos + ax, y_pos + ay

            return {
                "barcode_type": barcode_type, "data": data,
                "x": x_draw, "y": y_draw, "layout": layout,
                "output_type": output_type, "anchor": anchor
            }
        except Exception as e:
            self.logger.error(f"Błąd przygotowania info kodu: {e}", exc_info=True)
            return None

    def draw_barcode(self, c, code_type, data, x, y, layout, output_type, sx=None):
        try:
            settings = self.get_code_settings(output_type, layout, barcode_type=code_type)
            anchor = settings.get("anchor", "bottom-left")
            
            svg_buffer = barcode_qr.generate_qr(data) if code_type == 'code_qr' else barcode_qr.generate_barcode(data)
            if not svg_buffer:
                self.logger.error(f"Nie udało się wygenerować SVG dla: {data}")
                return

            drawing = svg2rlg(svg_buffer)
            if not (drawing and hasattr(drawing, 'width') and hasattr(drawing, 'height')): return

            # Correction factor for real-world sizes (based on 1:10 input scale)
            abs_scale = self._get_abs_scale(sx)

            bsx, bsy = 1.0, 1.0
            if code_type == 'code_qr':
                target = settings.get('scale', 20.0) * self.mm * abs_scale
                bsx = bsy = target / drawing.width if drawing.width > 0 else 1.0
            else:
                target_w = settings.get('scale_x', 80.0) * self.mm * abs_scale
                target_h = settings.get('scale_y', 10.0) * self.mm * abs_scale
                bsx = target_w / drawing.width if drawing.width > 0 else 1.0
                bsy = target_h / drawing.height if drawing.height > 0 else 1.0
            
            code_w, code_h = drawing.width * bsx, drawing.height * bsy
            bg_w, bg_h = code_w, code_h
            label, code_dx, code_dy = None, 0.0, 0.0

            if code_type == 'code_barcode' and self.config.settings.get("barcode_text_position", "side") == 'side':
                gs = self.config.settings.get("graphic_settings", {})
                font_size = gs.get("barcode_font_size", 1.6) * abs_scale
                gap, pad = 1 * self.mm * abs_scale, 1 * self.mm * abs_scale
                c.setFont("Helvetica", font_size)
                txt_w = c.stringWidth(data)
                bg_w = pad + code_w + gap + txt_w + pad
                bg_h = max(code_h, font_size)
                code_dy = (bg_h - code_h) / 2.0
                label = {"text": data, "x": pad + code_w + gap, "y": (bg_h - font_size) / 2.0, "size": font_size}

            dx_anchor, dy_anchor = self._anchor_to_offset(anchor, bg_w, bg_h)
            off_x = settings.get('offset_x', 0.0) * self.mm * abs_scale
            off_y = settings.get('offset_y', 0.0) * self.mm * abs_scale
            rot = settings.get('rotation', 0.0)

            pad_l = settings.get('bg_pad_left_mm', 0.0) * self.mm * abs_scale
            pad_r = settings.get('bg_pad_right_mm', 0.0) * self.mm * abs_scale
            pad_t = settings.get('bg_pad_top_mm', 0.0) * self.mm * abs_scale
            pad_b = settings.get('bg_pad_bottom_mm', 0.0) * self.mm * abs_scale
            
            c.saveState()
            c.translate(x + off_x + dx_anchor, y + off_y + dy_anchor)
            c.rotate(rot)
            c.setFillColor(white)
            c.rect(-pad_l, -pad_b, bg_w + pad_l + pad_r, bg_h + pad_b + pad_t, stroke=0, fill=1)
            c.translate(code_dx, code_dy); c.scale(bsx, bsy)
            renderPDF.draw(drawing, c, 0, 0)
            
            if label:
                c.scale(1/bsx, 1/bsy); c.translate(-code_dx, -code_dy)
                c.setFont("Helvetica", label["size"]); c.setFillColor(black)
                c.drawString(label["x"], label["y"], label["text"])
            
            c.restoreState()
        except Exception as e:
            self.logger.error(f"Błąd rysowania kodu dla '{data}': {e}", exc_info=True)
            if 'c' in locals() and hasattr(c, 'restoreState'): c.restoreState()
        except Exception as e:
            self.logger.error(f"Błąd rysowania kodu dla '{data}': {e}", exc_info=True)
            if 'c' in locals() and hasattr(c, 'restoreState'): c.restoreState()

    # =================================================================================
    # PODGLĄD
    # =================================================================================
    
    def generate_fast_preview(self, input_pdf_path: str, settings: dict) -> Image.Image | None:
        """[FIXED] Generuje podgląd dla trybu Billboard lub Poster z pełną logiką rysowania."""
        self.logger.debug("Generowanie szybkiego podglądu (PyMuPDF).")
        cache_key = f"{input_pdf_path}_{hash(str(sorted(settings.items())))}"
        if cache_key in self._preview_cache:
            return self._preview_cache[cache_key]
        
        source_doc = None
        try:
            product_mode = settings.get("product_mode", "billboard")
            
            source_doc = fitz.open(input_pdf_path)
            if not source_doc.page_count: return None
            page = source_doc.load_page(0)
            
            MAX_PROXY_DIM = 800.0
            zoom = MAX_PROXY_DIM / max(page.rect.width, page.rect.height)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
            proxy_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            if product_mode == 'poster':
                rotation = int(settings.get("input_rotation_deg", 0))
                repetitions = int(settings.get("repetitions", 1))
                gap_mm = float(settings.get("poster_gap_cm", 0.0))
                add_line_at_start = bool(settings.get("add_line_at_start", False))
                add_line_at_end = bool(settings.get("add_line_at_end", False))
                enable_cut_marks = bool(settings.get("enable_vertical_cut_marks", False))

                self.logger.debug(f"Poster PREVIEW settings: rotation={rotation}, reps={repetitions}, gap={gap_mm}mm, start_line={add_line_at_start}, end_line={add_line_at_end}, cut_marks={enable_cut_marks}")

                effective_rotation = rotation
                if rotation == 90:
                    effective_rotation = 270
                elif rotation == 270:
                    effective_rotation = 90

                if rotation != 0:
                    proxy_image = proxy_image.rotate(effective_rotation, expand=True)

                img_w_px, img_h_px = proxy_image.size
                gap_px = gap_mm * self.mm * zoom
                
                margin_top_px = self.margin_top * zoom
                margin_bottom_px = self.margin_bottom * zoom
                margin_left_px = self.margin_left * zoom
                margin_right_px = self.margin_right * zoom

                canvas_w = int(margin_left_px + margin_right_px + repetitions * img_w_px + (repetitions - 1) * gap_px)
                canvas_h = int(margin_top_px + margin_bottom_px + img_h_px)
                preview_canvas = Image.new("RGB", (canvas_w, canvas_h), (230, 230, 230))

                for i in range(repetitions):
                    dest_x = margin_left_px + i * (img_w_px + gap_px)
                    preview_canvas.paste(proxy_image, (int(dest_x), int(margin_top_px)))
                
                draw = ImageDraw.Draw(preview_canvas)
                line_color = (100, 100, 100)
                
                if add_line_at_start:
                    if margin_top_px > 1:
                        y = margin_top_px / 2
                        draw.line([(0, y), (canvas_w, y)], fill=line_color, width=1)
                if add_line_at_end:
                    if margin_bottom_px > 1:
                        y = canvas_h - (margin_bottom_px / 2)
                        draw.line([(0, y), (canvas_w, y)], fill=line_color, width=1)
                
                if enable_cut_marks:
                    for i in range(repetitions):
                        x = margin_left_px + i * (img_w_px + gap_px)
                        draw.line([(x, 0), (x, canvas_h)], fill=line_color, width=1)
                    
                    last_x = margin_left_px + repetitions * img_w_px + (repetitions - 1) * gap_px
                    draw.line([(last_x, 0), (last_x, canvas_h)], fill=line_color, width=1)

            else: # Tryb Billboard
                rows, cols = int(settings.get("split_rows", 1)), int(settings.get("split_cols", 1))
                layout = settings.get("layout", "layout_vertical")
                
                self.width, self.height = float(page.rect.width), float(page.rect.height)
                self.calculate_dimensions(
                    overlap=float(settings.get("overlap", 0.0)),
                    rows=rows, cols=cols,
                    white_stripe=float(settings.get("white_stripe", 0.0)),
                    add_white_to_overlap=bool(settings.get("add_white_to_overlap", False))
                )
                
                all_slices = [self.get_slice_info(r, c, rows, cols) for r in range(rows) for c in range(cols)]
                
                proxy_scale = proxy_image.width / self.width
                slice_w_px = self.slice_width * proxy_scale
                slice_h_px = self.slice_height * proxy_scale
                gap_px = settings.get("graphic_settings", {}).get("slice_gap", 2.0) * self.mm * proxy_scale
                margin_px = 10
                
                is_horizontal = "horizontal" in layout
                if is_horizontal:
                    canvas_w = int(cols * slice_w_px + (cols - 1) * gap_px + 2 * margin_px)
                    canvas_h = int(rows * slice_h_px + (rows - 1) * gap_px + 2 * margin_px)
                else: 
                    canvas_w = int(cols * slice_w_px + (cols - 1) * gap_px + 2 * margin_px)
                    canvas_h = int(rows * slice_h_px + (rows - 1) * gap_px + 2 * margin_px)

                preview_canvas = Image.new("RGB", (canvas_w, canvas_h), (230, 230, 230))

                for slice_info in all_slices:
                    row, col = slice_info["row"], slice_info["col"]
                    dest_x = margin_px + col * (slice_w_px + gap_px)
                    dest_y = margin_px + row * (slice_h_px + gap_px)

                    src_x = slice_info["offset"][0] * proxy_scale
                    src_y = (self.height - slice_info["offset"][1] - self.slice_height) * proxy_scale
                    
                    slice_img = proxy_image.crop((int(src_x), int(src_y), int(src_x + slice_w_px), int(src_y + slice_h_px)))
                    
                    if is_horizontal:
                        slice_img = slice_img.rotate(90, expand=True)
                    if int(settings.get("slice_rotation", 0)) == 180:
                        slice_img = slice_img.rotate(180)
                    
                    slice_img.thumbnail((int(slice_w_px), int(slice_h_px)), Image.Resampling.LANCZOS)
                    preview_canvas.paste(slice_img, (int(dest_x), int(dest_y)))

            if len(self._preview_cache) > 5: self._preview_cache.pop(next(iter(self._preview_cache)))
            self._preview_cache[cache_key] = preview_canvas
            return preview_canvas
        
        except Exception as e:
            self.logger.error(f"Błąd generowania podglądu: {e}", exc_info=True)
            return None
        finally:
            if source_doc: source_doc.close()