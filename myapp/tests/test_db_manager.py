import unittest
from unittest.mock import patch, MagicMock
from database import db_manager

class TestDatabaseManager(unittest.TestCase):
    @patch('psycopg2.connect')
    def setUp(self, mock_connect):
        self.db_manager = db_manager.DatabaseManager()
        self.mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_execute_query(self):
        query = "SELECT * FROM table"
        params = ("param1", "param2")
        self.db_manager.execute_query(query, params)
        self.mock_cursor.execute.assert_called_once_with(query, params)
        self.mock_cursor.fetchall.assert_called_once()

if __name__ == "__main__":
    unittest.main()