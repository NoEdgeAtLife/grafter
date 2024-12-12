import pytest

from grafter.feature_dag import FeatureGraph


@pytest.fixture
def feature_graph():
    return FeatureGraph()


def test_add_node(feature_graph):
    def mock_compute_func(data):
        return data["value"] * 2

    feature_graph.add_node("node1", mock_compute_func)
    assert "node1" in feature_graph.graph.nodes
    assert feature_graph.graph.nodes["node1"]["compute_func"] == mock_compute_func


def test_compute_features(feature_graph):
    def mock_compute_func1(data):
        return data["value"] * 2

    def mock_compute_func2(data):
        return data["value"] + 3

    feature_graph.add_node("node1", mock_compute_func1)
    feature_graph.add_node("node2", mock_compute_func2)
    feature_graph.add_edge("node1", "node2")

    input_data = {"ticker": "AAPL", "value": 5}
    result = feature_graph.compute_features(input_data)

    assert "timestamp" in result
    assert result["features"]["node1"] == 10
    assert result["features"]["node2"] == 8


def test_add_feature_dependencies(feature_graph):
    def mock_compute_func(data):
        return data["value"]

    feature_graph.add_node("node1", mock_compute_func)
    feature_graph.add_node("node2", mock_compute_func)
    feature_graph.add_node("node3", mock_compute_func)

    feature_graph.add_edge("node1", "node3")
    feature_graph.add_edge("node2", "node3")

    assert ("node1", "node3") in feature_graph.graph.edges
    assert ("node2", "node3") in feature_graph.graph.edges


def test_add_data_node(feature_graph):
    feature_graph.add_data_node("node1")
    assert "node1" in feature_graph.graph.nodes
    assert feature_graph.graph.nodes["node1"]["compute_func"] is None
