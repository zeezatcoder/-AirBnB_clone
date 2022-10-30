#!/usr/bin/python3
'''
Module: base.py
'''
import uuid
from datetime import datetime
import models


class BaseModel():
    """
    A base class for other model
    """

    def __init__(self, *arg, **kwargs):
        '''
        instantiaties an object of the BaseModel class
        '''
        if len(kwargs) > 0:

            for index, val in kwargs.items():
                if index == '__class__':
                    continue

                if index == 'created_at' or index == 'updated_at':
                    val = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, index, val)
            return
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        models.storage.new(self)

    def __str__(self):
        ''' return the string representation of an
        instance object
        '''
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self) -> None:
        """
        updates the public instance
        attribute updated_at with the
        current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):

        new_dict = self.__dict__.copy()
        new_dict['__class__'] = type(self).__name__
        new_dict['created_at'] = new_dict['created_at'].isoformat()
        new_dict['updated_at'] = new_dict['updated_at'].isoformat()
        return new_dict
