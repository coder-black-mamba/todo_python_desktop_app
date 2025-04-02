import sys
import os
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot, pyqtProperty ,QUrl

# Database setup
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

# Backend class to handle database
class Backend(QObject):
    def __init__(self):
        super().__init__()

    @pyqtSlot(str, int, str)
    def addStudent(self, name, age, course):
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)", (name, age, course))
        conn.commit()
        conn.close()

    @pyqtSlot(result=list)
    def getStudents(self):
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        print(students)
        conn.close()
        return students

# Main PyQt Application
class WebApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")
        self.setGeometry(200, 100, 800, 600)
        
        self.setMinimumSize(800, 600)    


        self.browser = QWebEngineView()
        self.channel = QWebChannel()
        self.backend = Backend()
        self.channel.registerObject("backend", self.backend)
        self.browser.page().setWebChannel(self.channel)
        
        print(os.path.abspath("index.html"))
        # Load HTML file
        # self.browser.setUrl(QUrl.fromLocalFile(os.path.join(__path__, "web/index.html")))  # Replace with correct path
        # self.browser.setUrl(QUrl.fromLocalFile(os.path.join(__path__, "web/index.html")))
        file_path = os.path.abspath("./web/index.html")
        self.browser.setUrl(QUrl.fromLocalFile(file_path))
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

# Run the application
app = QApplication(sys.argv)
window = WebApp()
window.show()
sys.exit(app.exec())
