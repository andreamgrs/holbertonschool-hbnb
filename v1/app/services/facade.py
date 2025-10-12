from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        """Return a list of all users"""
        return self.user_repo.get_all()  # InMemoryRepo has get_all function in persistence repo

    def update_user(self, user_id, data):
        """Update a user in the repos"""
        updated_user = self.user_repo.update(user_id, data)  # InMemoryRepo has update function in persistence repo
        return updated_user
    
