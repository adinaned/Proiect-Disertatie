from src.models import Role
from .test_base import BaseDatabaseTest
import unittest


class TestRoleDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Role)


if __name__ == "__main__":
    unittest.main()
