"""
watermelon.model.agent
----------------------
Modelling of the agent and its decisions.
"""

import numpy as np

from watermelon.model.state import AgentState
from watermelon.model.uncertainty import NoUncertainty
from watermelon.defaults import BATTERY_CAPACITY, MATERIAL_CAPACITY, BATTERY_EFFICIENCY


class AgentMetaClass(type):
    """Metaclass to allow Agent singletons, defined by their identifier"""

    _instances = {}

    def __call__(cls, identifier, *args, **kwargs):
        id_hash = hash(identifier)
        if id_hash not in cls._instances:
            instance = super().__call__(identifier, *args, **kwargs)
            cls._instances[id_hash] = instance
        return cls._instances[id_hash]


class Agent(metaclass=AgentMetaClass):
    """Agent in a graph."""

    def __init__(
        self,
        identifier,
        graph=None,
        actions=None,
        *,
        uncertainty=None,
        initial_state=None,
        battery_capacity=BATTERY_CAPACITY,
        material_capacity=MATERIAL_CAPACITY,
    ):
        self._id = identifier
        self._id_hash = hash(identifier)
        self.graph = graph
        self.battery_capacity = battery_capacity
        self.material_capacity = material_capacity
        self.uncertainty = NoUncertainty() if uncertainty is None else uncertainty
        self.state = AgentState() if initial_state is None else initial_state

        # Each element in `actions` is a 2-tuple of a vertex
        # and an action.
        self.actions = [] if actions is None else actions

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

    def insert_energy(self, energy_delta, battery_efficiency=BATTERY_EFFICIENCY):
        """Insert/remove a given amount of energy from the battery"""
        self.state.soc += energy_delta / (
            battery_efficiency * self.battery_capacity
        )

    @property
    def soc(self):
        """State of charge of the agent"""
        return np.clip(self.state.soc + self.uncertainty.sample(), 0, 1)

    @soc.setter
    def soc(self, val):
        self.state.soc = val + self.uncertainty.sample()
