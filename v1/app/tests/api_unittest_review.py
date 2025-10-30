"""
1. start your server with python3 run.py
2. Create an user POST http://localhost:5000/api/v1/users/ 
3. Create a place POST http://localhost:5000/api/v1/places/ 
4. Create a review POST http://localhost:5000/api/v1/reviews/
5. GET review GET http://localhost:5000/api/v1/reviews/
6. Update review PUT http://localhost:5000api/v1/reviews/<review_id>
7. Get review again to see update GET http://localhost:5000/api/v1/reviews/

"""
#To run python3 -m unittest app/tests/api_unittest_review.py
import json
import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

# testing models 
class TestReviewEndpoints(unittest.TestCase):

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
        print("Status code for user creation:",user_response.status_code)
        print("ID of the owner: {}".format(owner_id))


        # Then, create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id,
            "amenities": []
        })
        self.assertEqual(place_response.status_code, 201)
        #Get the id from places 
        place_data = json.loads(place_response.data)
        place_id = place_data['id']
        print("Status code for place creation:", place_response.status_code)
        print("ID of the place: {}".format(place_id))


        # Create a review
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
        print("Status code for review creation:", review_response.status_code)
        print("ID of review: {}".format(review_id))

        # Update a review
        update_review_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Not bad",
            "rating": 5
        })
        self.assertEqual(update_review_response.status_code, 200)
        print("Status code for update review:", update_review_response.status_code)
        # Verify that data was updated
        updated_data = json.loads(update_review_response.data)
        self.assertEqual(updated_data['message'], "Review updated successfully")
        print("Message for update review: {}".format(updated_data['message']))


        #Check the text is not empty 
        review_empty_text_response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": owner_id,
            "place_id": place_id
        })
        self.assertEqual(review_empty_text_response.status_code, 400) #400 if input data invalid
        error_text_data = json.loads(review_empty_text_response.data)
        print("Status Code of empty text:", review_empty_text_response.status_code)
        print("Message for error text: {}".format(error_text_data['error']))

        #Check the owner_id does not exist
        review_bad_owner_id_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good space",
            "rating": 5,
            "user_id": "no-existance",
            "place_id": place_id
        })
        self.assertEqual(review_bad_owner_id_response.status_code, 400) #404 if does not exist
        error_owner_data = json.loads(review_bad_owner_id_response.data)
        print("Status Code of invalid user id:", review_bad_owner_id_response.status_code)    
        print("Message for invalid user: {}".format(error_owner_data['error']))
        
        #Check the place_id does not exist
        review_bad_place_id_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good space",
            "rating": 5,
            "user_id": owner_id,
            "place_id": "jbcjdcj-jbc"
        })
        self.assertEqual(review_bad_place_id_response.status_code, 400) #404 if does not exist
        error_place_data = json.loads(review_bad_place_id_response.data)
        print("Status Code of invalid place id:", review_bad_place_id_response.status_code)
        print("Message for invalid user: {}".format(error_place_data['error']))
        
        #Check the place_id is empty string
        review_empty_place_response = self.client.post('/api/v1/reviews/', json={
            "text": "Good space",
            "rating": 5,
            "user_id": owner_id,
            "place_id": ""
        })
        self.assertEqual(review_empty_place_response.status_code, 400) #400 if input data invalid
        error_empty_place_data = json.loads(review_empty_place_response.data)
        print("Status Code for place id empty str:", review_empty_place_response.status_code)
        print("Message for place id empty str: {}".format(error_empty_place_data['error']))


