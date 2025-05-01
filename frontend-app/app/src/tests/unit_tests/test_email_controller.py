from src.models import Email
from .test_base import BaseDatabaseTest
import unittest


class TestEmailDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Email)


if __name__ == "__main__":
    unittest.main()
