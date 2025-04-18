import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from src.models import Country
from .test_base import BaseDatabaseTest
import unittest


class TestCountryDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Country)


if __name__ == "__main__":
    unittest.main()
