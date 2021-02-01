from .nodes import HyperthoughtNode
from .build import build_nx


def serialize_graph(G):
    """
    Serialize a graph generated from the hyperthought schema.

    Parameters
    ----------
    G : networkx.DiGraph
        Graph to be serialized

    Returns
    -------
    JSON serializable object

    Example
    -------
    Serialize and save a graph:

        ```
        # G = networkx.DiGraph generated from HyperthoughtNode's
        with open("file.json", "wb") as ofs:
            json.dump(serialize_graph(G), ofs)
        ```
    """
    import networkx as nx
    mapping = {n:n.contents.dumps() for n in G.nodes}
    labeled = nx.relabel_nodes(G, mapping, copy=True)
    return nx.readwrite.json_graph.node_link_data(labeled)


def deserialize_graph(data):
    """
    Deserialize a graph generated from the hyperthought schema and
    serialized using `serialize_graph`.

    Parameters
    ----------
    data : JSON serialized data

    Returns
    -------
    networkx.DiGraph
        Graph of `HyperthoughtNode`s.

    Example
    -------
    Deserialize a saved graph:

        ```
        with open("file.json", "rb") as ifs:
            graph = deserialize_graph(json.load(ifs))
        ```
    """
    import networkx as nx
    from ..schema import loads
    G = nx.readwrite.json_graph.node_link_graph(data)
    mapping = {n:HyperthoughtNode(contents=loads(n)) for n in G.nodes}
    return nx.relabel_nodes(G, mapping, copy=True)
