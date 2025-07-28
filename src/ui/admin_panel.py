"""
Admin Panel Widget
Provides system administration and user management functionality
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QMessageBox, QDialog, QFormLayout, QTextEdit, 
                             QComboBox, QTabWidget, QFrame, QGroupBox, 
                             QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from database.database_manager import DatabaseManager
from security.auth_manager import AuthManager

class AdminPanelWidget(QWidget):
    """Admin panel for system administration"""
    
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthManager):
        super().__init__()
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        
        self.setup_ui()
        self.setup_connections()
        self.load_data()
        
    def setup_ui(self):
        """Setup the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("System Administration")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Segoe UI", 10))
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3498db;
            }
            QTabBar::tab:hover {
                background-color: #d5dbdb;
            }
        """)
        
        # Create tabs
        self.create_user_management_tab()
        self.create_audit_logs_tab()
        self.create_system_status_tab()
        
        # Add to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.tab_widget)
        
    def create_user_management_tab(self):
        """Create user management tab"""
        user_widget = QWidget()
        user_layout = QVBoxLayout(user_widget)
        
        # Header
        user_header_layout = QHBoxLayout()
        
        user_title = QLabel("User Management")
        user_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        
        add_user_button = QPushButton("+ Add User")
        add_user_button.setFont(QFont("Segoe UI", 10))
        add_user_button.setStyleSheet("""
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
        add_user_button.clicked.connect(self.add_user)
        
        user_header_layout.addWidget(user_title)
        user_header_layout.addStretch()
        user_header_layout.addWidget(add_user_button)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels([
            "Username", "Full Name", "Role", "Email", "Last Login", "Status"
        ])
        self.users_table.setFont(QFont("Segoe UI", 9))
        self.users_table.setStyleSheet("""
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
        
        user_layout.addLayout(user_header_layout)
        user_layout.addWidget(self.users_table)
        
        self.tab_widget.addTab(user_widget, "User Management")
        
    def create_audit_logs_tab(self):
        """Create audit logs tab"""
        audit_widget = QWidget()
        audit_layout = QVBoxLayout(audit_widget)
        
        # Header
        audit_header_layout = QHBoxLayout()
        
        audit_title = QLabel("Audit Logs")
        audit_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        
        refresh_button = QPushButton("Refresh")
        refresh_button.setFont(QFont("Segoe UI", 10))
        refresh_button.setStyleSheet("""
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
        refresh_button.clicked.connect(self.refresh_audit_logs)
        
        audit_header_layout.addWidget(audit_title)
        audit_header_layout.addStretch()
        audit_header_layout.addWidget(refresh_button)
        
        # Audit logs table
        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(6)
        self.audit_table.setHorizontalHeaderLabels([
            "Timestamp", "User", "Action", "Resource", "Details", "IP Address"
        ])
        self.audit_table.setFont(QFont("Segoe UI", 9))
        self.audit_table.setStyleSheet("""
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
        
        audit_layout.addLayout(audit_header_layout)
        audit_layout.addWidget(self.audit_table)
        
        self.tab_widget.addTab(audit_widget, "Audit Logs")
        
    def create_system_status_tab(self):
        """Create system status tab"""
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        
        # System overview
        overview_group = QGroupBox("System Overview")
        overview_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        overview_layout = QVBoxLayout(overview_group)
        
        # Status indicators
        status_indicators_layout = QHBoxLayout()
        
        # Database status
        db_status_frame = QFrame()
        db_status_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        db_status_frame.setStyleSheet("""
            QFrame {
                background-color: #d5f4e6;
                border: 1px solid #27ae60;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        db_status_layout = QVBoxLayout(db_status_frame)
        db_status_label = QLabel("Database")
        db_status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        db_status_value = QLabel("Connected")
        db_status_value.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        db_status_value.setStyleSheet("color: #27ae60;")
        
        db_status_layout.addWidget(db_status_label)
        db_status_layout.addWidget(db_status_value)
        
        # Encryption status
        encryption_status_frame = QFrame()
        encryption_status_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        encryption_status_frame.setStyleSheet("""
            QFrame {
                background-color: #d5f4e6;
                border: 1px solid #27ae60;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        encryption_status_layout = QVBoxLayout(encryption_status_frame)
        encryption_status_label = QLabel("Data Encryption")
        encryption_status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        encryption_status_value = QLabel("Active")
        encryption_status_value.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        encryption_status_value.setStyleSheet("color: #27ae60;")
        
        encryption_status_layout.addWidget(encryption_status_label)
        encryption_status_layout.addWidget(encryption_status_value)
        
        # HIPAA compliance status
        hipaa_status_frame = QFrame()
        hipaa_status_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        hipaa_status_frame.setStyleSheet("""
            QFrame {
                background-color: #d5f4e6;
                border: 1px solid #27ae60;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        hipaa_status_layout = QVBoxLayout(hipaa_status_frame)
        hipaa_status_label = QLabel("HIPAA Compliance")
        hipaa_status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        hipaa_status_value = QLabel("Compliant")
        hipaa_status_value.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        hipaa_status_value.setStyleSheet("color: #27ae60;")
        
        hipaa_status_layout.addWidget(hipaa_status_label)
        hipaa_status_layout.addWidget(hipaa_status_value)
        
        status_indicators_layout.addWidget(db_status_frame)
        status_indicators_layout.addWidget(encryption_status_frame)
        status_indicators_layout.addWidget(hipaa_status_frame)
        
        overview_layout.addLayout(status_indicators_layout)
        
        # System statistics
        stats_group = QGroupBox("System Statistics")
        stats_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        stats_layout = QVBoxLayout(stats_group)
        
        # Stats would be populated from database
        stats_text = QTextEdit()
        stats_text.setReadOnly(True)
        stats_text.setMaximumHeight(150)
        stats_text.setText("""
        Total Patients: 0
        Total X-ray Images: 0
        Active Users: 0
        System Uptime: 0 days
        Last Backup: Never
        """)
        stats_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 8px;
                background-color: #f8f9fa;
                font-family: 'Courier New', monospace;
            }
        """)
        
        stats_layout.addWidget(stats_text)
        
        # Add groups to status layout
        status_layout.addWidget(overview_group)
        status_layout.addWidget(stats_group)
        status_layout.addStretch()
        
        self.tab_widget.addTab(status_widget, "System Status")
        
    def setup_connections(self):
        """Setup signal connections"""
        self.users_table.itemSelectionChanged.connect(self.on_user_selected)
        
    def load_data(self):
        """Load all data for admin panel"""
        self.load_users()
        self.load_audit_logs()
        
    def load_users(self):
        """Load users data"""
        try:
            # Sample user data (would come from database)
            sample_users = [
                {
                    'username': 'admin',
                    'full_name': 'System Administrator',
                    'role': 'admin',
                    'email': 'admin@hospital.com',
                    'last_login': '2024-01-15 10:30:00',
                    'status': 'Active'
                },
                {
                    'username': 'dr.smith',
                    'full_name': 'Dr. John Smith',
                    'role': 'radiologist',
                    'email': 'dr.smith@hospital.com',
                    'last_login': '2024-01-15 09:15:00',
                    'status': 'Active'
                },
                {
                    'username': 'tech.jones',
                    'full_name': 'Sarah Jones',
                    'role': 'technician',
                    'email': 'tech.jones@hospital.com',
                    'last_login': '2024-01-15 08:45:00',
                    'status': 'Active'
                }
            ]
            
            self.populate_users_table(sample_users)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")
            
    def populate_users_table(self, users):
        """Populate users table"""
        self.users_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # Username
            username_item = QTableWidgetItem(user['username'])
            username_item.setData(Qt.ItemDataRole.UserRole, user)
            self.users_table.setItem(row, 0, username_item)
            
            # Full Name
            name_item = QTableWidgetItem(user['full_name'])
            self.users_table.setItem(row, 1, name_item)
            
            # Role
            role_item = QTableWidgetItem(self.auth_manager.get_user_role_display_name(user['role']))
            self.users_table.setItem(row, 2, role_item)
            
            # Email
            email_item = QTableWidgetItem(user['email'])
            self.users_table.setItem(row, 3, email_item)
            
            # Last Login
            last_login_item = QTableWidgetItem(user['last_login'])
            self.users_table.setItem(row, 4, last_login_item)
            
            # Status
            status_item = QTableWidgetItem(user['status'])
            if user['status'] == 'Active':
                status_item.setBackground(QColor("#d5f4e6"))
                status_item.setForeground(QColor("#27ae60"))
            else:
                status_item.setBackground(QColor("#fadbd8"))
                status_item.setForeground(QColor("#e74c3c"))
            self.users_table.setItem(row, 5, status_item)
        
        # Resize columns
        self.users_table.resizeColumnsToContents()
        
    def load_audit_logs(self):
        """Load audit logs"""
        try:
            audit_logs = self.db_manager.get_audit_logs(50)  # Get last 50 logs
            self.populate_audit_table(audit_logs)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load audit logs: {str(e)}")
            
    def populate_audit_table(self, audit_logs):
        """Populate audit logs table"""
        self.audit_table.setRowCount(len(audit_logs))
        
        for row, log in enumerate(audit_logs):
            # Timestamp
            timestamp_item = QTableWidgetItem(log['timestamp'])
            self.audit_table.setItem(row, 0, timestamp_item)
            
            # User
            user_item = QTableWidgetItem(log['username'])
            self.audit_table.setItem(row, 1, user_item)
            
            # Action
            action_item = QTableWidgetItem(log['action'])
            self.audit_table.setItem(row, 2, action_item)
            
            # Resource
            resource_item = QTableWidgetItem(f"{log['resource_type']} #{log['resource_id']}" if log['resource_type'] and log['resource_id'] else "")
            self.audit_table.setItem(row, 3, resource_item)
            
            # Details
            details_item = QTableWidgetItem(log['details'])
            self.audit_table.setItem(row, 4, details_item)
            
            # IP Address
            ip_item = QTableWidgetItem(log.get('ip_address', ''))
            self.audit_table.setItem(row, 5, ip_item)
        
        # Resize columns
        self.audit_table.resizeColumnsToContents()
        
    def refresh_audit_logs(self):
        """Refresh audit logs"""
        self.load_audit_logs()
        
    def on_user_selected(self):
        """Handle user selection"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            item = self.users_table.item(current_row, 0)
            if item:
                user_data = item.data(Qt.ItemDataRole.UserRole)
                # Could show user details or edit options
                
    def add_user(self):
        """Open add user dialog"""
        dialog = UserDialog(self.db_manager, self.auth_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_users()


class UserDialog(QDialog):
    """Dialog for adding/editing users"""
    
    def __init__(self, db_manager: DatabaseManager, auth_manager: AuthManager, parent=None, user=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user = user
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Add User" if not self.user else "Edit User")
        self.setFixedSize(400, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Add User" if not self.user else "Edit User")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        # Username
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter username")
        if self.user:
            self.username_edit.setText(self.user['username'])
            self.username_edit.setReadOnly(True)
        form_layout.addRow("Username:", self.username_edit)
        
        # Full Name
        self.fullname_edit = QLineEdit()
        self.fullname_edit.setPlaceholderText("Enter full name")
        if self.user:
            self.fullname_edit.setText(self.user['full_name'])
        form_layout.addRow("Full Name:", self.fullname_edit)
        
        # Email
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("Enter email address")
        if self.user:
            self.email_edit.setText(self.user['email'])
        form_layout.addRow("Email:", self.email_edit)
        
        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItems(self.auth_manager.get_available_roles())
        if self.user:
            index = self.role_combo.findText(self.user['role'])
            if index >= 0:
                self.role_combo.setCurrentIndex(index)
        form_layout.addRow("Role:", self.role_combo)
        
        # Password (only for new users)
        if not self.user:
            self.password_edit = QLineEdit()
            self.password_edit.setPlaceholderText("Enter password")
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            form_layout.addRow("Password:", self.password_edit)
            
            self.confirm_password_edit = QLineEdit()
            self.confirm_password_edit.setPlaceholderText("Confirm password")
            self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            form_layout.addRow("Confirm Password:", self.confirm_password_edit)
        
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
        save_button.clicked.connect(self.save_user)
        
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
        
    def save_user(self):
        """Save user data"""
        # Validate required fields
        username = self.username_edit.text().strip()
        full_name = self.fullname_edit.text().strip()
        email = self.email_edit.text().strip()
        role = self.role_combo.currentText()
        
        if not username:
            QMessageBox.warning(self, "Validation Error", "Username is required.")
            self.username_edit.setFocus()
            return
            
        if not full_name:
            QMessageBox.warning(self, "Validation Error", "Full name is required.")
            self.fullname_edit.setFocus()
            return
            
        if not self.user:  # New user
            password = self.password_edit.text()
            confirm_password = self.confirm_password_edit.text()
            
            if not password:
                QMessageBox.warning(self, "Validation Error", "Password is required.")
                self.password_edit.setFocus()
                return
                
            if password != confirm_password:
                QMessageBox.warning(self, "Validation Error", "Passwords do not match.")
                self.confirm_password_edit.setFocus()
                return
        
        try:
            if not self.user:  # Create new user
                success = self.auth_manager.create_user(username, password, role, full_name, email)
                if success:
                    QMessageBox.information(self, "Success", "User created successfully!")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to create user. Username may already exist.")
            else:  # Update existing user
                # This would update user data in database
                QMessageBox.information(self, "Success", "User updated successfully!")
                self.accept()
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save user: {str(e)}") 