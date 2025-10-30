import json
import unittest
from unittest.mock import MagicMock
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.services.facade import HBnBFacade
#To run python3 -m unittest app/tests/facade_unittest_review.py

class TestReviewFacade(unittest.TestCase):
    def setUp(self):
        """Set up fresh facade instance for each test"""
        self.facade = HBnBFacade()

    def test_create_review_01(self):
        """Test creating a review"""
        # First create an owner
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        self.facade.get_user = MagicMock(return_value=mock_user)
        # owner = self.facade.create_user({
        #     'first_name': 'Alice',
        #     'last_name': 'Smith',
        #     'email': 'alice@example.com'
        # })

        # Create a place
        mock_place = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user)
        mock_place.id ="123p"
        self.facade.get_place = MagicMock(return_value=mock_place)
        # place = self.facade.create_place({
        #     'title': 'Cozy Apartment',
        #     'description': 'A nice place',
        #     'price': 100.0,
        #     'latitude': 37.7749,
        #     'longitude': -122.4194,
        #     'owner_id': owner.id
        # })

        # Data to create a valid review
        review_data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "123u",
            "place_id": "123p"
        }

        #Call de facade create review
        review1 = self.facade.create_review(review_data)

        # Validate return data from the facade
        self.assertEqual(review1.text, 'Great place to stay!')
        self.assertEqual(review1.rating, 5)
        self.assertEqual(review1.user.id, "123u")
        self.assertEqual(review1.place.id, "123p")


    def test_create_review_02(self):
        """Test creating a review with invalid rating"""
        # First create an owner
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        self.facade.get_user = MagicMock(return_value=mock_user)

        # Create a place
        mock_place = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user)
        mock_place.id ="123p"
        self.facade.get_place = MagicMock(return_value=mock_place)

        # # Data invalid rating
        review_data_invalid_rating = {
            "text": "Great place to stay!",
            "rating": 6,
            "user_id": "123u",
            "place_id": "123p"
        }

        # #Call de facade create review_invalid_rating
        with self.assertRaises(ValueError) as context:
            self.facade.create_review(review_data_invalid_rating)

        self.assertEqual(str(context.exception), "Rating must be between 1 and 5")


    def test_create_review_03(self):
        """Test creating a review with invalid user"""
        # Simulate a none owner
        self.facade.get_user = MagicMock(return_value=None)

        # Create a place with owner
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        mock_place = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user)
        mock_place.id ="123p"
        self.facade.get_place = MagicMock(return_value=mock_place)

        # # Data invalid rating
        review_data_invalid_user = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "noexistuser",
            "place_id": "123p"
        }

        # #Call de facade create review_invalid_rating
        with self.assertRaises(TypeError) as context:
            self.facade.create_review(review_data_invalid_user)

        self.assertEqual(str(context.exception), "User is not an instance of the User class")

    def test_create_review_04(self):
        """Test creating a review with invalid place"""
        # First create an owner
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        self.facade.get_user = MagicMock(return_value=mock_user)

        # Simulate a none place
        self.facade.get_place = MagicMock(return_value=None)

        # # Data invalid rating
        review_data_invalid_place = {
            "text": "Great place to stay!",
            "rating": 3,
            "user_id": "123u",
            "place_id": "nonexistplace"
        }

        # #Call de facade create review_invalid_rating
        with self.assertRaises(TypeError) as context:
            self.facade.create_review(review_data_invalid_place)

        self.assertEqual(str(context.exception), "Place is not an instance of the Place class")

        

    def test_create_review_05(self):
        """Test creating a review with invalid text"""
        # First create an owner
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        self.facade.get_user = MagicMock(return_value=mock_user)

        # Create a place
        mock_place = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user)
        mock_place.id ="123p"
        self.facade.get_place = MagicMock(return_value=mock_place)

        # Data to create a review with invalid text
        # This TypeError is inside the review class not in the facade
        review_data = {
            "text": "",
            "rating": 5,
            "user_id": "123u",
            "place_id": "123p"
        }

        with self.assertRaises(TypeError) as context:
            self.facade.create_review(review_data)

        self.assertEqual(str(context.exception), "Text must be a string and not an empty string")
    
    def test_get_review(self):
        """Test to get review"""
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        self.facade.get_user = MagicMock(return_value=mock_user)
         # Create a place
        mock_place = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user)
        mock_place.id ="123p"
        self.facade.get_place = MagicMock(return_value=mock_place)
        
        # Create review
        mock_review = Review(text = "Amazing stay!", rating= 4, user = mock_user, place= mock_place)
        mock_review.id ="123r"
        self.facade.review_repo.get = MagicMock(return_value=mock_review)
        result = self.facade.get_review("123r")
        self.assertIsNotNone(result)
        self.assertEqual(result.text, "Amazing stay!")
        self.assertEqual(result.rating, 4)
    
    def test_get_review_empty(self):
        """Test to get review empty"""
        self.facade.review_repo.get = MagicMock(return_value=None)
        result = self.facade.get_review("invalid_id")
        self.assertEqual(result, None)

    def test_updated_review(self):
        """Test to updated review"""

         # First create an owner
        mock_user = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user.id = "123u"
        self.facade.get_user = MagicMock(return_value=mock_user)

        # Create a place
        mock_place = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user)
        mock_place.id ="123p"
        self.facade.get_place = MagicMock(return_value=mock_place)

        mock_review = Review(text = "Amazing stay!", rating= 4, user = mock_user, place=mock_place)
        mock_review.id ="123r"
        self.facade.get_review = MagicMock(return_value=mock_review)


         # Updated data
        updated_data = {'text': "Great stay!", 'rating': 5}

        # Expected updated review
        updated_review = Review(text="Great stay!", rating=5, user=mock_user, place=mock_place)
        updated_review.id = "123r"

        # Mock the repo update method
        self.facade.review_repo.update = MagicMock(return_value=updated_review)
        result = self.facade.update_review("123r", updated_data)
        self.assertEqual(result.text, updated_review.text)
        self.assertEqual(result.rating, updated_review.rating)


    def test_get_all_reviews_multiple(self):
        """Test creating multiple reviews"""
        #------------FIRST OWNER--------------
        # First create owner
        mock_user1 = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user1.id = "123u"
        #self.facade.get_user = MagicMock(return_value=mock_user1)

        # Create a place
        mock_place1 = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user1)
        mock_place1.id ="123p"

        # Create review
        mock_review1 = Review(text = "Amazing stay!", rating= 4, user = mock_user1, place=mock_place1)
        mock_review1.id ="123r"

        #------------SECOND OWNER--------------
        # First create owner
        mock_user2 = User(first_name="Ana", last_name="Loa", email="ana@example.com")
        mock_user2.id = "1234u"

        # Create a place
        mock_place2 = Place(title = "Beach House", description= "A perfect place", price= 50.0, latitude= 70.0, longitude= -100.0, owner= mock_user2)
        mock_place2.id ="1234p"

        # Create review
        mock_review2 = Review(text = "Nice!", rating= 3, user = mock_user2, place=mock_place2)
        mock_review1.id ="1234r"

        # Mock the review_repo.get_all method
        self.facade.review_repo.get_all = MagicMock(return_value=[mock_review1, mock_review2])

        # Call the method
        result = self.facade.get_all_reviews()
        self.assertEqual(len(result), 2)

    def test_get_all_reviews_empty(self):
        """Test to get empty reviews"""
        self.facade.review_repo.get_all = MagicMock(return_value=0)

        result = self.facade.get_all_reviews()
        self.assertEqual(result, 0)

    def test_get_reviews_by_place(self):
        """Test to get reviews by place id"""
          # First create owner
        mock_user1 = User(first_name="Alice", last_name="Noe", email="alice@example.com")
        mock_user1.id = "123u"

        #Create another user
        mock_user2 = User(first_name="Gabe", last_name="Noe", email="Gabe@example.com")
        mock_user2.id = "1234u"

        # Create a place
        mock_place1 = Place(title = "Cozy Apartment", description= "A nice place to stay", price= 100.0, latitude= 37.7749, longitude= -122.4194, owner= mock_user1)
        mock_place1.id ="123p"

        # Create review
        mock_review1 = Review(text = "Amazing stay!", rating= 4, user =mock_user1, place=mock_place1)
        mock_review1.place = mock_place1
        mock_review2 = Review(text = "Nice!", rating= 5, user =mock_user2, place=mock_place1)
        mock_review2.place = mock_place1
    
        self.facade.review_repo.get_all = MagicMock(return_value=[mock_review1, mock_review2])
        result = self.facade.get_reviews_by_place("123p")
        self.assertEqual(len(result), 2)


    def test_get_reviews_by_no_place(self):
        """Test to get reviews by no place"""
        # Simulate no reviews found
        self.facade.review_repo.get_all = MagicMock(return_value=[])
        # Assert that ValueError is raised
        with self.assertRaises(ValueError) as context:
            self.facade.get_reviews_by_place("novalid123")
        self.assertEqual(str(context.exception), "No reviews found for this place")


