from watermelon.model import Edge, Graph, Vertex, EMPTY_VERTEX_TYPE
from watermelon_common.logger import LOGGER


def main():
    LOGGER.info("Creating vertices")
    verts = [Vertex(i) for i in range(5)]

    LOGGER.info("Initializing graph")
    graph = Graph()
    graph.add_vertices(verts)
    print(graph)

    LOGGER.info("Creating edges")
    graph.add_edges([
        Edge(Vertex(0), Vertex(1), 10),
        Edge(Vertex(1), Vertex(0), 4),
        Edge(Vertex(0), Vertex(2), 3),
        Edge(Vertex(2), Vertex(1), 2),
        Edge(Vertex(2), Vertex(4), 6),
        Edge(Vertex(4), Vertex(2), 2),
        Edge(Vertex(4), Vertex(3), 7),
        Edge(Vertex(3), Vertex(1), 2),
    ])


if __name__ == "__main__":
    main()
