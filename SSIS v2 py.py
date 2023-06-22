import mysql.connector

class Student:
    def __init__(self):
        self.students = []
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nawawi",
            database="ssis_db"
        )
        self.cursor = self.db.cursor()

    def load_from_db(self):
        self.cursor.execute("SELECT * FROM students")
        self.students = self.cursor.fetchall()
        print("Student data loaded successfully from the database.")

    def save_to_db(self):
        self.cursor.execute("TRUNCATE TABLE students")
        sql = "INSERT INTO students (student_id, name, gender, year_level, course_code, course_name) VALUES (%s, %s, %s, %s, %s, %s)"
        student_data = [(student[0], student[1], student[2], student[3], student[4], self.get_course_name(student[4])) for student in self.students]
        self.cursor.executemany(sql, student_data)
        self.db.commit()
        print("Student data saved successfully to the database.")

    def add(self):
        student_id = input("Enter Student ID: ")
        name = input("Enter Student Name: ")
        gender = input("Enter Gender: ")
        year_level = input("Enter Year Level: ")

        # Disconnect from the database
        self.cursor.close()
        self.db.close()

        # Reconnect to the database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nawawi",
            database="ssis_db"
        )
        self.cursor = self.db.cursor()

        self.cursor.execute("SELECT course_code, course_name FROM courses")
        courses = self.cursor.fetchall()

        print("Courses:")
        print("{:<20}{:<15}".format("Course Code", "Course Name"))
        print("________________________________________________________________")
        for course in courses:
            print("{:<20}{:<15}".format(course[0], course[1]))

        course_code = input("Enter Course Code: ")

        # Check if the entered course code exists
        if any(course[0] == course_code for course in courses):
            self.students.append((student_id, name, gender, year_level, course_code))
            print("Student added successfully.")

            # Get the corresponding course_name for the course_code
            course_name = next(course[1] for course in courses if course[0] == course_code)

            # Update the course_name in the students table
            self.cursor.execute("INSERT INTO students (student_id, name, gender, year_level, course_code, course_name) VALUES (%s, %s, %s, %s, %s, %s)",
                                (student_id, name, gender, year_level, course_code, course_name))
            self.db.commit()
        else:
            print("Invalid course code. Student not added.")
        self.save_to_db()

        # Disconnect from the database
        self.cursor.close()
        self.db.close()

        # Reconnect to the database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nawawi",
            database="ssis_db"
        )
        self.cursor = self.db.cursor()

    def get_course_name(self, course_code):
        self.cursor.execute("SELECT course_name FROM courses WHERE course_code = %s", (course_code,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return ""

    def delete(self, student_id):
        for student in self.students:
            if student[0] == student_id:
                self.students.remove(student)
                self.save_to_db()
                print("Student deleted successfully.")
                return
        print("Student not found.")

    def edit(self, student_id):
        for i, student in enumerate(self.students):
            if student[0] == student_id:
                student = list(student)
                print("Select field to edit:")
                print("1. Student ID")
                print("2. Student Name")
                print("3. Gender")
                print("4. Year Level")
                print("5. Course Code")
                choice = input("Enter Your Choice: ")

                if choice == '1':
                    student[0] = input("Enter New Student ID: ")
                    self.students[i] = tuple(student)
                    self.save_to_db()
                    print("Student ID updated successfully.")
                elif choice == '2':
                    student[1] = input("Enter New Student Name: ")
                    self.students[i] = tuple(student)
                    self.save_to_db()
                    print("Student Name updated successfully.")
                elif choice == '3':
                    student[2] = input("Enter New Gender: ")
                    self.students[i] = tuple(student)
                    self.save_to_db()
                    print("Gender updated successfully.")
                elif choice == '4':
                    student[3] = input("Enter New Year Level: ")
                    self.students[i] = tuple(student)
                    self.save_to_db()
                    print("Year Level updated successfully.")
                elif choice == '5':
                    self.cursor.execute("SELECT course_code, course_name FROM courses")
                    courses = self.cursor.fetchall()
                    print("Courses:")
                    print("{:<20}{:<15}".format("Course Code", "Course Name"))
                    print("________________________________________________________________")
                    for course in courses:
                        print("{:<20}{:<15}".format(course[0], course[1]))
                    course_code = input("Enter New Course Code: ")

                    if any(course[0] == course_code for course in courses):
                        student[4] = course_code
                        student[5] = self.get_course_name(course_code)
                        self.students[i] = tuple(student)
                        self.save_to_db()
                        print("Course name updated successfully.")
                    else:
                        print("Invalid course code. Course not updated.")
                else:
                    print("Invalid choice.")
                return
        print("Student not found.")

    def display_list(self):
        self.cursor.execute("SELECT students.student_id, students.name, students.gender, students.year_level, students.course_code, courses.course_name FROM students LEFT JOIN courses ON students.course_code = courses.course_code")
        students = self.cursor.fetchall()
        if not students:
            print("No students found.")
            return
        print("{:<15}{:<25}{:<10}{:<15}{:<20}{:<15}".format("Student ID", "Name", "Gender", "Year Level", "Course Code", "Course Name"))
        print("_________________________________________________________________________________________________________________")
        for student in students:
            course_code = student[4] if student[4] else ""  # Check if course code exists, otherwise set to empty string
            course_name = student[5] if student[5] else ""  # Check if course name exists, otherwise set to empty string
            print("{:<15}{:<25}{:<10}{:<15}{:<20}{:<15}".format(student[0], student[1], student[2], student[3], course_code, course_name))

    def search_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
        result = self.cursor.fetchone()
        if result:
            print("Student found:")
            print("{:<15}{:<25}{:<10}{:<15}{:<20}{:<15}".format("Student ID", "Name", "Gender", "Year Level", "Course Code", "Course Name"))
            print("_________________________________________________________________________________________________________________")
            self.cursor.execute("SELECT course_name FROM courses WHERE course_code=%s", (result[4],))
            course_name = self.cursor.fetchone()
            if course_name:
                print("{:<15}{:<25}{:<10}{:<15}{:<20}{:<15}".format(result[0], result[1], result[2], result[3], result[4], course_name[0]))
            print()
        else:
            print("Student not found.")

    def disconnect(self):
        self.cursor.close()
        self.db.close()
        print("Disconnected from the database.")

    def menu(self):
            while True:
                print("Student Menu:")
                print("1. Add Student")
                print("2. Delete Student")
                print("3. Edit Student")
                print("4. Display Students")
                print("5. Search Students")
                print("0. Exit")

                choice = input("Enter Your Choice: ")
                print()

                if choice == '1':
                    self.add()
                    self.save_to_db()
                    print()
                elif choice == '2':
                    student_id = input("Enter Student ID to Delete: ")
                    self.delete(student_id)
                    print()
                elif choice == '3':
                    student_id = input("Enter Student ID to Edit: ")
                    self.edit(student_id)
                    print()
                elif choice == '4':
                    # Disconnect from the database
                    self.cursor.close()
                    self.db.close()

                    # Reconnect to the database
                    self.db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="nawawi",
                        database="ssis_db"
                    )
                    self.cursor = self.db.cursor()
                    self.display_list()
                    print()
                elif choice == '5':
                    student_id = input("Enter Student ID to Search: ")
                    self.search_by_id(student_id)
                elif choice == '0': 
                    # Disconnect from the database
                    self.cursor.close()
                    self.db.close()

                    # Reconnect to the database
                    self.db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="nawawi",
                        database="ssis_db"
                    )
                    self.cursor = self.db.cursor()
                    break
                else:
                    print("Invalid choice. Please try again.\n")


