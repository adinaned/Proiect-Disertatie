from src.models import Option
from .test_base import BaseDatabaseTest
import unittest


class TestOptionDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Option)


if __name__ == "__main__":
    unittest.main()
