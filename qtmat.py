import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from qt_material import apply_stylesheet

class MaterialWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Material UI Example")
        self.resize(400, 300)

        self.button = QPushButton("Material Button")
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

app = QApplication(sys.argv)
apply_stylesheet(app, theme='dark_teal.xml')  # Apply Material Design theme
window = MaterialWindow()
window.show()
sys.exit(app.exec())
