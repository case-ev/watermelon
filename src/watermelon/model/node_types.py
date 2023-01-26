from watermelon.model.node_actions import NULL_ACTION


class NodeType:
    """Base interface for a node type."""
    pass


class EMPTY_NODE_TYPE(NodeType):
    """Empty node."""
    ACTIONS = [NULL_ACTION]
