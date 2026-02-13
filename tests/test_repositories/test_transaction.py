from datetime import date
from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.repositories.account import AccountRepository, AccountDto
from book_keeper.repositories.category import CategoryDto, CategoryRepository
from book_keeper.repositories.transaction import (
    TransactionRepository,
    HeaderDto,
    LineDto,
    TransactionType,
)


@fixture
def create_dependencies(db_session: Session) -> dict[str, int]:
    cat_repo = CategoryRepository(db_session)
    acc_repo = AccountRepository(db_session)

    cat = cat_repo.create(CategoryDto(name="GiftAid"))
    acc = acc_repo.create(AccountDto(name="CURRENT", number="01675667"))

    assert acc.id
    assert cat.id

    return {"cat_id": cat.id, "acc_id": acc.id}


def test_repository_creates_transaction(
    create_dependencies: dict[str, int], db_session: Session
) -> None:
    repo = TransactionRepository(db_session)
    test_date = date.today()

    dto = HeaderDto(
        item_description="test",
        transaction_on=test_date,
        transaction_type=TransactionType.PAYMENT,
        total_paid_into_bank=0,
        reconciled=False,
        account_id=create_dependencies["acc_id"],
        notes="test",
        lines=[
            LineDto(amount=2400, category_id=create_dependencies["cat_id"])
        ],
    )

    result = repo.create(dto)

    assert result.item_description == "test"
    assert result.transaction_on == test_date
    assert result.transaction_type == TransactionType.PAYMENT
    assert result.total_paid_into_bank == 0
    assert result.reconciled is False
    assert result.account_id == create_dependencies["acc_id"]
    assert result.notes == "test"

    assert len(result.lines) == 1
    assert result.lines[0].amount == 2400
    assert result.lines[0].category_id == create_dependencies["cat_id"]


def test_repository_list_returns_only_non_deleted(
    create_dependencies: dict[str, int], db_session: Session
):
    repo = TransactionRepository(db_session)

    # First transaction
    dto1 = HeaderDto(
        item_description="t1",
        transaction_on=date.today(),
        transaction_type=TransactionType.PAYMENT,
        total_paid_into_bank=0,
        reconciled=False,
        account_id=create_dependencies["acc_id"],
        notes="n1",
        lines=[
            LineDto(amount=2400, category_id=create_dependencies["cat_id"])
        ],
    )
    model1 = repo.create(dto1)

    # Second transaction
    dto2 = HeaderDto(
        item_description="t2",
        transaction_on=date.today(),
        transaction_type=TransactionType.RECEIPT,
        total_paid_into_bank=0,
        reconciled=False,
        account_id=create_dependencies["acc_id"],
        notes="n2",
        lines=[
            LineDto(amount=5000, category_id=create_dependencies["cat_id"])
        ],
    )
    model2 = repo.create(dto2)

    # Soft delete the second one
    repo.delete(model2.id)

    # Act
    results = repo.list()

    # Assert
    assert len(results) == 1

    tx = results[0]
    assert tx.id == model1.id
    assert tx.item_description == "t1"
    assert tx.account_id == create_dependencies["acc_id"]
    assert len(tx.lines) == 1
    assert tx.lines[0].amount == 2400
    assert tx.lines[0].category_id == create_dependencies["cat_id"]