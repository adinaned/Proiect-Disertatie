from src.models import Organisation
from .test_base import BaseDatabaseTest
import unittest


class TestOrganisationDatabaseOperations(BaseDatabaseTest):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName, model=Organisation)


if __name__ == "__main__":
    unittest.main()
