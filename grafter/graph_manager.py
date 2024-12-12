from grafter.config import EventTriggerConfig, FeatureConfig, FeatureStoreConfig
from grafter.event_trigger_dag import EventTriggerGraph
from grafter.feature_computer import FeatureComputer
from grafter.feature_dag import FeatureGraph
from grafter.feature_store import FeatureStore, InMemoryFeatureStore, LMDBFeatureStore
from grafter.state_manager import StateManager


class GraphManager:
    def __init__(
        self,
        feature_config: FeatureConfig,
        event_trigger_config: EventTriggerConfig,
        state_manager: StateManager,
        feature_store_config: FeatureStoreConfig,
    ):
        self.feature_graph = FeatureGraph()
        self.event_trigger_graph = EventTriggerGraph()
        self.feature_computer = FeatureComputer()
        self.feature_config = feature_config
        self.event_trigger_config = event_trigger_config
        self.state_manager = state_manager
        self.feature_store = self._init_feature_store(feature_store_config)

        self._validate_feature_methods()
        self._build_feature_graph()
        self._build_event_trigger_graph()

    def _init_feature_store(self, config: FeatureStoreConfig) -> FeatureStore:
        if config.type == "in_memory":
            return InMemoryFeatureStore()
        elif config.type == "lmdb":
            return LMDBFeatureStore(config.config)
        else:
            raise ValueError(f"Invalid feature store type: {config.type}")

    def _build_feature_graph(self):
        for feature, dependencies in self.feature_config.features.items():
            compute_method = getattr(self.feature_computer, f"_compute_{feature}", None)
            self.feature_graph.add_node(feature, compute_method)
            for dependency in dependencies:
                if dependency not in self.feature_config.features:
                    self.feature_graph.add_data_node(dependency)
                self.feature_graph.add_edge(dependency, feature)

    def _build_event_trigger_graph(self):
        for event, config in self.event_trigger_config.event_triggers.items():
            self.event_trigger_graph.add_event_trigger(
                event, config.get("trigger_type"), config.get("condition"), config.get("interval")
            )
            for dependency in config.get("dependencies", []):
                self.event_trigger_graph.add_edge(dependency, event)

    def _validate_feature_methods(self):
        for feature in self.feature_config.features:
            if not hasattr(self.feature_computer, f"_compute_{feature}"):
                raise AttributeError(f"FeatureComputer is missing method for feature: {feature}")

    def is_triggered(self, ticker) -> bool:
        current_state = self.state_manager.get_state(ticker)
        return self.event_trigger_graph.check_triggers(current_state)

    def compute_features(self, ticker):
        current_state = self.state_manager.get_state(ticker)
        features = self.feature_graph.compute_features(current_state)
        self.feature_store.save_features(features["timestamp"], ticker, features["features"])

    async def on_update(self, data: dict):
        if data is not None:
            await self.state_manager.update_state(**data)
            ticker = data["ticker"]
        if self.is_triggered(ticker):
            self.compute_features(ticker)
