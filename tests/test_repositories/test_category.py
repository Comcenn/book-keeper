from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.repositories.category import CategoryRepository


@fixture
def category_repo(db_session: Session) -> CategoryRepository:
    return CategoryRepository(session=db_session)


def test_repository_creates_an_account(category_repo: CategoryRepository) -> None:
    name = "test_cat"
    cat = category_repo.create(name)
    assert cat.name == name, "Does not match name"


def test_repository_returns_all_accounts(category_repo: CategoryRepository) -> None:
    test_data = [f"test_cat_{i}" for i in range(6)]
    for name in test_data:
        category_repo.create(name)
    cat_list = [cat.name for cat in category_repo.all()]
    assert cat_list == test_data


def test_repository_returns_empty_list_when_no_accounts_exist(
    category_repo: CategoryRepository,
) -> None:
    cat_list = category_repo.all()
    assert len(cat_list) == 0


def test_repository_updates_an_account(category_repo: CategoryRepository) -> None:
    name = "orig_test_cat"
    new_name = "new_test_cat"
    cat = category_repo.create(name)
    assert cat.name == name
    category_repo.update(cat, new_name)
    assert cat.name == new_name


def test_repository_soft_deletes_an_account(category_repo: CategoryRepository) -> None:
    name = "test_name"
    cat = category_repo.create(name)
    category_repo.delete(cat)
    assert cat.deleted
