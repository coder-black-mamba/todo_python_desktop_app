import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
import qdarkstyle

class DarkThemeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDarkStyle Example")
        self.resize(400, 300)

        self.button = QPushButton("Click Me")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet())  # Apply the dark theme
window = DarkThemeWindow()
window.show()
sys.exit(app.exec())
