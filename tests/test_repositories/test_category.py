from sqlalchemy.orm import Session
from pytest import fixture

from book_keeper.repositories.category import CategoryDto, CategoryRepository


@fixture
def category_repo(db_session: Session) -> CategoryRepository:
    return CategoryRepository(session=db_session)


def test_repository_creates_an_account(category_repo: CategoryRepository) -> None:
    name = "test_cat"
    dto = CategoryDto(name=name)
    cat = category_repo.create(dto)
    assert cat.name == name, "Does not match name"


def test_repository_returns_all_accounts(category_repo: CategoryRepository) -> None:
    test_data = [CategoryDto(name=f"test_cat_{i}") for i in range(6)]
    cat_list = [category_repo.create(cat) for cat in test_data]
    assert [cat.name for cat in cat_list] == [test.name for test in test_data]


def test_repository_returns_empty_list_when_no_accounts_exist(
    category_repo: CategoryRepository,
) -> None:
    cat_list = category_repo.all()
    assert len(cat_list) == 0


def test_repository_updates_an_account(category_repo: CategoryRepository) -> None:
    name = "orig_test_cat"
    new_name = "new_test_cat"
    dto = CategoryDto(name=name)
    cat = category_repo.create(dto)
    assert cat.name == name
    update_dto = cat.model_copy(update={"name": new_name})
    updated_cat = category_repo.update(update_dto)
    assert updated_cat.name == new_name


def test_repository_soft_deletes_an_account(category_repo: CategoryRepository) -> None:
    dto = CategoryDto(name="test_name")
    cat = category_repo.create(dto)
    assert cat.id
    category_repo.delete(cat)
    assert not category_repo.get(cat.id)
