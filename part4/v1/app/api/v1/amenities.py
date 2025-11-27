from flask_restx import Namespace, Resource, fields
from ...services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Path is '/api/v1/amentities/'
@api.route('/')
class AmenityList(Resource):
    
    # GET ALL AMENITIES - PUBLIC
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

# Path is '/api/v1/amentities/<amenity_id>'
@api.route('/<amenity_id>')
class AmenityResource(Resource):

    # GET SINGLE AMENITY USING ID
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
        