import abc
from watermelon.model.vertex_actions import NULL_ACTION


class VertexType(abc.ABC):
    """Base interface for a node type."""

    @abc.abstractstaticmethod
    def _char():
        pass

    @classmethod
    def __str__(cls):
        return cls._char()


class __EmptyVertexType(VertexType):
    """Empty node."""

    ACTIONS = [NULL_ACTION]

    @staticmethod
    def __repr__():
        return "EMPTY_VERTEX_TYPE"

    @staticmethod
    def _char():
        return "\u03b8"  # theta


EMPTY_VERTEX_TYPE = __EmptyVertexType()
