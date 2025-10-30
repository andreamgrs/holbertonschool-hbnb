from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource): #with resource we manage the methods GET POST PUT DELETE
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        # Placeholder for the logic to register a new review
        try:
        # Get the data from the user in json and convert it into a python dict 
            review_data = api.payload
            #We send the data into facade
            new_review = facade.create_review(review_data) #in method create store data in the repo, make sure user exist
        except Exception as e:
                    return {"error": "Invalid input data"}, 400
        return {'id': new_review.id, 'text': new_review.text, 'rating': new_review.rating, 'user_id': new_review.user.id, 'place_id': new_review.place.id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        reviews_list = []
        for review in all_reviews:
            reviews_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
            })
        return reviews_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user': review.user_id, 'place': review.place_id}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        update_review_json = request.get_json() # get the json data from request
        if not update_review_json: # if cannot find any request
            return {'error': 'Invalid input'}, 400

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        updated_review = facade.update_review(review_id, update_review_json)
        return {
            'message': "Review updated successfully"
        }, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
        except ValueError:
            return {'error': "No reviews found for this place"}, 404
        
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            })
        return reviews_list, 200