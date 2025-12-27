from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,
    QListWidget, QListWidgetItem, QLabel
)
from PySide6.QtCore import Qt

from db import get_connection


class ClientSearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите ФИО пациента (от 3 символов)")
        self.search_edit.textChanged.connect(self.on_text_changed)

        self.results = QListWidget()
        self.results.itemClicked.connect(self.on_item_clicked)

        self.selected_label = QLabel("Пациент не выбран")
        self.selected_label.setStyleSheet("font-weight: bold;")

        layout.addWidget(self.search_edit)
        layout.addWidget(self.results)
        layout.addWidget(self.selected_label)

        self.client_id = None

    # ---------- поиск ----------
    def on_text_changed(self, text: str):
        self.results.clear()
        self.client_id = None

        if len(text.strip()) < 3:
            return

        self.search_clients(text.strip())

    def search_clients(self, text: str):
        con = get_connection()
        cur = con.cursor()
        cur.execute("""
            SELECT PCODE, FULLNAME, BDATE
            FROM CLIENTS
            WHERE UPPER(FULLNAME) STARTING WITH ?
            ROWS 20
        """, (text.upper(),))

        for client_id, fullname, bdate in cur.fetchall():
            label = f"{fullname} ({bdate:%d.%m.%Y})"
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, (client_id, fullname, bdate))
            self.results.addItem(item)

        con.close()

    # ---------- выбор ----------
    def on_item_clicked(self, item: QListWidgetItem):
        client_id, fullname, bdate = item.data(Qt.UserRole)

        self.client_id = client_id
        self.selected_label.setText(
            f"Выбран пациент:\n{fullname}\nДата рождения: {bdate:%d.%m.%Y}"
        )

        self.results.clear()
        self.search_edit.setText(fullname)
