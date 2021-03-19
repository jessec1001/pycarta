from ...base import Node
from ..schema import File, Workflow, WorkflowTemplate
from copy import deepcopy

import logging
logger = logging.getLogger(__name__)


class HyperthoughtNode(Node):
    """
    Like Node, HyperthoughtNode is an object that can be used as a key in a
    dictionary or as a node in a graph. It is a type of dictionary, which
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

    name
        Name associated with this node. This can be any identifier, but will
        typically be a string, UUID, or int.

    key : str
        String representation of the UUID of the *contents* of the node.
        This is different than the UUID of the node, that is, the node
        has a unique identifier (accessible as `HypterthoughtNode.uid`) that
        uniquely identifies the node in the graph. The contents of the node
        also have a unique identifier to identify the record in the
        HyperThought database (a.k.a. *primary key*, hence the name of this
        property).

    node.add_alias(...)
        Add an alias, if it does not already exist.

    node.rm_alias(...)
        Remove an alias, if it exists.
    """

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

    def __hash__(self):
        return super().__hash__()

    # Accessors to properties defined in the Hyperthought schema
    @property
    def name(self):
        if isinstance(self.contents, (File, Workflow)):
            return self.contents["content"]["name"]
        elif isinstance(self.contents, WorkflowTemplate):
            return self.contents["name"]
        else:
            return getattr(super(), "name", self.key)

    @name.setter
    def name(self, value):
        if isinstance(self.contents, (File, Workflow)):
            self.contents["content"]["name"] = value
        elif isinstance(self.contents, WorkflowTemplate):
            self.contents["name"] = value
        else:
            super().name = value

    @property
    def key(self):
        if isinstance(self.contents, (File, Workflow)):
            return self.contents["content"]["pk"]
        elif isinstance(self.contents, WorkflowTemplate):
            return self.contents["key"]
        else:
            return None
