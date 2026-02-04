from PySide6.QtWidgets import QTableView, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot

from book_keeper.repositories.category import CategoryRepository
from book_keeper.views.dialogs.category_dialog import CategoryDialog
from book_keeper.views.models.category_table import CategoryTableModel


class CategoryView(QWidget):
    def __init__(self, repo: CategoryRepository) -> None:
        super().__init__()
        self.repo = repo

        self.table = QTableView()
        self.model = CategoryTableModel(self.repo.all())
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

    def refresh(self) -> None:
        self.model.refresh(self.repo.all())

    @Slot()
    def add_category(self) -> None:
        dlg = CategoryDialog()
        if dlg.exec():
            name = dlg.get_data()
            self.repo.create(name)
            self.refresh()

    @Slot()
    def edit_category(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return

        account = self.model.categories[index.row()]
        dlg = CategoryDialog()
        if dlg.exec():
            name = dlg.get_data()
            self.repo.update(account, name)
            self.refresh()

    @Slot()
    def delete_category(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return
        account = self.model.categories[index.row()]
        self.repo.delete(account)
        self.refresh()