class Course:
    def __init__(self):
        self.courses = []
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="nawawi",
            database="ssis_db"
        )
        self.cursor = self.db.cursor()

    def load_from_db(self):
        self.cursor.execute("SELECT * FROM courses")
        self.courses = self.cursor.fetchall()
        print("Course data loaded successfully from the database.")

    def save_to_db(self):
        self.cursor.execute("TRUNCATE TABLE courses")
        if self.courses:
            sql = "INSERT INTO courses (course_code, course_name) VALUES (%s, %s)"
            course_data = [(course[0], course[1]) for course in self.courses]
            self.cursor.executemany(sql, course_data)
        self.db.commit()
        print("Course data saved successfully to the database.")


    def add(self):
        course_code = input("Enter Course Code: ")
        course_name = input("Enter Course Name: ")
        self.courses.append((course_code, course_name))
        print("Course added successfully.")
        self.save_to_db()

    def delete(self, course_code):
        deleted_course = None
        for course in self.courses:
            if course[0] == course_code:
                deleted_course = course
                break

        if deleted_course:
            self.courses.remove(deleted_course)
            self.save_to_db()
            self.update_student_course_code(course_code)
            print("Course deleted successfully.")
        else:
            print("Course not found.")

    def update_student_course_code(self, course_code):
        self.cursor.execute("UPDATE students SET course_code = NULL, course_name = NULL WHERE course_code = %s", (course_code,))
        self.db.commit()
        print("Updated course code and course name in students table.")


    def edit(self, course_code):
        for i, course in enumerate(self.courses):
            if course[0] == course_code:
                course = list(course)
                print("Select field to edit:")
                print("1. Course Code")
                print("2. Course Name")
                choice = input("Enter Your Choice: ")
                if choice == '1':
                    course[0] = input("Enter New Course Code: ")
                    self.courses[i] = tuple(course)
                    self.save_to_db()
                elif choice == '2':
                    course[1] = input("Enter New Course Name: ")
                    self.courses[i] = tuple(course)
                    self.save_to_db()
                else:
                    print("Invalid choice.")
                return
        print("Course not found.")

    def display_list(self):
        if not self.courses:
            print("No courses found.")
        else:
            print("Courses:")
            print("{:<20}{:<15}".format("Course Code", "Course Name"))
            print("________________________________________________________________")
            for course in self.courses:
                print("{:<20}{:<15}".format(course[0], course[1]))
        print()

    def menu(self):
        while True:
            print("Course Menu:")
            print("1. Add Course")
            print("2. Delete Course")
            print("3. Edit Course")
            print("4. Display Courses")
            print("0. Exit")

            choice = input("Enter Your Choice: ")
            print()

            if choice == '1':
                self.add()
                print()
            elif choice == '2':
                course_code = input("Enter Course Code to Delete: ")
                self.delete(course_code)
                print()
            elif choice == '3':
                course_code = input("Enter Course Code to Edit: ")
                self.edit(course_code)
                print()
            elif choice == '4':
                self.display_list()
            elif choice == '0': 
                # Disconnect from the database
                self.cursor.close()
                self.db.close()

                # Reconnect to the database
                self.db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="nawawi",
                    database="ssis_db"
                )
                self.cursor = self.db.cursor()
                break

            else:
                print("Invalid choice. Please try again.\n")


def main_menu():
    student_menu = Student()
    course_menu = Course()
    student_menu.load_from_db()
    course_menu.load_from_db()

    while True:
        print("\nMain Menu:")
        print("1. Student Management")
        print("2. Course Management")
        print("0. Save and Exit")

        choice = input("Enter Your Choice: ")
        print()

        if choice == '1':
            student_menu.menu()
        elif choice == '2':
            course_menu.menu()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main_menu()
