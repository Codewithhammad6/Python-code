"""
Configuration utility for X-ray Management System
Manages application settings and configuration
"""

import json
import os
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        self.config_file = config_file
        self.config_data = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "database": {
                "path": "data/xray_system.db",
                "backup_enabled": True,
                "backup_interval_hours": 24
            },
            "security": {
                "session_timeout_minutes": 30,
                "max_login_attempts": 3,
                "password_min_length": 8,
                "require_special_chars": True
            },
            "dicom": {
                "supported_formats": [".dcm", ".dicom"],
                "max_file_size_mb": 100,
                "auto_import_enabled": True
            },
            "ui": {
                "theme": "default",
                "language": "en",
                "auto_save_interval_seconds": 300
            },
            "logging": {
                "level": "INFO",
                "max_file_size_mb": 10,
                "backup_count": 5
            },
            "equipment": {
                "scanner_check_interval_seconds": 30,
                "maintenance_reminder_days": 7
            }
        }
        
        # Create config directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Load existing config or create default
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with default config to ensure all keys exist
                    return self.merge_configs(default_config, config)
            except Exception as e:
                print(f"Error loading config: {e}")
                return default_config
        else:
            # Create default config file
            self.save_config(default_config)
            return default_config
    
    def merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Merge user config with default config"""
        result = default.copy()
        
        def merge_dicts(d1, d2):
            for key, value in d2.items():
                if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                    merge_dicts(d1[key], value)
                else:
                    d1[key] = value
        
        merge_dicts(result, user)
        return result
    
    def save_config(self, config_data: Optional[Dict] = None):
        """Save configuration to file"""
        if config_data is None:
            config_data = self.config_data
            
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)"""
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value by key (supports dot notation)"""
        keys = key.split('.')
        config = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
        
        # Save to file
        self.save_config()
    
    def get_database_path(self) -> str:
        """Get database file path"""
        return self.get("database.path", "data/xray_system.db")
    
    def get_session_timeout(self) -> int:
        """Get session timeout in minutes"""
        return self.get("security.session_timeout_minutes", 30)
    
    def get_max_login_attempts(self) -> int:
        """Get maximum login attempts"""
        return self.get("security.max_login_attempts", 3)
    
    def get_supported_dicom_formats(self) -> list:
        """Get supported DICOM file formats"""
        return self.get("dicom.supported_formats", [".dcm", ".dicom"])
    
    def get_max_dicom_file_size(self) -> int:
        """Get maximum DICOM file size in MB"""
        return self.get("dicom.max_file_size_mb", 100)
    
    def get_log_level(self) -> str:
        """Get logging level"""
        return self.get("logging.level", "INFO")
    
    def get_theme(self) -> str:
        """Get UI theme"""
        return self.get("ui.theme", "default")
    
    def get_language(self) -> str:
        """Get UI language"""
        return self.get("ui.language", "en")
    
    def is_backup_enabled(self) -> bool:
        """Check if database backup is enabled"""
        return self.get("database.backup_enabled", True)
    
    def get_backup_interval(self) -> int:
        """Get backup interval in hours"""
        return self.get("database.backup_interval_hours", 24)
    
    def get_scanner_check_interval(self) -> int:
        """Get scanner status check interval in seconds"""
        return self.get("equipment.scanner_check_interval_seconds", 30)
    
    def get_maintenance_reminder_days(self) -> int:
        """Get maintenance reminder days"""
        return self.get("equipment.maintenance_reminder_days", 7)
    
    def update_database_settings(self, path: str = None, backup_enabled: bool = None, 
                               backup_interval: int = None):
        """Update database configuration"""
        if path:
            self.set("database.path", path)
        if backup_enabled is not None:
            self.set("database.backup_enabled", backup_enabled)
        if backup_interval:
            self.set("database.backup_interval_hours", backup_interval)
    
    def update_security_settings(self, session_timeout: int = None, 
                               max_attempts: int = None, min_password_length: int = None):
        """Update security configuration"""
        if session_timeout:
            self.set("security.session_timeout_minutes", session_timeout)
        if max_attempts:
            self.set("security.max_login_attempts", max_attempts)
        if min_password_length:
            self.set("security.password_min_length", min_password_length)
    
    def update_ui_settings(self, theme: str = None, language: str = None):
        """Update UI configuration"""
        if theme:
            self.set("ui.theme", theme)
        if language:
            self.set("ui.language", language)
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        default_config = {
            "database": {
                "path": "data/xray_system.db",
                "backup_enabled": True,
                "backup_interval_hours": 24
            },
            "security": {
                "session_timeout_minutes": 30,
                "max_login_attempts": 3,
                "password_min_length": 8,
                "require_special_chars": True
            },
            "dicom": {
                "supported_formats": [".dcm", ".dicom"],
                "max_file_size_mb": 100,
                "auto_import_enabled": True
            },
            "ui": {
                "theme": "default",
                "language": "en",
                "auto_save_interval_seconds": 300
            },
            "logging": {
                "level": "INFO",
                "max_file_size_mb": 10,
                "backup_count": 5
            },
            "equipment": {
                "scanner_check_interval_seconds": 30,
                "maintenance_reminder_days": 7
            }
        }
        
        self.config_data = default_config
        self.save_config() 