import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, 
                            QMessageBox)
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet
import sqlite3

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# mongo credes
# import MONGO_USER,MONGO_PASSWORD from "./.env.py"
from env import *

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@freecluster.mwshian.mongodb.net/?retryWrites=true&w=majority&appName=freeCluster"

print(uri)
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# print(db)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db=client["todo_app"]
todo_collection = db["todos"]


class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo App")
        self.resize(500, 400)
        
        # Create database and table
        self.create_database()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create input field and buttons
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a task...")
        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(self.add_button)
        
        # Create list widget
        self.task_list = QListWidget()
        
        # Create action buttons
        button_layout = QHBoxLayout()
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.update_button.clicked.connect(self.update_task)
        self.delete_button.clicked.connect(self.delete_task)
        
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        
        # Add all widgets to main layout
        layout.addLayout(input_layout)
        layout.addWidget(self.task_list)
        layout.addLayout(button_layout)
        
        # Load existing tasks
        self.load_tasks()

    def create_database(self):
        conn = sqlite3.connect('todos.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             task TEXT NOT NULL)
        ''')
        conn.commit()
        conn.close()

    def load_tasks(self):
        self.task_list.clear()
        conn = sqlite3.connect('todos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        tasks2 = todo_collection.find()
        for task in tasks2:
            print(task["_id"])
            self.task_list.addItem(str(task["task"]))

        # for task in tasks:
        #     self.task_list.addItem(str(task[0]) + ": " + task[1])
        conn.close()

    def add_task(self):
        task = self.task_input.text().strip()
        if task:
            conn = sqlite3.connect('todos.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            todo_collection.insert_one({"task":task})
            conn.commit()
            conn.close()
            self.task_input.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a task!")

    def update_task(self):
        current_item = self.task_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a task to update!")
            return
        
        task_id = int(current_item.text().split(':')[0])
        new_task = self.task_input.text().strip()
        
        if new_task:
            conn = sqlite3.connect('todos.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
            conn.commit()
            conn.close()
            self.task_input.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Please enter a task!")

    def delete_task(self):
        current_item = self.task_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a task to delete!")
            return
        
        task_id = int(current_item.text().split(':')[0])
        
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                   'Are you sure you want to delete this task?',
                                   QMessageBox.StandardButton.Yes |
                                   QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('todos.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()
            conn.close()
            self.load_tasks()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_teal.xml')
    window = TodoApp()
    window.show()
    sys.exit(app.exec())
