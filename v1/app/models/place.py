"""
This is the place class
"""
from .base import BaseModel
from .amenity import Amenity
from .review import Review
from .user import User


class Place(BaseModel):

    def __init__(self, title, description, price, latitude,  longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

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
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("title must be a string")
        if len(value) <= 0:
            raise ValueError("title must not be empty")
        if len(value) > 100:
            raise ValueError("title must be less than 100 characters") 
        self._title = value        

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("description must be a string")
        # airbnb descuptions are limited to 500 characters
        if len(value) > 500:
            raise ValueError("description must be less than 500 characters")
        self._description = value

        
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise TypeError("price must be a float")
        if value < 0:
            raise ValueError('price must be greater than 0')
        self._price = value
        
    @property
    def latitude (self):
        return self._latitude 

    @latitude.setter
    def latitude (self, value):
        if not isinstance(value, float):
            raise TypeError("latitude must be a float")
        if value < -90 or value > 90:
            raise ValueError("latitude must be between -90 and 90")
        self._latitude  = value

    @property
    def longitude (self):
        return self._longitude 

    @longitude.setter
    def longitude (self, value):
        if not isinstance(value, float):
            raise TypeError("longitude must be a float")
        if value < -180 or value > 180:
            raise ValueError("longitude must be between -180 and 180")
        self._longitude  = value
       
    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError('Owner is not an instance of the User class')
        self._owner = value
