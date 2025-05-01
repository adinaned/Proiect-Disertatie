from src.models import VotingSession
from .test_base import BaseDatabaseTest
import unittest


class TestVotingSessionDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=VotingSession)


if __name__ == "__main__":
    unittest.main()
