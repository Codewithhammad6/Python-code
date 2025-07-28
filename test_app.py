#!/usr/bin/env python3
"""
Test script for X-ray Management System
Verifies basic functionality and startup
"""

import sys
import os

# Add src to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from database.database_manager import DatabaseManager
        print("✓ DatabaseManager imported successfully")
        
        from security.auth_manager import AuthManager
        print("✓ AuthManager imported successfully")
        
        from utils.logger import setup_logger
        print("✓ Logger utility imported successfully")
        
        from utils.config import Config
        print("✓ Config utility imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\nTesting database...")
    
    try:
        from database.database_manager import DatabaseManager
        
        db_manager = DatabaseManager("test_data/test.db")
        db_manager.initialize_database()
        print("✓ Database initialized successfully")
        
        # Clean up test database
        if os.path.exists("test_data/test.db"):
            os.remove("test_data/test.db")
        if os.path.exists("test_data/encryption.key"):
            os.remove("test_data/encryption.key")
        if os.path.exists("test_data"):
            os.rmdir("test_data")
            
        return True
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def test_config():
    """Test configuration system"""
    print("\nTesting configuration...")
    
    try:
        from utils.config import Config
        
        config = Config("test_config/test_settings.json")
        print("✓ Configuration loaded successfully")
        
        # Test getting values
        db_path = config.get_database_path()
        print(f"✓ Database path: {db_path}")
        
        # Test setting values
        config.set("test.key", "test_value")
        test_value = config.get("test.key")
        print(f"✓ Config set/get: {test_value}")
        
        # Clean up test config
        if os.path.exists("test_config/test_settings.json"):
            os.remove("test_config/test_settings.json")
        if os.path.exists("test_config"):
            os.rmdir("test_config")
            
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_logger():
    """Test logging system"""
    print("\nTesting logger...")
    
    try:
        from utils.logger import setup_logger
        
        logger = setup_logger("test_logger")
        logger.info("Test log message")
        print("✓ Logger created and message logged successfully")
        
        # Clean up test logs
        if os.path.exists("logs/xray_system.log"):
            os.remove("logs/xray_system.log")
        if os.path.exists("logs/audit.log"):
            os.remove("logs/audit.log")
        if os.path.exists("logs"):
            os.rmdir("logs")
            
        return True
    except Exception as e:
        print(f"✗ Logger error: {e}")
        return False

def test_auth():
    """Test authentication system"""
    print("\nTesting authentication...")
    
    try:
        from security.auth_manager import AuthManager
        
        auth_manager = AuthManager("test_data/test_auth.db")
        print("✓ AuthManager created successfully")
        
        # Test role display names
        role_name = auth_manager.get_user_role_display_name("admin")
        print(f"✓ Role display name: {role_name}")
        
        # Clean up test database
        if os.path.exists("test_data/test_auth.db"):
            os.remove("test_data/test_auth.db")
        if os.path.exists("test_data"):
            os.rmdir("test_data")
            
        return True
    except Exception as e:
        print(f"✗ Authentication error: {e}")
        return False

def main():
    """Run all tests"""
    print("X-ray Management System - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database,
        test_config,
        test_logger,
        test_auth
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The application should work correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 