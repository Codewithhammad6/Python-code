"""
Main Window for X-ray Management System
Provides the primary interface for patient management and X-ray operations
"""

import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QPushButton, QMessageBox,
                             QStatusBar, QMenuBar, QMenu, QToolBar,
                             QSplitter, QFrame, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QAction

from ui.patient_management import PatientManagementWidget
from ui.xray_viewer import XRayViewerWidget
from ui.equipment_tracking import EquipmentTrackingWidget
from ui.admin_panel import AdminPanelWidget
from database.database_manager import DatabaseManager
from security.auth_manager import AuthManager

class MainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self, user_data: dict, db_manager: DatabaseManager, auth_manager: AuthManager):
        super().__init__()
        self.user_data = user_data
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.current_patient = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_bar()
        self.setup_connections()
        
        # Log user login
        self.db_manager.add_usage_log(
            user_data['id'], 
            "LOGIN", 
            f"User {user_data['username']} logged in"
        )
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("Hospital X-ray Management System")
        self.setMinimumSize(1200, 800)
        
        # Center window on screen
        self.center_window()
        
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header with user info
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # User info
        user_info = QLabel(f"Welcome, {self.user_data['full_name']} ({self.auth_manager.get_user_role_display_name(self.user_data['role'])})")
        user_info.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        user_info.setStyleSheet("color: white;")
        
        # Logout button
        logout_button = QPushButton("Logout")
        logout_button.setFont(QFont("Segoe UI", 10))
        logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_button.clicked.connect(self.logout)
        
        header_layout.addWidget(user_info)
        header_layout.addStretch()
        header_layout.addWidget(logout_button)
        
        # Tab widget for main functionality
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
        
        # Create tabs based on user role
        self.create_tabs()
        
        # Add widgets to main layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.tab_widget)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
    def create_tabs(self):
        """Create tabs based on user permissions"""
        # Patient Management tab (all users)
        self.patient_widget = PatientManagementWidget(self.db_manager, self.auth_manager)
        self.tab_widget.addTab(self.patient_widget, "Patient Management")
        
        # X-ray Viewer tab (all users)
        self.xray_widget = XRayViewerWidget(self.db_manager, self.auth_manager)
        self.tab_widget.addTab(self.xray_widget, "X-ray Viewer")
        
        # Equipment Tracking tab (all users)
        self.equipment_widget = EquipmentTrackingWidget(self.db_manager, self.auth_manager)
        self.tab_widget.addTab(self.equipment_widget, "Equipment Tracking")
        
        # Admin Panel tab (admin only)
        if self.auth_manager.has_permission('system_admin'):
            self.admin_widget = AdminPanelWidget(self.db_manager, self.auth_manager)
            self.tab_widget.addTab(self.admin_widget, "Admin Panel")
        
        # Connect patient selection signal
        self.patient_widget.patient_selected.connect(self.on_patient_selected)
        
    def setup_menu(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        # New patient action
        new_patient_action = QAction('&New Patient', self)
        new_patient_action.setShortcut('Ctrl+N')
        new_patient_action.triggered.connect(self.new_patient)
        file_menu.addAction(new_patient_action)
        
        # Open patient action
        open_patient_action = QAction('&Open Patient', self)
        open_patient_action.setShortcut('Ctrl+O')
        open_patient_action.triggered.connect(self.open_patient)
        file_menu.addAction(open_patient_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('&Tools')
        
        # Equipment status action
        equipment_action = QAction('&Equipment Status', self)
        equipment_action.triggered.connect(self.show_equipment_status)
        tools_menu.addAction(equipment_action)
        
        # Usage logs action
        logs_action = QAction('&Usage Logs', self)
        logs_action.triggered.connect(self.show_usage_logs)
        tools_menu.addAction(logs_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        # About action
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_toolbar(self):
        """Setup application toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # New patient button
        new_patient_action = QAction('New Patient', self)
        new_patient_action.triggered.connect(self.new_patient)
        toolbar.addAction(new_patient_action)
        
        toolbar.addSeparator()
        
        # Equipment status button
        equipment_action = QAction('Equipment', self)
        equipment_action.triggered.connect(self.show_equipment_status)
        toolbar.addAction(equipment_action)
        
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Show current user and time
        self.status_bar.showMessage(f"Logged in as: {self.user_data['username']} | Role: {self.auth_manager.get_user_role_display_name(self.user_data['role'])}")
        
        # Timer to update status bar
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status_bar)
        self.status_timer.start(60000)  # Update every minute
        
    def setup_connections(self):
        """Setup signal connections"""
        # Connect tab changes
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
    def center_window(self):
        """Center the window on the screen"""
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def on_patient_selected(self, patient_data):
        """Handle patient selection from patient management tab"""
        self.current_patient = patient_data
        self.xray_widget.load_patient_xrays(patient_data['id'])
        self.status_bar.showMessage(f"Current patient: {patient_data.get('name', 'Unknown')} ({patient_data.get('patient_id', 'N/A')})")
        
    def on_tab_changed(self, index):
        """Handle tab changes"""
        tab_name = self.tab_widget.tabText(index)
        self.status_bar.showMessage(f"Current tab: {tab_name}")
        
    def new_patient(self):
        """Open new patient dialog"""
        self.tab_widget.setCurrentIndex(0)  # Switch to patient management tab
        self.patient_widget.new_patient()
        
    def open_patient(self):
        """Open patient search dialog"""
        self.tab_widget.setCurrentIndex(0)  # Switch to patient management tab
        self.patient_widget.search_patients()
        
    def show_equipment_status(self):
        """Show equipment status"""
        self.tab_widget.setCurrentIndex(2)  # Switch to equipment tracking tab
        
    def show_usage_logs(self):
        """Show usage logs"""
        if self.auth_manager.has_permission('view_usage_logs'):
            # This would open a usage logs dialog
            QMessageBox.information(self, "Usage Logs", "Usage logs feature coming soon...")
        else:
            QMessageBox.warning(self, "Access Denied", "You don't have permission to view usage logs.")
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About", 
                         "Hospital X-ray Management System\n\n"
                         "Version 1.0.0\n"
                         "A comprehensive solution for X-ray room management\n\n"
                         "Features:\n"
                         "• Patient record management\n"
                         "• DICOM image viewing\n"
                         "• Equipment tracking\n"
                         "• HIPAA compliant data handling")
        
    def update_status_bar(self):
        """Update status bar with current time"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_bar.showMessage(f"Logged in as: {self.user_data['username']} | Role: {self.auth_manager.get_user_role_display_name(self.user_data['role'])} | Time: {current_time}")
        
    def logout(self):
        """Logout current user"""
        reply = QMessageBox.question(
            self, 'Logout',
            'Are you sure you want to logout?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Log logout
            self.db_manager.add_usage_log(
                self.user_data['id'], 
                "LOGOUT", 
                f"User {self.user_data['username']} logged out"
            )
            
            self.auth_manager.logout()
            self.close()
            
    def closeEvent(self, event):
        """Handle window close event"""
        reply = QMessageBox.question(
            self, 'Exit Application',
            'Are you sure you want to exit the X-ray Management System?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Log logout
            self.db_manager.add_usage_log(
                self.user_data['id'], 
                "LOGOUT", 
                f"User {self.user_data['username']} logged out (application closed)"
            )
            event.accept()
        else:
            event.ignore() 