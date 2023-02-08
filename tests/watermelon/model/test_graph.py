import watermelon as wm


# \u03b8 theta


class TestVertex:
    def test_equality(self):
        v1 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        assert v1 == v2

        v1 = wm.Vertex(2, wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(2, wm.EMPTY_VERTEX_TYPE)
        assert v1 == v2

        # While they are of different types, they have the same
        # hash so they should be the same
        v1 = wm.Vertex(int(1), wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(float(1), wm.EMPTY_VERTEX_TYPE)
        assert v1 == v2

        v1 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(2, wm.EMPTY_VERTEX_TYPE)
        assert v1 != v2

        v1 = wm.Vertex("1", wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        assert v1 != v2

        v1 = wm.Vertex("1", wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        assert v1 != v2

        v1 = wm.Vertex("1", wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex("1", wm.EMPTY_VERTEX_TYPE)
        assert v1 == v2

    def test_repr(self):
        for i in range(10):
            v1 = wm.Vertex(i, wm.EMPTY_VERTEX_TYPE)
            v2 = wm.Vertex(str(i), wm.EMPTY_VERTEX_TYPE)
            assert repr(v1) == f"Vertex(id={i}, type=EMPTY_VERTEX_TYPE)"
            assert repr(v2) == f"Vertex(id='{i}', type=EMPTY_VERTEX_TYPE)"

    def test_str(self):
        for i in range(10):
            v1 = wm.Vertex(i, wm.EMPTY_VERTEX_TYPE)
            v2 = wm.Vertex(str(i), wm.EMPTY_VERTEX_TYPE)
            assert str(v1) == f"\u03b8({i})"
            assert str(v2) == f"\u03b8({i})"


class TestEdge:
    def test_equality(self):
        v1 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex(2, wm.EMPTY_VERTEX_TYPE)

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

        v1 = wm.Vertex(1, wm.EMPTY_VERTEX_TYPE)
        v2 = wm.Vertex("1", wm.EMPTY_VERTEX_TYPE)

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

    def test_repr(self):
        for i in range(10):
            v1 = wm.Vertex(i, wm.EMPTY_VERTEX_TYPE)
            v2 = wm.Vertex(i + 1, wm.EMPTY_VERTEX_TYPE)
            e1 = wm.Edge(v1, v2)
            e2 = wm.Edge(v1, v2, 10)
            e3 = wm.Edge(v1, v2, time=10)
            e4 = wm.Edge(v1, v2, 5, 6)
            assert repr(e1) == f"Edge(origin=Vertex(id={i}, type=EMPTY_VERTEX_TYPE), target=Vertex(id={i + 1}, type=EMPTY_VERTEX_TYPE), weight=None, time=None)"
            assert repr(e2) == f"Edge(origin=Vertex(id={i}, type=EMPTY_VERTEX_TYPE), target=Vertex(id={i + 1}, type=EMPTY_VERTEX_TYPE), weight=10, time=None)"
            assert repr(e3) == f"Edge(origin=Vertex(id={i}, type=EMPTY_VERTEX_TYPE), target=Vertex(id={i + 1}, type=EMPTY_VERTEX_TYPE), weight=None, time=10)"
            assert repr(e4) == f"Edge(origin=Vertex(id={i}, type=EMPTY_VERTEX_TYPE), target=Vertex(id={i + 1}, type=EMPTY_VERTEX_TYPE), weight=5, time=6)"

    def test_str(self):
        for i in range(10):
            v1 = wm.Vertex(i, wm.EMPTY_VERTEX_TYPE)
            v2 = wm.Vertex(i + 1, wm.EMPTY_VERTEX_TYPE)
            e1 = wm.Edge(v1, v2)
            e2 = wm.Edge(v1, v2, 10)
            e3 = wm.Edge(v1, v2, time=10)
            e4 = wm.Edge(v1, v2, 5, 6)
            assert str(e1) == f"(\u03b8({i})->\u03b8({i + 1}); w=None, t=None)"
            assert str(e2) == f"(\u03b8({i})->\u03b8({i + 1}); w=10, t=None)"
            assert str(e3) == f"(\u03b8({i})->\u03b8({i + 1}); w=None, t=10)"
            assert str(e4) == f"(\u03b8({i})->\u03b8({i + 1}); w=5, t=6)"
