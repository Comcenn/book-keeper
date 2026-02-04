from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton
from PySide6.QtCore import Signal, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem

from book_keeper.repositories.transaction import TransactionRepository


class TransactionListView(QWidget):
    create_requested = Signal()
    transaction_selected = Signal(int)  # emits header.id

    def __init__(self, repo: TransactionRepository) -> None:
        super().__init__()
        self.repo = repo

        layout = QVBoxLayout(self)

        self.table = QTableView()
        layout.addWidget(self.table)

        self.new_btn = QPushButton("New Transaction")
        layout.addWidget(self.new_btn)

        self.new_btn.clicked.connect(self.create_requested.emit)
        self.table.clicked.connect(self._row_clicked)

        self.refresh()

    def refresh(self) -> None:
        headers = self.repo.list()
        self._headers = headers

        model = QStandardItemModel(len(headers), 4)
        model.setHorizontalHeaderLabels(["Date", "Description", "Account", "Total"])

        for row, h in enumerate(headers):
            model.setItem(row, 0, QStandardItem(h.transaction_on.strftime("%Y-%m-%d")))
            model.setItem(row, 1, QStandardItem(h.item_description))
            model.setItem(row, 2, QStandardItem(h.account.name))
            model.setItem(row, 3, QStandardItem(str(h.total / 100)))

        self.table.setModel(model)
        self.table.resizeColumnsToContents()

    def _row_clicked(self, index: QModelIndex) -> None:
        header = self._headers[index.row()]
        self.transaction_selected.emit(header.id)
