from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QPushButton, QHeaderView
from PySide6.QtCore import Signal, QModelIndex
from PySide6.QtGui import QStandardItemModel, QStandardItem

from book_keeper.repositories.transaction import TransactionRepository
from book_keeper.views.models.transaction_table import TransactionTableModel


class TransactionListView(QWidget):
    create_requested = Signal()
    transaction_selected = Signal(int)  # emits header.id

    def __init__(self, transaction_model: TransactionTableModel) -> None:
        super().__init__()
        self.model = transaction_model

        layout = QVBoxLayout(self)

        self.table = QTableView()
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.model)
        layout.addWidget(self.table)

        self.new_btn = QPushButton("New Transaction")
        layout.addWidget(self.new_btn)

        self.new_btn.clicked.connect(self.create_requested.emit)
        self.table.clicked.connect(self._row_clicked)

        self._configure_columns()
        self.table.resizeColumnsToContents()

    def _row_clicked(self, index: QModelIndex) -> None:
        header = self.model.transaction_at(index.row())
        self.transaction_selected.emit(header.id)

    def _configure_columns(self) -> None:
        header = self.table.horizontalHeader()

        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)

        for col in [0, 1, 3, 4, 5, 6]:
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.table.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
