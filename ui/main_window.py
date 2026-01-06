from PySide6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLabel
)
from PySide6.QtGui import QAction, QIcon

from ui.widgets.client_search import ClientSearchWidget
from ui.widgets.client_registry_info import ClientRegistryInfo
from ui.widgets.delete_actions import DeleteActionWidget

from session import Session


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IC+")
        self.setWindowIcon(QIcon("icons/app.png"))

        self._build_menu()
        self.showMaximized()

    # ===== МЕНЮ =====
    def _build_menu(self):
        menubar = self.menuBar()

        prof_menu = menubar.addMenu("Профосмотры")
        registry_menu = prof_menu.addMenu("Реестры")

        action = QAction("Удаление пациентов", self)
        action.triggered.connect(self.open_delete_patients)
        registry_menu.addAction(action)

        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

    # ===== ОСНОВНОЙ ЭКРАН =====
    def open_delete_patients(self):
        central = QWidget(self)
        grid = QGridLayout(central)
        grid.setSpacing(6)

        # --- Виджеты ---
        self.client_search = ClientSearchWidget()
        self.client_info = ClientRegistryInfo()
        self.delete_action = DeleteActionWidget()

        log_label = QLabel(
            f"Пользователь: {Session.dname}\n"
            f"Филиал: {Session.filial}"
        )
        log_label.setStyleSheet(
            "border:1px solid #999; background:#f5f5f5; padding:8px;"
        )

        # --- Раскладка ---
        grid.addWidget(self.client_search, 0, 0)   # Поиск
        grid.addWidget(log_label,         0, 1)   # Лог
        grid.addWidget(self.client_info,  1, 0)   # Реестры
        grid.addWidget(self.delete_action,1, 1)   # Удаление

        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 2)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)

        self.setCentralWidget(central)

        # --- СИГНАЛЫ ---
        self.client_search.clientSelected.connect(
            self.client_info.load_registries
        )

        self.client_info.registrySelected.connect(
            self.on_registry_selected
        )

        self.delete_action.deleted.connect(
            self.refresh_registries
        )

    # ===== СЛОТЫ =====
    def on_registry_selected(self, pfdetid: int):
        print("Выбран реестр PFDETID =", pfdetid)  # 👈 полезно для отладки
        self.delete_action.set_registry(
            pfdetid,
            self.client_info.pcode
        )

    def refresh_registries(self):
        if self.client_info.pcode:
            self.client_info.load_registries(
                self.client_info.pcode
            )
