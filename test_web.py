import sys
import os
import time
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView 
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QObject, pyqtSlot, pyqtProperty ,QUrl 
from PyQt6.QtWebEngineCore import QWebEngineSettings
# debugging devtools
os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9000'  # Set debugging port to 9000

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
        time.sleep(5)  # Simulate delay
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        # Convert tuples to lists for JSON serialization
        students_list = [list(student) for student in students]
        print(students_list)  # Debug print
        conn.close()
        return students_list
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
        # self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)
        # self.browser.settings().setAttribute(QWebEngineSettings.DeveloperExtrasEnabled, True)
        # self.browser.settings().setAttribute(QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)
        # self.browser.settings().setAttribute(QWebEngineSettings.DeveloperExtrasEnabled, True)
        


        print(os.path.abspath("index.html"))
        # Load HTML file
        # self.browser.setUrl(QUrl.fromLocalFile(os.path.join(__path__, "web/index.html")))  # Replace with correct path
        # self.browser.setUrl(QUrl.fromLocalFile(os.path.join(__path__, "web/index.html")))
        file_path = os.path.abspath("./web/index.html")
        self.browser.setUrl(QUrl.fromLocalFile(file_path))
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # removing margins
        # self.browser.setStyleSheet("QMainWindow { margin: 0px; }")
        layout.setContentsMargins(0, 0, 0, 0)  # No margins
        layout.setSpacing(0)  # No spacing

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)






# Run the application
app = QApplication(sys.argv)
window = WebApp()
window.show()
sys.exit(app.exec())
