import datetime
from typing import List
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class SoftDeleteMixin:
    deleted: Mapped[bool] = mapped_column(default=False)


class Category(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "categories"
    name: Mapped[str]


class Account(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "accounts"
    name: Mapped[str]
    number: Mapped[str]


class TransactionHeader(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "transaction_headers"
    item_description: Mapped[str]
    transaction_on: Mapped[datetime.date]
    transaction_type: Mapped[str]
    total: Mapped[int]
    total_paid_into_bank: Mapped[int]
    reconciled: Mapped[bool]
    notes: Mapped[str]
    account_id = mapped_column(ForeignKey("accounts.id"))

    account: Mapped[Account] = relationship()
    lines: Mapped[List["TransactionLine"]] = relationship(
        back_populates="transaction_header"
    )


class TransactionLine(IdMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "transaction_lines"
    amount: Mapped[int]
    category_id = mapped_column(ForeignKey("categories.id"))
    transaction_header_id = mapped_column(ForeignKey("transaction_headers.id"))

    category: Mapped[Category] = relationship()
    transaction_header: Mapped[TransactionHeader] = relationship(back_populates="lines")
