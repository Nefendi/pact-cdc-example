from datetime import datetime
from typing import Any
from uuid import uuid4

import bcrypt
from fastapi import FastAPI, status
from src.entities import User
from src.schemas import UserIn, UserOut

app = FastAPI()

FAKE_DATABASE: list[User] = []


@app.get("/users", response_model=list[UserOut])
async def list_users() -> Any:
    return FAKE_DATABASE


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn) -> Any:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
    del user.password

    new_user = User(
        **user.dict(),
        id=uuid4(),
        hashed_password=hashed_password,
        date_of_creation=datetime.utcnow()
    )

    FAKE_DATABASE.append(new_user)

    return new_user
