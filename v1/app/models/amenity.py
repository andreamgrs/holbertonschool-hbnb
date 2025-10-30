"""
This is a amenity class
"""
from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    # --- Getters and Setters ---
    @property
    def name(self):
        """ Returns value of the amenity name"""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for amenity name"""
        if not isinstance(value, str):
            raise TypeError('Amenity name must be a string')
        
        if 0 < len(value.strip()) <= 50: # check name is <= 50 chars only after strip spaces
            self._name = value # originally want to store only the name that's stripped of spaces in between but removed this to be aligned with feedback and users model file
        else:
            raise ValueError("Invalid name length!")

