from watermelon.model.vertex_types import EMPTY_VERTEX_TYPE


class Edge:
    def __init__(self, origin, target, weight=0):
        self.origin = origin
        self.target = target
        self.weight = weight


class Vertex:
    def __init__(self, identifier, vertex_type=EMPTY_VERTEX_TYPE):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.type = vertex_type
        self.in_verts = []
        self.out_verts = []

    @property
    def id(self):
        return self._id
