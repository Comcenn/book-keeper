from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton, QHeaderView
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
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        self.new_btn = QPushButton("New Transaction")
        layout.addWidget(self.new_btn)

        self.new_btn.clicked.connect(self.create_requested.emit)
        self.table.clicked.connect(self._row_clicked)

        self.refresh()

    def refresh(self) -> None:
        headers = self.repo.list()
        self._headers = headers

        model = QStandardItemModel(len(headers), 8)
        model.setHorizontalHeaderLabels(["Date", "Type", "Description", "Account", "Total", "Total Paid Into Bank", "Reconciled", "Notes"])

        for row, h in enumerate(headers):
            model.setItem(row, 0, QStandardItem(h.transaction_on.strftime("%Y-%m-%d")))
            model.setItem(row, 1, QStandardItem(h.transaction_type))
            model.setItem(row, 2, QStandardItem(h.item_description))
            model.setItem(row, 3, QStandardItem(h.account.name))
            model.setItem(row, 4, QStandardItem(str(h.total / 100)))
            model.setItem(row, 5, QStandardItem(str(h.total_paid_into_bank / 100)))
            model.setItem(row, 6, QStandardItem(h.reconciled))
            model.setItem(row, 7, QStandardItem(h.notes))

        self.table.setModel(model)
        self._configure_columns()
        self.table.resizeColumnsToContents()

    def _row_clicked(self, index: QModelIndex) -> None:
        header = self._headers[index.row()]
        self.transaction_selected.emit(header.id)

    def _configure_columns(self) -> None:
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)

        for col in [0, 1, 3, 4, 5, 6]:
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerPixel)