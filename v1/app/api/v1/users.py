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

            # Simulate email uniqueness check (to be replaced by real validation with persistence)
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 409
            
            # call facade
            user = facade.create_user(user_data)


            # return user as dict if successful
            return {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }, 201

        except Exception:
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
    def get(self, user_id): 
        """Get user details by ID"""
        user = facade.get_user(user_id)

        if isinstance(user, dict) and 'status' in user:
            return {'error': user['error']}, user['status']

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200  

    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input')
    def put(self, user_id):
        """Update an existing user"""
        update_data = request.get_json() # get the json data from request
        if not update_data: # if cannot find any request
            return {'error': 'Invalid input'}, 400

        user = facade.get_user(user_id) # confirm can find user before update
        if not user:
            return {'error': 'User not found'}, 404

        # Update fields if provided
        if 'first_name' in update_data:
            user.first_name = update_data['first_name']
        if 'last_name' in update_data:
            user.last_name = update_data['last_name']
        if 'email' in update_data:
            user.email = update_data['email']

        updated_user = facade.update_user(user_id, update_data) # make sure your facade updates the repo
        if not updated_user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200