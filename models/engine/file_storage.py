#!/usr/bin/python3
"""This module defines the FileStorage class."""

import json


class FileStorage:
    """This class serializes and deserializes objects to/from JSON file."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)."""
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict()
        with open(FileStorage.__file_path, mode="w", encoding="utf-8") as f:
            json.dump(new_dict, f)

    def reload(self):
        """Deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists; otherwise, do nothing)."""
        try:
            with open(FileStorage.__file_path, mode="r", encoding="utf-8") as f:
                obj_dict = json.load(f)
                for key, value in obj_dict.items():
                    class_name = value["__class__"]
                    obj = eval(class_name + "(**value)")
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """Calls reload() method for deserializing the JSON file to objects."""
        self.reload()

