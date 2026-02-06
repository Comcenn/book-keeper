
from typing import Annotated 
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from book_keeper.models import Account


class AccountDto(BaseModel):
    id: Annotated[int | None, Field(default=None)]
    name: Annotated[str, Field(min_length=1, max_length=80)]
    number: Annotated[str, Field(min_length=1, max_length=50)]

    model_config = ConfigDict(frozen=True)


class AccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def all(self) -> list[AccountDto]:
        return [AccountDto(id=acc.id, name=acc.name, number=acc.number) for acc in self.session.query(Account).filter_by(deleted=False).all()]
    
    def get(self, account_id: int) -> AccountDto | None:
        acc = self.session.query(Account).filter(Account.id == account_id, Account.deleted == False).one_or_none()
        if not acc:
            return None
        return AccountDto(id=acc.id, name=acc.name, number=acc.number)

    def create(self, account: AccountDto) -> AccountDto:
        acc = Account(name=account.name, number=account.number)
        self.session.add(acc)
        self.session.commit()
        return AccountDto(id=acc.id, name=acc.name, number=acc.number)

    def update(self, account: AccountDto) -> AccountDto:
        acc = self.session.query(Account).filter(Account.id == account.id).one_or_none()
        if not acc:
            raise ValueError("Cannot find Account to update.")
        acc.name = account.name
        acc.number = account.number
        self.session.commit()
        return AccountDto(id=acc.id, name=acc.name, number=acc.number)

    def delete(self, account: AccountDto) -> None:
        if not account.id:
            raise ValueError("'acc_id' not supplied unable to delete Account")
        acc = self.session.query(Account).filter(Account.id == account.id).one_or_none()
        if not acc:
            raise ValueError("Unable to delete as Account does not exist.")
        acc.deleted = True
        self.session.commit()
