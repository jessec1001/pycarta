from .accessors import *
from .base import *
from .parsers import *
from hyperthought.auth import Authorization


def get_auth(token: str) -> Authorization:
    return Authorization(auth_payload=token)
