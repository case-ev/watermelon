"""
watermelon.model.graph
----------------------
Modelling of the graph that represents the environment.
"""

from typing import Callable, Hashable, List, Self

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from watermelon_common.logger import LOGGER
from watermelon.model.edge import Edge
from watermelon.model.vertex import Vertex
from watermelon.exceptions import NonExistentEdgeException


class Graph:
    """Data structure for an abstract graph"""

    def __init__(self, vertices: List[Vertex] = None, edges: List[Edge] = None) -> None:
        self._verts_id = {}
        self._vertices = set()
        self._adj_mat = pd.DataFrame()

        if vertices is not None:
            self.add_vertices(vertices)
        if edges is not None:
            self.add_edges(edges)

    def __repr__(self) -> str:
        return repr(self._adj_mat)

    def __str__(self) -> str:
        return str(
            self._adj_mat.applymap(lambda e: e.weight if not pd.isnull(e) else e)
        )

    def __getitem__(self, key: Hashable) -> Vertex:
        try:
            # See if an iterable of id's is given
            vertices = []
            for vertex_id in key:
                vertices.append(self._verts_id[hash(vertex_id)])
            return vertices
        except TypeError:
            # This would happen if it is not an iterable
            return self._verts_id[hash(key)]

    @property
    def id(self) -> Hashable:
        """IDs of all vertices"""
        return self._verts_id.keys()

    @property
    def vertices(self) -> List[Vertex]:
        """Vertices within the graph"""
        return self._vertices.copy()

    @property
    def adj_mat(self) -> pd.DataFrame:
        """Adjacency matrix of the graph, which codifies the edges"""
        return self._adj_mat.copy()

    def add_vertex(self, vertex: Hashable | Vertex) -> Self:
        """Add a vertex to the graph

        Parameters
        ----------
        vertex : watermelon.model.Vertex
            Vertex to add to the graph

        Returns
        -------
        self
        """
        # Allow creation from a hashable type
        if isinstance(vertex, Vertex):
            parsed_vertex = vertex
        else:
            parsed_vertex = Vertex(vertex)

        LOGGER.debug("Adding vertex %s", parsed_vertex)
        self._vertices.add(parsed_vertex)
        self._verts_id[parsed_vertex.hash] = parsed_vertex
        self._adj_mat[parsed_vertex] = np.nan
        self._adj_mat.loc[parsed_vertex] = np.nan
        return self

    def add_vertices(self, vertices: List[Hashable | Vertex]) -> Self:
        """Add a group of vertices to the graph

        Parameters
        ----------
        vertices : iterable of watermelon.model.Vertex
            Iterable where each iteration yields a vertex

        Returns
        -------
        self
        """
        for vertex in vertices:
            self.add_vertex(vertex)
        return self

    def add_edge(self, edge: Edge) -> Self:
        """Add an edge to the graph

        If the vertices are not found in the graph, it adds them first

        Parameters
        ----------
        edge : watermelon.model.Edge
            Edge connecting two vertices

        Returns
        -------
        self
        """
        LOGGER.debug("Adding edge %s", edge)
        if edge.origin not in self._vertices:
            LOGGER.warning("Vertex %s was not found. Registering it", edge.origin)
            self.add_vertex(edge.origin)
        if edge.target not in self._vertices:
            LOGGER.warning("Vertex %s was not found. Registering it", edge.target)
            self.add_vertex(edge.target)

        self._adj_mat.at[edge.origin, edge.target] = edge
        return self

    def add_edges(self, edges: List[Edge]) -> Self:
        """Add a group of edges to the graph

        If the vertices are not found in the graph, it adds them first

        Parameters
        ----------
        edges : iterable of watermelon.model.Edge
            Iterable that yields edges to be added

        Returns
        -------
        self
        """
        for edge in edges:
            self.add_edge(edge)
        return self

    def _parse_vertex(self, vertex_representation: Hashable | Vertex) -> Vertex:
        try:
            if vertex_representation in self._verts_id:
                return self[vertex_representation]
            return vertex_representation
        except AttributeError:
            return vertex_representation

    def get_vertex(self, vert_id: Hashable) -> Vertex:
        """Get the vertex associated with a given ID"""
        return self._parse_vertex(vert_id)

    def get_edge(self, vert1: Hashable | Vertex, vert2: Hashable | Vertex) -> Edge:
        """Get the edge that connects two vertices"""
        vert1 = self._parse_vertex(vert1)
        vert2 = self._parse_vertex(vert2)
        result = self._adj_mat[vert2][vert1]
        if pd.isnull(result):
            raise NonExistentEdgeException(vert1, vert2)
        return result

    def adjacent(self, vert1: Hashable | Vertex, vert2: Hashable | Vertex) -> bool:
        """Indicate whether two vertices are adjacent"""
        vert1 = self._parse_vertex(vert1)
        vert2 = self._parse_vertex(vert2)
        return not pd.isnull(self.get_edge(vert1, vert2))

    def neighbors(self, vertex: Hashable | Vertex) -> List[Vertex]:
        """Get the neighbors of a vertex"""
        vertex = self._parse_vertex(vertex)
        return (
            self._adj_mat[vertex][self._adj_mat[vertex].isna().map(lambda x: not x)]
            .keys()
            .to_list()
        )

    def draw(self, axis: plt.Axes = None, pos_fn: Callable = None, **kwargs) -> None:
        """Draw this graph using matplotlib

        It takes the graph, turns it into the convention used by networkx by taking the
        adjacency matrix first, and then draws it

        Parameters
        ----------
        axis : matplotlib.pyplot.Axes, optional
            Axis to draw the graph on, by default None. If None, it creates a new figure
            and axis.
        pos_fn : function_, optional
            Function to use to determine the position of the vertices, by default None.
        """
        return draw_graph(self, axis, pos_fn, **kwargs)


def draw_graph(
    graph: Graph, axis: plt.Axes = None, pos_fn: Callable = None, **kwargs
) -> None:
    """Draw a graph using matplotlib

    It takes the graph, turns it into the convention used by networkx by taking the
    adjacency matrix first, and then draws it

    Parameters
    ----------
    graph : watermelon.model.Graph
        Graph to draw
    axis : matplotlib.pyplot.Axes, optional
        Axis to draw the graph on, by default None. If None, it creates a new figure
        and axis.
    pos_fn : function_, optional
        Function to use to determine the position of the vertices, by default None.
    """
    # Parse the included graph data structure into the nx adjacency matrix format
    df = (
        1 - graph.adj_mat.applymap(lambda e: e.weight if not pd.isnull(e) else e).isna()
    )
    df.columns = df.columns.map(lambda c: c.id)
    df.index = df.index.map(lambda c: c.id)
    nx_graph = nx.from_pandas_adjacency(df, nx.DiGraph)

    if pos_fn is not None:
        pos = pos_fn(nx_graph)
    else:
        pos = None

    weights = [
        graph.adj_mat[graph.get_vertex(v)][graph.get_vertex(u)].weight
        for u, v in nx_graph.edges()
    ]
    weights_max = max(weights)
    weights = [
        (1 - w / weights_max, 1 - w / weights_max, 1 - w / weights_max) for w in weights
    ]
    nx.draw_networkx(nx_graph, ax=axis, pos=pos, edge_color=weights, **kwargs)
