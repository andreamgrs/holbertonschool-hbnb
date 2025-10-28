import unittest
from app.models.amenity import Amenity
# Run by python3 -m app.tests.class_model_amenity_test

class TestAmenityClass(unittest.TestCase):

    def test_01_valid_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_02_invalid_input_spaces_raises_value_error(self):
        with self.assertRaises(ValueError) as e:
            amenity = Amenity(name="   ")
        self.assertEqual(str(e.exception), "Invalid name length!")
    
    def test_03_invalid_input_too_long_raises_value_error(self):
        with self.assertRaises(ValueError) as e:
            amenity = Amenity(name="a" * 51)
        self.assertEqual(str(e.exception), "Invalid name length!")

if __name__ == "__main__":
    unittest.main()
