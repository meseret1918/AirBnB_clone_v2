#!/usr/bin/python3
"""This module defines the DBStorage class."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """This class manages the database storage."""

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and links it to the MySQL database."""
        self.__engine = create_engine('mysql+mysqldb://user:password@localhost/db')
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """Returns a dictionary of all objects of a given class."""
        objects = {}
        if cls:
            query = self.__session.query(cls)
            for obj in query:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for cls in Base.__subclasses__():
                query = self.__session.query(cls)
                for obj in query:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Adds the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes the object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database and creates the current
        database session."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def close(self):
        """Calls remove() method on the private session attribute (self.__session)."""
        self.__session.remove()

