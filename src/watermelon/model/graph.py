from watermelon.model.vertex_types import EMPTY_VERTEX_TYPE


class Vertex:
    def __init__(self, identifier, vertex_type=EMPTY_VERTEX_TYPE):
        self.id = identifier
        self.id_hash = hash(identifier)
        self.type = vertex_type
