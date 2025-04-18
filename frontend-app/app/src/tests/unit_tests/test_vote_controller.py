from src.models import Vote
from .test_base import BaseDatabaseTest
import unittest


class TestVoteDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Vote)


if __name__ == "__main__":
    unittest.main()
