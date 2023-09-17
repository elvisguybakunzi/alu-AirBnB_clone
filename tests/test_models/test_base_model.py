#!/usr/bin/python3
import unittest
import os
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel(unittest.TestCase):

    def test_init(self):
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_str(self):
        model = BaseModel()
        expected_str = f"[BaseModel] ({model.id}) {model.__dict__}"
        self.assertEqual(str(model), expected_str)

    def test_save(self):
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(old_updated_at, model.updated_at)

    def test_to_dict(self):
        model = BaseModel()
        model_dict = model.to_dict()

        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)

    def test_to_dict_with_custom_attributes(self):
        class CustomModel(BaseModel):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.custom_attr = "custom_value"

        custom_model = CustomModel()
        custom_model_dict = custom_model.to_dict()

        self.assertEqual(custom_model_dict['custom_attr'], 'custom_value')

    def test_save_and_reload(self):
        model = BaseModel()
        model_id = model.id
        model.save()

        new_model = BaseModel()
        new_model.reload()
        self.assertEqual(new_model.id, model_id)

    def test_save_and_reload_nonexistent_file(self):
        model = BaseModel()
        model.save()

        new_model = BaseModel()
        new_model.reload()
        self.assertIsNone(new_model)

    def tearDown(self):
        # Clean up any test data or files created during testing
        if os.path.exists("file.json"):
            os.remove("file.json")


if __name__ == '__main__':
    unittest.main()
