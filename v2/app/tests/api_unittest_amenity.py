import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
import json
###
# --- API Endpoint Tests ---
class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        amenity_response = self.client.post('/api/v1/amenities/', json={
            "name": "bed",
        })
        amenity_data = json.loads(amenity_response.data) 
        self.assertEqual(amenity_response.status_code, 201) 