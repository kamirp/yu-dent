from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLabel
)
from PySide6.QtGui import QAction, QIcon

from ui.widgets.client_search import ClientSearchWidget

from session import Session


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IC+")
        self.setWindowIcon(QIcon("icons/app.png"))

        self.create_menu()
        self.showMaximized()

    def create_menu(self):
        menubar = self.menuBar()

        # ===== Профосмотры =====
        prof_menu = menubar.addMenu("Профосмотры")

        # ----- Реестры -----
        registry_menu = prof_menu.addMenu("Реестры")

        # Удаление пациентов
        delete_patients_action = QAction("Удаление пациентов", self)
        delete_patients_action.triggered.connect(self.open_delete_patients)
        registry_menu.addAction(delete_patients_action)

        # ===== Выход =====
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

    def open_delete_patients(self):
        central = QWidget(self)
        grid = QGridLayout(central)
        grid.setSpacing(6)

        w1 = ClientSearchWidget()
        w2 = QLabel("Список пациентов")
        w3 = QLabel("Информация")
        w4 = QLabel("Лог / действия")

        for w in (w1, w2, w3, w4):
            w.setStyleSheet(
                "border: 1px solid #999;"
                "background: #f5f5f5;"
                "padding: 8px;"
            )

        grid.addWidget(w1, 0, 0)
        grid.addWidget(w2, 0, 1)
        grid.addWidget(w3, 1, 0)
        grid.addWidget(w4, 1, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)

        self.setCentralWidget(central)