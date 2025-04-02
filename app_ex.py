import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLineEdit, QSpinBox, QLabel, QTableWidget, QHeaderView
import qdarkstyle
from qt_material import apply_stylesheet
import sqlite3

def create_database():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            course TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_database()

class StudentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setGeometry(300, 200, 600, 400)

        # Layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter student name")
        self.name_input.setStyleSheet("QLineEdit::placeholder { color: white; }")

        self.age_input = QSpinBox(self)
        self.age_input.setRange(10, 100)
        self.age_input.setValue(18)

        self.course_input = QLineEdit(self)
        self.course_input.setPlaceholderText("Enter course")

        self.add_button = QPushButton("Add Student")
        self.add_button.clicked.connect(self.add_student)

        self.delete_button = QPushButton("Delete Student")
        self.delete_button.clicked.connect(self.delete_student)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Age", "Course"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Add widgets to layout
        self.layout.addWidget(QLabel("Student Name:"))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Age:"))
        self.layout.addWidget(self.age_input)
        self.layout.addWidget(QLabel("Course:"))
        self.layout.addWidget(self.course_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.table)

        self.load_students()

    def add_student(self):
        name = self.name_input.text()
        age = self.age_input.value()
        course = self.course_input.text()

        if name and course:
            conn = sqlite3.connect("students.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
            conn.commit()
            conn.close()

            self.name_input.clear()
            self.course_input.clear()
            self.load_students()
            QMessageBox.information(self, "Success", "Student added successfully!")
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields!")

    def load_students(self):
        self.table.setRowCount(0)
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        conn.close()

        for row_num, student in enumerate(students):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(student):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def delete_student(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Error", "Select a student to delete!")
            return

        student_id = self.table.item(selected, 0).text()
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()

        self.load_students()
        QMessageBox.information(self, "Deleted", "Student removed!")

# Run application
app = QApplication(sys.argv)

# 🎨 Apply QDarkStyle OR Qt-Material theme
use_qdarkstyle = False  # Change to True for QDarkStyle

if use_qdarkstyle:
    app.setStyleSheet(qdarkstyle.load_stylesheet())
else:
    apply_stylesheet(app, theme='dark_cyan.xml')

window = StudentApp()
window.show()
sys.exit(app.exec())
