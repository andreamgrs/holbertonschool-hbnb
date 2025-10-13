import unittest
from app import create_app
from app.models import User, Place, Review

# --- API Endpoint Tests ---
class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)


# --- User Class Tests ---
class TestUserClass(unittest.TestCase):

    def setUp(self):
        # Standard Jane Doe user
        self.jane = User("Jane", "Doe", "jane.doe@example.com")
        # Admin Jane Doe
        self.admin_jane = User("Jane", "Doe", "jane.doe@example.com")
        self.admin_jane.is_admin = True
        # Sample Place
        self.place = Place("Cafe", "A nice cafe")
        # Sample Review
        self.review = Review("Great!", self.place)

    # --- User Initialization ---
    def test_user_creation_valid(self):
        self.assertEqual(self.jane.first_name, "Jane")
        self.assertEqual(self.jane.last_name, "Doe")
        self.assertEqual(self.jane.email, "jane.doe@example.com")
        self.assertFalse(self.jane.is_admin)
        self.assertEqual(self.jane.places, [])
        self.assertEqual(self.jane.reviews, [])

    def test_user_creation_invalid_first_name(self):
        with self.assertRaises(TypeError):
            User("Jane123", "Doe", "jane.doe@example.com")
        with self.assertRaises(ValueError):
            User("", "Doe", "jane.doe@example.com")

    # --- Email Validation ---
    def test_user_email_validation(self):
        self.assertEqual(self.jane.email, "jane.doe@example.com")
        with self.assertRaises(ValueError):
            self.jane.email = "invalid-email"

    # --- Update Method ---
    def test_user_update_fields(self):
        self.jane.update({
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "is_admin": True
        })
        self.assertEqual(self.jane.first_name, "Jane")
        self.assertEqual(self.jane.last_name, "Doe")
        self.assertEqual(self.jane.email, "jane.doe@example.com")
        self.assertTrue(self.jane.is_admin)

    def test_user_update_invalid_field(self):
        # Should ignore unknown fields and not raise
        self.jane.update({"unknown_field": "value"})
        self.assertFalse(hasattr(self.jane, "unknown_field"))

    # --- Admin-only create_place ---
    def test_create_place_permission(self):
        self.admin_jane.create_place(self.place)
        self.assertIn(self.place, self.admin_jane.places)
        self.assertEqual(self.place.owner, self.admin_jane)

    def test_create_place_permission_denied(self):
        with self.assertRaises(PermissionError):
            self.jane.create_place(self.place)

    # --- Add Review ---
    def test_add_review(self):
        self.jane.add_review(self.review)
        self.assertIn(self.review, self.jane.reviews)
        self.assertEqual(self.review.user, self.jane)

        with self.assertRaises(TypeError):
            self.jane.add_review("not a review")

    # --- is_admin Setter ---
    def test_is_admin_setter(self):
        self.jane.is_admin = True
        self.assertTrue(self.jane.is_admin)

        with self.assertRaises(ValueError):
            self.jane.is_admin = "yes"


if __name__ == "__main__":
    unittest.main()
