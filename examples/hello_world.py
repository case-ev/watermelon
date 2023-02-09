"""
examples.hello_world
-------------------------
Example to show the creation of a basic graph.
"""

import matplotlib.pyplot as plt

from watermelon_common.logger import LOGGER
import watermelon as wm


def main():
    """Entry point for the example"""

    LOGGER.info("Creating vertices")
    verts = [wm.Vertex(i) for i in range(5)]

    LOGGER.info("Initializing graph")
    graph = wm.Graph()
    graph.add_vertices(verts)
    print("Graph without edges")
    print(graph)

    LOGGER.info("Creating edges")
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
    print("\nGraph with edges")
    print(graph)

    LOGGER.info("Drawing graph")
    fig, ax = plt.subplots()
    wm.draw_graph(graph, axis=ax)

    fig.suptitle("Hello World!")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")

    plt.show()


if __name__ == "__main__":
    main()
