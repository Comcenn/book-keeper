from PySide6.QtWidgets import QTableView, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot

from book_keeper.views.dialogs.category_dialog import CategoryDialog
from book_keeper.views.models.category_table import CategoryTableModel


class CategoryView(QWidget):
    def __init__(self, category_model: CategoryTableModel) -> None:
        super().__init__()
        self.model = category_model

        self.table = QTableView()
        self.table.setModel(self.model)

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")

        add_btn.clicked.connect(self.add_category)
        edit_btn.clicked.connect(self.edit_category)
        delete_btn.clicked.connect(self.delete_category)

        btns = QHBoxLayout()
        btns.addWidget(add_btn)
        btns.addWidget(edit_btn)
        btns.addWidget(delete_btn)

        layout = QVBoxLayout()
        layout.addLayout(btns)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.table.resizeColumnsToContents()

    @Slot()
    def add_category(self) -> None:
        dlg = CategoryDialog()
        if dlg.exec():
            name = dlg.get_data()
            self.model.add_category(name)
            self.table.resizeColumnsToContents()

    @Slot()
    def edit_category(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return

        account = self.model.category_at(index.row())
        dlg = CategoryDialog()
        if dlg.exec():
            name = dlg.get_data()
            dto = account.model_copy(update={"name": name})
            self.model.update_category(index.row(), dto)
            self.table.resizeColumnsToContents()

    @Slot()
    def delete_category(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return
        self.model.delete_category(index.row())
        self.table.resizeColumnsToContents()
