# billboard_splitter/pdf_renderer.py
import io
import logging
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white
from reportlab.lib.utils import ImageReader

import barcode_qr
import config

logger = logging.getLogger('BillboardSplitter')

def create_overlay(slice_info, all_settings):
    """Creates an overlay PDF with registration marks, stripes, etc."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(slice_info['width'], slice_info['height']))
    
    if all_settings.get("draw_slice_border", False):
        draw_full_slice_border(can, slice_info)

    if all_settings.get("add_white_to_overlap", False):
        draw_white_stripes(can, slice_info)

    if all_settings.get("enable_reg_marks"):
        draw_registration_marks(can, slice_info)

    if all_settings.get("enable_barcode"):
        draw_barcode(can, slice_info, all_settings['file_path'], all_settings['barcode_type'], all_settings['layout'], all_settings['output_type'], all_settings)

    can.save()
    packet.seek(0)
    return PdfReader(packet)

def draw_full_slice_border(can, slice_info):
    """Draws a border around the slice."""
    width, height = slice_info['width'], slice_info['height']
    can.setStrokeColor(black)
    can.setLineWidth(0.1 * mm)
    can.rect(0, 0, width, height)

def draw_white_stripes(can, slice_info):
    """Draws white stripes for overlap."""
    white_stripe_cm = config.settings.get("white_stripe", 0.0)
    if not config.settings.get("add_white_to_overlap") or white_stripe_cm <= 0:
        return
        
    ws_pt = white_stripe_cm * mm
    page_w, page_h = slice_info['width'], slice_info['height']
    row, col, total_rows, total_cols = slice_info["row"], slice_info["col"], slice_info["rows"], slice_info["cols"]

    is_last_row = (row == total_rows - 1)
    is_not_last_row = (row < total_rows - 1)
    is_not_last_col = (col < total_cols - 1)

    can.setFillColor(white)
    can.setStrokeColor(black)
    can.setLineWidth(0.1 * mm)

    # y=0 is at the bottom in reportlab
    if is_last_row and is_not_last_col:
        # Right stripe only
        can.rect(page_w - ws_pt, 0, ws_pt, page_h, fill=1, stroke=1)
    elif is_not_last_row:
        if is_not_last_col: # 'L' shape
            # Top stripe
            can.rect(0, 0, page_w, ws_pt, fill=1, stroke=1)
            # Right stripe
            can.rect(page_w - ws_pt, 0, ws_pt, page_h, fill=1, stroke=1)
        else: # Only top stripe
            can.rect(0, 0, page_w, ws_pt, fill=1, stroke=1)


def draw_registration_marks(can, slice_info):
    """Rysuje znaczniki pasowania (krzyżyki) na płótnie ReportLab."""
    gs = config.settings.get("graphic_settings", {})
    mark_width = gs.get("reg_mark_width", 5.0) * mm
    mark_height = gs.get("reg_mark_height", 5.0) * mm
    line_width_white = gs.get("reg_mark_white_line_width", 0.5) * mm
    line_width_black = gs.get("reg_mark_black_line_width", 0.7) * mm
    
    page_h, page_w = slice_info['height'], slice_info['width']
    row, col, total_rows, total_cols = slice_info["row"], slice_info["col"], slice_info["rows"], slice_info["cols"]

    half_mark_w, half_mark_h = mark_width / 2.0, mark_height / 2.0
    
    overlap_cm = config.settings.get("overlap", 0.0)
    white_stripe_cm = config.settings.get("white_stripe", 0.0)
    add_white_to_overlap = config.settings.get("add_white_to_overlap", False)
    effective_overlap = (overlap_cm + white_stripe_cm if add_white_to_overlap else overlap_cm) * mm

    core_slice_height = page_h - effective_overlap
    core_slice_width = page_w - effective_overlap

    # Coordinates are from bottom-left in reportlab
    center_bottom_y = 0
    center_top_y = core_slice_height

    center_left_x = 0
    center_right_x = core_slice_width

    def _draw_mark(x, y):
        can.setStrokeColor(white)
        can.setLineWidth(line_width_white)
        can.line(x - half_mark_w, y, x + half_mark_w, y)
        can.line(x, y - half_mark_h, x, y + half_mark_h)
        can.setStrokeColor(black)
        can.setLineWidth(line_width_black)
        can.line(x - half_mark_w, y, x + half_mark_w, y)
        can.line(x, y - half_mark_h, x, y + half_mark_h)

    # Top-left corner of the slice
    if row > 0 and col > 0:
        _draw_mark(center_left_x, center_top_y)

    # Top-right corner of the slice
    if row > 0 and col < total_cols - 1:
        _draw_mark(center_right_x, center_top_y)

    # Bottom-left corner of the slice
    if row < total_rows - 1 and col > 0:
        _draw_mark(center_left_x, center_bottom_y)

    # Bottom-right corner of the slice
    if row < total_rows - 1 and col < total_cols - 1:
        _draw_mark(center_right_x, center_bottom_y)

def get_code_settings(output_type, layout, barcode_type):
    """Pobiera ustawienia (pozycja, rotacja, skala) dla kodu kreskowego/QR."""
    try:
        settings_key = "separate_files" if output_type == "output_separate_files" else "common_sheet"
        layout_key = "horizontal" if "horizontal" in layout else "vertical"

        code_settings_root = config.settings.get("graphic_settings", {}).get("code_settings", {})
        type_settings = code_settings_root.get(barcode_type, {})
        output_settings = type_settings.get(settings_key, {})
        layout_settings = output_settings.get(layout_key)

        if layout_settings is None:
            layout_settings = output_settings.get("default", {})
        return layout_settings.copy()
    except Exception as e:
        logger.error(f"Błąd pobierania ustawień kodu: {e}", exc_info=True)
        return {}

def draw_barcode(can, slice_info, file_path, barcode_type, layout, output_type, settings):
    """Draws a barcode on the canvas."""
    if not settings.get("enable_barcode"):
        return

    code_settings = get_code_settings(output_type, layout, barcode_type)
    if not code_settings:
        return

    data = f"{os.path.splitext(os.path.basename(file_path))[0]}_{slice_info['name']}"
    
    text_mode = config.settings.get("barcode_text_position", "side")
    show_text_in_barcode = not (barcode_type == 'code_barcode' and text_mode == 'side')

    png_bytes = barcode_qr.generate_barcode_in_memory(barcode_type, data, show_text=show_text_in_barcode)
    if not png_bytes:
        return

    img_reader = ImageReader(io.BytesIO(png_bytes))
    
    page_w, page_h = slice_info['width'], slice_info['height']
    anchor = code_settings.get("anchor", "bottom-left")

    if barcode_type == 'code_qr':
        img_w = img_h = code_settings.get('scale', 20.0) * mm
    else:
        img_w, img_h = code_settings.get('scale_x', 80.0) * mm, code_settings.get('scale_y', 10.0) * mm
    
    off_x, off_y = code_settings.get('offset_x', 0.0) * mm, code_settings.get('offset_y', 0.0) * mm

    x0, y0 = 0, 0
    if "right" in anchor: x0 = page_w - img_w - off_x
    else: x0 = off_x
    if "bottom" in anchor: y0 = off_y
    else: y0 = page_h - img_h - off_y
    if "center" in anchor:
        if "left" not in anchor and "right" not in anchor: x0 = (page_w - img_w) / 2 + off_x
        if "top" not in anchor and "bottom" not in anchor: y0 = (page_h - img_h) / 2 + off_y

    can.drawImage(img_reader, x0, y0, width=img_w, height=img_h)

    if barcode_type == 'code_barcode' and text_mode == 'side':
        text_x = x0 + img_w + 1*mm
        text_y = y0
        
        # White background for the text
        can.setFillColor(white)
        can.rect(text_x - 0.5*mm, text_y - 0.5*mm, len(data) * 3.5, 8, fill=1, stroke=0)

        can.setFillColor(black)
        can.setFont("Helvetica", 6)
        can.drawString(text_x, text_y, data)

def draw_separation_lines(can, page_w, page_h, total_slices, layout, gap, settings):
    """Draws separation lines on the common sheet."""
    if not settings.get("enable_separation_lines") or total_slices <= 1:
        return

    gs = config.settings.get("graphic_settings", {})
    line_width_white = gs.get("sep_line_white_width", 0.3) * mm
    line_width_black = gs.get("sep_line_black_width", 0.5) * mm
    
    margin_top = gs.get("margin_top", 2.0) * mm
    margin_left = gs.get("margin_left", 2.0) * mm
    margin_right = gs.get("margin_right", 2.0) * mm
    margin_bottom = gs.get("margin_bottom", 2.0) * mm

    if "vertical" in layout:
        slice_dim = (page_h - margin_top - margin_bottom - (total_slices - 1) * gap) / total_slices
        x_start, x_end = 0, page_w
        for i in range(1, total_slices):
            y_pos = margin_bottom + i * slice_dim + (i - 1) * gap + gap/2
            can.setStrokeColor(white)
            can.setLineWidth(line_width_black + line_width_white)
            can.line(x_start, y_pos, x_end, y_pos)
            can.setStrokeColor(black)
            can.setLineWidth(line_width_black)
            can.line(x_start, y_pos, x_end, y_pos)
    else: # horizontal
        slice_dim = (page_w - margin_left - margin_right - (total_slices - 1) * gap) / total_slices
        y_start, y_end = 0, page_h
        for i in range(1, total_slices):
            x_pos = margin_left + i * slice_dim + (i - 1) * gap + gap/2
            can.setStrokeColor(white)
            can.setLineWidth(line_width_black + line_width_white)
            can.line(x_pos, y_start, x_pos, y_end)
            can.setStrokeColor(black)
            can.setLineWidth(line_width_black)
            can.line(x_pos, y_start, x_pos, y_end)

def draw_poster_barcodes(can, repetitions, img_w, img_h, gap, margin_left, margin_bottom, file_path, barcode_type, settings):
    """Draws barcodes for each poster repetition."""
    if not settings.get("enable_barcode"):
        return

    for i in range(repetitions):
        poster_slice_info = {
            "name": f"P{i+1}",
            "width": img_w,
            "height": img_h
        }
        
        code_settings = get_code_settings("common_sheet", "horizontal", barcode_type)
        if not code_settings:
            continue

        data = f"{os.path.splitext(os.path.basename(file_path))[0]}_{poster_slice_info['name']}"
        
        text_mode = config.settings.get("barcode_text_position", "side")
        show_text_in_barcode = not (barcode_type == 'code_barcode' and text_mode == 'side')

        png_bytes = barcode_qr.generate_barcode_in_memory(barcode_type, data, show_text=show_text_in_barcode)
        if not png_bytes:
            continue

        img_reader = ImageReader(io.BytesIO(png_bytes))
        
        anchor = code_settings.get("anchor", "bottom-left")

        if barcode_type == 'code_qr':
            bc_img_w = bc_img_h = code_settings.get('scale', 20.0) * mm
        else:
            bc_img_w, bc_img_h = code_settings.get('scale_x', 80.0) * mm, code_settings.get('scale_y', 10.0) * mm
        
        off_x, off_y = code_settings.get('offset_x', 0.0) * mm, code_settings.get('offset_y', 0.0) * mm

        x_pos = margin_left + i * (img_w + gap)
        y_pos = margin_bottom

        x0, y0 = 0, 0
        if "right" in anchor: x0 = x_pos + img_w - bc_img_w - off_x
        else: x0 = x_pos + off_x
        if "bottom" in anchor: y0 = y_pos + off_y
        else: y0 = y_pos + img_h - bc_img_h - off_y
        if "center" in anchor:
            if "left" not in anchor and "right" not in anchor: x0 = x_pos + (img_w - bc_img_w) / 2 + off_x
            if "top" not in anchor and "bottom" not in anchor: y0 = y_pos + (img_h - bc_img_h) / 2 + off_y

        can.drawImage(img_reader, x0, y0, width=bc_img_w, height=bc_img_h)

        if barcode_type == 'code_barcode' and text_mode == 'side':
            text_x = x0 + bc_img_w + 1*mm
            text_y = y0
            
            can.setFillColor(white)
            can.rect(text_x - 0.5*mm, text_y - 0.5*mm, len(data) * 3.5, 8, fill=1, stroke=0)

            can.setFillColor(black)
            can.setFont("Helvetica", 6)
            can.drawString(text_x, text_y, data)

def draw_poster_separation_lines(can, repetitions, img_w, img_h, gap, margin_left, margin_bottom):
    """Draws separation lines between posters."""
    if repetitions <= 1:
        return
    
    gs = config.settings.get("graphic_settings", {})
    line_width_white = gs.get("sep_line_white_width", 0.3) * mm
    line_width_black = gs.get("sep_line_black_width", 0.5) * mm

    for i in range(1, repetitions):
        x_center = margin_left + (i * img_w) + (i - 0.5) * gap
        y_start = margin_bottom
        y_end = margin_bottom + img_h
        
        can.setStrokeColor(white)
        can.setLineWidth(line_width_black + line_width_white)
        can.line(x_center, y_start, x_center, y_end)
        
        can.setStrokeColor(black)
        can.setLineWidth(line_width_black)
        can.line(x_center, y_start, x_center, y_end)

def draw_poster_vertical_cut_marks(can, page_w, page_h):
    """Draws vertical cut marks on the sides of the sheet."""
    gs = config.settings.get("graphic_settings", {})
    line_width_white = gs.get("reg_mark_white_line_width", 0.5) * mm
    line_width_black = gs.get("reg_mark_black_line_width", 0.7) * mm
    line_len = 5 * mm

    # Left side
    y_center = page_h / 2
    can.setStrokeColor(white)
    can.setLineWidth(line_width_black + line_width_white)
    can.line(0, y_center, line_len, y_center)
    can.setStrokeColor(black)
    can.setLineWidth(line_width_black)
    can.line(0, y_center, line_len, y_center)

    # Right side
    can.setStrokeColor(white)
    can.setLineWidth(line_width_black + line_width_white)
    can.line(page_w - line_len, y_center, page_w, y_center)
    can.setStrokeColor(black)
    can.setLineWidth(line_width_black)
    can.line(page_w - line_len, y_center, page_w, y_center)

def draw_trial_watermark(page):
    """Adds a trial watermark to the page."""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(page.mediabox.width, page.mediabox.height))
    can.setFont("Helvetica", 50)
    can.setFillColor(black, alpha=0.15)
    can.saveState()
    can.translate(float(page.mediabox.width)/2, float(page.mediabox.height)/2)
    can.rotate(45)
    can.drawCentredString(0, 0, "TRIAL VERSION")
    can.restoreState()
    can.save()
    packet.seek(0)
    watermark_pdf = PdfReader(packet)
    page.merge_page(watermark_pdf.pages[0])


def save_pdf(pdf_writer, path):
    """Saves a PdfWriter object to a file."""
    with open(path, "wb") as f:
        pdf_writer.write(f)
    logger.info(f"Saved PDF: {path}")