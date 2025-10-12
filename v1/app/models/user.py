"""
This is the user class
"""
from . import BaseModel
import re


class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        self.reviews = []

    # --- Methods ---
    def create_place(self, place):
        """User create a place"""
        from . import Place
        if not isinstance(place, Place):
            raise TypeError('expecting a place')
        
        if not self.is_admin:
            raise PermissionError('only admins/owners can add places.')

        if place not in self.places:
            self.places.append(place)
            place.owner = self
    
    

    def add_review(self, review):
        """User write a review"""
        from . import Review
        from . import Place

        if not isinstance(review, Review):
            raise TypeError('expecting a review')
        if not isinstance(review.place, Place):
            raise TypeError("review must be for a valid place")

        if review not in self.reviews:
            self.reviews.append(review)
            review.user = self

    def update(self, data):
        """update user details"""
        allowed_fields = ['first_name', 'last_name', 'email', 'is_admin']
        for key, value in data.items():
            if key in allowed_fields:
                setattr(self, key, value)


    # --- Getters and Setters ---
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str) or not value.isalpha():
            raise TypeError('first name must be a string')
       
        is_valid_name = 0 < len(value.strip()) <= 50

        if is_valid_name:
            self._first_name = value
        else:
            raise ValueError('first name has max length of 50 chars')
        
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str) or not value.isalpha():
            raise TypeError('last name must be a string')
 
        is_valid_name = 0 < len(value.strip()) <= 50

        if is_valid_name:
            self._last_name = value
        else:
            raise ValueError('last name has max length of 50 chars')
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        clean_value = value.strip()
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.fullmatch(pattern, clean_value):
            self._email = clean_value.lower()
        else:
            raise ValueError('Invalid email')
        
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if isinstance(value, bool):
            self._is_admin = value
        else:
            raise ValueError("is_admin must be true or false")



