"""
Author: rugh1
Date: 8.11.2024
Description: testing implementation for threads
"""
import DataBaseTest
import DataBaseSynced
import threading
from threading import Thread


class Test(DataBaseTest.Test):

    def __init__(self, testpath='test.pickle'):
        self.mode = 1
        self.filepath = testpath
        self.create_empty_pickle_file(self.filepath)
        self.db = DataBaseSynced.DataBase(self.mode, self.filepath)

    def is_locked(self, mutex):
        if isinstance(mutex, threading.Semaphore):
            locked = not mutex.acquire(blocking=False)
            if not locked:
                mutex.release()
        else:
            locked = mutex.locked()
        return locked

    def get_func_runner(self, func, args):
        p = Thread(target=func, args=args)
        return p
