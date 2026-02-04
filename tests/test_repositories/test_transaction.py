from datetime import date
from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.repositories.account import AccountRepository
from book_keeper.repositories.category import CategoryRepository
from book_keeper.repositories.transaction import (
    TransactionRepository,
    Header,
    Line,
    TransactionType,
)


@fixture
def create_dependencies(db_session: Session) -> dict[str, int]:
    cat_repo = CategoryRepository(db_session)
    acc_repo = AccountRepository(db_session)
    cat = cat_repo.create("GiftAid")
    acc = acc_repo.create(name="CURRENT", number="01675667")
    return {"cat_id": cat.id, "acc_id": acc.id}


def test_repository_creates_transaction(
    create_dependencies: dict[str, int], db_session: Session
) -> None:
    repo = TransactionRepository(db_session)
    test_date = date.today()
    line = Line(amount=2400, category_id=create_dependencies["cat_id"])
    trans = Header(
        item_description="test",
        transaction_on=test_date,
        transaction_type=TransactionType.PAYMENT,
        total_paid_into_bank=0,
        reconciled=False,
        account_id=create_dependencies["acc_id"],
        notes="test",
        lines=[line],
    )

    model = repo.create(trans)
    assert model.item_description == "test"
    assert model.transaction_on == test_date
    assert model.transaction_type == str(TransactionType.PAYMENT)
    assert model.total_paid_into_bank == 0
    assert model.reconciled == False
    assert model.account.name == "CURRENT"
    assert model.notes == "test"
    assert len(model.lines) == 1
    assert model.lines[0].amount == 2400
    assert model.lines[0].category.name == "GiftAid"
    assert model.lines[0].transaction_header_id == model.id


def test_repository_list_returns_only_non_deleted(
    create_dependencies: dict[str, int], db_session: Session
):
    repo = TransactionRepository(db_session)

    # --- Create first transaction ---
    line1 = Line(amount=2400, category_id=create_dependencies["cat_id"])
    header1 = Header(
        item_description="t1",
        transaction_on=date.today(),
        transaction_type=TransactionType.PAYMENT,
        total_paid_into_bank=0,
        reconciled=False,
        account_id=create_dependencies["acc_id"],
        notes="n1",
        lines=[line1],
    )
    model1 = repo.create(header1)

    # --- Create second transaction ---
    line2 = Line(amount=5000, category_id=create_dependencies["cat_id"])
    header2 = Header(
        item_description="t2",
        transaction_on=date.today(),
        transaction_type=TransactionType.RECEIPT,
        total_paid_into_bank=0,
        reconciled=False,
        account_id=create_dependencies["acc_id"],
        notes="n2",
        lines=[line2],
    )
    model2 = repo.create(header2)

    # --- Soft delete the second one ---
    model2.deleted = True
    db_session.commit()

    # --- Act ---
    results = repo.list()

    # --- Assert ---
    assert len(results) == 1
    tx = results[0]

    assert tx.id == model1.id
    assert tx.item_description == "t1"
    assert tx.account.name == "CURRENT"  # eager-loaded
    assert len(tx.lines) == 1  # eager-loaded
    assert tx.lines[0].amount == 2400
    assert tx.lines[0].category.name == "GiftAid"
