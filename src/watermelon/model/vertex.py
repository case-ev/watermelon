"""
watermelon.model.vertex
-----------------------
Definition of a vertex in the graph.
"""

from watermelon.model.types import EmptyVertexType


class Vertex:
    """Vertex of a graph, which has a certain type and identifier

    The identifier must be a hashable type, and if the type is omitted
    then it is assumed to be an empty vertex
    """

    def __init__(self, identifier, vertex_type=EmptyVertexType()):
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
