import os
# import sys
import pytest

from pycarta.api import create_agent


@pytest.fixture
def cartaAuth():
    if "CARTA_AUTH" not in os.environ:
        print("Set 'export CARTA_AUTH=[Carta auth token]' before testing.")
        raise ValueError(
            "Envinronment variable CARTA_AUTH must be set to run tests."
        )
    return os.environ["CARTA_AUTH"]

@pytest.fixture
def  cartaUrl():
    if "CARTA_URL" not in os.environ:
        print("Set 'export CARTA_URL=[Carta URL]' before testing.")
        raise ValueError(
            "Envinronment variable CARTA_URL must be set to run tests."
        )
    return os.environ["CARTA_URL"]


def test_agent(cartaAuth, cartaUrl):
    token = cartaAuth
    url = cartaUrl
    agent = create_agent(token, url=url)
    assert agent.url == url


def test_authenticated(cartaAuth, cartaUrl):
    token = cartaAuth
    url = cartaUrl
    agent = create_agent(token, url=url)
    response = agent.get("user/authenticated", verify=False)
    assert response
    assert response.json()
