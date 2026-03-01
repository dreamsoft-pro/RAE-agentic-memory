import sys
import json
import os
import shutil
import logging
import traceback
import requests
import re
from logging.handlers import RotatingFileHandler
from mss import mss
from PIL import Image, ImageOps
import pytesseract

# --- Tesseract Auto-Installation Logic ---
def ensure_tesseract():
    app_dir = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    target_bin_dir = os.path.join(app_dir, "bin", "tesseract")
    target_exe = os.path.join(target_bin_dir, "tesseract.exe")
    if not os.path.exists(target_exe):
        if getattr(sys, 'frozen', False):
            internal_tess_dir = os.path.join(sys._MEIPASS, "tesseract_bin")
            if os.path.exists(internal_tess_dir):
                try:
                    os.makedirs(os.path.dirname(target_bin_dir), exist_ok=True)
                    if os.path.exists(target_bin_dir): shutil.rmtree(target_bin_dir)
                    shutil.copytree(internal_tess_dir, target_bin_dir)
                except: pass
        else:
            std_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(std_path): return std_path
    return target_exe if os.path.exists(target_exe) else "tesseract"

pytesseract.pytesseract.tesseract_cmd = ensure_tesseract()

class ROI:
    def __init__(self, x, y, w, h, name="Nowy Obszar", data_type="text", transformations=None, 
                 metric_key="", unit="", category="General"):
        self.rect = QRect(x, y, w, h)
        self.name, self.data_type = name, data_type 
        self.transformations = transformations or []
        self.metric_key = metric_key or name.lower().replace(" ", "_")
        self.unit, self.category = unit, category

    def to_dict(self):
        return {
            "name": self.name, "type": self.data_type, "x": self.rect.x(), "y": self.rect.y(),
            "w": self.rect.width(), "h": self.rect.height(), "transformations": self.transformations,
            "metric_key": self.metric_key, "unit": self.unit, "category": self.category
        }

    @staticmethod
    def from_dict(data):
        return ROI(data["x"], data["y"], data["w"], data["h"], data["name"], data.get("type", "text"),
                   data.get("transformations", []), data.get("metric_key", ""), data.get("unit", ""), data.get("category", "General"))

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rois, self.current_start, self.current_end = [], None, None
        self.selected_roi_index, self.drawing = -1, False
        self.setMouseTracking(True)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap(): return
        painter = QPainter(self)
        for i, roi in enumerate(self.rois):
            painter.setPen(QPen(QColor(0, 255, 0) if i == self.selected_roi_index else QColor(255, 0, 0), 2))
            painter.drawRect(roi.rect)
            painter.fillRect(roi.rect.x(), roi.rect.y() - 20, len(roi.name) * 10 + 10, 20, QColor(0, 0, 0, 180))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(roi.rect.x() + 5, roi.rect.y() - 5, roi.name)
        if self.current_start and self.current_end:
            painter.setPen(QPen(QColor(0, 0, 255), 2, Qt.PenStyle.DashLine))
            painter.drawRect(QRect(self.current_start, self.current_end).normalized())

    def mousePressEvent(self, event):
        if not self.pixmap(): return
        for i, roi in enumerate(reversed(self.rois)):
            if roi.rect.contains(event.pos()):
                self.selected_roi_index = len(self.rois) - 1 - i
                self.window().roi_selected(self.selected_roi_index)
                self.update(); return
        self.drawing, self.current_start, self.current_end, self.selected_roi_index = True, event.pos(), event.pos(), -1
        self.window().roi_selected(-1)

    def mouseMoveEvent(self, event):
        if self.drawing: self.current_end = event.pos(); self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False
            rect = QRect(self.current_start, event.pos()).normalized()
            if rect.width() > 5 and rect.height() > 5:
                new_roi = ROI(rect.x(), rect.y(), rect.width(), rect.height(), f"Pole_{len(self.rois)+1}")
                self.rois.append(new_roi); self.selected_roi_index = len(self.rois) - 1
                self.window().roi_created(new_roi)
            self.current_start = self.current_end = None; self.update()

