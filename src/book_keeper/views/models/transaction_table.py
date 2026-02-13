from typing import Any
from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from book_keeper.repositories.transaction import HeaderDto, TransactionRepository
from book_keeper.views.models.account_table import AccountTableModel


class TransactionTableModel(QAbstractTableModel):
    COL_DATE = 0
    COL_TRAN_TYPE = 1
    COL_DESC = 2
    COL_ACC_NAME = 3
    COL_TOTAL = 4
    COL_TOTAL_TO_BANK = 5
    COL_RECONCILED = 6
    COL_NOTES = 7

    HEADERS = [
        "Date",
        "Type",
        "Description",
        "Account",
        "Total",
        "Total Paid Into Bank",
        "Reconciled",
        "Notes",
    ]

    def __init__(self, transaction_repository: TransactionRepository, account_model: AccountTableModel) -> None:
        super().__init__()
        self._repo = transaction_repository
        self._acc_model = account_model
        self._transactions: list[HeaderDto] = self._repo.list()

    # ------------------------------------------------------------
    # Qt model basics
    # ------------------------------------------------------------
    def rowCount(self, parent=None) -> int:
        return len(self._transactions)

    def columnCount(self, parent=None) -> int:
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None

        transaction = self._transactions[index.row()]

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            col = index.column()
            if col == self.COL_DATE:
                return transaction.transaction_on.strftime("%Y-%m-%d")
            if col == self.COL_TRAN_TYPE:
                return transaction.transaction_type
            if col == self.COL_DESC:
                return transaction.item_description
            if col == self.COL_ACC_NAME:
                return self._acc_model.name_from_id(transaction.account_id) or ""
            if col == self.COL_TOTAL:
                return f"{transaction.total / 100:.2f}" if transaction.total else "0.00"
            if col == self.COL_TOTAL_TO_BANK:
                return f"{transaction.total_paid_into_bank / 100:.2f}"
            if col == self.COL_RECONCILED:
                return transaction.reconciled
            if col == self.COL_NOTES:
                return transaction.notes

        return None

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    def transaction_at(self, row: int) -> HeaderDto:
        return self._transactions[row]

    # ------------------------------------------------------------
    # CRUD operations
    # ------------------------------------------------------------
    def add_transaction(self, dto: HeaderDto) -> None:
        """Create a new transaction and insert it into the model."""
        created = self._repo.create(dto)

        insert_row = len(self._transactions)
        self.beginInsertRows(QModelIndex(), insert_row, insert_row)
        self._transactions.append(created)
        self.endInsertRows()

    def update_transaction(self, row: int, dto: HeaderDto) -> None:
        """Update an existing transaction and refresh the row."""
        updated = self._repo.update(dto)

        self._transactions[row] = updated
        top_left = self.index(row, 0)
        bottom_right = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])

    def delete_transaction(self, row: int) -> None:
        """Soft-delete a transaction and remove it from the model."""
        dto = self._transactions[row]
        self._repo.delete(dto.id)

        self.beginRemoveRows(QModelIndex(), row, row)
        del self._transactions[row]
        self.endRemoveRows()
    
    def row_from_id(self, transaction_id: int) -> int | None:
        for idx, dto in enumerate(self._transactions):
            if transaction_id == dto.id:
                return idx
        return None
        

    # ------------------------------------------------------------
    # Convenience refresh
    # ------------------------------------------------------------
    def reload(self) -> None:
        """Reload all transactions from the repository."""
        self.beginResetModel()
        self._transactions = self._repo.list()
        self.endResetModel()