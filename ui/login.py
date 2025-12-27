from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox,
    QLineEdit, QPushButton, QMessageBox
)

from auth import get_users, check_password, load_user_session
from session import Session
from ui.main_window import MainWindow


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Вход в систему")
        self.setModal(True)
        self.resize(300, 140)

        layout = QVBoxLayout(self)

        # ===== Выбор пользователя =====
        self.user_box = QComboBox()
        self.user_box.setEditable(False)

        # ===== Пароль =====
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Пароль")

        # ===== Кнопка входа =====
        self.login_btn = QPushButton("Войти")
        self.login_btn.setDefault(True)
        self.login_btn.setAutoDefault(True)

        layout.addWidget(self.user_box)
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)

        self.load_users()

        # ===== Сигналы =====
        self.login_btn.clicked.connect(self.login)
        self.password.returnPressed.connect(self.login)

    # ---------- загрузка логинов ----------
    def load_users(self):
        self.users = get_users()
        for dcode, dname in self.users:
            self.user_box.addItem(dname, dcode)

        if self.users:
            self.password.setFocus()

    # ---------- вход ----------
    def login(self):
        dcode = self.user_box.currentData()
        pwd = self.password.text().strip()

        if not pwd:
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            return

        if not check_password(dcode, pwd):
            QMessageBox.warning(self, "Ошибка", "Неверный пароль")
            self.password.selectAll()
            self.password.setFocus()
            return

        self.accept_login(dcode)

    # ---------- успешный вход ----------
    def accept_login(self, dcode: int):
        data = load_user_session(dcode)
        if not data:
            QMessageBox.warning(
                self, "Ошибка", "Не удалось загрузить данные пользователя"
            )
            return

        # ===== Session =====
        Session.dcode = dcode
        Session.dname = data["dname"]
        Session.accesslevel = data["accesslevel"]
        Session.drights = data["drights"]
        Session.filial = data["filial"]

        # ===== Главное окно =====
        self.main = MainWindow()
        self.main.show()

        self.accept()  # закрывает диалог корректно
