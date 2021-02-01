from collections.abc import Hashable, MutableMapping
from typing import Optional
from uuid import UUID, uuid4 as uid

import logging
logger = logging.getLogger(__name__)


__all__ = ["Node"]


class Node(Hashable, MutableMapping):
    def __init__(self, *names, contents: dict=dict(), uuid: Optional[str]=None):
        """
        Node is an object that can be used as a key in a dictionary
        or as a node in a graph. It is a type of dictionary, which
        holds the attributes of the node.

        Parameters
        ----------
        names : positional parameters
            Names by which this node is known. The first is the primary
            names, all others are aliases.

        contents : dict-like
            Contents of the node.

        uuid : str, optional
            An optional string representation of a 32-character hex UID. By
            default, this is generated automatically.

        API
        ---
        uid : str
            Node UID formatted as xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

        name
            Getter/setter for the primary node identifier. While this is most
            naturally a string, type is not enforced.

            Example: node_instance.name = 'foo'  # setting the name
            Example: rval = node_instance.name   # getting the name

        alias
            Alternative names/identifiers for the node.

            Example: if identifier in node_instance.alias: print("True")

        node.add_alias(...)
            Add an alias, if it does not already exist.

        node.rm_alias(...)
            Remove an alias, if it exists.
        """
        self.__uid = uid() if uuid is None else UUID(uuid)
        self.__alias: tuple = names
        self.contents = contents

    def __hash__(self):
        return self.__uid.int

    def __getitem__(self, key):
        return self.contents[key]

    def __setitem__(self, key, value):
        self.contents[key] = value

    def __delitem__(self, key):
        del self.contents[key]

    def __iter__(self):
        return iter(self.contents)

    def __len__(self):
        return len(self.contents)

    def __eq__(self, rhs):
        return rhs in (hash(self),
                       self.uid,
                       *self.alias)

    def __str__(self):
        return str(self.contents)

    @property
    def uid(self) -> str:
        return str(self.__uid)

    @property
    def name(self):
        try:
            return self.alias[0]
        except IndexError:
            return None

    @name.setter
    def name(self, name_):
        if name_ is not None:
            self.rm_alias(name_)
            self.__alias = (name_, *self.__alias)

    @property
    def alias(self):
        return self.__alias

    def add_alias(self, alias):
        """
        Adds an alias. Aliases are retained in the order in which they were
        added. Attempting to add an alias already present does not update the
        alias order.

        Parameters
        ----------
        alias
            Alias to add.

        Returns
        -------
        Node
            Returns this node, allowing these functions to be daisy-chained.

        Examples
        --------
        Add an alias to a Node instance,

            >>> node.add_alias('foo')

        Ensure an alias is the last alias in the set,

            >>> node.rm_alias('foo').add_alias('foo')
        """
        if alias is not None:
            # we could use set, except:
            # 1. order matters--the first alias is the name
            # 2. set is mutable, so returning a set allows user modification.
            if alias not in self.__alias:
                self.__alias = (*self.__alias, alias)
        return self

    def rm_alias(self, alias):
        """
        Removes an alias. If this alias is also the name, then the name will
        be reset to one of the other aliases.

        Parameters
        ----------
        alias
            Alias to remove.

        Returns
        -------
        Node
            Returns this node, allowing these functions to be daisy-chained.
        """
        self.__alias = tuple(set(self.__alias) - set((alias,)))
        return self
