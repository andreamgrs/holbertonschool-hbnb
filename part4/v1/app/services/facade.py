from app.persistence.repository import InMemoryRepository, SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
import uuid


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    # METHODS FOR USERS
    def create_user(self, user_data):
        """ Create a new user """
        # Check for duplicate email
        if self.user_repo.get_by_attribute('email', user_data['email']):
            raise ValueError('Email already registered')
        # Create the user — note the model validates first_name, last_name, email
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user
    
    def _is_valid_uuid(self, value):
        """ Check id is a valid UUID """
        try:
            uuid.UUID(value, version=4)
            return True
        except (ValueError, TypeError):
            return False

    def get_user(self, user_id):
        """ Get a single user from the user_id """
        if not self._is_valid_uuid(user_id):
            raise ValueError(f"User id '{user_id}' is not valid")
        user = self.user_repo.get(user_id)
        # User will be none if id is not found
        if not user:
            raise TypeError(f"User with '{user_id}' not found")
        return user
    
    def get_user_by_email(self, email):
        """ Get single user by email """
        return self.user_repo.get_user_by_email(email)
    
    def get_all_users(self):
        """Return a list of all users"""
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """Update a user using setters to enforce validation"""
        # Get the user from the user_id
        user = self.get_user(user_id)
        # Update fields via setters to enforce validation
        if "first_name" in user_data:
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            user.email = user_data["email"]
        if "password" in user_data:
            user.hash_password(user_data["password"])
        # Save updated data to repo
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user
            
    def delete_user(self, user_id):
        """ Delete user """
        user = self.get_user(user_id)
        self.user_repo.delete(user_id)
        return {'message': 'User deleted successfully'}

    # METHODS FOR REVIEW
    def create_review(self, review_data):
        """Create review"""
        # Get user and place objects for the review
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        # Extract fields from input
        review = Review(text=review_data.get('text'), 
                        rating=review_data.get('rating'), 
                        place=place, 
                        user=user)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get review by ID"""
        review = self.review_repo.get(review_id)
        if not review:
            raise TypeError(f"Review with '{review_id}' not found")
        return review
    
    def get_all_reviews(self):
        """Get all the reviews"""
        return self.review_repo.get_all() 
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a place by place_id"""
        # Get all the reviews
        reviews = self.review_repo.get_review_by_place(place_id)
        return reviews
    
    def delete_review(self, review_id):
        """ Delete review """
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError(f"Review with id {review_id} not found")
        self.review_repo.delete(review_id)
        return {'message': 'Review deleted successfully'}
    
    def update_review(self, review_id, review_data):
        """ Update review """
        review = self.get_review(review_id)
        # Update fields via setters to enfore validation logic
        if "text" in review_data:
            review.text = review_data.get("text")
        if "rating" in review_data:
            review.rating = review_data.get("rating")
        updated_review = self.review_repo.update(review_id, review_data)
        return updated_review

    # METHODS FOR PLACE
    def create_place(self, place_data):
        """ Create a new place """
        # Get owner object using owner id
        owner = self.get_user(place_data['owner_id'])
        # Get amenity objects using amenty ids
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
        # Add amenities to place
        for amenity in amenities_list:
            place.add_amenity(amenity)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """ Get single place using place_id """
        # Retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """ Get all places """
        # Retrieve all places
        return self.place_repo.get_all() 
    
    def update_place(self, place_id, place_data):
        """ Update a place using the place_id """
        # Get the place object
        place = self.get_place(place_id)
        # Update fields via setters to enforce validation logic
        if "title" in place_data:
            place.title = place_data.get("title")
        if "description" in place_data:
            place.description = place_data.get("description")
        if "price" in place_data:
            place.price = place_data.get("price")
        if "amenities" in place_data:
            # Add amenity objects for the amenity ids
            amenities_id = place_data.get('amenities')
            for amenity_id in amenities_id:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
                place.add_amenity(amenity)
            del place_data["amenities"]
        updated_place = self.place_repo.update(place_id, place_data)
        return updated_place
    
    def delete_place(self, place_id):
        """ Delete place using place_id """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError(f"Place with id {place_id} not found")
        self.place_repo.delete(place_id)
        return {'message': 'Place deleted successfully'}

    
    # METHODS FOR AMENITIES
    def create_amenity(self, amenity_data):
        """ Create new amenity """
        # Check if amenity already exists
        if self.amenity_repo.get(amenity_data.get('id')):
            raise ValueError('Amenity already exists')
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_all_amenities(self):
        """ Get all amenities """
        return self.amenity_repo.get_all()

    def get_amenity(self, amenity_id):
        """ Get single amenity from amenity_id """
        if not self._is_valid_uuid(amenity_id):
            raise ValueError(f"Amenity id  '{amenity_id}' is not valid")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise TypeError(f"Amenity with '{amenity_id}' not found")
        return amenity

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity using setters to enforce validation"""
        amenity = self.get_amenity(amenity_id)
        if "name" in amenity_data:
            amenity.name = amenity_data.get("name")
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def delete_amenity(self, amenity_id):
        """ Delete an amenity using amenity_id """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError(f"Amenity with id {amenity_id} not found")
        self.amenity_repo.delete(amenity_id)
        return {'message': 'Amenity deleted successfully'}


