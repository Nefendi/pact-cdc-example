# Source: https://github.com/pact-foundation/pact-python/blob/master/examples/fastapi_provider/tests/pact_provider.py

from datetime import datetime
from uuid import uuid4

import requests
from fastapi import APIRouter
from pactman.verifier.verify import ProviderStateMissing
from pydantic import BaseModel
from src.entities import User
from src.schemas import UserIn
from src.server import FAKE_DATABASE, app

pact_router = APIRouter()


class ProviderState(BaseModel):
    state: str


# pact-python way of setting provider states, pactman does it differently, see below
@pact_router.post("/_pact/provider_states")
async def pact_python_provider_states(provider_state: ProviderState):
    mapping = {"there exists at least one user in the database": insert_a_user_into_db}

    try:
        mapping[provider_state.state]()
    except KeyError:
        return {
            "result": f"No setup provided for the condition: {provider_state.state}"
        }

    return {"result": mapping[provider_state.state]}


app.include_router(pact_router)


def insert_a_user_into_db():
    user = User(
        id=uuid4(),
        name="Allice",
        surname="Smith",
        username="Mallice",
        age=28,
        hashed_password="super_secret_password123".encode("utf-8"),
        job_title="Accountant",
        phone_number="+48999888777",
        date_of_creation=datetime.utcnow(),
    )

    FAKE_DATABASE.append(user)


# pactman way of setting provider states
# HACK: The shenanigans with making a request manually are needed
# because the testing server is running in a different process and making any changes to the fake databases
# has no effect for the application. Probably with a real database involved, it would not be a problem.
def pactman_provider_states(root_address, name, **params):
    if name == "there exists at least one user in the database":
        user = UserIn(
            name="Allice",
            surname="Smith",
            username="Mallice",
            password="super_secret_password123",
            age=28,
            job_title="Accountant",
            phone_number="+48999888777",
            date_of_creation=datetime.utcnow(),
        )

        requests.post(root_address + "/users", json=user.dict())
    else:
        raise ProviderStateMissing(name)
