from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QCheckBox,
)
from PySide6.QtCore import QDate

from book_keeper.repositories.transaction import Header, TransactionType
from book_keeper.models import TransactionHeader
from book_keeper.repositories.account import AccountRepository


class HeaderForm(QWidget):
    """
    A self-contained widget that manages the transaction header fields.
    Responsible only for UI + mapping to/from Header dataclass (except lines).
    """

    def __init__(self, account_repo: AccountRepository, parent=None):
        super().__init__(parent)

        self.account_repo = account_repo

        form = QFormLayout(self)

        # Description
        self.desc_edit = QLineEdit()
        form.addRow("Description", self.desc_edit)

        # Date
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Date", self.date_edit)

        # Transaction type
        self.type_combo = QComboBox()
        for t in TransactionType:
            self.type_combo.addItem(t.name.title(), t)
        form.addRow("Type", self.type_combo)

        # Account
        self.account_combo = QComboBox()
        for acc in self.account_repo.all():
            self.account_combo.addItem(acc.name, acc.id)
        form.addRow("Account", self.account_combo)

        # Reconciled
        self.reconciled_check = QCheckBox("Reconciled")
        form.addRow("Status", self.reconciled_check)

        # Total paid into bank (user-editable)
        self.total_edit = QLineEdit()
        self.total_edit.setPlaceholderText("Amount in minor units (e.g. pence)")
        form.addRow("Paid Into Bank", self.total_edit)

        # Notes
        self.notes_edit = QLineEdit()
        form.addRow("Notes", self.notes_edit)

        self._current_header: TransactionHeader | None = None

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def load_header(self, header: TransactionHeader) -> None:
        """Populate the form from an existing TransactionHeader."""
        self._current_header = header

        self.desc_edit.setText(header.item_description)
        self.date_edit.setDate(QDate(header.transaction_on))
        self.notes_edit.setText(header.notes or "")

        # Transaction type
        idx = self.type_combo.findData(header.transaction_type)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)

        # Account
        acc_idx = self.account_combo.findData(header.account_id)
        if acc_idx >= 0:
            self.account_combo.setCurrentIndex(acc_idx)

        # Reconciled
        self.reconciled_check.setChecked(bool(header.reconciled))

        # Total paid into bank (user-editable)
        self.total_edit.setText(str(header.total_paid_into_bank))

    def clear(self) -> None:
        """Reset the form for a new transaction."""
        self._current_header = None

        self.desc_edit.clear()
        self.notes_edit.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.account_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.reconciled_check.setChecked(False)
        self.total_edit.clear()

    def to_header(self, lines):
        """
        Convert the form fields into a Header dataclass.
        The caller provides the line items.
        """
        try:
            total_paid = int(self.total_edit.text() or 0)
        except ValueError:
            total_paid = 0  # You may want validation later

        return Header(
            item_description=self.desc_edit.text(),
            transaction_on=self.date_edit.date().toPython(),
            transaction_type=self.type_combo.currentData(),
            total_paid_into_bank=total_paid,
            reconciled=self.reconciled_check.isChecked(),
            account_id=self.account_combo.currentData(),
            notes=self.notes_edit.text(),
            lines=lines,
        )