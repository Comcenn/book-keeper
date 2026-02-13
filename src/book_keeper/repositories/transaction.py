from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import List

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload, with_loader_criteria

from book_keeper.models import TransactionHeader, TransactionLine


class TransactionType(StrEnum):
    RECEIPT = "RECEIPT"
    PAYMENT = "PAYMENT"


class LineDto(BaseModel):
    id: int | None = None
    amount: int = Field(..., ge=0)
    category_id: int


class HeaderDto(BaseModel):
    id: int | None = None
    item_description: str
    transaction_on: date
    transaction_type: TransactionType
    total_paid_into_bank: int = Field(..., ge=0)
    total: int | None
    reconciled: bool = False
    account_id: int
    notes: str = ""
    lines: List[LineDto]


class TransactionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(self) -> list[HeaderDto]:
        headers = (
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
        return [self._to_dto(h) for h in headers]

    def get(self, transaction_id: int) -> HeaderDto | None:
        header = (
            self.session.query(TransactionHeader)
            .options(
                joinedload(TransactionHeader.account),
                joinedload(TransactionHeader.lines),
                with_loader_criteria(TransactionLine, lambda cls: cls.deleted == False),
            )
            .filter(
                TransactionHeader.deleted == False,
                TransactionHeader.id == transaction_id,
            )
            .one_or_none()
        )
        return self._to_dto(header) if header else None

    def create(self, dto: HeaderDto) -> HeaderDto:
        self._validate_lines(dto.lines)

        header = TransactionHeader(
            item_description=dto.item_description,
            transaction_on=dto.transaction_on,
            transaction_type=dto.transaction_type.value,
            total=sum(line.amount for line in dto.lines),
            total_paid_into_bank=dto.total_paid_into_bank,
            reconciled=dto.reconciled,
            notes=dto.notes,
            account_id=dto.account_id,
        )

        for line in dto.lines:
            header.lines.append(
                TransactionLine(
                    amount=line.amount,
                    category_id=line.category_id,
                )
            )

        self.session.add(header)
        self.session.commit()
        self.session.refresh(header)
        return self._to_dto(header)

    def update(self, dto: HeaderDto) -> HeaderDto:
        if dto.id is None:
            raise ValueError("HeaderDto.id is required for update")

        self._validate_lines(dto.lines)

        header = self.session.get(TransactionHeader, dto.id)
        if not header or header.deleted:
            raise ValueError(f"Transaction {dto.id} not found")

        header.item_description = dto.item_description
        header.transaction_on = dto.transaction_on
        header.transaction_type = dto.transaction_type.value
        header.total_paid_into_bank = dto.total_paid_into_bank
        header.reconciled = dto.reconciled
        header.account_id = dto.account_id
        header.notes = dto.notes
        header.total = sum(line.amount for line in dto.lines)

        header.lines.clear()
        for line in dto.lines:
            header.lines.append(
                TransactionLine(
                    amount=line.amount,
                    category_id=line.category_id,
                )
            )

        self.session.commit()
        self.session.refresh(header)
        return self._to_dto(header)

    def delete(self, transaction_id: int) -> None:
        header = self.session.get(TransactionHeader, transaction_id)
        if not header or header.deleted:
            return
        header.deleted = True
        self.session.commit()

    def _validate_lines(self, lines: List[LineDto]) -> None:
        if not lines:
            raise ValueError("Transaction requires at least one line.")
        for line in lines:
            if line.category_id is None:
                raise ValueError("Line is missing category_id.")

    def _to_dto(self, header: TransactionHeader) -> HeaderDto:
        return HeaderDto(
            id=header.id,
            item_description=header.item_description,
            transaction_on=header.transaction_on,
            transaction_type=TransactionType(header.transaction_type),
            total_paid_into_bank=header.total_paid_into_bank,
            total=header.total,
            reconciled=header.reconciled,
            account_id=header.account_id,
            notes=header.notes,
            lines=[
                LineDto(
                    id=line.id,
                    amount=line.amount,
                    category_id=line.category_id,
                )
                for line in header.lines
                if not line.deleted
            ],
        )