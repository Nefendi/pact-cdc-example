from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    username: str
    name: str
    surname: str
    hashed_password: bytes
    age: int
    job_title: str | None
    phone_number: str | None
    date_of_creation: datetime
