import abc
from watermelon.model.vertex_actions import NULL_ACTION


class VertexType(abc.ABC):
    """Base interface for a node type."""
    @abc.abstractstaticmethod
    def _char(self): pass

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self._char()


class EMPTY_VERTEX_TYPE(VertexType):
    """Empty node."""
    ACTIONS = [NULL_ACTION]

    @staticmethod
    def _char(self):
        return "\u03b1"
