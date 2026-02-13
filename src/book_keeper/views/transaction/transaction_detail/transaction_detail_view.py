from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Signal

from book_keeper.repositories.transaction import HeaderDto
from book_keeper.views.models.account_table import AccountTableModel
from book_keeper.views.models.category_table import CategoryTableModel
from book_keeper.views.models.transaction_table import TransactionTableModel

from .header_form import HeaderForm
from .lines_editor.lines_editor import LinesEditor


class TransactionDetailView(QWidget):
    saved = Signal()
    back_requested = Signal()

    def __init__(
        self,
        transaction_model: TransactionTableModel,
        account_model: AccountTableModel,
        category_model: CategoryTableModel,
    ) -> None:
        super().__init__()

        self.tran_model = transaction_model
        self.acc_model = account_model
        self.cat_model = category_model

        layout = QVBoxLayout(self)

        # --------------------------------------------------------------
        # Header bar
        # --------------------------------------------------------------
        header = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("BackButton")
        back_btn.clicked.connect(self.back_requested)
        header.addWidget(back_btn)
        header.addStretch()
        layout.addLayout(header)

        # --------------------------------------------------------------
        # Header form
        # --------------------------------------------------------------
        self.header_form = HeaderForm(self.acc_model)
        layout.addWidget(self.header_form)

        # --------------------------------------------------------------
        # Lines editor
        # --------------------------------------------------------------
        self.lines_editor = LinesEditor(category_model)
        layout.addWidget(self.lines_editor)

        # --------------------------------------------------------------
        # Buttons
        # --------------------------------------------------------------
        btns = QHBoxLayout()
        layout.addLayout(btns)

        self.save_btn = QPushButton("Save")
        btns.addStretch()
        btns.addWidget(self.save_btn)

        self.save_btn.clicked.connect(self._save)

        # Track currently loaded transaction row
        self._current_row: int | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, row: int) -> None:
        """
        Load an existing transaction from the table model.
        """
        self._current_row = row
        dto: HeaderDto = self.tran_model.transaction_at(row)

        self.header_form.load_header(dto)
        self.lines_editor.set_lines(dto.lines)

    def clear(self) -> None:
        """
        Reset the form for a new transaction.
        """
        self._current_row = None
        self.header_form.clear()
        self.lines_editor.set_lines([])

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------

    def _save(self):
        """
        Collect data from the form + lines editor and persist it.
        """
        lines = self.lines_editor.get_lines()
        dto = self.header_form.to_header(lines)

        if self._current_row is None:
            # New transaction
            self.tran_model.add_transaction(dto)
        else:
            # Update existing
            self.tran_model.update_transaction(self._current_row, dto)

        self.saved.emit()