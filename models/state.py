#!/usr/bin/python3
"""This is the state class"""

import models
from models.base_model import BaseModel
from models.base_model import Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        state_id: The state id
        name: input name
    """

    """This init method allows the class to access BaseModel's attributes"""

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    if getenv("HBNB_TYPE_STORAGE", None) != "db":

        @property
        def cities(self):
            """
            Returns the list of City instances with state_id equals to the
            current State.id as private
            """
            c_list = []

            all_cities = models.storage.all("City")

            for key, value in all_cities.items():

                if value.__dict__.get('state_id') == self.id:
                    c_list.append(value)

            return (c_list)
