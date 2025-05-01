from src.models import User
from .test_base import BaseDatabaseTest
import unittest


class TestUserDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=User)


if __name__ == "__main__":
    unittest.main()
