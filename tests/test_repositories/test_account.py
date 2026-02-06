from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.repositories.account import AccountRepository, AccountDto


@fixture
def account_repo(db_session: Session) -> AccountRepository:
    return AccountRepository(session=db_session)


def test_repository_creates_an_account(account_repo: AccountRepository) -> None:
    name = "test_account"
    number = "00111TEST"
    account = AccountDto(name=name, number=number)
    acc = account_repo.create(account)
    assert acc.name == name, "Does not match name"
    assert acc.number == number, "Does not match number"


def test_repository_returns_all_accounts(account_repo: AccountRepository) -> None:
    test_data = [AccountDto(name=f"test_acc_{i}", number=f"011{i}TEST{i}") for i in range(6)]
    acc_list = [account_repo.create(acc) for acc in test_data]
    assert list(map(lambda acc: (acc.name, acc.number),acc_list)) == list(map(lambda acc: (acc.name, acc.number) ,test_data))


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

    account = AccountDto(name=name, number=number)
    acc = account_repo.create(account)
    assert acc.name == name
    assert acc.number == number
    update_dto = AccountDto(id=acc.id, name=new_name, number=new_number)
    updated_acc = account_repo.update(update_dto)
    assert updated_acc.name == new_name
    assert updated_acc.number == new_number


def test_repository_soft_deletes_an_account(account_repo: AccountRepository) -> None:
    name = "test_name"
    number = "test_number"
    account = AccountDto(name=name, number=number)
    acc = account_repo.create(account)
    assert acc.id
    account_repo.delete(acc)
    assert not account_repo.get(acc.id)
