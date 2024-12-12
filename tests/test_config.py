from tempfile import NamedTemporaryFile

import yaml

from grafter.config import AppConfig, EventTriggerConfig, FeatureConfig


def test_app_config_from_yaml():
    sample_config = {
        "data_source": {"type": "csv", "path": "sample_data.csv"},
        "features": {
            "moving_average": ["market_price"],
            "price_momentum": ["market_price", "moving_average"],
            "sentiment_momentum": ["sentiment_score"],
            "headline_sentiment": ["headline"],
            "text_sentiment": ["text_body"],
            "headline_sentiment_spread": ["sentiment_score", "headline_sentiment"],
            "text_sentiment_spread": ["text_sentiment", "headline_sentiment"],
        },
        "event_triggers": {
            "daily_1300": {"type": "time", "trigger_time": ["13:00"], "dependencies": ["price", "news_update"]},
            "price": {"type": "condition", "condition": "['price'] > 1"},
            "news_update": {"type": "condition", "condition": "['has_new_news']"},
        },
        "feature_store": {"type": "lmdb", "config": {"path": "/path/to/feature_store"}},
    }

    with NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        yaml.dump(sample_config, temp_file)
        temp_file_path = temp_file.name

    app_config = AppConfig.from_yaml(temp_file_path)

    assert app_config.data_source == sample_config["data_source"]
    assert app_config.features == sample_config["features"]
    assert app_config.event_triggers == sample_config["event_triggers"]
    assert app_config.feature_store == sample_config["feature_store"]

    assert isinstance(app_config.feature_config, FeatureConfig)
    assert app_config.feature_config.features == sample_config["features"]

    assert isinstance(app_config.event_trigger_config, EventTriggerConfig)
    assert app_config.event_trigger_config.event_triggers == sample_config["event_triggers"]
