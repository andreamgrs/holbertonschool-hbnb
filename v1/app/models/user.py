"""
This is the user class
"""
from . import BaseModel


class User(BaseModel):
    pass

    def __init__(self, first_name, last_name, email, is_admin = False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email


