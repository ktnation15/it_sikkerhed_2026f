import json
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    person_id: int
    first_name: str
    last_name: str
    address: str
    street_number: int
    password: str            # NB: I en rigtig applikation skal dette hashes!
    enabled: bool = True


class DataHandler:
    """Håndterer brugere gemt i en JSON-fil (flat file database)."""

    def __init__(self, filename: str = "users.json"):
        self.filename = filename
        self.users: List[User] = self._load()

    def _load(self) -> List[User]:
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [User(**item) for item in raw]

    def _save(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(
                [vars(u) for u in self.users],
                f,
                ensure_ascii=False,
                indent=2
            )

    def create_user(
        self,
        first_name: str,
        last_name: str,
        address: str,
        street_number: int,
        password: str,
        enabled: bool = True
    ) -> User:
        """Opretter en ny bruger og tildeler automatisk næste ledige ID."""
        next_id = max((u.person_id for u in self.users), default=-1) + 1

        user = User(
            person_id=next_id,
            first_name=first_name,
            last_name=last_name,
            address=address,
            street_number=street_number,
            password=password,
            enabled=enabled,
        )

        self.users.append(user)
        self._save()
        return user

    def get_user_by_id(self, person_id: int) -> Optional[User]:
        for user in self.users:
            if user.person_id == person_id:
                return user
        return None

    def get_number_of_users(self) -> int:
        return len(self.users)

    def enable_user(self, person_id: int) -> bool:
        """Sætter enabled = True. Returnerer True hvis brugeren blev fundet."""
        user = self.get_user_by_id(person_id)
        if user is None:
            return False
        user.enabled = True
        self._save()
        return True

    def disable_user(self, person_id: int) -> bool:
        """Sætter enabled = False. Returnerer True hvis brugeren blev fundet."""
        user = self.get_user_by_id(person_id)
        if user is None:
            return False
        user.enabled = False
        self._save()
        return True

    def get_all_users(self) -> List[User]:
        return self.users.copy()