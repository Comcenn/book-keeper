from typing import Any
from PySide6 import QtCore

from book_keeper.models import Account


class AccountTableModel(QtCore.QAbstractTableModel):
    def __init__(self, accounts: list[Account]) -> None:
        super().__init__()
        self._accounts = accounts

    @property
    def accounts(self) -> list[Account]:
        return self._accounts

    def rowCount(self, parent=None) -> int:
        return len(self._accounts)

    def columnCount(self, parent=None) -> int:
        return 2

    def data(
        self,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        account = self._accounts[index.row()]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return account.name
            if index.column() == 1:
                return account.number

    def headerData(
        self,
        section: int,
        orientation: QtCore.Qt.Orientation,
        /,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            role == QtCore.Qt.ItemDataRole.DisplayRole
            and orientation == QtCore.Qt.Orientation.Horizontal
        ):
            return ["Name", "Number"][section]

    def refresh(self, accounts: list[Account]) -> None:
        self.beginResetModel()
        self._accounts = accounts
        self.endResetModel()
