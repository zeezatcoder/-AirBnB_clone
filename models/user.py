#!usr/bin/python3
'''
Module: User
'''
from models.base_model import BaseModel


class User(BaseModel):
    ''' the user module inherit the based module
    extends it some user attributes '''
    email = ""
    password = ""
    first_name = ""
    last_name = ""
