#!/usr/bin/env python3
"""
Quick Start Script for X-ray Management System
Provides easy launch with environment setup
"""

import sys
import os
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'PyQt6', 'pydicom', 'Pillow', 'cryptography', 
        'bcrypt', 'numpy', 'scipy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def setup_environment():
    """Setup the environment for the application"""
    print("Setting up environment...")
    
    # Add src to Python path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, 'src')
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    
    # Create necessary directories
    directories = ['data', 'config', 'logs', 'assets/icons']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Environment setup complete")

def launch_application():
    """Launch the main application"""
    try:
        print("\n🚀 Launching X-ray Management System...")
        
        # Import and run the main application
        from main import main
        main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Application error: {e}")
        return False
    
    return True

def main():
    """Main quick start function"""
    print("🏥 Hospital X-ray Management System")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check dependencies
    print("\nChecking dependencies...")
    if not check_dependencies():
        return 1
    
    # Setup environment
    setup_environment()
    
    # Launch application
    if not launch_application():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 