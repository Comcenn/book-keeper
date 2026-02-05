from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Signal, QDate

from book_keeper.models import TransactionHeader
from book_keeper.repositories.account import AccountRepository
from book_keeper.repositories.category import CategoryRepository
from book_keeper.repositories.transaction import (
    Header,
    TransactionRepository,
    TransactionType,
)

from .lines_editor.lines_editor import LinesEditor


class TransactionDetailView(QWidget):
    saved = Signal()
    back_requested = Signal()

    def __init__(
        self,
        transaction_repo: TransactionRepository,
        account_repo: AccountRepository,
        category_repo: CategoryRepository,
    ) -> None:
        super().__init__()

        self.tran_repo = transaction_repo
        self.acc_repo = account_repo
        self.cat_repo = category_repo

        # Preload categories into a dict {id: name}
        self.categories = {c.id: c.name for c in self.cat_repo.all()}

        layout = QVBoxLayout(self)

        # Header bar
        header = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("BackButton")
        back_btn.clicked.connect(self.back_requested)
        header.addWidget(back_btn)
        header.addStretch()
        layout.addLayout(header)

        # Form fields
        form = QFormLayout()
        layout.addLayout(form)

        self.desc_edit = QLineEdit()
        form.addRow("Description", self.desc_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Date", self.date_edit)

        self.account_combo = QComboBox()
        for acc in self.acc_repo.all():
            self.account_combo.addItem(acc.name, acc.id)
        form.addRow("Account", self.account_combo)

        self.notes_edit = QLineEdit()
        form.addRow("Notes", self.notes_edit)

        # Lines editor
        self.lines_editor = LinesEditor(self.categories)
        layout.addWidget(self.lines_editor)

        # Buttons
        btns = QHBoxLayout()
        layout.addLayout(btns)

        self.save_btn = QPushButton("Save")
        btns.addStretch()
        btns.addWidget(self.save_btn)

        self.save_btn.clicked.connect(self._save)

        # Track the currently loaded transaction (None = new)
        self._current_header: TransactionHeader | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, header: TransactionHeader) -> None:
        """Load an existing transaction into the view."""
        self._current_header = header

        self.desc_edit.setText(header.item_description)
        self.date_edit.setDate(QDate(header.transaction_on))
        self.notes_edit.setText(header.notes or "")

        # Select account
        idx = self.account_combo.findData(header.account_id)
        if idx >= 0:
            self.account_combo.setCurrentIndex(idx)

        # Load lines into the editor
        self.lines_editor.set_lines(header.lines)

    def clear(self) -> None:
        """Reset the form for a new transaction."""
        self._current_header = None

        self.desc_edit.clear()
        self.notes_edit.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.account_combo.setCurrentIndex(0)
        self.lines_editor.set_lines([])

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------

    def _save(self):
        lines = self.lines_editor.get_lines()

        header = Header(
            item_description=self.desc_edit.text(),
            transaction_on=self.date_edit.date().toPython(),
            transaction_type=TransactionType.PAYMENT,  # TODO: user-selectable
            total_paid_into_bank=0,  # TODO: compute from lines if needed
            reconciled=False,
            account_id=self.account_combo.currentData(),
            notes=self.notes_edit.text(),
            lines=lines,
        )

        if self._current_header is None:
            # New transaction
            self.tran_repo.create(header)
        else:
            # Update existing
            self.tran_repo.update(self._current_header.id, header)

        self.saved.emit()