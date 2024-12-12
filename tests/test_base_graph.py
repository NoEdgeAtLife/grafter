import pytest

from grafter.base_graph import BaseGraph


def test_add_node():
    graph = BaseGraph()
    graph.add_node("A")
    assert "A" in graph.graph.nodes


def test_add_node_with_attributes():
    graph = BaseGraph()
    graph.add_node("A", color="red")
    assert graph.graph.nodes["A"]["color"] == "red"


def test_add_edge():
    graph = BaseGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B")
    assert ("A", "B") in graph.graph.edges


def test_add_edge_creates_cycle():
    graph = BaseGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    with pytest.raises(ValueError, match="cycle"):
        graph.add_edge("C", "A")


def test_add_edge_no_cycle():
    graph = BaseGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B")
    assert ("A", "B") in graph.graph.edges
    assert not graph.graph.has_edge("B", "A")
