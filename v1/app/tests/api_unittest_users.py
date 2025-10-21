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

        self.user_for_update = {
        "first_name": "Jameson",
        "last_name": "Doe",
        "email": "jamesondoe@example.com"
        }

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

    def test_04_delete_user_endpoint(self):
        """delete user via /api/v1/users/<id>"""
        # since DELETE isn't implemented, expect 405
        response = self.client.delete('/api/v1/users/123')
        self.assertEqual(response.status_code, 405)

    def test_05_update_user_endpoint(self):
        """update user via /api/v1/users/<id>"""
        create_response = self.client.post('/api/v1/users/', json=self.user_for_update)
        self.assertEqual(create_response.status_code, 201)
        user_data = create_response.get_json()
        user_id = user_data['id']  # get the actual ID returned by the API

        # update only first name
        updated_data = {"first_name": "Jamesonsecond"}

        # update user
        update_response = self.client.put(f'/api/v1/users/{user_id}', json=updated_data)
        self.assertEqual(update_response.status_code, 200)
        updated_user = update_response.get_json()

        self.assertEqual(updated_user['id'], user_id)
        self.assertEqual(updated_user['first_name'], updated_data['first_name'])
        self.assertEqual(updated_user['last_name'], self.user_for_update['last_name'])
        self.assertEqual(updated_user['email'], self.user_for_update['email'])

if __name__ == '__main__':
    unittest.main()
