"""
Login Window for X-ray Management System
Provides secure user authentication interface
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QGridLayout, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon, QPalette, QColor

from security.auth_manager import AuthManager

class LoginWindow(QWidget):
    """Secure login window with modern UI"""
    
    # Signals
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    
    def __init__(self, auth_manager: AuthManager):
        super().__init__()
        self.auth_manager = auth_manager
        self.setup_ui()
        self.setup_connections()
        
    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Hospital X-ray Management System - Login")
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        
        # Center window on screen
        self.center_window()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo/Header
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # App title
        title_label = QLabel("Hospital X-ray Management System")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        
        # Subtitle
        subtitle_label = QLabel("Secure Login")
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        
        # Login form
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Username field
        username_label = QLabel("Username:")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        username_label.setStyleSheet("color: #2c3e50;")
        
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Enter your username")
        self.username_edit.setFont(QFont("Segoe UI", 10))
        self.username_edit.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 12px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
                color: #2c3e50;
            }
        """)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        password_label.setStyleSheet("color: #2c3e50;")
        
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Enter your password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFont(QFont("Segoe UI", 10))
        self.password_edit.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ecf0f1;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 12px;
                color: #2c3e50;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
                color: #2c3e50;
            }
        """)
        
        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show password")
        self.show_password_checkbox.setFont(QFont("Segoe UI", 9))
        self.show_password_checkbox.setStyleSheet("color: #7f8c8d;")
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add widgets to form layout
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.show_password_checkbox)
        form_layout.addWidget(self.login_button)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #e74c3c; font-size: 11px;")
        self.status_label.setWordWrap(True)
        
        # Add all to main layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(form_frame)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Set window style
        self.setStyleSheet("""
            QWidget {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.login_button.clicked.connect(self.attempt_login)
        self.password_edit.returnPressed.connect(self.attempt_login)
        self.username_edit.returnPressed.connect(self.password_edit.setFocus)
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        
    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def toggle_password_visibility(self, checked: bool):
        """Toggle password field visibility"""
        if checked:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            
    def attempt_login(self):
        """Attempt to authenticate user"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        # Validate input
        if not username:
            self.show_error("Please enter a username")
            self.username_edit.setFocus()
            return
            
        if not password:
            self.show_error("Please enter a password")
            self.password_edit.setFocus()
            return
        
        # Disable login button and show loading state
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        self.clear_error()
        
        # Attempt authentication
        user_data = self.auth_manager.authenticate_user(username, password)
        
        if user_data:
            # Success - emit signal with user data
            self._login_successful = True  # Flag to prevent exit dialog
            self.login_successful.emit(user_data)
        else:
            # Failed - show error and reset
            self.show_error("Invalid username or password")
            self.password_edit.clear()
            self.password_edit.setFocus()
            self.login_button.setEnabled(True)
            self.login_button.setText("Login")
            
    def show_error(self, message: str):
        """Show error message"""
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: #e74c3c; font-size: 11px;")
        
    def clear_error(self):
        """Clear error message"""
        self.status_label.setText("")
        
    def closeEvent(self, event):
        """Handle window close event"""
        # Only show exit dialog if this is a manual close attempt
        # (not when login is successful and window is being closed programmatically)
        if hasattr(self, '_login_successful') and self._login_successful:
            event.accept()
            return
            
        reply = QMessageBox.question(
            self, 'Exit Application',
            'Are you sure you want to exit the X-ray Management System?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
            sys.exit(0)
        else:
            event.ignore() 