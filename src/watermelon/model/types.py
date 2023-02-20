"""
watermelon.model.types
----------------------
Types of vertices there are.
"""

import abc


class VertexType(abc.ABC):
    """Base interface for a node type"""

    def __repr__(self) -> str:
        return self.__class__.__name__

    def __eq__(self, __o) -> bool:
        return self.__class__ is __o.__class__

    @classmethod
    def __str__(cls) -> str:
        return cls.char()

    @staticmethod
    @abc.abstractmethod
    def char() -> str:
        """Get the identifying character"""


class EmptyVertexType(VertexType):
    """Empty node"""

    @staticmethod
    def char() -> str:
        return "\u0398"  # theta


class EVChargerType(VertexType):
    """Charger for electric vehicles"""

    def __init__(self, charge_power: float) -> None:
        self._charge_power = charge_power

    @staticmethod
    def char() -> str:
        return "C"

    @property
    def charge_power(self) -> float:
        """Power with which the EV charges"""
        return self._charge_power


class MaterialLoadType(VertexType):
    """Load material"""

    def __init__(self, load_rate: float) -> None:
        self._load_rate = load_rate

    @staticmethod
    def char() -> str:
        return "X"

    @property
    def load_rate(self) -> float:
        """Rate in kg/minute at which material is loaded"""
        return self._load_rate


class MaterialDischargeType(VertexType):
    """Discharge material"""

    def __init__(self, discharge_rate: float) -> None:
        self._discharge_rate = discharge_rate

    @staticmethod
    def char() -> str:
        return "O"

    @property
    def discharge_rate(self) -> float:
        """Rate in kg/minute at which material is discharged"""
        return self._discharge_rate
