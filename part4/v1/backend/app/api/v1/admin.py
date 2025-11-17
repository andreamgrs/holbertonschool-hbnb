from flask_restx import Namespace, Resource, fields
from ...services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request


api = Namespace('admin', description='User operations') #creates a “group” of endpoints under /users aka everything in this file will be prefix with users in the url

# Define the user model for input validation and documentation
# All fields required to create a user
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})
# Any fields can be supplied for user update
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user')
})
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# CREATE USER - ADMIN ONLY
@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new user"""
        user_data = api.payload  # JSON body sent by client

        existing_users = facade.get_all_users()
        if not existing_users:
            message = "First user successfully created"
        # Only run the jwt checks if there are already existing users
        else:
            message = "User successfully created"
            # Equivalent to the jwt_required decorator verification
            verify_jwt_in_request()
            current_user = get_jwt()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403        
        
        # Check if email is already in use
        email = user_data.get('email')
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400
        
        try:           
            # call facade
            user = facade.create_user(user_data)

            # return user as dict if successful
            return {
                'message': message,
                'user':
                {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                }
            }, 201

        except ValueError:
            return {'error': 'Email already registered'}, 400
        except TypeError as e:
            # Return e to provide details on which input is invalid
            return {"error": str(e)}, 400

    
# UPDATE SINGLE USER BY ID - ADMIN ONLY
@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        current_user = get_jwt()

        # If 'is_admin' is part of the identity payload
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        
        update_data = request.get_json()
        if not update_data: # if cannot find any request
            return {'error': 'Invalid input'}, 400

        try:
            updated_user = facade.update_user(user_id, update_data) # prevent user from modifying email and password via the facade when update user 
            return {
                'message': 'User updated successfully',
                'user': {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
                }
            }, 200
        
        # catch errors and return e to give more detail
        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 404
        
    # DELETE USER - ADMIN ONLY
    @api.response(200, 'User successfully deleted')
    @api.response(404, 'User not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, user_id):
        """Delete an user information"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            facade.delete_user(user_id)
            return {'message': f'User with id {user_id} successfully deleted'}, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except TypeError as e:
            return {'error': str(e)}, 400
    
        
# ADD AMENITY - ADMIN ONLY
@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt()
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

# MODIFY AMENITY - ADMIN ONLY
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt()
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
        
    # DELETE AMENITY - ADMIN ONLY
    @api.response(200, 'Amenity successfully deleted')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity's information"""
        current_user = get_jwt()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        try:
            facade.delete_amenity(amenity_id)
            return {'message': f'Amenity with id {amenity_id} successfully deleted'}, 200

        except ValueError as e:
            return {'error': str(e)}, 404
        except TypeError as e:
            return {'error': str(e)}, 400

