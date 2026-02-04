from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDateEdit,
    QComboBox,
    QTableView,
    QHBoxLayout,
    QPushButton,
)
from PySide6.QtCore import Signal, QDate
from PySide6.QtGui import QStandardItemModel, QStandardItem

from book_keeper.models import TransactionHeader
from book_keeper.repositories.account import AccountRepository
from book_keeper.repositories.category import CategoryRepository
from book_keeper.repositories.transaction import (
    Header,
    Line,
    TransactionRepository,
    TransactionType,
)


class TransactionDetailView(QWidget):
    saved = Signal()

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
        form.addRow(self.account_combo)

        self.notes_edit = QLineEdit()
        form.addRow(self.notes_edit)

        self.lines: list[Line] = []
        self.lines_table = QTableView()
        layout.addWidget(self.lines_table)

        btns = QHBoxLayout()
        layout.addLayout(btns)

        self.add_line_btn = QPushButton("Add Line")
        self.save_btn = QPushButton("Save")

        btns.addWidget(self.add_line_btn)
        btns.addWidget(self.save_btn)

        self.add_line_btn.clicked.connect(self._add_line)
        self.save_btn.clicked.connect(self._save)

        self._refresh_lines()

    def _add_line(self) -> None:
        # For now: add a dummy line (you’ll replace this with a proper editor)
        self.lines.append(Line(amount=0, category_id=self.cat_repo.all()[0].id))
        self._refresh_lines()

    def _refresh_lines(self):
        model = QStandardItemModel(len(self.lines), 2)
        model.setHorizontalHeaderLabels(["Category", "Amount"])

        for row, line in enumerate(self.lines):
            cat = self.cat_repo.get(line.category_id)
            if not cat is None:
                model.setItem(row, 0, QStandardItem(cat.name))
                model.setItem(row, 1, QStandardItem(str(line.amount)))

        self.lines_table.setModel(model)
        self.lines_table.resizeColumnsToContents()

    def _save(self):
        header = Header(
            item_description=self.desc_edit.text(),
            transaction_on=self.date_edit.date().toPython(),
            transaction_type=TransactionType.PAYMENT,  # temporary
            total_paid_into_bank=0,
            reconciled=False,
            account_id=self.account_combo.currentData(),
            notes=self.notes_edit.text(),
            lines=self.lines,
        )

        self.tran_repo.create(header)
        self.saved.emit()
    
    def load(self, header: TransactionHeader) -> None:
        pass

    def clear(self) -> None:
        pass
