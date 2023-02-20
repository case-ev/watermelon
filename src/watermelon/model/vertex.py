"""
watermelon.model.vertex
-----------------------
Definition of a vertex in the graph, as well as the types of vertices and
the possible actions you can take in them.
"""

import abc
import dataclasses

from watermelon_common.logger import LOGGER
from watermelon.defaults import BATTERY_EFFICIENCY, LEAKAGE_POWER
from watermelon.exceptions import ForbiddenActionException


_MINUTES_PER_HOUR = 60


class VertexAction(abc.ABC):
    """Type of action"""

    @staticmethod
    @abc.abstractmethod
    def _char():
        """Unique character that represents an action"""

    @abc.abstractmethod
    def _act(self, agent, vertex):
        """Take an action in a vertex"""

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
        if self.__class__ not in vertex.type.ACTIONS:
            raise ForbiddenActionException(self, vertex.type)
        return self._act(agent, vertex)

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

    def _act(self, agent, vertex):
        return 0, 0


class ChargeBatteryAction(VertexAction):
    """Action for charging the battery"""

    def __init__(self, limit=0.8, battery_eff=BATTERY_EFFICIENCY):
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
    def _char():
        return "c"

    def _act(self, agent, vertex):
        if agent.soc >= self.limit:
            return 0, 0
        energy = (self.limit - agent.soc) * self.battery_eff * agent.battery_capacity
        time = _MINUTES_PER_HOUR * energy / vertex.type.charge_power
        LOGGER.info(
            "%s charging %.0f Wh (%.0f minutes) at %s", agent, energy, time, vertex
        )
        return time, energy


class WaitAction(VertexAction):
    """Action for waiting"""

    def __init__(self, time=0):
        """Wait for the given amount of time"""
        self.time = time

    @staticmethod
    def _char():
        return "w"

    def _act(self, agent, vertex):
        energy = LEAKAGE_POWER * self.time / _MINUTES_PER_HOUR
        return self.time, -energy


class LoadMaterialAction(VertexAction):
    """Action for loading material"""

    def __init__(self, limit=1, material=None):
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
    def _char():
        return "x"

    def _act(self, agent, vertex):
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

    def __init__(self, limit=0, material=None):
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
    def _char():
        return "o"

    def _act(self, agent, vertex):
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


class VertexType(abc.ABC):
    """Base interface for a node type"""

    @staticmethod
    @abc.abstractmethod
    def _char() -> str:
        pass

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, __o) -> bool:
        return self.__class__ is __o.__class__

    @classmethod
    def __str__(cls) -> str:
        return cls._char()


class EmptyVertexType(VertexType):
    """Empty node"""

    ACTIONS = [NullAction, WaitAction]

    @staticmethod
    def _char() -> str:
        return "\u03b8"  # theta


class EVChargerType(VertexType):
    """Charger for electric vehicles"""

    ACTIONS = [ChargeBatteryAction, NullAction, WaitAction]

    def __init__(self, charge_power) -> None:
        self._charge_power = charge_power

    @staticmethod
    def _char() -> str:
        return "C"

    @property
    def charge_power(self) -> float:
        """Power with which the EV charges"""
        return self._charge_power


class MaterialLoadType(VertexType):
    """Load material"""

    ACTIONS = [LoadMaterialAction, NullAction, WaitAction]

    def __init__(self, load_rate) -> None:
        self._load_rate = load_rate

    @staticmethod
    def _char() -> str:
        return "X"

    @property
    def load_rate(self) -> float:
        """Rate in kg/minute at which material is loaded"""
        return self._load_rate


class MaterialDischargeType(VertexType):
    """Discharge material"""

    ACTIONS = [DischargeMaterialAction, NullAction, WaitAction]

    def __init__(self, discharge_rate) -> None:
        self._discharge_rate = discharge_rate

    @staticmethod
    def _char() -> str:
        return "O"

    @property
    def discharge_rate(self) -> float:
        """Rate in kg/minute at which material is discharged"""
        return self._discharge_rate


class VertexMetaClass(type):
    """Metaclass to allow Vertex singletons, defined by their identifier"""

    _instances = {}

    def __call__(cls, identifier: object, *args, **kwargs):
        id_hash = hash(identifier)
        if id_hash not in cls._instances:
            instance = super().__call__(identifier, *args, **kwargs)
            cls._instances[id_hash] = instance
        return cls._instances[id_hash]


class Vertex(metaclass=VertexMetaClass):
    """Vertex of a graph, which has a certain type and identifier

    The identifier must be a hashable type, and if the type is omitted
    then it is assumed to be an empty vertex
    """

    def __init__(
        self, identifier: object, capacity: int = None, vertex_type: VertexType = None
    ) -> None:
        self._id = identifier
        self._id_hash = hash(identifier)
        self.type = EmptyVertexType() if vertex_type is None else vertex_type
        self.members = set()
        self.capacity = float("inf") if capacity is None else capacity

    def __hash__(self) -> int:
        return self.hash

    def __eq__(self, __o: object) -> bool:
        return (
            hash(self) == hash(__o)
            and self.type == __o.type
            and isinstance(__o, self.__class__)
        )

    def __repr__(self) -> str:
        return f"Vertex(identifier={repr(self.id)}, vertex_type={repr(self.type)})"

    def __str__(self) -> str:
        return f"{str(self.type)}({str(self.id)})"

    @property
    def id(self) -> object:
        """Unique ID of the vertex"""
        return self._id

    @property
    def hash(self) -> int:
        """Hash of the unique ID of the vertex"""
        return self._id_hash


@dataclasses.dataclass
class Decision:
    """Decision containing an action and a tuple"""

    vertex: Vertex
    action: VertexAction

    def __str__(self) -> str:
        return f"({str(self.vertex)}, {str(self.action)})"

    def tuple(self) -> tuple:
        """Parse into a tuple"""
        return self.vertex, self.action
