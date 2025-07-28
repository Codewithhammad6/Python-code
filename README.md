# Hospital X-ray Room Management System

A comprehensive PC-based software solution for hospital X-ray rooms with DICOM compatibility, patient record management, and HIPAA compliance.

## Features

- **Patient Record Integration**: Fetch and display patient data with HL7/FHIR compatibility
- **DICOM Image Viewer**: Full DICOM support with zoom, pan, and annotation tools
- **Position Presets**: Quick-select templates for common X-ray positions
- **Usage Logs**: Track scanner usage, radiographer notes, and timestamps
- **User Role Management**: Secure login for radiologists, technicians, and admins
- **HIPAA/GDPR Compliance**: Encrypted data storage and secure access controls
- **Offline Mode**: Works without network connection
- **Equipment Tracking**: Monitor scanner status and maintenance logs

## Installation

1. Clone the repository
2. Install Python 3.8 or higher
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:
```bash
python main.py
```

## System Requirements

- Windows 10/11
- Python 3.8+
- 4GB RAM minimum
- 2GB free disk space
- DICOM-compatible X-ray scanner

## Security

- All patient data is encrypted at rest
- Role-based access control
- Audit logging for all actions
- HIPAA/GDPR compliant data handling

## License

Medical Software License - For Hospital Use Only 