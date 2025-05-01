from src.models import ProfileStatus
from .test_base import BaseDatabaseTest
import unittest


class TestProfileStatusDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=ProfileStatus)


if __name__ == "__main__":
    unittest.main()
