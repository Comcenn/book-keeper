from collections.abc import Callable
from importlib import resources
import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QStackedWidget,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)

from book_keeper.bootstrap import bootstrap
from book_keeper.db import sessionLocal
from book_keeper.repositories.account import AccountRepository
from book_keeper.repositories.category import CategoryRepository
from book_keeper.repositories.transaction import TransactionRepository
from book_keeper.views.account_view import AccountView
from book_keeper.views.category_view import CategoryView
from book_keeper.views.transaction.transaction_view import TransactionView


def load_stylesheet() -> str:
    return resources.files("book_keeper.resources").joinpath("style.qss").read_text()


bootstrap()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("BookKeeper")

        session = sessionLocal()
        tran_repo = TransactionRepository(session)
        acc_repo = AccountRepository(session)
        cat_repo = CategoryRepository(session)

        main_container = QWidget()
        layout = QHBoxLayout(main_container)

        self.sidebar = QVBoxLayout()
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setSpacing(10)

        layout.addLayout(self.sidebar)

        self.view_stack = QStackedWidget()
        layout.addWidget(self.view_stack, stretch=1)
        transactions_view = TransactionView(tran_repo, acc_repo, cat_repo)
        accounts_view = AccountView(acc_repo)
        category_view = CategoryView(cat_repo)
        self.view_stack.addWidget(transactions_view)
        self.view_stack.addWidget(accounts_view)
        self.view_stack.addWidget(category_view)

        self.add_sidebar_button(
            "Transactions", lambda: self.view_stack.setCurrentWidget(transactions_view)
        )

        self.add_sidebar_button(
            "Accounts", lambda: self.view_stack.setCurrentWidget(accounts_view)
        )
        self.add_sidebar_button(
            "Categories", lambda: self.view_stack.setCurrentWidget(category_view)
        )

        self.setCentralWidget(main_container)

    def add_sidebar_button(self, text: str, callback: Callable) -> None:
        btn = QPushButton(text)
        btn.setFixedWidth(150)
        btn.setObjectName("SidebarButton")
        btn.setCheckable(True)
        btn.clicked.connect(callback)
        self.sidebar.addWidget(btn)


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())

    window = MainWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
