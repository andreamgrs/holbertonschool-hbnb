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
        """Setter for prop name"""
        if 0 < len(value.strip()) <= 50: # check name is <= 50 chars only after strip spaces
            self._name = value.strip() #store only the name that's stripped of spaces in between
        else:
            raise ValueError("Invalid name length!")

