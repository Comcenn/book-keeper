from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Signal

from book_keeper.models import TransactionHeader
from book_keeper.repositories.account import AccountRepository
from book_keeper.repositories.category import CategoryRepository
from book_keeper.repositories.transaction import TransactionRepository

from .header_form import HeaderForm
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
        # Header form (new modular component)
        # --------------------------------------------------------------
        self.header_form = HeaderForm(self.acc_repo)
        layout.addWidget(self.header_form)

        # --------------------------------------------------------------
        # Lines editor
        # --------------------------------------------------------------
        categories = {c.id: c.name for c in self.cat_repo.all()}
        self.lines_editor = LinesEditor(categories)
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

        # Track currently loaded transaction
        self._current_header: TransactionHeader | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, header: TransactionHeader) -> None:
        """
        Load an existing transaction into the view.
        """
        self._current_header = header

        # Populate header form
        self.header_form.load_header(header)

        # Populate lines
        self.lines_editor.set_lines(header.lines)

    def clear(self) -> None:
        """
        Reset the form for a new transaction.
        """
        self._current_header = None

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

        # Build Header dataclass from form fields
        header = self.header_form.to_header(lines)

        if self._current_header is None:
            # New transaction
            self.tran_repo.create(header)
        else:
            # Update existing
            self.tran_repo.update(self._current_header.id, header)

        self.saved.emit()