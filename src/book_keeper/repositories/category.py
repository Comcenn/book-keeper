from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from book_keeper.models import Category


class CategoryDto(BaseModel):
    id: Annotated[int | None, Field(default=None)]
    name: Annotated[str, Field(min_length=1, max_length=80)]

    model_config = ConfigDict(frozen=True)


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def all(self) -> list[CategoryDto]:
        return [
            CategoryDto(id=cat.id, name=cat.name)
            for cat in self.session.query(Category).filter_by(deleted=False).all()
        ]

    def get(self, category_id: int) -> CategoryDto | None:
        cat = (
            self.session.query(Category)
            .filter(Category.id == category_id, Category.deleted == False)
            .one_or_none()
        )
        if not cat:
            return None
        return CategoryDto(id=cat.id, name=cat.name)

    def create(self, category: CategoryDto) -> CategoryDto:
        cat = Category(name=category.name)
        self.session.add(cat)
        self.session.commit()
        return CategoryDto(id=cat.id, name=cat.name)

    def update(self, category: CategoryDto) -> CategoryDto:
        cat = (
            self.session.query(Category)
            .filter(Category.id == category.id)
            .one_or_none()
        )
        if not cat:
            raise ValueError("Cannot find Category to update")
        cat.name = category.name
        self.session.commit()
        return CategoryDto(id=cat.id, name=cat.name)

    def delete(self, category: CategoryDto) -> None:
        if not category.id:
            raise ValueError("'id' not supplied for Category, unable to delete.")
        cat = (
            self.session.query(Category)
            .filter(Category.id == category.id)
            .one_or_none()
        )
        if not cat:
            raise ValueError("Unable to delete as category does not exist")
        cat.deleted = True
        self.session.commit()
