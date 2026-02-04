from typing import Any
from PySide6 import QtCore

from book_keeper.models import Category


class CategoryTableModel(QtCore.QAbstractTableModel):
    def __init__(self, accounts: list[Category]) -> None:
        super().__init__()
        self._categories = accounts

    @property
    def categories(self) -> list[Category]:
        return self._categories

    def rowCount(self, parent=None) -> int:
        return len(self._categories)

    def columnCount(self, parent=None) -> int:
        return 1

    def data(
        self,
        index: QtCore.QModelIndex | QtCore.QPersistentModelIndex,
        role: int = QtCore.Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if not index.isValid():
            return None

        account = self._categories[index.row()]

        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return account.name

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
            return ["Name"][section]

    def refresh(self, categories: list[Category]) -> None:
        self.beginResetModel()
        self._categories = categories
        self.endResetModel()
