from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from book_keeper.repositories.transaction import Line

class LineModel(QAbstractTableModel):
    COL_CATEGORY = 0
    COL_AMOUNT = 1

    def __init__(self, categories: dict[int, str], lines: list[Line] | None = None) -> None:
        super().__init__()
        self._categories = categories # {id: name}

        self._lines: list[Line] = lines or []
    
    def rowCount(self, parent=None) -> int:
        return len(self._lines)
    
    def columnCount(self, /, parent=None) -> int:
        return 2
    
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        line = self._lines[index.row()]

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if index.column() == self.COL_CATEGORY:
                return self._categories.get(line.category_id, "")
            if index.column() == self.COL_AMOUNT:
                return f"{line.amount / 100:.2f}"

        
        return None
        
    def headerData(self, section: int, orientation: Qt.Orientation, /, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return None
        return ["Category", "Amount"][section]
    
    def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEnabled
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
    
    def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, /, role: int = Qt.ItemDataRole.DisplayRole) -> bool:
        if not index.isValid() or role != Qt.ItemDataRole.EditRole:
            return False
        
        line = self._lines[index.row()]

        if (col_idx := index.column()) == self.COL_CATEGORY:
            # delegate will pass category_id
            line.category_id = int(value)
        elif col_idx == self.COL_AMOUNT:
            try:
                line.amount = int(value)
            except ValueError:
                return False
        
        self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
        return True
    
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
        if 0<= row < len(self._lines):
            self._lines[row] = new_line
            top_left = self.index(row, 0)
            bottom_right = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])