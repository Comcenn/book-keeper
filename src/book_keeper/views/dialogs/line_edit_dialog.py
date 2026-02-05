from decimal import Decimal, InvalidOperation
from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox
from PySide6.QtCore import Qt

from book_keeper.repositories.transaction import Line


class LineEditDialog(QDialog):
    def __init__(self, categories: dict[int, str], line: Line | None = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Edit Line")

        self._categories = categories
        self._line = line

        layout = QVBoxLayout(self)
        form = QFormLayout()
        layout.addLayout(form)

        self.category_combo = QComboBox()
        for cat_id, name in categories.items():
            self.category_combo.addItem(name, cat_id)
        form.addRow("Category", self.category_combo)

        self.amount_edit = QLineEdit()
        form.addRow("Amount", self.amount_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            orientation=Qt.Orientation.Horizontal,
            parent=self
        )
        layout.addWidget(buttons)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        if line is not None:
            self._load_line(line)
    
    def _load_line(self, line: Line) -> None:
        idx = self.category_combo.findData(line.category_id)
        if idx >= 0:
            self.category_combo.setCurrentIndex(idx)
        self.amount_edit.setText(f"{line.amount / 100:.2f}")
    
    def get_line(self) -> Line | None:
        category_id = self.category_combo.currentData()
        amount_text = self.amount_edit.text().strip()
        try:
            dec = Decimal(amount_text)
            amount_int = int(dec * 100)
        except (InvalidOperation, ValueError):
            return None
        return Line(amount=amount_int, category_id=category_id)
