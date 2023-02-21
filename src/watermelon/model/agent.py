"""
watermelon.model.agent
----------------------
Modelling of the agent and its decisions, as well as the actions they can take
on a vertex.
"""

import abc
import dataclasses
from typing import Hashable, List, Tuple, Self

import numpy as np

from watermelon_common.logger import LOGGER

from watermelon.exceptions import ForbiddenActionException
from watermelon.model import types
from watermelon.model.graph import Graph
from watermelon.model.uncertainty import NoUncertainty, UncertaintySource
from watermelon.model.vertex import Vertex
from watermelon.defaults import (
    BATTERY_CAPACITY,
    MATERIAL_CAPACITY,
    BATTERY_EFFICIENCY,
    LEAKAGE_POWER,
)


_MINUTES_PER_HOUR = 60


class VertexAction(abc.ABC):
    """Type of action"""

    @classmethod
    def __repr__(cls) -> str:
        return cls.__class__.__name__

    @classmethod
    def __str__(cls) -> str:
        return cls.char()

    @abc.abstractmethod
    def _act(self, agent: "Agent", vertex: Vertex) -> Tuple[float, float]:
        """Take an action in a vertex"""

    def act(self, agent: "Agent", vertex: Vertex) -> Tuple[float, float]:
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
        if not self.can_act_on(vertex):
            raise ForbiddenActionException(self, vertex.type)
        return self._act(agent, vertex)

    @classmethod
    def can_act_on(cls, vertex: Vertex) -> bool:
        """Indicate whether this action can occur on the vertex"""
        return cls.allowed_types() is None or type(vertex.type) in cls.allowed_types()

    @staticmethod
    @abc.abstractmethod
    def allowed_types():
        """Get the types that this action can act on. If None, it can act on every type"""

    @staticmethod
    @abc.abstractmethod
    def char() -> str:
        """Unique character that represents an action"""


@dataclasses.dataclass
class Decision:
    """Decision containing an action and a tuple"""

    vertex: Vertex
    action: VertexAction

    def __str__(self) -> str:
        return f"({str(self.vertex)}, {str(self.action)})"

    def tuple(self) -> Tuple[Vertex, VertexAction]:
        """Parse into a tuple (vertex, action)"""
        return self.vertex, self.action


@dataclasses.dataclass
class AgentState:
    """State of an agent at an instant"""

    vertex: Vertex = None
    action: VertexAction = None
    _soc: float = 1
    payload: float = 0
    current_action: int = 0
    action_time: float = 0
    finished_action: bool = False
    is_waiting: bool = False
    is_done: bool = False
    is_travelling: Tuple[bool, Vertex, Vertex] = (False, None, None)
    just_arrived: bool = False
    out_of_charge: bool = False
    overcharged: bool = False

    @property
    def soc(self) -> float:
        """True state of charge. In reality this would be unobtainable, but it
        is left as available for simulation purposes.
        """
        return self._soc

    @soc.setter
    def soc(self, val: float) -> None:
        self._soc = val
        if self._soc <= 0:
            self._soc = 0
            self.out_of_charge = True
        elif self._soc > 1:
            self.overcharged = True
        else:
            self.out_of_charge = False
            self.overcharged = False

    def copy(self) -> Self:
        """Create a copy of itself"""
        return dataclasses.replace(self)


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

    def energy_as_soc(
        self, energy: float, battery_efficiency: float = BATTERY_EFFICIENCY
    ) -> float:
        """Interpret some given amount of energy as SoC"""
        return energy / (battery_efficiency * self.battery_capacity)

    def insert_energy(
        self, energy_delta: float, battery_efficiency: float = BATTERY_EFFICIENCY
    ) -> None:
        """Insert/remove a given amount of energy from the battery"""
        self.state.soc += self.energy_as_soc(energy_delta, battery_efficiency)

    @property
    def soc(self) -> float:
        """State of charge of the agent"""
        return np.clip(self.state.soc + self.uncertainty.sample(), 0, 1)

    @soc.setter
    def soc(self, val: float) -> None:
        self.state.soc = val + self.uncertainty.sample()


###############################################################################
# |=============================| Actions |=================================| #
###############################################################################


class NullAction(VertexAction):
    """Action for not doing anything"""

    @staticmethod
    def allowed_types():
        return None

    @staticmethod
    def char() -> str:
        return "\u03d5"  # phi

    def _act(self, agent: Agent, vertex: Vertex) -> Tuple[float, float]:
        return 0, 0


