"""
watermelon.model.vertex
-----------------------
Definition of a vertex in the graph.
"""

from typing import Hashable

from watermelon.model.types import EmptyVertexType, VertexType


class VertexMetaClass(type):
    """Metaclass to allow Vertex singletons, defined by their identifier"""

    _instances = {}

    def __call__(cls, identifier: Hashable, *args, **kwargs):
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

    def __init__(
        self, identifier: Hashable, capacity: int = None, vertex_type: VertexType = None
    ) -> None:
        self._id = identifier
        self._id_hash = hash(identifier)
        self.type = EmptyVertexType() if vertex_type is None else vertex_type
        self.members = set()
        self.capacity = float("inf") if capacity is None else capacity

    def __hash__(self) -> int:
        return self.hash

    def __eq__(self, __o: Hashable) -> bool:
        return (
            hash(self) == hash(__o)
            and self.type == __o.type
            and isinstance(__o, self.__class__)
        )

    def __repr__(self) -> str:
        return f"Vertex(identifier={repr(self.id)}, vertex_type={repr(self.type)})"

    def __str__(self) -> str:
        return f"{str(self.type)}({str(self.id)})"

    @property
    def id(self) -> Hashable:
        """Unique ID of the vertex"""
        return self._id

    @property
    def hash(self) -> int:
        """Hash of the unique ID of the vertex"""
        return self._id_hash
