from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
import uuid
#import logging
#logger = logging.getLogger(__name__)


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

    def _is_valid_uuid(self, value):
        try:
            uuid.UUID(value, version=4)
            return True
        except (ValueError, TypeError):
            return False

    def get_user(self, user_id):
            if not self._is_valid_uuid(user_id):
                return {'error': 'Invalid input', 'status': 400}

            user = self.user_repo.get(user_id)
            if not user:
                return {'error': 'User not found', 'status': 404}

            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }

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
        try:
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
            return review, 201
        
        except (ValueError,TypeError) as e:
        # Handle known error
            #logger.warning(f"Review creation failed: {e}") #helps to debug, this we developers look it

            #let know the user something went wrong, this the user look it with json.loads
            error_message = str(e)
            if error_message == "User must exist" or error_message == "Place must exist":
                return {"status": "error", "message": error_message}, 404
            return {"status": "error", "message": error_message}, 400


    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all the reviews"""
        return self.review_repo.get_all() 

    def get_reviews_by_place(self, place_id):
        """Get reviews by place_id"""
        reviews = self.review_repo.get_by_attribute("place_id", place_id)
        if not reviews:
            raise ValueError("No reviews found for this place")
        return reviews


    def update_review(self, review_id, review_data):
        updated_review = self.review_repo.update(review_id, review_data)
        return updated_review

    # Methods for place
    def create_place(self, place_data):
        ''' Check input data is valid '''
        if len(place_data['title']) < 0:
            raise ValueError("title must not be empty")
        if len(place_data['title']) > 50:
            raise ValueError("title must be less than 50 characters") 
        if len(place_data['description']) > 500:
            raise ValueError("description must be less than 500 characters")
        if place_data['price'] < 0:
            raise ValueError('price must be greater than 0')
        if place_data['latitude'] < -90 or place_data['latitude'] > 90:
            raise ValueError("latitude must be between -90 and 90")
        if place_data['longitude'] < -180 or place_data['longitude'] > 180:
            raise ValueError("longitude must be between -180 and 180")
        
        ''' Create user from owner id '''
        owner = self.get_user(place_data['owner_id'])
        if owner is None:
            raise ValueError("Owner not found")

        place = Place(
                title=place_data.get('title'),
                description=place_data.get('description', ''),
                price=place_data.get('price'),
                latitude=place_data.get('latitude'),
                longitude=place_data.get('longitude'),
                owner=owner  # Pass the actual User object
                )
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
        if len(place_data['title']) < 0:
            raise ValueError("title must not be empty")
        if len(place_data['title']) > 50:
            raise ValueError("title must be less than 50 characters") 
        if len(place_data['description']) > 500:
            raise ValueError("description must be less than 500 characters")
        if place_data['price'] < 0:
            raise ValueError('price must be greater than 0')
        updated_place = self.place_repo.update(place_id, place_data)
        return updated_place