import watermelon as wm
from watermelon_common.logger import LOGGER
from examples._graphs.toy import ex_graph1


def main(delta=1e-3):
    LOGGER.info("Parsing example arguments")
    delta = float(delta)

    LOGGER.info("Creating environment")
    graph = ex_graph1()

    LOGGER.info("Creating agents")
    agents = [
        wm.Agent(i, graph, [wm.Decision(wm.Vertex(0), wm.NULL_ACTION)])
        for i in range(2)
    ]

    LOGGER.info("Initializing simulation")
    sim = wm.sim.Simulator(graph, agents, delta=delta)
    sim.start()

    LOGGER.info("Going into main loop")
    while sim.time <= 1:
        sim.update()

    LOGGER.info("Finished simulation, showing results")
    print(sim.data_extractor.data)
