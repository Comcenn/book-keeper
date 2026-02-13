from typing import cast, Optional

from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QCheckBox,
)
from PySide6.QtCore import QDate

from book_keeper.repositories.account import AccountDto
from book_keeper.repositories.transaction import HeaderDto, TransactionType
from book_keeper.views.models.account_table import AccountRole, AccountTableModel


class HeaderForm(QWidget):
    """
    A self-contained widget that manages the transaction header fields.
    Responsible only for UI + mapping to/from HeaderDto (except lines).
    """

    def __init__(self, account_model: AccountTableModel, parent=None):
        super().__init__(parent)

        self.acc_model = account_model
        self._current_id: Optional[int] = None  # preserve ID for updates

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
        self.account_combo.setModel(self.acc_model)
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

    # --------------------------------------------------------------
    # Public API
    # --------------------------------------------------------------

    def load_header(self, dto: HeaderDto) -> None:
        """Populate the form from an existing HeaderDto."""
        self._current_id = dto.id

        self.desc_edit.setText(dto.item_description)
        self.date_edit.setDate(QDate(dto.transaction_on))
        self.notes_edit.setText(dto.notes or "")

        # Transaction type
        idx = self.type_combo.findData(dto.transaction_type)
        if idx >= 0:
            self.type_combo.setCurrentIndex(idx)

        # Account
        acc_idx = self.account_combo.findData(dto.account_id, role=AccountRole)
        if acc_idx >= 0:
            self.account_combo.setCurrentIndex(acc_idx)

        # Reconciled
        self.reconciled_check.setChecked(dto.reconciled)

        # Total paid into bank
        self.total_edit.setText(str(dto.total_paid_into_bank))

    def clear(self) -> None:
        """Reset the form for a new transaction."""
        self._current_id = None

        self.desc_edit.clear()
        self.notes_edit.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.account_combo.setCurrentIndex(0)
        self.type_combo.setCurrentIndex(0)
        self.reconciled_check.setChecked(False)
        self.total_edit.clear()

    def to_header(self, lines):
        """
        Convert the form fields into a HeaderDto.
        The caller provides the line DTOs.
        """
        try:
            total_paid = int(self.total_edit.text() or 0)
        except ValueError:
            total_paid = 0  # TODO: validation hook

        account_dto: AccountDto = cast(
            AccountDto, self.account_combo.currentData(AccountRole)
        )
        account_id = account_dto.id

        return HeaderDto(
            id=self._current_id,
            item_description=self.desc_edit.text(),
            transaction_on=self.date_edit.date().toPython(),
            transaction_type=self.type_combo.currentData(),
            total_paid_into_bank=total_paid,
            reconciled=self.reconciled_check.isChecked(),
            account_id=account_id,
            notes=self.notes_edit.text(),
            total=None,  # repository will compute this
            lines=lines,
        )