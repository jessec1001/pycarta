.. _quickstart:

==========
Quickstart
==========

.. highlight:: python

Start by importing the library tools we need to access Hyperthought through
its API.

::

    import sys, os
    import json
    from getpass import getpass
    from pprint import pprint
    from hyperthought import auth, api
    from hyperthought.graph import (HyperthoughtNode,
                                    build_nx,
                                    serialize_graph,
                                    deserialize_graph)
    from hyperthought.schema import load, loads

Then enable access through the Hyperthought authentication protocol. Because
authentication is time-limited, this must be done interactively.

::

    key = getpass("Paste API Key: ")
    auth_ = auth.Authorization(key)

Once authenticated, set the project ID, which is the 32-character hexadecimal
string in the URL when you access this project.

::

    workflow_api = api.workflow.WorkflowAPI(auth=auth_)
    project_id = '245f8eda-77b4-49ae-8589-2bb16afbbbce'


At this point, we are ready to construct the graph from data stored in
Hyperthought. Depending on the size of the data in the dataset, this can take
quite a while, so the following code has some logic to avoid re-reading data
that has already been read and processed.

::

    # Check if this data has already been processed and saved.
    # Simply change this to `if False:` to force the data to be
    # reprocessed.
    if os.path.isfile("graphs.json"):
        with open("graphs.json", "r") as ifs:
            graphs = [deserialize_graph(data) for data in json.load(ifs)]
    else:
        # get the roots from this experiment. Each is stored in a
        # HyperthoughtNode.
        roots = [HyperthoughtNode(contents=load(experiment)) for experiment
                 in workflow_api.get_templates(project_id)]

        # Build graphs from each experiment.
        def get_children(node):
            """
            Returns a list of processed child nodes from the given parent.
            """
            return load(workflow_api.get_children(node.key), force=True)

        graphs = list()
        for root in roots:
            print(f"Building graph for root {root.name} ({root.key})")
            graphs.append(build_nx(root, key=get_children))

        # Save the results to facilitate later loading.
        with open("graphs.json", "w") as ofs:
            json.dump([serialize_graph(G) for G in graphs], ofs)

With the graphs now constructed, the following code block can be used
to visualize each graph separately. First, load the necessary libraries.

::

    from pyvis.network import Network
    from json2html import *
    import networkx as nx

We may want to differentiate the nodes based on their process type: workflow
vs. template vs. process, etc.

::

    def process_type(node):
        try:
            return node.contents["content"]["process_type"]
        except KeyError:
            return None

A quick one-liner to set the graph we want to plot::

    G = graphs[0]

Unfortunately, `pyvis` nodes must be strings, so we must relabel the graph
with the name, which is accessible through `name` property in the Hyperthought
API.

::

    mapping = {n:n.name for n in graphs[0].nodes}
    inverse = {n.name:n for n in graphs[0].nodes}
    labeled = nx.relabel_nodes(G, mapping, copy=True)

We want to customize colors, sizes, edges, labels, titles, and other
information contained in the graph visualization. This is a bit exploratory,
giving you the opportunity to experiment before coding the formatting in
a more concrete way.

::

    colors = ['#00ff1e', '#162347', '#dd4b39', '#1e47dd']
    cmap = dict()
    for key in labeled.nodes.keys():
        node = inverse[key]
        if process_type(node) not in cmap:
            cmap[process_type(node)] = colors.pop()
        labeled.nodes[key]['label'] = key
        labeled.nodes[key]['title'] = \
            '<div style="font-family:courier new;">' + \
                json2html.convert(
                    node.contents.get("metadata", None),
                    table_attributes='class="table table-borderless"'
                ) + \
            '</div>'
        labeled.nodes[key]['color'] = cmap[process_type(node)]

Now there's nothing left but to generate the graph.::

    g = Network(height=800, width=800, notebook=True)
    g.toggle_hide_edges_on_drag(False)
    g.barnes_hut()
    g.from_nx(labeled)
    g.show("graph.html")

.. raw:: html
    :file: resources/graph.html
