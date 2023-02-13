"""
examples.basic_simulation
-------------------------
Example to show how a basic simulation can be created.
"""

from watermelon_common.logger import LOGGER
from examples._graphs.toy import ex_graph1
import watermelon as wm


def main(delta=1e-3):
    """Entry point for the example"""

    LOGGER.info("Parsing example arguments")
    delta = float(delta)

    LOGGER.info("Creating environment")
    graph = ex_graph1()

    LOGGER.info("Creating agents")
    agents = [
        wm.Agent(i, graph, [wm.Decision(wm.Vertex(0), wm.NullAction())])
        for i in range(2)
    ]

    LOGGER.info("Initializing simulation")
    sim = wm.sim.Simulator(graph, agents, delta=delta)
    sim.start(1)

    LOGGER.info("Going into main loop")
    while not sim.should_close:
        sim.update()

    LOGGER.info("Finished simulation, showing results")
    print(sim.data_extractor.data)
