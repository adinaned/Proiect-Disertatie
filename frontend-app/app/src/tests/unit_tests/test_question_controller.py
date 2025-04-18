from src.models import Question
from .test_base import BaseDatabaseTest
import unittest


class TestQuestionDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Question)


if __name__ == "__main__":
    unittest.main()
