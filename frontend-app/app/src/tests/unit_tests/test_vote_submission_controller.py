from src.models import VoteSubmission
from .test_base import BaseDatabaseTest
import unittest


class TestVoteSubmissionDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=VoteSubmission)


if __name__ == "__main__":
    unittest.main()
