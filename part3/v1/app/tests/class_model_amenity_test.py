import unittest
from app.models.amenity import Amenity
# Run by python3 -m app.tests.class_model_amenity_test

# TEST 1: Create amenity successfully
def test_amenity_creation():
    amenity = Amenity("Pool")
    assert amenity.name == "Pool"
    print("Amenity creation test passed!")

# TEST 2: Amenity name is not a string
def test_amenity_name_not_string():
    try:
        Amenity(123)
    except TypeError as e:
        assert str(e) == "Amenity name must be a string"
        print("Amenity name not string test passed")

# TEST 3: Amenity name empty string
def test_amenity_name_empty():
    try:
        Amenity("")
    except ValueError as e:
        assert str(e) == "Invalid name length!"
        print("Amenity name empty string test passed")

# TEST 4: Amenity name too long
def test_amenity_name_too_long():
    try:
        long_name = "A" * 51
        Amenity(long_name)
    except ValueError as e:
        assert str(e) == "Invalid name length!"
        print("Amenity name too long test passed")

test_amenity_creation()
test_amenity_name_empty()
test_amenity_name_not_string()
test_amenity_name_too_long()
