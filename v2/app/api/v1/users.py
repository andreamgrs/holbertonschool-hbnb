from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('users', description='User operations') #creates a “group” of endpoints under /users aka everything in this file will be prefix with users in the url

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload  # JSON body sent by client

        try:           
            # call facade
            user = facade.create_user(user_data)


            # return user as dict if successful
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 201

        except ValueError:
            return {'error': 'Email already registered'}, 400
        except TypeError:
            return {"error": "Invalid input data"}, 400

    
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
    

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid request')
    def get(self, user_id):
        """Get user details by ID"""
        try:
            user = facade.get_user(user_id)
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 200

        except ValueError:
            # raised for invalid UUID
            return {'error': 'User id not valid'}, 400
        except TypeError:
            # raised when user not found
            return {'error': 'User not found'}, 404
            

    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        """Update a user's information"""
        update_data = request.get_json()
        if not update_data: # if cannot find any request
            return {'error': 'Invalid input'}, 400

        user = facade.get_user(user_id)
        if not user:
             return {'error': 'User not found'}, 404
        updated_user = facade.update_user(user_id, update_data)
    
        return {
            'message': "User updated successfully"
        }, 200