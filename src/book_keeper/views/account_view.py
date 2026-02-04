from PySide6.QtWidgets import QTableView, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot

from book_keeper.repositories.account import AccountRepository
from book_keeper.views.dialogs.account_dialog import AccountDialog
from book_keeper.views.models.account_table import AccountTableModel


class AccountView(QWidget):
    def __init__(self, repo: AccountRepository) -> None:
        super().__init__()
        self.repo = repo

        self.table = QTableView()
        self.model = AccountTableModel(self.repo.all())
        self.table.setModel(self.model)

        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")

        add_btn.clicked.connect(self.add_account)
        edit_btn.clicked.connect(self.edit_account)
        delete_btn.clicked.connect(self.delete_account)

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
    def add_account(self) -> None:
        dlg = AccountDialog()
        if dlg.exec():
            name, number = dlg.get_data()
            self.repo.create(name, number)
            self.refresh()

    @Slot()
    def edit_account(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return

        account = self.model.accounts[index.row()]
        dlg = AccountDialog()
        if dlg.exec():
            name, number = dlg.get_data()
            self.repo.update(account, name, number)
            self.refresh()

    @Slot()
    def delete_account(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return
        account = self.model.accounts[index.row()]
        self.repo.delete(account)
        self.refresh()
