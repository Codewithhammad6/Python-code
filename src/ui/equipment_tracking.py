"""
Equipment Tracking Widget
Monitors X-ray scanner status and maintenance logs
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QDialog, QFormLayout, QTextEdit, 
                             QComboBox, QDateEdit, QFrame, QGroupBox, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTimer
from PyQt6.QtGui import QFont, QColor

from database.database_manager import DatabaseManager
from security.auth_manager import AuthManager

class EquipmentTrackingWidget(QWidget):
    """Widget for tracking equipment status and maintenance"""
    
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthManager):
        super().__init__()
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        
        self.setup_ui()
        self.setup_connections()
        self.load_equipment_data()
        
        # Timer for status updates
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_equipment_status)
        self.status_timer.start(30000)  # Update every 30 seconds
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Equipment Tracking & Maintenance")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        add_equipment_button = QPushButton("+ Add Equipment")
        add_equipment_button.setFont(QFont("Segoe UI", 10))
        add_equipment_button.setStyleSheet("""
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
        add_equipment_button.clicked.connect(self.add_equipment)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(add_equipment_button)
        
        # Status overview cards
        status_layout = QHBoxLayout()
        
        # Operational equipment card
        self.operational_card = self.create_status_card("Operational", "0", "#27ae60")
        
        # Maintenance needed card
        self.maintenance_card = self.create_status_card("Maintenance Needed", "0", "#f39c12")
        
        # Out of service card
        self.outofservice_card = self.create_status_card("Out of Service", "0", "#e74c3c")
        
        status_layout.addWidget(self.operational_card)
        status_layout.addWidget(self.maintenance_card)
        status_layout.addWidget(self.outofservice_card)
        
        # Equipment table
        equipment_group = QGroupBox("Equipment List")
        equipment_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        equipment_layout = QVBoxLayout(equipment_group)
        
        # Table
        self.equipment_table = QTableWidget()
        self.equipment_table.setColumnCount(7)
        self.equipment_table.setHorizontalHeaderLabels([
            "Name", "Type", "Status", "Location", "Last Maintenance", 
            "Next Maintenance", "Actions"
        ])
        self.equipment_table.setFont(QFont("Segoe UI", 9))
        self.equipment_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #bdc3c7;
                background-color: white;
                gridline-color: #ecf0f1;
            }
            QHeaderView::section {
                background-color: #ecf0f1;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        equipment_layout.addWidget(self.equipment_table)
        
        # Add to main layout
        main_layout.addLayout(header_layout)
        main_layout.addLayout(status_layout)
        main_layout.addWidget(equipment_group)
        
    def create_status_card(self, title: str, count: str, color: str) -> QFrame:
        """Create a status overview card"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Count
        count_label = QLabel(count)
        count_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        count_label.setStyleSheet(f"color: {color};")
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(count_label)
        
        return card
        
    def setup_connections(self):
        """Setup signal connections"""
        self.equipment_table.itemSelectionChanged.connect(self.on_equipment_selected)
        
    def load_equipment_data(self):
        """Load equipment data from database"""
        try:
            # This would normally fetch from database
            # For now, we'll create sample data
            sample_equipment = [
                {
                    'id': 1,
                    'name': 'X-ray Scanner A',
                    'type': 'Digital Radiography',
                    'status': 'operational',
                    'location': 'Room 101',
                    'last_maintenance': '2024-01-15',
                    'next_maintenance': '2024-04-15'
                },
                {
                    'id': 2,
                    'name': 'X-ray Scanner B',
                    'type': 'Computed Radiography',
                    'status': 'maintenance_needed',
                    'location': 'Room 102',
                    'last_maintenance': '2023-12-01',
                    'next_maintenance': '2024-03-01'
                },
                {
                    'id': 3,
                    'name': 'Mobile X-ray Unit',
                    'type': 'Portable',
                    'status': 'operational',
                    'location': 'Mobile',
                    'last_maintenance': '2024-02-01',
                    'next_maintenance': '2024-05-01'
                }
            ]
            
            self.populate_equipment_table(sample_equipment)
            self.update_status_cards(sample_equipment)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load equipment data: {str(e)}")
            
    def populate_equipment_table(self, equipment_list):
        """Populate the equipment table"""
        self.equipment_table.setRowCount(len(equipment_list))
        
        for row, equipment in enumerate(equipment_list):
            # Name
            name_item = QTableWidgetItem(equipment['name'])
            name_item.setData(Qt.ItemDataRole.UserRole, equipment)
            self.equipment_table.setItem(row, 0, name_item)
            
            # Type
            type_item = QTableWidgetItem(equipment['type'])
            self.equipment_table.setItem(row, 1, type_item)
            
            # Status
            status_item = QTableWidgetItem(equipment['status'].replace('_', ' ').title())
            status_item.setData(Qt.ItemDataRole.UserRole, equipment['status'])
            self.set_status_color(status_item, equipment['status'])
            self.equipment_table.setItem(row, 2, status_item)
            
            # Location
            location_item = QTableWidgetItem(equipment['location'])
            self.equipment_table.setItem(row, 3, location_item)
            
            # Last Maintenance
            last_maint_item = QTableWidgetItem(equipment['last_maintenance'])
            self.equipment_table.setItem(row, 4, last_maint_item)
            
            # Next Maintenance
            next_maint_item = QTableWidgetItem(equipment['next_maintenance'])
            self.equipment_table.setItem(row, 5, next_maint_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            
            view_button = QPushButton("View")
            view_button.setFont(QFont("Segoe UI", 8))
            view_button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            view_button.clicked.connect(lambda checked, eq=equipment: self.view_equipment(eq))
            
            edit_button = QPushButton("Edit")
            edit_button.setFont(QFont("Segoe UI", 8))
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #e67e22;
                }
            """)
            edit_button.clicked.connect(lambda checked, eq=equipment: self.edit_equipment(eq))
            
            actions_layout.addWidget(view_button)
            actions_layout.addWidget(edit_button)
            actions_layout.addStretch()
            
            self.equipment_table.setCellWidget(row, 6, actions_widget)
        
        # Resize columns
        self.equipment_table.resizeColumnsToContents()
        
    def set_status_color(self, item: QTableWidgetItem, status: str):
        """Set color for status items"""
        if status == 'operational':
            item.setBackground(QColor("#d5f4e6"))
            item.setForeground(QColor("#27ae60"))
        elif status == 'maintenance_needed':
            item.setBackground(QColor("#fef9e7"))
            item.setForeground(QColor("#f39c12"))
        elif status == 'out_of_service':
            item.setBackground(QColor("#fadbd8"))
            item.setForeground(QColor("#e74c3c"))
            
    def update_status_cards(self, equipment_list):
        """Update status overview cards"""
        operational_count = sum(1 for eq in equipment_list if eq['status'] == 'operational')
        maintenance_count = sum(1 for eq in equipment_list if eq['status'] == 'maintenance_needed')
        outofservice_count = sum(1 for eq in equipment_list if eq['status'] == 'out_of_service')
        
        # Update card counts
        self.operational_card.findChild(QLabel, "").setText(str(operational_count))
        self.maintenance_card.findChild(QLabel, "").setText(str(maintenance_count))
        self.outofservice_card.findChild(QLabel, "").setText(str(outofservice_count))
        
    def update_equipment_status(self):
        """Update equipment status (called by timer)"""
        # This would normally check real-time status from equipment
        # For now, just reload data
        self.load_equipment_data()
        
    def on_equipment_selected(self):
        """Handle equipment selection"""
        current_row = self.equipment_table.currentRow()
        if current_row >= 0:
            item = self.equipment_table.item(current_row, 0)
            if item:
                equipment_data = item.data(Qt.ItemDataRole.UserRole)
                # Could show detailed info in a side panel
                
    def add_equipment(self):
        """Open add equipment dialog"""
        if not self.auth_manager.has_permission('add_equipment'):
            QMessageBox.warning(self, "Access Denied", 
                              "You don't have permission to add equipment.")
            return
            
        dialog = EquipmentDialog(self.db_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_equipment_data()
            
    def view_equipment(self, equipment):
        """View equipment details"""
        dialog = EquipmentDetailsDialog(equipment, self.db_manager, self)
        dialog.exec()
        
    def edit_equipment(self, equipment):
        """Edit equipment details"""
        if not self.auth_manager.has_permission('edit_equipment'):
            QMessageBox.warning(self, "Access Denied", 
                              "You don't have permission to edit equipment.")
            return
            
        dialog = EquipmentDialog(self.db_manager, self, equipment)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_equipment_data()


class EquipmentDialog(QDialog):
    """Dialog for adding/editing equipment"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None, equipment=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.equipment = equipment
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Add Equipment" if not self.equipment else "Edit Equipment")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Add Equipment" if not self.equipment else "Edit Equipment")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter equipment name")
        if self.equipment:
            self.name_edit.setText(self.equipment['name'])
        form_layout.addRow("Name:", self.name_edit)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Digital Radiography", "Computed Radiography", "Portable",
            "Fluoroscopy", "CT Scanner", "MRI Scanner"
        ])
        if self.equipment:
            index = self.type_combo.findText(self.equipment['type'])
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
        form_layout.addRow("Type:", self.type_combo)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["operational", "maintenance_needed", "out_of_service"])
        if self.equipment:
            index = self.status_combo.findText(self.equipment['status'])
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
        form_layout.addRow("Status:", self.status_combo)
        
        # Location
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Enter location")
        if self.equipment:
            self.location_edit.setText(self.equipment['location'])
        form_layout.addRow("Location:", self.location_edit)
        
        # Last Maintenance
        self.last_maintenance_edit = QDateEdit()
        self.last_maintenance_edit.setCalendarPopup(True)
        if self.equipment:
            self.last_maintenance_edit.setDate(QDate.fromString(self.equipment['last_maintenance'], 'yyyy-MM-dd'))
        else:
            self.last_maintenance_edit.setDate(QDate.currentDate())
        form_layout.addRow("Last Maintenance:", self.last_maintenance_edit)
        
        # Next Maintenance
        self.next_maintenance_edit = QDateEdit()
        self.next_maintenance_edit.setCalendarPopup(True)
        if self.equipment:
            self.next_maintenance_edit.setDate(QDate.fromString(self.equipment['next_maintenance'], 'yyyy-MM-dd'))
        else:
            self.next_maintenance_edit.setDate(QDate.currentDate().addMonths(3))
        form_layout.addRow("Next Maintenance:", self.next_maintenance_edit)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(80)
        self.notes_edit.setPlaceholderText("Enter equipment notes...")
        if self.equipment:
            self.notes_edit.setText(self.equipment.get('notes', ''))
        form_layout.addRow("Notes:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        save_button.clicked.connect(self.save_equipment)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
    def save_equipment(self):
        """Save equipment data"""
        # Validate required fields
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation Error", "Equipment name is required.")
            self.name_edit.setFocus()
            return
            
        # Create equipment data
        equipment_data = {
            'name': name,
            'type': self.type_combo.currentText(),
            'status': self.status_combo.currentText(),
            'location': self.location_edit.text().strip(),
            'last_maintenance': self.last_maintenance_edit.date().toString('yyyy-MM-dd'),
            'next_maintenance': self.next_maintenance_edit.date().toString('yyyy-MM-dd'),
            'notes': self.notes_edit.toPlainText()
        }
        
        try:
            # Save to database (this would be implemented in database manager)
            QMessageBox.information(self, "Success", "Equipment saved successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save equipment: {str(e)}")


class EquipmentDetailsDialog(QDialog):
    """Dialog for viewing equipment details"""
    
    def __init__(self, equipment: dict, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.equipment = equipment
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(f"Equipment Details - {self.equipment['name']}")
        self.setFixedSize(600, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel(f"Equipment Details: {self.equipment['name']}")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Equipment info
        info_group = QGroupBox("Equipment Information")
        info_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        info_layout = QFormLayout(info_group)
        
        info_layout.addRow("Name:", QLabel(self.equipment['name']))
        info_layout.addRow("Type:", QLabel(self.equipment['type']))
        info_layout.addRow("Status:", QLabel(self.equipment['status'].replace('_', ' ').title()))
        info_layout.addRow("Location:", QLabel(self.equipment['location']))
        info_layout.addRow("Last Maintenance:", QLabel(self.equipment['last_maintenance']))
        info_layout.addRow("Next Maintenance:", QLabel(self.equipment['next_maintenance']))
        
        layout.addWidget(info_group)
        
        # Maintenance history (would be populated from database)
        history_group = QGroupBox("Maintenance History")
        history_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        history_layout = QVBoxLayout(history_group)
        
        history_text = QTextEdit()
        history_text.setReadOnly(True)
        history_text.setMaximumHeight(150)
        history_text.setText("No maintenance history available.")
        history_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
            }
        """)
        
        history_layout.addWidget(history_text)
        layout.addWidget(history_group)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        close_button.clicked.connect(self.accept)
        
        layout.addWidget(close_button) 