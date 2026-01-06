from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit,
    QPushButton, QMessageBox, QLabel
)


class ReasonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Причина удаления")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        label = QLabel("Укажите причину удаления пациента из реестра:")
        self.text = QTextEdit()

        self.ok_btn = QPushButton("Удалить")
        self.cancel_btn = QPushButton("Отмена")

        layout.addWidget(label)
        layout.addWidget(self.text)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)

        self.ok_btn.clicked.connect(self.accept_reason)
        self.cancel_btn.clicked.connect(self.reject)

    def accept_reason(self):
        if not self.text.toPlainText().strip():
            QMessageBox.warning(
                self, "Ошибка", "Причина удаления обязательна"
            )
            return

        self.accept()

    def get_reason(self) -> str:
        return self.text.toPlainText().strip()
