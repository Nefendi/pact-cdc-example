from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    age: int
    job_title: str | None
    phone_number: str | None


class UserIn(UserBase):
    password: str


# Notice an additional field 'date_of_creation', it will be also sent to the consumer
# but additional fields do not violate pacts due to Postel's Law:
# "Be liberal in what you accept, and conservative in what you send".
# Different consumers may require different data from the same provider so no consumer
# should tell the provider that it sends more data than needed.
class UserOut(UserBase):
    id: UUID
    date_of_creation: datetime