class ConfiguratorWindow(QMainWindow):
    INDUSTRIAL_UNITS = ["", "pcs", "kg", "t", "m", "m2", "m3", "°C", "bar", "m/min", "kW", "kWh", "%", "s", "min", "h"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScreenWatcher Configurator v2.2")
        self.resize(1400, 900); self.init_ui()

    def init_ui(self):
        central = QWidget(); self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        splitter = QSplitter(Qt.Orientation.Horizontal); main_layout.addWidget(splitter)
        
        self.image_label = ImageLabel()
        self.image_scroll = QScrollArea(); self.image_scroll.setWidget(self.image_label)
        self.image_scroll.setWidgetResizable(False); splitter.addWidget(self.image_scroll)
        
        controls_scroll = QScrollArea(); controls_scroll.setWidgetResizable(True); controls_scroll.setMaximumWidth(500)
        controls_container = QWidget(); controls_layout = QVBoxLayout(controls_container); controls_scroll.setWidget(controls_container)
        splitter.addWidget(controls_scroll)
        
        # 1. Settings
        group1 = QGroupBox("1. Konfiguracja Połączenia"); form = QFormLayout()
        self.input_mcode = QLineEdit("M01"); self.input_api_url = QLineEdit("http://localhost:9000/api/collector/ingest/")
        self.input_token = QLineEdit(); self.input_token.setPlaceholderText("Wklej Klucz API (Token) z Admina")
        self.input_interval = QSpinBox(); self.input_interval.setRange(1, 3600); self.input_interval.setValue(10)
        self.combo_monitor = QComboBox(); self.refresh_monitors()
        self.combo_log = QComboBox(); self.combo_log.addItems(["DEBUG", "INFO", "WARNING", "ERROR"]); self.combo_log.setCurrentText("INFO")
        self.check_offline = QCheckBox("TRYB OFFLINE (Zapis na Pendrive)"); self.check_offline.setStyleSheet("font-weight: bold; color: red;")
        
        form.addRow("Kod Maszyny:", self.input_mcode); form.addRow("Klucz API (Token):", self.input_token)
        form.addRow("URL Ingestora:", self.input_api_url); form.addRow("Interwał (s):", self.input_interval)
        form.addRow("Wybierz Ekran:", self.combo_monitor); form.addRow("Poziom Logów:", self.combo_log); form.addRow("Tryb Pracy:", self.check_offline)
        group1.setLayout(form); controls_layout.addWidget(group1)

        # 2. Tools
        group2 = QGroupBox("2. Przechwytywanie i OCR"); layout2 = QVBoxLayout()
        btns = QHBoxLayout(); self.btn_cap = QPushButton("Capture Live"); self.btn_cap.clicked.connect(self.capture_screen)
        self.btn_file = QPushButton("Wczytaj z pliku"); self.btn_file.clicked.connect(self.load_image)
        btns.addWidget(self.btn_cap); btns.addWidget(self.btn_file); layout2.addLayout(btns)
        self.btn_ocr = QPushButton("Sprawdź silnik OCR"); self.btn_ocr.clicked.connect(self.check_ocr)
        
        btn_layout = QHBoxLayout()
        self.btn_load = QPushButton("WCZYTAJ KONFIG"); self.btn_load.clicked.connect(self.load_config)
        self.btn_save = QPushButton("ZAPISZ KONFIG"); self.btn_save.clicked.connect(self.save_config)
        self.btn_save.setStyleSheet("background-color: #4caf50; color: white; font-weight: bold; padding: 10px;")
        self.btn_load.setStyleSheet("background-color: #ff9800; color: white; font-weight: bold; padding: 10px;")
        btn_layout.addWidget(self.btn_load); btn_layout.addWidget(self.btn_save)
        
        layout2.addWidget(self.btn_ocr); layout2.addLayout(btn_layout); group2.setLayout(layout2); controls_layout.addWidget(group2)

        # 3. ROIs
        self.roi_list = QListWidget(); self.roi_list.setMaximumHeight(150); self.roi_list.currentRowChanged.connect(self.list_selection_changed)
        controls_layout.addWidget(QLabel("Zdefiniowane pola (ROIs):")); controls_layout.addWidget(self.roi_list)

        # 4. ROI Props
        group3 = QGroupBox("3. Właściwości Pola"); form3 = QFormLayout()
        self.in_name, self.in_key = QLineEdit(), QLineEdit()
        self.cb_type = QComboBox(); self.cb_type.addItems(["text", "number", "status", "table"])
        self.cb_unit = QComboBox(); self.cb_unit.addItems(self.INDUSTRIAL_UNITS)
        self.in_cat = QLineEdit("General"); self.in_trans = QTextEdit(); self.in_trans.setMaximumHeight(80)
        for w in [self.in_name, self.in_key, self.cb_type, self.cb_unit, self.in_cat, self.in_trans]:
            if isinstance(w, QComboBox): w.currentTextChanged.connect(self.update_roi_data)
            else: w.textChanged.connect(self.update_roi_data)
        form3.addRow("Nazwa:", self.in_name); form3.addRow("Klucz Metryki (Kod):", self.in_key)
        form3.addRow("Typ:", self.cb_type); form3.addRow("Jednostka:", self.cb_unit)
        form3.addRow("Kategoria:", self.in_cat); form3.addRow("Transformacje:", self.in_trans)
        
        self.btn_test_roi = QPushButton("Testuj odczyt (OCR)"); self.btn_test_roi.clicked.connect(self.test_roi_ocr)
        self.btn_test_roi.setStyleSheet("background-color: #2196f3; color: white; font-weight: bold;")
        form3.addRow(self.btn_test_roi)
        
        btn_del = QPushButton("Usuń zaznaczone pole"); btn_del.clicked.connect(self.delete_roi); form3.addRow(btn_del)
        group3.setLayout(form3); controls_layout.addWidget(group3); controls_layout.addStretch(); splitter.setSizes([900, 500])

    def test_roi_ocr(self):
        row = self.roi_list.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Błąd", "Najpierw zaznacz pole na liście.")
            return
        
        if not self.image_label.pixmap():
            QMessageBox.warning(self, "Błąd", "Brak obrazu do analizy. Użyj 'Capture' lub 'Wczytaj'.")
            return

        try:
            roi = self.image_label.rois[row]
            # Convert QPixmap to PIL Image
            qimg = self.image_label.pixmap().toImage()
            ptr = qimg.bits()
            ptr.setsize(qimg.sizeInBytes())
            img = Image.frombuffer("RGBA", (qimg.width(), qimg.height()), ptr, "raw", "BGRA", 0, 1)
            img = img.convert("RGB")
            
            # Crop to ROI
            crop = img.crop((roi.rect.x(), roi.rect.y(), roi.rect.x() + roi.rect.width(), roi.rect.y() + roi.rect.height()))
            
            # Apply transformations for testing
            text_to_show = ""
            for ts in roi.transformations:
                if ts.get("type") == "invert":
                    crop = ImageOps.invert(crop)
                    text_to_show += "[Inverted] "

            # Run OCR
            text = pytesseract.image_to_string(crop).strip()
            QMessageBox.information(self, "Wynik OCR", f"Program odczytał:\n\n{text_to_show}'{text}'")
        except Exception as e:
            QMessageBox.critical(self, "Błąd OCR", f"Nie udało się odczytać tekstu:\n{e}")

    def refresh_monitors(self):
        self.combo_monitor.clear()
        try:
            with mss() as sct:
                for i, m in enumerate(sct.monitors):
                    if i == 0: continue # Skip the virtual 'all monitors' screen
                    label = f"Ekran {i}: {m['width']}x{m['height']} {'(Główny)' if i==1 else ''}"
                    self.combo_monitor.addItem(label, i)
        except: self.combo_monitor.addItem("Nie wykryto monitorów", 1)

    def capture_screen(self):
        try:
            with mss() as sct:
                idx = self.combo_monitor.currentData() or 1
                if idx >= len(sct.monitors): idx = 1
                img = Image.frombytes("RGB", sct.monitors[idx]["width"], sct.monitors[idx]["height"], sct.grab(sct.monitors[idx]).rgb)
                self.display_image(img)
        except Exception as e: QMessageBox.critical(self, "Błąd", str(e))

    def load_image(self):
        f, _ = QFileDialog.getOpenFileName(self, "Otwórz obraz", "", "Images (*.png *.jpg *.bmp)")
        if f: self.display_image(Image.open(f))

    def display_image(self, pil_img):
        from PIL.ImageQt import ImageQt
        self.image_label.setPixmap(QPixmap.fromImage(ImageQt(pil_img)))
        self.image_label.setFixedSize(self.image_label.pixmap().size())

    def check_ocr(self):
        try:
            ver = pytesseract.get_tesseract_version()
            QMessageBox.information(self, "OCR OK", f"Silnik gotowy!\nWersja: {ver}\nŚcieżka: {pytesseract.pytesseract.tesseract_cmd}")
        except Exception as e: QMessageBox.critical(self, "Błąd OCR", str(e))

    def test_connection(self):
        try:
            r = requests.options(self.input_api_url.text(), timeout=3)
            QMessageBox.information(self, "Połączenie", f"Backend dostępny! Status: {r.status_code}")
        except Exception as e: QMessageBox.critical(self, "Błąd", str(e))

    def roi_created(self, roi):
        self.roi_list.addItem(f"{roi.name} [{roi.metric_key}]"); self.roi_list.setCurrentRow(len(self.image_label.rois) - 1)

    def roi_selected(self, index):
        widgets = [self.in_name, self.in_key, self.cb_type, self.cb_unit, self.in_cat, self.in_trans]
        for w in widgets: w.blockSignals(True)
        if index >= 0:
            roi = self.image_label.rois[index]
            self.in_name.setText(roi.name); self.in_key.setText(roi.metric_key)
            self.cb_type.setCurrentText(roi.data_type)
            if roi.unit in self.INDUSTRIAL_UNITS: self.cb_unit.setCurrentText(roi.unit)
            self.in_cat.setText(roi.category); self.in_trans.setText(json.dumps(roi.transformations, indent=2))
        else:
            for w in [self.in_name, self.in_key, self.in_cat, self.in_trans]: w.clear()
            self.cb_unit.setCurrentIndex(0)
        for w in widgets: w.blockSignals(False)

    def list_selection_changed(self, row):
        if row >= 0: self.image_label.selected_roi_index = row; self.image_label.update(); self.roi_selected(row)

    def update_roi_data(self):
        row = self.roi_list.currentRow()
        if row >= 0:
            roi = self.image_label.rois[row]; roi.name, roi.metric_key = self.in_name.text(), self.in_key.text()
            roi.data_type, roi.unit, roi.category = self.cb_type.currentText(), self.cb_unit.currentText(), self.in_cat.text()
            try: roi.transformations = json.loads(self.in_trans.toPlainText() or "[]")
            except: pass
            self.roi_list.item(row).setText(f"{roi.name} [{roi.metric_key}]"); self.image_label.update()

    def delete_roi(self):
        row = self.roi_list.currentRow()
        if row >= 0: self.image_label.rois.pop(row); self.roi_list.takeItem(row); self.image_label.selected_roi_index = -1; self.image_label.update()

    def save_config(self):
        f, _ = QFileDialog.getSaveFileName(self, "Zapisz", "config.json", "JSON Files (*.json)")
        if f:
            data = {
                "machine_code": self.input_mcode.text(), "api_url": self.input_api_url.text(),
                "api_token": self.input_token.text(), "interval_sec": self.input_interval.value(),
                "monitor_index": self.combo_monitor.currentData() or 1, 
                "log_level": self.combo_log.currentText(),
                "offline_mode": self.check_offline.isChecked(),
                "rois": [r.to_dict() for r in self.image_label.rois]
            }
            with open(f, 'w') as out: json.dump(data, out, indent=4)
            QMessageBox.information(self, "Sukces", "Zapisano pomyślnie.")

    def load_config(self):
        f, _ = QFileDialog.getOpenFileName(self, "Otwórz", "", "JSON Files (*.json)")
        if f:
            with open(f, 'r') as inp: data = json.load(inp)
            self.input_mcode.setText(data.get("machine_code", "DEFAULT")); self.input_api_url.setText(data.get("api_url", ""))
            self.input_token.setText(data.get("api_token", "")); self.input_interval.setValue(data.get("interval_sec", 10))
            self.combo_log.setCurrentText(data.get("log_level", "INFO"))
            self.check_offline.setChecked(data.get("offline_mode", False))
            self.image_label.rois = [ROI.from_dict(r) for r in data.get("rois", [])]
            self.roi_list.clear()
            for roi in self.image_label.rois: self.roi_list.addItem(f"{roi.name} [{roi.metric_key}]")
            self.image_label.update()

if __name__ == "__main__":
    if sys.platform == 'win32': QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv); app.setStyle("Fusion"); window = ConfiguratorWindow(); window.show(); sys.exit(app.exec())
