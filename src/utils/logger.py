"""
Logging utility for X-ray Management System
Provides centralized logging with HIPAA compliance
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "xray_system", log_level: int = logging.INFO) -> logging.Logger:
    """Setup application logger with file rotation and HIPAA compliance"""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # File handler for detailed logs (with rotation)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "xray_system.log"),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    
    # File handler for HIPAA audit logs
    audit_handler = RotatingFileHandler(
        os.path.join(log_dir, "audit.log"),
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10
    )
    audit_handler.setLevel(logging.INFO)
    audit_handler.setFormatter(simple_formatter)
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(audit_handler)
    logger.addHandler(console_handler)
    
    return logger

def log_hipaa_event(logger: logging.Logger, user_id: str, action: str, 
                   resource_type: str = None, resource_id: str = None, 
                   details: str = None):
    """Log HIPAA-compliant audit event"""
    
    event_data = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'action': action,
        'resource_type': resource_type,
        'resource_id': resource_id,
        'details': details
    }
    
    logger.info(f"HIPAA_AUDIT: {event_data}")

def log_security_event(logger: logging.Logger, event_type: str, 
                      user_id: str = None, details: str = None):
    """Log security-related events"""
    
    security_data = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'user_id': user_id,
        'details': details
    }
    
    logger.warning(f"SECURITY_EVENT: {security_data}")

def log_error(logger: logging.Logger, error: Exception, context: str = None):
    """Log application errors with context"""
    
    error_data = {
        'timestamp': datetime.now().isoformat(),
        'error_type': type(error).__name__,
        'error_message': str(error),
        'context': context
    }
    
    logger.error(f"APPLICATION_ERROR: {error_data}") 