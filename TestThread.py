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
        """
                Checks if a given mutex is locked.

                Args:
                    mutex: The mutex object to check.

                Returns:
                    bool: True if the mutex is locked, False otherwise.
        """
        if isinstance(mutex, threading.Semaphore):
            locked = not mutex.acquire(blocking=False)
            if not locked:
                mutex.release()
        else:
            locked = mutex.locked()
        return locked

    def get_func_runner(self, func, args):
        """
                Creates a new thread to run the given function with the specified arguments.

                Args:
                    func: The function to run.
                    args: The arguments to pass to the function.

                Returns:
                    Thread: The created thread.
        """
        p = Thread(target=func, args=args)
        return p
