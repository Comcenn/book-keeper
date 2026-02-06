from typing import Any
from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt

from book_keeper.models import TransactionHeader


class TransactionTableModel(QAbstractTableModel):
    COL_DATE = 0
    COL_TRAN_TYPE = 1
    COL_DESC = 2
    COL_ACC_NAME = 3
    COL_TOTAL = 4
    COL_TOTAL_TO_BANK = 5
    COL_RECONCILED = 6
    COL_NOTES = 7

    def __init__(self, transactions: list[TransactionHeader]) -> None:
        super().__init__()
        self._transactions = transactions
    
    def rowCount(self, /, parent=None) -> int:
        return len(self._transactions)
    
    def columnCount(self, /, parent=None) -> int:
        return 8
    
    def data(self, index: QModelIndex | QPersistentModelIndex, /, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid():
            return None
        
        transaction = self._transactions[index.row()]

        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            match index.column():
                case self.COL_DATE:
                    return transaction.transaction_on.strftime("%Y-%m-%d")
                case self.COL_TRAN_TYPE:
                    return transaction.transaction_type
                case self.COL_DESC:
                    return transaction.item_description
                case self.COL_ACC_NAME:
                    return transaction.account.name
                case self.COL_TOTAL:
                    return f"{transaction.total / 100:.2f}"
                case self.COL_TOTAL_TO_BANK:
                    return f"{transaction.total_paid_into_bank / 100:.2f}"
                case self.COL_RECONCILED:
                    return transaction.reconciled
                case self.COL_NOTES:
                    return transaction.notes
                case _:
                    raise ValueError("Column number mismatch")
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, /, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if role != Qt.ItemDataRole.DisplayRole or orientation != Qt.Orientation.Horizontal:
            return None
        return ["Date", "Type", "Description", "Account", "Total", "Total Paid Into Bank", "Reconciled", "Notes"][section]

