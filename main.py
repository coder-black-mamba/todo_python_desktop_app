import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QListWidget, 
                             QMessageBox)
from PyQt6.QtCore import Qt
import sqlite3

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do App")
        self.setGeometry(100, 100, 400, 500)  # Position and size of window

        # Set up the database
        self.init_db()

        # Create the main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Input field for new tasks
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a new task...")
        self.layout.addWidget(self.task_input)

        # Buttons for adding and deleting tasks
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Task")
        self.delete_button = QPushButton("Delete Selected")
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.delete_button)
        self.layout.addLayout(self.button_layout)

        # List to display tasks
        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        # Connect buttons to functions
        self.add_button.clicked.connect(self.add_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.task_list.itemDoubleClicked.connect(self.toggle_task_completion)

        # Load tasks from database
        self.load_tasks()

    def init_db(self):
        # Create SQLite database and table
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                            (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER)''')
        self.conn.commit()
    def load_tasks(self):
        # Load tasks from database into the list
        self.task_list.clear()
        self.cursor.execute("SELECT id, task, completed FROM tasks")
        for task_id, task_text, completed in self.cursor.fetchall():
            item = f"[{'✓' if completed else ' '}] {task_text}"
            list_item = QListWidgetItem(item)
            list_item.setData(Qt.ItemDataRole.UserRole, task_id)  # Store task ID
            if completed:
                list_item.setFlags(list_item.flags() & ~Qt.ItemFlag.ItemIsEnabled)  # Disable if completed
            self.task_list.addItem(list_item)

    def add_task(self):
        # Add a new task to the database and list
        task_text = self.task_input.text().strip()
        if task_text:
            self.cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, 0)", (task_text,))
            self.conn.commit()
            self.task_input.clear()
            self.load_tasks()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a task!")

    def delete_task(self):
        # Delete the selected task
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select a task to delete!")
            return
        for item in selected_items:
            task_id = item.data(Qt.ItemDataRole.UserRole)
            self.cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def toggle_task_completion(self, item):
        # Toggle task completion status
        task_id = item.data(Qt.ItemDataRole.UserRole)
        self.cursor.execute("SELECT completed FROM tasks WHERE id = ?", (task_id,))
        completed = self.cursor.fetchone()[0]
        new_status = 0 if completed else 1
        self.cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (new_status, task_id))
        self.conn.commit()
        self.load_tasks()

    def closeEvent(self, event):
        # Close database connection when app closes
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec())