#!/usr/bin/python3
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
import unittest
import os


class TestFileStorage(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(storage._FileStorage__file_path):
            os.remove(storage._FileStorage__file_path)

    def test_all(self):
        # Ensure the __objects dictionary is initially empty
        self.assertEqual(storage.all(), {})

    def test_new_and_all(self):
        # Create a BaseModel instance
        model = BaseModel()
        # Add it to storage
        storage.new(model)
        # Ensure the model is in the __objects dictionary
        self.assertIn(f"BaseModel.{model.id}", storage.all())

    def test_save_and_reload(self):
        # Create a BaseModel instance
        model = BaseModel()
        # Add it to storage
        storage.new(model)
        # Save the data to a file
        storage.save()
        # Reload the data from the file
        new_storage = FileStorage()
        new_storage.reload()
        # Ensure the reloaded data contains the model
        self.assertIn(f"BaseModel.{model.id}", new_storage.all())


if __name__ == '__main__':
    unittest.main()
