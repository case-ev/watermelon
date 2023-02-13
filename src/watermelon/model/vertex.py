"""
watermelon.model.vertex
-----------------------
Definition of a vertex in the graph.
"""

from watermelon.model.types import EmptyVertexType


class VertexMetaClass(type):
    """Metaclass to allow Vertex singletons, defined by their identifier"""

    _instances = {}

    def __call__(cls, identifier, *args, **kwargs):
        id_hash = hash(identifier)
        if id_hash not in cls._instances:
            instance = super().__call__(identifier, *args, **kwargs)
            cls._instances[id_hash] = instance
        return cls._instances[id_hash]


class Vertex(metaclass=VertexMetaClass):
    """Vertex of a graph, which has a certain type and identifier

    The identifier must be a hashable type, and if the type is omitted
    then it is assumed to be an empty vertex
    """

    def __init__(self, identifier, capacity=None, vertex_type=EmptyVertexType()):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.type = vertex_type
        self.members = set()
        self.capacity = float("inf") if capacity is None else capacity

    def __hash__(self):
        return self.hash

    def __eq__(self, __o):
        return (
            hash(self) == hash(__o)
            and self.type == __o.type
            and isinstance(__o, self.__class__)
        )

    def __repr__(self):
        return f"Vertex(identifier={repr(self.id)}, vertex_type={repr(self.type)})"

    def __str__(self):
        return f"{str(self.type)}({str(self.id)})"

    @property
    def id(self):
        """Unique ID of the vertex"""
        return self._id

    @property
    def hash(self):
        """Hash of the unique ID of the vertex"""
        return self._id_hash
