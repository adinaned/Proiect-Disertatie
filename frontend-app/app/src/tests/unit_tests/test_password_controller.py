from src.models import Password
from .test_base import BaseDatabaseTest
import unittest


class TestPasswordDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Password)


if __name__ == "__main__":
    unittest.main()
