"""
This is the Amenity class
"""
from app import db
from .base import BaseModel
from .place import place_amenity
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    # --- Properties ---
    _name  = db.Column(db.String(50), nullable=False)
    # Define relationship to places
    places = relationship('Place',
                          secondary=place_amenity,
                          back_populates='amenities',
                          lazy=True)

    # --- Getters and Setters ---
    @hybrid_property
    def name(self):
        """ Returns value of the amenity name"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @validates("_name")
    def validate_name(self, key, value):
        if not isinstance(value, str):
            raise TypeError('Amenity name must be a string')
        # Check name is <= 50 chars only after strip spaces
        if 0 < len(value.strip()) <= 50:
            return value
        else:
            raise ValueError("Invalid name length!")

