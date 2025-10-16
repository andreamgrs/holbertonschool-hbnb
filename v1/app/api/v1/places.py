from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Adding the review model
review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        payload_data = api.payload #contains the JSON body the user sent
        # Perform basic input validation - move this
        if not payload_data['title'] \
        or payload_data['latitude'] < -90 or payload_data['latitude'] > 90 \
        or payload_data['longitude'] < -180 or payload_data['longitude'] > 180 \
        or payload_data['price'] < 0:
            return 'Invalid input data', 400
        owner = facade.get_user(payload_data["owner_id"])
        if owner is None:
           return  {'error': 'Owner not found'}, 404
        # Convert payload data to place data
        place_data = payload_data
        del place_data["owner_id"]
        place_data["owner"] = owner
        new_place = facade.create_place(place_data)
        return {'id': new_place.id, 'title': new_place.title, 'description': new_place.description,
                'price': new_place.price, 'latitude': new_place.latitude, 'longitude': new_place.longitude,
                'owner_id': new_place.owner.id}, 201
    

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        all_places = facade.get_all_places()
        places_list = []
        for place in all_places:
            places_list.append({
                'id': place.id,
                'title': place.title,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude})
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                }}
        # need to add amenities to the return dict once the class is implemented

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        update_data = request.get_json() # get the json data from request
        if not update_data: # if cannot find any request
            return {'error': 'Invalid input'}, 400

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Update fields if provided
        if 'title' in update_data:
            place.title = update_data['title']
        if 'description' in update_data:
            place.description = update_data['description']
        if 'price' in update_data:
            place.price = update_data['price']

        updated_place = facade.update_place(place_id, update_data)
        return {"message": "Place updated successfully"}, 200
    
