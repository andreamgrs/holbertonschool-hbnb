"""This is the review class"""
from app.models.base import BaseModel # Import the class BaseModel from the package inside models 


class Review(BaseModel):
    """Class for review
    """

    def __init__(self, text, rating, place, user):
        """Initializes a Review instance.
        """
        super().__init__() # call init method from BaseModel 
        self.text = text
        self.rating = rating
        self.place = place 
        self.user = user
    
    # --- Getters and Setters ---
    #Text
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        # Validates that text is not an empty string
        if not isinstance(value, str) or value.strip() == "":
            raise TypeError('Text must be a string and not an empty string')
        self._text = value

    #rating 
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value < 1 or value > 5:
            raise ValueError('Rating must be between 1 and 5')
        self._rating = value
    #place  
    @property
    def place(self):
        return self._place
    
    @place.setter
    def place(self, value):
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError('Place is not an instance of the Place class')
        self._place = value
    #user
    @property
    def user(self):
        return self._user
    
    @user.setter
    def user(self, value):
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError('User is not an instance of the User class')
        self._user = value
