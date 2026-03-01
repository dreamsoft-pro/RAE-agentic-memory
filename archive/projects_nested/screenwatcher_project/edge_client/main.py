import sys
import time
import json
import os
import shutil
import requests
import re
import logging
import traceback
from logging.handlers import RotatingFileHandler
from datetime import datetime
from mss import mss
from PIL import Image, ImageOps
import pytesseract

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QInputDialog, 
    QMessageBox, QFrame, QStatusBar, QTextEdit, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QCoreApplication
from PyQt6.QtGui import QFont, QIcon, QGuiApplication

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

# Setup professional logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
log_file = 'agent.log'
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def excepthook(exc_type, exc_value, exc_traceback):
    logging.critical("Uncaught exception in Agent", exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = excepthook

CONFIG_FILE = "config.json"

class AgentThread(QThread):
    telemetry_sent = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.running = True

    def run(self):
        logging.info("Agent thread started")
        while self.running:
            try:
                start_time = time.time()
                data = self.agent.capture_and_send()
                if data:
                    self.telemetry_sent.emit(data)
                
                elapsed = time.time() - start_time
                wait_time = max(0.1, self.agent.config.get("interval_sec", 10) - elapsed)
                
                for _ in range(int(wait_time * 10)):
                    if not self.running: break
                    time.sleep(0.1)
                    
            except Exception as e:
                logging.error(f"Error in agent loop: {str(e)}")
                self.error_occurred.emit(str(e))
                time.sleep(5)
        logging.info("Agent thread stopped")

    def stop(self):
        self.running = False

class ScreenWatcherAgent:
    def __init__(self, config_path=CONFIG_FILE):
        self.config_path = config_path
        self.config = self.load_config()
        self.status = "STOPPED"
        self.reason = ""
        
        # Apply log level from config
        log_level_str = self.config.get("log_level", "INFO").upper()
        level = getattr(logging, log_level_str, logging.INFO)
        logging.getLogger().setLevel(level)

    def load_config(self):
        if not os.path.exists(self.config_path):
            default_conf = {
                "machine_code": "DEFAULT",
                "api_url": "http://localhost:9000/api/collector/ingest/",
                "api_token": "",
                "interval_sec": 10,
                "monitor_index": 1,
                "offline_mode": False,
                "log_level": "INFO",
                "rois": []
            }
            with open(self.config_path, 'w') as f: json.dump(default_conf, f, indent=4)
            return default_conf
        try:
            with open(self.config_path, 'r') as f: return json.load(f)
        except Exception as e:
            logging.error(f"Failed to load config: {e}")
            return {}

    def process_roi(self, img, roi):
        try:
            x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]
            roi_img = img.crop((x, y, x + w, y + h))
            text = pytesseract.image_to_string(roi_img).strip()
            
            if roi.get("type") == "table":
                rows = [r.strip() for r in text.split('\n') if r.strip()]
                value = []
                for row in rows:
                    cols = [c.strip() for c in re.split(r'\s{2,}', row) if c.strip()]
                    if cols: value.append(cols)
            else:
                value = text
            
            for ts in roi.get("transformations", []):
                try:
                    t_type = ts.get("type")
                    if t_type == "regex":
                        match = re.search(ts.get("pattern"), value)
                        value = match.group(0) if match else value
                    elif t_type == "replace":
                        value = re.sub(ts.get("old"), ts.get("new"), value)
                    elif t_type == "map":
                        value = ts.get("values", {}).get(value, value)
                    elif t_type == "round" and roi.get("type") == "number":
                        value = round(float(value.replace(',', '.')), ts.get("precision", 2))
                except: pass

            if roi.get("type") == "number" and isinstance(value, str):
                try: value = float(value.replace(',', '.').replace(' ', ''))
                except: pass
            return value
        except Exception as e:
            logging.error(f"ROI error {roi.get('name')}: {e}")
            return None

    def capture_and_send(self):
        try:
            with mss() as sct:
                monitor_idx = self.config.get("monitor_index", 1)
                if monitor_idx >= len(sct.monitors): monitor_idx = 1
                sct_img = sct.grab(sct.monitors[monitor_idx])
                img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

            metrics, metadata = {}, {}
            for roi in self.config.get("rois", []):
                m_key = roi.get("metric_key") or roi["name"].lower().replace(" ", "_")
                metrics[m_key] = self.process_roi(img, roi)
                metadata[m_key] = {
                    "name": roi["name"], "unit": roi.get("unit", ""),
                    "type": roi.get("type", "text"), "category": roi.get("category", "General")
                }
            
            metrics["status"] = self.status
            if self.reason: metrics["reason_code"] = self.reason

            payload = {
                "machine_code": self.config.get("machine_code", "UNKNOWN"),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "metrics": metrics,
                "metadata": metadata
            }
            
            if self.config.get("offline_mode", False):
                with open("offline_data.jsonl", "a") as f: f.write(json.dumps(payload) + "\n")
                return {"status": "saved_locally"}
            else:
                headers = {}
                if self.config.get("api_token"): headers["Authorization"] = f"Token {self.config['api_token']}"
                requests.post(self.config["api_url"], json=payload, headers=headers, timeout=5).raise_for_status()
                return payload
        except Exception as e:
            logging.error(f"Capture error: {str(e)}")
            raise e

class OperatorPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agent = ScreenWatcherAgent()
        self.init_ui()
        self.thread = AgentThread(self.agent)
        self.thread.telemetry_sent.connect(self.on_telemetry_sent)
        self.thread.error_occurred.connect(self.on_error)
        self.thread.start()

    def init_ui(self):
        self.setWindowTitle(f"SW Agent - {self.agent.config.get('machine_code')}")
        self.setMinimumSize(450, 550)
        central = QWidget(); self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QFrame(); header.setFrameShape(QFrame.Shape.StyledPanel)
        h_layout = QHBoxLayout(header)
        self.lbl_machine = QLabel(f"MACHINE: {self.agent.config.get('machine_code')}")
        self.lbl_machine.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.lbl_status = QLabel("STOPPED"); self.lbl_status.setStyleSheet("color: red; font-weight: bold;")
        h_layout.addWidget(self.lbl_machine); h_layout.addStretch(); h_layout.addWidget(self.lbl_status)
        layout.addWidget(header)

        btn_layout = QVBoxLayout()
        self.btn_start = QPushButton("START PRODUCTION"); self.btn_start.setMinimumHeight(60); self.btn_start.setStyleSheet("background-color: #1b5e20; color: white; font-weight: bold; font-size: 14px; border-radius: 5px;")
        self.btn_start.clicked.connect(self.start_prod)
        
        self.btn_pause = QPushButton("PAUSE / DOWNTIME"); self.btn_pause.setMinimumHeight(60); self.btn_pause.setStyleSheet("background-color: #e65100; color: white; font-weight: bold; font-size: 14px; border-radius: 5px;")
        self.btn_pause.clicked.connect(self.pause_prod)

        self.btn_sync = QPushButton("SYNC OFFLINE DATA (USB)"); self.btn_sync.setStyleSheet("background-color: #455a64; color: white; font-weight: bold;")
        self.btn_sync.clicked.connect(self.sync_offline_data)
        
        btn_layout.addWidget(self.btn_start); btn_layout.addWidget(self.btn_pause); btn_layout.addWidget(self.btn_sync)
        layout.addLayout(btn_layout)

        self.log_output = QTextEdit(); self.log_output.setReadOnly(True); self.log_output.setFont(QFont("Consolas", 9))
        layout.addWidget(QLabel("Logs:")); layout.addWidget(self.log_output)

    def sync_offline_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Offline Data", "", "JSONL Files (*.jsonl)")
        if not file_path: return
        self.log_output.append("Starting sync...")
        try:
            with open(file_path, "r") as f: lines = f.readlines()
            for i, line in enumerate(lines):
                headers = {}
                if self.agent.config.get("api_token"): headers["Authorization"] = f"Token {self.agent.config['api_token']}"
                requests.post(self.agent.config["api_url"], json=json.loads(line), headers=headers, timeout=5)
                if i % 5 == 0:
                    self.log_output.append(f"Synced {i+1}/{len(lines)}...")
                    QCoreApplication.processEvents()
            QMessageBox.information(self, "Success", f"Synced {len(lines)} points.")
        except Exception as e: QMessageBox.critical(self, "Failed", str(e))

    def start_prod(self):
        self.agent.status = "RUNNING"; self.lbl_status.setText("RUNNING"); self.lbl_status.setStyleSheet("color: green; font-weight: bold;")
        logging.info("Production started by operator")

    def pause_prod(self):
        reason, ok = QInputDialog.getText(self, "Downtime", "Reason code:")
        if ok:
            self.agent.status = "PAUSED"; self.agent.reason = reason
            self.lbl_status.setText(f"PAUSED ({reason})"); self.lbl_status.setStyleSheet("color: orange; font-weight: bold;")

    def on_telemetry_sent(self, data):
        mode = "OFFLINE" if self.agent.config.get("offline_mode") else "ONLINE"
        self.log_output.append(f"[{datetime.now().strftime('%H:%M:%S')}] Data saved ({mode}).")

    def on_error(self, err): self.log_output.append(f"<span style='color:red'>ERROR: {err}</span>")

if __name__ == "__main__":
    if sys.platform == 'win32': QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv); app.setStyle("Fusion"); panel = OperatorPanel(); panel.show(); sys.exit(app.exec())