import sqlite3

# Connect to SQLite DB
db = sqlite3.connect("A3_05_4_2_43.db")
cursor = db.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    roll_no INTEGER PRIMARY KEY,
    math INTEGER DEFAULT 0,
    science INTEGER DEFAULT 0,
    english INTEGER DEFAULT 0,
    total INTEGER DEFAULT 0,
    FOREIGN KEY (roll_no) REFERENCES students(roll_no)
)
""")

db.commit()


# ==============================
# ADMIN FUNCTION
# ==============================

def add_student():
    roll = int(input("Enter Roll Number: "))
    name = input("Enter Name: ")

    cursor.execute("INSERT INTO students VALUES (?, ?)", (roll, name))
    cursor.execute("INSERT INTO marks (roll_no) VALUES (?)", (roll,))
    db.commit()

    print("Student added successfully.")


# ==============================
# TEACHER FUNCTIONS
# ==============================

def update_marks(subject):
    roll = int(input("Enter Roll Number: "))
    mark = int(input(f"Enter {subject} marks: "))

    if subject == "math":
        cursor.execute("UPDATE marks SET math=? WHERE roll_no=?", (mark, roll))
    elif subject == "science":
        cursor.execute("UPDATE marks SET science=? WHERE roll_no=?", (mark, roll))
    elif subject == "english":
        cursor.execute("UPDATE marks SET english=? WHERE roll_no=?", (mark, roll))

    db.commit()
    print(f"{subject} marks updated.")


def view_students():
    cursor.execute("SELECT roll_no, name FROM students")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


# ==============================
# FINAL SUBMISSION
# ==============================

def calculate_total():
    cursor.execute("""
    UPDATE marks
    SET total = math + science + english
    """)
    db.commit()


def view_results():
    calculate_total()

    cursor.execute("""
    SELECT students.roll_no, students.name, marks.math, marks.science, marks.english, marks.total
    FROM students
    JOIN marks ON students.roll_no = marks.roll_no
    ORDER BY marks.total DESC
    """)

    rows = cursor.fetchall()

    print("\n===== FINAL RESULT (Sorted by Total Marks) =====")
    for row in rows:
        print(row)


# ==============================
# MAIN MENU
# ==============================

while True:
    print("\n===== Marks Management System =====")
    print("1. Add Student (Admin)")
    print("2. View Students")
    print("3. Math Teacher Update")
    print("4. Science Teacher Update")
    print("5. English Teacher Update")
    print("6. View Final Result")
    print("7. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        update_marks("math")

    elif choice == "4":
        update_marks("science")

    elif choice == "5":
        update_marks("english")

    elif choice == "6":
        view_results()

    elif choice == "7":
        break

    else:
        print("Invalid choice")
