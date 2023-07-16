import unittest
from unittest import TestCase
from unittest.mock import patch
import sqlite3

# Import the necessary functions or classes from your module
from main import login, logout
from main import instructor, student, Admin




class LoginTestCase(TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')  # Create an in-memory SQLite database
        self.cursor = self.conn.cursor()

        # Create sample tables and insert test data for admin, instructor, and student
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
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('admin@example.com', 'admin123', 'Admin User')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsInstance(user, Admin)
                mock_print.assert_called_with("Welcome, Admin!")

    @patch('builtins.input', side_effe\ct=['instructor@example.com', 'instructor123'])
    def test_login_instructor(self, mock_input):
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('instructor@example.com', 'instructor123', 'Instructor User')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsInstance(user, instructor)
                mock_print.assert_called_with("Welcome, Instructor!")

    @patch('builtins.input', side_effect=['student@example.com', 'student123'])
    def test_login_student(self, mock_input):
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('student@example.com', 'student123', 'Student User')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsInstance(user, student)
                mock_print.assert_called_with("Welcome, Student!")

    @patch('builtins.input', side_effect=['invalid@example.com', 'invalid123'])
    def test_login_incorrect_credentials(self, mock_input):
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = None
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsNone(user)
                mock_print.assert_called_with("Incorrect username or password, please try again")









class LogoutTestCase(TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')  # Create an in-memory SQLite database
        self.cursor = self.conn.cursor()
        self.student_data = self.cursor.fetchone()

    def tearDown(self):
        self.conn.close()

    # Test logout Function

    @patch('builtins.input', return_value='no')
    def test_logout_login(self, mock_input):
        with patch('main.print') as mock_print:
            with patch('main.login') as mock_login:
                result = logout()
                self.assertEqual(result, mock_login.return_value)
                mock_print.assert_called_with("Logging out...")
                mock_login.assert_called_once()

    @patch('builtins.input', return_value='yes')
    def test_logout_exit_program(self, mock_input):
        with patch('main.print') as mock_print:
            with patch('main.db') as mock_db:
                result = logout()
                self.assertIsNone(result)
                mock_print.assert_called_with("Exiting the program...")
                mock_db.commit.assert_called_once()
                mock_db.close.assert_called_once()

    @patch('builtins.input', side_effect=['invalid', 'no'])
    def test_logout_invalid_choice_then_login(self, mock_input):
        with patch('main.print') as mock_print:
            with patch('main.login') as mock_login:
                result = logout()
                self.assertEqual(result, mock_login.return_value)
                mock_print.assert_called_with("Logging out...")
                self.assertEqual(mock_input.call_count, 2)
                mock_login.assert_called_once()


class InstructorTestCase(TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')  # Create an in-memory SQLite database
        self.cursor = self.conn.cursor()

        # Create a sample courses table with required columns
        self.cursor.execute('''
            CREATE TABLE courses (
                CRN INTEGER PRIMARY KEY,
                CourseName TEXT,
                StartTime TEXT,
                EndTime TEXT,
                Day TEXT
            )
        ''')

        # Insert test data into the courses table
        self.cursor.execute('''
            INSERT INTO courses VALUES
            (1001, 'Course 1', '9:00', '10:00', 'Monday'),
            (1002, 'Course 2', '10:30', '11:30', 'Wednesday'),
            (1003, 'Course 3', '13:00', '14:00', 'Friday')
        ''')

    def tearDown(self):
        self.conn.close()

    def test_search_course_valid_choice(self):
        with patch('builtins.input', side_effect=['2', 'Course 2']):
            with patch('main.cursor') as mock_cursor:
                with patch('main.print') as mock_print:
                    inst = instructor('ID123', 'John', 'Doe', 'Instructor', '2020', 'Math', 'instructor@example.com')
                    inst.searchCourse()
                    mock_cursor.execute.assert_called_with("SELECT * FROM courses WHERE CourseName=?", ('Course 2',))
                    mock_print.assert_called_with("Search Results:\n(1002, 'Course 2', '10:30', '11:30', 'Wednesday')")

    def test_search_course_invalid_choice(self):
        with patch('builtins.input', side_effect=['5', 'value']):
            with patch('main.print') as mock_print:
                self.cursor
                inst = instructor('ID123', 'John', 'Doe', 'Instructor', '2020', 'Math', 'instructor@example.com')
                inst.searchCourse()
                mock_print.assert_called_with("No results found.")

    def test_search_course_no_results(self):
        with patch('builtins.input', side_effect=['1', 'Unknown']):
            with patch('main.cursor') as mock_cursor:
                with patch('main.print') as mock_print:
                    inst = instructor('ID123', 'John', 'Doe', 'Instructor', '2020', 'Math', 'instructor@example.com')
                    inst.searchCourse()
                    mock_cursor.execute.assert_called_with("SELECT * FROM courses WHERE CRN=?", ('Unknown',))
                    mock_print.assert_called_with("No results found.")





if __name__ == '__main__':
    unittest.main()
