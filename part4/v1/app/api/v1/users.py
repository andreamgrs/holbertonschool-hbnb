from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request


api = Namespace('users', description='User operations') #creates a “group” of endpoints under /users aka everything in this file will be prefix with users in the url

user_model = api.model('User', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email address')
})

# Path is '/api/v1/users/'
@api.route('/')
class UserList(Resource):

    # GET ALL USER 
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve all users"""
        all_users = facade.get_all_users()
        users_list = []
        for user in all_users:
            users_list.append({
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })
        return users_list, 200
    
# Path is '/api/v1/user/<user_id>'
@api.route('/<user_id>')
class UserResource(Resource):

    # GET SINGLE USER BY ID
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid request')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            return {
                'message': 'User details retrieved successfully',
                'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
                }
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except TypeError as e:
            return {'error': str(e)}, 404