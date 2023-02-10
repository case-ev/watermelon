"""Unittest for agents"""

import watermelon as wm


EMPTY_GRAPH = wm.Graph()


def test_id():
    """Test whether singletons are working"""
    agent1 = wm.Agent(1, EMPTY_GRAPH)
    agent2 = wm.Agent(1, EMPTY_GRAPH)
    assert agent1 == agent2
    assert agent1 is agent2
