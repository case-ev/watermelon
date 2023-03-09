"""Unittest for vertices"""

import watermelon as wm


def test_equality():
    """Test __eq__"""
    v1 = wm.Vertex(1, wm.EmptyVertexType())
    v2 = wm.Vertex(1, wm.EmptyVertexType())
    assert v1 == v2
    assert v1 is v2

    v1 = wm.Vertex(2, wm.EmptyVertexType())
    v2 = wm.Vertex(2, wm.EmptyVertexType())
    assert v1 == v2
    assert v1 is v2

    # While they are of different types, they have the same
    # hash so they should be the same
    v1 = wm.Vertex(int(1), wm.EmptyVertexType())
    v2 = wm.Vertex(float(1), wm.EmptyVertexType())
    assert v1 == v2
    assert v1 is v2

    v1 = wm.Vertex(1, wm.EmptyVertexType())
    v2 = wm.Vertex(2, wm.EmptyVertexType())
    assert v1 != v2

    v1 = wm.Vertex("1", wm.EmptyVertexType())
    v2 = wm.Vertex(1, wm.EmptyVertexType())
    assert v1 != v2

    v1 = wm.Vertex("1", wm.EmptyVertexType())
    v2 = wm.Vertex(1, wm.EmptyVertexType())
    assert v1 != v2

    v1 = wm.Vertex("1", wm.EmptyVertexType())
    v2 = wm.Vertex("1", wm.EmptyVertexType())
    assert v1 == v2
    assert v1 is v2


def test_repr():
    """Test __repr__"""
    for i in range(10):
        v1 = wm.Vertex(i, wm.EmptyVertexType())
        v2 = wm.Vertex(str(i), wm.EmptyVertexType())
        assert repr(v1) == f"Vertex(identifier={i}, vertex_type=EmptyVertexType)"
        assert repr(v2) == f"Vertex(identifier='{i}', vertex_type=EmptyVertexType)"


def test_str():
    """Test __str__"""
    for i in range(10):
        v1 = wm.Vertex(i, wm.EmptyVertexType())
        v2 = wm.Vertex(str(i), wm.EmptyVertexType())
        assert str(v1) == f"\u0398({i})"
        assert str(v2) == f"\u0398({i})"
