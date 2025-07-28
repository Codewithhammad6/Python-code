#!/usr/bin/env python3
"""
Simple Launcher for X-ray Management System
Works on all platforms (Windows, Mac, Linux)
"""

import sys
import os
import subprocess

def main():
    """Main launcher function"""
    print("🏥 Hospital X-ray Management System")
    print("=" * 50)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if Python is available
    try:
        import PyQt6
        print("✅ PyQt6 is installed")
    except ImportError:
        print("❌ PyQt6 not found. Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Please run: pip install -r requirements.txt")
            return 1
    
    # Check if src directory exists
    if not os.path.exists("src"):
        print("❌ src directory not found")
        return 1
    
    # Add src to Python path
    src_path = os.path.join(script_dir, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Create necessary directories
    directories = ['data', 'config', 'logs', 'assets/icons']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # Try to import and run the main application
    try:
        print("🚀 Starting application...")
        from main import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Application error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 