class ChargeBatteryAction(VertexAction):
    """Action for charging the battery"""

    def __init__(
        self, limit: float = 0.8, battery_eff: float = BATTERY_EFFICIENCY
    ) -> None:
        """Charge the battery.

        The specified battery efficiency indicates which percentage of
        the energy given by the battery is used as mechanical work to
        travel the graph.

        Parameters
        ----------
        limit : float, optional
            State of charged to be reached, by default 0.8
        battery_eff : float, optional
            Efficiency of the battery, by default BATTERY_EFFICIENCY
        """
        self.limit = limit
        self.battery_eff = battery_eff

    @staticmethod
    def allowed_types():
        return [types.EmptyVertexType, types.EVChargerType]

    @staticmethod
    def char() -> str:
        return "c"

    def _act(self, agent: Agent, vertex: Vertex) -> Tuple[float, float]:
        if agent.soc >= self.limit:
            return 0, 0
        energy = (self.limit - agent.soc) * self.battery_eff * agent.battery_capacity
        time = _MINUTES_PER_HOUR * energy / vertex.type.charge_power
        return time, energy


class WaitAction(VertexAction):
    """Action for waiting"""

    def __init__(self, time: float = 0) -> None:
        """Wait for the given amount of time"""
        self.time = time

    @staticmethod
    def allowed_types():
        return None

    @staticmethod
    def char() -> str:
        return "w"

    def _act(self, agent: Agent, vertex: Vertex) -> Tuple[float, float]:
        energy = LEAKAGE_POWER * self.time / _MINUTES_PER_HOUR
        return self.time, -energy


class LoadMaterialAction(VertexAction):
    """Action for loading material"""

    def __init__(self, limit: float = 1, material: float = None) -> None:
        """Make the agent load material.

        Parameters
        ----------
        limit : float, 0 <= limit <= 1, optional
            Payload limit as a proportion, by default 1
        material : float, optional
            Amount of material to be loaded in kg, by default None. If
            it is specified, it overrides the value given by limit.
        """
        self.limit = limit
        self.material = material

    @staticmethod
    def allowed_types():
        return [types.EmptyVertexType, types.MaterialLoadType]

    @staticmethod
    def char() -> str:
        return "x"

    def _act(self, agent: Agent, vertex: Vertex) -> Tuple[float, float]:
        if agent.state.payload >= self.limit:
            return 0, 0
        if self.material is None:
            material = (self.limit - agent.state.payload) * agent.material_capacity
        else:
            material = self.material
        time = material / vertex.type.load_rate

        leakage_energy = LEAKAGE_POWER * time / _MINUTES_PER_HOUR
        action_energy = 0
        energy = leakage_energy + action_energy
        LOGGER.info(
            "%s Loading %.0f kg (%.0f Wh, %.0f minutes) at %s",
            agent,
            material,
            energy,
            time,
            vertex,
        )
        return time, -energy


class DischargeMaterialAction(VertexAction):
    """Action for discharging material"""

    def __init__(self, limit: float = 0, material: float = None) -> None:
        """Make the agent discharge material.

        Parameters
        ----------
        limit : float, 0 <= limit <= 1, optional
            Payload limit as a proportion, by default 1
        material : float, optional
            Amount of material to be discharged in kg, by default None. If
            it is specified, it overrides the value given by limit.
        """
        self.limit = limit
        self.material = material

    @staticmethod
    def allowed_types():
        return [types.EmptyVertexType, types.MaterialDischargeType]

    @staticmethod
    def char() -> str:
        return "o"

    def _act(self, agent: Agent, vertex: Vertex) -> Tuple[float, float]:
        if agent.state.payload <= self.limit:
            return 0, 0
        if self.material is None:
            material = (agent.state.payload - self.limit) * agent.material_capacity
        else:
            material = self.material
        time = material / vertex.type.load_rate

        leakage_energy = LEAKAGE_POWER * time / _MINUTES_PER_HOUR
        action_energy = 0
        energy = leakage_energy + action_energy
        LOGGER.info(
            "%s Discharging %.0f kg (%.0f Wh, %.0f minutes) at %s",
            agent,
            material,
            energy,
            time,
            vertex,
        )
        return time, -energy
