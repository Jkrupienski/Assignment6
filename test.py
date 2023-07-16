import unittest
from unittest import TestCase
from unittest.mock import patch
import sqlite3

# Import the necessary functions or classes from your module
from main import login, logout, cursor


class LoginLogoutTestCase(TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')  # Create an in-memory SQLite database
        self.cursor = self.conn.cursor()

        # Create sample tables and insert test data
        self.cursor.execute('''
            CREATE TABLE admin (
                EMAIL TEXT PRIMARY KEY,
                ID TEXT,
                Name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE instructor (
                EMAIL TEXT PRIMARY KEY,
                ID TEXT,
                Name TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE student (
                EMAIL TEXT PRIMARY KEY,
                ID TEXT,
                Name TEXT
            )
        ''')

        self.cursor.execute('''
            INSERT INTO admin VALUES ('admin@example.com', 'admin123', 'Admin User')
        ''')

        self.cursor.execute('''
            INSERT INTO instructor VALUES ('instructor@example.com', 'instructor123', 'Instructor User')
        ''')

        self.cursor.execute('''
            INSERT INTO student VALUES ('student@example.com', 'student123', 'Student User')
        ''')

    def tearDown(self):
        self.conn.close()

    @patch('builtins.input', side_effect=['admin@example.com', 'admin123'])
    def test_login_admin(self, mock_input):
        with patch('cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('admin@example.com', 'admin123', 'Admin User')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsNotNone(user)
                mock_print.assert_called_with("Welcome, Admin!")

    @patch('builtins.input', side_effect=['instructor@example.com', 'instructor123'])
    def test_login_instructor(self, mock_input):
        with patch('cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('instructor@example.com', 'instructor123', 'Instructor User')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsNotNone(user)
                mock_print.assert_called_with("Welcome, Instructor!")

    @patch('builtins.input', side_effect=['student@example.com', 'student123'])
    def test_login_student(self, mock_input):
        with patch('cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('student@example.com', 'student123', 'Student User')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsNotNone(user)
                mock_print.assert_called_with("Welcome, Student!")

    @patch('builtins.input', side_effect=['invalid@example.com', 'invalid123', 'yes'])
    def test_login_incorrect_credentials(self, mock_input):
        with patch('cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = None
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsNone(user)
                mock_print.assert_called_with("Incorrect username or password, please try again")

    @patch('builtins.input', return_value='yes')
    def test_logout_exit_program(self, mock_input):
        with patch('main.print') as mock_print:
            with patch('assignment3.db') as mock_db:
                result = logout()
                self.assertIsNone(result)
                mock_print.assert_called_with("Exiting the program...")
                mock_db.commit.assert_called_once()
                mock_db.close.assert_called_once()

    @patch('builtins.input', return_value='no')
    def test_logout_login(self, mock_input):
        with patch('main.print') as mock_print:
            with patch('main.login') as mock_login:
                result = logout()
                self.assertEqual(result, mock_login.return_value)
                mock_print.assert_called_with("Logging out...")
                mock_login.assert_called_once()

    @patch('builtins.input', side_effect=['invalid', 'no'])
    def test_logout_invalid_choice_then_login(self, mock_input):
        with patch('your_module.print') as mock_print:
            with patch('main.login') as mock_login:
                result = logout()
                self.assertEqual(result, mock_login.return_value)
                mock_print.assert_called_with("Invalid choice. Please enter 'Yes' or 'No'.")
                self.assertEqual(mock_input.call_count, 2)
                mock_login.assert_called_once()


if __name__ == '__main__':
    unittest.main()
