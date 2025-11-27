"""
This is the Review class
"""
from app.models.base import BaseModel
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property

class Review(BaseModel):
    __tablename__ = 'reviews'

    # --- Properties ---
    _text = db.Column(db.String(100), nullable=False)
    _rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)

    
    
    # --- Getters and Setters ---
    @hybrid_property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @validates("_text")
    def validate_text(self, key, value):
        # Validates that text is not an empty string
        if not isinstance(value, str) or value.strip() == "":
            raise TypeError('Text must be a string and not an empty string')
        return value
    
    @hybrid_property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        self._rating = value

    @validates("_rating")
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError('Rating must be between 1 and 5')
        return value


    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError('Place is not an instance of the Place class')
        self._place = value

    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError('User is not an instance of the User class')
        self._user = value
