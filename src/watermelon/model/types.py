"""
watermelon.model.vertex_types
-----------------------------
Types of vertices
"""

import abc

import watermelon.model.actions as actions


class VertexType(abc.ABC):
    """Base interface for a node type"""

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
    """Empty node"""

    ACTIONS = [actions.NullAction(), actions.WaitAction()]

    @staticmethod
    def _char():
        return "\u03b8"  # theta


class EVChargerType(VertexType):
    """Charger for electric vehicles"""

    ACTIONS = [actions.ChargeBatteryAction(), actions.NullAction(), actions.WaitAction()]

    def __init__(self, charge_power):
        self._charge_power = charge_power

    @staticmethod
    def _char():
        return "C"

    @property
    def charge_power(self):
        """Power with which the EV charges"""
        return self._charge_power


class MaterialLoadType(VertexType):
    """Load material"""

    ACTIONS = [actions.LoadMaterialAction(), actions.NullAction(), actions.WaitAction()]

    def __init__(self, load_rate):
        self._load_rate = load_rate

    @staticmethod
    def _char():
        return "X"

    @property
    def load_rate(self):
        """Rate at which material is loaded"""
        return self._load_rate


class MaterialDischargeType(VertexType):
    """Discharge material"""

    ACTIONS = [actions.DischargeMaterialAction(), actions.NullAction(), actions.WaitAction()]

    def __init__(self, discharge_rate):
        self._discharge_rate = discharge_rate

    @staticmethod
    def _char():
        return "O"

    @property
    def discharge_rate(self):
        """Rate at which material is discharged"""
        return self._discharge_rate
