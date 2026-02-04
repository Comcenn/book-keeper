from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import List
from sqlalchemy.orm import Session, joinedload, with_loader_criteria

from book_keeper.models import TransactionHeader, TransactionLine


class TransactionType(StrEnum):
    RECEIPT = "RECEIPT"
    PAYMENT = "PAYMENT"


@dataclass
class Line:
    amount: int
    category_id: int


@dataclass
class Header:
    item_description: str
    transaction_on: date
    transaction_type: TransactionType
    total_paid_into_bank: int
    reconciled: bool
    account_id: int
    notes: str
    lines: list[Line]


class TransactionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[TransactionHeader]:
        return (
            self.session.query(TransactionHeader)
            .options(
                joinedload(TransactionHeader.account),
                joinedload(TransactionHeader.lines),
                with_loader_criteria(TransactionLine, lambda cls: cls.deleted == False),
            )
            .filter(TransactionHeader.deleted == False)
            .order_by(TransactionHeader.transaction_on.desc())
            .all()
        )
    
    def get(self, transaction_id: int) -> TransactionHeader | None:
        return (self.session.query(TransactionHeader)
            .options(
                joinedload(TransactionHeader.account),
                joinedload(TransactionHeader.lines),
                with_loader_criteria(TransactionLine, lambda cls: cls.deleted == False),
            )
            .filter(TransactionHeader.deleted == False, TransactionHeader.id == transaction_id)
            .order_by(TransactionHeader.transaction_on.desc()).one_or_none()
        )

    def create(self, transaction_obj: Header) -> TransactionHeader:
        lines = transaction_obj.lines
        self._validate_lines_payload(lines)

        header = TransactionHeader(
            item_description=transaction_obj.item_description,
            transaction_on=transaction_obj.transaction_on,
            transaction_type=str(transaction_obj.transaction_type),
            total=sum(line.amount for line in transaction_obj.lines),
            total_paid_into_bank=transaction_obj.total_paid_into_bank,
            reconciled=transaction_obj.reconciled,
            notes=transaction_obj.notes,
            account_id=transaction_obj.account_id,
        )

        for line in lines:
            header.lines.append(
                TransactionLine(amount=line.amount, category_id=line.category_id)
            )

        self.session.add(header)
        self.session.commit()
        return header

    def _validate_lines_payload(self, lines: List[Line]) -> None:
        if not lines:
            raise ValueError("Invalid Transaction requires at least one line.")
        for line in lines:
            if line.amount < 0:
                raise ValueError("Amount cannot be negative.")
            if line.category_id is None:
                raise ValueError("Line is missing Category.")
