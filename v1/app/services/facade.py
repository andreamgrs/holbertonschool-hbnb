from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import uuid
#import logging
#logger = logging.getLogger(__name__)


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository() # connect to memory for testing before connecting to actual database later
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

# Methods for users

    def create_user(self, user_data):
        # check for duplicate email first
        if self.user_repo.get_by_attribute('email', user_data['email']):
            raise ValueError('Email already registered')

        # then create the user — model validates first_name, last_name, email
        user = User(**user_data)
        self.user_repo.add(user)

        return user  # always return User object

    def _is_valid_uuid(self, value):
        try:
            uuid.UUID(value, version=4)
            return True
        except (ValueError, TypeError):
            return False

    def get_user(self, user_id):
            if not self._is_valid_uuid(user_id):
                raise ValueError("User id not valid")

            user = self.user_repo.get(user_id)
            if not user:
                raise TypeError("User not found")

            return user
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        """Return a list of all users"""
        return self.user_repo.get_all()  # InMemoryRepo has get_all function in persistence repo

    def update_user(self, user_id, data):
        """Update a user in the repos"""
        updated_user = self.user_repo.update(user_id, data)  # InMemoryRepo has update function in persistence repo
        return updated_user
    

# Methods for review
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
        owner = self.get_user(place_data['owner_id'])
        
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
        updated_place = self.place_repo.update(place_id, place_data)
        return updated_place
    
# Methods for amenities

    def create_amenity(self, amenity_data):
        # check that amenity client trying to create doesn't already exist
        if self.amenity_repo.get(amenity_data.get('id')):
            raise ValueError('Amenity already exists')

        # call facade to create amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)

        return amenity # return amenity obj

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def update_amenity(self, amenity_id, update_data):
        return self.amenity_repo.update(amenity_id, update_data)
