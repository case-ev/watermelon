"""
watermelon.model.vertex_types
-----------------------------
Types of vertices
"""

import abc

from watermelon.model.vertex_actions import NullAction


class VertexType(abc.ABC):
    """Base interface for a node type."""

    @staticmethod
    @abc.abstractmethod
    def _char():
        pass

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, __o):
        return self.__class__ is __o.__class__

    @classmethod
    def __str__(cls):
        return cls._char()


class EmptyVertexType(VertexType):
    """Empty node."""

    ACTIONS = [NullAction()]

    @staticmethod
    def _char():
        return "\u03b8"  # theta
