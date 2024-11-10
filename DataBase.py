"""
Author: rugh1
Date: 8.11.2024
Description: base db class
"""


class DataBase:
    def __init__(self, db_dict=None) -> None:
        if db_dict is not None:
            self.db = db_dict
        else:
            self.db = {}

    def set_value(self, key, val):
        self.db[key] = val
        return self.db.get(key, None) == val  # not sure if its needed

    def get_value(self, key):
        return self.db.get(key, None)

    def delete_value(self, key):
        val = self.db.get(key, None)
        if key in self.db:
            self.db.pop(key)
        return val
