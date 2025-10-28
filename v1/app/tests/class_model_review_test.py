import unittest
from app.models.review import Review
# Run by python3 -m app.tests.class_model_review_test

class TestReviewClass(unittest.TestCase):

    def test_01_valid_review_creation(self):
        review = Review(text="Great stay!", rating=5, place_id="123", user_id="s56")
        self.assertEqual(review.text, "Great stay!")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.place_id, "123")
        self.assertEqual(review.user_id, "s56")

    def test_02_empty_text_raises_type_error(self):
        with self.assertRaises(TypeError) as e:
            Review(text="", rating=4, place_id="place_123", user_id="user_456")
        self.assertEqual(str(e.exception), "Text must be a string and not an empty string")


    def test_03_invalid_rating_low(self):
        with self.assertRaises(ValueError) as e:
            Review("Nice", 0, "place_123", "user_456")
        self.assertEqual(str(e.exception), "Rating must be between 1 and 5")

    def test_04_invalid_rating_high(self):
        with self.assertRaises(ValueError) as e:
            Review("Nice", 6, "place_123", "user_456")
        self.assertEqual(str(e.exception), "Rating must be between 1 and 5")

    def test_05_invalid_place_id_type(self):
        with self.assertRaises(TypeError) as e:
            Review("Nice", 4, 123, "user_456")
        self.assertEqual(str(e.exception), "Place ID must be a non-empty string")

    def test_06_empty_place_id(self):
        with self.assertRaises(TypeError) as e:
            Review("Nice", 4, "", "user_456")
        self.assertEqual(str(e.exception), "Place ID must be a non-empty string")

    def test_07_invalid_user_id_type(self):
        with self.assertRaises(TypeError) as e:
            Review("Nice", 4, "place_123", 789)
        self.assertEqual(str(e.exception), "User ID must be a non-empty string")

    def test_08_empty_user_id(self):
        with self.assertRaises(TypeError) as e:
            Review("Nice", 4, "place_123", "")
        self.assertEqual(str(e.exception), "User ID must be a non-empty string")


if __name__ == "__main__":
    unittest.main()
