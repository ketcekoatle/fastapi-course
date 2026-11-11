from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User

class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)
        return self.db.scalar(stmt)

    def create_user(self, login: str, email: str, password: str) -> User:
        user = User(login=login, email=email, hashed_password=password)
        self.db.add(user)
        self.db.flush()
        return user
