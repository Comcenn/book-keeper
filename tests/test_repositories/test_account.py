from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.repositories.account import AccountRepository


@fixture
def account_repo(db_session: Session) -> AccountRepository:
    return AccountRepository(session=db_session)


def test_repository_creates_an_account(account_repo: AccountRepository) -> None:
    name = "test_account"
    number = "00111TEST"
    acc = account_repo.create(name, number)
    assert acc.name == name, "Does not match name"
    assert acc.number == number, "Does not match number"


def test_repository_returns_all_accounts(account_repo: AccountRepository) -> None:
    test_data = [(f"test_acc_{i}", f"011{i}TEST{i}") for i in range(6)]
    for name, number in test_data:
        account_repo.create(name, number)
    acc_list = [(acc.name, acc.number) for acc in account_repo.all()]
    assert acc_list == test_data


def test_repository_returns_empty_list_when_no_accounts_exist(
    account_repo: AccountRepository,
) -> None:
    acc_list = account_repo.all()
    assert len(acc_list) == 0


def test_repository_updates_an_account(account_repo: AccountRepository) -> None:
    name = "orig_test_acc"
    number = "orig_test_number"
    new_name = "new_test_acc"
    new_number = "new_test_number"
    acc = account_repo.create(name, number)
    assert acc.name == name
    assert acc.number == number
    account_repo.update(acc, new_name, new_number)
    assert acc.name == new_name
    assert acc.number == new_number


def test_repository_soft_deletes_an_account(account_repo: AccountRepository) -> None:
    name = "test_name"
    number = "test_number"
    acc = account_repo.create(name, number)
    account_repo.delete(acc)
    assert acc.deleted
