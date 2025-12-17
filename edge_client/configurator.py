import sys
import json
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QListWidget, QLineEdit, QComboBox, QSplitter, 
                             QMessageBox, QListWidgetItem, QGroupBox, QFormLayout)
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QAction

class ROI:
    def __init__(self, x, y, w, h, name="New Region", data_type="text"):
        self.rect = QRect(x, y, w, h)
        self.name = name
        self.data_type = data_type # text, number, table, status

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.data_type,
            "x": self.rect.x(),
            "y": self.rect.y(),
            "w": self.rect.width(),
            "h": self.rect.height()
        }

    @staticmethod
    def from_dict(data):
        return ROI(data["x"], data["y"], data["w"], data["h"], data["name"], data.get("type", "text"))

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rois = []  # List of ROI objects
        self.current_start = None
        self.current_end = None
        self.selected_roi_index = -1
        self.setMouseTracking(True)
        self.drawing = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.pixmap():
            return

        painter = QPainter(self)
        
        # Draw all saved ROIs
        for i, roi in enumerate(self.rois):
            if i == self.selected_roi_index:
                pen = QPen(QColor(0, 255, 0), 2, Qt.PenStyle.SolidLine) # Green for selected
            else:
                pen = QPen(QColor(255, 0, 0), 2, Qt.PenStyle.SolidLine) # Red for others
            painter.setPen(pen)
            painter.drawRect(roi.rect)
            
            # Draw label background
            painter.fillRect(roi.rect.x(), roi.rect.y() - 20, len(roi.name) * 8 + 10, 20, QColor(0, 0, 0, 150))
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(roi.rect.x() + 5, roi.rect.y() - 5, roi.name)

        # Draw current drawing rectangle
        if self.current_start and self.current_end:
            painter.setPen(QPen(QColor(0, 0, 255), 2, Qt.PenStyle.DashLine))
            rect = QRect(self.current_start, self.current_end).normalized()
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        if not self.pixmap():
            return
            
        # Check if clicking on existing ROI to select it
        clicked_roi = False
        for i, roi in enumerate(reversed(self.rois)): # Check newest (top) first
            if roi.rect.contains(event.pos()):
                self.selected_roi_index = len(self.rois) - 1 - i
                self.parent().parent().roi_selected(self.selected_roi_index)
                clicked_roi = True
                self.update()
                break
        
        if not clicked_roi:
            self.drawing = True
            self.current_start = event.pos()
            self.current_end = event.pos()
            self.selected_roi_index = -1
            self.parent().parent().roi_selected(-1)

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.current_end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False
            self.current_end = event.pos()
            rect = QRect(self.current_start, self.current_end).normalized()
            
            if rect.width() > 5 and rect.height() > 5: # Minimal size filter
                new_roi = ROI(rect.x(), rect.y(), rect.width(), rect.height(), 
                             f"Field_{len(self.rois)+1}")
                self.rois.append(new_roi)
                self.selected_roi_index = len(self.rois) - 1
                self.parent().parent().roi_created(new_roi)
            
            self.current_start = None
            self.current_end = None
            self.update()

class ConfiguratorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScreenWatcher - ROI Configurator")
        self.resize(1200, 800)
        self.current_config_path = None

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left Panel - Image Area
        self.image_container = QWidget()
        image_layout = QVBoxLayout(self.image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = ImageLabel(self.image_container)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        image_layout.addWidget(self.image_label)
        image_layout.addStretch() # Push image to top-left

        scroll_area = QWidget() # Placeholder for scroll if needed, simple widget for now
        # Ideally QScrollArea, but let's keep it simple for fixed screenshots
        splitter.addWidget(self.image_container)

        # Right Panel - Controls
        controls_panel = QWidget()
        controls_layout = QVBoxLayout(controls_panel)
        
        # File Operations
        file_group = QGroupBox("File Operations")
        file_layout = QVBoxLayout()
        self.btn_load_image = QPushButton("Load Screenshot")
        self.btn_load_image.clicked.connect(self.load_image)
        self.btn_save_config = QPushButton("Save Configuration")
        self.btn_save_config.clicked.connect(self.save_config)
        self.btn_load_config = QPushButton("Load Configuration")
        self.btn_load_config.clicked.connect(self.load_config)
        
        file_layout.addWidget(self.btn_load_image)
        file_layout.addWidget(self.btn_load_config)
        file_layout.addWidget(self.btn_save_config)
        file_group.setLayout(file_layout)
        controls_layout.addWidget(file_group)

        # ROI List
        controls_layout.addWidget(QLabel("Defined Regions:"))
        self.roi_list_widget = QListWidget()
        self.roi_list_widget.currentRowChanged.connect(self.list_selection_changed)
        controls_layout.addWidget(self.roi_list_widget)

        # Selected ROI Properties
        prop_group = QGroupBox("Selected Region Properties")
        prop_layout = QFormLayout()
        
        self.input_name = QLineEdit()
        self.input_name.textChanged.connect(self.update_roi_data)
        
        self.combo_type = QComboBox()
        self.combo_type.addItems(["text", "number", "status", "table"])
        self.combo_type.currentTextChanged.connect(self.update_roi_data)

        self.btn_delete_roi = QPushButton("Delete Region")
        self.btn_delete_roi.setStyleSheet("background-color: #ffcccc;")
        self.btn_delete_roi.clicked.connect(self.delete_roi)

        prop_layout.addRow("Name:", self.input_name)
        prop_layout.addRow("Type:", self.combo_type)
        prop_layout.addRow(self.btn_delete_roi)
        
        prop_group.setLayout(prop_layout)
        controls_layout.addWidget(prop_group)
        
        controls_layout.addStretch()
        splitter.addWidget(controls_panel)
        
        # Set initial sizes
        splitter.setSizes([900, 300])

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Screenshot", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedSize(pixmap.size())
            # Auto-load config if exists
            possible_conf = file_name + ".json"
            if os.path.exists(possible_conf):
                 self.load_config_from_file(possible_conf)

    def roi_created(self, roi):
        item = QListWidgetItem(f"{roi.name} ({roi.data_type})")
        self.roi_list_widget.addItem(item)
        self.roi_list_widget.setCurrentRow(len(self.image_label.rois) - 1)
        self.input_name.setFocus()
        self.input_name.selectAll()

    def roi_selected(self, index):
        if index >= 0:
            self.roi_list_widget.setCurrentRow(index)
            roi = self.image_label.rois[index]
            self.input_name.setText(roi.name)
            self.combo_type.setCurrentText(roi.data_type)
        else:
            self.roi_list_widget.clearSelection()
            self.input_name.clear()

    def list_selection_changed(self, row):
        if row >= 0:
            self.image_label.selected_roi_index = row
            self.image_label.update()
            self.roi_selected(row)

    def update_roi_data(self):
        row = self.roi_list_widget.currentRow()
        if row >= 0:
            roi = self.image_label.rois[row]
            roi.name = self.input_name.text()
            roi.data_type = self.combo_type.currentText()
            
            # Update list item text
            self.roi_list_widget.item(row).setText(f"{roi.name} ({roi.data_type})")
            self.image_label.update()

    def delete_roi(self):
        row = self.roi_list_widget.currentRow()
        if row >= 0:
            self.image_label.rois.pop(row)
            self.roi_list_widget.takeItem(row)
            self.image_label.selected_roi_index = -1
            self.image_label.update()

    def save_config(self):
        if not self.image_label.pixmap():
            return
            
        data = {
            "rois": [r.to_dict() for r in self.image_label.rois]
        }
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
            self.current_config_path = file_name
            QMessageBox.information(self, "Success", f"Configuration saved to {file_name}")

    def load_config(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Configuration", "", "JSON Files (*.json)")
        if file_name:
            self.load_config_from_file(file_name)

    def load_config_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.image_label.rois = [ROI.from_dict(r) for r in data.get("rois", [])]
            
            self.roi_list_widget.clear()
            for roi in self.image_label.rois:
                item = QListWidgetItem(f"{roi.name} ({roi.data_type})")
                self.roi_list_widget.addItem(item)
            
            self.image_label.update()
            self.current_config_path = file_path
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load config: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfiguratorWindow()
    window.show()
    sys.exit(app.exec())
