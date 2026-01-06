from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget,
    QListWidgetItem, QLabel
)
from PySide6.QtCore import Qt, Signal

from db import get_connection


class ClientRegistryInfo(QWidget):
    registrySelected = Signal(int)  # PFDETID
    deleted = Signal()

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.title = QLabel("Реестры пациента")
        self.title.setStyleSheet("font-weight: bold;")

        self.list = QListWidget()
        self.list.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.title)
        layout.addWidget(self.list)

        self.pcode = None
        self.pfdetid = None

    def clear(self):
        self.list.clear()
        self.pcode = None
        self.pfdetid = None

    def load_registries(self, pcode: int):
        self.clear()
        self.pcode = pcode

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT pc.PFDETID, pc2.PFGRNAME
            FROM PROF_CLIENTSDET pc
            JOIN PROF_CLIENTSGROUP pc2 ON pc.PFGRID = pc2.PFGRID
            WHERE pc.PCODE = ?
            ORDER BY pc2.FDATE DESC
        """, (pcode,))

        for pfdetid, name in cur.fetchall():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, pfdetid)
            self.list.addItem(item)

        con.close()

    def reload(self):
        if self.pcode:
            self.load_registries(self.pcode)

    def on_item_clicked(self, item: QListWidgetItem):
        self.pfdetid = item.data(Qt.UserRole)
        self.registrySelected.emit(self.pfdetid)
