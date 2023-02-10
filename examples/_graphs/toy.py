"""
examples._graphs.toy
--------------------
Toy graphs which are created with arbitrary parameters to show some
functionality of watermelon.
"""

import watermelon as wm


def ex_graph1():
    """Create graph1"""
    return (
        wm.Graph()
        .add_vertices([wm.Vertex(i) for i in range(5)])
        .add_edges(
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
    )


def ex_graph2():
    """Create graph2"""
    return (
        wm.Graph()
        .add_vertices(
            [
                wm.Vertex(0),
                wm.Vertex(1, 10, wm.MaterialDischargeType(10)),
                wm.Vertex(2, 5, wm.EVChargerType(50000)),
                wm.Vertex(3),
                wm.Vertex(4),
                wm.Vertex(5),
                wm.Vertex(6, 10, wm.MaterialLoadType(10)),
                wm.Vertex(7, 5, wm.EVChargerType(50000)),
            ]
        )
        .add_edges(
            [
                wm.Edge(wm.Vertex(0), wm.Vertex(2), 15000, 8),
                wm.Edge(wm.Vertex(2), wm.Vertex(3), 5000, 5),
                wm.Edge(wm.Vertex(3), wm.Vertex(2), 5000, 5),
                wm.Edge(wm.Vertex(3), wm.Vertex(0), 20000, 10),
                wm.Edge(wm.Vertex(0), wm.Vertex(3), 20000, 10),
                wm.Edge(wm.Vertex(3), wm.Vertex(1), 20000, 10),
                wm.Edge(wm.Vertex(1), wm.Vertex(0), 20000, 10),
                wm.Edge(wm.Vertex(2), wm.Vertex(4), 40000, 25),
                wm.Edge(wm.Vertex(4), wm.Vertex(3), 20000, 10),
                wm.Edge(wm.Vertex(3), wm.Vertex(4), 20000, 10),
                wm.Edge(wm.Vertex(4), wm.Vertex(5), 20000, 10),
                wm.Edge(wm.Vertex(5), wm.Vertex(4), 20000, 10),
                wm.Edge(wm.Vertex(5), wm.Vertex(7), 20000, 10),
                wm.Edge(wm.Vertex(7), wm.Vertex(5), 20000, 10),
                wm.Edge(wm.Vertex(7), wm.Vertex(6), 10000, 3),
                wm.Edge(wm.Vertex(6), wm.Vertex(5), 25000, 15),
            ]
        )
    )
