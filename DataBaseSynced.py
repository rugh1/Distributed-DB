"""
Author: rugh1
Date: 8.11.2024
Description: class adding sync for db
"""
import time
import DataBaseFile
import threading
import multiprocessing


class DataBase(DataBaseFile.DataBase):
    MAX_READ = 10
    MAX_WRITE = 1  # shouldn't really be changed
    default_path = 'DB.pickle'

    def __init__(self, mode, filepath: str = default_path):  # mode : 1 is threading 2 is semaphore
        super().__init__(filepath)
        self.mode = mode
        self.semaphore = threading.Semaphore(self.MAX_READ) if mode == 1 else multiprocessing.Semaphore(self.MAX_READ)
        self.lock = threading.Lock() if mode == 1 else multiprocessing.Lock()

    def get_value(self, key, delay=0):  # delay for testing
        """
            Retrieves the value associated with the given key from the database.

            Args:
                key (str): The key to retrieve the value for.
                delay (int, optional): A delay in seconds to simulate latency for testing purposes. Defaults to 0.

            Returns:
                The value associated with the key.

            This method acquires a semaphore to ensure synchronized access to the database.
            After retrieving the value, it optionally delays execution for testing purposes
            and then releases the semaphore.
        """
        self.semaphore.acquire()
        value = super().get_value(key)
        time.sleep(delay)
        self.semaphore.release()
        return value

    def get_write_access(self):
        """
            Acquires a write lock and the maximum number of read semaphores.

            This method is used to ensure exclusive write access to the database.
            It acquires a write lock and then acquires the maximum number of read semaphores
            to prevent concurrent read operations while the write operation is in progress.
        """
        self.lock.acquire()
        for i in range(self.MAX_READ):
            self.semaphore.acquire()

    def release_write_access(self):
        """
           Releases the write lock and all acquired read semaphores.

           This method is used to release the exclusive write access to the database.
           It releases all acquired read semaphores and then releases the write lock.
        """
        for i in range(self.MAX_READ):
            self.semaphore.release()
        self.lock.release()

    def set_value(self, key, val, delay=0):  # delay for testing
        """
            Sets the value associated with the given key in the database.

            Args:
                key (str): The key to set the value for.
                val: The value to set.
                delay (int, optional): A delay in seconds to simulate latency for testing purposes. Defaults to 0.

            Returns:
                The previous value associated with the key, or None if the key was not found.

            This method acquires a write lock and the maximum number of read semaphores to ensure exclusive write access.
            After setting the value, it optionally delays execution for testing purposes and then releases the locks and semaphores.
        """
        self.get_write_access()
        value = super().set_value(key, val)
        time.sleep(delay)
        self.release_write_access()
        return value

    def delete_value(self, key):
        """
            Deletes the value associated with the given key from the database.

            Args:
                key (str): The key to delete.

            Returns:
                The deleted value, or None if the key was not found.

            This method acquires a write lock and the maximum number of read semaphores to ensure exclusive write access.
            After deleting the value, it releases the locks and semaphores.
        """
        self.get_write_access()
        value = super().delete_value(key)
        self.release_write_access()
        return value
