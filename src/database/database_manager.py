"""
Database Manager for X-ray Management System
Handles all database operations with HIPAA compliance
"""

import sqlite3
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from cryptography.fernet import Fernet
import json

class DatabaseManager:
    """Manages database operations with encryption for HIPAA compliance"""
    
    def __init__(self, db_path: str = "data/xray_system.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.encryption_key = self._load_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
    def _load_or_create_key(self) -> bytes:
        """Load existing encryption key or create new one"""
        key_file = "data/encryption.key"
        os.makedirs(os.path.dirname(key_file), exist_ok=True)
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode())
    
    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data).decode()
    
    def initialize_database(self):
        """Initialize database and create all tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Patients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT UNIQUE NOT NULL,
                    encrypted_data BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # X-ray images table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS xray_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER NOT NULL,
                    image_path TEXT NOT NULL,
                    position TEXT NOT NULL,
                    body_part TEXT NOT NULL,
                    dicom_data BLOB,
                    technician_id INTEGER,
                    radiologist_id INTEGER,
                    acquisition_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    annotations TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients (id),
                    FOREIGN KEY (technician_id) REFERENCES users (id),
                    FOREIGN KEY (radiologist_id) REFERENCES users (id)
                )
            ''')
            
            # Equipment table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    status TEXT DEFAULT 'operational',
                    last_maintenance TIMESTAMP,
                    next_maintenance TIMESTAMP,
                    location TEXT,
                    notes TEXT
                )
            ''')
            
            # Usage logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    equipment_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (equipment_id) REFERENCES equipment (id)
                )
            ''')
            
            # Audit logs table for HIPAA compliance
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    resource_type TEXT,
                    resource_id INTEGER,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Position presets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS position_presets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    body_part TEXT NOT NULL,
                    description TEXT,
                    settings TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            self.logger.info("Database tables created successfully")
            
            # Insert default admin user if not exists
            self._create_default_admin()
    
    def _create_default_admin(self):
        """Create default admin user"""
        import bcrypt
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            
            if not cursor.fetchone():
                # Default password: Admin123! (should be changed on first login)
                password_hash = bcrypt.hashpw("Admin123!".encode(), bcrypt.gensalt())
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, full_name, email)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', password_hash, 'admin', 'System Administrator', 'admin@hospital.com'))
                conn.commit()
                self.logger.info("Default admin user created")
    
    def add_patient(self, patient_data: Dict) -> int:
        """Add a new patient with encrypted data"""
        encrypted_data = self._encrypt_data(json.dumps(patient_data))
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO patients (patient_id, encrypted_data)
                VALUES (?, ?)
            ''', (patient_data['patient_id'], encrypted_data))
            
            patient_id = cursor.lastrowid
            conn.commit()
            
            # Log the action
            self._log_audit_action(None, "CREATE", "patient", patient_id, "New patient added")
            
            return patient_id
    
    def get_patient(self, patient_id: str) -> Optional[Dict]:
        """Retrieve patient data by patient ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, encrypted_data, created_at, updated_at
                FROM patients WHERE patient_id = ?
            ''', (patient_id,))
            
            row = cursor.fetchone()
            if row:
                encrypted_data = row[1]
                patient_data = json.loads(self._decrypt_data(encrypted_data))
                patient_data.update({
                    'id': row[0],
                    'created_at': row[2],
                    'updated_at': row[3]
                })
                return patient_data
            return None
    
    def search_patients(self, search_term: str) -> List[Dict]:
        """Search patients by name or ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, patient_id, encrypted_data, created_at, updated_at
                FROM patients
            ''')
            
            results = []
            for row in cursor.fetchall():
                try:
                    patient_data = json.loads(self._decrypt_data(row[2]))
                    if (search_term.lower() in patient_data.get('name', '').lower() or
                        search_term.lower() in row[1].lower()):
                        patient_data.update({
                            'id': row[0],
                            'patient_id': row[1],
                            'created_at': row[3],
                            'updated_at': row[4]
                        })
                        results.append(patient_data)
                except Exception as e:
                    self.logger.error(f"Error decrypting patient data: {e}")
            
            return results
    
    def add_xray_image(self, patient_id: int, image_path: str, position: str, 
                      body_part: str, technician_id: int, notes: str = "") -> int:
        """Add a new X-ray image record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO xray_images 
                (patient_id, image_path, position, body_part, technician_id, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (patient_id, image_path, position, body_part, technician_id, notes))
            
            image_id = cursor.lastrowid
            conn.commit()
            
            # Log the action
            self._log_audit_action(technician_id, "CREATE", "xray_image", image_id, 
                                 f"New X-ray image added: {body_part} - {position}")
            
            return image_id
    
    def get_patient_xrays(self, patient_id: int) -> List[Dict]:
        """Get all X-ray images for a patient"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, image_path, position, body_part, acquisition_date, 
                       notes, annotations, technician_id, radiologist_id
                FROM xray_images 
                WHERE patient_id = ?
                ORDER BY acquisition_date DESC
            ''', (patient_id,))
            
            return [{
                'id': row[0],
                'image_path': row[1],
                'position': row[2],
                'body_part': row[3],
                'acquisition_date': row[4],
                'notes': row[5],
                'annotations': row[6],
                'technician_id': row[7],
                'radiologist_id': row[8]
            } for row in cursor.fetchall()]
    
    def update_image_annotations(self, image_id: int, annotations: str, user_id: int):
        """Update image annotations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE xray_images 
                SET annotations = ?, radiologist_id = ?
                WHERE id = ?
            ''', (annotations, user_id, image_id))
            conn.commit()
            
            # Log the action
            self._log_audit_action(user_id, "UPDATE", "xray_image", image_id, 
                                 "Image annotations updated")
    
    def add_usage_log(self, user_id: int, action: str, details: str = "", 
                     equipment_id: int = None):
        """Add usage log entry"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usage_logs (user_id, equipment_id, action, details)
                VALUES (?, ?, ?, ?)
            ''', (user_id, equipment_id, action, details))
            conn.commit()
    
    def _log_audit_action(self, user_id: Optional[int], action: str, 
                         resource_type: str, resource_id: int, details: str):
        """Log audit action for HIPAA compliance"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (user_id, action, resource_type, resource_id, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, action, resource_type, resource_id, details))
            conn.commit()
    
    def get_audit_logs(self, limit: int = 100) -> List[Dict]:
        """Get recent audit logs"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT al.id, u.username, al.action, al.resource_type, 
                       al.resource_id, al.details, al.timestamp
                FROM audit_logs al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.timestamp DESC
                LIMIT ?
            ''', (limit,))
            
            return [{
                'id': row[0],
                'username': row[1] or 'System',
                'action': row[2],
                'resource_type': row[3],
                'resource_id': row[4],
                'details': row[5],
                'timestamp': row[6]
            } for row in cursor.fetchall()] 