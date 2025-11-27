from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Path is /api/v1/auth/login'
@api.route('/login')
class Login(Resource):
    
    # LOGIN AND AUTHENTICATE USER
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        #  Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id),   # only user ID goes here
            additional_claims={"is_admin": user.is_admin}  # extra info here
            )
        
        # Return the JWT token to the client
        return {'access_token': access_token}, 200
    
# Path is '/api/v1/auth/protected'
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        print("jwt------")
        print(get_jwt_identity())
        current_user = get_jwt_identity() # Retrieve the user's identity from the token
        return {'message': f'Hello, user {current_user}'}, 200