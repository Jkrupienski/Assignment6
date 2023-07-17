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
                ID TEXT,
                First TEXT,
                Last TEXT,
                Title TEXT,
                Office TEXT,
                EMAIL TEXT PRIMARY KEY
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE instructor (
                ID TEXT,
                First TEXT,
                Last TEXT,
                Title TEXT,
                Year TEXT,
                Dept TEXT,
                EMAIL TEXT PRIMARY KEY
                
                
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE student (
                ID TEXT,
                First TEXT,
                Last TEXT,
                Year TEXT,
                Major TEXT,
                EMAIL TEXT PRIMARY KEY
                
            )
        ''')

        self.cursor.execute('''
            INSERT INTO admin VALUES ('001', 'bob','bobby', 'Admin User', 'somewhere', 'bobbyb')
        ''')

        self.cursor.execute('''
            INSERT INTO instructor VALUES ('002', 'Luke', 'Bassett', 'teacher', '2020', 'math', 'bassettl')
        ''')

        self.cursor.execute('''
            INSERT INTO student VALUES ('10012', 'Jack', 'Krupienski', '2024', 'CE', 'krupienskij')
        ''')

    def tearDown(self):
        self.conn.close()

    @patch('builtins.input', side_effect=['bobbyb', '001'])
    def test_login_admin(self, mock_input):
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('001', 'bob', 'bobby', 'Admin User', 'somewhere', 'bobbyb')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsInstance(user, Admin)
                mock_print.assert_called_with("Welcome, Admin!")

    @patch('builtins.input', side_effect=['bassettl', '002'])
    def test_login_instructor(self, mock_input):
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('002', 'Luke', 'Bassett', 'teacher', '2020', 'math', 'bassettl')
            with patch('main.print') as mock_print:
                user = login()
                self.assertIsInstance(user, instructor)
                mock_print.assert_called_with("Welcome, Instructor!")

    @patch('builtins.input', side_effect=['krupienskij', '10012'])
    def test_login_student(self, mock_input):
        with patch('main.cursor') as mock_cursor:
            mock_cursor.fetchone.return_value = ('10012', 'Jack', 'Krupienski', '2024', 'CE', 'krupienskij')
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



class testprintRoster(TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                    CREATE TABLE admin (
                        ID TEXT,
                        First TEXT,
                        Last TEXT,
                        Title TEXT,
                        Office TEXT,
                        EMAIL TEXT PRIMARY KEY
                    )
                ''')

        self.cursor.execute('''
                            CREATE TABLE courses (
                                CRN TEXT,
                                TITLE TEXT,
                                DEPT TEXT,
                                TIME TEXT,
                                DAYS TEXT,
                                SEMESTER TEXT,
                                YEAR TEXT,
                                CREDITS
                            )
                        ''')

        self.cursor.execute(('''
                    INSERT INTO courses VALUES ('34285', 'ADVANCED DIGITAL CIRCUIT DESIGN','ELEC', '12:30-13:50', 'WF', 'Summer', '2023', '4')
                '''))



    def tearDown(self):
        self.conn.close()


    def testPrintall(self):
        with patch('main.cursor') as mock_cursor:
            ad = Admin('10012', 'Jack','Krupienski', 'Admin User', 'somewhere', 'krupienskij')
            #ad.printRoster()

            mock_cursor.fetchall.return_value = ['----- Courses -----']
        with patch('builtins.print') as mock_print:
            ad.printRoster()
            expected_calls = unittest.mock.call[('----- Courses -----')]
            mock_print.assert_has_calls(expected_calls)





####

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
        self.cursor.close()
        self.conn.close()

    def test_search_course_valid_choice(self):
        with patch('builtins.input', side_effect=['2', 'Course 2']):
            with patch('main.cursor') as mock_cursor:
                with patch('main.print') as mock_print:
                    inst = instructor('ID123', 'John', 'Doe', 'Instructor', '2020', 'Math', 'instructor@example.com')
                    inst.searchCourse()
                    mock_cursor.execute.assert_called_with('PRAGMA table_info(courses)')
                    mock_print.assert_called_with("Search Results:\n(1002, 'Course 2', '10:30', '11:30', 'Wednesday')")

    def test_search_course_invalid_choice(self):
        with patch('builtins.input', side_effect=['5', 'value']):
            with patch('main.print') as mock_print:
                inst = instructor('ID123', 'John', 'Doe', 'Instructor', '2020', 'Math', 'instructor@example.com')
                inst.searchCourse()
                mock_print.assert_called_with("No results found.")

    def test_search_course_no_results(self):
        with patch('builtins.input', side_effect=['1', 'Unknown']):
            with patch('main.cursor') as mock_cursor:
                with patch('main.print') as mock_print:
                    inst = instructor('ID123', 'John', 'Doe', 'Instructor', '2020', 'Math', 'instructor@example.com')
                    inst.searchCourse()
                    mock_cursor.execute.assert_called_with("PRAGMA table_info(courses)")
                    mock_cursor.fetchall.assert_called()
                    mock_print.assert_called_with("No results found.")



if __name__ == '__main__':
    unittest.main()
