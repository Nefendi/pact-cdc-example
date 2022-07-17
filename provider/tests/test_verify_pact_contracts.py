from functools import partial
from pathlib import Path

import pytest
from pact import Verifier

# WARN: This needs to be here in order to set up a path with provider states for pact-python
from . import pact_provider


@pytest.mark.usefixtures("run_server")
def test_verify_pact_contracts_with_pact_python(root_address: str) -> None:
    pacts_directory = Path().cwd().parent / "pact_contracts"
    pacts = [
        str(pact)
        for pact in pacts_directory.iterdir()
        if pact.is_file() and pact.suffix == ".json"
    ]
    verifier = Verifier(
        provider="User Provider Service", provider_base_url=root_address
    )

    output, _ = verifier.verify_pacts(
        *pacts, provider_states_setup_url=f"{root_address}/_pact/provider_states"
    )

    assert output == 0


# For a pactman pytest plugin to work, --pact-files or a --pact-broker-url flag must be given to pytest
# @pytest.mark.usefixtures("run_server")
# def test_verify_pact_contracts_with_pactman(root_address: str, pact_verifier) -> None:
#     provider_states = partial(pact_provider.pactman_provider_states, root_address)
#
#     pact_verifier.verify(root_address, provider_states)
