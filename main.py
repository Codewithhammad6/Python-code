#!/usr/bin/env python3
"""
Hospital X-ray Room Management System
Main Application Entry Point
"""

import sys
import os

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, QTranslator, QLocale
from PyQt6.QtGui import QIcon, QFont

from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from database.database_manager import DatabaseManager
from utils.logger import setup_logger
from utils.config import Config
from security.auth_manager import AuthManager

class XRayManagementSystem:
    """Main application class for the X-ray Management System"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_application()
        self.logger = setup_logger()
        self.config = Config()
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager()
        
    def setup_application(self):
        """Configure application settings and appearance"""
        self.app.setApplicationName("Hospital X-ray Management System")
        self.app.setApplicationVersion("1.0.0")
        self.app.setOrganizationName("Hospital X-ray Department")
        
        # Set application icon
        icon_path = os.path.join("assets", "icons", "app_icon.png")
        if os.path.exists(icon_path):
            self.app.setWindowIcon(QIcon(icon_path))
        
        # Set application style
        self.app.setStyle('Fusion')
        
        # Set default font
        font = QFont("Segoe UI", 9)
        self.app.setFont(font)
        
        # Enable high DPI scaling (only for older Qt versions)
        try:
            self.app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
            self.app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        except AttributeError:
            # These attributes are deprecated in newer Qt versions
            pass
        
    def initialize_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            self.db_manager.initialize_database()
            self.logger.info("Database initialized successfully")
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            QMessageBox.critical(None, "Database Error", 
                               f"Failed to initialize database: {str(e)}")
            return False
        return True
    
    def show_login(self):
        """Display login window"""
        self.login_window = LoginWindow(self.auth_manager)
        self.login_window.login_successful.connect(self.show_main_window)
        self.login_window.show()
        
    def show_main_window(self, user_data):
        """Display main application window after successful login"""
        self.login_window.close()
        self.main_window = MainWindow(user_data, self.db_manager, self.auth_manager)
        self.main_window.show()
        
    def run(self):
        """Start the application"""
        try:
            # Initialize database
            if not self.initialize_database():
                return 1
                
            # Show login window
            self.show_login()
            
            # Start event loop
            return self.app.exec()
            
        except Exception as e:
            self.logger.error(f"Application startup failed: {e}")
            QMessageBox.critical(None, "Startup Error", 
                               f"Application failed to start: {str(e)}")
            return 1

def main():
    """Main entry point"""
    try:
        app = XRayManagementSystem()
        sys.exit(app.run())
    except KeyboardInterrupt:
        print("\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 