from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from book_keeper.repositories.transaction import Line
from book_keeper.views.models.category_table import CategoryTableModel


class LineModel(QAbstractTableModel):
    COL_CATEGORY = 0
    COL_AMOUNT = 1

    def __init__(self, category_model: CategoryTableModel, lines: list[Line] | None = None) -> None:
        super().__init__()
        self._cat_model = category_model
        self._lines = list(lines) if lines else []

    def rowCount(self, parent=None) -> int:
        return len(self._lines)

    def columnCount(self, parent=None) -> int:
        return 2

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        line = self._lines[index.row()]

        if index.column() == self.COL_CATEGORY:
            return self._cat_model.name_from_id(line.category_id) or ""

        if index.column() == self.COL_AMOUNT:
            return f"{line.amount / 100:.2f}"

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ["Category", "Amount"][section]
        return None

    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled

    def add_line(self, category_id: int, amount: int = 0) -> None:
        row = len(self._lines)
        self.beginInsertRows(QModelIndex(), row, row)
        self._lines.append(Line(amount=amount, category_id=category_id))
        self.endInsertRows()

    def remove_line(self, row: int) -> None:
        if 0 <= row < len(self._lines):
            self.beginRemoveRows(QModelIndex(), row, row)
            del self._lines[row]
            self.endRemoveRows()

    def get_lines(self) -> list[Line]:
        return list(self._lines)

    def get_line(self, row: int) -> Line:
        return self._lines[row]

    def set_lines(self, lines: list[Line]) -> None:
        self.beginResetModel()
        self._lines = list(lines)
        self.endResetModel()

    def update_line(self, row: int, new_line: Line) -> None:
        if 0 <= row < len(self._lines):
            self._lines[row] = new_line
            top_left = self.index(row, 0)
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole])