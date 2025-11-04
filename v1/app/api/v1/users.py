from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations') #creates a “group” of endpoints under /users aka everything in this file will be prefix with users in the url

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# CREATE USER
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
                'message': 'User successfully created',
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
    
# GET SINGLE USER BY ID
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
        
        
    # UPDATE SINGLE USER BY ID
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, user_id):
        """Update a user's information"""
        current_user_id = get_jwt_identity()
        print(f"JWT user: {current_user_id}")
        print(f"Route user: {user_id}")

        if user_id  != current_user_id: # prevent modify other user data
            return {'error': 'Unauthorized action.'}, 403
        
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