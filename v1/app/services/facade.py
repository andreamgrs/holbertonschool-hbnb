from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository() # connect to memory for testing before connecting to actual database later
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data): # create a User object using data received from the API.
        user = User(**user_data) # User(**user_data) is equivalent to User(id='u001', name='Alice', email='alice@example.com').
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
    

# Adding methods for review
    def create_review(self, review_data):
        """Create review"""
        # Extract fields from input
        review = Review(**review_data) #unpacking
        
        # Validates that rating is between 1 and 5
        if review.rating < 1 or review.rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Validator of exitance for user_id 
        if self.get_user(review.user_id) is None:
            raise ValueError("User must exist")
        
        # Validator of exitance for place_id
        if self.get_place(review.place_id) is None:
            raise ValueError("Place must exist")
        self.review_repo.add(review)

        return review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all the reviews"""
        return self.review_repo.get_all() 

    def get_reviews_by_place(self, place_id):
        """Get review by place"""
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found")

    def update_review(self, review_id, review_data):
        updated_review = self.place_repo.update(review_id, review_data)
        return updated_review

    # Methods for place
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Retrieve all places
        return self.place_repo.get_all() 

    def update_place(self, place_id, place_data):
        # Update a place
        updated_place = self.place_repo.update(place_id, place_data)
        return updated_place