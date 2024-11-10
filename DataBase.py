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
        """
            Sets the value associated with the given key in the in-memory database.

            Args:
                key (str): The key to set the value for.
                val: The value to set.

            Returns:
                True if the value was set successfully, False otherwise.
        """
        self.db[key] = val
        return self.db.get(key, None) == val  # not sure if its needed

    def get_value(self, key):
        """
            Retrieves the value associated with the given key from the in-memory database.

            Args:
                key (str): The key to retrieve the value for.

            Returns:
                The value associated with the key, or None if the key is not found.  

        """
        return self.db.get(key, None)

    def delete_value(self, key):
        """
            Deletes the value associated with the given key from the in-memory database.

            Args:
                key (str): The key to delete.

            Returns:
                The deleted value, or None if the key was not found.
        """
        val = self.db.get(key, None)
        if key in self.db:
            self.db.pop(key)
        return val
