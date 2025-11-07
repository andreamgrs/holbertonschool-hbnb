"""
This is the place class
"""
from app import db, bcrypt
from app.models.base import BaseModel
from .amenity import Amenity
from .review import Review
from .user import User
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property


class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column(db.String(100), nullable=False)
    _description = db.Column(db.String(500), nullable=False)
    _price = db.Column(db.Float, nullable=False)
    _latitude = db.Column(db.Float, nullable=False)
    _longitude = db.Column(db.Float, nullable=False)

    # --- Methods ---
    def add_review(self, review):
        """Add a review to the place."""
        # check review is a Review instance
        if not isinstance(review, Review):
            raise TypeError('Review not an instance of the Review class')
        # check if review already exists
        if review in self.reviews:
            raise ValueError('Review already exists')
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        # check amenity is an Amenity instance
        if not isinstance(amenity, Amenity):
            raise TypeError('Amenity not an instance of the Amenity class')
        # check if amenity already exists
        if amenity in self.amenities:
            raise ValueError('Amenity already exists')
        
        self.amenities.append(amenity)
    
    def list_amenities(self):
        """List all the amenities of a place"""
        print(f"The {self._title} listing has the following amenities:")
        for element in self.amenities:
            print(element)
    
    # --- Getters and Setters ---
    @hybrid_property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value   

    @validates("_title")
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError("title must be a string")
        if len(value) <= 0:
            raise ValueError("title must not be empty")
        if len(value) > 100:
            raise ValueError("title must be less than 100 characters") 
        return value

    @hybrid_property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        self._description = value

    @validates("_description")
    def validate_description(self, key, value):
        if not isinstance(value, str):
            raise TypeError("description must be a string")
        # airbnb descuptions are limited to 500 characters
        if len(value) > 500:
            raise ValueError("description must be less than 500 characters")
        return value
        
    @hybrid_property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value

    @validates("_price")
    def validate_price(self, key, value):
        # accept int or float and coerce to float
        if not isinstance(value, (int, float)):
            raise TypeError("price must be a number")
        value = float(value)
        if value < 0:
            raise ValueError('price must be greater than 0')
        return value
        
    @hybrid_property
    def latitude (self):
        return self._latitude 

    @latitude.setter
    def latitude (self, value):
        self._latitude  = value

    @validates("_latitude")
    def validate_latitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("latitude must be a number")
        value = float(value)
        if value < -90 or value > 90:
            raise ValueError("latitude must be between -90 and 90")
        return value

    @hybrid_property
    def longitude (self):
        return self._longitude 

    @longitude.setter
    def longitude (self, value):
        self._longitude  = value

    @validates("_longitude")
    def validate_longitude(self, key, value):
        if not isinstance(value, (int, float)):
            raise TypeError("longitude must be a number")
        value = float(value)
        if value < -180 or value > 180:
            raise ValueError("longitude must be between -180 and 180")
        return value
    
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError('Owner is not an instance of the User class')
        self._owner = value