# Installation Guide - Hospital X-ray Management System

This guide will help you install and configure the X-ray Management System on your Windows machine.

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 2GB free disk space
- **Display**: 1920x1080 minimum resolution
- **Network**: Internet connection for initial setup

### Software Requirements
- Python 3.8+ (Download from [python.org](https://www.python.org/downloads/))
- Git (Optional, for version control)

## Installation Steps

### 1. Clone or Download the Project

**Option A: Using Git (Recommended)**
```bash
git clone <repository-url>
cd xray-management-system
```

**Option B: Manual Download**
1. Download the project ZIP file
2. Extract to your desired location
3. Open command prompt in the project directory

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Run Initial Setup

```bash
# Test the installation
python test_app.py

# If all tests pass, you can run the application
python main.py
```

## Configuration

### 1. Database Setup
The system will automatically create the database on first run. The database file will be located at:
```
data/xray_system.db
```

### 2. Default Login Credentials
- **Username**: `admin`
- **Password**: `Admin123!`

**Important**: Change the default password immediately after first login!

### 3. Configuration Files
The system creates configuration files in:
```
config/settings.json
```

You can modify these settings through the admin panel or by editing the file directly.

## First Run Setup

### 1. Launch the Application
```bash
python main.py
```

### 2. Login with Default Credentials
- Username: `admin`
- Password: `Admin123!`

### 3. Initial Configuration
1. **Change Admin Password**: Go to Admin Panel → User Management
2. **Add Users**: Create accounts for radiologists and technicians
3. **Configure Equipment**: Add your X-ray equipment details
4. **Set Up Position Presets**: Configure common X-ray positions

## Directory Structure

```
xray-management-system/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── test_app.py            # Test suite
├── src/                   # Source code
│   ├── database/          # Database management
│   ├── security/          # Authentication & authorization
│   ├── ui/               # User interface components
│   └── utils/            # Utility functions
├── data/                 # Application data (created automatically)
│   ├── xray_system.db    # SQLite database
│   └── encryption.key    # Encryption key
├── config/               # Configuration files (created automatically)
│   └── settings.json     # Application settings
├── logs/                 # Log files (created automatically)
│   ├── xray_system.log   # Application logs
│   └── audit.log         # HIPAA audit logs
└── assets/               # Static assets (icons, images)
```

## Security Features

### HIPAA Compliance
- All patient data is encrypted at rest
- Comprehensive audit logging
- Role-based access control
- Session management
- Secure password handling

### Data Protection
- Patient data encryption using Fernet (AES-128)
- Secure key management
- Audit trail for all data access
- Automatic session timeout

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure you're in the correct directory
cd xray-management-system

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**2. Database Errors**
```bash
# Remove existing database and restart
rm data/xray_system.db
python main.py
```

**3. Permission Errors**
- Run as Administrator if needed
- Check file permissions in the project directory

**4. PyQt6 Installation Issues**
```bash
# Try alternative installation
pip install PyQt6-Qt6 PyQt6-sip
```

### Log Files
Check the following log files for detailed error information:
- `logs/xray_system.log` - Application logs
- `logs/audit.log` - Security audit logs

## Development Setup

### For Developers
1. Install development dependencies:
```bash
pip install -r requirements.txt
pip install black flake8 pytest
```

2. Run tests:
```bash
python test_app.py
```

3. Code formatting:
```bash
black src/
flake8 src/
```

## Backup and Recovery

### Database Backup
The system automatically creates backups in the `data/` directory. For manual backup:

```bash
# Copy the database file
cp data/xray_system.db backup/xray_system_backup_$(date +%Y%m%d).db
```

### Configuration Backup
```bash
# Backup configuration
cp config/settings.json backup/settings_backup_$(date +%Y%m%d).json
```

## Support

### Getting Help
1. Check the log files for error details
2. Review the README.md for feature documentation
3. Run the test suite to verify installation
4. Contact system administrator for technical support

### System Requirements Verification
Run the test suite to verify your system meets all requirements:
```bash
python test_app.py
```

## Updates

### Updating the System
1. Backup your data and configuration
2. Download the latest version
3. Install new dependencies: `pip install -r requirements.txt`
4. Run the test suite: `python test_app.py`
5. Start the application: `python main.py`

## License

This software is licensed for hospital use only. Please ensure compliance with local healthcare regulations and data protection laws.

---

**Note**: This system is designed for medical use and contains sensitive patient data. Always follow your organization's security policies and HIPAA compliance requirements. 
