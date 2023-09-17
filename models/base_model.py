#!/usr/bin/python3
"""Module for Base Model
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """BaseModel Class
    Contains attributes that all other models will have
    Therefore serves as the Base class.
    """

    def __init__(self, *args, **kwargs):

        if kwargs:
            # Adding all kwargs as instance attributes
            for key, value in kwargs.items():

                # Converting iso format string dates to date objects
                if key in ['created_at', 'updated_at']:
                    value = datetime.fromisoformat(value)

                # Adding all attributes except __class__
                if key != "__class__":
                    setattr(self, key, value)
        else:
            # Else we create new base attributes
            self.id = uuid4().hex
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

            # Add the object to storage
            models.storage.new(self)

    def __str__(self):
        class_name = self.__class__.__name__
        instance_id = self.id
        attributes = self.__dict__

        return "[{}] ({}) {}".format(class_name, instance_id, attributes)

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        attributes = self.__dict__.copy()
        attributes['__class__'] = self.__class__.__name__
        attributes['created_at'] = attributes['created_at'].isoformat()
        attributes['updated_at'] = attributes['updated_at'].isoformat()
        return attributes
