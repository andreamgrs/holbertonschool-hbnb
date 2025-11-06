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

# METHODS FOR USERS

    # CREATE SINGLE USER
    def create_user(self, user_data):
        # check for duplicate email first
        if self.user_repo.get_by_attribute('email', user_data['email']):
            raise ValueError('Email already registered')

        # then create the user — model validates first_name, last_name, email
        user = User(**user_data)
        self.user_repo.add(user)

        return user  # Q: Whether should allow this to be return user or not
    
    # CHECK ID IS VALID
    def _is_valid_uuid(self, value):
        try:
            uuid.UUID(value, version=4)
            return True
        except (ValueError, TypeError):
            return False

    # GET SINGLE USER BY ID
    def get_user(self, user_id):
            if not self._is_valid_uuid(user_id):
                raise ValueError(f"User id '{user_id}' is not valid")
            
            user = self.user_repo.get(user_id)

            if not user:
                raise TypeError(f"User with '{user_id}' not found")

            return user
    
    # GET SINGLE USER BY EMAIL
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    # GET ALL USERS
    def get_all_users(self):
        """Return a list of all users"""
        return self.user_repo.get_all()  # InMemoryRepo has get_all function in persistence repo
    
    # UPDATE SINGLE USER 
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
        if "password" in user_data:
            user.hash_password(user_data["password"])


        #save updated data to repo
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user
    

# METHODS FOR REVIEW

    # CREATE REVIEW
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        """Create review"""
        # Extract fields from input
        review = Review(text=review_data.get('text'), rating=review_data.get('rating'), place=place, user=user) #unpacking
            
        self.review_repo.add(review)
        return review

    # GET A REVIEW USING REVIEW ID
    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)
    
    # GET ALL REVIEWS
    def get_all_reviews(self):
        """Get all the reviews"""
        return self.review_repo.get_all() 
    
    # GET ALL REVIEWS OF A SINGLE PLACE USING PLACE ID
    def get_reviews_by_place(self, place_id):
        """Get reviews by place_id"""
        #get all the reviews
        reviews = self.review_repo.get_all()
        reviews_by_place_id = []

        for review in reviews:
            if review.place.id == place_id:
                reviews_by_place_id.append(review)
        if not reviews_by_place_id:
            return reviews_by_place_id 
            #raise ValueError("No reviews found for this place")
        return reviews_by_place_id
    
    # DELETE REVIEW
    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review: #Check if I need to return false or a ValueError
            raise ValueError(f"Review with id {review_id} not found")
        self.review_repo.delete(review_id)
        return True

    
    # UPDATE REVIEW
    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        review.text = review_data.get("text")
        review.rating = review_data.get("rating")
        updated_review = self.review_repo.update(review_id, review_data)
        return updated_review

# METHODS FOR PLACE

    # CREATE PLACE
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

    # GET PLACE BY PLACE ID
    def get_place(self, place_id):
        # Retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)
    
    # GET ALL PLACES
    def get_all_places(self):
        # Retrieve all places
        return self.place_repo.get_all() 
    
    # UPDATE PLACE USING PLACEID
    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        place.title = place_data.get("title")
        place.description = place_data.get("description")
        place.price = place_data.get("price")
        updated_place = self.place_repo.update(place_id, place_data)
        return updated_place
    
# METHODS FOR AMENITIES

    # CREATE AMENITY
    def create_amenity(self, amenity_data):
        # check amenity doesn't exist already
        if self.amenity_repo.get(amenity_data.get('id')):
            raise ValueError('Amenity already exists')

        # call facade to create amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)

        return amenity # return amenity obj

    # GET ALL AMENITIES
    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    

    # GET AMENITY USING AMENITY ID
    def get_amenity(self, amenity_id):
        if not self._is_valid_uuid(amenity_id):
            raise ValueError(f"Amenity id  '{amenity_id}' is not valid")

        amenity = self.amenity_repo.get(amenity_id)

        if not amenity:
            raise TypeError(f"Amenity with '{amenity_id}' not found")

        return amenity

    # UPDATE AMENITY USING AMENITY ID
    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity using setters to enforce validation"""
        
        amenity = self.get_amenity(amenity_id)

        if "name" in amenity_data:
            amenity.name = amenity_data.get("name")

        updated_amenity = self.amenity_repo.update(amenity_id, amenity_data)
        return updated_amenity

