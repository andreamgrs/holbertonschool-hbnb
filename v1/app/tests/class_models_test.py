from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Run by python3 -m app.tests.class_models_test

# TEST 1: Creating user successfully 
def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

# TEST 2: User first name is not string

def test_first_name_not_string():
    try:
        User(first_name=123, last_name="Smith", email="alice@example.com")
    except TypeError as e:
        assert str(e) == "first name must be a string"
        print("Test first name not string passed")

    # Adding a review
    review = Review(text="Great stay!", rating=5, place="123", user_id="s56")
    place.add_review(review)

def test_first_name_too_long():
    try:
        long_name = "L" * 51

        user = User(first_name=long_name, last_name="Smith", email="alice.smith@example.com")

    except ValueError as e:
        assert str(e) == "first name has max length of 50 chars"
        print("First name too long test passed")

# TEST 4: User last name is not string

def test_last_name_not_string():
    try:
        User(first_name="Alice", last_name=123, email="alice@example.com")
    except TypeError as e:
        assert str(e) == "last name must be a string"
        print("Test last name not string passed")

# TEST 5: User last name is too long

def test_last_name_too_long():
    try:
        long_name = "L" * 51

        user = User(first_name="Alice", last_name=long_name, email="alice.smith@example.com")

    except ValueError as e:
        assert str(e) == "last name has max length of 50 chars"
        print("Last name too long test passed")

# TEST 6: User email is invalid
def test_user_invalid_email():
    try:
        User(first_name="Alice", last_name="Smith", email="invalid-email")
    except ValueError as e:
        assert str(e) == "Invalid email"
        print("User with invalid email format test passed")

test_user_creation()
test_first_name_not_string()
test_first_name_too_long()
test_last_name_not_string()
test_last_name_too_long()
test_user_invalid_email()