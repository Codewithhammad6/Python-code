# 🏥 Hospital X-ray Management System - Quick Start

## 🚀 How to Run the Application

### Method 1: Simple Launcher (Recommended)
```bash
python launch_simple.py
```

### Method 2: Windows Batch File
Double-click `start_app.bat`

### Method 3: Original Launcher
```bash
python main.py
```

## 🔐 Default Login Credentials

**Username:** `admin`  
**Password:** `Admin123!`

## 📋 What You'll See

1. **Login Window**: A secure login form with modern UI
2. **Main Application**: Tabbed interface with:
   - Patient Management
   - X-ray Viewer
   - Equipment Tracking
   - Admin Panel

## 🛠️ System Requirements

- Python 3.8 or higher
- Windows 10/11 (tested)
- 4GB RAM minimum
- 2GB free disk space

## 📦 Dependencies

All required packages are automatically installed:
- PyQt6 (GUI framework)
- pydicom (DICOM image support)
- Pillow (Image processing)
- cryptography (Data encryption)
- bcrypt (Password hashing)

## 🔧 Troubleshooting

### If the application doesn't start:
1. Make sure Python is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Try the simple launcher: `python launch_simple.py`

### If login doesn't work:
1. Use exact credentials: `admin` / `Admin123!`
2. Check that the database was created in the `data/` folder

### If GUI doesn't appear:
1. Make sure you're running on a system with display
2. Try running in a terminal/command prompt
3. Check Windows display settings

## 📁 Project Structure

```
xray-management-system/
├── launch_simple.py      # Simple launcher (use this)
├── start_app.bat         # Windows batch file
├── main.py              # Original launcher
├── src/                 # Source code
├── data/                # Database files
├── logs/                # Log files
└── config/              # Configuration
```

## 🎯 Features Available

✅ **Patient Management**: Add, search, and manage patient records  
✅ **X-ray Viewer**: View and annotate DICOM images  
✅ **Equipment Tracking**: Monitor X-ray equipment status  
✅ **User Management**: Admin panel for user management  
✅ **Secure Login**: HIPAA-compliant authentication  
✅ **Audit Logging**: Complete activity tracking  

## 🆘 Need Help?

1. Check the logs in the `logs/` folder
2. Run `python test_login.py` to test login functionality
3. Run `python test_app.py` for comprehensive testing

---

**🎉 The application is ready to use!** 