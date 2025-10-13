"""This is the review class"""
from . import BaseModel # Import the class BaseModel from the package inside models 


class Review(BaseModel):
    """Class for review
    """

    def __init__(self, text, rating, place, user):
        """Initializes a Review instance.
        """
        super().__init__() # call init method from BaseModel 
        self.text = text
        self.rating = rating
        self.place_id = place.id 
        self.user_id = user.id
    
    # --- Getters and Setters ---
    #Text
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        # Validates that text is not an empty string
        if not value:
            raise TypeError('Text must be a string and not an empty string')
        self._text = value

    #rating 
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5")
        self._rating = value
    #place  
    @property
    def place_id(self):
        return self._place_id
    
    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise TypeError('Place ID must be a non-empty string')
        self._place_id = value
    #user
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise TypeError('User ID must be a non-empty string')
        self._user_id = value

