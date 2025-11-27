"""
This is a amenity class
"""
from app import db
from .base import BaseModel
from .place import place_amenity
import re
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property



class Amenity(BaseModel):
    __tablename__ = 'amenities'

    _name  = db.Column(db.String(50), nullable=False)
    places = relationship('Place',
                          secondary=place_amenity,
                          lazy='subquery',
                          backref=db.backref('amenity', lazy=True))


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
        
        if 0 < len(value.strip()) <= 50: # check name is <= 50 chars only after strip spaces
            return value # originally want to store only the name that's stripped of spaces in between but removed this to be aligned with feedback and users model file
        else:
            raise ValueError("Invalid name length!")

