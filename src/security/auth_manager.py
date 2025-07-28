"""
Authentication Manager for X-ray Management System
Handles user authentication and authorization
"""

import bcrypt
import sqlite3
import logging
from datetime import datetime
from typing import Optional, Dict
from PyQt6.QtCore import QObject, pyqtSignal

class AuthManager(QObject):
    """Manages user authentication and authorization"""
    
    # Signals
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    login_failed = pyqtSignal(str)      # Emits error message on failed login
    logout_successful = pyqtSignal()    # Emits on successful logout
    
    def __init__(self, db_path: str = "data/xray_system.db"):
        super().__init__()
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.current_user = None
        
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user with username and password"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, password_hash, role, full_name, email, is_active
                    FROM users WHERE username = ?
                ''', (username,))
                
                row = cursor.fetchone()
                if not row:
                    self.logger.warning(f"Login attempt with non-existent username: {username}")
                    return None
                
                user_id, db_username, password_hash, role, full_name, email, is_active = row
                
                if not is_active:
                    self.logger.warning(f"Login attempt for inactive user: {username}")
                    return None
                
                # Verify password
                if bcrypt.checkpw(password.encode(), password_hash):
                    # Update last login
                    cursor.execute('''
                        UPDATE users SET last_login = ? WHERE id = ?
                    ''', (datetime.now(), user_id))
                    conn.commit()
                    
                    user_data = {
                        'id': user_id,
                        'username': db_username,
                        'role': role,
                        'full_name': full_name,
                        'email': email,
                        'login_time': datetime.now()
                    }
                    
                    self.current_user = user_data
                    self.logger.info(f"Successful login for user: {username} (Role: {role})")
                    return user_data
                else:
                    self.logger.warning(f"Failed login attempt for user: {username}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Authentication error: {e}")
            return None
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            self.logger.info(f"User logged out: {self.current_user['username']}")
            self.current_user = None
            self.logout_successful.emit()
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged-in user data"""
        return self.current_user
    
    def has_permission(self, permission: str) -> bool:
        """Check if current user has specific permission"""
        if not self.current_user:
            return False
        
        role = self.current_user['role']
        
        # Define role-based permissions
        permissions = {
            'admin': [
                'view_patients', 'add_patients', 'edit_patients', 'delete_patients',
                'view_xrays', 'add_xrays', 'edit_xrays', 'delete_xrays',
                'view_users', 'add_users', 'edit_users', 'delete_users',
                'view_equipment', 'add_equipment', 'edit_equipment', 'delete_equipment',
                'view_audit_logs', 'view_usage_logs', 'system_admin'
            ],
            'radiologist': [
                'view_patients', 'view_xrays', 'edit_xrays', 'add_annotations',
                'view_equipment', 'view_usage_logs'
            ],
            'technician': [
                'view_patients', 'add_patients', 'view_xrays', 'add_xrays',
                'view_equipment', 'add_usage_logs'
            ]
        }
        
        return permission in permissions.get(role, [])
    
    def require_permission(self, permission: str) -> bool:
        """Decorator-like function to check permission and emit signal if denied"""
        if not self.has_permission(permission):
            self.logger.warning(f"Permission denied: {self.current_user['username']} tried to access {permission}")
            return False
        return True
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current password hash
                cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
                row = cursor.fetchone()
                if not row:
                    return False
                
                current_hash = row[0]
                
                # Verify old password
                if not bcrypt.checkpw(old_password.encode(), current_hash):
                    return False
                
                # Hash new password
                new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                
                # Update password
                cursor.execute('''
                    UPDATE users SET password_hash = ? WHERE id = ?
                ''', (new_hash, user_id))
                conn.commit()
                
                self.logger.info(f"Password changed for user ID: {user_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Password change error: {e}")
            return False
    
    def create_user(self, username: str, password: str, role: str, 
                   full_name: str, email: str = None) -> bool:
        """Create a new user (admin only)"""
        if not self.has_permission('add_users'):
            return False
        
        try:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password_hash, role, full_name, email)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password_hash, role, full_name, email))
                conn.commit()
                
                self.logger.info(f"New user created: {username} (Role: {role})")
                return True
                
        except sqlite3.IntegrityError:
            self.logger.warning(f"User creation failed - username already exists: {username}")
            return False
        except Exception as e:
            self.logger.error(f"User creation error: {e}")
            return False
    
    def get_user_role_display_name(self, role: str) -> str:
        """Get display name for user role"""
        role_names = {
            'admin': 'System Administrator',
            'radiologist': 'Radiologist',
            'technician': 'X-ray Technician'
        }
        return role_names.get(role, role.title())
    
    def get_available_roles(self) -> list:
        """Get list of available user roles"""
        return ['admin', 'radiologist', 'technician'] 