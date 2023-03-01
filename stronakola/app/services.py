from typing import Iterator
from app.repository import UserRepository
from app.schemas import UserSchema
from app.models import User


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self._repository: UserRepository = user_repository

    def get_all(self) -> Iterator[User]:
        return self._repository.get_all()

    def get(self, nick: str) -> User:
        return self._repository.get_by_nick(nick)

    def delete(self, nick: str) -> None:
        return self._repository.delete_by_nick(nick)

    def add_user(self, user: UserSchema) -> User:
        return self._repository.add(user)
