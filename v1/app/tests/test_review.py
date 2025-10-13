from app.models.review import Review
from app.models.place import Place
from app.models.user import User

def test_review():
    try:
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=user)
        review = Review("Great food", 5, place, user)
        print("Review created successfully!")
        print("Text:", review.text)
        print("Rating:", review.rating)
        print("User:", user.first_name)
        print("Place title:", place.title)
    except Exception as e:
        print("Error:", e)
test_review()