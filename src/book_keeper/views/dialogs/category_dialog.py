from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel

from book_keeper.models import Category


class CategoryDialog(QDialog):
    def __init__(self, category: Category | None = None):
        super().__init__()
        self.setWindowTitle("Category")

        self.name_label = QLabel("Name")
        self.name_edit = QLineEdit()

        if category:
            self.name_edit.setText(category.name)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(save_btn)
        self.setLayout(layout)

    def get_data(self) -> str:
        return self.name_edit.text()
