from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=False, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_model_updated = api.model('ReviewUpdated', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

# Path is '/api/v1/reviews/'
@api.route('/')
class ReviewList(Resource):

    # CREATE REVIEW
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
         # Get the data from the user in json and convert it into a python dict 
        review_data = api.payload

        # Set the user_id for the review to the current user
        current_user_id = get_jwt_identity()
        review_data['user_id'] = current_user_id
        
        # Logic to prevent an owner reviewing their own place
        place_from_facade = facade.get_place(review_data['place_id'])
        owner_id_from_place = place_from_facade.owner.id
        if owner_id_from_place == current_user_id:
            return {'error': 'You cannot review your own place.'}, 400
        
        # Logic to check if the user has already reviewed the place
        reviews_from_get_place = facade.get_reviews_by_place(review_data['place_id'])
        for review in reviews_from_get_place:
            if review.user.id == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400
        
        # Create new review via facade
        try:
            new_review = facade.create_review(review_data)
        except Exception as e:
                    return {"error": str(e)}, 400
        
        return {'id': new_review.id, 'text': new_review.text,
                'rating': new_review.rating, 'user_id': new_review.user.id,
                'place_id': new_review.place.id}, 201
    
    # GET ALL REVIEWS
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        all_reviews = facade.get_all_reviews()
        reviews_list = []
        for review in all_reviews:
            reviews_list.append({
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            })
        return reviews_list, 200

# Path is '/api/v1/reviews/<review_id>'
@api.route('/<review_id>')
class ReviewResource(Resource):

    # GET SINGLE REVIEW BY ID
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': f"Review with id '{review_id}' not found"}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user.id, 'place_id': review.place.id}, 200

    # UPDATE SINGLE REVIEW BY ID
    @api.expect(review_model_updated, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        update_review_json = request.get_json() # get the json data from request
        if not update_review_json: # if cannot find any request
            return {'error': 'Invalid input'}, 400

        review = facade.get_review(review_id)
        if not review:
            return {'error': f"Review with id '{review_id}' not found"}, 404
        
        # Get dict of jwt payload
        current_user_dict = get_jwt()
        # Extract admin status and user_id from pjwt payload
        admin_status = current_user_dict.get('is_admin', False)
        user_id = current_user_dict.get('sub')
        
        # Only an admin or the user that created the review can update it
        if not admin_status and review.user.id != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        # Update the review via the facade
        try:
            updated_review = facade.update_review(review_id, update_review_json)
        except Exception as e:
            return {"error": str(e)}, 400
        
        return {
            'message': "Review updated successfully",
            'review': {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }
        }, 200
    
    # DELETE A REVIEW
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': f"Review with id '{review_id}' not found"}, 404
        
        # Get dict of jwt payload and extract admin status and user_id
        current_user_dict = get_jwt()
        admin_status = current_user_dict.get('is_admin', False)
        user_id = current_user_dict.get('sub')

        # Only an admin or the user that created the review can delete
        if not admin_status and review.user.id != user_id:
            return {'error': 'Unauthorized action'}, 403

        deleted = facade.delete_review(review_id)
        if deleted:
            return {'message': 'Review deleted successfully'}, 200
        return {'message': 'Review not found'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):

    # GET LIST OF REVIEWS FOR PLACE BY PLACE ID
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
                'rating': review.rating,
                'user_id': review.user.id
            })
        return reviews_list, 200