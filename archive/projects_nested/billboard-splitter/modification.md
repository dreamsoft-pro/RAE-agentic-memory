modification.md
# MODIFICATION — Agentic Design Pattern Plan (3+1 steps)

We will apply **Prompt-Chaining + Tool-Use + Reflection** patterns (from “Agentic Design Patterns”) to deliver features safely and iteratively. reference: book summary provided by user :contentReference[oaicite:8]{index=8}

---

## Step 1 — Input Rasterization (Settings + Pipeline)

### 1.1 Data model (settings)
Extend `config.default_settings` with a new group:
```python
"rasterization": {
  "enabled": False,
  "dpi": 300,
  "compression": "LZW"  # ["NONE","LZW"]
}


Ensure load_settings()/save_settings() persist these keys (they already merge JSON into defaults). 

wszystkie-pliki-billboard_cieci…

1.2 UI (Settings tab)

Add a new frame above “Logging settings” section:

Checkbox: Enable rasterization

Number input: DPI (int, min 72, default 300)

Select: Compression: None / LZW
Add localized strings in lang_pl.py/lang_en.py (consistent with existing key style like processing_mode_*, logging_*). 

wszystkie-pliki-billboard_cieci…

PL strings (propozycja):

"section_raster": " Rasteryzacja wejścia ",
"raster_enable": "Włącz rasteryzację wejścia",
"raster_dpi": "Rozdzielczość (DPI):",
"raster_compression": "Kompresja:",
"raster_compression_none": "brak",
"raster_compression_lzw": "LZW (bezstratna)"


EN strings:

"section_raster": " Input rasterization ",
"raster_enable": "Enable input rasterization",
"raster_dpi": "Resolution (DPI):",
"raster_compression": "Compression:",
"raster_compression_none": "none",
"raster_compression_lzw": "LZW (lossless)"

1.3 Core

Create services/rasterize.py:

If settings["rasterization"]["enabled"]:

For PDF: render to image at given DPI using the preferred library in project (PyMuPDF recommended in your environment; fallback to poppler if already wired). Keep original colorspace (no color conversion). Export PNG/TIFF:

If compression=="LZW" → TIFF LZW

Else tiff uncompressed

For bitmap inputs: if already a bitmap, do nothing (optionally re-save with target compression only).

Return path/bytes of the new bitmap to be fed to existing splitter pipeline exactly as standard inputs (no special branches later).

Non-functional constraints

One rasterization per input; reuse the same raster for preview and processing to avoid CPU spikes.

Clean temp files in output/temp or OS temp dir.

1.4 Acceptance tests

Toggle on/off → output files equal layout; only file type differs.

Visual parity: no hue shift ΔE noticeable (no color space change).

Commit
feat(raster): add input rasterization settings + pipeline (DPI & LZW)

Step 2 — Product Type Switch (Billboard | Poster)
2.1 Data model

Extend settings:

"product_type": "billboard",  # ["billboard","poster"]
"poster": {
  "repetitions": 1,        # 1..10
  "outer_margin_cm": 0.0,  # like bryty margins
  "enable_sep_lines": False,
  "input_rotation_deg": 0,
  "enable_vertical_cut_marks": False,
  "poster_gap_cm": 0.0     # spacing between posters
}

2.2 UI (Home tab)

Add two buttons/toggle above “Ustawienia podziału”:

Billboard (keeps current sections from “Ustawienia podziału” to “Obrót brytów”)

Poster (shows a new sub-frame with poster fields):

Ilość powtórzeń (1–10, stepper)

Margines zewnętrzny [mm]

Linie separacyjne (checkbox; reuse drawing routine used for “separate files” lines) 

wszystkie-pliki-billboard_cieci…

Obrót pliku wejściowego (°)

Pionowe znaczniki cięcia (checkbox)

Odsunięcie posterów [mm] (analog to slice_gap) 

wszystkie-pliki-billboard_cieci…

Add EN/PL strings aligned to existing naming in lang_*.

2.3 Engine

When product_type=="poster":

Bypass bryt slicing; instead:

Apply optional input rotation.

Add outer margin to canvas.

Tile the same poster repetitions times on a sheet/grid using poster_gap_cm as spacing.

If enable_sep_lines: draw separation lines between posters (reuse current drawing functions used for separation lines and registration coloring rules). Keys for line widths already exist in graphic_settings (sep_line_*). 

wszystkie-pliki-billboard_cieci…

If enable_vertical_cut_marks: draw two long composite lines along left/right edges from top to bottom; implement “white under, black over” strokes using existing config widths (reg_mark_white_line_width, reg_mark_black_line_width) to keep visual style coherent. 

wszystkie-pliki-billboard_cieci…

Commit
feat(poster): add product switch with poster layout, margins, lines and vertical cut marks

Step 3 — Real Input Size Next to Preview
3.1 UI

In the Input file preview frame add a small, read-only label:

Rozmiar pliku: <Szerokość> × <Wysokość> cm

3.2 Logic

PDF: read page size from the file metadata; convert to cm and display (respect page rotation).

Bitmap:

If DPI present → use it.

Else assume 300 DPI (as requested) to compute cm = pixels / dpi * 2.54, and display with a ~ prefix to indicate assumption (optional).

Cache the value per loaded file to avoid repeated I/O.

Commit
feat(preview): show real input size (PDF metadata or bitmap@300dpi)

Step 4 — Vendor Print Spec (Placeholder)
4.1 Settings hook

Add empty structure:

"vendor_preset": {
  "enabled": False,
  "name": "",
  "params": {}
}


UI: disabled combobox “Specyfikacja producenta (wkrótce)”.

Core: no-op if disabled.

Commit
chore(spec-hook): add vendor preset placeholders in settings and UI

Strings (examples)

Update lang_pl.py and lang_en.py with keys outlined above, consistent with existing style (e.g., label_*, section_*, button_*) visible in the language files (tabs, sections, labels). 

wszystkie-pliki-billboard_cieci…

Risk & Mitigation

Color shifts during rasterization → enforce no colorspace conversion.

Performance → single raster pass; reuse for preview/output.

Regression in billboard flow → isolate poster path behind product_type.

Validation Checklist

Load sample → toggle raster on/off → compare outputs.

Switch Billboard/Poster → confirm fields show/hide correctly; generate outputs.

Verify size label for: PDF A4, PNG w/ DPI, JPG without DPI (assumed 300).

Logs contain no new errors; profiling unchanged (see benchmark.py for reference shape).