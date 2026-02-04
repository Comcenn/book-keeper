from sqlalchemy.orm import Session

from book_keeper.models import Account


class AccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def all(self) -> list[Account]:
        return self.session.query(Account).filter_by(deleted=False).all()

    def create(self, name: str, number: str) -> Account:
        acc = Account(name=name, number=number)
        self.session.add(acc)
        self.session.commit()
        return acc

    def update(self, account: Account, name: str, number: str) -> None:
        account.name = name
        account.number = number
        self.session.commit()

    def delete(self, account: Account) -> None:
        account.deleted = True
        self.session.commit()
