#!/usr/bin/python3
"""Module for FileStorage Engine
"""
from json import dump, load
from models.base_model import BaseModel


class FileStorage:
    """FileStorage class used to serialise objects to JSON files
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        # Creating a key to store the object
        key = "{}.{}".format(obj.__class__.__name__, obj.id)

        # Adding the object to our dictionary of objects
        self.__objects[key] = obj

    def save(self):
        # Convert objects to dictionaries
        object_dictionaries = {}
        for key, value in self.__objects.items():
            object_dictionaries[key] = value.to_dict()

        # Writing the object dictionaries to file
        with open(self.__file_path, "w+") as f:
            dump(object_dictionaries, f)

    def reload(self):
        try:
            with open(self.__file_path, "r") as f:

                # Parse the objects from JSON
                object_dictionaries = load(f)

                # Convert them to BaseModels
                for key, value in object_dictionaries.items():
                    class_name = key.split(".")[0]
                    self.__objects[key] = eval(class_name)(**value)

        except FileNotFoundError:
            pass
