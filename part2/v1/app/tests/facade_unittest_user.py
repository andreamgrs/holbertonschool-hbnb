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
