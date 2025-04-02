import sys
from PyQt6.QtWidgets import QApplication, QWidget,  QLabel, QVBoxLayout, QPushButton


# app  = QApplication(sys.argv)

# window = QWidget()

# window.setWindowTitle("Test 1")
# # window.setGeometry(100, 100, 300, 200)
# window.button = QPushButton("Click me")
# window.show()
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test 1")
        self.button = QPushButton("Click me")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        # self.show() 


app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
