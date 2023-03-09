"""Unittest for edges"""

import watermelon as wm


def test_equality():
    """Test __eq__"""
    v1 = wm.Vertex(1, wm.EmptyVertexType())
    v2 = wm.Vertex(2, wm.EmptyVertexType())

    e1 = wm.Edge(v1, v2, 1)
    e2 = wm.Edge(v1, v2, 1)
    assert e1 == e2
    e1 = wm.Edge(v1, v2, 1, 10)
    e2 = wm.Edge(v1, v2, 1, 10)
    assert e1 == e2
    e1 = wm.Edge(v1, v2, 1)
    e2 = wm.Edge(v1, v2, 2)
    assert e1 != e2
    e1 = wm.Edge(v1, v2, 1, 10)
    e2 = wm.Edge(v1, v2, 1, 11)
    assert e1 != e2
    e1 = wm.Edge(v1, v2)
    e2 = wm.Edge(v2, v1)
    assert e1 != e2
    e1 = wm.Edge(v1, v1)
    e2 = wm.Edge(v1, v1)
    assert e1 == e2

    v1 = wm.Vertex(1, wm.EmptyVertexType())
    v2 = wm.Vertex("1", wm.EmptyVertexType())

    e1 = wm.Edge(v1, v2, 1)
    e2 = wm.Edge(v1, v2, 1)
    assert e1 == e2
    e1 = wm.Edge(v1, v2, 1, 10)
    e2 = wm.Edge(v1, v2, 1, 10)
    assert e1 == e2
    e1 = wm.Edge(v1, v2, 1)
    e2 = wm.Edge(v1, v2, 2)
    assert e1 != e2
    e1 = wm.Edge(v1, v2, 1, 10)
    e2 = wm.Edge(v1, v2, 1, 11)
    assert e1 != e2
    e1 = wm.Edge(v1, v2)
    e2 = wm.Edge(v2, v1)
    assert e1 != e2
    e1 = wm.Edge(v1, v1)
    e2 = wm.Edge(v1, v1)
    assert e1 == e2


def test_repr():
    """Test __repr__"""
    for i in range(10):
        v1 = wm.Vertex(i, wm.EmptyVertexType())
        v2 = wm.Vertex(i + 1, wm.EmptyVertexType())
        e1 = wm.Edge(v1, v2)
        e2 = wm.Edge(v1, v2, 10)
        e3 = wm.Edge(v1, v2, time=10)
        e4 = wm.Edge(v1, v2, 5, 6)
        assert (
            repr(e1)
            == f"Edge(origin=Vertex(identifier={i}, vertex_type=EmptyVertexType), \
target=Vertex(identifier={i + 1}, vertex_type=EmptyVertexType), weight=None, time=None)"
        )
        assert (
            repr(e2)
            == f"Edge(origin=Vertex(identifier={i}, vertex_type=EmptyVertexType), \
target=Vertex(identifier={i + 1}, vertex_type=EmptyVertexType), weight=10, time=None)"
        )
        assert (
            repr(e3)
            == f"Edge(origin=Vertex(identifier={i}, vertex_type=EmptyVertexType), \
target=Vertex(identifier={i + 1}, vertex_type=EmptyVertexType), weight=None, time=10)"
        )
        assert (
            repr(e4)
            == f"Edge(origin=Vertex(identifier={i}, vertex_type=EmptyVertexType), \
target=Vertex(identifier={i + 1}, vertex_type=EmptyVertexType), weight=5, time=6)"
        )


def test_str():
    """Test __str__"""
    for i in range(10):
        v1 = wm.Vertex(i, wm.EmptyVertexType())
        v2 = wm.Vertex(i + 1, wm.EmptyVertexType())
        e1 = wm.Edge(v1, v2)
        e2 = wm.Edge(v1, v2, 10)
        e3 = wm.Edge(v1, v2, time=10)
        e4 = wm.Edge(v1, v2, 5, 6)
        assert str(e1) == f"(\u0398({i})->\u0398({i + 1}); w=None, t=None)"
        assert str(e2) == f"(\u0398({i})->\u0398({i + 1}); w=10, t=None)"
        assert str(e3) == f"(\u0398({i})->\u0398({i + 1}); w=None, t=10)"
        assert str(e4) == f"(\u0398({i})->\u0398({i + 1}); w=5, t=6)"
