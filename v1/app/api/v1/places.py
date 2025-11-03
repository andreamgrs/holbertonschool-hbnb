from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from flask import request

api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

# Define the place model for the update method
update_place_model = api.model('Place', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String('Description of the place'),
    'price': fields.Float(description='Price per night'),
})


# CREATE PLACE
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        payload_data = api.payload #contains the JSON body the user sent
        current_user = get_jwt_identity()
        payload_data["owner_id"] = current_user
        try:
            new_place = facade.create_place(payload_data)
        except Exception as e:
            return {"error": str(e)}, 400
        
        return {'id': new_place.id, 'title': new_place.title, 'description': new_place.description,
                'price': new_place.price, 'latitude': new_place.latitude, 'longitude': new_place.longitude,
                'owner_id': new_place.owner.id}, 201
    

    # GET ALL PLACES
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

# GET SINGLE PLACE BY ID
@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': f"Place with id '{place_id}' not found"}, 404
        
        ammenity_list = []
        for amenity in place.amenities:
            amenity_dict = {"id": amenity.id, "name": amenity.name}
            ammenity_list.append(amenity_dict)
        
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
                },
                'amenities': ammenity_list}

    # UPDATE SINGLE PLACE BY ID
    @api.expect(update_place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        update_data = request.get_json() # get the json data from request
        if not update_data: # if cannot find any request
            return {'error': 'Invalid input'}, 400
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': f"Place with id '{place_id}' not found"}, 404

        current_user = get_jwt_identity()
        print(f"current user is {current_user}")
        print(f"owner id is {place.owner.id}")
        if current_user != place.owner.id:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_place = facade.update_place(place_id, update_data)
        except Exception as e:
            return {"error": str(e)}, 400
        
        return {"message": "Place updated successfully"}, 200
    