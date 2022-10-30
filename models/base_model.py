#!/usr/bin/python3
"""
    Contains the Base Model module
"""
import models
import uuid
from datetime import datetime


class BaseModel():
    """
        Defines the base model class of an instance
    """
    def __init__(self, *args, **kwargs):
        """
            Initialization attributes
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key == "__class__":
                    continue
                setattr(self, key, value)

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        cls_name = self.__class__.__name__
        return ('[{}] ({}) {}'.format(cls_name, self.id, self.__dict__))

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            Returns an updated dictionary containing all keys/values
            of __dict__ of the instance with a __class__ entry and
            iso-formatted datetime
        """
        n_dict = self.__dict__.copy()
        n_dict.update({"__class__": str(self.__class__.__name__)})
        n_dict["created_at"] = self.created_at.isoformat()
        n_dict["updated_at"] = self.updated_at.isoformat()

        return n_dict
