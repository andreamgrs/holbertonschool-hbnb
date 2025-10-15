import json
import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        #First create user 
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        #raw content of the HTTP response. If the server returns JSON, response.data will contain that JSON as a byte string.
        user_data = json.loads(user_response.data) 
        owner_id = user_data['id']
        self.assertEqual(user_response.status_code, 201) #It verify that user_response.status_code is equal to 201, 
        #user_data = user_response.get_json()
        #user_id = user_data.get("id")
        #self.assertIsNotNone(user_id) #check that user_id is not None
        print("ID of the owner: {}".format(owner_id))


        # Then, create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id
        })
        self.assertEqual(place_response.status_code, 201)
        #Get the id from places 
        place_data = json.loads(place_response.data)
        place_id = place_data['id']
        print("ID of the place: {}".format(place_id))


        # Now, create the review
        review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": owner_id,
            "place_id": place_id
        })
        self.assertEqual(review_response.status_code, 201)
         #Get the id from the review
        review_data = json.loads(review_response.data)
        review_id = review_data['id']
        print("ID of review: {}".format(review_id))

