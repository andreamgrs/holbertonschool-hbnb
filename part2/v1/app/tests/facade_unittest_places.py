#!/usr/bin/python3
"""
Unit tests for the HBnB Facade layer for the places model
Run from project root with:
python3 -m unittest app/tests/facade_test_places.py
"""
import unittest
from unittest.mock import ANY
from app.services.facade import HBnBFacade
import json


class TestHBnBFacade(unittest.TestCase):

    def setUp(self):
        """Set up fresh facade instance for each test"""
        self.facade = HBnBFacade()
 
    def test_create_place(self):
        """Test creating a place"""
        # First create an owner
        owner = self.facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        })
        
        # Create valid place data
        place_data = {
            'title': 'Cozy Apartment',
            'description': 'A nice place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': owner.id
        }

        # Call facade to create place
        place = self.facade.create_place(place_data)
        # Validate return data from the facade
        self.assertEqual(place.title, 'Cozy Apartment')
        self.assertEqual(place.description, 'A nice place')
        self.assertEqual(place.price, 100.0)
        self.assertEqual(place.latitude, 37.7749)
        self.assertEqual(place.longitude, -122.4194)
        self.assertEqual(place.owner.id, owner.id)


    def test_create_place_invalid(self):
        """Test creating a place with invalid data"""
        owner = self.facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        })
        # Create place data with invalid title
        place_data = {
            'title': '',
            'description': 'A nice place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': owner.id,
        }
        # Check that create place raises a value error
        self.assertRaises(ValueError, self.facade.create_place, place_data)

        # Change title to valid and make price invalid
        place_data['title'] = 'Cozy Apartment'
        place_data['price'] = -50.0
        self.assertRaises(ValueError, self.facade.create_place, place_data)

    def test_get_all_places(self):
        # Create an owner and two places
        owner = self.facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        })
        place_data_1 = {
            'title': 'Cozy Apartment',
            'description': 'A nice place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': owner.id,
        }
        create_place_1 = self.facade.create_place(place_data_1)
        place_data_2 = {
            'title': 'Spacious House',
            'description': 'Perfect for a family holiday',
            'price': 200.0,
            'latitude': 33.8727,
            'longitude': 151.2057,
            'owner_id': owner.id,
        }
        create_place_2 = self.facade.create_place(place_data_2)

        # Call get all users
        place_list = self.facade.get_all_places()
        get_place_1 = place_list[0]
        get_place_2 = place_list[1]
        get_place_1.id = ANY
        get_place_2.id = ANY
        self.assertEqual(create_place_1, get_place_1)
        self.assertEqual(create_place_2, get_place_2)


    def test_get_place(self):
        # Create an owner and place
        owner = self.facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        })
        place_data = {
            'title': 'Cozy Apartment',
            'description': 'A nice place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': owner.id,
        }
        create_place = self.facade.create_place(place_data)
      
        # Get place using place id
        get_place = self.facade.get_place(create_place.id)

        # Compare data from create place and get place
        self.assertEqual(create_place, get_place)

    def test_update_place(self):
         # Create an owner and place
        owner = self.facade.create_user({
            'first_name': 'Alice',
            'last_name': 'Smith',
            'email': 'alice@example.com'
        })
        place_data = {
            'title': 'Cozy Apartment',
            'description': 'A nice place',
            'price': 100.0,
            'latitude': 37.7749,
            'longitude': -122.4194,
            'owner_id': owner.id,
        }
        create_place = self.facade.create_place(place_data)

        # Update place title, description, and price
        updated_place_data = {
            'title': 'Luxury Condo',
            'description': 'An upscale location',
            'price': 150.0
        }
        update_place = self.facade.update_place(create_place.id, updated_place_data)

        # Confirm title, desciption, and price have been updated
        self.assertEqual(update_place.title, updated_place_data["title"])
        self.assertEqual(update_place.description, updated_place_data["description"])
        self.assertEqual(update_place.price, updated_place_data["price"])
        
        # Check other attributes are still the same
        self.assertEqual(update_place.latitude, create_place.latitude)
        self.assertEqual(update_place.longitude, create_place.longitude)
        self.assertEqual(update_place.owner, create_place.owner)