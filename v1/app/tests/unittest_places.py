import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
import json

# --- API Endpoint Tests ---
class TestPlaceEndpoints(unittest.TestCase):
    test_owner_id = ''
    test_place_id = ''

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_01_get_all_places_empty(self):
        response_places = self.client.get('/api/v1/places/')
        self.assertEqual(json.loads(response_places.data), [])
        self.assertEqual(response_places.status_code, 200)

    def test_02_create_place(self):
        global test_owner_id
        global test_place_id
        # Create user first
        response_user = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response_user.status_code, 201)
        # Get user id to use as owner id
        user_data = json.loads(response_user.data)
        test_owner_id = user_data["id"]
        # Create place
        request_place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": test_owner_id
            }
        response_places = self.client.post('/api/v1/places/', json=request_place_data)
        response_place_data = json.loads(response_places.data)
        test_place_id = response_place_data["id"]
        # Remove id from response for comparison with request
        del response_place_data["id"]
        self.assertEqual(request_place_data, response_place_data)
        self.assertEqual(response_places.status_code, 201)

    def test_03_create_place_invalid_data(self):
        response_places = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -10,
            "latitude": 100.0,
            "longitude": -200.0,
            "owner_id": test_owner_id
            })
        self.assertEqual(response_places.status_code, 400)

    def test_04_get_place_list_one_place(self):
        # Request data is from test_02
        request_place_data = {
            "title": "Cozy Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
            }
        response = self.client.get('/api/v1/places/')
        response_data = json.loads(response.data)
        # Get id of first place in list
        response_place = response_data[0]
        self.assertEqual(response_place['id'], test_place_id)
        # Remove id from response for comparison with request
        del response_place['id']
        self.assertEqual(request_place_data, response_place)

    def test_05_get_place_data(self):
        endpoint = '/api/v1/places/' + str(test_place_id)
        response = self.client.get(endpoint)
        response_data = json.loads(response.data)
        expected_response = {
            "id": test_place_id,
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner": {
                "id": test_owner_id,
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            }
        }
        self.assertEqual(response_data, expected_response)
    
    # Update place data
    def test_06_update_place_invalid_input(self):
        endpoint = '/api/v1/places/' + str(test_place_id)
        response = self.client.put(endpoint, json='')
        self.assertEqual(response.status_code, 400)

    def test_07_update_place_not_found(self):
        # provide random place id
        endpoint = '/api/v1/places/' + '7c1acc68-76a9-4a3c-8949-9c4c36469817'
        response = self.client.put(endpoint, json={
            "title": "Luxury Condo",
            "description": "An upscale location",
            "price": 200.0
        })
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    def test_08_update_place(self):
        endpoint = '/api/v1/places/' + str(test_place_id)
        response = self.client.put(endpoint, json={
            "title": "Luxury Condo",
            "description": "An upscale location",
            "price": 200.0
        })
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
