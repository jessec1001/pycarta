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
import asyncio
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


# def background(f):
#     def wrapper(*args, **kwds):
#         return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwds)
#     return wrapper


# @background
# def add_subtree(graph, parent, child, key):
#     graph.add_edge(parent, child)
#     build_nx(child, graph=graph, key=key, progress=False)


async def build_nx(
        parent: HyperthoughtNode,
        graph: Union[None, nx.DiGraph, nx.Graph]=None,
        *,
        key: Callable[[HyperthoughtNode], RETURN_TYPE]):
    """
    Builds a networkx graph rooted at the supplied parent node. This
    function is asynchronous to allow for parallel IO. Therefore,
    it should always be called as:

        graph = await build_nx(root, key=lambda x: get_children(parent))

    Interacting through the HyperThought API, this is typically:

        graph = await build_nx(
            root,
            key=lambda node: workflow_api.get_children(node.key)
        )

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


    Returns
    -------
    networkx.Graph or networkx.DiGraph
        The graph constructed from the parent node.

    Examples
    --------

        project_id = ...
        workflow_api = ...
        roots = [HyperthoughtNode(contents=experiment)
                for experiment in workflow_api.get_templates(project_id)]
        graph = await asyncio.gather(*[
            build_nx(
                root,
                key=lambda n: workflow_api.get_children(n.key)
            )
            for root in roots
        ])
    """
    graph = graph or nx.DiGraph()
    children = [
        HyperthoughtNode(contents=load(child, force=True))
        for child in key(parent)
    ]
    graph.add_edges_from([(parent, child) for child in children])
    result = await asyncio.gather(*[
        build_nx(child, graph, key=key) for child in children
    ])
    return graph
