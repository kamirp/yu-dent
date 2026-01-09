from PySide6.QtWidgets import (
    QWidget, QGridLayout, QLabel,
    QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt

from ui.widgets.client_search import ClientSearchWidget
from db import get_connection


class TransferWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.client_pcode = None
        self.current_pfdetid = None
        self.current_pfgrid = None
        self.current_org_jid = None

        self.build_ui()
        self.bind_signals()

    # ================= UI =================
    def build_ui(self):
        grid = QGridLayout(self)
        grid.setSpacing(8)

        # --------- ПОИСК ПАЦИЕНТА ---------
        self.client_search = ClientSearchWidget()

        # --------- ТЕКУЩИЕ РЕЕСТРЫ ---------
        self.current_registries = QListWidget()
        # --- Откуда (красный акцент) ---
        self.current_registries.setStyleSheet("""
            QListWidget {
                border: 1px solid #999;
            }
            QListWidget::item:selected {
                background-color: #f8d7da;
                color: #721c24;
                font-weight: bold;
            }
        """)

        # --------- ОРГАНИЗАЦИИ ---------
        self.org_list = QListWidget()
        # --- Организации (нейтрально) ---
        self.org_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #999;
            }
            QListWidget::item:selected {
                background-color: #e2e3e5;
                color: #333;
            }
        """)

        # --------- РЕЕСТРЫ ОРГАНИЗАЦИИ ---------
        self.target_registries = QListWidget()
        # --- Куда (зелёно-голубой акцент) ---
        self.target_registries.setStyleSheet("""
            QListWidget {
                border: 1px solid #999;
            }
            QListWidget::item:selected {
                background-color: #d1ecf1;
                color: #0c5460;
                font-weight: bold;
            }
        """)

        # --------- ПОДПИСИ ---------
        lbl_current = QLabel("Текущие реестры пациента (откуда переносим)")
        lbl_orgs = QLabel("Организации")
        lbl_target = QLabel("Реестры организации (куда переносим)")

        for lbl in (lbl_current, lbl_orgs, lbl_target):
            lbl.setStyleSheet("font-weight: bold;")
            lbl.setAlignment(Qt.AlignCenter)

        # --------- LAYOUT ---------
        # верх — поиск на всю ширину
        grid.addWidget(self.client_search, 0, 0, 1, 3)

        # заголовки
        grid.addWidget(lbl_current, 1, 0)
        grid.addWidget(lbl_orgs, 1, 1)
        grid.addWidget(lbl_target, 1, 2)

        # списки
        grid.addWidget(self.current_registries, 2, 0)
        grid.addWidget(self.org_list, 2, 1)
        grid.addWidget(self.target_registries, 2, 2)

        # 🔑 КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: одинаковая ширина
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        grid.setRowStretch(2, 1)

    # ================= СИГНАЛЫ =================
    def bind_signals(self):
        self.client_search.clientSelected.connect(
            self.load_current_registries
        )

        self.org_list.itemClicked.connect(
            self.load_target_registries
        )

    # ================= ТЕКУЩИЕ РЕЕСТРЫ =================
    def load_current_registries(self, pcode: int):
        self.client_pcode = pcode
        self.current_registries.clear()
        self.org_list.clear()
        self.target_registries.clear()

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT
                pc.PFDETID,
                pc.PFGRID,
                pc2.PFGRNAME
            FROM
                PROF_CLIENTSDET pc
                JOIN PROF_CLIENTSGROUP pc2 ON pc.PFGRID = pc2.PFGRID
            WHERE
                pc.PCODE = ?
            ORDER BY
                pc2.FDATE DESC
        """, (pcode,))

        for pfdetid, pfgrid, name in cur.fetchall():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, (pfdetid, pfgrid))
            self.current_registries.addItem(item)

        con.close()

        self.load_organizations()

    # ================= ОРГАНИЗАЦИИ =================
    def load_organizations(self):
        self.org_list.clear()

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT j.JID, j.JNAME
            FROM JPERSONS j
            WHERE j.JID IN (10822, 238, 10824, 10825, 10826, 10832, 10833, 10842)
            ORDER BY j.JNAME
        """)

        for jid, name in cur.fetchall():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, jid)
            self.org_list.addItem(item)

        con.close()

    # ================= РЕЕСТРЫ ОРГАНИЗАЦИИ =================
    def load_target_registries(self, item: QListWidgetItem):
        self.target_registries.clear()
        self.current_org_jid = item.data(Qt.UserRole)

        con = get_connection()
        cur = con.cursor()

        cur.execute("""
            SELECT
                pc.PFGRID,
                pc.PFGRNAME
            FROM
                JPERSONS j
                JOIN JPAGREEMENT j2 ON j.JID = j2.JID
                JOIN PROF_CLIENTSGROUP pc ON j2.AGRID = pc.AGRID
            WHERE
                j.JID = ?
            ORDER BY
                pc.FDATE DESC
        """, (self.current_org_jid,))

        for pfgrid, name in cur.fetchall():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, pfgrid)
            self.target_registries.addItem(item)

        con.close()
