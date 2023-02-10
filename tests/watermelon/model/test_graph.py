"""Unittest for graphs"""

import watermelon as wm


def test_get():
    """Test for getters and __getitem__"""
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

    for i in range(5):
        assert graph[i] is wm.Vertex(i)

    assert graph.neighbors(2) == [wm.Vertex(0), wm.Vertex(4)]
