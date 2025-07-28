# 🚀 Startup Guide - X-ray Management System

## Quick Start (Choose One Method)

### **Method 1: Simple Launcher (Recommended)**
```bash
python launch.py
```

### **Method 2: Windows Batch File**
```bash
# Double-click or run:
start_xray_system.bat
```

### **Method 3: Quick Start Script**
```bash
python quick_start.py
```

### **Method 4: Direct Launch**
```bash
python main.py
```

## 🔧 Prerequisites Check

### **1. Python Version**
```bash
python --version
# Should show Python 3.8 or higher
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Test Installation**
```bash
python test_app.py
```

## 🎯 First Time Setup

### **Step 1: Install Python**
- Download from: https://python.org
- Make sure to check "Add Python to PATH" during installation

### **Step 2: Open Terminal/Command Prompt**
- Navigate to the project folder
- You should see: `main.py`, `requirements.txt`, `src/` folder

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Launch Application**
```bash
python launch.py
```

### **Step 5: Login**
- **Username**: `admin`
- **Password**: `Admin123!`

## 🔍 Troubleshooting Common Issues

### **Issue 1: "python is not recognized"**
**Solution:**
```bash
# Try these commands:
python3 --version
py --version
python3.8 --version

# If none work, reinstall Python and check "Add to PATH"
```

### **Issue 2: "ModuleNotFoundError: No module named 'PyQt6'"**
**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# If that fails:
pip install PyQt6 pydicom Pillow cryptography bcrypt numpy scipy
```

### **Issue 3: "ImportError: cannot import name"**
**Solution:**
```bash
# Clean install
pip uninstall PyQt6 pydicom Pillow cryptography bcrypt
pip install -r requirements.txt
```

### **Issue 4: "Permission denied"**
**Solution:**
```bash
# Windows: Run as Administrator
# Mac/Linux: Use sudo
sudo pip install -r requirements.txt
```

### **Issue 5: "Database Error"**
**Solution:**
```bash
# Remove existing database and restart
rm data/xray_system.db  # Mac/Linux
del data\xray_system.db  # Windows
python launch.py
```

## 📋 Step-by-Step Verification

### **1. Check Python Installation**
```bash
python --version
# Should show: Python 3.8.x or higher
```

### **2. Check Current Directory**
```bash
# Windows:
dir
# Should show: main.py, requirements.txt, src/

# Mac/Linux:
ls
# Should show: main.py, requirements.txt, src/
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
# Should complete without errors
```

### **4. Run Test Suite**
```bash
python test_app.py
# Should show: "All tests passed!"
```

### **5. Launch Application**
```bash
python launch.py
# Should show login window
```

## 🖥️ Platform-Specific Instructions

### **Windows**
1. **Install Python**: Download from python.org
2. **Open Command Prompt**: Press Win+R, type `cmd`
3. **Navigate to project**: `cd path\to\xray-management-system`
4. **Install dependencies**: `pip install -r requirements.txt`
5. **Launch**: `python launch.py` or double-click `start_xray_system.bat`

### **macOS**
1. **Install Python**: `brew install python` or download from python.org
2. **Open Terminal**: Applications → Utilities → Terminal
3. **Navigate to project**: `cd path/to/xray-management-system`
4. **Install dependencies**: `pip3 install -r requirements.txt`
5. **Launch**: `python3 launch.py`

### **Linux**
1. **Install Python**: `sudo apt install python3 python3-pip` (Ubuntu/Debian)
2. **Open Terminal**: Ctrl+Alt+T
3. **Navigate to project**: `cd path/to/xray-management-system`
4. **Install dependencies**: `pip3 install -r requirements.txt`
5. **Launch**: `python3 launch.py`

## 🔧 Advanced Setup

### **Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Launch application
python launch.py
```

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Run tests
python test_app.py

# Format code
black src/
```

## 📱 What You'll See

### **Login Window**
- Clean, professional interface
- Username and password fields
- "Show password" checkbox
- Login button

### **Main Application**
- **Patient Management Tab**: Add/search patients
- **X-ray Viewer Tab**: View and annotate DICOM images
- **Equipment Tracking Tab**: Monitor scanner status
- **Admin Panel Tab**: System administration (admin only)

### **Features Available**
- ✅ Patient record management
- ✅ DICOM image viewing with zoom/pan
- ✅ Image annotations and measurements
- ✅ Equipment status monitoring
- ✅ User management and permissions
- ✅ Audit logging for HIPAA compliance

## 🆘 Getting Help

### **Check Log Files**
- `logs/xray_system.log` - Application logs
- `logs/audit.log` - Security audit logs

### **Run Test Suite**
```bash
python test_app.py
```

### **Common Commands**
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Install specific package
pip install package_name

# Update pip
python -m pip install --upgrade pip
```

## ✅ Success Indicators

When everything is working correctly, you should see:

1. **No error messages** during startup
2. **Login window appears** with professional styling
3. **Login works** with admin/admin123!
4. **Main application loads** with tabbed interface
5. **All tabs are accessible** and functional
6. **Database is created** in `data/` folder
7. **Logs are generated** in `logs/` folder

## 🎉 You're Ready!

Once you see the main application window, you're ready to:
- Add patients
- Import DICOM images
- Configure equipment
- Set up user accounts
- Start using the system in your hospital environment

**Remember**: Change the default admin password immediately after first login! 
