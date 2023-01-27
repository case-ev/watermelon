from watermelon.model.vertex_types import EMPTY_VERTEX_TYPE
from watermelon_common.logger import LOGGER


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
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def register_vertex(self, vertex):
        self.vertices.add(vertex)

    def register_edge(self, edge):
        if self.vertices.get(edge.origin) is None:
            LOGGER.warning(f"Vertex {edge.origin} was not found. Registering it")
            self.register_vertex(edge.origin)
        if self.vertices.get(edge.target) is None:
            LOGGER.warning(f"Vertex {edge.target} was not found. Registering it")
            self.register_vertex(edge.target)

        if self.edges.get(edge.origin, edge.target) is None:
            self.edges[(edge.origin, edge.target)] = [edge]
        else:
            self.edges[(edge.origin, edge.target)].append(edge)

    def get_edge(self, origin, target):
        return self.edges.get((origin, target))
