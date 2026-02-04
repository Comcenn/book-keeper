from sqlalchemy.orm import Session

from book_keeper.models import Category


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def all(self) -> list[Category]:
        return self.session.query(Category).filter_by(deleted=False).all()

    def get(self, category_id: int) -> Category | None:
        return (
            self.session.query(Category)
            .filter(Category.id == category_id)
            .one_or_none()
        )

    def create(self, name: str) -> Category:
        cat = Category(name=name)
        self.session.add(cat)
        self.session.commit()
        return cat

    def update(self, category: Category, name: str) -> None:
        category.name = name
        self.session.commit()

    def delete(self, category: Category) -> None:
        category.deleted = True
        self.session.commit()
