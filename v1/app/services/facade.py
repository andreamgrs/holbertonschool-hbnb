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
                raise ValueError(f"User id '{user_id}' is not valid")
            
            user = self.user_repo.get(user_id)

            if not user:
                raise TypeError(f"User with '{user_id}' not found")

            return user
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_all_users(self):
        """Return a list of all users"""
        return self.user_repo.get_all()  # InMemoryRepo has get_all function in persistence repo
    
    def update_user(self, user_id, user_data):
        """Update a user using setters to enforce validation"""

        # get the existing user
        user = self.get_user(user_id)
        # update fields via setters
        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            user.email = user_data["email"]

        #save updated data to repo
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user
    

# Methods for review
    def create_review(self, review_data):
        """Create review"""
        # Extract fields from input
        review = Review(**review_data) #unpacking
            
        # Validator of exitance for user_id 
        if self.get_user(review.user_id) is None:
            raise ValueError("User must exist")#in the api test doesnt show user_must_exist -> show user id not valid
            
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
        """Get reviews by place_id"""
        #get all the reviews
        reviews = self.review_repo.get_all()
        reviews_by_place_id = []

        for review in reviews:
            if review.place_id == place_id:
                reviews_by_place_id.append(review)
        if not reviews_by_place_id:
            raise ValueError("No reviews found for this place")
        return reviews_by_place_id

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        review.text = review_data.get("text")
        review.rating = review_data.get("rating")
        updated_review = self.review_repo.update(review_id, review_data)
        return updated_review

# Methods for place
    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        amenities_id = place_data.get('amenities', [])
        amenities_list = []

        for amenity_id in amenities_id:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            amenities_list.append(amenity)
        
        try:
            place = Place(
                        title=place_data.get('title'),
                        description=place_data.get('description', ''),
                        price=place_data.get('price'),
                        latitude=place_data.get('latitude'),
                        longitude=place_data.get('longitude'),
                        owner=owner  # Pass the actual User object
                        )
        except ValueError as e:
            raise ValueError(e)
        
        for amenity in amenities_list:
            place.add_amenity(amenity)
        
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        # Retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Retrieve all places
        return self.place_repo.get_all() 

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        place.title = place_data.get("title")
        place.description = place_data.get("description")
        place.price = place_data.get("price")
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
        if not self._is_valid_uuid(amenity_id):
            raise ValueError('Amenity id not valid')

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise TypeError('Amenity not found')

        return amenity

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity using setters to enforce validation"""
        
        amenity = self.amenity_repo.get(amenity_id)

        amenity.name = amenity_data.get("name")

        updated_amenity = self.amenity_repo.update(amenity_id, amenity_data)
        return updated_amenity

