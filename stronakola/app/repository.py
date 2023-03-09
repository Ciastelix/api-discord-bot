from contextlib import AbstractContextManager
from typing import Callable, Iterator
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from app.models import User
from app.schemas import UserSchema

class UserRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[User]:
        with self.session_factory() as session:
            return session.query(User).all()

    def get_by_nick(self, nick: str) -> UserSchema:
        with self.session_factory() as session:
            return session.query(User).filter_by(nick=nick).first()

    def add(self, user: UserSchema) -> User:
        with self.session_factory() as session:
            user = User(**user.dict(exclude_unset=True))
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def delete_by_nick(self, nick: str) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.nick == nick).first()
            if not entity:
                raise NoResultFound
            session.delete(entity)
            session.commit()
