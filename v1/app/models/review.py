"""This is the review class"""
from . import BaseModel # Import the class BaseModel from the package inside models 

class Place(BaseModel):
    def __init__(self, name):
        self.name = name

class Review(BaseModel):
    """Class for review
    """

    def __init__(self, text, rating, place, user):
        """Initializes a Review instance.
        """
        super().__init__() # call init method from BaseModel 
        self.validator_existance("place",place)
        self.validator_existance("user",user)
        self.validate_rating("rating", rating)
        self.validator_text("text", text)
        self.text = text
        self.rating = rating
        self.place = place 
        self.user = user

    # Validates that rating is between 1 and 5
    def validate_rating(self, name, value):
        """Validates that rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise ValueError("{} must be between 1 and 5".format(name))
    
    # Validator of exitance for user and place ASK -> Already validates in USER CLASS
    def validator_existance(self, name, value):
        """Validates the existance of place/user"""
        if value is None:
            raise ValueError("{} must exist".format(name))
        
    # Validates that text is not an empty string
    def validator_text(self, name, value):
        """Validates text"""
        if not value:
            raise ValueError("Review {} is required.".format(name))
