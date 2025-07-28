#!/usr/bin/env python3
"""
Simple launcher for X-ray Management System
"""

import sys
import os
import traceback

def main():
    """Main launcher function"""
    try:
        # Add src to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(current_dir, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Import required modules
        from PyQt6.QtWidgets import QApplication
        from database.database_manager import DatabaseManager
        from security.auth_manager import AuthManager
        from ui.login_window import LoginWindow
        from ui.main_window import MainWindow
        
        print("🏥 Hospital X-ray Management System")
        print("=" * 50)
        print("Starting application...")
        
        # Create application
        app = QApplication(sys.argv)
        app.setApplicationName("Hospital X-ray Management System")
        
        # Initialize database
        print("Initializing database...")
        db_manager = DatabaseManager()
        db_manager.initialize_database()
        print("✅ Database initialized")
        
        # Create auth manager
        auth_manager = AuthManager()
        
        # Create login window
        print("Creating login window...")
        login_window = LoginWindow(auth_manager)
        
        # Connect login success to main window
        def on_login_success(user_data):
            print(f"✅ Login successful for user: {user_data['username']}")
            login_window._login_successful = True  # Prevent exit dialog
            login_window.close()
            main_window = MainWindow(user_data, db_manager, auth_manager)
            main_window.show()
            print("✅ Main window opened")
        
        login_window.login_successful.connect(on_login_success)
        
        # Show login window
        login_window.show()
        print("✅ Login window displayed")
        print("\n📋 Login Credentials:")
        print("Username: admin")
        print("Password: Admin123!")
        print("\n🎯 Application is ready!")
        
        # Start event loop
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\n🔍 Full error details:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 