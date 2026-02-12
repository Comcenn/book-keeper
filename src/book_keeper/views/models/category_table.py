from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from book_keeper.repositories.category import CategoryDto, CategoryRepository


CategoryRole = Qt.ItemDataRole.UserRole + 2


class CategoryTableModel(QAbstractTableModel):
    def __init__(self, category_repo: CategoryRepository) -> None:
        super().__init__()
        self._repo = category_repo
        self._categories = self._repo.all()

    def rowCount(self, parent=None) -> int:
        return len(self._categories)

    def columnCount(self, parent=None) -> int:
        return 1

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None

        category = self._categories[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() == 0:
                return category.name
        
        if role == CategoryRole:
            return category.id

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
            return ["Name"][section]
    
    def name_from_id(self, cat_id: int) -> str | None:
        for dto in self._categories:
            if dto.id == cat_id:
                return dto.name
        return None
    
    def add_category(self, name: str) -> None:
        dto = CategoryDto(name=name)
        created = self._repo.create(dto)

        row = len(self._categories)
        self.beginInsertRows(QModelIndex(), row, row)
        self._categories.append(created)
        self.endInsertRows()
    
    def category_at(self, row: int) -> CategoryDto:
        return self._categories[row]
    
    def update_category(self, row, updated: CategoryDto) -> None:
        saved_dto = self._repo.update(updated)
        self._categories[row] = saved_dto
        top_left = self.index(row, 0)
        bottom_right = self.index(row, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right)
    
    def delete_category(self, row: int) -> None:
        dto = self._categories[row]
        self._repo.delete(dto)
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._categories[row]
        self.endRemoveRows()

    def reload(self) -> None:
        self.beginResetModel()
        self._categories = self._repo.all()
        self.endResetModel()
