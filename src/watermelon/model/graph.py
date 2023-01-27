from watermelon.model.vertex_types import EMPTY_VERTEX_TYPE
from watermelon_common.logger import LOGGER

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
            self.hash == __o.hash
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
        return str(self._adj_mat)

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
        if self._vertices.get(e.origin) is None:
            LOGGER.warning(f"Vertex {e.origin} was not found. Registering it")
            self.add_vertex(e.origin)
        if self._vertices.get(e.target) is None:
            LOGGER.warning(f"Vertex {e.target} was not found. Registering it")
            self.add_vertex(e.target)

        self._adj_mat[e.origin][e.target] = e

    def add_edges(self, edges):
        for e in edges:
            self.add_edge(e)

    def get_vertex(self, vert_id):
        return self._verts_id[vert_id]

    def get_edge(self, v, u):
        return self._adj_mat[v][u]

    def adjacent(self, v, u):
        return not np.isnan(self.get_edge(v, u))

    def neighbors(self, v):
        return self._adj_mat[v][self._adj_mat[v].isna() == False].keys().to_list()
