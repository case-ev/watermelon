"""
watermelon.model.agent
----------------------
Modelling of the agent and its decisions.
"""

from typing import Hashable, List

import numpy as np

from watermelon.model.graph import Graph
from watermelon.model.state import AgentState
from watermelon.model.uncertainty import NoUncertainty, UncertaintySource
from watermelon.model.vertex import Decision
from watermelon.defaults import BATTERY_CAPACITY, MATERIAL_CAPACITY, BATTERY_EFFICIENCY


class AgentMetaClass(type):
    """Metaclass to allow Agent singletons, defined by their identifier"""

    _instances = {}

    def __call__(cls, identifier: Hashable, *args, **kwargs) -> None:
        id_hash = hash(identifier)
        if id_hash not in cls._instances:
            instance = super().__call__(identifier, *args, **kwargs)
            cls._instances[id_hash] = instance
        return cls._instances[id_hash]


class Agent(metaclass=AgentMetaClass):
    """Agent in a graph."""

    def __init__(
        self,
        identifier: Hashable,
        graph: Graph = None,
        actions: List[Decision] = None,
        *,
        uncertainty: UncertaintySource = None,
        initial_state: AgentState = None,
        battery_capacity: float = BATTERY_CAPACITY,
        material_capacity: float = MATERIAL_CAPACITY,
    ) -> None:
        self._id = identifier
        self._id_hash = hash(identifier)
        self.graph = graph
        self.battery_capacity = battery_capacity
        self.material_capacity = material_capacity
        self.uncertainty = NoUncertainty() if uncertainty is None else uncertainty
        self.state = AgentState() if initial_state is None else initial_state
        self.actions = [] if actions is None else actions

    def __hash__(self) -> None:
        return self.hash

    def __eq__(self, __o: object) -> bool:
        return (
            hash(self) == hash(__o)
            and self.graph == __o.graph
            and self.actions == __o.actions
            and isinstance(__o, self.__class__)
        )

    def __repr__(self) -> str:
        return f"Agent({repr(self.id)})"

    def __str__(self) -> str:
        return f"Agent({str(self.id)})"

    @property
    def id(self) -> Hashable:
        """Unique ID of the agent."""
        return self._id

    @property
    def hash(self) -> int:
        """Hash of the unique ID of the agent."""
        return self._id_hash

    def insert_energy(self, energy_delta: float, battery_efficiency: float = BATTERY_EFFICIENCY) -> None:
        """Insert/remove a given amount of energy from the battery"""
        self.state.soc += energy_delta / (
            battery_efficiency * self.battery_capacity
        )

    @property
    def soc(self) -> float:
        """State of charge of the agent"""
        return np.clip(self.state.soc + self.uncertainty.sample(), 0, 1)

    @soc.setter
    def soc(self, val: float) -> None:
        self.state.soc = val + self.uncertainty.sample()
