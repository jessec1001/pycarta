from .nodes import HyperthoughtNode
from ..schema import (File,
                      FileContent,
                      Header,
                      Metadata,
                      Permissions,
                      Restrictions,
                      Triple,
                      WorkflowTemplate,
                      Workflow,
                      WorkflowContent)
from ..schema import load
from tqdm.auto import tqdm
from typing import Union, Callable, Iterable, Mapping, Any
import networkx as nx

import logging
logger = logging.getLogger(__name__)


__all__ = ["build_nx"]


RETURN_TYPE = Union[ \
    Iterable[Mapping[Any, Any]], \
    File, \
    FileContent, \
    Header, \
    Metadata, \
    Permissions, \
    Restrictions, \
    Triple, \
    WorkflowTemplate, \
    Workflow, \
    WorkflowContent \
]


def build_nx(
        parent: HyperthoughtNode,
        graph: Union[None, nx.DiGraph, nx.Graph]=None,
        *,
        key: Callable[[HyperthoughtNode], RETURN_TYPE],
        progress: bool=True):
    """
    Builds a networkx graph rooted at the supplied parent node.

    Parameters
    ----------
    parent : HyperthoughtNode
        Root node for the graph.

    graph : networkx.Graph, networkx.DiGraph (optional)
        The graph object into which the graph is built. If not specified
        a networkx DiGraph is created.

    key : callable
        Function for identifying the child contents of a node that takes
        one positional parameter:

        - `node`, HyperthoughtNode: parent node whose children are to be
          collected.

        and returns a list of dictionary-like object. Each dictionary-like
        object are the child contents.

    progress : bool
        Whether or not to display a progress bar as the graph is being
        built.

    Returns
    -------
    networkx.Graph or networkx.DiGraph
        The graph constructed from the parent node.

    Examples
    --------

    >>> project_id = ...
    >>> workflow_api = ...
    >>> root = [HyperthoughtNode(contents=experiment)
                for experiment in workflow_api.get_templates(project_id)][0]
    >>> graph = build(root, key=lambda n: workflow_api.get_children(n.key))
    """
    if graph is None:
        graph = nx.DiGraph()
    # get the children
    children = [HyperthoughtNode(contents=child) for child in key(parent)]
    for child in (tqdm(children) if progress else children):
        # this builds the graph through preorder access
        graph.add_edge(parent, child)
        build_nx(child, graph=graph, key=key)
    graph.nodes[parent]["label"] = parent.name
    return graph
