from unittest.mock import MagicMock, patch

import pytest

from grafter.config import EventTriggerConfig, FeatureConfig, FeatureStoreConfig
from grafter.feature_store import InMemoryFeatureStore
from grafter.graph_manager import GraphManager
from grafter.state_manager import StateManager


@pytest.fixture
def feature_config():
    return FeatureConfig(features={"feature1": ["dependency1", "dependency2"], "feature2": ["dependency3"]})


@pytest.fixture
def event_trigger_config():
    return EventTriggerConfig(
        event_triggers={
            "event1": {"trigger_type": "type1"},
            "event2": {"trigger_type": "type2", "dependencies": ["event1"]},
        }
    )


@pytest.fixture
def state_manager():
    mock_state_manager = MagicMock(spec=StateManager)
    mock_state_manager.get_state.return_value = {"timestamp": 1234567890, "ticker": "AAPL", "state_data": {}}
    return mock_state_manager


@pytest.fixture
def feature_store_config():
    return FeatureStoreConfig(type="in_memory")


@pytest.fixture
def mock_feature_computer():
    mock_computer = MagicMock()
    mock_computer._compute_feature1.return_value = 1.0
    mock_computer._compute_feature2.return_value = 2.0
    return mock_computer


@pytest.fixture
def graph_manager(feature_config, event_trigger_config, state_manager, feature_store_config, mock_feature_computer):
    with patch("grafter.graph_manager.FeatureComputer", return_value=mock_feature_computer):
        return GraphManager(feature_config, event_trigger_config, state_manager, feature_store_config)


def test_init_feature_store(graph_manager):
    assert isinstance(graph_manager.feature_store, InMemoryFeatureStore)


def test_build_feature_graph(graph_manager):
    assert "feature1" in graph_manager.feature_graph.graph.nodes
    assert "feature2" in graph_manager.feature_graph.graph.nodes
    assert ("dependency1", "feature1") in graph_manager.feature_graph.graph.edges
    assert ("dependency2", "feature1") in graph_manager.feature_graph.graph.edges
    assert ("dependency3", "feature2") in graph_manager.feature_graph.graph.edges
    assert graph_manager.feature_graph.graph.nodes["feature1"]["compute_func"] is not None
    assert graph_manager.feature_graph.graph.nodes["feature2"]["compute_func"] is not None
    assert graph_manager.feature_graph.graph.nodes["feature2"]["compute_func"]() == 2.0


def test_build_event_trigger_graph(graph_manager):
    assert "event1" in graph_manager.event_trigger_graph.graph.nodes
    assert "event2" in graph_manager.event_trigger_graph.graph.nodes
    assert ("event1", "event2") in graph_manager.event_trigger_graph.graph.edges
