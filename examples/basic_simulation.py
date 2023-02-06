import watermelon as wm
from watermelon_common.logger import LOGGER


def main(delta=1e-3):
    LOGGER.info("Parsing example arguments")
    delta = float(delta)

    LOGGER.info("Creating environment")
    graph = wm.Graph()

    verts = [wm.Vertex(i) for i in range(5)]
    graph.add_vertices(verts)
    graph.add_edges(
        [
            wm.Edge(wm.Vertex(0), wm.Vertex(1), 10),
            wm.Edge(wm.Vertex(1), wm.Vertex(0), 4),
            wm.Edge(wm.Vertex(0), wm.Vertex(2), 3),
            wm.Edge(wm.Vertex(2), wm.Vertex(1), 2),
            wm.Edge(wm.Vertex(2), wm.Vertex(4), 6),
            wm.Edge(wm.Vertex(4), wm.Vertex(2), 2),
            wm.Edge(wm.Vertex(4), wm.Vertex(3), 7),
            wm.Edge(wm.Vertex(3), wm.Vertex(1), 2),
        ]
    )

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
