from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout,
    QLabel, QPushButton, QMessageBox, QDialog
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

from ui.widgets.client_search import ClientSearchWidget
from ui.widgets.client_registry_info import ClientRegistryInfo
from ui.dialogs.reason_dialog import ReasonDialog

from db import get_connection
from session import Session


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IC+")
        self.setWindowIcon(QIcon("icons/app.png"))
        self.showMaximized()

        self.create_menu()
        self.show_welcome()

    # ---------------- МЕНЮ ----------------
    def create_menu(self):
        menubar = self.menuBar()

        prof_menu = menubar.addMenu("Профосмотры")
        registry_menu = prof_menu.addMenu("Реестры")

        delete_action = QAction("Удаление пациентов", self)
        delete_action.triggered.connect(self.open_delete_patients)
        registry_menu.addAction(delete_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

    # ---------------- СТАРТОВЫЙ ЭКРАН ----------------
    def show_welcome(self):
        widget = QWidget(self)
        layout = QGridLayout(widget)

        label = QLabel(
            f"Пользователь: {Session.dname}\nФилиал: {Session.filial}"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #999;")

        layout.addWidget(label, 0, 0)
        self.setCentralWidget(widget)

    # ---------------- ОСНОВНОЙ ЭКРАН ----------------
    def open_delete_patients(self):
        central = QWidget(self)
        grid = QGridLayout(central)
        grid.setSpacing(8)

        # ===== ВИДЖЕТЫ =====
        self.client_search = ClientSearchWidget()
        self.client_info = ClientRegistryInfo()

        self.delete_btn = QPushButton("Удалить пациента")
        self.delete_btn.setEnabled(False)

        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #4aa3df;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:disabled {
                background-color: #b0cfe8;
                color: #eeeeee;
            }
            QPushButton:hover:!disabled {
                background-color: #3796d6;
            }
        """)

        # ===== LAYOUT =====
        # верхняя строка
        grid.addWidget(self.client_search, 0, 0)
        grid.addWidget(self.delete_btn, 0, 1, alignment=Qt.AlignTop)

        # нижняя строка (на всю ширину)
        grid.addWidget(self.client_info, 1, 0, 1, 2)

        grid.setColumnStretch(0, 4)
        grid.setColumnStretch(1, 1)
        grid.setRowStretch(1, 1)

        self.setCentralWidget(central)

        # ===== СИГНАЛЫ =====
        self.client_search.clientSelected.connect(
            self.client_info.load_registries
        )
        self.client_info.registrySelected.connect(
            self.enable_delete
        )
        self.client_info.deleted.connect(
            self.client_info.reload
        )
        self.delete_btn.clicked.connect(
            self.delete_selected
        )

    # ---------------- АКТИВАЦИЯ КНОПКИ ----------------
    def enable_delete(self, pfdetid: int):
        self.delete_btn.setEnabled(True)

    # ---------------- УДАЛЕНИЕ ----------------
    def delete_selected(self):
        pfdetid = self.client_info.pfdetid
        if not pfdetid:
            return

        dlg = ReasonDialog(self)
        if dlg.exec() != QDialog.Accepted:
            return

        reason = dlg.get_reason()

        if QMessageBox.question(
            self,
            "Подтверждение",
            "Удалить пациента из выбранного реестра?",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            return

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM PROF_JORNAL WHERE PFDETID = ?", (pfdetid,)
        )
        cur.execute(
            "DELETE FROM PROF_CLIENTSDET WHERE PFDETID = ?", (pfdetid,)
        )

        cur.execute("""
            INSERT INTO PROF_DELETE_LOG
            (PFDETID, DCODE, REASON, LOGDATE)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (pfdetid, Session.dcode, reason))

        con.commit()
        con.close()

        QMessageBox.information(
            self, "Готово", "Пациент удалён из реестра"
        )

        self.delete_btn.setEnabled(False)
        self.client_info.reload()
