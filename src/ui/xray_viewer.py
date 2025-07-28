"""
X-ray Viewer Widget
Provides DICOM image viewing with annotation and measurement tools
"""

import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QComboBox, QListWidget,
                             QListWidgetItem, QSplitter, QFrame, QGroupBox,
                             QScrollArea, QMessageBox, QFileDialog, QTextEdit)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QPen, QColor, QImage
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

import pydicom
import numpy as np
from PIL import Image, ImageEnhance

class XRayViewerWidget(QWidget):
    """X-ray image viewer with DICOM support and annotation tools"""
    
    def __init__(self, db_manager, auth_manager):
        super().__init__()
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.current_patient_id = None
        self.current_image = None
        self.dicom_data = None
        self.zoom_factor = 1.0
        self.brightness = 1.0
        self.contrast = 1.0
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left panel - Image list and controls
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        left_panel.setMaximumWidth(300)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
        """)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        
        # Image list group
        image_list_group = QGroupBox("Patient X-rays")
        image_list_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        image_list_layout = QVBoxLayout(image_list_group)
        
        self.image_list = QListWidget()
        self.image_list.setFont(QFont("Segoe UI", 9))
        self.image_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        image_list_layout.addWidget(self.image_list)
        
        # Import button
        import_button = QPushButton("Import DICOM")
        import_button.setFont(QFont("Segoe UI", 10))
        import_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        image_list_layout.addWidget(import_button)
        
        # Image controls group
        controls_group = QGroupBox("Image Controls")
        controls_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        controls_layout = QVBoxLayout(controls_group)
        
        # Zoom control
        zoom_label = QLabel("Zoom:")
        zoom_label.setFont(QFont("Segoe UI", 9))
        
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(25, 400)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.zoom_slider.setTickInterval(25)
        
        self.zoom_value_label = QLabel("100%")
        self.zoom_value_label.setFont(QFont("Segoe UI", 9))
        self.zoom_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(zoom_label)
        zoom_layout.addWidget(self.zoom_slider)
        zoom_layout.addWidget(self.zoom_value_label)
        
        # Brightness control
        brightness_label = QLabel("Brightness:")
        brightness_label.setFont(QFont("Segoe UI", 9))
        
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 200)
        self.brightness_slider.setValue(100)
        
        self.brightness_value_label = QLabel("100%")
        self.brightness_value_label.setFont(QFont("Segoe UI", 9))
        self.brightness_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        brightness_layout = QHBoxLayout()
        brightness_layout.addWidget(brightness_label)
        brightness_layout.addWidget(self.brightness_slider)
        brightness_layout.addWidget(self.brightness_value_label)
        
        # Contrast control
        contrast_label = QLabel("Contrast:")
        contrast_label.setFont(QFont("Segoe UI", 9))
        
        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)
        
        self.contrast_value_label = QLabel("100%")
        self.contrast_value_label.setFont(QFont("Segoe UI", 9))
        self.contrast_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        contrast_layout = QHBoxLayout()
        contrast_layout.addWidget(contrast_label)
        contrast_layout.addWidget(self.contrast_slider)
        contrast_layout.addWidget(self.contrast_value_label)
        
        # Reset button
        reset_button = QPushButton("Reset View")
        reset_button.setFont(QFont("Segoe UI", 9))
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        # Add controls to group
        controls_layout.addLayout(zoom_layout)
        controls_layout.addLayout(brightness_layout)
        controls_layout.addLayout(contrast_layout)
        controls_layout.addWidget(reset_button)
        
        # Position presets group
        presets_group = QGroupBox("Position Presets")
        presets_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        presets_layout = QVBoxLayout(presets_group)
        
        self.position_combo = QComboBox()
        self.position_combo.addItems([
            "Chest AP", "Chest PA", "Chest Lateral",
            "Spine AP", "Spine PA", "Spine Lateral",
            "Abdomen AP", "Abdomen PA",
            "Skull AP", "Skull PA", "Skull Lateral",
            "Upper Limb", "Lower Limb"
        ])
        self.position_combo.setFont(QFont("Segoe UI", 9))
        
        presets_layout.addWidget(self.position_combo)
        
        # Add groups to left panel
        left_layout.addWidget(image_list_group)
        left_layout.addWidget(controls_group)
        left_layout.addWidget(presets_group)
        left_layout.addStretch()
        
        # Right panel - Image viewer
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
        """)
        
        right_layout = QVBoxLayout(right_panel)
        
        # Image viewer header
        self.viewer_header = QLabel("No image selected")
        self.viewer_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.viewer_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.viewer_header.setStyleSheet("color: #7f8c8d; padding: 10px;")
        
        # Image viewer
        self.image_view = QGraphicsView()
        self.image_view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.image_view.setStyleSheet("border: 1px solid #bdc3c7; background-color: #2c3e50;")
        
        self.image_scene = QGraphicsScene()
        self.image_view.setScene(self.image_scene)
        
        # Image info group
        info_group = QGroupBox("Image Information")
        info_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        info_layout = QVBoxLayout(info_group)
        
        self.image_info_text = QTextEdit()
        self.image_info_text.setReadOnly(True)
        self.image_info_text.setMaximumHeight(100)
        self.image_info_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
                font-family: 'Courier New', monospace;
                font-size: 9px;
            }
        """)
        
        info_layout.addWidget(self.image_info_text)
        
        # Annotations group
        annotations_group = QGroupBox("Annotations")
        annotations_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        annotations_layout = QVBoxLayout(annotations_group)
        
        self.annotations_text = QTextEdit()
        self.annotations_text.setMaximumHeight(100)
        self.annotations_text.setPlaceholderText("Enter annotations for this image...")
        self.annotations_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        save_annotations_button = QPushButton("Save Annotations")
        save_annotations_button.setFont(QFont("Segoe UI", 9))
        save_annotations_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        annotations_layout.addWidget(self.annotations_text)
        annotations_layout.addWidget(save_annotations_button)
        
        # Add to right panel
        right_layout.addWidget(self.viewer_header)
        right_layout.addWidget(self.image_view)
        right_layout.addWidget(info_group)
        right_layout.addWidget(annotations_group)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.image_list.itemSelectionChanged.connect(self.on_image_selected)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        self.brightness_slider.valueChanged.connect(self.on_brightness_changed)
        self.contrast_slider.valueChanged.connect(self.on_contrast_changed)
        
    def load_patient_xrays(self, patient_id):
        """Load X-ray images for the specified patient"""
        self.current_patient_id = patient_id
        
        if not patient_id:
            self.image_list.clear()
            return
            
        # Get patient X-rays from database
        xrays = self.db_manager.get_patient_xrays(patient_id)
        
        # Populate image list
        self.image_list.clear()
        for xray in xrays:
            item_text = f"{xray['body_part']} - {xray['position']} ({xray['acquisition_date']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, xray)
            self.image_list.addItem(item)
            
    def on_image_selected(self):
        """Handle image selection from list"""
        current_item = self.image_list.currentItem()
        if current_item:
            xray_data = current_item.data(Qt.ItemDataRole.UserRole)
            self.load_image(xray_data)
            
    def load_image(self, xray_data):
        """Load and display the selected X-ray image"""
        try:
            image_path = xray_data['image_path']
            
            if not os.path.exists(image_path):
                QMessageBox.warning(self, "File Not Found", 
                                  f"Image file not found: {image_path}")
                return
                
            # Try to load as DICOM first
            try:
                self.dicom_data = pydicom.dcmread(image_path)
                self.display_dicom_image()
            except:
                # Fall back to regular image
                self.display_regular_image(image_path)
                
            # Update header
            self.viewer_header.setText(f"{xray_data['body_part']} - {xray_data['position']}")
            
            # Load annotations
            self.annotations_text.setText(xray_data.get('annotations', ''))
            
            # Update image info
            self.update_image_info(xray_data)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
            
    def display_dicom_image(self):
        """Display DICOM image with proper windowing"""
        if not self.dicom_data:
            return
            
        # Get pixel data
        pixel_array = self.dicom_data.pixel_array
        
        # Apply window/level if available
        if hasattr(self.dicom_data, 'WindowCenter') and hasattr(self.dicom_data, 'WindowWidth'):
            window_center = self.dicom_data.WindowCenter
            window_width = self.dicom_data.WindowWidth
            
            # Apply windowing
            min_val = window_center - window_width // 2
            max_val = window_center + window_width // 2
            pixel_array = np.clip(pixel_array, min_val, max_val)
            
        # Normalize to 0-255
        pixel_array = ((pixel_array - pixel_array.min()) / 
                      (pixel_array.max() - pixel_array.min()) * 255).astype(np.uint8)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(pixel_array)
        
        # Apply brightness and contrast
        pil_image = self.apply_image_adjustments(pil_image)
        
        # Convert to QPixmap
        qimage = self.pil_to_qimage(pil_image)
        pixmap = QPixmap.fromImage(qimage)
        
        # Display in viewer
        self.display_pixmap(pixmap)
        
    def display_regular_image(self, image_path):
        """Display regular image file"""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", "Failed to load image file")
            return
            
        # Apply adjustments
        pil_image = Image.open(image_path)
        pil_image = self.apply_image_adjustments(pil_image)
        
        qimage = self.pil_to_qimage(pil_image)
        pixmap = QPixmap.fromImage(qimage)
        
        self.display_pixmap(pixmap)
        
    def apply_image_adjustments(self, pil_image):
        """Apply brightness and contrast adjustments"""
        # Apply brightness
        if self.brightness != 1.0:
            enhancer = ImageEnhance.Brightness(pil_image)
            pil_image = enhancer.enhance(self.brightness)
            
        # Apply contrast
        if self.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(self.contrast)
            
        return pil_image
        
    def pil_to_qimage(self, pil_image):
        """Convert PIL Image to QImage"""
        if pil_image.mode == "RGB":
            r, g, b = pil_image.split()
            pil_image = Image.merge("RGB", (b, g, r))
        elif pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            pil_image = Image.merge("RGBA", (b, g, r, a))
        elif pil_image.mode == "L":
            pil_image = pil_image.convert("RGBA")
            
        im_data = pil_image.tobytes("raw", pil_image.mode)
        qim = QImage(im_data, pil_image.size[0], pil_image.size[1], 
                    QImage.Format.Format_RGBA8888)
        return qim
        
    def display_pixmap(self, pixmap):
        """Display pixmap in the viewer"""
        self.image_scene.clear()
        
        # Add pixmap to scene
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.image_scene.addItem(pixmap_item)
        
        # Fit to view
        self.image_view.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        
    def on_zoom_changed(self, value):
        """Handle zoom slider change"""
        self.zoom_factor = value / 100.0
        self.zoom_value_label.setText(f"{value}%")
        
        if self.image_scene.items():
            self.image_view.setTransform(self.image_view.transform().scale(self.zoom_factor, self.zoom_factor))
            
    def on_brightness_changed(self, value):
        """Handle brightness slider change"""
        self.brightness = value / 100.0
        self.brightness_value_label.setText(f"{value}%")
        
        # Reload current image with new settings
        current_item = self.image_list.currentItem()
        if current_item:
            xray_data = current_item.data(Qt.ItemDataRole.UserRole)
            self.load_image(xray_data)
            
    def on_contrast_changed(self, value):
        """Handle contrast slider change"""
        self.contrast = value / 100.0
        self.contrast_value_label.setText(f"{value}%")
        
        # Reload current image with new settings
        current_item = self.image_list.currentItem()
        if current_item:
            xray_data = current_item.data(Qt.ItemDataRole.UserRole)
            self.load_image(xray_data)
            
    def update_image_info(self, xray_data):
        """Update image information display"""
        info_text = f"Body Part: {xray_data['body_part']}\n"
        info_text += f"Position: {xray_data['position']}\n"
        info_text += f"Acquisition Date: {xray_data['acquisition_date']}\n"
        info_text += f"Notes: {xray_data.get('notes', 'None')}\n"
        
        if self.dicom_data:
            info_text += f"\nDICOM Info:\n"
            info_text += f"Modality: {getattr(self.dicom_data, 'Modality', 'Unknown')}\n"
            info_text += f"Manufacturer: {getattr(self.dicom_data, 'Manufacturer', 'Unknown')}\n"
            info_text += f"Image Size: {getattr(self.dicom_data, 'Rows', 'Unknown')}x{getattr(self.dicom_data, 'Columns', 'Unknown')}\n"
            
        self.image_info_text.setText(info_text) 