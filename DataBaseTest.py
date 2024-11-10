"""
Author: rugh1
Date: 8.11.2024
Description: general testing for threads and processes
"""
from abc import ABC, abstractmethod
import pickle
import os
import time
import DataBaseSynced


class Test(ABC):
    db = None

    def __init__(self):
        self.filepath = None
        self.mode = None

    @abstractmethod
    def is_locked(self, mutex):
        pass

    @abstractmethod
    def get_func_runner(self, func, args):
        pass

    @staticmethod
    def create_empty_pickle_file(file_name):
        """Creates an empty pickle file with an empty dictionary."""
        try:
            with open(file_name, 'wb') as f:
                pickle.dump({}, f)
            print(f"Empty dictionary pickled to {file_name}.")
        except Exception as e:
            print(f"Error creating file {file_name}: {e}")

    @staticmethod
    def delete_pickle_file(file_name):
        """Deletes the pickled file."""
        try:
            os.remove(file_name)
            print(f"Deleted {file_name}.")
        except FileNotFoundError:
            print(f"Error: {file_name} does not exist.")
        except PermissionError:
            print(f"Error: Permission denied to delete {file_name}.")
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")

    def run_test(self):
        print('testing simple_write_permission')
        self.test_simple_write_permission()
        print('testing simple_read_permission')
        self.test_simple_read_permission()
        print('testing no_read_during_write')
        self.test_no_read_during_write()
        print('testing multiple_readers')
        self.test_multiple_readers()
        print('testing write_after_multiple_readers')
        self.test_write_after_multiple_readers()
        print('testing basic db functions')

        database = DataBaseSynced.DataBase(self.mode, self.filepath)
        print('testing persistent memmory')
        assert database.get_value('key1') == 'value3', 'data base should have persistent memmory'
        print('testing changing')
        assert database.set_value('key1', 3), ' changing failed'
        assert database.get_value('key1') == 3, 'changing failed'
        print('testing deleting')
        assert database.delete_value('key1') == 3, 'deleting failed'
        assert database.get_value('key1') is None, 'deleting failed'
        print('trying to delete file')
        self.delete_pickle_file(self.filepath)
        print('done testing deleted test file')

    def test_simple_write_permission(self):
        assert not self.is_locked(self.db.lock), 'Database should initially be unlocked for writing.'
        self.db.set_value('key1', 'value1')
        assert not self.is_locked(self.db.lock), 'Database should be unlocked after write operation.'
        assert self.db.db.get('key1') == 'value1', 'failed to write'

    def test_simple_read_permission(self):
        assert not self.is_locked(self.db.semaphore), 'Database should initially be unlocked for reading.'
        self.db.get_value('key1')
        assert not self.is_locked(self.db.semaphore), 'Database should be unlocked after read operation.'

    def reader_no_read_during_write(self, tmp):
        self.db.get_value('key1')

    def writer_no_read_during_write(self, tmp):
        self.db.set_value('key1', 'value2', 1)

    def test_no_read_during_write(self):
        read_func = self.get_func_runner(self.reader_no_read_during_write, (self,))
        write_func = self.get_func_runner(self.writer_no_read_during_write, (self,))
        write_func.start()
        time.sleep(0.1)  # Ensure the reader has acquired the semaphore
        assert self.is_locked(self.db.semaphore), 'write lock should prevent read.'
        read_func.start()
        read_func.join()
        assert not self.is_locked(self.db.semaphore), 'write lock should be released.'

    def reader_multiple_readers(self, tmp):
        assert not self.is_locked(self.db.semaphore), 'accesses should be granted'
        self.db.get_value('key1')

    def test_multiple_readers(self):
        readers = [self.get_func_runner(self.reader_multiple_readers, (self,)) for _ in range(self.db.MAX_READ)]
        for reader_thread in readers:
            reader_thread.start()

        for reader_thread in readers:
            reader_thread.join()

    def reader_write_after_multiple_readers(self, tmp):
        self.db.get_value('key1', 1)

    def writer_write_after_multiple_readers(self, tmp):
        self.db.set_value('key1', 'value3', 1.5)

    def test_write_after_multiple_readers(self):

        readers = [self.get_func_runner(self.reader_write_after_multiple_readers, (self,)) for _ in
                   range(self.db.MAX_READ)]
        writer_thread = self.get_func_runner(self.writer_write_after_multiple_readers, (self,))

        for reader_thread in readers:
            reader_thread.start()

        time.sleep(0.4)  # Ensure all readers are active
        assert self.is_locked(self.db.semaphore), 'Readers should hold read semaphore. (prevent write)'

        writer_thread.start()
        time.sleep(1)
        assert self.is_locked(self.db.lock) and self.is_locked(
            self.db.semaphore), 'Writer should acquire lock and semaphore after all readers have released it.'
        writer_thread.join()

        assert not self.is_locked(self.db.lock) and not self.is_locked(
            self.db.semaphore), 'Writer should release lock and semaphore after finished writing'
