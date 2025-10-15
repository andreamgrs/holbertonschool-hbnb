import unittest
from app import create_app
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

class TestUserClass(unittest.TestCase):

    def setUp(self):
        # Standard user
        self.jane = User("Jane", "Doe", "jane.doe@example.com")
        # Admin user
        self.admin_jane = User("Jane", "Doe", "jane.doe@example.com")
        self.admin_jane.is_admin = True
        # Sample Place for testing
        self.place = Place("Cafe", "A nice cafe", 10.0, 10.0, 20.0, self.admin_jane)
        # Sample Review for testing
        self.review = Review("Great!", 5, "place_1", "user_1")

    # --- User creation ---
    def test_user_creation_valid(self):
        self.assertEqual(self.jane.first_name, "Jane")
        self.assertEqual(self.jane.last_name, "Doe")
        self.assertEqual(self.jane.email, "jane.doe@example.com")
        self.assertFalse(self.jane.is_admin)
        self.assertEqual(self.jane.places, [])
        self.assertEqual(self.jane.reviews, [])

    # --- Email validation ---
    def test_user_email_validation(self):
        self.assertEqual(self.jane.email, "jane.doe@example.com")
        with self.assertRaises(ValueError):
            self.jane.email = "invalid-email"

    # --- Update method ---
    def test_user_update_fields(self):
        self.jane.update({
            "first_name": "Janet",
            "last_name": "Smith",
            "email": "janet.smith@example.com",
            "is_admin": True
        })
        self.assertEqual(self.jane.first_name, "Janet")
        self.assertEqual(self.jane.last_name, "Smith")
        self.assertEqual(self.jane.email, "janet.smith@example.com")
        self.assertTrue(self.jane.is_admin)

    def test_user_update_invalid_field(self):
        self.jane.update({"unknown_field": "value"})
        self.assertFalse(hasattr(self.jane, "unknown_field"))


    # --- is_admin setter ---
    def test_is_admin_setter(self):
        self.jane.is_admin = True
        self.assertTrue(self.jane.is_admin)
        with self.assertRaises(ValueError):
            self.jane.is_admin = "yes"

if __name__ == "__main__":
    unittest.main()