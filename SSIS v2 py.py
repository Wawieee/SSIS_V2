import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nawawi",
    database="test"
)
cursor = conn.cursor()

# Course Menu Display Function
def student_menu():
    while True:

        print("\n\nSTUDENT MANAGEMENT MENU")
        print("-----------------------")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Edit Student")
        print("4. List Students")
        print("5. Search Student")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            delete_student()
        elif choice == '3':
            edit_student()
        elif choice == '4':
            list_students()
        elif choice == '5':
            search_student()
        elif choice == '0':
            break
        else:
            print("\nInvalid choice. Please try again.")
            prompt()

# Course Menu Display Function
def course_menu():
    while True:

        print("\n\nCOURSE MANAGEMENT MENU")
        print("----------------------")
        print("1. Add Course")
        print("2. Delete Course")
        print("3. Edit Course")
        print("4. List Courses")
        print("5. Search Course")
        print("0. Exit")
        choice = input("Enter your choice (0-5): ")

        if choice == '1':
            add_course()
        elif choice == '2':
            delete_course()
        elif choice == '3':
            edit_course()
        elif choice == '4':
            list_courses()
        elif choice == '5':
            search_course()
        elif choice == '0':
            break
        else:
            print("\nInvalid choice. Please try again.")
            prompt()

# Student Add Function
def add_student():
    print("Enter student details:")
    student_id = input("Student ID: ")
    name = input("Name: ")
    gender = input("Gender: ")
    year_level = input("Year Level: ")

    # Fetch the courses data from the database
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    if courses:
        print("\nAvailable Courses:")
        print("{:<12} {:<20}".format("Course Code", "Course Name"))
        for course in courses:
            print("{:<12} {:<20}".format(course[0], course[1]))
    else:
        print("\nNo courses found.")

    course_code = input("Course Code: ")

    cursor.execute('''
        INSERT INTO students (student_id, name, gender, year_level, course_code)
        VALUES (%s, %s, %s, %s, %s)
    ''', (student_id, name, gender, year_level, course_code))
    conn.commit()
    print("\nStudent created successfully!")
    prompt()

# Student Delete Function
def delete_student():
    student_id = input("Enter student ID: ")
    cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    student = cursor.fetchone()
    if student:
        confirm = input("\nPRESS '1' TO CONFIRM\nPRESS '2' TO CANCEL\n\nEnter choice: ")
        if confirm.lower() == '1':
            cursor.execute('DELETE FROM students WHERE student_id = %s', (student_id,))
            conn.commit()
            print("\nStudent deleted successfully!")
        else:
            print("\nDeletion canceled.")
    else:
        print("\nStudent not found.")
    prompt()

# Student Edit Function
def edit_student():
    student_id = input("Enter student ID: ")
    cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    student = cursor.fetchone()
    if student:
        print("\nCurrent Student Details:")
        print("{:<12} {:<20} {:<8} {:<12} {:<12}".format("Student ID", "Name", "Gender", "Year Level", "Course Code"))
        print("{:<12} {:<20} {:<8} {:<12} {:<12}".format(student[0], student[1], student[2], student[3], student[4]))

        print("\nEnter new student details:")
        name = input("Name (Press ENTER to skip): ")
        gender = input("Gender (Press ENTER to skip): ")
        year_level = input("Year Level (Press ENTER to skip): ")
        course_code = input("Course Code (Press ENTER to skip): ")

        if name == '':
            name = student[1]
        if gender == '':
            gender = student[2]
        if year_level == '':
            year_level = student[3]
        if course_code == '':
            course_code = student[4]

        cursor.execute('''
            UPDATE students
            SET name = %s, gender = %s, year_level = %s, course_code = %s
            WHERE student_id = %s
        ''', (name, gender, year_level, course_code, student_id))
        conn.commit()
        print("\nStudent updated successfully!")
    else:
        print("\nStudent not found.")
    prompt()

# Student List Function
def list_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    if students:
        print("\nList of Students:")
        print("{:<12} {:<20} {:<8} {:<12} {:<12}".format("Student ID", "Name", "Gender", "Year Level", "Course Code"))
        for student in students:
            print("{:<12} {:<20} {:<8} {:<12} {:<12}".format(student[0], student[1], student[2], student[3], student[4]))
    else:
        print("\nNo students found.")
    prompt()

