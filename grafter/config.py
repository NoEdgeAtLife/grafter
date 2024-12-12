from dataclasses import dataclass, field
from typing import Any

import yaml


@dataclass
class AppConfig:
    """Contains the entire configuration for the application."""

    data_source: dict[str, Any]
    features: dict[str, list[str]]
    event_triggers: dict[str, dict[str, Any]]
    feature_store: dict[str, Any]
    feature_config: "FeatureConfig" = field(init=False)
    event_trigger_config: "EventTriggerConfig" = field(init=False)
    feature_store_config: "FeatureStoreConfig" = field(init=False)

    def __post_init__(self):
        self.feature_config = FeatureConfig(self.features)
        self.event_trigger_config = EventTriggerConfig(self.event_triggers)
        self.feature_store_config = FeatureStoreConfig(**self.feature_store)

    @staticmethod
    def from_yaml(file_path: str) -> "AppConfig":
        with open(file_path) as file:
            config_data = yaml.safe_load(file)
        return AppConfig(**config_data)


@dataclass
class FeatureConfig:
    """
    FeatureConfig is a class that contains the configuration for the features and their dependencies.
    e.g.
    features:
      moving_average: [market_price]
      price_momentum: [market_price, moving_average]
    """

    features: dict[str, list[str]]


@dataclass
class EventTriggerConfig:
    """
    EventTriggerConfig is a class that contains the configuration for event triggers.
    e.g.
    event_triggers:
      daily:
        type: time
        interval: 10
        features: [moving_average, sentiment_momentum]
        last_trigger: {}
      price_change:
        type: condition
        condition: "abs(state['price_change']) > 0.05"
        features: [price_momentum]
    """

    event_triggers: dict[str, dict[str, Any]]


@dataclass
class FeatureStoreConfig:
    """
    Configuration for the feature store.

    This class holds the configuration details for the feature store, which is used to store
    and retrieve feature data. The `type` attribute specifies the type of the feature store
    (e.g., 'lmdb', 'redis', etc.), and the `config` attribute contains additional configuration
    parameters required for the specified feature store type.

    Attributes:
        type (str): The type of the feature store.
        config (dict[str, Any]): Additional configuration parameters for the feature store.
    """

    type: str
    config: dict[str, Any] = field(default_factory=dict)
