from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from book_keeper.repositories.account import AccountRepository, AccountDto


AccountRole = Qt.ItemDataRole.UserRole + 1


class AccountTableModel(QAbstractTableModel):
    def __init__(self, account_repo: AccountRepository) -> None:
        super().__init__()
        self.acc_repo = account_repo
        self._accounts = account_repo.all()

    def rowCount(self, parent=None) -> int:
        return len(self._accounts)

    def columnCount(self, parent=None) -> int:
        return 2

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None

        account = self._accounts[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return account.name
            if index.column() == 1:
                return account.number

        if role == AccountRole:
            return account

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return ["Name", "Number"][section]
    
    def name_from_id(self, account_id: int) -> str | None:
        for acc in self._accounts:
            if acc.id == account_id:
                return acc.name
        return None

    def add_account(self, name: str, number: str) -> None:
        dto = AccountDto(name=name, number=number)
        created = self.acc_repo.create(dto)

        row = len(self._accounts)
        self.beginInsertRows(QModelIndex(), row, row)
        self._accounts.append(created)
        self.endInsertRows()

    def account_at(self, row: int) -> AccountDto:
        return self._accounts[row]

    def update_account(self, row: int, updated: AccountDto) -> None:
        saved_dto = self.acc_repo.update(updated)
        self._accounts[row] = saved_dto
        top_left = self.index(row, 0)
        bottom_right = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right)

    def delete_account(self, row: int) -> None:
        dto = self._accounts[row]
        self.acc_repo.delete(dto)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._accounts[row]
        self.endRemoveRows()

    def reload(self) -> None:
        self.beginResetModel()
        self._accounts = self.acc_repo.all()
        self.endResetModel()
