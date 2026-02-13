from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableView,
    QHBoxLayout,
    QPushButton,
    QDialog,
    QMessageBox,
    QHeaderView,
)

from book_keeper.repositories.transaction import LineDto
from book_keeper.views.dialogs.line_edit_dialog import LineEditDialog
from book_keeper.views.models.category_table import CategoryTableModel
from book_keeper.views.models.line_table import LineModel


class LinesEditor(QWidget):
    def __init__(self, category_model: CategoryTableModel, parent=None) -> None:
        super().__init__(parent)

        self._cat_model = category_model

        layout = QVBoxLayout(self)

        self.table = QTableView()
        self.table.setAlternatingRowColors(True)
        self.model = LineModel(category_model)
        self.table.setModel(self.model)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # category
        header.setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )  # amount
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        layout.addLayout(btn_layout)

        self.add_btn = QPushButton("Add Line")
        self.edit_btn = QPushButton("Edit Line")
        self.remove_btn = QPushButton("Remove Line")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.remove_btn)

        self.add_btn.clicked.connect(self._add_line)
        self.edit_btn.clicked.connect(self._edit_line)
        self.remove_btn.clicked.connect(self._remove_line)

    def get_lines(self) -> list[LineDto]:
        return self.model.get_lines()

    def set_lines(self, lines: list[LineDto]) -> None:
        self.model.set_lines(lines)

    def _add_line(self) -> None:
        dlg = LineEditDialog(self._cat_model, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            line = dlg.get_line()
            if line:
                self.model.add_line(line.category_id, line.amount)

    def _edit_line(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        line = self.model.get_line(row)
        dlg = LineEditDialog(self._cat_model, line, parent=self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            updated = dlg.get_line()
            if updated:
                self.model.update_line(row, updated)

    def _remove_line(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return

        row = index.row()
        reply = QMessageBox.question(
            self,
            "Remove Line",
            "Are you sure you want to remove this line?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.remove_line(row)
