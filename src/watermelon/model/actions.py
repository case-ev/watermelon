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

    def tuple(self):
        """Parse into a tuple"""
        return self.vertex, self.action


class VertexAction:
    """Type of action"""

    @staticmethod
    @abc.abstractmethod
    def _char():
        """Unique character that represents an action"""

    @abc.abstractmethod
    def act(self, agent, vertex):
        """Make an agent take this action on a vertex.

        This method returns both the time it takes to do the action and
        the amount of energy required to do it.

        Parameters
        ----------
        agent : watermelon.model.Agent
            Agent that takes the action
        vertex : watermelon.model.Vertex
            Vertex to add to the graph

        Returns
        -------
        time, energy : (float, float)
            Amount of time and energy that it takes to do the action
        """

    @classmethod
    def __repr__(cls):
        return cls.__class__.__name__

    @classmethod
    def __str__(cls):
        return cls._char()


class NullAction(VertexAction):
    """Action for not doing anything"""

    @staticmethod
    def _char():
        return "\u03d5"  # phi

    def act(self, agent, vertex):
        return 0, 0


class ChargeBatteryAction(VertexAction):
    """Action for charging the battery"""

    @staticmethod
    def _char():
        return "c"

    def act(self, agent, vertex):
        return 0, 0


class WaitAction(VertexAction):
    """Action for waiting"""

    @staticmethod
    def _char():
        return "w"

    def act(self, agent, vertex):
        return 0, 0


class LoadMaterialAction(VertexAction):
    """Action for loading material"""

    @staticmethod
    def _char():
        return "x"

    def act(self, agent, vertex):
        return 0, 0
