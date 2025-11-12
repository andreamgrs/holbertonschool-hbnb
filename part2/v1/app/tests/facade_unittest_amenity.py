#!/usr/bin/python3
"""
unit tests for the amenity facade
"""
import unittest
from app import create_app
from app.services.facade import HBnBFacade


class TestAmenityFacade(unittest.TestCase):

    def setUp(self):
        """run before each test: create a test app, client, and fresh facade"""
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

        # clear all amenities before each test
        for amenity in self.facade.get_all_amenities():
            self.facade.amenity_repo.delete(amenity.id)

        # valid data for amenity creation
        self.valid_amenity_data = {"name": "WiFi"}
        self.new_amenity_data = {"name": "Pool"}
        self.invalid_amenity_data = {"name": ""}  # invalid if empty name is disallowed

    # --- test facade: create ---
    def test_create_amenity_success(self):
        """create a valid amenity"""
        amenity = self.facade.create_amenity(self.valid_amenity_data)
        self.assertEqual(amenity.name, "WiFi")
        self.assertIsNotNone(amenity.id)

    def test_create_duplicate_amenity_raises_error(self):
        """creating amenity that already exists should raise ValueError"""
        amenity = self.facade.create_amenity(self.valid_amenity_data)
        duplicate_data = {"id": amenity.id, "name": "WiFi"}
        with self.assertRaises(ValueError):
            self.facade.create_amenity(duplicate_data)

    def test_create_amenity_invalid_data(self):
        """creating amenity with invalid data raises error"""
        with self.assertRaises((TypeError, ValueError)):
            self.facade.create_amenity(self.invalid_amenity_data)

    # --- test facade: retrieval ---
    def test_get_all_amenities(self):
        """get all amenities"""
        self.facade.create_amenity(self.valid_amenity_data)
        self.facade.create_amenity(self.new_amenity_data)
        all_amenities = self.facade.get_all_amenities()
        self.assertGreaterEqual(len(all_amenities), 2)

    def test_get_amenity_by_id(self):
        """get a single amenity by id"""
        amenity = self.facade.create_amenity(self.valid_amenity_data)
        retrieved = self.facade.get_amenity(amenity.id)
        self.assertEqual(retrieved.id, amenity.id)
        self.assertEqual(retrieved.name, "WiFi")

    def test_get_amenity_invalid_id(self):
        """raise error for invalid amenity id format"""
        with self.assertRaises(ValueError):
            self.facade.get_amenity("not-a-valid-uuid")

    def test_get_amenity_not_found(self):
        """raise error if amenity not found"""
        import uuid
        non_existent_id = str(uuid.uuid4())
        with self.assertRaises(TypeError):
            self.facade.get_amenity(non_existent_id)

    # --- test facade: update ---
    def test_update_amenity(self):
        """update an existing amenity"""
        amenity = self.facade.create_amenity(self.valid_amenity_data)
        updated_data = {"name": "High-Speed WiFi"}
        updated = self.facade.update_amenity(amenity.id, updated_data)
        self.assertEqual(updated.name, "High-Speed WiFi")


if __name__ == "__main__":
    unittest.main()

