from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# CREATE AMENITY
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 400

    # GET ALL AMENITIES
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        all_amenities = facade.get_all_amenities()

        amenities_list = []
        for amenity in all_amenities:
            amenities_list.append({
                'id': amenity.id,
                'name': amenity.name
            })

        return amenities_list, 200

# GET SINGLE AMENITY USING ID
@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except TypeError as e:
            return {'error': str(e)}, 404
        

    # UPDATE SINGLE AMENITY BY ID
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        update_data = request.get_json()
        if not update_data:
            return {'error': 'Invalid input'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, update_data)
            return {
                'message': 'Amenity updated successfully',
                'amenity': {
                    'id': updated_amenity.id,
                    'name': updated_amenity.name
                }
            }, 200
        
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 404
