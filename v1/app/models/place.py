"""
This is the place class
"""
from . import BaseModel
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
        if amenity in self._amenities:
            raise ValueError('Amenity already exists')
        
        self._amenities.append(amenity)
    
    def list_amenities(self):
        """List all the amenities of a place"""
        print(f"The {self._title} listing has the following amenities:")
        for element in self._amenities:
            print(element)

    # --- Getters and Setters ---
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError('title must be a string')
       
        # airbnb titles are limited to 50 characters
        is_valid_title = 0 < len(value)<= 50

        if is_valid_title:
            self._title = value
        else:
            raise ValueError('title has max length of 50 chars')
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError('description must be a string')
 
        # airbnb descuptions are limited to 500 characters
        is_valid_description = 0 < len(value) <= 500

        if is_valid_description:
            self._description = value
        else:
            raise ValueError('description has max length of 500 chars')
        
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if not isinstance(value, float):
            raise TypeError('Price must be a float')
        if value < 0:
            raise ValueError("Price must be a non-negative value")
        self._price = value
        
    @property
    def latitude (self):
        return self._latitude 

    @latitude.setter
    def latitude (self, value):
        if not isinstance(value, float):
            raise TypeError('Latitude must be a float')
        if value > -90.0 and value < 90.0:
            self._latitude  = value
        else:
            raise ValueError('Latitude must be between -90.0 and 90.0')

    @property
    def longitude (self):
        return self._longitude 

    @longitude.setter
    def longitude (self, value):
        if not isinstance(value, float):
            raise TypeError('Longitude must be a float')
        if value > -180.0 and value < 180.0:
            self._longitude  = value
        else:
            raise ValueError('Longitude must be between -180.0 and 180.0')

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, value):
        if not isinstance(value, User):
            raise TypeError('User is not an instance of the User class')
        self._owner = value
