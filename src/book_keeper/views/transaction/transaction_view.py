from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget

from book_keeper.repositories.account import AccountRepository
from book_keeper.repositories.category import CategoryRepository
from book_keeper.repositories.transaction import TransactionRepository
from book_keeper.views.transaction.transaction_detail.transaction_detail_view import TransactionDetailView
from book_keeper.views.transaction.transaction_list_view import TransactionListView


class TransactionView(QWidget):
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        account_repo: AccountRepository,
        category_repo: CategoryRepository,
    ) -> None:
        super().__init__()

        layout = QHBoxLayout(self)

        self.list_view = TransactionListView(transaction_repo)
        self.detail_view = TransactionDetailView(
            transaction_repo, account_repo, category_repo
        )

        self.stack = QStackedWidget()
        self.stack.addWidget(self.list_view)
        self.stack.addWidget(self.detail_view)
        layout.addWidget(self.stack)

        self.stack.setCurrentWidget(self.list_view)

        self.list_view.create_requested.connect(self._show_create)
        self.list_view.transaction_selected.connect(self._show_existing)
        self.detail_view.saved.connect(self._back_to_list)
        self.detail_view.back_requested.connect(self._back_to_list)

    def _show_create(self):
        self.detail_view.clear()
        self.stack.setCurrentWidget(self.detail_view)

    def _show_existing(self, transaction_id: int):
        header = self.list_view.repo.get(transaction_id)
        if header:
            self.detail_view.load(header)
            self.stack.setCurrentWidget(self.detail_view)

    def _back_to_list(self):
        self.list_view.refresh()
        self.stack.setCurrentWidget(self.list_view)