from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

from book_keeper.models import Account


class AccountDialog(QDialog):
    def __init__(self, account: Account | None = None):
        super().__init__()
        self.setWindowTitle("Account")

        self.name_label = QLabel("Name")
        self.number_label = QLabel("Number")
        self.name_edit = QLineEdit()
        self.number_edit = QLineEdit()

        if account:
            self.name_edit.setText(account.name)
            self.number_edit.setText(account.number)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.number_label)
        layout.addWidget(self.number_edit)
        layout.addWidget(save_btn)
        self.setLayout(layout)

    def get_data(self) -> tuple[str, str]:
        return self.name_edit.text(), self.number_edit.text()
