# simple_repo.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True

class UserRepository:
    def __init__(self):
        self._users: List[User] = []
        self._next_id = 1

    def create(self, name: str, email: str) -> User:
        if not name.strip():
            raise ValueError("Navn må ikke være tomt")
        if "@" not in email:
            raise ValueError("Ugyldig email")

        user = User(id=self._next_id, name=name, email=email)
        self._users.append(user)
        self._next_id += 1
        return user

    def read(self, user_id: int) -> Optional[User]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def update(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> User:
        user = self.read(user_id)
        if not user:
            raise ValueError(f"Bruger med id {user_id} findes ikke")

        if name is not None:
            if not name.strip():
                raise ValueError("Navn må ikke være tomt")
            user.name = name

        if email is not None:
            if "@" not in email:
                raise ValueError("Ugyldig email")
            user.email = email

        return user

    def delete(self, user_id: int) -> bool:
        for i, user in enumerate(self._users):
            if user.id == user_id:
                del self._users[i]
                return True
        return False

    def list_all(self) -> List[User]:
        return self._users.copy()