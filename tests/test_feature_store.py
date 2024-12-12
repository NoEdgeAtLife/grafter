import shutil
import tempfile

import pytest

from grafter.feature_store import InMemoryFeatureStore, LMDBFeatureStore


@pytest.fixture
def lmdb_feature_store():
    temp_dir = tempfile.mkdtemp()
    config = {"path": temp_dir}
    store = LMDBFeatureStore(config)
    yield store
    shutil.rmtree(temp_dir)


@pytest.fixture
def in_memory_feature_store():
    return InMemoryFeatureStore()


def test_lmdb_save_and_load_features(lmdb_feature_store):
    timestamp = 1234567890
    ticker = "AAPL"
    features = {"feature1": 1.0, "feature2": 2.0}

    lmdb_feature_store.save_features(timestamp, ticker, features)
    loaded_features = lmdb_feature_store.load_latest_features(ticker)

    assert loaded_features == features


def test_in_memory_save_and_load_features(in_memory_feature_store):
    timestamp = 1234567890
    ticker = "AAPL"
    features = {"feature1": 1.0, "feature2": 2.0}

    in_memory_feature_store.save_features(timestamp, ticker, features)
    loaded_features = in_memory_feature_store.load_latest_features(ticker)

    assert loaded_features == features


def test_lmdb_serialize_and_deserialize_features(lmdb_feature_store):
    features = {"feature1": 1.0, "feature2": 2.0}
    serialized = lmdb_feature_store.serialize_features(features)
    deserialized = lmdb_feature_store.deserialize_features(serialized)

    assert deserialized == features


def test_in_memory_serialize_and_deserialize_features(in_memory_feature_store):
    features = {"feature1": 1.0, "feature2": 2.0}
    serialized = in_memory_feature_store.serialize_features(features)
    deserialized = in_memory_feature_store.deserialize_features(serialized)

    assert deserialized == features


def test_lmdb_load_latest_features_empty(lmdb_feature_store):
    ticker = "AAPL"
    loaded_features = lmdb_feature_store.load_latest_features(ticker)

    assert loaded_features == {}


def test_in_memory_load_latest_features_empty(in_memory_feature_store):
    ticker = "AAPL"
    loaded_features = in_memory_feature_store.load_latest_features(ticker)

    assert loaded_features == {}


def test_lmdb_load_latest_features_multiple(lmdb_feature_store):
    ticker = "AAPL"
    features1 = {"feature1": 1.0, "feature2": 2.0}
    features2 = {"feature1": 3.0, "feature2": 4.0}

    lmdb_feature_store.save_features(1, ticker, features1)
    lmdb_feature_store.save_features(2, ticker, features2)
    loaded_features = lmdb_feature_store.load_latest_features(ticker)

    assert loaded_features == features2


def test_in_memory_load_latest_features_multiple(in_memory_feature_store):
    ticker = "AAPL"
    features1 = {"feature1": 1.0, "feature2": 2.0}
    features2 = {"feature1": 3.0, "feature2": 4.0}

    in_memory_feature_store.save_features(1, ticker, features1)
    in_memory_feature_store.save_features(2, ticker, features2)
    loaded_features = in_memory_feature_store.load_latest_features(ticker)

    assert loaded_features == features2


def test_lmdb_save_features_overwrite(lmdb_feature_store):
    ticker = "AAPL"
    features1 = {"feature1": 1.0, "feature2": 2.0}
    features2 = {"feature1": 3.0, "feature2": 4.0}

    lmdb_feature_store.save_features(1, ticker, features1)
    lmdb_feature_store.save_features(1, ticker, features2)
    loaded_features = lmdb_feature_store.load_latest_features(ticker)

    assert loaded_features == features2


def test_in_memory_save_features_overwrite(in_memory_feature_store):
    ticker = "AAPL"
    features1 = {"feature1": 1.0, "feature2": 2.0}
    features2 = {"feature1": 3.0, "feature2": 4.0}

    in_memory_feature_store.save_features(1, ticker, features1)
    in_memory_feature_store.save_features(1, ticker, features2)
    loaded_features = in_memory_feature_store.load_latest_features(ticker)

    assert loaded_features == features2
