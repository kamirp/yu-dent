from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget,
    QListWidgetItem, QLabel
)
from PySide6.QtCore import Qt, Signal

from db import get_connection


class ClientRegistryInfo(QWidget):
    """
    Отображает список реестров пациента.
    Эмитит registrySelected(pfdetid) при выборе.
    """

    registrySelected = Signal(int)  # PFDETID

    def __init__(self):
        super().__init__()

        self.pcode = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.title = QLabel("Реестры пациента")
        self.title.setStyleSheet("font-weight: bold;")

        self.list = QListWidget()
        self.list.itemClicked.connect(self.on_item_clicked)

        layout.addWidget(self.title)
        layout.addWidget(self.list)

    # ================= ЗАГРУЗКА РЕЕСТРОВ =================
    def load_registries(self, pcode: int):
        self.pcode = pcode
        self.list.clear()

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT pc.PFDETID, pc2.PFGRNAME
            FROM PROF_CLIENTSDET pc
            JOIN PROF_CLIENTSGROUP pc2
              ON pc.PFGRID = pc2.PFGRID
            WHERE pc.PCODE = ?
            ORDER BY pc2.FDATE DESC
        """, (pcode,))

        rows = cur.fetchall()
        cur.close()
        con.close()

        if not rows:
            self.list.addItem("Реестры не найдены")
            self.list.setEnabled(False)
            return

        self.list.setEnabled(True)

        for pfdetid, name in rows:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, pfdetid)
            self.list.addItem(item)

    # ================= ВЫБОР РЕЕСТРА =================
    def on_item_clicked(self, item: QListWidgetItem):
        pfdetid = item.data(Qt.UserRole)

        if pfdetid is None:
            return

        self.registrySelected.emit(pfdetid)
