"""
This is the user class
"""
from app import db, bcrypt
import uuid
from .base import BaseModel
import re
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel):

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # --- Methods ---

    def hash_password(self, password):
        from app import bcrypt 
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from app import bcrypt  # import bcrypt for each method only
        return bcrypt.check_password_hash(self.password, password)

    # --- Getters and Setters ---
    @hybrid_property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self._first_name = value
    
    @validates("first_name")
    def validate_first_name(self, key, value):
        
        if not isinstance(value, str):
            raise TypeError('first name must be a string')
       
        if len(value.strip()) <= 50 and len(value.strip()) > 0:
            return value
        
        else:
            raise ValueError('first name has max length of 50 chars')
        
    @hybrid_property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        self.last_name = value

    @validates("last_name")
    def validate_last_name(self, key, value):

        if not isinstance(value, str):
            raise TypeError('last name must be a string')
       
        if len(value.strip()) <= 50 and len(value.strip()) > 0:
            return value
        
        else:
            raise ValueError('last name has max length of 50 chars')
        
    @hybrid_property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self.email = value
    
    @validates("email")
    def validate_email(self, key, value):

        clean_value = value.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(pattern, clean_value):
            return clean_value.lower()
        else:
            raise ValueError('Invalid email')
        
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @hybrid_property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        return value
    
    @validates("is_admin")
    def validate_admin(self, key, value):
        if isinstance(value, bool):
            return value
        else:
            raise ValueError("is_admin must be true or false")



