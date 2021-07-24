from .agent import Agent
from ..base.logger import functionlogger
from numbers import Number
from typing import Any, Optional, Union


JsonType = Union[str, int, float, bool, None, dict[str, Any], list[Any]]


@functionlogger
def user(agent: Agent, **kwds)) -> Optional[JsonType]:
    """
    Gets the current user information from Carta.

    Parameters
    ----------
    agent : Agent
        Agent to handle communication with the Carta server.

    Returns
    -------
    dict
        Information about the current user:
            id: Unique ID for this user.
            name: Username for this user.
            email: Email for this user.
            firstName: First (Given) name for this user.
            lastName: Last (Family) name for this user.
    """
    response = agent.get("user", **kwds)
    if response:
        return response.json()
    else:
        return None


@functionlogger
def authenticated(agent: Agent, **kwds) -> bool:
    """
    Returns whether the current user is authenticated.

    Returns
    -------
    bool
        True if user is authenticated. False otherwise.
    """
    response = agent.get("user/authenticated")
    if response:
        return response.json()
    else:
        return None


@functionlogger
def users(agent: Agent,
    attribute: str=None,
    value: str=None,
    filter: str='equal',
    **kwds)
) -> Optional[JsonType]:
    """
    Gets the current user information from Carta.

    Parameters
    ----------
    agent : Agent
        Agent to handle communication with the Carta server.
    attribute : str (optional)
        Attribute on which to filter the users. Must be one of:
            UserName
            Email
            FirstName
            LastName
    value : str (optional)
        Value to search for. Must be specified if `attribute` is given.
    filter : str (optional)
        Method of comparison. Must be one of:
            equal
            startswith

    Returns
    -------
    list of dict
        Information about the matching users. Each user contains:
            id: Unique ID for this user.
            name: Username for this user.
            email: Email for this user.
            firstName: First (Given) name for this user.
            lastName: Last (Family) name for this user.
    """
    # set up the parameters of the API call
    params = dict()
    if attribute:
        params = {
            "attributeName": attribute,
            "attributeValue": value,
            "attributeFilter": {
                "equal": "=",
                "equals": "=",
                "startswith": "^="
            }[filter.lower()]
        }
    kwds["params"] = {
        **params,
        **kwds.get("params", dict())
    }
    response = agent.get("user", **kwds)
    if response:
        return response.json()
    else:
        return None
