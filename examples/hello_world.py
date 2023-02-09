"""
examples.hello_world
-------------------------
Example to show the creation of a basic graph.
"""

import matplotlib.pyplot as plt

from watermelon_common.logger import LOGGER
from watermelon.model import Edge, Graph, Vertex, draw_graph


def main():
    """Entry point for the example"""

    LOGGER.info("Creating vertices")
    verts = [Vertex(i) for i in range(5)]

    LOGGER.info("Initializing graph")
    graph = Graph()
    graph.add_vertices(verts)
    print("Graph without edges")
    print(graph)

    LOGGER.info("Creating edges")
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
    print("\nGraph with edges")
    print(graph)

    LOGGER.info("Drawing graph")
    fig, ax = plt.subplots()
    draw_graph(graph, axis=ax)

    fig.suptitle("Hello World!")
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")

    plt.show()


if __name__ == "__main__":
    main()
