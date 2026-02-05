from typing import cast
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox, QWidget, QStyleOptionViewItem
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt

from book_keeper.views.models.line_table import LineModel


class CategoryDelegate(QStyledItemDelegate):
    def __init__(self, categories: dict[int, str], parent=None) -> None:
        super().__init__(parent)
        self._categories = categories
    
    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> QComboBox:
        combo = QComboBox(parent)
        for cat_id, name in self._categories.items():
            combo.addItem(name, cat_id)
        return combo
    
    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        # The model returns the *display name*, but we need the raw ID
        # So we ask the model directly for the underlying Line object
        model: LineModel  = cast(LineModel, index.model())
        line = model.get_line(index.row())  # safe: internal use only

        # Find the combobox index with matching category_id
        cat_id = line.category_id
        combo_editor: QComboBox = cast(QComboBox, editor)
        combo_index = combo_editor.findData(cat_id)
        if combo_index >= 0:
            combo_editor.setCurrentIndex(combo_index)
    
    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex) -> None:
        combo_editor: QComboBox = cast(QComboBox, editor)
        cat_id = combo_editor.currentData()
        model.setData(index, cat_id, Qt.ItemDataRole.EditRole)
    
    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex) -> None:
        editor.setGeometry(option.rect)