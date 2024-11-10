"""
Author: rugh1
Date: 8.11.2024
Description: testing implementation for process
"""
import DataBaseTest
import DataBaseSynced
from multiprocessing import Process


class Test(DataBaseTest.Test):

    def __init__(self, testpath='test.pickle'):
        self.mode = 2
        self.filepath = testpath
        self.create_empty_pickle_file(self.filepath)
        self.db = DataBaseSynced.DataBase(self.mode, self.filepath)

    def is_locked(self, mutex):
        locked = mutex.acquire(block=False)
        if locked:
            mutex.release()
        return not locked

    def get_func_runner(self, func, args):
        p = Process(target=func, args=args)
        return p
