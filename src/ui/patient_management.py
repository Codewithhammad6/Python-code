"""
Patient Management Widget
Handles patient search, creation, and viewing
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QDialog, QFormLayout, QTextEdit, QComboBox,
                             QDateEdit, QFrame, QSplitter, QScrollArea, QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QPixmap

from database.database_manager import DatabaseManager
from security.auth_manager import AuthManager

class PatientManagementWidget(QWidget):
    """Widget for managing patient records"""
    
    # Signals
    patient_selected = pyqtSignal(dict)  # Emits patient data when selected
    
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthManager):
        super().__init__()
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.current_patient = None
        
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left panel - Search and list
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.Shape.StyledPanel)
        left_panel.setMaximumWidth(400)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
        """)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        
        # Search section
        search_group = QGroupBox("Search Patients")
        search_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        search_layout = QVBoxLayout(search_group)
        
        # Search input
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name or patient ID...")
        self.search_edit.setFont(QFont("Segoe UI", 10))
        self.search_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #ecf0f1;
                border-radius: 4px;
                background-color: #f8f9fa;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: white;
            }
        """)
        
        # Search button
        search_button = QPushButton("Search")
        search_button.setFont(QFont("Segoe UI", 10))
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_button)
        
        # New patient button
        new_patient_button = QPushButton("+ New Patient")
        new_patient_button.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        new_patient_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        
        # Patients table
        self.patients_table = QTableWidget()
        self.patients_table.setColumnCount(3)
        self.patients_table.setHorizontalHeaderLabels(["Patient ID", "Name", "Age"])
        self.patients_table.setFont(QFont("Segoe UI", 9))
        self.patients_table.setStyleSheet("""
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
        
        # Add widgets to left panel
        left_layout.addWidget(search_group)
        left_layout.addWidget(new_patient_button)
        left_layout.addWidget(self.patients_table)
        
        # Right panel - Patient details
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
        
        # Patient details header
        self.patient_header = QLabel("Select a patient to view details")
        self.patient_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.patient_header.setStyleSheet("color: #2c3e50; padding: 10px;")
        self.patient_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Patient details scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none;")
        
        self.patient_details_widget = QWidget()
        self.patient_details_layout = QVBoxLayout(self.patient_details_widget)
        
        # Patient info group
        self.patient_info_group = QGroupBox("Patient Information")
        self.patient_info_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.patient_info_layout = QFormLayout(self.patient_info_group)
        
        # Patient info fields
        self.patient_id_label = QLabel("")
        self.patient_name_label = QLabel("")
        self.patient_dob_label = QLabel("")
        self.patient_gender_label = QLabel("")
        self.patient_phone_label = QLabel("")
        self.patient_email_label = QLabel("")
        
        # Style for info labels
        info_style = "color: #2c3e50; font-weight: normal;"
        self.patient_id_label.setStyleSheet(info_style)
        self.patient_name_label.setStyleSheet(info_style)
        self.patient_dob_label.setStyleSheet(info_style)
        self.patient_gender_label.setStyleSheet(info_style)
        self.patient_phone_label.setStyleSheet(info_style)
        self.patient_email_label.setStyleSheet(info_style)
        
        # Add fields to form
        self.patient_info_layout.addRow("Patient ID:", self.patient_id_label)
        self.patient_info_layout.addRow("Name:", self.patient_name_label)
        self.patient_info_layout.addRow("Date of Birth:", self.patient_dob_label)
        self.patient_info_layout.addRow("Gender:", self.patient_gender_label)
        self.patient_info_layout.addRow("Phone:", self.patient_phone_label)
        self.patient_info_layout.addRow("Email:", self.patient_email_label)
        
        # Medical history group
        self.medical_history_group = QGroupBox("Medical History")
        self.medical_history_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        medical_history_layout = QVBoxLayout(self.medical_history_group)
        
        self.medical_history_text = QTextEdit()
        self.medical_history_text.setReadOnly(True)
        self.medical_history_text.setMaximumHeight(150)
        self.medical_history_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
            }
        """)
        
        medical_history_layout.addWidget(self.medical_history_text)
        
        # Doctor notes group
        self.doctor_notes_group = QGroupBox("Doctor's Notes")
        self.doctor_notes_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        doctor_notes_layout = QVBoxLayout(self.doctor_notes_group)
        
        self.doctor_notes_text = QTextEdit()
        self.doctor_notes_text.setReadOnly(True)
        self.doctor_notes_text.setMaximumHeight(150)
        self.doctor_notes_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
            }
        """)
        
        doctor_notes_layout.addWidget(self.doctor_notes_text)
        
        # Add groups to patient details
        self.patient_details_layout.addWidget(self.patient_info_group)
        self.patient_details_layout.addWidget(self.medical_history_group)
        self.patient_details_layout.addWidget(self.doctor_notes_group)
        self.patient_details_layout.addStretch()
        
        scroll_area.setWidget(self.patient_details_widget)
        
        # Add to right panel
        right_layout.addWidget(self.patient_header)
        right_layout.addWidget(scroll_area)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.patients_table.itemSelectionChanged.connect(self.on_patient_selected)
        
    def search_patients(self):
        """Search for patients"""
        search_term = self.search_edit.text().strip()
        if not search_term:
            # Show all patients
            patients = self.db_manager.search_patients("")
        else:
            patients = self.db_manager.search_patients(search_term)
        
        self.populate_patients_table(patients)
        
    def populate_patients_table(self, patients):
        """Populate the patients table with search results"""
        self.patients_table.setRowCount(len(patients))
        
        for row, patient in enumerate(patients):
            # Patient ID
            id_item = QTableWidgetItem(patient.get('patient_id', ''))
            id_item.setData(Qt.ItemDataRole.UserRole, patient)
            self.patients_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(patient.get('name', ''))
            self.patients_table.setItem(row, 1, name_item)
            
            # Age (calculate from DOB)
            dob = patient.get('date_of_birth', '')
            age = self.calculate_age(dob) if dob else ''
            age_item = QTableWidgetItem(str(age) if age else '')
            self.patients_table.setItem(row, 2, age_item)
        
        # Resize columns
        self.patients_table.resizeColumnsToContents()
        
    def calculate_age(self, dob_str):
        """Calculate age from date of birth string"""
        try:
            from datetime import datetime
            dob = datetime.strptime(dob_str, '%Y-%m-%d')
            today = datetime.now()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            return age
        except:
            return None
            
    def on_patient_selected(self):
        """Handle patient selection from table"""
        current_row = self.patients_table.currentRow()
        if current_row >= 0:
            item = self.patients_table.item(current_row, 0)
            if item:
                patient_data = item.data(Qt.ItemDataRole.UserRole)
                self.display_patient_details(patient_data)
                self.patient_selected.emit(patient_data)
                
    def display_patient_details(self, patient_data):
        """Display patient details in the right panel"""
        self.current_patient = patient_data
        
        # Update header
        self.patient_header.setText(f"Patient: {patient_data.get('name', 'Unknown')}")
        
        # Update patient info
        self.patient_id_label.setText(patient_data.get('patient_id', ''))
        self.patient_name_label.setText(patient_data.get('name', ''))
        self.patient_dob_label.setText(patient_data.get('date_of_birth', ''))
        self.patient_gender_label.setText(patient_data.get('gender', ''))
        self.patient_phone_label.setText(patient_data.get('phone', ''))
        self.patient_email_label.setText(patient_data.get('email', ''))
        
        # Update medical history
        self.medical_history_text.setText(patient_data.get('medical_history', ''))
        
        # Update doctor notes
        self.doctor_notes_text.setText(patient_data.get('doctor_notes', ''))
        
    def new_patient(self):
        """Open new patient dialog"""
        if not self.auth_manager.has_permission('add_patients'):
            QMessageBox.warning(self, "Access Denied", 
                              "You don't have permission to add new patients.")
            return
            
        dialog = NewPatientDialog(self.db_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Refresh patient list
            self.search_patients()


class NewPatientDialog(QDialog):
    """Dialog for creating a new patient"""
    
    def __init__(self, db_manager: DatabaseManager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("New Patient")
        self.setFixedSize(500, 600)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Add New Patient")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Patient ID
        self.patient_id_edit = QLineEdit()
        self.patient_id_edit.setPlaceholderText("Enter patient ID")
        form_layout.addRow("Patient ID:", self.patient_id_edit)
        
        # Name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter full name")
        form_layout.addRow("Full Name:", self.name_edit)
        
        # Date of Birth
        self.dob_edit = QDateEdit()
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setDate(QDate.currentDate().addYears(-30))
        form_layout.addRow("Date of Birth:", self.dob_edit)
        
        # Gender
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Male", "Female", "Other"])
        form_layout.addRow("Gender:", self.gender_combo)
        
        # Phone
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("Enter phone number")
        form_layout.addRow("Phone:", self.phone_edit)
        
        # Email
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter email address")
        form_layout.addRow("Email:", self.email_edit)
        
        # Medical History
        self.medical_history_edit = QTextEdit()
        self.medical_history_edit.setMaximumHeight(100)
        self.medical_history_edit.setPlaceholderText("Enter medical history...")
        form_layout.addRow("Medical History:", self.medical_history_edit)
        
        # Doctor Notes
        self.doctor_notes_edit = QTextEdit()
        self.doctor_notes_edit.setMaximumHeight(100)
        self.doctor_notes_edit.setPlaceholderText("Enter doctor's notes...")
        form_layout.addRow("Doctor's Notes:", self.doctor_notes_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Patient")
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
        save_button.clicked.connect(self.save_patient)
        
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
        
    def save_patient(self):
        """Save the new patient"""
        # Validate required fields
        patient_id = self.patient_id_edit.text().strip()
        name = self.name_edit.text().strip()
        
        if not patient_id:
            QMessageBox.warning(self, "Validation Error", "Patient ID is required.")
            self.patient_id_edit.setFocus()
            return
            
        if not name:
            QMessageBox.warning(self, "Validation Error", "Patient name is required.")
            self.name_edit.setFocus()
            return
        
        # Create patient data
        patient_data = {
            'patient_id': patient_id,
            'name': name,
            'date_of_birth': self.dob_edit.date().toString('yyyy-MM-dd'),
            'gender': self.gender_combo.currentText(),
            'phone': self.phone_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'medical_history': self.medical_history_edit.toPlainText(),
            'doctor_notes': self.doctor_notes_edit.toPlainText()
        }
        
        try:
            # Save to database
            self.db_manager.add_patient(patient_data)
            QMessageBox.information(self, "Success", "Patient added successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add patient: {str(e)}") 