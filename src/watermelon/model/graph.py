from watermelon.model.vertex_types import EMPTY_VERTEX_TYPE
from watermelon_common.logger import LOGGER

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np


class Vertex:
    """Vertex of a graph, which has a certain type and identifier.

    The identifier must be a hashable type, and if the type is omitted
    then it is assumed to be an empty vertex.
    """

    def __init__(self, identifier, vertex_type=EMPTY_VERTEX_TYPE):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.type = vertex_type

    def __hash__(self):
        return self.hash

    def __eq__(self, __o):
        return (
            hash(self) == hash(__o)
            and self.type == __o.type
            and isinstance(__o, self.__class__)
        )

    def __repr__(self):
        return f"{repr(self.type)}({repr(self.id)})"

    def __str__(self):
        return f"{str(self.type)}({str(self.id)})"

    @property
    def id(self):
        return self._id

    @property
    def hash(self):
        return self._id_hash


class Edge:
    """Edge connecting two vertices."""

    def __init__(self, origin, target, weight=None):
        self.origin = origin
        self.target = target
        self.weight = weight

    def __eq__(self, __o):
        return (
            self.origin == __o.origin
            and self.target == __o.target
            and self.weight == __o.weight
            and isinstance(__o, self.__class__)
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.origin)}->{repr(self.target)}; {repr(self.weight)})"

    def __str__(self):
        return f"({str(self.origin)}->{str(self.target)}; {str(self.weight)})"


class Graph:
    """Data structure for an abstract graph."""

    def __init__(self):
        self._verts_id = {}
        self._vertices = set()
        self._adj_mat = pd.DataFrame()

    def __repr__(self):
        return repr(self._adj_mat)

    def __str__(self):
        return str(self._adj_mat.applymap(lambda e: e.weight if not pd.isnull(e) else e))

    @property
    def vertices(self):
        return self._vertices.copy()

    @property
    def adj_mat(self):
        return self._adj_mat.copy()

    def add_vertex(self, v):
        LOGGER.debug(f"Adding vertex {v}")
        self._vertices.add(v)
        self._verts_id[v.id] = v
        self._adj_mat[v] = np.nan
        self._adj_mat.loc[v] = np.nan

    def add_vertices(self, vertices):
        for v in vertices:
            self.add_vertex(v)

    def add_edge(self, e):
        LOGGER.debug(f"Adding edge {e}")
        if e.origin not in self._vertices:
            LOGGER.warning(f"Vertex {e.origin} was not found. Registering it")
            self.add_vertex(e.origin)
        if e.target not in self._vertices:
            LOGGER.warning(f"Vertex {e.target} was not found. Registering it")
            self.add_vertex(e.target)

        self._adj_mat.at[e.origin, e.target] = e

    def add_edges(self, edges):
        for e in edges:
            self.add_edge(e)

    def get_vertex(self, vert_id):
        return self._verts_id[vert_id]

    def get_edge(self, v, u):
        return self._adj_mat[v][u]

    def adjacent(self, v, u):
        return not pd.isnull(self.get_edge(v, u))

    def neighbors(self, v):
        return self._adj_mat[v][self._adj_mat[v].isna() == False].keys().to_list()


def draw_graph(graph, ax=None, pos_fn=None, **kwargs):
    # Parse the included graph data structure into the nx adjacency matrix format
    df = 1 - graph.adj_mat.applymap(lambda e: e.weight if not pd.isnull(e) else e).isna()
    df.columns = df.columns.map(lambda c: c.id)
    df.index = df.index.map(lambda c: c.id)
    G = nx.from_pandas_adjacency(df, nx.DiGraph)

    if pos_fn is not None:
        pos = pos_fn(G)
    else:
        pos = None

    nx.draw_networkx(G, ax=ax, pos=pos, **kwargs)
