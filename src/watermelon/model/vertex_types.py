from watermelon.model.vertex_actions import NULL_ACTION


class VertexType:
    """Base interface for a vertex type."""
    pass


class EMPTY_VERTEX_TYPE(VertexType):
    """Empty vertex."""
    ACTIONS = [NULL_ACTION]
