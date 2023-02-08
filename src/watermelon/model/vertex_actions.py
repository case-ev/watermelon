"""
watermelon.model.vertex_actions
-------------------------------
Types of actions that the agents can take
"""

import abc


class Decision:
    """Decision containing an action and a tuple"""

    def __init__(self, vertex, action):
        self.vertex = vertex
        self.action = action

    def __repr__(self):
        return f"Decision({repr(self.vertex)}, {repr(self.action)})"

    def __str__(self):
        return f"({str(self.vertex)}, {str(self.action)})"


class VertexAction:
    """Type of action"""

    @staticmethod
    @abc.abstractmethod
    def _char():
        pass

    @classmethod
    def __repr__(cls):
        return cls.__class__.__name__

    @classmethod
    def __str__(cls):
        return cls._char()


class NullAction(VertexAction):
    """Action that represents not doing anything"""

    @staticmethod
    def _char():
        return "\u03d5"  # phi
