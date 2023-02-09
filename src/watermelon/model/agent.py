"""
watermelon.model.agent
----------------------
Modelling of the agent and its decisions.
"""

from watermelon.model.state import AgentState


DEFAULT_BATTERY_CAPACITY = 1000


class Agent:
    """Agent in a graph."""

    def __init__(
        self,
        identifier,
        graph,
        actions=None,
        *,
        initial_state=AgentState(),
        battery_capacity=None,
    ):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.graph = graph
        self.state = initial_state

        if battery_capacity is None:
            self.battery_capacity = DEFAULT_BATTERY_CAPACITY
        else:
            self.battery_capacity = battery_capacity

        # Each element in `actions` is a 2-tuple of a vertex
        # and an action.
        if actions is None:
            self.actions = []
        else:
            self.actions = actions

        self.current_action = 0
        self.finished_action = False
        self.is_waiting = False
        self.is_done = False

    def __hash__(self):
        return self.hash

    def __eq__(self, __o):
        return (
            hash(self) == hash(__o)
            and self.graph == __o.graph
            and self.actions == __o.actions
            and isinstance(__o, self.__class__)
        )

    def __repr__(self):
        return f"Agent({repr(self.id)})"

    def __str__(self):
        return f"Agent({str(self.id)})"

    @property
    def id(self):
        """Unique ID of the agent."""
        return self._id

    @property
    def hash(self):
        """Hash of the unique ID of the agent."""
        return self._id_hash
