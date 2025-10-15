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
        payload = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        }
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 201)
