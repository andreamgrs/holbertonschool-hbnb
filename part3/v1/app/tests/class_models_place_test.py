from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Run by python3 -m app.tests.class_models_test

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    
    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.latitude == 37.7749
    assert place.longitude == -122.4194
    assert place.owner == owner
    assert len(place.reviews) == 0
    assert len(place.amenities) == 0
    print("Place creation test passed!")

def test_title_invalid_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title=1, 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except TypeError as e:
        assert str(e) == "title must be a string"
        print("Title invalid - invalid type test passed")
    
def test_title_invalid_empty():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="", 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except ValueError as e:
        assert str(e) == "title must not be empty"
        print("Title invalid - title empty test passed")

def test_title_invalid_too_long():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        title_str = 101 * "a"
        place = Place(title=title_str, 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except ValueError as e:
        assert str(e) == "title must be less than 100 characters"
        print("Title invalid - title too long test passed")

def test_description_invalid_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description=1, 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except TypeError as e:
        assert str(e) == "description must be a string"
        print("Description invalid - invalid type test passed")

def test_description_invalid_too_long():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        desc_str = 501 * "a"
        place = Place(title="Cozy Apartment", 
                  description=desc_str, 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except ValueError as e:
        assert str(e) == "description must be less than 500 characters"
        print("Description invalid - description too long test passed")

def test_price_invalid_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price="one hundred", 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except TypeError as e:
        assert str(e) == "price must be a float"
        print("Price invalid - invalid type test passed")

def test_price_invalid_negative():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price=-100.0, 
                  latitude=37.7749, 
                  longitude=-122.4194, 
                  owner=owner)
    except ValueError as e:
        assert str(e) == "price must be greater than 0"
        print("Price invalid - price negative test passed")

def test_latitude_invalid_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude="number", 
                  longitude=-122.4194, 
                  owner=owner)
    except TypeError as e:
        assert str(e) == "latitude must be a float"
        print("Latitude invalid - invalid type test passed")

def test_latitude_invalid_out_of_range():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=-100.0, 
                  longitude=-122.4194, 
                  owner=owner)
    except ValueError as e:
        print(e)
        assert str(e) == "latitude must be between -90 and 90"
        print("Latitude invalid - latitude out of range test passed")

def test_longitude_invalid_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude="number", 
                  owner=owner)
    except TypeError as e:
        assert str(e) == "longitude must be a float"
        print("Longitude invalid - invalid type test passed")

def test_longitude_invalid_out_of_range():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=200.0, 
                  owner=owner)
    except ValueError as e:
        assert str(e) == "longitude must be between -180 and 180"
        print("Longitude invalid - longitude out of range test passed")

def test_owner_invalid_type():
    try:
        place = Place(title="Cozy Apartment", 
                  description="A nice place to stay", 
                  price=100.0, 
                  latitude=37.7749, 
                  longitude=100.0, 
                  owner="owner")
    except TypeError as e:
        assert str(e) == "Owner is not an instance of the User class"
        print("Owner invalid - invalid type test passed")

def test_add_review_valid():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Great stay!", rating=5, place_id="123", user_id="s56")
    
    place.add_review(review)
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Add review test passed!")

def test_add_review_invalid_review_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)

    try:
        place.add_review("review")
    except TypeError as e:
        assert str(e) == 'Review not an instance of the Review class'
        print("Add review invalid - invalid review type test passed!")

def test_add_review_invalid_review_already_exists():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    review = Review(text="Great stay!", rating=5, place_id="123", user_id="s56")
    
    place.add_review(review)
    try:
        place.add_review(review)
    except ValueError as e:
        assert str(e) == 'Review already exists'
        print("Add review invalid - review already exists type test passed!")

def test_add_amenity_valid():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    amenity = Amenity(name="Wifi")

    place.add_amenity(amenity)
    assert len(place.amenities) == 1
    assert place.amenities[0].name == "Wifi"
    print("Add amenity test passed!")

def test_add_amenity_invalid_amenity_type():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    amenity = Amenity(name="Wifi")

    try:
        place.add_amenity("amenity")
    except TypeError as e:
        assert str(e) == 'Amenity not an instance of the Amenity class'
        print("Add amenity invalid - invalid amenity type test passed!")

def test_add_amenity_invalid_amenity_already_exists():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    amenity = Amenity(name="Wifi")
    
    place.add_amenity(amenity)
    try:
        place.add_amenity(amenity)
    except ValueError as e:
        assert str(e) == 'Amenity already exists'
        print("Add amenity invalid - amenity already exists type test passed!")

test_place_creation()
test_title_invalid_type()
test_title_invalid_empty()
test_title_invalid_too_long()
test_description_invalid_type()
test_description_invalid_too_long()
test_price_invalid_type()
test_price_invalid_negative()
test_latitude_invalid_type()
test_latitude_invalid_out_of_range()
test_longitude_invalid_type()
test_longitude_invalid_out_of_range()
test_owner_invalid_type()
test_add_review_valid()
test_add_review_invalid_review_type()
test_add_review_invalid_review_already_exists()
test_add_amenity_valid()
test_add_amenity_invalid_amenity_type()
test_add_amenity_invalid_amenity_already_exists()
