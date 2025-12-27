from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLabel
)
from PySide6.QtGui import QAction, QIcon

from ui.widgets.client_search import ClientSearchWidget
from ui.widgets.client_registry_info import ClientRegistryInfo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IC+")
        self.setWindowIcon(QIcon("icons/app.png"))

        self.delete_patients_widget = None

        self.create_menu()
        self.showMaximized()

    def create_menu(self):
        menubar = self.menuBar()

        prof_menu = menubar.addMenu("Профосмотры")
        registry_menu = prof_menu.addMenu("Реестры")

        delete_patients_action = QAction("Удаление пациентов", self)
        delete_patients_action.triggered.connect(self.open_delete_patients)
        registry_menu.addAction(delete_patients_action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

    def open_delete_patients(self):
        if self.delete_patients_widget:
            self.setCentralWidget(self.delete_patients_widget)
            return

        central = QWidget(self)
        grid = QGridLayout(central)
        grid.setSpacing(6)

        self.client_search = ClientSearchWidget()
        self.client_info = ClientRegistryInfo()

        w2 = QLabel("Список пациентов")
        w4 = QLabel("Лог / действия")

        for w in (w2, w4):
            w.setStyleSheet(
                "border: 1px solid #999;"
                "background: #f5f5f5;"
                "padding: 8px;"
            )

        grid.addWidget(self.client_search, 0, 0)
        grid.addWidget(w2, 0, 1)
        grid.addWidget(self.client_info, 1, 0)
        grid.addWidget(w4, 1, 1)

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 2)

        self.setCentralWidget(central)
        self.delete_patients_widget = central

        self.client_search.clientSelected.connect(
            self.client_info.load_registries
        )
