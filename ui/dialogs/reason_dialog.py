from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit,
    QPushButton, QMessageBox
)


class ReasonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Причина удаления")

        layout = QVBoxLayout(self)

        self.text = QTextEdit()
        self.text.setPlaceholderText("Укажите причину удаления")

        self.ok_btn = QPushButton("Подтвердить")
        self.ok_btn.clicked.connect(self.accept_reason)

        layout.addWidget(self.text)
        layout.addWidget(self.ok_btn)

    def accept_reason(self):
        if not self.text.toPlainText().strip():
            QMessageBox.warning(
                self,
                "Ошибка",
                "Причина удаления обязательна"
            )
            return

        self.accept()

    def get_reason(self) -> str:
        return self.text.toPlainText().strip()
