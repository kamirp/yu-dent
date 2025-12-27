from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt

from db import get_connection


class ClientRegistryInfo(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.title = QLabel("Реестры пациента")
        self.title.setStyleSheet("font-weight: bold;")

        self.list = QListWidget()

        layout.addWidget(self.title)
        layout.addWidget(self.list)

    def load_registries(self, pcode: int):
        self.list.clear()

        con = get_connection()
        cur = con.cursor()

        try:
            cur.execute("""
                SELECT pc2.PFGRNAME
                FROM CLIENTS c
                JOIN PROF_CLIENTSDET pc ON c.PCODE = pc.PCODE
                JOIN PROF_CLIENTSGROUP pc2 ON pc.PFGRID = pc2.PFGRID
                WHERE c.PCODE = ?
                ORDER BY pc2.FDATE DESC
            """, (pcode,))

            rows = cur.fetchall()

            if not rows:
                self.list.addItem("Реестры не найдены")
                return

            for (name,) in rows:
                item = QListWidgetItem(name)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.list.addItem(item)

        finally:
            cur.close()
            con.close()
