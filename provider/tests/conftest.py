import socket
from multiprocessing import Process
from time import sleep
from typing import Generator, cast

import pytest
import uvicorn


@pytest.fixture(scope="module")
def random_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return cast(int, s.getsockname()[1])


@pytest.fixture(scope="module")
def host() -> str:
    return "127.0.0.1"


@pytest.fixture(scope="module")
def root_address(host: str, random_port: int) -> str:
    return f"http://{host}:{random_port}"


@pytest.fixture(scope="module")
def path_to_app() -> str:
    return "src.server:app"


@pytest.fixture(scope="module")
def run_server(
    host: str, random_port: int, path_to_app: str
) -> Generator[None, None, None]:
    server_process = Process(
        target=uvicorn.run,
        args=(path_to_app,),
        kwargs={"host": host, "port": random_port, "log_level": "critical"},
        daemon=True,
    )
    server_process.start()
    _wait_for_server_to_start(host, random_port)
    yield
    server_process.kill()


def _wait_for_server_to_start(host: str, port: int) -> None:
    seconds = 5

    for _ in range(seconds * 10):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
        except ConnectionRefusedError:
            sleep(0.1)
            continue
        else:
            return

    raise TimeoutError(
        f"Could not set up the test server in {seconds} seconds. Aborting!"
    )
