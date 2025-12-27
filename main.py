import sys
from PySide6.QtWidgets import QApplication
from ui.login import LoginWindow
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icons/app.png"))

w = LoginWindow()
w.show()

sys.exit(app.exec())
