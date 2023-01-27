from watermelon.model.vertex_actions import NULL_ACTION


class VertexType:
    """Base interface for a node type."""
    pass


class EMPTY_VERTEX_TYPE(VertexType):
    """Empty node."""
    ACTIONS = [NULL_ACTION]
