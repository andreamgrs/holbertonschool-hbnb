from app.models.review import Review
from app.models.review import Place
from app.models.user import User

def test_review():
    try:
        place = Place("Beach house")
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
        review = Review("Great food", 5, place, user)
        print("Review created successfully!")
        print("Text:", review.text)
        print("Rating:", review.rating)
    except Exception as e:
        print("Error:", e)
test_review()