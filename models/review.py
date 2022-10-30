#!/usr/bin/python3
"""
Module: Review
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """A model to create reviews
    Attributes:
        text
        user_id
        place_id
    """
    place_id = ""
    user_id = ""
    text = ""
