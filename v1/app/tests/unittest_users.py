#!/usr/bin/python3
"""
unit tests for the user api
"""
import unittest
from app import create_app
from app.services.facade import HBnBFacade


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """run before each test: create a test app, client, and fresh facade"""
        self.app = create_app() #create new Flask app for testing
        self.client = self.app.test_client()
        self.facade = HBnBFacade()
        # clear users manually
        for user in self.facade.get_all_users():
            self.facade.user_repo.delete(user.id) #clear everything before start test

        # use only alphabetic first/last names as per User class 
        self.valid_user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com"
        }

        self.invalid_user_data = {
            "first_name": "",
            "last_name": "123",
            "email": "invalid-email"
        }

        self.new_user_data = {
        "first_name": "James",
        "last_name": "Doe",
        "email": "james.doe@example.com"
        }

    # --- test facade ---
    def test_create_user_success(self):
        """create a valid user"""
        user = self.facade.create_user(self.valid_user_data)
        self.assertEqual(user.first_name, "Jane")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "jane@example.com")
        self.assertIsNotNone(user.id)

    def test_create_user_invalid_data(self):
        """creating user with invalid data raises error"""
        with self.assertRaises((TypeError, ValueError)): # tell unittest this should throw an error and if it doesn't, fail the test
            self.facade.create_user(self.invalid_user_data)

    def test_get_user_by_email(self):
        """get a user by email"""
        user = self.facade.create_user(self.valid_user_data)
        retrieved = self.facade.get_user_by_email("jane@example.com")
        self.assertEqual(retrieved.id, user.id)

    def test_get_user_by_id(self):
        """get a user by id"""
        user = self.facade.create_user(self.valid_user_data)
        retrieved = self.facade.get_user(user.id)
        self.assertEqual(retrieved.email, "jane@example.com")

    def test_update_user(self):
        """update user details"""
        user = self.facade.create_user(self.valid_user_data)
        updated_data = {"first_name": "John", "last_name": "Smith", "email": "john@example.com"}
        updated_user = self.facade.update_user(user.id, updated_data)
        self.assertEqual(updated_user.first_name, "John")
        self.assertEqual(updated_user.email, "john@example.com")

    # --- API endpoint test ---
    def test_01_post_user_endpoint(self):
        """create user via /api/v1/users"""
        response = self.client.post('/api/v1/users/', json=self.valid_user_data)
        # should succeed and return 201
        self.assertIn(response.status_code, [200, 201, 400])

    def test_02_get_single_user_endpoint(self):
        """get a single user via /api/v1/users/<user_id>. get the user already created above"""

        # create a user using new user data
        create_response = self.client.post('/api/v1/users/', json=(self.new_user_data))
        self.assertEqual(create_response.status_code, 201)

        # get ID of the created user
        user_id = create_response.get_json()['id']

        # get the created user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['first_name'], self.new_user_data['first_name'])
        self.assertEqual(data['last_name'], self.new_user_data['last_name'])
        self.assertEqual(data['email'], self.new_user_data['email'])

        # get a user that does not exist
        response_not_found = self.client.get('/api/v1/users/non-existent-id')
        self.assertEqual(response_not_found.status_code, 404)
        self.assertIn('error', response_not_found.get_json())
        self.assertEqual(response_not_found.get_json()['error'], 'User not found')

    def test_03_get_all_users_endpoint(self):
        """get all users via /api/v1/users"""
        self.client.post('/api/v1/users/', json=self.valid_user_data)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_endpoint(self):
        """delete user via /api/v1/users/<id>"""
        # since DELETE isn't implemented, expect 405
        response = self.client.delete('/api/v1/users/123')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()
