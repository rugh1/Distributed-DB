"""
Author: rugh1
Date: 8.11.2024
Description: main file
"""
import TestProcess
import TestThread


def test_database():
    print('running process test:')
    test = TestProcess.Test()
    test.run_test()
    print('running thread test:')
    test = TestThread.Test()
    test.run_test()


if __name__ == '__main__':
    test_database()
