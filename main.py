import sqlite3
import unittest
from unittest import TestCase
from unittest.mock import patch


# Using the database from assignment 3
db = sqlite3.connect('assignment3.db')
cursor = db.cursor()


# User parent class definition
class user:
    def __init__(self, ID, f, l):
        self.firstname = f
        self.lastname = l
        self.ID = ID

    def setFirstName(self, f):
        self.firstname = f

    def setLastName(self, l):
        self.lastname = l;

    def setID(self, i):
        self.ID = i


# Student class definition.
class student(user):
    def __init__(self, ID, firstname, lastname, expdgradyr, major, email):
        super().__init__(ID, firstname, lastname)
        self.expdgradyr = expdgradyr
        self.major = major
        self.email = email
        self.schedule = []  # Schedule is a list of CRN's that can be added

    # Searches for course
    def searchCourse(self):
        # Opens up courses database
        cursor.execute("PRAGMA table_info(courses)")
        columns = cursor.fetchall()
        # pulls the headers of each of the columns
        column_names = [column[1] for column in columns]

        # Prints out to the user column names that they can query by
        print("Available columns for search:")
        for i, column in enumerate(column_names, start=1):
            print(f"{i}. {column}")

        # Based on choice, it will query the user's choice and print all rows that meet the requirements.
        choice = input("Enter the column number to search: ")
        if choice.isdigit() and int(choice) in range(1, len(column_names) + 1):
            column = column_names[int(choice) - 1]
            value = input(f"Enter the value to search for in {column}: ")

            cursor.execute(f"SELECT * FROM courses WHERE {column}=?", (value,))
            results = cursor.fetchall()

            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found.")
        else:
            print("Invalid column choice.")

    # Add drop course. Takes in ad. If ad == true, then it will add course, else it will drop.
    def addDropCourse(self, ad):
        crn = input("Enter the CRN of the course: ")

        cursor.execute("""SELECT * FROM courses WHERE CRN=?""", (crn,))
        course_data = cursor.fetchone()

        if course_data:
            if ad and crn in self.schedule:
                print("Course with CRN", crn, "is already in your schedule.")
            elif not ad and crn not in self.schedule:
                print("Course with CRN", crn, "is not in your schedule.")
            else:
                if ad:
                    # Checks for conflicting courses in schedule
                    conflicting_courses = []
                    for scheduled_crn in self.schedule:
                        cursor.execute("""SELECT * FROM courses WHERE CRN=?""", (scheduled_crn,))
                        scheduled_course_data = cursor.fetchone()
                        if scheduled_course_data[4] == course_data[4] and scheduled_course_data[5] == course_data[5]:
                            conflicting_courses.append(scheduled_course_data)
                    if conflicting_courses:
                        print("The course conflicts with the following courses in your schedule:")
                        for course in conflicting_courses:
                            print(course)
                    else:
                        self.schedule.append(crn)
                        print("Course with CRN", crn, "added to your schedule.")
                else:
                    self.schedule.remove(crn)
                    print("Course with CRN", crn, "removed from your schedule.")
        else:
            print("Course with CRN", crn, "does not exist.")

    # Prints the schedule of the user based on the CRN's in their schedule
    def printSchedule(self):
        print("------ Schedule ------")

        cursor.execute("""SELECT * FROM courses WHERE CRN IN ({}) ORDER BY TIME""".format(','.join(self.schedule)))
        scheduled_courses = cursor.fetchall()

        # Maps the days based on the database format to text format
        day_mapping = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday'}

        sorted_courses = sorted(scheduled_courses, key=lambda x: x[3])

        current_day = None

        for course in sorted_courses:
            crn, title, dept, time, days, semester, year, credits = course

            day_codes = list(days)
            start_time, end_time = time.split('-')

            if current_day != day_codes:
                current_day = day_codes
                print("\n" + ', '.join(day_mapping[day] for day in current_day) + ":")

            start_time = convert_time_format(start_time)
            end_time = convert_time_format(end_time)

            print(f"CRN: {crn} | Course: {title} | Time: {start_time}-{end_time}")

        print("----------------------")


