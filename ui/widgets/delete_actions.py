from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton,
    QMessageBox
)
from PySide6.QtCore import Signal

from db import get_connection
from session import Session
from ui.dialogs.reason_dialog import ReasonDialog


class DeleteActionWidget(QWidget):
    deleted = Signal()

    def __init__(self):
        super().__init__()

        self.pfdetid = None
        self.pcode = None

        layout = QVBoxLayout(self)

        self.delete_btn = QPushButton("Удалить пациента из реестра")
        self.delete_btn.setEnabled(False)

        layout.addWidget(self.delete_btn)

        self.delete_btn.clicked.connect(self.ask_and_delete)

    def set_registry(self, pfdetid: int, pcode: int):
        self.pfdetid = pfdetid
        self.pcode = pcode
        self.delete_btn.setEnabled(True)

    def ask_and_delete(self):
        dlg = ReasonDialog(self)

        if not dlg.exec():
            return

        reason = dlg.get_reason()
        self.delete_registry(reason)

    def delete_registry(self, reason: str):
        con = get_connection()
        cur = con.cursor()

        try:
            # удаляем из журналов
            cur.execute(
                "DELETE FROM PROF_JORNAL WHERE PFDETID = ?",
                (self.pfdetid,)
            )

            cur.execute(
                "DELETE FROM PROF_CLIENTSDET WHERE PFDETID = ?",
                (self.pfdetid,)
            )

            # логируем
            cur.execute("""
                INSERT INTO PROF_DELETE_LOG
                (LOGDATE, DCODE, DNAME, PCODE, PFDETID, REASON)
                VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
            """, (
                Session.dcode,
                Session.dname,
                self.pcode,
                self.pfdetid,
                reason
            ))

            con.commit()

        except Exception as e:
            con.rollback()
            QMessageBox.critical(self, "Ошибка", str(e))
            return

        finally:
            con.close()

        QMessageBox.information(
            self, "Готово", "Пациент удалён из реестра"
        )

        self.delete_btn.setEnabled(False)
        self.pfdetid = None

        self.deleted.emit()
