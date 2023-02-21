"""
examples.simulation1
-------------------------
Example to show how a simulation can be created, which has many agents,
many actions and waiting times.
"""

import matplotlib.pyplot as plt

from watermelon_common.logger import LOGGER
from examples._graphs.toy import ex_graph2
import watermelon as wm
from watermelon.defaults import BATTERY_EFFICIENCY


def main(
    delta=1,
    stop_time=180,
    show=False,
    battery_eff=BATTERY_EFFICIENCY,
    out_file=None,
    save=False,
    uncertainty=None,
    **kwargs,
):
    """Entry point for the example"""

    LOGGER.info("Parsing example arguments")
    delta = float(delta)
    stop_time = float(stop_time)
    battery_eff = float(battery_eff)
    if out_file is None:
        eff_str = f"{battery_eff:.2f}"
        out_file = (
            f"examples/simulation1/results/result-eff={eff_str[:-3]}_{eff_str[-2:]}.csv"
        )

    match uncertainty:
        case "no" | None:
            uncertainty_source = wm.NoUncertainty()
        case "gaussian":
            mean = kwargs.get("mean")
            std = kwargs.get("std")
            uncertainty_kwargs = {}
            if mean is not None:
                uncertainty_kwargs["mean"] = float(mean)
            if std is not None:
                uncertainty_kwargs["std"] = float(std)
            uncertainty_source = wm.GaussianUncertainty(**uncertainty_kwargs)

    LOGGER.info(
        "Using parameters delta=%.2f, stop_time=%.2f, battery_eff=%.2f",
        delta,
        stop_time,
        battery_eff,
    )
    if save:
        LOGGER.info("Output file is %s", out_file)

    LOGGER.info("Creating environment")
    graph = ex_graph2()
    print("Using the following graph")
    print(graph)

    if show:
        _, ax = plt.subplots()
        wm.draw_graph(graph, axis=ax)
        plt.show()

    LOGGER.info("Creating agents")
    agents = _create_agents(graph, uncertainty_source)

    LOGGER.info("Initializing simulation")
    sim = wm.sim.Simulator(graph, agents, delta=delta, battery_eff=battery_eff)
    sim.start(stop_time)

    LOGGER.info("Going into main loop")
    while not sim.should_close:
        sim.update()

    LOGGER.info("Finished simulation, showing results")
    print(sim.data_extractor.data)
    if save:
        LOGGER.info("Saving file to %s", out_file)
        sim.data_extractor.data.to_csv(out_file, index=False)


def _create_agents(graph, uncertainty=None):
    return [
        wm.Agent(
            0,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            1,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            2,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            3,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            4,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            5,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            6,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
        wm.Agent(
            7,
            graph,
            [
                wm.Decision(wm.Vertex(0), wm.NullAction()),
                wm.Decision(wm.Vertex(2), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(7), wm.ChargeBatteryAction()),
                wm.Decision(wm.Vertex(6), wm.LoadMaterialAction()),
                wm.Decision(wm.Vertex(5), wm.NullAction()),
                wm.Decision(wm.Vertex(4), wm.NullAction()),
                wm.Decision(wm.Vertex(3), wm.NullAction()),
                wm.Decision(wm.Vertex(1), wm.DischargeMaterialAction()),
                wm.Decision(wm.Vertex(0), wm.NullAction()),
            ],
            uncertainty=uncertainty,
        ),
    ]
