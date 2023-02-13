"""
examples.simulation1
-------------------------
Example to show how a simulation can be created, which has many agents,
many actions and waiting times.
"""

from watermelon_common.logger import LOGGER
from examples._graphs.toy import ex_graph2
import watermelon as wm


def main(delta=1, stop_time=180):
    """Entry point for the example"""

    LOGGER.info("Parsing example arguments")
    delta = float(delta)
    stop_time = float(stop_time)

    LOGGER.info("Creating environment")
    graph = ex_graph2()
    print("Using the following graph")
    print(graph)

    LOGGER.info("Creating agents")
    agents = [
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
        ),
    ]

    LOGGER.info("Initializing simulation")
    sim = wm.sim.Simulator(graph, agents, delta=delta)
    sim.start(stop_time)

    LOGGER.info("Going into main loop")
    while not sim.should_close:
        sim.update()

    LOGGER.info("Finished simulation, showing results")
    print(sim.data_extractor.data)
    sim.data_extractor.data.to_csv("examples/simulation1/result.csv")
