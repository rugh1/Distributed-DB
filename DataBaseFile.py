"""
Author: rugh1
Date: 8.11.2024
Description: class adding file usage for db
"""
import DataBase
import pickle
import os.path


class DataBase(DataBase.DataBase):
    default_path = 'DB.pickle'

    def __init__(self, filepath: str = default_path):
        try:
            if filepath == '':
                filepath = self.default_path
            if not os.path.isfile(filepath) or os.path.getsize(filepath) < 0:  # if file is not exist or empty.
                with open(filepath, 'ab') as f:
                    pickle.dump({}, f)
            self.filepath = filepath
            file = open(filepath, 'rb')
            dictionary = pickle.load(file)
            super().__init__(dictionary)

        except Exception as err:
            print("errr:   " + str(err))

    def set_value(self, key, val):
        """
            Sets the value associated with the given key in the database and persists the changes to disk.

            Args:
                key (str): The key to set the value for.
                val: The value to set.

            Returns:
                True if the value was set successfully, False otherwise.

            This method first sets the value in the in-memory database.
            If successful, it then attempts to persist the updated database state to disk.
            If the persistence operation fails, the method returns False to indicate the failure.
        """
        success = super().set_value(key, val)
        if success:
            try:
                with open(self.filepath, 'wb') as f:
                    pickle.dump(self.db, f)
            except Exception as err:
                print('err: ' + str(err))
                success = False
        return success

    def delete_value(self, key):
        """
            Deletes the value associated with the given key from the database and persists the changes to disk.

            Args:
                key (str): The key to delete.

            Returns:
                The deleted value, or None if the key was not found.

            This method first deletes the value from the in-memory database.
            If successful, it then attempts to persist the updated database state to disk.
        """
        val = super().delete_value(key)
        try:
            with open(self.filepath, 'wb') as f:
                pickle.dump(self.db, f)
        except Exception as err:
            print('err: ' + str(err))
        return val
