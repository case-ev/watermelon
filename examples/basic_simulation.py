from watermelon.sim.simulator import Simulator
from watermelon.model import Agent, Graph, Vertex, Edge, NULL_ACTION, Decision
from watermelon_common.logger import LOGGER


def main(delta=1e-3):
    LOGGER.info("Parsing example arguments")
    delta = float(delta)

    LOGGER.info("Creating environment")
    graph = Graph()

    verts = [Vertex(i) for i in range(5)]
    graph.add_vertices(verts)
    graph.add_edges(
        [
            Edge(Vertex(0), Vertex(1), 10),
            Edge(Vertex(1), Vertex(0), 4),
            Edge(Vertex(0), Vertex(2), 3),
            Edge(Vertex(2), Vertex(1), 2),
            Edge(Vertex(2), Vertex(4), 6),
            Edge(Vertex(4), Vertex(2), 2),
            Edge(Vertex(4), Vertex(3), 7),
            Edge(Vertex(3), Vertex(1), 2),
        ]
    )

    LOGGER.info("Creating agents")
    agents = [Agent(i, graph, [Decision(Vertex(0), NULL_ACTION)]) for i in range(2)]

    LOGGER.info("Initializing simulation")
    sim = Simulator(graph, agents, delta)
    sim.start()

    LOGGER.info("Going into main loop")
    while sim.time <= 1:
        sim.update()

    LOGGER.info("Finished simulation, showing results")
    print(sim.data_extractor.data)
