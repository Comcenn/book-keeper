from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QHBoxLayout, QPushButton, QDialog, QMessageBox

from book_keeper.repositories.transaction import Line
from book_keeper.views.dialogs.line_edit_dialog import LineEditDialog
from book_keeper.views.models.line_table import LineModel
from book_keeper.views.transaction.transaction_detail.lines_editor.category_delegate import CategoryDelegate


class LinesEditor(QWidget):
    def __init__(self, categories: dict[int, str], parent=None) -> None:
        super().__init__(parent)

        self._categories = categories

        layout = QVBoxLayout(self)

        self.table = QTableView()
        self.model = LineModel(categories)
        self.table.setModel(self.model)

        delegate = CategoryDelegate(categories)
        self.table.setItemDelegateForColumn(LineModel.COL_CATEGORY, delegate)

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
    
    def get_lines(self) -> list[Line]:
        return self.model.get_lines()
    
    def set_lines(self, lines: list[Line]) -> None:
        self.model.set_lines(lines)
    
    def _add_line(self) -> None:
        dlg = LineEditDialog(self._categories, parent=self)
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
        dlg = LineEditDialog(self._categories, line, parent=self)
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
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.model.remove_line(row)