"""Unittest for vertices"""

import watermelon as wm


def test_equality():
    """Test __eq__"""
    v1 = wm.Vertex(1, wm.EmptyVertexType())
    v2 = wm.Vertex(1, wm.EmptyVertexType())
    assert v1 == v2

    v1 = wm.Vertex(2, wm.EmptyVertexType())
    v2 = wm.Vertex(2, wm.EmptyVertexType())
    assert v1 == v2

    # While they are of different types, they have the same
    # hash so they should be the same
    v1 = wm.Vertex(int(1), wm.EmptyVertexType())
    v2 = wm.Vertex(float(1), wm.EmptyVertexType())
    assert v1 == v2

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


def test_repr():
    """Test __repr__"""
    for i in range(10):
        v1 = wm.Vertex(i, wm.EmptyVertexType())
        v2 = wm.Vertex(str(i), wm.EmptyVertexType())
        assert repr(v1) == f"Vertex(id={i}, type=EmptyVertexType)"
        assert repr(v2) == f"Vertex(id='{i}', type=EmptyVertexType)"


def test_str():
    """Test __str__"""
    for i in range(10):
        v1 = wm.Vertex(i, wm.EmptyVertexType())
        v2 = wm.Vertex(str(i), wm.EmptyVertexType())
        assert str(v1) == f"\u03b8({i})"
        assert str(v2) == f"\u03b8({i})"
