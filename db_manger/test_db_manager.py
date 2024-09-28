import unittest
from db_creator import *

# This test create for check if ram table is exsite or not
class TestDatabaseInitialization(unittest.TestCase):
    TEST_DB_PATH = "../ram_data.db"

    def get_test_db_connection(self):
        conn = sqlite3.connect(self.TEST_DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def test_initialize_db(self):
        """Test if the `ram` table is created in the database"""
        # Initialize the database
        initialize_db()

        # Connect to the test database
        conn = self.get_test_db_connection()
        cursor = conn.cursor()

        # Check if the 'ram' table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ram';")
        table = cursor.fetchone()

        self.assertIsNotNone(table, "Table 'ram' should exist")
        self.assertEqual(table['name'], 'ram', "Table name should be 'ram'")

        conn.close()


if __name__ == '__main__':
    unittest.main()
