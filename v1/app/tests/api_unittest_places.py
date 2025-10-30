import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
import json


# --- API Endpoint Tests ---
class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_01_get_all_places_empty_return_200_and_empty_list(self):
        response_places = self.client.get('/api/v1/places/')
        self.assertEqual(json.loads(response_places.data), [])
        self.assertEqual(response_places.status_code, 200)

    def test_02_create_place_valid_return_201_and_place_data(self):
        # Create user and get owner_id
        response_user = self.client.post('/api/v1/users/', json={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            })
        user_data = json.loads(response_user.data)
        test_owner_id = user_data["id"]
        # Create place
        request_place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": test_owner_id,
            "amenities": []
            }
        response_places = self.client.post('/api/v1/places/', json=request_place_data)
        response_place_data = json.loads(response_places.data)
        test_place_id = response_place_data["id"]
        # Remove id from response for comparison with request
        del response_place_data["id"]
        del request_place_data["amenities"]
        self.assertEqual(request_place_data, response_place_data)
        self.assertEqual(response_places.status_code, 201)

    def test_03_create_place_invalid_title_return_400_and_error_message(self):
        # Get id of the first user
        response_user = self.client.get('/api/v1/users/')
        user_data = json.loads(response_user.data)
        test_owner_id = user_data[0].get("id")
        # Create place data with invalid title
        response_places = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "A nice place to stay",
            "price": 10.0,
            "latitude": 10.0,
            "longitude": -20.0,
            "owner_id": test_owner_id,
            "amenities": []
            })
        response_place_data = json.loads(response_places.data)
        self.assertEqual(response_places.status_code, 400)
        self.assertEqual(response_place_data, {'error': 'title must not be empty'})

    def test_04_create_place_invalid_price_return_400_and_error_message(self):
        # Get id of the first user
        response_user = self.client.get('/api/v1/users/')
        user_data = json.loads(response_user.data)
        test_owner_id = user_data[0].get("id")
        # Create place data with invalid title
        response_places = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -10.0,
            "latitude": 10.0,
            "longitude": -20.0,
            "owner_id": test_owner_id,
            "amenities": []
            })
        response_place_data = json.loads(response_places.data)
        self.assertEqual(response_places.status_code, 400)
        self.assertEqual(response_place_data, {'error': 'price must be greater than 0'})

    def test_05_create_place_invalid_latitude_return_400_and_error_message(self):
        # Get id of the first user
        response_user = self.client.get('/api/v1/users/')
        user_data = json.loads(response_user.data)
        test_owner_id = user_data[0].get("id")
        # Create place data with invalid title
        response_places = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 10.0,
            "latitude": 100.0,
            "longitude": -20.0,
            "owner_id": test_owner_id,
            "amenities": []
            })
        response_place_data = json.loads(response_places.data)
        self.assertEqual(response_places.status_code, 400)
        self.assertEqual(response_place_data, {'error': 'latitude must be between -90 and 90'})

    def test_06_create_place_invalid_title_return_400_and_error_message(self):
        # Get id of the first user
        response_user = self.client.get('/api/v1/users/')
        user_data = json.loads(response_user.data)
        test_owner_id = user_data[0].get("id")
        # Create place data with invalid title
        response_places = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 10.0,
            "latitude": 10.0,
            "longitude": -200.0,
            "owner_id": test_owner_id,
            "amenities": []
            })
        response_place_data = json.loads(response_places.data)
        self.assertEqual(response_places.status_code, 400)
        self.assertEqual(response_place_data, {'error': 'longitude must be between -180 and 180'})

    def test_07_create_place_invalid_owner_id_return_400_and_error_message(self):
        # Get id of the first user
        response_user = self.client.get('/api/v1/users/')
        user_data = json.loads(response_user.data)
        test_owner_id = user_data[0].get("id")
        # Create place data with invalid title
        response_places = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -10.0,
            "latitude": 100.0,
            "longitude": -200.0,
            "owner_id": "0387c53c-7891-4022-98bb-55030eea5f3f",
            "amenities": []
            })
        response_place_data = json.loads(response_places.data)
        self.assertEqual(response_places.status_code, 400)
        self.assertEqual(response_place_data, {'error': 'User not found'})

    def test_08_create_place_invalid_amenity_id_return_400_and_error_message(self):
        # Get id of the first user
        response_user = self.client.get('/api/v1/users/')
        user_data = json.loads(response_user.data)
        test_owner_id = user_data[0].get("id")
        # Create place data with invalid title
        response_places = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 10.0,
            "latitude": 10.0,
            "longitude": -20.0,
            "owner_id": test_owner_id,
            "amenities": ["0387c53c-7891-4022-98bb-55030eea5f3f"]
            })
        response_place_data = json.loads(response_places.data)
        self.assertEqual(response_places.status_code, 400)
        self.assertEqual(response_place_data, {'error': 'Amenity with ID 0387c53c-7891-4022-98bb-55030eea5f3f not found'})

    def test_09_get_places_with_one_place_return_200_and_place_data(self):
        # Request data is from test_02 which has already been posted
        request_place_data = {
            "title": "Cozy Apartment",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
            }
        response = self.client.get('/api/v1/places/')
        response_data = json.loads(response.data)
        response_place = response_data[0]
        del response_place["id"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(request_place_data, response_place)

    def test_10_get_place_data_using_id_return_200_and_expected_response(self):
        # Get place id of posted place (i.e. first place in get all)
        get_places_response = self.client.get('/api/v1/places/')
        get_places_response_data = json.loads(get_places_response.data)
        place_id = get_places_response_data[0].get("id")
        # Get owner id of posted user (i.e. first owner in get all)
        get_users_reponse = self.client.get('/api/v1/users/')
        get_users_data = json.loads(get_users_reponse.data)
        owner_id = get_users_data[0].get("id")
        # Use place id to construct endpoint
        endpoint = '/api/v1/places/' + str(place_id)
        response = self.client.get(endpoint)
        response_data = json.loads(response.data)
        expected_response = {
            "id": place_id,
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner": {
                "id": owner_id,
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            },
            "amenities": []
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_response)
    
    ### Update Place Tests ###
    def test_11_update_place_invalid_title_return_400(self):
        # Get place id for endpoint construction
        get_places_response = self.client.get('/api/v1/places/')
        get_places_response_data = json.loads(get_places_response.data)
        place_id = get_places_response_data[0].get("id")
        endpoint = '/api/v1/places/' + str(place_id)
        response = self.client.put(endpoint, json={
            "title": "",
            "description": "A nice place to stay",
            "price": 10.0})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'error': 'title must not be empty'})

    def test_12_update_place_invalid_price_return_400(self):
        # Get place id for endpoint construction
        get_places_response = self.client.get('/api/v1/places/')
        get_places_response_data = json.loads(get_places_response.data)
        place_id = get_places_response_data[0].get("id")
        endpoint = '/api/v1/places/' + str(place_id)
        response = self.client.put(endpoint, json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": -10.0})
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data, {'error': 'price must be greater than 0'})

    def test_13_update_place_not_found_return_404(self):
        # provide random place id
        endpoint = '/api/v1/places/' + '7c1acc68-76a9-4a3c-8949-9c4c36469817'
        response = self.client.put(endpoint, json={
            "title": "Luxury Condo",
            "description": "An upscale location",
            "price": 200.0
        })
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data, {"error": "Place not found"})

    def test_14_update_place_return_200(self):
        get_places_response = self.client.get('/api/v1/places/')
        get_places_response_data = json.loads(get_places_response.data)
        place_id = get_places_response_data[0].get("id")
        endpoint = '/api/v1/places/' + str(place_id)
        response = self.client.put(endpoint, json={
            "title": "Luxury Condo",
            "description": "An upscale location",
            "price": 200.0
        })
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
