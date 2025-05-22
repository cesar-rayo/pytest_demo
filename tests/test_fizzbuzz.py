import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from fizzbuzz import fizzBuzz


class TestSuiteFizzBuzz:
    @staticmethod
    def checkFizzBuzz(value, expected):
        assert fizzBuzz(value) == expected

    def test_returns1With1PassedIn(self):
        self.checkFizzBuzz(1, "1")

    def test_returns2With2PassedIn(self):
        self.checkFizzBuzz(2, "2")

    def test_returnsFizzWith3PassedIn(self):
        self.checkFizzBuzz(3, "Fizz")

    def test_returnsBuzzWith5PassedIn(self):
        self.checkFizzBuzz(5, "Buzz")

    def test_returnsFizzWith6PassedIn(self):
        self.checkFizzBuzz(6, "Fizz")

    def test_returnsBuzzWith10PassedIn(self):
        self.checkFizzBuzz(10, "Buzz")

    def test_returnsFizzBuzzWith15PassedIn(self):
        self.checkFizzBuzz(15, "FizzBuzz")