# Student Search Function
def search_student():
    print("Search Options:")
    print("1. Search by Student ID")
    print("2. Search by Student Name")
    choice = input("Enter your choice (1-2): ")

    if choice == '1':
        student_id = input("Enter student ID: ")
        cursor.execute('SELECT * FROM students WHERE student_id = %s', (student_id,))
    elif choice == '2':
        student_name = input("Enter student name: ")
        cursor.execute('SELECT * FROM students WHERE name = %s', (student_name,))
    else:
        print("\nInvalid choice. Returning to main menu.")
        prompt()
        return

    student = cursor.fetchone()
    if student:
        print("\nStudent Details:")
        print("{:<12} {:<20} {:<8} {:<12} {:<12}".format("Student ID", "Name", "Gender", "Year Level", "Course Code"))
        print("{:<12} {:<20} {:<8} {:<12} {:<12}".format(student[0], student[1], student[2], student[3], student[4]))
    else:
        print("\nStudent not found.")
    prompt()

# Course Add Function
def add_course():
    print("Enter course details:")
    course_code = input("Course Code: ")
    course_name = input("Course Name: ")

    cursor.execute('''
        INSERT INTO courses (course_code, course_name)
        VALUES (%s, %s)
    ''', (course_code, course_name))
    conn.commit()
    print("\nCourse created successfully!")
    prompt()

# Course Delete Function
def delete_course():
    course_code = input("Enter course code: ")
    cursor.execute('SELECT * FROM courses WHERE course_code = %s', (course_code,))
    course = cursor.fetchone()
    if course:
        confirm = input("\nPRESS '1' TO CONFIRM\nPRESS '2' TO CANCEL\n\nEnter choice: ")
        if confirm.lower() == '1':
            cursor.execute('DELETE FROM courses WHERE course_code = %s', (course_code,))
            conn.commit()
            print("\nCourse deleted successfully!")
        else:
            print("\nDeletion canceled.")
    else:
        print("\nCourse not found.")
    prompt()

# Course Edit Function
def edit_course():
    course_code = input("Enter course code: ")
    cursor.execute('SELECT * FROM courses WHERE course_code = %s', (course_code,))
    course = cursor.fetchone()
    if course:
        print("\nCurrent Course Details:")
        print("{:<12} {:<20}".format("Course Code", "Course Name"))
        print("{:<12} {:<20}".format(course[0], course[1]))

        print("\nEnter new course details:")
        course_name = input("Course Name (Press ENTER to skip): ")

        if course_name == '':
            course_name = course[1]

        cursor.execute('''
            UPDATE courses
            SET course_name = %s
            WHERE course_code = %s
        ''', (course_name, course_code))
        conn.commit()
        print("\nCourse updated successfully!")
    else:
        print("\nCourse not found.")
    prompt()

# Course List Function
def list_courses():
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    if courses:
        print("\nList of Courses:")
        print("{:<12} {:<20}".format("Course Code", "Course Name"))
        for course in courses:
            print("{:<12} {:<20}".format(course[0], course[1]))
    else:
        print("\nNo courses found.")
    prompt()

# Course Search Function
def search_course():
    course_code = input("Enter course code: ")
    cursor.execute('SELECT * FROM courses WHERE course_code = %s', (course_code,))
    course = cursor.fetchone()
    if course:
        print("\nCourse Details:")
        print("{:<12} {:<20}".format("Course Code", "Course Name"))
        print("{:<12} {:<20}".format(course[0], course[1]))
    else:
        print("\nCourse not found.")
    prompt()

def prompt():
    input("\nPress Enter to continue...")

# Main program
def main():
    while True:

        print("\n\nMAIN MENU")
        print("---------")
        print("1. Student Management")
        print("2. Course Management")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            student_menu()
        elif choice == '2':
            course_menu()
        elif choice == '0':
            break
        else:
            print("\nInvalid choice. Please try again.")
            prompt()

    conn.close()

if __name__ == '__main__':
    main()