class instructor(user):
    def __init__(self, ID, firstname, lastname, title, yearofhire, department, email):
        super().__init__(ID, firstname, lastname)
        self.title = title
        self.yearofhire = yearofhire
        self.department = department
        self.email = email
        self.schedule = []

    # Prints the schedule of the user based on the CRN's in their schedule
    def printSchedule(self):
        print("------ Schedule ------")

        cursor.execute("""SELECT * FROM courses WHERE CRN IN ({}) ORDER BY TIME""".format(','.join(self.schedule)))
        scheduled_courses = cursor.fetchall()

        day_mapping = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday', 'R': 'Thursday', 'F': 'Friday'}

        sorted_courses = sorted(scheduled_courses, key=lambda x: x[3])

        current_day = None

        for course in sorted_courses:
            crn, title, dept, time, days, semester, year, credits = course

            day_codes = list(days)
            start_time, end_time = time.split('-')

            if current_day != day_codes:
                current_day = day_codes
                print("\n" + ', '.join(day_mapping[day] for day in current_day) + ":")

            start_time = convert_time_format(start_time)
            end_time = convert_time_format(end_time)

            print(f"CRN: {crn} | Course: {title} | Time: {start_time}-{end_time}")

        print("----------------------")

    # Not implemented/added
    def printClassList(self):
        print("Printed out your class list! Kinda...")

    # searches for courses in database (same as student)
    def searchCourse(self):
        cursor.execute("PRAGMA table_info(courses)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        print("Available columns for search:")
        for i, column in enumerate(column_names, start=1):
            print(f"{i}. {column}")

        choice = input("Enter the column number to search: ")
        if choice.isdigit() and int(choice) in range(1, len(column_names) + 1):
            column = column_names[int(choice) - 1]
            value = input(f"Enter the value to search for in {column}: ")

            cursor.execute(f"SELECT * FROM courses WHERE {column}=?", (value,))
            results = cursor.fetchall()

            if results:
                print("Search Results:")
                for row in results:
                    print(row)
            else:
                print("No results found.")
        else:
            print("Invalid column choice.")

    # Adds/Drops course (same as student)
    def addDropCourse(self, ad):
        crn = input("Enter the CRN of the course: ")
        cursor.execute("""SELECT * FROM courses WHERE CRN=?""", (crn,))
        course_data = cursor.fetchone()

        if course_data:
            if ad and crn in self.schedule:
                print("Course with CRN", crn, "is already in your schedule.")
            elif not ad and crn not in self.schedule:
                print("Course with CRN", crn, "is not in your schedule.")
            else:
                if ad:
                    conflicting_courses = []
                    for scheduled_crn in self.schedule:
                        cursor.execute("""SELECT * FROM courses WHERE CRN=?""", (scheduled_crn,))
                        scheduled_course_data = cursor.fetchone()

                        if scheduled_course_data[4] == course_data[4] and scheduled_course_data[5] == course_data[5]:
                            conflicting_courses.append(scheduled_course_data)

                    if conflicting_courses:
                        print("The course conflicts with the following courses in your schedule:")
                        for course in conflicting_courses:
                            print(course)
                    else:
                        self.schedule.append(crn)
                        print("Course with CRN", crn, "added to your schedule.")
                else:
                    self.schedule.remove(crn)
                    print("Course with CRN", crn, "removed from your schedule.")
        else:
            print("Course with CRN", crn, "does not exist.")


class Admin(user):
    def __init__(self, ID, firstname, lastname, title, office, email):
        super().__init__(ID, firstname, lastname)
        self.title = title
        self.office = office
        self.email = email

    # Add or remove user. If ar == true, then it will add user, else remove user
    def addRemoveUser(self, ar):
        if ar == True:
            print("What type of user would you like to add?")
            choice = input("Enter your choice (Admin, Instructor, Student): ")
            if choice == "Admin":
                print("Please enter the following information")
                idn = input("ID number: ")
                fn = input("First name: ")
                ln = input("Last name: ")
                title = input("Title: ")
                office = input("Office: ")
                email = input("Email: ")
                new_admin(idn, fn, ln, title, office, email)
            elif choice == "Instructor":
                print("Please enter the following information")
                idn = input("ID number: ")
                fn = input("First name: ")
                ln = input("Last name: ")
                title = input("Title: ")
                yoh = input("Year of Hire: ")
                dept = input("Department: ")
                email = input("Email: ")
                new_instructor(idn, fn, ln, title, yoh, dept, email)
            elif choice == "Student":
                print("Please enter the following information")
                idn = input("ID number: ")
                fn = input("First name: ")
                ln = input("Last name: ")
                egy = input("Expected graduation year: ")
                major = input("Major: ")
                email = input("Email: ")
                new_student(idn, fn, ln, egy, major, email)
            else:
                print("Invalid Input!")
        else:
            # remove user based on ID.
            print("Please enter the ID of the user")
            removeid = input("ID Number: ")
            cursor.execute("""SELECT ID FROM admin WHERE ID=?""", (removeid,))
            admin_check = cursor.fetchone()
            cursor.execute("""SELECT ID FROM instructor WHERE ID=?""", (removeid,))
            instructor_check = cursor.fetchone()
            cursor.execute("""SELECT ID FROM student WHERE ID=?""", (removeid,))
            student_check = cursor.fetchone()
            if admin_check or instructor_check or student_check:
                confirm = input(f"Are you sure you want to remove user ID: {removeid}? (Yes/No): ")
                if confirm == "Yes":
                    if admin_check:
                        cursor.execute("""DELETE FROM admin WHERE ID=?""", (removeid,))
                        db.commit()
                        print("User removed from the admin table.")
                    if instructor_check:
                        cursor.execute("""DELETE FROM instructor WHERE ID=?""", (removeid,))
                        db.commit()
                        print("User removed from the instructor table.")
                    if student_check:
                        cursor.execute("""DELETE FROM student WHERE ID=?""", (removeid,))
                        db.commit()
                        print("User removed from the student table.")
                else:
                    print("Canceling user removal...")
            else:
                print("User not found in the database")

    # Add/remove course. If ar == true, add course, else remove course
    def addRemoveCourse(self, ar):
        if ar:
            print("Please enter the following information")
            crn = input("CRN: ")
            title = input("Title: ")
            department = input("Department: ")
            time = input("Time: ")
            days = input("Day(s): ")
            semester = input("Semester: ")
            year = input("Year: ")
            creditnum = input("Credits: ")
            cursor.execute("""SELECT CRN FROM courses WHERE CRN=?""", (crn,))
            existing_crn = cursor.fetchone()

            if existing_crn:
                print("Error: Course with CRN ", crn, "already exists.")
            else:
                cursor.execute(
                    """INSERT INTO courses (CRN, TITLE, DEPT, TIME, DAYS, SEMESTER, YEAR, CREDITS) VALUES (?,?,?,?,?,?,?,?)""",
                    (crn, title, department, time, days, semester, year, creditnum))
                db.commit()
        else:
            print("Course Removal - Please enter the following information")
            removecrn = input("Course CRN: ")
            cursor.execute("""SELECT ID FROM courses WHERE ID=?""", (removecrn,))
            courses_check = cursor.fetchone()
            if courses_check:
                confirm = input(f"Are you sure you want ro remove CRN: {removecrn}? (Yes/No): ")
                if confirm == "Yes":
                    cursor.execute("""DELETE FROM courses WHERE CRN=?""", (removecrn,))
                    db.commit()
                    print("Course removed from the courses table.")
                elif confirm == "No":
                    print("Exiting...")
                else:
                    print("Invalid input!")

    # prints all courses
    def printRoster(self):
        cursor.execute("""SELECT * FROM courses""")
        course_info = cursor.fetchall()
        print("----- Courses -----")
        for row in course_info:
            print(row)

    # modify user based on selected ID
    def modifyUser(self):
        print("Enter the ID of the user that you would like to edit")
        editID = input("ID Number: ")
        cursor.execute("""SELECT ID FROM admin WHERE ID=?""", (editID,))
        admin_check = cursor.fetchone()
        cursor.execute("""SELECT ID FROM instructor WHERE ID=?""", (editID,))
        instructor_check = cursor.fetchone()
        cursor.execute("""SELECT ID FROM student WHERE ID=?""", (editID,))
        student_check = cursor.fetchone()
        if admin_check or instructor_check or student_check:
            print("Enter the attribute you would like to edit")
            if admin_check:
                print("1. ID Number")
                print("2. First Name")
                print("3. Last Name")
                print("4. Title")
                print("5. Office")
                print("6. Email")
                print("7. Exit")
                choice = input("Please enter your choice (1-7): ")
                match choice:
                    case "1":
                        newID = input("Please enter a new ID number: ")
                        cursor.execute("""UPDATE admin SET ID = ? WHERE ID = ?""", (newID, editID,))
                        db.commit()
                    case "2":
                        newFN = input("Please enter a new First name: ")
                        cursor.execute("""UPDATE admin SET NAME = ? WHERE ID = ?""", (newFN, editID,))
                        db.commit()
                    case "3":
                        newLN = input("Please enter a new Last name: ")
                        cursor.execute("""UPDATE admin SET SURNAME = ? WHERE ID = ?""", (newLN, editID,))
                        db.commit()
                    case "4":
                        newTitle = input("Please enter a new Title: ")
                        cursor.execute("""UPDATE admin SET TITLE = ? WHERE ID = ?""", (newTitle, editID,))
                        db.commit()
                    case "5":
                        newOffice = input("Please enter a new Office: ")
                        cursor.execute("""UPDATE admin SET OFFICE = ? WHERE ID = ?""", (newOffice, editID,))
                        db.commit()
                    case "6":
                        newEmail = input("Please enter a new Email: ")
                        cursor.execute("""UPDATE admin SET EMAIL = ? WHERE ID = ?""", (newEmail, editID,))
                        db.commit()
                    case "7":
                        print("Exiting...")
                    case _:
                        print("Invalid input!")
            elif instructor_check:
                print("1. ID Number")
                print("2. First Name")
                print("3. Last Name")
                print("4. Title")
                print("5. Year of Hire")
                print("6. Department")
                print("7. Email")
                print("8. Exit")
                choice = input("Please enter your choice (1-8): ")
                match choice:
                    case "1":
                        newID = input("Please enter a new ID number: ")
                        cursor.execute("""UPDATE instructor SET ID = ? WHERE ID = ?""", (newID, editID,))
                        db.commit()
                    case "2":
                        newFN = input("Please enter a new First name: ")
                        cursor.execute("""UPDATE instructor SET NAME = ? WHERE ID = ?""", (newFN, editID,))
                        db.commit()
                    case "3":
                        newLN = input("Please enter a new Last name: ")
                        cursor.execute("""UPDATE instructor SET SURNAME = ? WHERE ID = ?""", (newLN, editID,))
                        db.commit()
                    case "4":
                        newTitle = input("Please enter a new Title: ")
                        cursor.execute("""UPDATE instructor SET TITLE = ? WHERE ID = ?""", (newTitle, editID,))
                        db.commit()
                    case "5":
                        newHRYR = input("Please enter a new hire year: ")
                        cursor.execute("""UPDATE instructor SET HIREYR = ? WHERE ID = ?""", (newHRYR, editID,))
                        db.commit()
                    case "6":
                        newDEPT = input("Please enter a new Department: ")
                        cursor.execute("""UPDATE instructor SET DEPT = ? WHERE ID = ?""", (newDEPT, editID,))
                        db.commit()
                    case "7":
                        newEmail = input("Please enter a new Email: ")
                        cursor.execute("""UPDATE instructor SET EMAIL = ? WHERE ID = ?""", (newEmail, editID,))
                        db.commit()
                    case "8":
                        print("Exiting...")
                    case _:
                        print("Invalid input!")

            elif student_check:
                print("1. ID Number")
                print("2. First Name")
                print("3. Last Name")
                print("4. Expected Graduation Year")
                print("5. Major")
                print("6. Email")
                print("7. Exit")
                choice = input("Please enter your choice (1-7): ")
                match choice:
                    case "1":
                        newID = input("Please enter a new ID number: ")
                        cursor.execute("""UPDATE student SET ID = ? WHERE ID = ?""", (newID, editID,))
                        db.commit()
                    case "2":
                        newFN = input("Please enter a new First name: ")
                        cursor.execute("""UPDATE student SET NAME = ? WHERE ID = ?""", (newFN, editID,))
                        db.commit()
                    case "3":
                        newLN = input("Please enter a new Last name: ")
                        cursor.execute("""UPDATE student SET SURNAME = ? WHERE ID = ?""", (newLN, editID,))
                        db.commit()
                    case "4":
                        newGRADYR = input("Please enter a new Graduation year: ")
                        cursor.execute("""UPDATE student SET GRADYEAR = ? WHERE ID = ?""", (newGRADYR, editID,))
                        db.commit()
                    case "5":
                        newMajor = input("Please enter a new Major: ")
                        cursor.execute("""UPDATE student SET MAJOR = ? WHERE ID = ?""", (newMajor, editID,))
                        db.commit()
                    case "6":
                        newEmail = input("Please enter a new Email: ")
                        cursor.execute("""UPDATE student SET EMAIL = ? WHERE ID = ?""", (newEmail, editID,))
                        db.commit()
                    case "7":
                        print("Exiting...")
                    case _:
                        print("Invalid input!")


# function to add admin's to a list of objets
def add_admin():
    admin_list = []
    cursor.execute("""SELECT * FROM admin""")
    all_admin_info = cursor.fetchall()

    for admin_info in all_admin_info:
        ID, first_name, last_name, title, office, email = admin_info
        existing_admin = next((Admin for Admin in admin_list if Admin.ID == ID), None)
        if existing_admin:
            continue

        newadmin = Admin(ID, first_name, last_name, title, office, email)
        admin_list.append(newadmin)

    return admin_list


# function to add students's to a list of objets
def add_student():
    student_list = []
    cursor.execute("""SELECT * FROM student""")
    all_student_info = cursor.fetchall()

    for student_info in all_student_info:
        ID, first_name, last_name, expectedgradyear, major, email = student_info
        existing_student = next((student for student in student_list if student.ID == ID), None)
        if existing_student:
            continue

        newstudent = student(ID, first_name, last_name, expectedgradyear, major, email)
        student_list.append(newstudent)

    return student_list


# function to add instructors's to a list of objets
def add_instructor():
    instructor_list = []
    cursor.execute("""SELECT * FROM instructor""")
    all_instructor_info = cursor.fetchall()

    for instructor_info in all_instructor_info:
        ID, first_name, last_name, title, yearofhire, department, email = instructor_info
        existing_instructor = next((instructor for instructor in instructor_list if instructor.ID == ID), None)
        if existing_instructor:
            continue

        newinstructor = instructor(ID, first_name, last_name, title, yearofhire, department, email)
        instructor_list.append(newinstructor)

    return instructor_list


# Adds a new admin to the database
def new_admin(ID, firstname, lastname, title, office, email):
    cursor.execute("""SELECT ID FROM admin WHERE ID=?""", (ID,))
    existing_id = cursor.fetchone()

    if existing_id:
        print("Error: User with ID", ID, "already exists.")
    else:
        cursor.execute("""INSERT INTO admin (ID, NAME, SURNAME, TITLE, OFFICE, EMAIL) VALUES (?,?,?,?,?,?)""",
                       (ID, firstname, lastname, title, office, email))
        db.all


# Adds a new instructor to the database
def new_instructor(ID, first_name, last_name, title, yearofhire, department, email):
    cursor.execute("""SELECT ID FROM instructor WHERE ID=?""", (ID,))
    existing_id = cursor.fetchone()

    if existing_id:
        print("Error: User with ID", ID, "already exists.")
    else:
        cursor.execute(
            """INSERT INTO instructor (ID, NAME, SURNAME, TITLE, HIREYR, DEPT, EMAIL) VALUES (?,?,?,?,?,?,?)""",
            (ID, first_name, last_name, title, yearofhire, department, email))
        db.commit()


# Adds a new student to the database
def new_student(ID, first_name, last_name, expectedgradyear, major, email):
    cursor.execute("""SELECT ID FROM student WHERE ID=?""", (ID,))
    existing_id = cursor.fetchone()

    if existing_id:
        print("Error: User with ID", ID, "already exists.")
    else:
        cursor.execute("""INSERT INTO student (ID, NAME, SURNAME, GRADYEAR, MAJOR, EMAIL) VALUES (?,?,?,?,?,?)""",
                       (ID, first_name, last_name, expectedgradyear, major, email))
        db.commit()


# Print's the database at start of program
def print_database():
    admin_objects = add_admin()
    student_objects = add_student()
    instructor_object = add_instructor()

    print("----- Students -----")
    for student in student_objects:
        print(student.ID, student.firstname, student.lastname, student.expdgradyr, student.major, student.email)

    print("----- Instructors -----")
    for instructor in instructor_object:
        print(instructor.ID, instructor.firstname, instructor.lastname, instructor.title, instructor.yearofhire,
              instructor.department, instructor.email)

    print("----- Admins -----")
    for Admin in admin_objects:
        print(Admin.ID, Admin.firstname, Admin.lastname, Admin.title, Admin.office, Admin.email)


# Init functions when program is run
admin_objects = add_admin()
student_objects = add_student()
instructor_object = add_instructor()
print_database()


# Converts the 24 hour format to 12 hour format for schedule printing
def convert_time_format(time):
    hours, minutes = time.split(':')
    period = 'AM' if int(hours) < 12 else 'PM'

    if int(hours) > 12:
        hours = str(int(hours) - 12)

    return f"{hours}:{minutes} {period}"


# Login function for all users
def login():
    while True:

        print("------ Login Screen ------")
        username = input("Please enter email: ")
        password = input("Please enter id number: ")

        cursor.execute("""SELECT * FROM admin WHERE EMAIL=? AND ID=?""", (username, password))
        admin_data = cursor.fetchone()

        cursor.execute("""SELECT * FROM instructor WHERE EMAIL=? AND ID=?""", (username, password))
        instructor_data = cursor.fetchone()

        cursor.execute("""SELECT * FROM student WHERE EMAIL=? AND ID=?""", (username, password))
        student_data = cursor.fetchone()

        if admin_data:
            print("Welcome, Admin!")
            access_granted = True
            return Admin(*admin_data)
        elif instructor_data:
            print("Welcome, Instructor!")
            access_granted = True
            return instructor(*instructor_data)
        elif student_data:
            print("Welcome, Student!")
            access_granted = True
            return student(*student_data)
        else:
            print("Incorrect username or password, please try again")


# Logout function -- Give the user the option to either switch users (log out and log back in) or end the program.
def logout():
    global access_granted
    access_granted = False
    while True:
        choice = input("Do you want to exit the program? (Yes/No): ")
        if choice.lower() == "yes":
            print("Exiting the program...")
            db.commit()
            # db.close()
            return None
        elif choice.lower() == "no":
            print("Logging out...")
            return login()
        else:
            print("Invalid choice. Please enter 'Yes' or 'No'.")


# default login functionality
access_granted = False
logged_in_user = None
while not access_granted:
    logged_in_user = login()
    access_granted = True

# main menu. Changes based on user type that is logged in. the isinstance will check the user type to see what type of object they are.
while True:
    # Admin menu
    if isinstance(logged_in_user, Admin):
        print("Welcome to the admin control panel, what would you like to do?")
        print("1. Add/Remove User")
        print("2. Update User")
        print("3. Print all...")
        print("4. Add/Remove Course")
        print("5. Update Course")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            print("Would you like to add or remove a user?")
            choice = input("Enter add or remove: ")
            if choice == "add":
                logged_in_user.addRemoveUser(True)
            elif choice == "remove":
                logged_in_user.addRemoveUser(False)
            else:
                print("Invalid Choice")
        elif choice == "2":
            logged_in_user.modifyUser()
        elif choice == "3":
            print_database()
            logged_in_user.printRoster()
        elif choice == "4":
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='courses'")
            table_exists = cursor.fetchone()
            if not table_exists:
                cursor.execute("""
                    CREATE TABLE courses (
                        CRN INTEGER,
                        TITLE TEXT,
                        DEPT TEXT,
                        TIME TEXT,
                        DAYS TEXT,
                        SEMESTER TEXT,
                        YEAR INTEGER,
                        CREDITS INTEGER
                    )
                """)
                db.commit()
                print("The 'courses' table has been created")

            print("Would you like to add or remove a course?")
            choice = input("Enter add or remove: ")
            if choice == "add":
                logged_in_user.addRemoveCourse(True)
            elif choice == "remove":
                logged_in_user.addRemoveCourse(False)
            else:
                print("Invalid Choice")
        elif choice == "5":
            print("Test5")
        elif choice == "6":
            logout()
            break
        else:
            print("Invalid choice. Please try again.")

    # instructor menu
    elif isinstance(logged_in_user, instructor):
        print("Welcome to the instructor control panel, what would you like to do?")
        print("1. Print Schedule")
        print("2. Print Class List")
        print("3. Add/Drop Course")
        print("4. Search Course")
        print("5. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            logged_in_user.printSchedule()
        elif choice == "2":
            logged_in_user.printClassList()
        elif choice == "3":
            ad = input("Add or drop? (add/drop): ")
            if ad == "add":
                ad = True
            else:
                ad = False
            logged_in_user.addDropCourse(ad)
        elif choice == "4":
            logged_in_user.searchCourse()
        elif choice == "5":
            logout()
            break
        else:
            print("Invalid choice. Please try again.")

    # Student menu
    elif isinstance(logged_in_user, student):
        print("Welcome to the student control panel, what would you like to do?")
        print("1. Print Schedule")
        print("2. Search Course")
        print("3. Add/Drop Course")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            logged_in_user.printSchedule()
        elif choice == "2":
            logged_in_user.searchCourse()
        elif choice == "3":
            ad = input("Add or drop? (add/drop): ")
            if ad == "add":
                ad = True
            else:
                ad = False
            logged_in_user.addDropCourse(ad)
        elif choice == "4":
            logout()
            break
        else:
            print("Invalid choice. Please try again.")
    else:
        print("Errror!!")
        db.commit()
        db.close()
        break




