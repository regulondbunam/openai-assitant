import os
from unittest import TestCase
from unittest.mock import patch
from pymongo.database import Database
from app.tools.get_database import get_database

class TestGetDatabase(TestCase):
    @patch.dict(os.environ, {'MONGODB_CONNECTION_URI': 'mongodb://localhost:27017'})
    def test_get_database_success(self):
        # Arrange
        expected_database_name = 'chatbot'

        # Act
        database = get_database()

        # Assert
        self.assertIsInstance(database, Database)
        self.assertEqual(database.name, expected_database_name)

    @patch.dict(os.environ, {})
    def test_get_database_missing_env_variable(self):
        # Arrange & Act & Assert
        with self.assertRaises(Exception) as context:
            get_database()
        self.assertEqual(str(context.exception), "MONGODB_CONNECTION_URI environment variable is not set.")