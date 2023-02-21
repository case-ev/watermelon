"""
watermelon.sim.simulation_variables
-----------------------------------
Variables used by the simulation.
"""

from watermelon.defaults import BATTERY_EFFICIENCY


class SimulationParameters:
    """Parameters for the simulation"""

    def __init__(self, *, battery_eff: float = BATTERY_EFFICIENCY, **_) -> None:
        self.battery_eff = battery_eff


class SimulationControl:
    """Control variables for the simulation"""

    def __init__(
        self,
        *,
        time: float = 0.0,
        delta: float = 1e-3,
        iteration: int = 0,
        should_close: bool = False,
        stop_time: float = 0.0,
        **_,
    ) -> None:
        self.time = time
        self.delta = delta
        self.iteration = iteration
        self.should_close = should_close
        self.stop_time = stop_time
