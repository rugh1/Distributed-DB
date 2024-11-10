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
        self.semaphore.acquire()
        value = super().get_value(key)
        time.sleep(delay)
        self.semaphore.release()
        return value

    def get_write_access(self):
        self.lock.acquire()
        for i in range(self.MAX_READ):
            self.semaphore.acquire()

    def release_write_access(self):
        for i in range(self.MAX_READ):
            self.semaphore.release()
        self.lock.release()

    def set_value(self, key, val, delay=0):  # delay for testing
        self.get_write_access()
        value = super().set_value(key, val)
        time.sleep(delay)
        self.release_write_access()
        return value

    def delete_value(self, key):
        self.get_write_access()
        value = super().delete_value(key)
        self.release_write_access()
        return value
